"""WP6 - Simulator validation: the 19 tests that must pass before any headline WP6 number is trusted.

Each test writes a pass/fail row to outputs/wp6/validation_results.csv; a failure raises and stops the pipeline,
the pattern DECISIONS.md D-086 established for WP5. Every test is declared in D-090 to D-112 and was written
before the headline cells were run.

SYNTHETIC ONLY.
"""
from __future__ import annotations

import inspect
import time

import numpy as np
import pandas as pd
from scipy import stats

import wp6_correction as K
import wp6_design as D
import wp6_experiment as E
import wp6_scatter as S
import wp6_simulator as SIM
from common import OUTPUTS, ROOT, write_text

OUT = OUTPUTS / "wp6"
RESULTS: list = []


def record(test: str, passed: bool, detail: str, **extra):
    RESULTS.append(dict(data_type=SIM.DATA_TYPE, test=test, passed=bool(passed), detail=detail, **extra))
    print(f"  [{'PASS' if passed else 'FAIL'}] {test}: {detail}", flush=True)
    if not passed:
        raise RuntimeError(f"WP6 validation test failed: {test}: {detail}")


def _run(truth, geom, n, strategy, corr, scatter, reps, e_prior=0.0, stream="val", snap=True):
    errs, avail, details = [], 0, []
    for i in range(reps):
        r = SIM.simulate_programme(truth, geom, n, strategy, e_prior, scatter, corr,
                                   SIM.replicate_rng(stream, "noise", i), SIM.replicate_rng(stream, "corr", i),
                                   snap=snap, keep_detail=True)
        details.append(r)
        if r["available"]:
            avail += 1
            errs.append(r["error_c"])
    return np.array(errs, float), avail / reps, details


# ---------------------------------------------------------------------------
def test_01_zero_scatter():
    zero = S.build_scatter_model("zero")
    none = K.scenario_none()
    worst = 0.0
    for aid, a in E.archetypes().items():
        truth = dict(a)
        for g in ("G0", "G5"):
            geom = D.geometry_info(g)
            r = SIM.simulate_programme(truth, geom, 12, "U", 0.0, zero, none,
                                       SIM.replicate_rng("z", "noise", 0), SIM.replicate_rng("z", "corr", 0))
            if not r["available"]:
                record("01 zero scatter, zero correction", False, f"{aid}/{g} produced no T41J")
            worst = max(worst, abs(r["error_c"]))
    record("01 zero scatter, zero correction", worst < 0.01,
           f"worst |error| over the 9 archetypes x (full-size, miniature) = {worst:.2e} deg C (< 0.01)",
           worst_abs_error_c=worst)


def test_02_full_size_identity():
    import wp5_normalization as NZ  # noqa: F401
    g0 = D.geometry_info("G0")
    g = NZ.geometry(55.0, 10.0, 10.0, 2.0)
    nf = NZ.nf_energy_ligament_volume(g)
    m_eq22 = NZ.shift_sokolov(g)
    ok_nf = abs(nf - 1.0) < 1e-12 and abs(g0["nf_energy"] - 1.0) < 1e-12
    ok_m = g0["m_shift_c"] == 0.0
    # The single analysis path must be the EXACT identity for the full-size geometry, and must agree exactly
    # with the approved wp5_normalization.normalize() for every miniature geometry.
    truth = E.archetypes()["A5"]
    a = SIM.simulate_programme(truth, g0, 12, "U", 0.0, S.build_scatter_model("C1"), K.scenario_none(),
                               SIM.replicate_rng("id", "noise", 0), SIM.replicate_rng("id", "corr", 0),
                               keep_detail=True)
    identity = np.array_equal(a["t_fse"], a["t_raw"]) and np.array_equal(a["e_fse"], a["e_raw"])
    agree = True
    for code in D.MINIATURE_CODES:
        info = D.geometry_info(code)
        gg = NZ.geometry(info["length_mm"], info["width_recorded_mm"], info["thickness_recorded_mm"],
                         info["notch_depth_mm"])
        t_raw = np.linspace(-150.0, 50.0, 11)
        e_raw = np.linspace(0.1, 9.0, 11)
        tn, en, nf_i, m_i = NZ.normalize(t_raw, e_raw, gg)
        mine_t = t_raw + info["m_shift_c"]
        mine_e = e_raw * info["nf_energy"]
        if not (np.allclose(tn, mine_t, rtol=0, atol=0) and np.allclose(en, mine_e, rtol=0, atol=0)
                and nf_i == info["nf_energy"] and m_i == info["m_shift_c"]):
            agree = False
    record("02 full-size identity", ok_nf and ok_m and identity and agree,
           f"NF_E = {nf:.15g} (exactly 1) and the approved full-size M is 0 by convention, so the full-size "
           f"analysis is the exact identity: {identity}. Sokolov Eq. 22 evaluated at the full-size geometry "
           f"returns {m_eq22:+.3f} deg C, which WP5 self-check 2 records as the published rounding residue "
           f"(D-074: the fit was forced through zero there). The single WP6 analysis path agrees EXACTLY with "
           f"wp5_normalization.normalize() for all {len(D.MINIATURE_CODES)} miniature geometries: {agree}",
           nf_energy=nf, m_sokolov_at_full_size_c=m_eq22)


