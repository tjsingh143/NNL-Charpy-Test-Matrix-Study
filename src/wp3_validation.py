"""WP3 - Fitter validation on SYNTHETIC curves with known truth (no published measurement is used anywhere in this file).

Every curve here is generated from a known tanh curve plus controlled random scatter, fitted with src/wp3_fitter.py, and compared
with the truth. Nothing produced here is, or may be mixed with, published Charpy data; every output file name starts with
'synthetic_' and every table carries a data_type column saying SYNTHETIC.

Order (DECISIONS.md D-042, D-048):
  1. Block L compares the four lower-shelf strategies on the same synthetic data sets and applies the decision rule written in
     choose_lse_strategy() before any result existed. LOCKED_LSE_STRATEGY records the outcome; the run stops if the rule ever
     gives a different answer, so the choice cannot drift silently.
  2. Blocks A-D validate the locked strategy across sampling density, sampling pattern, parameter values, noise and a fixed test
     window, including designs expected to fail.

Outputs (outputs/wp3/): synthetic_validation_design.csv, synthetic_validation_replicates.csv.gz, synthetic_validation_metrics.csv,
synthetic_lse_strategy_comparison.csv, synthetic_lse_strategy_rule.md, synthetic_flag_check.csv, synthetic_trust_limits.csv,
synthetic_*.png. Fixed seed SEED; results are identical for any number of worker processes.

Run:  .venv/bin/python src/wp3_validation.py
"""
from __future__ import annotations

import hashlib
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from common import OUTPUTS, md_table, write_text
from wp3_fitter import (CRITERION_J, LSE_STRATEGIES, OUTCOMES, classify, criterion_temperature, fit_curve, index_temperature,
                        lse_setting, tanh_energy)

OUT = OUTPUTS / "wp3"
DATA_TYPE = "SYNTHETIC (fitter validation; not published measurements)"
SEED = 20260913
REPLICATES = 200

# D-048. Controlled, uncalibrated synthetic scatter (NOT the WP4 scatter model). Standard deviation at temperature T:
#   sd(T) = sigma_T * |dE/dT| + cv * E(T) + 3 * cv * LSE
# term 1 grows with the steepness of the curve, as if each specimen's transition were shifted by a few degrees (scatter peaks at
# mid-transition, as Marini 2020 §3.1 describes); term 2 scales with the energy; term 3 keeps lower-shelf energies from being
# unrealistically precise. Gaussian; an energy drawn below 0 J is set to 0 J and counted. The mean curve is exactly the truth.
NOISE = {"zero": (0.0, 0.0), "low": (2.0, 0.03), "moderate": (5.0, 0.06), "high": (10.0, 0.12)}  # (sigma_T in °C, cv)

REFERENCE_FULL = dict(lse=5.0, use=150.0, t0=0.0, c=30.0)
# Reference scales used only to summarise errors (not acceptance criteria), D-048: 10 °C for T41J and T0 (about the 17 °F
# = 9.4 °C base-metal scatter limit for credible surveillance shifts in 10 CFR 50.61(c)(2)(i)(C)); 10 % for USE; 25 % for C.
REF_TEMPERATURE_C, REF_USE_REL, REF_C_REL = 10.0, 0.10, 0.25

# D-042. Filled in only after Block L was run with the rule below (None = run Block L and stop).
LOCKED_LSE_STRATEGY = None


# ---------------------------------------------------------------------------
# 1. Scenarios
# ---------------------------------------------------------------------------
def _x(values) -> tuple:
    return ("x", tuple(float(v) for v in values))


