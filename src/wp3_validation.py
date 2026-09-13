"""WP3 - Fitter validation on SYNTHETIC curves with known truth (no published measurement is used anywhere in this file).

Every curve here is generated from a known tanh curve plus controlled random scatter, fitted with src/wp3_fitter.py, and compared
with the truth. Nothing produced here is, or may be mixed with, published Charpy data; every output file name starts with
'synthetic_' and every table carries a data_type column saying SYNTHETIC.

Order (DECISIONS.md D-042, D-048):
  1. Block L compares the four lower-shelf strategies on the same synthetic data sets and applies the decision rule written in
     choose_lse_strategy() before any result existed. LOCKED_LSE_STRATEGY records the outcome; the run stops if the rule ever
     gives a different answer, so the choice cannot drift silently.
  2. Blocks A-D validate the locked strategy across sampling density, sampling pattern, parameter values, noise and a fixed test
     window, including designs expected to fail. Block E (non-flat upper shelves) was added after A-D had been run, to test the
     upper-shelf trend flag, whose role changed as a result (D-047).

Outputs (outputs/wp3/): synthetic_validation_design.csv, synthetic_validation_replicates_blocks_A-E.csv.gz, synthetic_validation_metrics.csv,
synthetic_lse_strategy_comparison.csv, synthetic_lse_strategy_per_dataset.csv, synthetic_lse_strategy_rule.md,
synthetic_flag_check.csv, synthetic_trust_limits.csv, synthetic_nonflat_upper_shelf_check.csv,
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
from wp3_fitter import (CRITERION_J, LSE_STRATEGIES, OUTCOMES, classify, criterion_temperature, fit_curve, index_fraction_of_rise,
                        index_temperature, lse_setting, tanh_energy)

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
LOCKED_LSE_STRATEGY = "fitted"  # Block L outcome under the pre-registered rule (rule 3), recorded in D-042


# ---------------------------------------------------------------------------
# 1. Scenarios
# ---------------------------------------------------------------------------
def _x(values) -> tuple:
    return ("x", tuple(float(v) for v in values))


def build_scenarios() -> list:
    """One dict per scenario: block, design, truth, noise, lower-shelf strategy, temperature specification."""
    rows = []

    def add(block, design, spec, truth, noise, scale="full-size", strategy=None, replicates=None, shelf_slope=0.0):
        rows.append(dict(block=block, design=design, spec=spec, scale=scale, noise=noise, lse_strategy=strategy,
                         replicates=1 if noise == "zero" else (replicates or REPLICATES),
                         lse_true=truth["lse"], use_true=truth["use"], t0_true=truth["t0"], c_true=truth["c"], shelf_slope=shelf_slope))

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
    # Block E (added after Blocks A-D had been run, D-047): upper shelves that are NOT flat, which a tanh cannot represent. Above
    # x = 1.5 the true energy changes linearly by `shelf_slope` x USE per 100 °C (negative: falling, as ref 104 is described in D-037).
    # Tests whether the upper-shelf trend flag detects them and how far the fitted USE is pulled.
    for slope in (-0.20, -0.10, 0.10):
        for design, spec in [("uniform x -3..5, n=12 (upper shelf sampled to x = 5)", _x(np.linspace(-3, 5, 12))),
                             ("x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15)", _x(np.repeat([-2.5, -1.0, 0.0, 2.0, 4.0], 3)))]:
            for noise in ("low", "moderate"):
                add("E", f"upper shelf {100 * slope:+g} % of USE per 100 °C; {design}", spec, REFERENCE_FULL, noise, strategy=s,
                    shelf_slope=slope)
    return rows


def temperatures(spec, truth: dict) -> np.ndarray:
    if spec[0] == "x":
        return truth["t0"] + truth["c"] * np.asarray(spec[1], float)
    _, n, span, reference, value = spec  # centre at truth T0 + value ("T0") or at the absolute temperature value ("absolute")
    centre = truth["t0"] + value if reference == "T0" else value
    return centre + np.linspace(-span / 2.0, span / 2.0, n)


def data_key(sc: dict) -> str:
    """Identifies the synthetic data (not the strategy), so strategies are compared on identical data (common random numbers)."""
    key = "|".join(str(sc[k]) for k in ["block", "design", "scale", "noise", "lse_true", "use_true", "t0_true", "c_true"])
    return key if sc.get("shelf_slope", 0.0) == 0.0 else f"{key}|shelf_slope={sc['shelf_slope']}"


def true_energy(t: np.ndarray, truth: dict, shelf_slope: float = 0.0) -> np.ndarray:
    """Mean synthetic energy: the tanh, plus (Block E only) a linear change of shelf_slope x USE per 100 °C above x = 1.5."""
    t_break = truth["t0"] + 1.5 * truth["c"]
    return tanh_energy(t, **truth) + shelf_slope * truth["use"] / 100.0 * np.clip(t - t_break, 0.0, None)


def synthetic_energies(t: np.ndarray, truth: dict, noise: str, rng, shelf_slope: float = 0.0) -> tuple:
    sigma_t, cv = NOISE[noise]
    mean = true_energy(t, truth, shelf_slope)
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
        e, n_clipped = synthetic_energies(t, truth, sc["noise"], rng, sc.get("shelf_slope", 0.0))
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
                       upper_shelf_trend_p_value=fit["upper_shelf_trend_p_value"], index_fraction_of_rise=index_fraction_of_rise(fit, criterion),
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
        if len(g) != int(design.loc[design["scenario_id"] == sid, "replicates"].iloc[0]):
            raise AssertionError(f"{sid}: replicate count differs from the design")
        m = dict(scenario_id=sid, clipped_energies_per_replicate=g["n_clipped_at_zero"].mean())
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
    # Reported only (added after Block L was first run; NOT part of the rule): the two scale groups weighted by the primary cohort's
    # geometry counts instead of by the number of synthetic data sets (D-042, weighting sensitivity).
    mem = pd.read_csv(OUTPUTS / "wp2" / "cohort_membership.csv")
    counts = mem[mem["cohort"] == "primary"]["geometry_class"].str.startswith("full-size").value_counts()
    w_full = counts.get(True, 0) / counts.sum()
    summary["cohort_weighted_score_c_not_used_by_rule"] = w_full * summary["score_full-size_c"] + (1 - w_full) * summary["score_miniature_c"]
    summary["cohort_weight_full_size"] = w_full
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
        temperatures_c=" ".join(f"{v:.6g}" for v in temperatures(sc["spec"], dict(lse=sc["lse_true"], use=sc["use_true"],
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
    write_text(OUT / "synthetic_lse_strategy_rule.md", lse_rule_markdown(choice, reason, summary, per))
    reps.insert(0, "data_type", DATA_TYPE)
    design.to_csv(OUT / "synthetic_validation_design.csv", index=False)
    ad = reps["scenario_id"].isin(design.loc[design["block"] != "L", "scenario_id"])
    reps[ad].to_csv(OUT / "synthetic_validation_replicates_blocks_A-E.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    metrics = scenario_metrics(design, reps)
    metrics.to_csv(OUT / "synthetic_validation_metrics.csv", index=False)
    checks = flag_check(reps, design)
    checks.to_csv(OUT / "synthetic_flag_check.csv", index=False)
    limits = trust_limits(metrics)
    limits.to_csv(OUT / "synthetic_trust_limits.csv", index=False)
    misspecified_shelf_check(reps, design).to_csv(OUT / "synthetic_nonflat_upper_shelf_check.csv", index=False)
    figures(scenarios, design, reps, metrics, per)
    print(f"Synthetic validation: {len(design)} scenarios, {len(reps)} fits -> {OUT}")




# ---------------------------------------------------------------------------
# 5. Validation tables and figures (all SYNTHETIC)
# ---------------------------------------------------------------------------
def lse_rule_markdown(choice, reason, summary, per) -> str:
    return "\n".join([
        "# SYNTHETIC: lower-shelf strategy comparison (Block L, D-042)", "",
        f"Data type: {DATA_TYPE}.", "",
        "Key temperature: T41J from the analytic crossing (full-size truths) or T0 (miniature-scale truths). Score = mean over synthetic "
        "data sets of the 90th percentile of |error| (°C). Missing = share of replicates without a key temperature.", "",
        md_table(summary.drop(columns=["data_type"]).round(3)), "", f"**Rule outcome: `{choice}`** ({reason}).", ""])


def flag_check(reps: pd.DataFrame, design: pd.DataFrame) -> pd.DataFrame:
    """Do the outcome categories and flags separate accurate from inaccurate recoveries? Pooled over Blocks A-D with scatter."""
    d = reps.merge(design[["scenario_id", "block", "noise"]], on="scenario_id")
    d = d[d["block"].isin(["A", "B", "C", "D"]) & (d["noise"] != "zero")]
    rows = []

    def summarise(label, kind, h):
        r = dict(data_type=DATA_TYPE, group=label, kind=kind, fits=len(h), share_of_fits=len(h) / len(d))
        for col, ref, name in [("err_t0_c", REF_TEMPERATURE_C, "t0"), ("err_t41_analytic_c", REF_TEMPERATURE_C, "t41_analytic"),
                               ("err_use_rel", REF_USE_REL, "use_rel"), ("err_c_rel", REF_C_REL, "c_rel")]:
            x = h[col].dropna().abs() if col in h else pd.Series(dtype=float)
            r[f"{name}_median_abs"] = x.median() if len(x) else np.nan
            r[f"{name}_p90_abs"] = x.quantile(0.9) if len(x) else np.nan
            r[f"{name}_share_beyond_reference"] = float((x > ref).mean()) if len(x) else np.nan
        rows.append(r)

    for outcome in OUTCOMES:
        summarise(outcome, "outcome", d[d["outcome"] == outcome])
    summarise("all usable outcomes", "outcome group", d[d["outcome"].isin(USABLE)])
    summarise("all fits with estimates", "outcome group", d[d["outcome"] != OUTCOMES[0]])
    flags = [c for c in d.columns if c.startswith("flag_") and c != "flag_index_unavailable"]
    for flag in flags:
        summarise(f"{flag} = True", "flag", d[d[flag]])
        summarise(f"{flag} = False", "flag", d[~d[flag]])
    # The clean comparison: fits carrying exactly one flag against fits carrying none (flags overlap heavily otherwise).
    n_flags = d[flags].sum(axis=1)
    summarise("no flag", "only this flag", d[(n_flags == 0) & (d["outcome"] != OUTCOMES[0])])
    for flag in flags:
        summarise(f"only {flag}", "only this flag", d[(n_flags == 1) & d[flag]])
    summarise("two or more flags", "only this flag", d[n_flags >= 2])
    ok = d[d["outcome"] != OUTCOMES[0]].copy()
    ok["condition_number_quartile"] = pd.qcut(np.log10(ok["jacobian_condition_number"].replace(np.inf, 1e300)), 4,
                                              labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
    for q, h in ok.groupby("condition_number_quartile", observed=True):
        summarise(f"Jacobian condition number {q}", "audit: condition number", h)
    summarise("starts within 1 % of best cost disagree on T0 by > 1 °C", "audit: start agreement",
              ok[ok["t0_spread_within_1pct_of_best_cost_c"] > 1.0])
    summarise("starts within 1 % of best cost agree on T0 within 1 °C", "audit: start agreement",
              ok[ok["t0_spread_within_1pct_of_best_cost_c"] <= 1.0])
    return pd.DataFrame(rows)


def misspecified_shelf_check(reps: pd.DataFrame, design: pd.DataFrame) -> pd.DataFrame:
    """Block E: detection rate of the upper-shelf trend flag and the pull on USE when the true upper shelf is not flat.
    USE error is relative to the flat tanh USE of the truth (the energy just before the shelf starts to change)."""
    d = reps.merge(design[["scenario_id", "block", "design", "noise", "shelf_slope"]], on="scenario_id")
    rows = []
    for (design_name, noise, slope), h in d[d["block"] == "E"].groupby(["design", "noise", "shelf_slope"], sort=False):
        applicable = h["upper_shelf_trend_p_value"].notna()
        rows.append(dict(data_type=DATA_TYPE, design=design_name, noise=noise, shelf_slope_fraction_of_use_per_100c=slope, fits=len(h),
                         share_trend_test_applicable=float(applicable.mean()),
                         share_trend_flagged=float(h["flag_nonflat_upper_shelf"].mean()),
                         share_trend_flagged_when_applicable=float(h.loc[applicable, "flag_nonflat_upper_shelf"].mean()) if applicable.any() else np.nan,
                         share_usable=float(h["outcome"].isin(USABLE).mean()),
                         use_error_rel_median=h["err_use_rel"].median(), use_error_rel_p90_abs=h["err_use_rel"].abs().quantile(0.9),
                         t41_error_p90_abs_c=h["err_t41_analytic_c"].abs().quantile(0.9), t0_error_p90_abs_c=h["err_t0_c"].abs().quantile(0.9)))
    return pd.DataFrame(rows)


def trust_limits(metrics: pd.DataFrame) -> pd.DataFrame:
    """Per scenario with scatter (Blocks A-D): is truth recovered within the reference scales by all fits, and by usable fits only?"""
    m = metrics[metrics["block"].isin(["A", "B", "C", "D"]) & (metrics["noise"] != "zero")].copy()
    m["share_usable"] = m[[f"share_{o}" for o in USABLE]].sum(axis=1)
    m["share_not_usable"] = 1.0 - m["share_usable"]
    ok_all = (m["all_t41_analytic_p90_abs"] <= REF_TEMPERATURE_C) & (m["all_t0_p90_abs"] <= REF_TEMPERATURE_C) & \
             (m["all_use_rel_p90_abs"] <= REF_USE_REL)
    m["all_fits_within_reference_p90"] = ok_all
    ok_usable = (m["usable_t41_p90_abs"].fillna(np.inf) <= REF_TEMPERATURE_C) & (m["usable_t0_p90_abs"].fillna(np.inf) <= REF_TEMPERATURE_C) & \
                (m["usable_use_rel_p90_abs"].fillna(np.inf) <= REF_USE_REL)
    m["usable_fits_within_reference_p90"] = ok_usable & (m["share_usable"] > 0)
    cols = ["data_type", "scenario_id", "block", "design", "noise", "lse_true", "use_true", "t0_true", "c_true", "share_usable",
            "share_not_usable", "share_index_calculated", "all_t41_analytic_p90_abs", "all_t0_p90_abs", "all_use_rel_p90_abs",
            "all_c_rel_p90_abs", "usable_t41_p90_abs", "usable_t0_p90_abs", "usable_use_rel_p90_abs", "all_fits_within_reference_p90",
            "usable_fits_within_reference_p90"]
    return m[cols]


INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
NOISE_STYLE = {"low": ("#86b6ef", "o", "-"), "moderate": ("#2a78d6", "s", "-"), "high": ("#0d366b", "^", "-")}


def _style(ax):
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=INK2, labelsize=8)


def _replicate_data(sc: dict, rep: int) -> tuple:
    """Regenerate the synthetic energies of one replicate exactly as run_scenario drew them (same temperatures, seed and draws)."""
    truth = dict(lse=sc["lse_true"], use=sc["use_true"], t0=sc["t0_true"], c=sc["c_true"])
    t = temperatures(sc["spec"], truth)
    seed = int(hashlib.sha256(data_key(sc).encode()).hexdigest()[:15], 16)
    rng = np.random.default_rng(np.random.SeedSequence([SEED, seed]))
    for _ in range(rep + 1):
        e, _n = synthetic_energies(t, truth, sc["noise"], rng)
    return t, e, truth


EXAMPLE_SCENARIOS = [("good sampling: fits cluster around the truth", "A", "uniform x -3..3, n=12", "moderate"),
                     ("poor sampling: every fit converges, but they disagree", "B", "shelves + 1 transition point (n=7)", "moderate")]


def figures(scenarios, design, reps, metrics, per) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # 1. Two teaching examples: the same true curve and scatter, two sampling plans. Each panel overlays the fitted curves of the first
    # 40 replicates; the spread of those curves is what "reliable" and "unreliable" mean. Points shown: replicate 0 only.
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8))
    for ax, (title, block, name, noise) in zip(axes, EXAMPLE_SCENARIOS):
        sc = next(x for x in scenarios if x["block"] == block and x["design"] == name and x["noise"] == noise)
        truth = dict(lse=sc["lse_true"], use=sc["use_true"], t0=sc["t0_true"], c=sc["c_true"])
        r = reps[reps["scenario_id"] == sc["scenario_id"]].sort_values("replicate")
        m = metrics[metrics["scenario_id"] == sc["scenario_id"]].iloc[0]
        grid_t = np.linspace(truth["t0"] - 4 * truth["c"], truth["t0"] + 4 * truth["c"], 400)
        _style(ax)
        for k, (_, rr) in enumerate(r.head(40).iterrows()):
            if np.isfinite(rr.get("lse_j", np.nan)):
                ax.plot(grid_t, tanh_energy(grid_t, rr["lse_j"], rr["use_j"], rr["t0_c"], rr["c_c"]), color=BLUE, lw=0.7, alpha=0.35,
                        zorder=2, label="tanh fits to 40 synthetic replicates" if k == 0 else None)
        ax.plot(grid_t, tanh_energy(grid_t, **truth), color=INK, lw=1.8, ls="--", label="true curve (known)", zorder=3)
        t, e, _ = _replicate_data(sc, 0)
        ax.scatter(t, e, s=34, marker="^", facecolor="white", edgecolor=INK, linewidth=1.0, zorder=4,
                   label="SYNTHETIC specimens (replicate 0)")
        t41_true = criterion_temperature(**truth, e_crit=41.0)[0]
        ax.axhline(41.0, color=MUTED, lw=0.8, zorder=1)
        ax.text(grid_t[0], 41.0, " 41 J", fontsize=7, color=INK2, va="bottom")
        ax.set_xlabel("Test temperature (°C)", fontsize=8.5, color=INK)
        ax.set_ylabel("Absorbed energy (J)", fontsize=8.5, color=INK)
        ax.set_title(f"SYNTHETIC: {title}\n{name}, {noise} scatter", fontsize=8.5, color=INK)
        usable = float(sum(m[f"share_{o}"] for o in USABLE))
        txt = (f"true curve: LSE {truth['lse']:g} J, USE {truth['use']:g} J, T0 {truth['t0']:g} °C, C {truth['c']:g} °C, T41J {t41_true:.1f} °C\n"
               f"90 % of the {int(m['replicates'])} replicate fits have: |T41J error| <= {m['all_t41_analytic_p90_abs']:.1f} °C,\n"
               f"|T0 error| <= {m['all_t0_p90_abs']:.1f} °C, |USE error| <= {100 * m['all_use_rel_p90_abs']:.0f} %; "
               f"flagged not usable: {100 * (1 - usable):.0f} %")
        ax.text(0.0, -0.2, txt, transform=ax.transAxes, fontsize=7.2, va="top", color=INK2)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, 0.95))
    fig.suptitle("SYNTHETIC fitter-validation examples (not published data)", fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0.02, 1, 0.9))
    fig.subplots_adjust(bottom=0.27)
    fig.savefig(OUT / "synthetic_examples.png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    # 2. Error against specimen count and scatter (Block A).
    a = metrics[(metrics["block"] == "A") & (metrics["noise"] != "zero")].copy()
    a["n"] = a["design"].str.extract(r"n=(\d+)", expand=False).astype(int)
    panels = [("all_t41_analytic_p90_abs", "T41J: 90th percentile |error| (°C)", REF_TEMPERATURE_C, 1.0),
              ("all_t0_p90_abs", "T0: 90th percentile |error| (°C)", REF_TEMPERATURE_C, 1.0),
              ("all_use_rel_p90_abs", "USE: 90th percentile |error| (%)", 100 * REF_USE_REL, 100.0),
              ("share_not_usable", "Share of fits not usable (%)", None, 100.0)]
    a["share_not_usable"] = 1.0 - a[[f"share_{o}" for o in USABLE]].sum(axis=1)
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
    for ax, (col, label, ref, scale) in zip(axes, panels):
        _style(ax)
        for noise, (color, marker, ls) in NOISE_STYLE.items():
            g = a[a["noise"] == noise].sort_values("n")
            ax.plot(g["n"], g[col] * scale, color=color, marker=marker, ms=6, lw=2, ls=ls, label=f"{noise} scatter")
        if ref is not None:
            ax.axhline(ref, color=MUTED, lw=0.8)
            ax.text(31, ref, "reference", fontsize=7, color=INK2, va="bottom", ha="right")
        ax.set_xlabel("Specimens per curve (uniform over x = -3...3)", fontsize=8, color=INK)
        ax.set_title(label, fontsize=8.5, color=INK)
        ax.set_xticks([6, 8, 12, 18, 30])
        ax.set_ylim(bottom=0)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("SYNTHETIC validation: recovery error vs specimen count (all fits that returned estimates; 200 replicates each)",
                 fontsize=9.5, color=INK, y=0.9)
    fig.tight_layout(rect=(0, 0, 1, 0.84))
    fig.savefig(OUT / "synthetic_error_vs_specimens.png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    # 3. Sampling patterns (Block B, moderate scatter): errors for all fits and for usable fits, and the share flagged.
    b = metrics[(metrics["block"] == "B") & (metrics["noise"] == "moderate")].copy()
    b["share_not_usable"] = 1.0 - b[[f"share_{o}" for o in USABLE]].sum(axis=1)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), sharey=True)
    y = np.arange(len(b))[::-1]
    for ax, (col_all, col_usable, label, ref, scale) in zip(axes[:2], [
            ("all_t41_analytic_p90_abs", "usable_t41_p90_abs", "T41J: 90th percentile |error| (°C)", REF_TEMPERATURE_C, 1.0),
            ("all_use_rel_p90_abs", "usable_use_rel_p90_abs", "USE: 90th percentile |error| (%)", 100 * REF_USE_REL, 100.0)]):
        _style(ax)
        ax.scatter(b[col_all] * scale, y, marker="o", s=40, facecolor="white", edgecolor=INK, zorder=3, label="all fits with estimates")
        ax.scatter(b[col_usable] * scale, y, marker="s", s=34, color=BLUE, zorder=4, label="usable fits only")
        ax.axvline(ref, color=MUTED, lw=0.8)
        ax.set_xscale("log")
        ax.set_xlabel(label + " (log scale)", fontsize=8, color=INK)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(b["design"], fontsize=7.5)
    _style(axes[2])
    axes[2].barh(y, b["share_not_usable"] * 100, color=BLUE, height=0.6)
    axes[2].set_xlim(0, 100)
    axes[2].set_xlabel("Share of fits flagged not usable (%)", fontsize=8, color=INK)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=2, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.99))
    fig.suptitle("SYNTHETIC validation: sampling patterns, moderate scatter (reference lines: 10 °C, 10 %)", fontsize=9.5, color=INK, y=0.93)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "synthetic_sampling_patterns.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


if __name__ == "__main__":
    main()