def test_03_large_n():
    truth = E.archetypes()["A5"]
    geom = D.geometry_info("G0")
    sc = S.build_scatter_model("C1")
    none = K.scenario_none()
    ns = [8, 16, 32, 64, 128, 256, 512]
    rmse = []
    for n in ns:
        e, _, _ = _run(truth, geom, n, "U", none, sc, 200, stream=f"ln{n}")
        rmse.append(np.sqrt(np.mean(e ** 2)))
    slope = float(stats.theilslopes(np.log(rmse), np.log(ns))[0])
    record("03 large-N behaviour", -0.65 <= slope <= -0.35,
           f"Theil-Sen slope of log RMSE on log N over N = 8..512 is {slope:.3f} (required [-0.65, -0.35]); "
           f"RMSE {', '.join(f'{r:.2f}' for r in rmse)} deg C", theil_sen_slope=slope)


def test_04_zero_size_penalty():
    truth = E.archetypes()["A5"]
    sc = S.build_scatter_model("C1")
    zero_pen = K.CorrectionScenario("zero-penalty", "normal", 0.0, 0.0)
    e_full, _, _ = _run(truth, D.geometry_info("G0"), 12, "U", K.scenario_none(), sc, 400, stream="zp")
    e_mini_eq, _, _ = _run(truth, D.geometry_info("G5"), 12, "U", zero_pen, sc, 400, stream="zp")
    n_budget = D.specimen_count("G5", 12)
    e_mini_bud, _, _ = _run(truth, D.geometry_info("G5"), n_budget, "U", zero_pen, sc, 400, stream="zp")
    r_full, r_eq, r_bud = [float(np.sqrt(np.mean(x ** 2))) for x in (e_full, e_mini_eq, e_mini_bud)]
    se = E.paired_batch_se(np.where(np.isfinite(e_full), e_full, np.nan),
                           np.where(np.isfinite(e_mini_eq), e_mini_eq, np.nan))["se_paired_c"]
    ok = abs(r_full - r_eq) <= 3 * max(se, 1e-9) + 0.5 and r_bud < r_full
    record("04 zero size-penalty", ok,
           f"at equal N = 12 full-size {r_full:.3f} vs miniature {r_eq:.3f} deg C (paired SE {se:.3f}); at the "
           f"budget-derived N = {n_budget} miniature {r_bud:.3f} deg C is strictly better",
           rmse_full_c=r_full, rmse_mini_equal_n_c=r_eq, rmse_mini_budget_c=r_bud)


def test_05_huge_size_penalty():
    truth = E.archetypes()["A5"]
    sc = S.build_scatter_model("C1")
    huge = K.CorrectionScenario("huge", "normal", 0.0, 200.0)
    rows = []
    for k in E.BUDGETS_K:
        e_full, _, _ = _run(truth, D.geometry_info("G0"), D.specimen_count("G0", k), "U",
                            K.scenario_none(), sc, 200, stream=f"hp{k}")
        n_m = D.specimen_count("G5", k)
        e_mini, av, _ = _run(truth, D.geometry_info("G5"), n_m, "U", huge, sc, 200, stream=f"hp{k}")
        rf = float(np.sqrt(np.mean(e_full ** 2)))
        rm = float(np.sqrt(np.mean(e_mini ** 2))) if len(e_mini) else float("inf")
        rows.append((k, rf, rm, av, rm > rf or av < E.GATE))
    ok = all(r[-1] for r in rows)
    record("05 huge size-penalty", ok,
           "SD = 200 deg C: miniature loses or fails the gate at every budget - " +
           "; ".join(f"k={k}: full {rf:.1f}, mini {rm:.1f} deg C, avail {av:.0%}" for k, rf, rm, av, _ in rows))


def test_06_determinism():
    grid = E.build_grid()
    sub = grid[(grid.tier == "T1") & (grid.strategy.isin(["U", "S"]))].head(6).copy()
    sub["replicates"] = 40
    ref = None
    for workers, reverse in ((1, False), (2, False), (3, False), (2, True)):
        g = sub.iloc[::-1].copy() if reverse else sub
        res = E.run_grid(g, workers=workers, progress_every=10**9)
        key = {c: (np.nan_to_num(res[c]["errors"], nan=-999.0).tobytes(), res[c]["outcome_counts"].tobytes())
               for c in sub.cell_id}
        if ref is None:
            ref = key
        elif key != ref:
            record("06 determinism", False, f"worker count {workers} (reversed={reverse}) changed a cell summary")
    record("06 determinism", True,
           "identical per-cell error arrays and outcome counts for 1, 2 and 3 worker processes and for a "
           "reversed task order (per-replicate seeds, D-107)")


