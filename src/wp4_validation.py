"""WP4 - SYNTHETIC checks of the bootstrap implementation (no published measurement is used anywhere in this file).

Every data set here is a synthetic curve with known truth, generated exactly as the approved WP3 validation generated it (the WP3 scenario
definitions, scatter model and seeds of src/wp3_validation.py; nothing is redesigned). The checks (DECISIONS.md D-060):
  1. zero scatter: data lying exactly on the approved model; the fixed-design bootstrap must collapse and the pairs bootstrap must
     reproduce the original estimate in (almost) every replicate - no artificial uncertainty from a coding error;
  2. determinism: the same data set and seed give identical replicates and summaries, whatever the number of worker processes or chunks;
  3. failure accounting: in difficult synthetic data sets, failed and target-unavailable replicates stay in the denominator and the
     interval-reporting rule switches off below a 95 % finite-target fraction;
  4. coverage: for a few WP3 scenarios (well sampled, weakly sampled, high scatter, and a miniature curve with a fitted lower shelf), how
     often the 95 % percentile intervals of both methods contain the known truth, and how the bootstrap SD compares with the actual
     spread of the estimate over repeated synthetic data sets.
Outputs (outputs/wp4/): synthetic_bootstrap_zero_scatter_check.csv, synthetic_bootstrap_determinism_check.csv,
synthetic_bootstrap_failure_accounting_check.csv, synthetic_bootstrap_coverage_by_dataset.csv, synthetic_bootstrap_coverage_summary.csv,
synthetic_bootstrap_validation.md. Every file carries a data_type column (or heading) saying SYNTHETIC.

Run:  .venv/bin/python src/wp4_validation.py
"""
from __future__ import annotations

import hashlib
import os
import time

import numpy as np
import pandas as pd

import wp3_fitter as F
import wp3_validation as V
import wp4_bootstrap as B
from common import OUTPUTS, md_table, write_text

OUT = OUTPUTS / "wp4"
DATA_TYPE = "SYNTHETIC (WP4 bootstrap validation; not published measurements)"
WORKERS = max(1, min(8, os.cpu_count() or 1))

# D-060. Zero scatter: truths the final method can represent exactly (full-size LSE equal to the fixed 2.7 J; miniature LSE fitted), on the
# WP3 Block A / Block L design uniform over x = -3...3 with 12 specimens.
EXACT_DESIGN = ("uniform x -3..3, n=12", V._x(np.linspace(-3, 3, 12)))
EXACT_TRUTHS = [("full-size", dict(lse=F.FIXED_LSE_CONVENTION_J["full-size"], use=150.0, t0=0.0, c=30.0)),
                ("miniature", dict(lse=0.48, use=8.0, t0=0.0, c=30.0))]
EXACT_TOLERANCE_C = 1e-3            # a coding error would move replicate temperatures by degrees, not by 0.001 °C
EXACT_TOLERANCE_USE_REL = 1e-5
PAIRS_EXACT_MIN_SHARE = 0.95        # pairs replicates that lose every transition temperature cannot pin T0 and C, even on exact data

# D-060. Failure accounting: difficult WP3 scenarios (final method, moderate scatter, WP3 replicate 0), in this predeclared order.
FAILURE_CANDIDATES = [("B", "x -0.5..3, n=12 (lower shelf missing)"), ("B", "shelves + 1 transition point (n=7)"),
                      ("B", "clustered cold side: x -3..-0.5, n=12")]

# D-060. Coverage: a small subset of approved WP3 scenarios (their first COVERAGE_DATASETS replicates, regenerated exactly).
COVERAGE_SCENARIOS = [("well sampled", "A", "uniform x -3..3, n=18", "moderate", "full-size", None),
                      ("weakly sampled", "B", "shelves + 2 transition points (n=8)", "moderate", "full-size", None),
                      ("high scatter", "A", "uniform x -3..3, n=18", "high", "full-size", None),
                      ("miniature, fitted lower shelf", "L", "uniform x -3..3, n=12 (lower shelf well sampled)", "moderate", "miniature",
                       dict(use_true=8.0, lse_true=0.48))]
COVERAGE_DATASETS = 200           # WP3's replicate count per scenario
# Benchmarked before any coverage result existed (1.85 ms of wall time per refit with 8 worker processes on the project machine): 1,000
# replicates per data set would take about 49 min, 500 about 25 min. 500 is recorded in D-060 with that reason; Efron & Tibshirani (1986) §9
# find about 250 replicates useful for a percentile interval. The published curves keep B = 2,000 (D-055).
COVERAGE_REPLICATES = 500