def build_scenarios() -> list:
    """One dict per scenario: block, design, truth, noise, lower-shelf strategy, temperature specification."""
    rows = []

    def add(block, design, spec, truth, noise, scale="full-size", strategy=None, replicates=None):
        rows.append(dict(block=block, design=design, spec=spec, scale=scale, noise=noise, lse_strategy=strategy,
                         replicates=1 if noise == "zero" else (replicates or REPLICATES),
                         lse_true=truth["lse"], use_true=truth["use"], t0_true=truth["t0"], c_true=truth["c"]))

    # Block L: lower-shelf strategies on common synthetic data (low, moderate and high scatter).
    l_designs = [("uniform x -3..3, n=12 (lower shelf well sampled)", _x(np.linspace(-3, 3, 12))),
                 ("x -1.5..3, n=12 (lower shelf weak)", _x(np.linspace(-1.5, 3, 12))),
                 ("x -0.5..3, n=12 (lower shelf missing)", _x(np.linspace(-0.5, 3, 12))),
                 ("window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf)", ("window", 12, 250.0, "T0", -60.0)),
                 ("window 250 °C, n=12, T0 60 °C below centre (cold end near transition)", ("window", 12, 250.0, "T0", 60.0))]
    l_truths = [("full-size", dict(lse=v, use=150.0, t0=0.0, c=30.0)) for v in (2.0, 5.0, 10.0)]
    l_truths += [("miniature", dict(lse=r * u, use=u, t0=0.0, c=30.0)) for u in (1.0, 8.0) for r in (0.01, 0.06, 0.12)]
    for scale, truth in l_truths:
        for design, spec in l_designs:
            for noise in ("low", "moderate", "high"):
                for strategy in LSE_STRATEGIES:
                    add("L", design, spec, truth, noise, scale, strategy)
    if LOCKED_LSE_STRATEGY is None:
        return rows
    s = LOCKED_LSE_STRATEGY
    noises = ["zero", "low", "moderate", "high"]
    # Block A: sampling density (uniform over both shelves and the transition).
    for n in (6, 8, 12, 18, 30):
        for noise in noises:
            add("A", f"uniform x -3..3, n={n}", _x(np.linspace(-3, 3, n)), REFERENCE_FULL, noise, strategy=s)
    # Block B: sampling patterns.
    shelves = [-3.5, -3.0, -2.5, 2.5, 3.0, 3.5]
    patterns = [("shelves only, 0 transition points (n=6)", _x(shelves)),
                ("shelves + 1 transition point (n=7)", _x(shelves + [0.0])),
                ("shelves + 2 transition points (n=8)", _x(shelves + [-0.5, 0.5])),
                ("shelves + 3 transition points (n=9)", _x(shelves + [-0.7, 0.0, 0.7])),
                ("x -1.5..3, n=12 (lower shelf weak)", _x(np.linspace(-1.5, 3, 12))),
                ("x -0.5..3, n=12 (lower shelf missing)", _x(np.linspace(-0.5, 3, 12))),
                ("x -3..1.5, n=12 (upper shelf weak)", _x(np.linspace(-3, 1.5, 12))),
                ("x -3..0.5, n=12 (upper shelf missing)", _x(np.linspace(-3, 0.5, 12))),
                ("clustered at centre: 2+2 shelf points, 8 in |x|<=0.5 (n=12)", _x([-3, -3, 3, 3] + list(np.linspace(-0.5, 0.5, 8)))),
                ("clustered cold side: x -3..-0.5, n=12", _x(np.linspace(-3, -0.5, 12))),
                ("5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15)", _x(np.repeat([-2.5, -1.0, 0.0, 1.0, 2.5], 3)))]
    for design, spec in patterns:
        for noise in noises:
            add("B", design, spec, REFERENCE_FULL, noise, strategy=s)
    # Block C: parameter values (one at a time around the reference), moderate scatter.
    for label, change in [("USE 44 J (41 J near upper shelf)", dict(use=44.0)), ("USE 70 J", dict(use=70.0)),
                          ("USE 250 J", dict(use=250.0)), ("LSE 2 J", dict(lse=2.0)), ("LSE 10 J", dict(lse=10.0)),
                          ("C 12 °C (narrow)", dict(c=12.0)), ("C 60 °C (broad)", dict(c=60.0))]:
        for design, spec in [("uniform x -3..3, n=12", _x(np.linspace(-3, 3, 12))),
                             ("5 temperatures x 3 specimens (n=15)", _x(np.repeat([-2.5, -1.0, 0.0, 1.0, 2.5], 3)))]:
            add("C", f"{label}; {design}", spec, {**REFERENCE_FULL, **change}, "moderate", strategy=s)
    # Block D: a fixed test window planned without knowing T0 (cohort 10th percentile / median / 90th percentile of points and span).
    for n, span in [(9, 150.0), (12, 250.0), (24, 360.0)]:
        for t0 in (-60.0, 0.0, 60.0):
            for c in (12.0, 30.0, 60.0):
                add("D", f"window {span:g} °C, n={n}; true T0 {t0:+g} °C from centre; true C {c:g} °C", ("window", n, span, "absolute", 0.0),
                    {**REFERENCE_FULL, "t0": t0, "c": c}, "moderate", strategy=s)
    return rows