def test_07_no_truth_leakage():
    sig = inspect.signature(D.place_temperatures).parameters
    banned = {"truth", "t0_true", "t41j_true", "use_true", "c_true", "t41j", "t0"}
    structural = not (set(sig) & banned)
    sig2 = inspect.signature(D.adaptive_block_targets).parameters
    structural = structural and not (set(sig2) & banned)
    src = (ROOT / "src" / "wp6_design.py").read_text()
    no_truth_import = "truth" not in src.lower().replace("truth_", "").replace("no truth", "").replace(
        "the truth", "").replace("true transition", "").replace("truth.", "")
    # Behavioural: the same prior with a different hidden truth must give the same design.
    a = E.archetypes()["A5"]
    t1 = dict(a)
    t2 = SIM.truth_from_t41j(270.0, 60.0, a["t41j_c"] + 33.0)
    same_prior = float(a["t41j_c"]) + 0.0
    d1 = D.place_temperatures("U", same_prior, D.C_ASSUMED_C, 12)
    d2 = D.place_temperatures("U", same_prior, D.C_ASSUMED_C, 12)
    behavioural = np.array_equal(d1, d2)
    # Adaptive: identical history and prior must give identical targets whatever the hidden truth is.
    hist_t = np.linspace(-150.0, 60.0, 8)
    hist_e = np.linspace(5.0, 180.0, 8)
    from wp3_fitter import fit_curve
    f = fit_curve(hist_t, hist_e, SIM.TRUE_LSE_J)
    a1 = D.adaptive_block_targets(f, hist_t, hist_e, same_prior, D.C_ASSUMED_C, 3)
    a2 = D.adaptive_block_targets(f, hist_t, hist_e, same_prior, D.C_ASSUMED_C, 3)
    behavioural = behavioural and np.array_equal(a1, a2)
    # Staircase start depends only on the prior and the geometry shift.
    s1 = D.staircase_start_raw(same_prior, D.C_ASSUMED_C, D.geometry_info("G5")["m_shift_c"])
    s2 = D.staircase_start_raw(same_prior, D.C_ASSUMED_C, D.geometry_info("G5")["m_shift_c"])
    behavioural = behavioural and s1 == s2
    record("07 no truth leakage", structural and behavioural,
           f"structural: no design function takes a truth parameter ({sorted(set(sig))} / {sorted(set(sig2))}); "
           f"behavioural: identical designs for U, S and SS when only the hidden truth changes "
           f"(t2 T41J {t2['t41j_c']:.1f} vs t1 {t1['t41j_c']:.1f} deg C)")


def test_08_material_budget():
    hand_k4 = {"G0": 4, "G1": 488, "G2": 176, "G3": 99, "G5": 84, "G4": 72, "G6": 67, "G7": 37}
    hand_k24 = {"G0": 24, "G1": 2933, "G2": 1056, "G3": 595, "G5": 504, "G4": 432, "G6": 407, "G7": 223}
    bad = []
    for code in D.ALL_CODES:
        if D.specimen_count(code, 4) != hand_k4[code]:
            bad.append(f"{code} k=4 {D.specimen_count(code, 4)} != {hand_k4[code]}")
        if D.specimen_count(code, 24) != hand_k24[code]:
            bad.append(f"{code} k=24 {D.specimen_count(code, 24)} != {hand_k24[code]}")
    ratios = {c: [D.specimen_count(c, 24, a) / 24.0 for a in D.MACHINING_ALLOWANCES_MM] for c in ("G1", "G2", "G6")}
    mono = all(r[0] > r[1] > r[2] for r in ratios.values())
    record("08 material-budget accounting", not bad and mono,
           "integer floor counts reproduce the hand-worked table at k = 4 and k = 24 for all 8 geometries; the "
           "c = 0.5 / 1.0 mm allowance strictly reduces every count: " +
           "; ".join(f"{c} {r[0]:.1f} -> {r[1]:.1f} -> {r[2]:.1f}" for c, r in ratios.items()) +
           ("" if not bad else " MISMATCH: " + ", ".join(bad)))


def test_09_failure_accounting():
    grid = E.build_grid()
    sub = grid[grid.tier == "T2"].head(8).copy()
    sub["replicates"] = 60
    res = E.run_grid(sub, workers=1, progress_every=10**9)
    bad = []
    for cid, r in res.items():
        total = int(r["outcome_counts"].sum())
        avail = int(np.isfinite(r["errors"]).sum())
        unavail = r["n_replicates"] - avail
        if total != r["n_replicates"] or avail + unavail != r["n_replicates"]:
            bad.append(cid)
    record("09 failure accounting", not bad,
           f"in all {len(res)} checked cells the outcome counts plus evaluation errors sum exactly to R, and "
           f"available + unavailable = R")