def scenarios() -> list:
    sc = V.build_scenarios()
    for i, s in enumerate(sc):
        s["scenario_id"] = f"S{i + 1:03d}"
    return sc


def find_scenario(all_sc, block, design, noise, scale="full-size", truth=None) -> dict:
    """The final-method scenario of WP3 (Blocks A-E: geometry_specific; Block L: its final-method component for the scale)."""
    strategy = V.FINAL_METHOD_BLOCK_L_COMPONENTS[scale] if block == "L" else F.PRIMARY_LSE_STRATEGY
    hits = [s for s in all_sc if s["block"] == block and s["design"] == design and s["noise"] == noise and s["scale"] == scale
            and s["lse_strategy"] == strategy and all(np.isclose(s[k], v) for k, v in (truth or {}).items())]
    if len(hits) != 1:
        raise AssertionError(f"expected one WP3 scenario for {block} / {design} / {noise} / {truth}, found {len(hits)}")
    return hits[0]


def wp3_datasets(sc: dict, n: int) -> list:
    """The first n synthetic data sets of a WP3 scenario, drawn exactly as src/wp3_validation.py::run_scenario drew them."""
    truth = dict(lse=sc["lse_true"], use=sc["use_true"], t0=sc["t0_true"], c=sc["c_true"])
    t = V.temperatures(sc["spec"], truth)
    seed = int(hashlib.sha256(V.data_key(sc).encode()).hexdigest()[:15], 16)
    rng = np.random.default_rng(np.random.SeedSequence([V.SEED, seed]))
    return [(t, V.synthetic_energies(t, truth, sc["noise"], rng, sc.get("shelf_slope", 0.0))[0]) for _ in range(n)]


def truth_values(truth: dict, scale: str) -> dict:
    crit = F.CRITERION_J[scale]
    return dict(t41j=F.criterion_temperature(**truth, e_crit=crit)[0] if crit else np.nan, t0=truth["t0"], use=truth["use"],
                lse=truth["lse"], c=truth["c"])


# ---------------------------------------------------------------------------
# 1. Zero scatter
# ---------------------------------------------------------------------------
def zero_scatter_check() -> pd.DataFrame:
    rows, tasks, originals = [], [], {}
    for scale, truth in EXACT_TRUTHS:
        t = V.temperatures(EXACT_DESIGN[1], truth)
        e = F.tanh_energy(t, **truth)
        originals[scale] = (t, e, B.wp3_estimate(t, e, scale))
        for method in [B.PAIRS, B.WILD]:
            tasks += B.make_tasks((scale, method), t, e, scale, method, f"zero-scatter|{scale}", B.B_REPLICATES)
    reps = B.run_tasks(tasks, WORKERS)
    for scale, truth in EXACT_TRUTHS:
        t, e, est = originals[scale]
        fit = est["fit"]
        key_target = "t41j" if scale == "full-size" else "t0"
        orig = dict(t41j=est["t41"], t0=fit["t0_c"], use=fit["use_j"])
        adj = B.leverage_adjusted_residuals(t, e, fit)
        tv = truth_values(truth, scale)
        for method in [B.PAIRS, B.WILD]:
            r = reps[(scale, method)]
            acc = B.accounting(r, scale)
            avail = B.target_available(r, key_target)
            dev = np.abs(r[key_target][avail] - orig[key_target])
            use_dev = np.abs(r["use"][B.target_available(r, "use")] / orig["use"] - 1.0)
            share_key = float(np.sum(dev <= EXACT_TOLERANCE_C) / len(avail))
            share_use = float(np.sum(use_dev <= EXACT_TOLERANCE_USE_REL) / len(avail))
            if method == B.WILD:
                passed = bool(avail.all() and dev.max() <= EXACT_TOLERANCE_C and use_dev.max() <= EXACT_TOLERANCE_USE_REL)
                rule = f"every replicate admissible with |key target - original| <= {EXACT_TOLERANCE_C:g} °C and |USE ratio - 1| <= {EXACT_TOLERANCE_USE_REL:g}"
            else:
                passed = bool(share_key >= PAIRS_EXACT_MIN_SHARE and share_use >= PAIRS_EXACT_MIN_SHARE)
                rule = (f">= {100 * PAIRS_EXACT_MIN_SHARE:g} % of replicates reproduce the key target within {EXACT_TOLERANCE_C:g} °C and USE "
                        f"within {EXACT_TOLERANCE_USE_REL:g} (replicates that lose every transition temperature cannot pin T0 and C)")
            rows.append(dict(data_type=DATA_TYPE, check="zero scatter (data exactly on the approved model)", scale=scale,
                             design=EXACT_DESIGN[0], truth=f"LSE {truth['lse']:g} J, USE {truth['use']:g} J, T0 {truth['t0']:g} °C, C {truth['c']:g} °C",
                             method=method, key_target=key_target, original_minus_truth_key_target=orig[key_target] - tv[key_target],
                             original_outcome=est["cls"]["outcome"], max_abs_residual_j=float(np.abs(adj["residual"]).max()),
                             max_abs_leverage_adjusted_residual_j=float(np.abs(adj["adjusted"]).max()), replicates=len(r["outcome_code"]),
                             replicates_admissible=acc["replicates_admissible"], replicates_usable_outcome=acc["replicates_usable_outcome"],
                             share_key_target_within_tolerance=share_key, share_use_within_tolerance=share_use,
                             max_abs_key_target_deviation_c=float(dev.max()) if len(dev) else np.nan,
                             median_abs_key_target_deviation_c=float(np.median(dev)) if len(dev) else np.nan,
                             key_target_bootstrap_sd_c=float(np.std(r[key_target][avail], ddof=1)) if avail.sum() > 1 else np.nan,
                             rule=rule, passed=passed))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Determinism