def temperatures(spec, truth: dict) -> np.ndarray:
    if spec[0] == "x":
        return truth["t0"] + truth["c"] * np.asarray(spec[1], float)
    _, n, span, reference, value = spec  # centre at truth T0 + value ("T0") or at the absolute temperature value ("absolute")
    centre = truth["t0"] + value if reference == "T0" else value
    return centre + np.linspace(-span / 2.0, span / 2.0, n)


def data_key(sc: dict) -> str:
    """Identifies the synthetic data (not the strategy), so strategies are compared on identical data (common random numbers)."""
    return "|".join(str(sc[k]) for k in ["block", "design", "scale", "noise", "lse_true", "use_true", "t0_true", "c_true"])


def synthetic_energies(t: np.ndarray, truth: dict, noise: str, rng) -> tuple:
    sigma_t, cv = NOISE[noise]
    mean = tanh_energy(t, **truth)
    slope = 0.5 * (truth["use"] - truth["lse"]) / truth["c"] * (1.0 - np.tanh((t - truth["t0"]) / truth["c"]) ** 2)
    sd = sigma_t * slope + cv * mean + 3.0 * cv * truth["lse"]
    e = mean + sd * rng.standard_normal(len(t))
    return np.where(e < 0, 0.0, e), int(np.sum(e < 0))