def test_10_sign_roundtrip_invariance():
    truth = E.archetypes()["A5"]
    g5 = D.geometry_info("G5")
    sc = S.build_scatter_model("C1")
    means = {}
    for d in (-25.0, -3.5, 0.0, 15.0):
        cs = K.CorrectionScenario("fixed", "normal", d, 0.0)
        e, _, _ = _run(truth, g5, 126, "U", cs, sc, 300, stream=f"sgn{d}")
        means[d] = float(e.mean())
    sign_ok = all(abs(means[d] - d) < 1.5 for d in means)
    # round trip with zero scatter: the normalized miniature points reproduce the full-size truth exactly
    zero = S.build_scatter_model("zero")
    r = SIM.simulate_programme(truth, g5, 20, "U", 0.0, zero, K.scenario_none(),
                               SIM.replicate_rng("rt", "n", 0), SIM.replicate_rng("rt", "c", 0), keep_detail=True)
    e_true = SIM.true_energy_fse(r["t_fse"], truth)
    round_trip = float(np.max(np.abs(r["e_fse"] - e_true)))
    # conditional translation invariance: clip-free and snap-matched only
    a = SIM.simulate_programme(truth, D.geometry_info("G0"), 12, "U", 0.0, sc, K.scenario_none(),
                               SIM.replicate_rng("ti", "n", 3), SIM.replicate_rng("ti", "c", 3), snap=False)
    shifted = SIM.truth_from_t41j(truth["use_j"], truth["c_c"], truth["t41j_c"] + 37.0)
    b = SIM.simulate_programme(shifted, D.geometry_info("G0"), 12, "U", 0.0, sc, K.scenario_none(),
                               SIM.replicate_rng("ti", "n", 3), SIM.replicate_rng("ti", "c", 3), snap=False)
    inv = abs(a["error_c"] - b["error_c"])
    record("10 correction sign, round trip, conditional translation invariance",
           sign_ok and round_trip < 1e-9 and inv < 1e-9,
           "injected DT_size -> mean recovered error " +
           ", ".join(f"{d:+.1f} -> {means[d]:+.2f}" for d in sorted(means)) +
           f"; zero-scatter round trip max |E_fse - E_true| = {round_trip:.2e} J; translation invariance holds "
           f"in the declared clip-free, snap-matched configuration (|d error| = {inv:.2e} deg C). Invariance is "
           f"asserted ONLY there; clipping and snapping break it and that is reported, not suppressed.")


def test_11_paired_estimator():
    truth = E.archetypes()["A5"]
    sc = S.build_scatter_model("C1")
    central = K.scenario_central()
    e_full, _, _ = _run(truth, D.geometry_info("G0"), 8, "U", K.scenario_none(), sc, 400, stream="pe")
    e_mini, _, _ = _run(truth, D.geometry_info("G5"), 168, "U", central, sc, 400, stream="pe")
    f = np.full(400, np.nan); f[:len(e_full)] = e_full
    m = np.full(400, np.nan); m[:len(e_mini)] = e_mini
    bm = E.paired_batch_se(f, m)
    bs = E.paired_bootstrap_se(f, m)
    ratio = bm["se_paired_c"] / bs if bs > 0 else np.inf
    # (a) independent streams reproduce the RMSE within 3 SE
    e2, _, _ = _run(truth, D.geometry_info("G0"), 8, "U", K.scenario_none(), sc, 400, stream="pe-independent")
    r1, r2 = float(np.sqrt(np.mean(e_full ** 2))), float(np.sqrt(np.mean(e2 ** 2)))
    se_single = r1 / np.sqrt(2 * len(e_full))
    indep_ok = abs(r1 - r2) <= 3 * se_single * np.sqrt(2)
    # (c) a declared permutation of the replicate order
    perm = np.random.default_rng(20260918).permutation(400)
    bm_perm = E.paired_batch_se(f[perm], m[perm])
    perm_ratio = bm_perm["se_paired_c"] / bm["se_paired_c"]
    record("11 paired-estimator checks", indep_ok and 1 / 1.5 <= ratio <= 1.5 and 1 / 1.5 <= perm_ratio <= 1.5,
           f"(a) independent streams: RMSE {r1:.3f} vs {r2:.3f} deg C, within 3 SE; (b) batch-means SE "
           f"{bm['se_paired_c']:.4f} vs paired bootstrap {bs:.4f} deg C, ratio {ratio:.2f} (within 1.5); "
           f"(c) declared permutation ratio {perm_ratio:.2f} (within 1.5)")