# ---------------------------------------------------------------------------
def determinism_check(all_sc) -> pd.DataFrame:
    sc = find_scenario(all_sc, "A", "uniform x -3..3, n=12", "moderate")
    t, e = wp3_datasets(sc, 1)[0]
    stream = f"determinism|{V.data_key(sc)}"
    rows = []
    for method in [B.PAIRS, B.WILD]:
        runs = {"single process, one chunk (run 1)": B.run_tasks(B.make_tasks("k", t, e, "full-size", method, stream, B.B_REPLICATES,
                                                                               chunk=B.B_REPLICATES), 1)["k"],
                "single process, one chunk (run 2)": B.run_tasks(B.make_tasks("k", t, e, "full-size", method, stream, B.B_REPLICATES,
                                                                               chunk=B.B_REPLICATES), 1)["k"],
                f"{WORKERS} worker processes, chunks of 97": B.run_tasks(B.make_tasks("k", t, e, "full-size", method, stream,
                                                                                      B.B_REPLICATES, chunk=97), WORKERS)["k"]}
        ref_name = "single process, one chunk (run 1)"
        ref = runs[ref_name]
        est = B.wp3_estimate(t, e, "full-size")
        ref_summary = {tg: B.summarise_target(ref, tg, est["t41"] if tg == "t41j" else est["fit"][B.ORIGINAL_COLUMN[tg]], est["cls"]["outcome"])
                       for tg in B.TARGETS["full-size"]}
        for name, r in runs.items():
            arrays_equal = all(np.array_equal(ref[k], r[k], equal_nan=r[k].dtype.kind == "f") for k in B.REPLICATE_FIELDS)
            summary = {tg: B.summarise_target(r, tg, est["t41"] if tg == "t41j" else est["fit"][B.ORIGINAL_COLUMN[tg]], est["cls"]["outcome"])
                       for tg in B.TARGETS["full-size"]}
            summaries_equal = all(pd.Series(summary[tg]).equals(pd.Series(ref_summary[tg])) for tg in summary)
            rows.append(dict(data_type=DATA_TYPE, check="determinism", data_set=f"{V.data_key(sc)} (WP3 replicate 0)", method=method,
                             run=name, compared_with=ref_name, replicates=len(r["outcome_code"]), per_replicate_arrays_identical=arrays_equal,
                             summaries_identical=summaries_equal, t41j_sd_c=summary["t41j"]["sd"], t41j_q025_c=summary["t41j"]["q025"],
                             t41j_q975_c=summary["t41j"]["q975"], passed=bool(arrays_equal and summaries_equal)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 3. Failure accounting
# ---------------------------------------------------------------------------
def failure_accounting_check(all_sc) -> pd.DataFrame:
    tasks, data = [], {}
    for block, design in FAILURE_CANDIDATES:
        sc = find_scenario(all_sc, block, design, "moderate")
        t, e = wp3_datasets(sc, 1)[0]
        data[design] = (sc, t, e, B.wp3_estimate(t, e, "full-size"))
        for method in [B.PAIRS, B.WILD]:
            tasks += B.make_tasks((design, method), t, e, "full-size", method, f"failure-accounting|{V.data_key(sc)}", B.B_REPLICATES)
    reps = B.run_tasks(tasks, WORKERS)
    rows = []
    for block, design in FAILURE_CANDIDATES:
        sc, t, e, est = data[design]
        for method in [B.PAIRS, B.WILD]:
            r = reps[(design, method)]
            acc = B.accounting(r, "full-size")
            requested = acc["replicates_requested"]
            outcome_sum = acc["replicate_evaluation_errors"] + sum(acc[f"replicates_{o}"] for o in F.OUTCOMES)
            status_sum = sum(acc[f"t41j_status_{k}"] for k in range(len(B.INDEX_STATUS_LABELS)))
            for target in B.TARGETS["full-size"]:
                original = est["t41"] if target == "t41j" else est["fit"][B.ORIGINAL_COLUMN[target]]
                s = B.summarise_target(r, target, original, est["cls"]["outcome"])
                finite_independent = int(np.sum(np.isfinite(r[target]) & B.target_available(r, target)))
                fraction_independent = finite_independent / len(r["outcome_code"])
                expected_label = (B.INTERVAL_UNAVAILABLE if fraction_independent < B.REPORTABLE_FINITE_FRACTION else
                                  B.INTERVAL_PRIMARY if est["cls"]["outcome"] in F.OUTCOMES[4:] else B.INTERVAL_DIAGNOSTIC)
                checks = dict(outcome_counts_sum_to_requested=outcome_sum == requested,
                              t41j_status_counts_sum_to_requested=status_sum == requested,
                              finite_plus_unavailable_equals_requested=s["finite_target_values"] + s["target_unavailable"] == requested,
                              finite_fraction_uses_all_requested=np.isclose(s["finite_target_fraction"], fraction_independent),
                              reportable_flag_follows_95pct_rule=s["interval_reportable"] == (fraction_independent >= B.REPORTABLE_FINITE_FRACTION),
                              label_follows_rule=s["interval_label"] == expected_label)
                rows.append(dict(data_type=DATA_TYPE, check="failure accounting", data_set=f"{V.data_key(sc)} (WP3 replicate 0)",
                                 method=method, target=target, original_outcome=est["cls"]["outcome"], original_index_status=est["index_status"],
                                 replicates_requested=requested, **{f"replicates_{o}": acc[f"replicates_{o}"] for o in F.OUTCOMES},
                                 replicate_evaluation_errors=acc["replicate_evaluation_errors"],
                                 t41j_unavailable_below_lowest_temperature=acc["t41j_status_4"],
                                 t41j_unavailable_other=requested - acc["t41j_status_0"] - acc["t41j_status_4"],
                                 finite_target_values=s["finite_target_values"], target_unavailable=s["target_unavailable"],
                                 finite_target_fraction=s["finite_target_fraction"], conditional_q025=s["q025"], conditional_q975=s["q975"],
                                 interval_reportable=s["interval_reportable"], interval_label=s["interval_label"],
                                 exercises_switch_off=bool(not s["interval_reportable"]), **checks, passed=all(checks.values())))
    out = pd.DataFrame(rows)
    if not out["passed"].all():
        raise AssertionError("bootstrap failure accounting check failed:\n" + out[~out["passed"]].to_string())
    if not out["exercises_switch_off"].any():
        raise AssertionError("no predeclared difficult data set produced a finite-target fraction below 95 %: the switch-off branch is untested")
    return out


# ---------------------------------------------------------------------------
# 4. Coverage
# ---------------------------------------------------------------------------
def coverage_study(all_sc) -> tuple:
    tasks, meta = [], {}
    for label, block, design, noise, scale, truth_sel in COVERAGE_SCENARIOS:
        sc = find_scenario(all_sc, block, design, noise, scale, truth_sel)
        truth = dict(lse=sc["lse_true"], use=sc["use_true"], t0=sc["t0_true"], c=sc["c_true"])
        for i, (t, e) in enumerate(wp3_datasets(sc, COVERAGE_DATASETS)):
            meta[(label, i)] = (sc, scale, truth, t, e, B.wp3_estimate(t, e, scale))
            for method in [B.PAIRS, B.WILD]:
                tasks += B.make_tasks((label, i, method), t, e, scale, method, f"coverage|{V.data_key(sc)}|dataset={i}",
                                      COVERAGE_REPLICATES, chunk=COVERAGE_REPLICATES)
    t_start = time.perf_counter()
    reps = B.run_tasks(tasks, WORKERS)
    elapsed = time.perf_counter() - t_start
    rows = []
    for (label, i), (sc, scale, truth, t, e, est) in meta.items():
        tv = truth_values(truth, scale)
        targets = ["t41j", "t0", "use"] if scale == "full-size" else ["t0", "use"]
        for method in [B.PAIRS, B.WILD]:
            r = reps[(label, i, method)]
            for target in targets:
                original = est["t41"] if target == "t41j" else est["fit"][B.ORIGINAL_COLUMN[target]]
                s = B.summarise_target(r, target, original, est["cls"]["outcome"])
                rows.append(dict(data_type=DATA_TYPE, scenario=label, wp3_scenario=f"{sc['block']}: {sc['design']} [{sc['noise']}]",
                                 scale=scale, dataset=i, method=method, target=target, truth=tv[target], original_estimate=original,
                                 original_outcome=est["cls"]["outcome"], finite_target_fraction=s["finite_target_fraction"],
                                 interval_reportable=s["interval_reportable"], q025=s["q025"], q975=s["q975"], sd=s["sd"],
                                 interval_width=s["interval_width"],
                                 truth_below_interval=bool(tv[target] < s["q025"]) if np.isfinite(s["q025"]) else np.nan,
                                 truth_above_interval=bool(tv[target] > s["q975"]) if np.isfinite(s["q975"]) else np.nan,
                                 covered=bool(s["q025"] <= tv[target] <= s["q975"]) if np.isfinite(s["q025"]) else np.nan))
    per = pd.DataFrame(rows)
    summary = []
    for (label, method, target), g in per.groupby(["scenario", "method", "target"], sort=False):
        rep = g[g["interval_reportable"]]
        est_ok = g["original_estimate"].dropna()
        n_rep = len(rep)
        cov = float(rep["covered"].astype(bool).mean()) if n_rep else np.nan
        emp_sd = float(est_ok.std(ddof=1)) if len(est_ok) > 1 else np.nan
        summary.append(dict(data_type=DATA_TYPE, scenario=label, wp3_scenario=g["wp3_scenario"].iloc[0], method=method, target=target,
                            truth=g["truth"].iloc[0], datasets=len(g), bootstrap_replicates_per_dataset=COVERAGE_REPLICATES,
                            share_datasets_with_original_estimate=len(est_ok) / len(g), share_datasets_interval_reportable=n_rep / len(g),
                            coverage_of_reportable_intervals=cov,
                            coverage_monte_carlo_se=float(np.sqrt(0.95 * 0.05 / n_rep)) if n_rep else np.nan,
                            share_truth_below_interval=float(rep["truth_below_interval"].astype(bool).mean()) if n_rep else np.nan,
                            share_truth_above_interval=float(rep["truth_above_interval"].astype(bool).mean()) if n_rep else np.nan,
                            coverage_all_intervals_with_values=float(g["covered"].dropna().astype(bool).mean()) if g["covered"].notna().any() else np.nan,
                            median_interval_width=float(rep["interval_width"].median()) if n_rep else np.nan,
                            median_bootstrap_sd=float(rep["sd"].median()) if n_rep else np.nan,
                            empirical_sd_of_original_estimates=emp_sd,
                            ratio_median_bootstrap_sd_to_empirical_sd=float(rep["sd"].median()) / emp_sd if n_rep and emp_sd > 0 else np.nan,
                            original_estimate_bias=float(est_ok.mean() - g["truth"].iloc[0]) if len(est_ok) else np.nan,
                            original_estimate_rmse=float(np.sqrt(np.mean((est_ok - g["truth"].iloc[0]) ** 2))) if len(est_ok) else np.nan))
    return per, pd.DataFrame(summary), elapsed, len(tasks)


def summary_markdown(zero, det, fail, cov_summary, elapsed, n_tasks) -> str:
    fmt = lambda d: d.drop(columns=["data_type"]).round(4)
    cov_t = cov_summary.drop(columns=["data_type", "wp3_scenario"]).copy()
    for c in ["share_datasets_with_original_estimate", "share_datasets_interval_reportable", "coverage_of_reportable_intervals",
              "share_truth_below_interval", "share_truth_above_interval", "coverage_all_intervals_with_values"]:
        cov_t[c] = cov_t[c].map(lambda x: "" if pd.isna(x) else f"{100 * x:.1f} %")
    L = ["# SYNTHETIC: WP4 bootstrap validation (not published measurements)", "",
         f"Data type: {DATA_TYPE}. Synthetic data sets are regenerated exactly from the approved WP3 validation (src/wp3_validation.py: "
         f"scenario definitions, scatter model, seed {V.SEED}); bootstrap seeds derive from WP4 seed {B.WP4_SEED} (D-055). Both bootstrap "
         "methods refit every replicate with the approved WP3 method (full-size LSE fixed at 2.7 J, miniature LSE fitted; D-054). Decisions: "
         "DECISIONS.md D-060.", "",
         "## 1. Zero scatter (data exactly on the approved model)", "", md_table(fmt(zero)), "",
         "## 2. Determinism", "", md_table(fmt(det)), "",
         "## 3. Failure accounting (failed and target-unavailable replicates stay in the denominator)", "", md_table(fmt(fail)), "",
         "## 4. Coverage of 95 % percentile intervals (WP3 scenarios, final method)", "",
         f"{COVERAGE_DATASETS} synthetic data sets per scenario (WP3 replicates 0-{COVERAGE_DATASETS - 1}); {COVERAGE_REPLICATES} bootstrap "
         f"replicates per data set and method ({n_tasks} bootstrap runs, {elapsed / 60:.1f} min with {WORKERS} worker processes). Coverage "
         "counts only reportable intervals (finite-target fraction >= 95 %); the nominal level is 95 %, and the Monte Carlo standard error of "
         "an estimated coverage of 95 % is shown. The empirical SD is the spread of the original estimate over the synthetic data sets (the "
         "actual sampling SD for this fixed design); the ratio compares the median bootstrap SD with it. Full-size truths have LSE 5 J while "
         "the final method fixes 2.7 J, so the original estimates carry the small bias recorded in WP3 (D-042).", "",
         md_table(cov_t.round(3)), ""]
    return "\n".join(L)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    all_sc = scenarios()
    t0 = time.perf_counter()
    zero = zero_scatter_check()
    zero.to_csv(OUT / "synthetic_bootstrap_zero_scatter_check.csv", index=False)
    print(zero[["scale", "method", "share_key_target_within_tolerance", "max_abs_key_target_deviation_c", "passed"]].to_string(index=False))
    if not zero["passed"].all():
        raise AssertionError("zero-scatter check failed")
    det = determinism_check(all_sc)
    det.to_csv(OUT / "synthetic_bootstrap_determinism_check.csv", index=False)
    print(det[["method", "run", "per_replicate_arrays_identical", "summaries_identical"]].to_string(index=False))
    if not det["passed"].all():
        raise AssertionError("determinism check failed")
    fail = failure_accounting_check(all_sc)
    fail.to_csv(OUT / "synthetic_bootstrap_failure_accounting_check.csv", index=False)
    print(fail[["data_set", "method", "target", "finite_target_fraction", "interval_label", "passed"]].to_string(index=False))
    per, cov_summary, elapsed, n_tasks = coverage_study(all_sc)
    per.to_csv(OUT / "synthetic_bootstrap_coverage_by_dataset.csv", index=False)
    cov_summary.to_csv(OUT / "synthetic_bootstrap_coverage_summary.csv", index=False)
    print(cov_summary[["scenario", "method", "target", "share_datasets_interval_reportable", "coverage_of_reportable_intervals",
                       "ratio_median_bootstrap_sd_to_empirical_sd"]].to_string(index=False))
    write_text(OUT / "synthetic_bootstrap_validation.md", summary_markdown(zero, det, fail, cov_summary, elapsed, n_tasks))
    print(f"WP4 synthetic bootstrap validation complete in {(time.perf_counter() - t0) / 60:.1f} min -> {OUT}")


if __name__ == "__main__":
    main()