# ---------------------------------------------------------------------------
# 2. Running one scenario
# ---------------------------------------------------------------------------
def run_scenario(sc: dict) -> list:
    truth = dict(lse=sc["lse_true"], use=sc["use_true"], t0=sc["t0_true"], c=sc["c_true"])
    t = temperatures(sc["spec"], truth)
    criterion = CRITERION_J[sc["scale"]]
    t41_true = criterion_temperature(**truth, e_crit=criterion)[0] if criterion else np.nan
    seed = int(hashlib.sha256(data_key(sc).encode()).hexdigest()[:15], 16)
    rng = np.random.default_rng(np.random.SeedSequence([SEED, seed]))
    rows = []
    for rep in range(sc["replicates"]):
        e, n_clipped = synthetic_energies(t, truth, sc["noise"], rng)
        lse_fixed = lse_setting(sc["lse_strategy"], sc["scale"], t, e)
        fit = fit_curve(t, e, lse_fixed)
        t41, index_status = index_temperature(fit, t, criterion)
        cls = classify(fit, index_status)
        row = dict(scenario_id=sc["scenario_id"], replicate=rep, n_clipped_at_zero=n_clipped, lse_mode=fit["lse_mode"],
                   outcome=cls["outcome"], outcome_reason=cls["outcome_reason"], index_status=index_status, t41_c=t41,
                   **{k: v for k, v in cls.items() if k.startswith("flag_")})
        if fit.get("optimizer_success"):
            t41_any = criterion_temperature(fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"], criterion)[0] if criterion else np.nan
            row.update(lse_j=fit["lse_j"], use_j=fit["use_j"], t0_c=fit["t0_c"], c_c=fit["c_c"], t41_analytic_c=t41_any,
                       use_support=fit["use_support"], lse_support=fit["lse_support"], n_T_transition_fit=fit["n_T_transition_fit"],
                       jacobian_condition_number=fit["jacobian_condition_number"],
                       t0_spread_within_1pct_of_best_cost_c=fit["t0_spread_within_1pct_of_best_cost_c"],
                       err_lse_j=fit["lse_j"] - truth["lse"], err_use_rel=fit["use_j"] / truth["use"] - 1.0,
                       err_t0_c=fit["t0_c"] - truth["t0"], err_c_rel=fit["c_c"] / truth["c"] - 1.0,
                       err_t41_c=t41 - t41_true, err_t41_analytic_c=t41_any - t41_true)
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# 3. Summaries
# ---------------------------------------------------------------------------
def error_stats(x: pd.Series, prefix: str, reference: float) -> dict:
    x = x.dropna()
    if len(x) == 0:
        return {f"{prefix}_n": 0}
    a = x.abs()
    return {f"{prefix}_n": len(x), f"{prefix}_bias": x.mean(), f"{prefix}_sd": x.std(ddof=1) if len(x) > 1 else 0.0,
            f"{prefix}_rmse": float(np.sqrt(np.mean(x ** 2))), f"{prefix}_median_abs": a.median(),
            f"{prefix}_p90_abs": a.quantile(0.9), f"{prefix}_share_within_reference": float((a <= reference).mean())}


USABLE = OUTCOMES[4:]


def scenario_metrics(design: pd.DataFrame, reps: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for sid, g in reps.groupby("scenario_id", sort=False):
        m = dict(scenario_id=sid, replicates=len(g), clipped_energies_per_replicate=g["n_clipped_at_zero"].mean())
        for o in OUTCOMES:
            m[f"share_{o}"] = float((g["outcome"] == o).mean())
        for k in [c for c in g.columns if c.startswith("flag_")]:
            m[f"share_{k}"] = float(g[k].mean())
        m["share_index_calculated"] = float((g["index_status"] == "calculated").mean())
        usable = g[g["outcome"].isin(USABLE)]
        for subset, h in [("all", g), ("usable", usable)]:
            m.update(error_stats(h.get("err_t0_c", pd.Series(dtype=float)), f"{subset}_t0", REF_TEMPERATURE_C))
            m.update(error_stats(h.get("err_t41_c", pd.Series(dtype=float)), f"{subset}_t41", REF_TEMPERATURE_C))
            m.update(error_stats(h.get("err_use_rel", pd.Series(dtype=float)), f"{subset}_use_rel", REF_USE_REL))
            m.update(error_stats(h.get("err_c_rel", pd.Series(dtype=float)), f"{subset}_c_rel", REF_C_REL))
            m.update(error_stats(h.get("err_lse_j", pd.Series(dtype=float)), f"{subset}_lse_j", np.inf))
        m.update(error_stats(g.get("err_t41_analytic_c", pd.Series(dtype=float)), "all_t41_analytic", REF_TEMPERATURE_C))
        rows.append(m)
    return design.merge(pd.DataFrame(rows), on="scenario_id", how="left")


def choose_lse_strategy(block_l: pd.DataFrame) -> tuple:
    """Decision rule for the lower shelf, written before Block L was run (D-042).
    Key temperature = T41J from the analytic crossing (full-size truths) or T0 (miniature truths), so that no strategy is
    judged on an easier subset. Per data set and strategy: P90 of |error| over replicates, and the share of replicates in which
    the key temperature could not be obtained (optimizer failure or criterion not crossed). Score = mean P90 over data sets.
      1. A strategy is eligible if its mean missing share is at most 5 percentage points above the lowest.
      2. The eligible strategy with the lowest score wins if its score is at least 10 % below every other eligible score.
      3. Otherwise 'fitted' is chosen if its score is within that 10 % of the lowest (no externally imposed value; the sourced
         fixed values contradict measured lowest energies for some geometries of the cohort), else the lowest score."""
    rows = []
    for (key, strategy), g in block_l.groupby(["data_key", "lse_strategy"], sort=False):
        err = g["err_t41_analytic_c"] if g["scale"].iloc[0] == "full-size" else g["err_t0_c"]
        rows.append(dict(data_key=key, lse_strategy=strategy, scale=g["scale"].iloc[0], p90_abs_key_temperature_c=err.abs().quantile(0.9),
                         median_abs_key_temperature_c=err.abs().median(), missing_share=float(err.isna().mean())))
    per = pd.DataFrame(rows)
    summary = per.groupby("lse_strategy", sort=False).agg(score_mean_p90_c=("p90_abs_key_temperature_c", "mean"),
                                                          mean_missing_share=("missing_share", "mean")).reindex(LSE_STRATEGIES)
    for scale in ["full-size", "miniature"]:
        summary[f"score_{scale}_c"] = per[per["scale"] == scale].groupby("lse_strategy")["p90_abs_key_temperature_c"].mean()
    eligible = summary[summary["mean_missing_share"] <= summary["mean_missing_share"].min() + 0.05]
    best = eligible["score_mean_p90_c"].idxmin()
    others = eligible.drop(index=best)["score_mean_p90_c"]
    if len(others) == 0 or (eligible.loc[best, "score_mean_p90_c"] <= 0.9 * others).all():
        choice, reason = best, "rule 2: lowest score, at least 10 % below every other eligible strategy"
    elif "fitted" in eligible.index and eligible.loc["fitted", "score_mean_p90_c"] < eligible.loc[best, "score_mean_p90_c"] / 0.9:
        choice, reason = "fitted", "rule 3: no strategy at least 10 % better; 'fitted' within 10 % of the lowest score"
    else:
        choice, reason = best, "rule 3: no strategy at least 10 % better; 'fitted' not within 10 % of the lowest, lowest score chosen"
    summary["eligible"] = summary.index.isin(eligible.index)
    return choice, reason, summary.reset_index(), per


# ---------------------------------------------------------------------------
# 4. Driver
# ---------------------------------------------------------------------------
def run_all(scenarios: list) -> pd.DataFrame:
    workers = max(1, min(8, os.cpu_count() or 1))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        chunks = list(pool.map(run_scenario, scenarios, chunksize=1))
    return pd.DataFrame([row for chunk in chunks for row in chunk])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    scenarios = build_scenarios()
    for i, sc in enumerate(scenarios):
        sc["scenario_id"] = f"S{i + 1:03d}"
    design = pd.DataFrame([{k: v for k, v in sc.items() if k != "spec"} | dict(
        temperatures_c=" ".join(f"{v:.4g}" for v in temperatures(sc["spec"], dict(lse=sc["lse_true"], use=sc["use_true"],
                                                                                   t0=sc["t0_true"], c=sc["c_true"]))),
        data_key=data_key(sc)) for sc in scenarios])
    design.insert(0, "data_type", DATA_TYPE)
    reps = run_all(scenarios)
    block_l = reps.merge(design[["scenario_id", "data_key", "lse_strategy", "scale"]], on="scenario_id")
    block_l = block_l[block_l["scenario_id"].isin(design.loc[design["block"] == "L", "scenario_id"])]
    choice, reason, summary, per = choose_lse_strategy(block_l)
    print(f"Lower-shelf rule (Block L): {choice} ({reason})")
    print(summary.to_string(index=False))
    summary.insert(0, "data_type", DATA_TYPE)
    per.insert(0, "data_type", DATA_TYPE)
    summary.to_csv(OUT / "synthetic_lse_strategy_comparison.csv", index=False)
    per.to_csv(OUT / "synthetic_lse_strategy_per_dataset.csv", index=False)
    if LOCKED_LSE_STRATEGY is None:
        print("LOCKED_LSE_STRATEGY is not set: Block L only. Record the decision in DECISIONS.md, set it, and rerun.")
        return
    if choice != LOCKED_LSE_STRATEGY:
        raise RuntimeError(f"The lower-shelf decision rule now selects {choice!r}, but {LOCKED_LSE_STRATEGY!r} is locked (D-042).")


if __name__ == "__main__":
    main()