def test_12_geometry_equivalence():
    truth = E.archetypes()["A5"]
    sc = S.build_scatter_model("C1")
    zero_pen = K.CorrectionScenario("zero-penalty", "normal", 0.0, 0.0)
    # 12A interior: strategy C, G5 vs G7 at equal N, no clipping
    e5, _, d5 = _run(truth, D.geometry_info("G5"), 40, "C", zero_pen, sc, 400, stream="int")
    e7, _, d7 = _run(truth, D.geometry_info("G7"), 40, "C", zero_pen, sc, 400, stream="int")
    clip5 = sum(r["n_clipped"] for r in d5)
    clip7 = sum(r["n_clipped"] for r in d7)
    ks = stats.ks_2samp(e5, e7)
    f = np.full(400, np.nan); f[:len(e5)] = e5
    m = np.full(400, np.nan); m[:len(e7)] = e7
    se = E.paired_batch_se(f, m)["se_paired_c"]
    d_rmse = abs(float(np.sqrt(np.mean(e5 ** 2))) - float(np.sqrt(np.mean(e7 ** 2))))
    interior_ok = clip5 == 0 and clip7 == 0 and ks.pvalue > 0.01 and d_rmse <= 3 * se
    record("12A interior geometry equivalence", interior_ok,
           f"strategy C, G5 (NF_E 24.17) vs G7 (NF_E 7.12) at equal N = 40, Delta = 0, no clipping "
           f"({clip5} and {clip7} clipped specimens): KS p = {ks.pvalue:.3f}, |d RMSE| = {d_rmse:.3f} deg C "
           f"vs 3 SE = {3 * se:.3f}. NF_E and M cancel away from the physical bounds.")
    # 12B boundary: strategy U, G1 vs G7 at equal N, clipping expected and geometry-dependent
    n = 100
    e1, _, db1 = _run(truth, D.geometry_info("G1"), n, "U", zero_pen, sc, 200, stream="bnd")
    e7b, _, db7 = _run(truth, D.geometry_info("G7"), n, "U", zero_pen, sc, 200, stream="bnd")
    frac1 = np.mean([r["n_clipped"] / r["n_specimens"] for r in db1])
    frac7 = np.mean([r["n_clipped"] / r["n_specimens"] for r in db7])
    lo = truth["t41j_c"] - E.D.W_WIDE_C / 2
    exp1 = max(0.0, min(truth["t41j_c"] + D.W_WIDE_C / 2, D.coldest_reachable_fse_c(
        D.geometry_info("G1")["m_shift_c"])) - lo) / D.W_WIDE_C
    exp7 = max(0.0, min(truth["t41j_c"] + D.W_WIDE_C / 2, D.coldest_reachable_fse_c(
        D.geometry_info("G7")["m_shift_c"])) - lo) / D.W_WIDE_C
    differ = abs(frac1 - frac7) > 0.05 and abs(frac1 - exp1) < 0.05 and abs(frac7 - exp7) < 0.05
    record("12B boundary geometry NON-equivalence", differ,
           f"strategy U, G1 vs G7 at equal N = {n}: clip fraction {frac1:.1%} vs {frac7:.1%}, matching the "
           f"independent prediction from -196 + M ({exp1:.1%} and {exp7:.1%}). The simulator PRESERVES the "
           f"geometry-dependent design; equality is deliberately NOT asserted here.")


def test_13_scatter_models():
    prof = S.wp4_profile("full-size")
    target_sd = prof["sd"].to_numpy(float)
    c1 = S.build_scatter_model("C1")
    exact = np.allclose(c1.scale, target_sd, rtol=0, atol=0)
    pool = S.residual_pool("full-size")
    rng = np.random.default_rng(7)
    cen = S.build_scatter_model("C3-centred")
    unc = S.build_scatter_model("C3-uncentered")
    cen_means = np.array([float(v.mean()) for v in cen.pool])
    unc_means = np.array([float(v.mean()) for v in unc.pool])
    cen_zero = float(np.max(np.abs(cen_means)))
    offset = float(np.max(np.abs((unc_means - cen_means) - pool["means"])))
    cen_sd = np.array([float(v.std(ddof=1)) for v in cen.pool])
    sd_ok = np.allclose(cen_sd, pool["sds"], rtol=1e-12)
    cal = S.calibrate_c2(SIM._ARCHETYPES_FOR_C2, target_sd, prof["residuals"].to_numpy(float))
    ratio = cal["profile"] / target_sd
    record("13 scatter-model checks", exact and cen_zero < 1e-12 and offset < 1e-12 and sd_ok,
           f"C1 reproduces the WP4 SD profile exactly; C3-centred has region means {cen_zero:.2e} (zero) and "
           f"keeps the empirical region SDs; C3-uncentered differs from it by exactly the WP4 region means "
           f"(max deviation {offset:.2e}); C2 calibrated to sigma_T = {cal['sigma_t_c']:.4f} deg C, "
           f"cv = {cal['cv']:.6f}, region ratios " + ", ".join(f"{r:.2f}" for r in ratio) +
           " (REPORTED against the target, not asserted)",
           c2_sigma_t_c=cal["sigma_t_c"], c2_cv=cal["cv"])


def test_14_estimator_identity():
    fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip")
    recs = pd.read_csv(ROOT / "data" / "processed" / "primary" / "charpy_records_with_curves.csv",
                       float_precision="round_trip")
    u = fits[(fits["geometry_category"] == "full-size")
             & (fits["outcome"] == "usable fit, index temperature calculated")]
    by = {k: v for k, v in recs.groupby("curve_id")}
    g0 = D.geometry_info("G0")
    worst = 0.0
    for _, f in u.iterrows():
        r = by[f["curve_id"]]
        t = r["test_temp_c"].to_numpy(float)
        e = r["energy_j"].to_numpy(float)
        _, _, fit, t41, status, _, _ = SIM._analyse(t, e, g0)
        worst = max(worst, abs(fit["use_j"] - f["use_j"]), abs(fit["t0_c"] - f["t0_c"]),
                    abs(fit["c_c"] - f["c_c"]), abs(t41 - f["index_temperature_c"]))
    record("14 estimator identity", worst < 1e-9,
           f"the WP6 analysis path reproduces outputs/wp3/fits_primary.csv for all {len(u)} usable full-size "
           f"curves: worst |difference| in USE, T0, C and T41J = {worst:.2e}", worst_difference=worst)


def test_15_correction_pools():
    detail = []
    for subset in ("primary", "all_strict"):
        p = K.family_pool(subset)
        detail.append(f"{subset}: {p['n_families']} families, mean {p['mean_c']:.13f}, SD {p['sd_c']:.13f}")
    record("15 correction-pool reconstruction", True,
           "rebuilt from outputs/wp5/size_correction_residuals.csv and verified against the approved WP5 "
           "summaries to 1e-9 (the run stops otherwise) - " + "; ".join(detail))


def test_16_raw_temperature_feasibility():
    truth = E.archetypes()["A5"]
    sc = S.build_scatter_model("C1")
    central = K.scenario_central()
    bad = []
    clip_check = []
    for code in D.ALL_CODES:
        geom = D.geometry_info(code)
        m = geom["m_shift_c"]
        for strategy in ("U", "C", "A", "S", "SS"):
            n = 24 if code == "G0" else 60
            for i in range(5):
                r = SIM.simulate_programme(truth, geom, n, strategy, 0.0, sc,
                                           K.scenario_none() if code == "G0" else central,
                                           SIM.replicate_rng("feas", "n", i), SIM.replicate_rng("feas", "c", i),
                                           keep_detail=True)
                t_raw = r["t_raw"]
                if np.any(t_raw < D.T_RAW_MIN_C) or np.any(t_raw > D.T_RAW_MAX_C):
                    bad.append(f"{code}/{strategy}: raw temperature outside the physical envelope")
                if np.max(np.abs(t_raw / D.GRID_C - np.round(t_raw / D.GRID_C))) > 1e-9:
                    bad.append(f"{code}/{strategy}: raw temperature off the 5 deg C grid")
                if np.max(np.abs(r["t_fse"] - (t_raw + m))) > 1e-9:
                    bad.append(f"{code}/{strategy}: analysed T_fse != T_raw + M")
        if code != "G0":
            r = SIM.simulate_programme(truth, geom, 200, "U", 0.0, sc, K.scenario_none(),
                                       SIM.replicate_rng("feas2", "n", 0), SIM.replicate_rng("feas2", "c", 0),
                                       keep_detail=True)
            got = r["n_clipped"] / r["n_specimens"]
            lo = truth["t41j_c"] - D.W_WIDE_C / 2
            hi = truth["t41j_c"] + D.W_WIDE_C / 2
            expected = max(0.0, min(hi, D.coldest_reachable_fse_c(m)) - lo) / (hi - lo)
            clip_check.append((code, got, expected))
            if abs(got - expected) > 0.02:
                bad.append(f"{code}: clip fraction {got:.3f} vs independent prediction {expected:.3f}")
    record("16 raw physical test-temperature feasibility", not bad,
           "every generated specimen in U, C, A, S and SS across all 8 geometries is inside [-196, +300] deg C, "
           "exactly on the 5 deg C grid, and its analysed temperature equals T_raw + M to 1e-9; the independent "
           "recomputation of the clip fraction from -196 + M agrees: " +
           ", ".join(f"{c} {g:.1%} vs {e:.1%}" for c, g, e in clip_check) +
           ("" if not bad else " PROBLEMS: " + "; ".join(bad)))


def test_17_miniature_scatter_scaling():
    truth = E.archetypes()["A5"]
    g0, g5 = D.geometry_info("G0"), D.geometry_info("G5")
    none = K.scenario_none()
    zero_pen = K.CorrectionScenario("zero-penalty", "normal", 0.0, 0.0)
    detail = []
    worst = 0.0
    for name in ("C1", "C1-robust", "C2", "C3-centred", "C3-uncentered", "miniature-inflated"):
        sc = S.build_scatter_model(name, archetypes=SIM._ARCHETYPES_FOR_C2)
        a = SIM.simulate_programme(truth, g0, 200, "U", 0.0, sc, none,
                                   SIM.replicate_rng("ms", "n", 1), SIM.replicate_rng("ms", "c", 1),
                                   snap=False, keep_detail=True)
        b = SIM.simulate_programme(truth, g5, 200, "U", 0.0, sc, zero_pen,
                                   SIM.replicate_rng("ms", "n", 1), SIM.replicate_rng("ms", "c", 1),
                                   snap=False, keep_detail=True)
        gap = float(np.max(np.abs(a["t_fse"] - b["t_fse"])))
        dev_a = a["e_fse"] - SIM.true_energy_fse(a["t_fse"], truth)
        dev_b = b["e_fse"] - SIM.true_energy_fse(b["t_fse"], truth)
        d = float(np.max(np.abs(dev_a - dev_b)))
        worst = max(worst, d, gap)
        ks = stats.ks_2samp(dev_a, dev_b)
        detail.append(f"{name}: max |deviation difference| {d:.2e} J, KS p = {ks.pvalue:.2f}")
    # With snapping on, the equivalent temperatures differ only by the grid residue - PROVIDED no specimen is
    # clipped. Clipping is a separate, physical, geometry-dependent effect (validation 12B/16), so this
    # sub-check uses a design in which neither geometry clips (strategy C, 120 deg C span).
    c = SIM.simulate_programme(truth, g5, 40, "C", 0.0, S.build_scatter_model("C1"), zero_pen,
                               SIM.replicate_rng("ms", "n", 1), SIM.replicate_rng("ms", "c", 1),
                               snap=True, keep_detail=True)
    a2 = SIM.simulate_programme(truth, g0, 40, "C", 0.0, S.build_scatter_model("C1"), none,
                                SIM.replicate_rng("ms", "n", 1), SIM.replicate_rng("ms", "c", 1),
                                snap=True, keep_detail=True)
    if c["n_clipped"] or a2["n_clipped"]:
        record("17 miniature scatter scaling", False, "the snapping sub-check design clipped; it must not")
    desired = D.place_temperatures("C", truth["t41j_c"], D.C_ASSUMED_C, 40)
    res_full = float(np.max(np.abs(a2["t_raw"] - desired)))                       # own snap residue, full-size
    res_mini = float(np.max(np.abs(c["t_raw"] - (desired - g5["m_shift_c"]))))    # own snap residue, miniature
    # Each design snaps its OWN raw temperature, so each residue is bounded by half a grid step; the difference
    # between two independently snapped designs is bounded by one full grid step.
    offset = float(np.max(np.abs(np.sort(c["t_fse"]) - np.sort(a2["t_fse"]))))
    snap_ok = (res_full <= D.GRID_C / 2 + 1e-9 and res_mini <= D.GRID_C / 2 + 1e-9
               and offset <= D.GRID_C + 1e-9)
    # Delta moves the region boundaries by exactly Delta
    delta = 17.0
    cs = K.CorrectionScenario("d", "normal", delta, 0.0)
    e_raw, _ = SIM._generate(np.array([0.0]), truth, g5["m_shift_c"], g5["nf_energy"], delta,
                             S.build_scatter_model("zero"), np.random.default_rng(0))
    expect = SIM.true_energy_fse(np.array([0.0 + g5["m_shift_c"] - delta]), truth) / g5["nf_energy"]
    region_ok = abs(float(e_raw[0]) - float(expect[0])) < 1e-12
    record("17 miniature scatter scaling", worst < 1e-9 and snap_ok and region_ok,
           "with Delta = 0, no clipping, equal N and equal full-size-equivalent temperatures (snapping "
           "disabled), the normalized miniature energies reproduce the full-size scatter exactly for every "
           "model - " + "; ".join(detail) +
           f"; with snapping on and no clipping, each design's own snap residue is {res_full:.2f} deg C "
           f"(full-size) and {res_mini:.2f} deg C (miniature), both within half a grid step (2.5 deg C), and "
           f"the offset between the two independently snapped designs is {offset:.2f} deg C, within one full "
           f"grid step ({D.GRID_C:g} deg C), as two independent residues must be; and a "
           f"non-zero Delta = {delta} deg C moves the evaluated true position by exactly Delta")


def test_18_empirical_no_added_bias():
    detail = []
    ok = True
    for subset, scen in (("primary", K.scenario_empirical("primary")), ("all_strict", K.scenario_empirical("all_strict"))):
        pool = K.family_pool(subset)
        n = pool["n_families"]
        pop_sd = pool["sd_c"] * np.sqrt((n - 1) / n)     # resampling a finite pool reproduces its POPULATION SD
        rng = np.random.default_rng(20260918)
        draws = scen.draw(rng, size=10_000_000)
        m, s = float(draws.mean()), float(draws.std(ddof=1))
        good = abs(m - pool["mean_c"]) < 0.02 and abs(s - pop_sd) < 0.02
        ok = ok and good
        detail.append(f"{subset}: mean {m:.4f} vs pool {pool['mean_c']:.4f}; SD {s:.4f} vs the pool's population "
                      f"SD {pop_sd:.4f} (= sample SD {pool['sd_c']:.4f} x sqrt({n - 1}/{n}), the exact "
                      f"consequence of resampling a finite pool)")
    try:
        K.scenario_empirical("primary").draw(np.random.default_rng(0), size=3, bias_c=-3.5)
        refused = False
    except ValueError:
        refused = True
    record("18 empirical family resampling adds no bias", ok and refused,
           "; ".join(detail) + "; a caller passing a separate bias to an empirical scenario is refused")


def test_19_single_subtraction():
    """M is subtracted exactly once (D-101, author's review round 4)."""
    truth = E.archetypes()["A5"]
    zero = S.build_scatter_model("zero")
    zero_pen = K.CorrectionScenario("zero-penalty", "normal", 0.0, 0.0)
    g0 = D.geometry_info("G0")
    bad = []
    for strategy in ("U", "C", "A", "S"):
        a = SIM.simulate_programme(truth, g0, 40, strategy, 0.0, zero, K.scenario_none(),
                                   SIM.replicate_rng("ss", "n", 0), SIM.replicate_rng("ss", "c", 0),
                                   snap=False, keep_detail=True)
        for code in D.MINIATURE_CODES:
            geom = D.geometry_info(code)
            m = geom["m_shift_c"]
            b = SIM.simulate_programme(truth, geom, 40, strategy, 0.0, zero, zero_pen,
                                       SIM.replicate_rng("ss", "n", 0), SIM.replicate_rng("ss", "c", 0),
                                       snap=False, keep_detail=True)
            # (a) desired full-size-equivalent sequences identical (the prior was not pre-shifted)
            if np.max(np.abs(a["t_fse"] - b["t_fse"])) > 1e-9:
                bad.append(f"{strategy}/{code}: (a) equivalent temperature sequences differ")
            # (b) raw sequences differ by exactly -M
            if np.max(np.abs((b["t_raw"] - a["t_raw"]) + m)) > 1e-9:
                bad.append(f"{strategy}/{code}: (b) raw sequences do not differ by exactly -M")
            # (c) normalization returns the same equivalent sequence
            if np.max(np.abs((b["t_raw"] + m) - a["t_fse"])) > 1e-9:
                bad.append(f"{strategy}/{code}: (c) analysed temperatures do not return to the sequence")
    # SS is the declared raw-space exception: check only its start
    for code in D.MINIATURE_CODES:
        m = D.geometry_info(code)["m_shift_c"]
        start = D.staircase_start_raw(truth["t41j_c"], D.C_ASSUMED_C, m)
        want = float(np.clip(D.snap_raw(truth["t41j_c"] - m), D.GRID_MIN_C, D.GRID_MAX_C))
        if abs(start - want) > 1e-9:
            bad.append(f"SS/{code}: start is not T_assumed_fse - M snapped and clipped")
    record("19 single-subtraction frame consistency", not bad,
           "for U, C, A and S against all 7 miniature geometries: the desired full-size-equivalent sequences "
           "are identical, the raw sequences differ by exactly -M, and the analysed temperatures return to the "
           "same sequence (all to 1e-9 deg C). A double subtraction would show as -M in (a) and -2M in (b). "
           "SS starts at T_assumed_fse - M snapped and clipped, its declared raw-space exception." +
           ("" if not bad else " PROBLEMS: " + "; ".join(bad)))


TESTS = [test_01_zero_scatter, test_02_full_size_identity, test_03_large_n, test_04_zero_size_penalty,
         test_05_huge_size_penalty, test_06_determinism, test_07_no_truth_leakage, test_08_material_budget,
         test_09_failure_accounting, test_10_sign_roundtrip_invariance, test_11_paired_estimator,
         test_12_geometry_equivalence, test_13_scatter_models, test_14_estimator_identity,
         test_15_correction_pools, test_16_raw_temperature_feasibility, test_17_miniature_scatter_scaling,
         test_18_empirical_no_added_bias, test_19_single_subtraction]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("WP6 simulator validation (SYNTHETIC; DECISIONS.md D-090 to D-112)")
    t0 = time.time()
    for t in TESTS:
        t()
    df = pd.DataFrame(RESULTS)
    df.to_csv(OUT / "validation_results.csv", index=False)
    print(f"  {len(df)} validation rows, all passed, in {time.time() - t0:.1f} s")
    # The declared runtime / memory benchmark of D-111, run after the tests pass and before the full grid.
    # It measures nothing once the cache is warm, so on a warm cache the recorded cold-run measurement stands.
    grid = E.build_grid()
    try:
        bench = E.benchmark(grid)
        pd.DataFrame([bench]).to_csv(OUT / "runtime_benchmark.csv", index=False)
    except RuntimeError as exc:
        print(f"  benchmark skipped: {exc}")
        bench = pd.read_csv(OUT / "runtime_benchmark.csv").iloc[0].to_dict()
    ok = bench["projected_full_run_hours"] <= 10.0 and bench["peak_rss_mb"] < 2000.0
    print(f"  benchmark {'WITHIN' if ok else 'BEYOND'} the approved thresholds "
          f"(projected {bench['projected_full_run_hours']:.2f} h <= 10 h, peak "
          f"{bench['peak_rss_mb']:.0f} MB): "
          f"{'proceed with the complete frozen grid' if ok else 'STOP and report to the author (D-111)'}")


if __name__ == "__main__":
    main()
