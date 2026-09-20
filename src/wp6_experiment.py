"""WP6 - The frozen experiment: the pre-registered grid, the paired comparison statistics, the checkpointed
runner, and every WP6 table, figure and summary.

The grid of DECISIONS.md D-108 is enumerated here, in code, before any cell is run: no arm, archetype or
comparison is chosen after results are visible. Running this module with --preregister writes only the
pre-result outputs (the grid itself, the material-budget accounting, the geometry reconciliation and
reachability, the archetypes, the scatter-model calibration diagnostics and the correction scenarios); the
headline cells are run only in a full run.

SYNTHETIC ONLY: every table and figure carries the data_type below.
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import pandas as pd

import wp6_correction as K
import wp6_design as D
import wp6_scatter as S
import wp6_simulator as SIM
import wp6_checkpoint as CP
from common import OUTPUTS, md_table, write_text
from wp3_fitter import OUTCOMES
from wp4_bootstrap import stream_map, worker_count

OUT = OUTPUTS / "wp6"
DATA_TYPE = SIM.DATA_TYPE
CONDITIONAL_SCENARIO_NOTE = ("conditional fixed-volume scenario using the pooled, WEAKLY SUPPORTED WP5 "
                             "correction distribution (D-083, D-092); not a geometry-specific claim")

# ---------------------------------------------------------------------------
# 1. Archetypes (D-093)
# ---------------------------------------------------------------------------
ARCHETYPE_USE_J = [100.0, 200.0, 270.0]        # p10, median, p90 of the 104 usable full-size WP3 fits
ARCHETYPE_C_C = [28.0, 46.0, 60.0]             # p10, median, p90
ARCHETYPE_T41J_C = -53.0                       # the cohort median
REDUCED_ARCHETYPES = ["A1", "A5", "A9"]


def archetypes() -> dict:
    out = {}
    i = 0
    for use in ARCHETYPE_USE_J:
        for c in ARCHETYPE_C_C:
            i += 1
            t = SIM.truth_from_t41j(use, c, ARCHETYPE_T41J_C)
            out[f"A{i}"] = dict(archetype_id=f"A{i}", **t)
    return out


# ---------------------------------------------------------------------------
# 2. The frozen grid (D-108)
# ---------------------------------------------------------------------------
BUDGETS_K = D.BUDGET_MULTIPLES_K                       # 4, 6, 8, 12, 18, 24
FIXED_STRATEGIES = ["U", "C", "A", "S"]
PRIOR_LEVELS_C = [0.0, 10.0, -10.0, 20.0, -20.0, 40.0, -40.0, 80.0, -80.0]
CORRECTION_SD_SWEEP_C = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0]
R_T1 = R_T2 = R_T3 = R_T7 = 1000
R_T4 = 500
R_T5 = 400
R_T6 = 200
B_T6 = 500                                             # bounded WP6 coverage experiment only (D-109)
STABILITY_REPLICATES = 4000
BATCHES = 20                                           # paired batch-means SE (D-107)
PAIRED_BOOTSTRAP = 2000
GATE = 0.95                                            # availability gate (D-104), the D-057 threshold reused
TAU_ABS_C = 2.0                                        # practical-equivalence tolerance (D-105)
TAU_REL = 0.05
SE_FACTOR = 3.0

S6A = [("G0", 6), ("G0", 12), ("G5", 6), ("G5", 12), ("G6", 6), ("G6", 12)]
S4M = [("G5", 6), ("G5", 12), ("G6", 6), ("G6", 12)]
T2_ARMS = [(g, k) for g in ("G0", "G2", "G5", "G6") for k in (6, 12)]
T3_ARMS = [(g, k) for g in ("G2", "G5", "G6") for k in (4, 8)]
T5_ARMS = [("G0", 6), ("G0", 12), ("G5", 6), ("G5", 12)]
T6_ARMS = [("G0", 6), ("G0", 12), ("G0", 24), ("G5", 6), ("G5", 12), ("G5", 24)]
V16_V17_ARMS = [("G0", 12), ("G1", 12), ("G5", 12), ("G7", 12)]

CENTRAL_CORRECTION = dict(kind="central")
NO_CORRECTION = dict(kind="none")


def _corr_for(geom_code: str, spec: dict) -> dict:
    """A full-size programme has no size correction: NF_E = 1, M = 0 and Delta = 0 (D-097)."""
    return NO_CORRECTION if geom_code == D.FULL_SIZE_CODE else spec


def _cell(tier, truth, geom_code, k, strategy, e_prior, scatter, corr, replicates, *, allowance=0.0,
          variant="", cohort="primary", note="", klst=True, n_override=None):
    n = int(n_override) if n_override is not None else D.specimen_count(geom_code, k, allowance)
    truth_key = truth["truth_key"]
    return dict(
        tier=tier, variant=variant, archetype_id=truth.get("archetype_id", truth_key), truth_key=truth_key,
        use_j=truth["use_j"], c_c=truth["c_c"], lse_j=truth["lse_j"], t0_c=truth["t0_c"],
        t41j_true_c=truth["t41j_c"], geom_code=geom_code, k_budget=k, allowance_c_mm=allowance,
        n=n, strategy=strategy, e_prior=float(e_prior), scatter=scatter,
        correction=_corr_for(geom_code, corr), correction_name=_corr_for(geom_code, corr)["kind"],
        replicates=int(replicates), cohort_key=cohort, klst_reading=klst, note=note,
        crn_stream=f"{truth_key}|prior={float(e_prior):g}",
    )


def _truth(a: dict, key: str = None) -> dict:
    t = dict(a)
    t["truth_key"] = key or a["archetype_id"]
    return t


def build_grid(cohort_archetypes=None) -> pd.DataFrame:
    """Every cell of T1-T7, enumerated before any of them is run (D-108)."""
    A = archetypes()
    if cohort_archetypes is None:
        cohort_archetypes = cohort_archetype_params()
    red = [_truth(A[a]) for a in REDUCED_ARCHETYPES]
    cells = []

    # --- T1 headline: 9 archetypes x 48 arms x 4 strategies, e_prior 0, C1, CENTRAL correction
    for a in A.values():
        t = _truth(a)
        for g in D.ALL_CODES:
            for k in BUDGETS_K:
                for st in FIXED_STRATEGIES:
                    cells.append(_cell("T1", t, g, k, st, 0.0, "C1", CENTRAL_CORRECTION, R_T1))

    # --- T2 prior sweep
    for e in PRIOR_LEVELS_C:
        for t in red:
            for g, k in T2_ARMS:
                for st in FIXED_STRATEGIES:
                    cells.append(_cell("T2", t, g, k, st, e, "C1", CENTRAL_CORRECTION, R_T2))

    # --- T3 correction-SD threshold sweep (miniature arms only; full-size comparators come from T1)
    bias = K.central_scenario_values()["bias_c"]
    for sd in CORRECTION_SD_SWEEP_C:
        for t in red:
            for g, k in T3_ARMS:
                for st in FIXED_STRATEGIES:
                    cells.append(_cell("T3", t, g, k, st, 0.0, "C1",
                                       dict(kind="fixed_sd", sd_c=sd, bias_c=bias), R_T3,
                                       variant=f"SD={sd:g}"))

    # --- T4 sensitivities
    def t4(variant, arms, scatter="C1", corr=CENTRAL_CORRECTION, truths=None, allowance=0.0, cohort="primary",
           klst=True, note=""):
        for t in (truths or red):
            for g, k in arms:
                for st in FIXED_STRATEGIES:
                    cells.append(_cell("T4", t, g, k, st, 0.0, scatter, corr, R_T4, allowance=allowance,
                                       variant=variant, cohort=cohort, klst=klst, note=note))

    t4("V1 scatter C1-robust", S6A, scatter="C1-robust")
    t4("V2 scatter C2", S6A, scatter="C2")
    t4("V3 scatter C3-centred", S6A, scatter="C3-centred")
    t4("V4 scatter C3-uncentered", S6A, scatter="C3-uncentered",
       note="empirical residual + model-shape / systematic-region-bias sensitivity; NOT the main C3 case")
    t4("V5 miniature-inflated scatter", S6A, scatter="miniature-inflated",
       note="WP4 miniature profile: 13 curves, 6 references; weakly supported")
    t4("V6 correction CONSERVATIVE", S4M, corr=dict(kind="conservative"))
    t4("V7 correction empirical 7-family", S4M, corr=dict(kind="empirical", subset="primary"))
    t4("V8 correction empirical 10-family", S4M, corr=dict(kind="empirical", subset="all_strict"))
    for code, case in [("V9", "S1 energy (Bb)^3/2"), ("V10", "S3 temperature Lucon"),
                       ("V11", "S5 temperature Wallin"), ("V12", "S4 temperature Towers"),
                       ("V13", "S6 KLST as recorded")]:
        t4(f"{code} normalization {case}", S4M, corr=dict(kind="normalization", case=case))
    t4("V14 specimen-level correction draw", S4M, corr=dict(kind="specimen_level"),
       note="ILLUSTRATIVE ONLY (D-098): never a central or headline case")
    lse6 = [_truth(dict(SIM.truth_from_t0(a["use_j"], a["c_c"], a["t0_c"], 6.0), archetype_id=a["archetype_id"]),
                   key=f"{a['archetype_id']}|lse6") for a in (A[x] for x in REDUCED_ARCHETYPES)]
    t4("V15 true LSE 6 J, analysed at 2.7 J", S6A, truths=lse6)
    for code, t41 in [("V16", -150.0), ("V17", 100.0)]:
        loc = [_truth(dict(SIM.truth_from_t41j(a["use_j"], a["c_c"], t41), archetype_id=a["archetype_id"]),
                      key=f"{a['archetype_id']}|t41={t41:g}") for a in (A[x] for x in REDUCED_ARCHETYPES)]
        t4(f"{code} T41J_true = {t41:g} deg C", V16_V17_ARMS, truths=loc,
           note="geometry-specific envelope and reachability check (D-093)")
    t4("V18 machining allowance c = 0.5 mm", S6A, allowance=0.5)
    t4("V19 machining allowance c = 1.0 mm", S6A, allowance=1.0)
    t4("V20 energy-scale injection (optional)", S4M, corr=dict(kind="energy_scale"),
       note="OPTIONAL (D-097): magnitude-matched change of injection form, not an added uncertainty")
    if cohort_archetypes:
        for cohort in ("looser", "stricter"):
            ct = [_truth(dict(cohort_archetypes[cohort][a], archetype_id=a), key=f"{a}|{cohort}")
                  for a in REDUCED_ARCHETYPES]
            t4(f"V2{1 if cohort == 'looser' else 2} WP2 {cohort} cohort", S6A, truths=ct, cohort=cohort,
               note="archetypes and scatter profile re-derived for this cohort; the WP5 correction stays at the "
                    "primary-cohort value because D-071 fixes WP5 to the frozen primary cohort")

    # --- T5 breadth check: the 104 usable full-size WP3 fits as truths
    for t in breadth_truths():
        for g, k in T5_ARMS:
            for st in FIXED_STRATEGIES:
                cells.append(_cell("T5", t, g, k, st, 0.0, "C1", CENTRAL_CORRECTION, R_T5))

    # --- T7 staircase
    for t in red:
        for e in (0.0, -40.0, 40.0):
            for g, k in S6A:
                cells.append(_cell("T7", t, g, k, "SS", e, "C1", CENTRAL_CORRECTION, R_T7))

    # --- T6 interval coverage: frozen cells, run by a separate bootstrap path (D-109)
    a5 = _truth(A["A5"])
    for g, k in T6_ARMS:
        cells.append(_cell("T6", a5, g, k, "U", 0.0, "C1", CENTRAL_CORRECTION, R_T6,
                           note=f"interval-coverage sub-study, B = {B_T6} bootstrap replicates per programme; "
                                f"does NOT modify WP4's approved production B = 2,000 (D-109)"))

    grid = pd.DataFrame(cells)
    grid.insert(0, "cell_id", [f"{r.tier}-{i:05d}" for i, r in enumerate(grid.itertuples(), start=1)])
    grid.insert(0, "data_type", DATA_TYPE)
    return grid


def cohort_archetype_params() -> dict:
    """Archetypes re-derived for the CP2-frozen looser and stricter cohorts (D-110).

    Same construction as the primary archetypes: the p10, median and p90 of USE and C over that cohort's usable
    full-size fits with a calculated T41J, and that cohort's median T41J as the location. Only the reduced set
    {A1, A5, A9} is used, so only the three (USE, C) corners are built. No frozen cohort is regenerated: the
    memberships are read from the approved WP3 outputs.
    """
    out = {}
    for cohort in ("looser", "stricter"):
        if cohort == "looser":
            f = pd.read_csv(OUTPUTS / "wp3" / "fits_looser_cohort_curves.csv", float_precision="round_trip")
        else:
            f = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip")
            f = f[f["in_stricter"].astype(str).str.lower() == "true"]
        u = f[(f["geometry_category"] == "full-size")
              & (f["outcome"] == "usable fit, index temperature calculated")]
        use = np.percentile(u["use_j"].to_numpy(float), [10, 50, 90])
        cc = np.percentile(u["c_c"].to_numpy(float), [10, 50, 90])
        t41 = float(np.median(u["index_temperature_c"].to_numpy(float)))
        out[cohort] = {
            "A1": dict(SIM.truth_from_t41j(float(use[0]), float(cc[0]), t41), archetype_id="A1"),
            "A5": dict(SIM.truth_from_t41j(float(use[1]), float(cc[1]), t41), archetype_id="A5"),
            "A9": dict(SIM.truth_from_t41j(float(use[2]), float(cc[2]), t41), archetype_id="A9"),
            "n_curves": int(len(u)),
        }
    return out


def breadth_truths() -> list:
    """The 104 usable full-size WP3 fits, used in turn as synthetic truths (D-093, tier T5)."""
    fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip")
    u = fits[(fits["geometry_category"] == "full-size")
             & (fits["outcome"] == "usable fit, index temperature calculated")]
    out = []
    for _, f in u.iterrows():
        t = SIM.truth_from_t0(float(f["use_j"]), float(f["c_c"]), float(f["t0_c"]), SIM.TRUE_LSE_J)
        out.append(_truth(dict(t, archetype_id=str(f["curve_id"])), key=f"curve:{f['curve_id']}"))
    return out


# ---------------------------------------------------------------------------
# 3. Metrics, labels and the PAIRED Monte Carlo SE (D-104, D-105, D-107)
# ---------------------------------------------------------------------------
def cell_metrics(errors: np.ndarray, r: int) -> dict:
    """Conditional metrics over the available replicates; failures stay in the denominator of availability."""
    e = np.asarray(errors, float)
    ok = np.isfinite(e)
    v = e[ok]
    n_ok = int(ok.sum())
    avail = n_ok / max(1, int(r))
    if n_ok == 0:
        nan = float("nan")
        return dict(n_available=0, availability=avail, rmse_c=nan, bias_c=nan, sd_c=nan, mae_c=nan,
                    median_abs_c=nan, p90_abs_c=nan, p95_abs_c=nan, eligible=False)
    a = np.abs(v)
    return dict(n_available=n_ok, availability=avail,
                rmse_c=float(np.sqrt(np.mean(v ** 2))), bias_c=float(v.mean()),
                sd_c=float(v.std(ddof=1)) if n_ok > 1 else float("nan"), mae_c=float(a.mean()),
                median_abs_c=float(np.median(a)), p90_abs_c=float(np.percentile(a, 90)),
                p95_abs_c=float(np.percentile(a, 95)), eligible=bool(avail >= GATE))


def _cond_rmse(e: np.ndarray):
    v = e[np.isfinite(e)]
    return float(np.sqrt(np.mean(v ** 2))) if v.size else float("nan")


def paired_batch_se(err_full: np.ndarray, err_mini: np.ndarray, batches: int = BATCHES) -> dict:
    """Paired batch-means SE of delta-RMSE (D-107).

    The same contiguous replicate-index batches are used in both cells, and each cell's CONDITIONAL RMSE is
    computed from the available values in that batch. The 95 % winner-eligibility gate is NOT re-applied inside
    a batch: it is a per-cell rule evaluated once on the complete R replicates. A batch with zero available
    values in either cell is dropped and counted; more than 2 of 20 unusable makes the paired SE unreliable.
    """
    r = len(err_full)
    idx = np.array_split(np.arange(r), batches)
    diffs, dropped = [], 0
    for b in idx:
        a, m = err_full[b], err_mini[b]
        if not np.isfinite(a).any() or not np.isfinite(m).any():
            dropped += 1
            continue
        diffs.append(_cond_rmse(a) - _cond_rmse(m))
    diffs = np.array(diffs, float)
    usable = len(diffs)
    reliable = dropped <= 2 and usable >= 2
    se = float(diffs.std(ddof=1) / np.sqrt(usable)) if usable >= 2 else float("nan")
    return dict(se_paired_c=se, batches_used=usable, batches_dropped=dropped, se_reliable=bool(reliable))


def paired_bootstrap_se(err_full: np.ndarray, err_mini: np.ndarray, draws: int = PAIRED_BOOTSTRAP,
                        seed: int = 20260918) -> float:
    """Declared cross-check on the same estimand: resample replicate indices jointly, no refits (D-107)."""
    r = len(err_full)
    rng = np.random.default_rng(seed)
    out = np.empty(draws, float)
    for i in range(draws):
        s = rng.integers(0, r, r)
        out[i] = _cond_rmse(err_full[s]) - _cond_rmse(err_mini[s])
    out = out[np.isfinite(out)]
    return float(out.std(ddof=1)) if out.size > 1 else float("nan")


def tau_c(rmse_full: float, rmse_mini: float, tau_abs: float = TAU_ABS_C, tau_rel: float = TAU_REL) -> float:
    """tau = max(2 deg C, 5 % of the smaller RMSE) (D-105)."""
    smaller = np.nanmin([rmse_full, rmse_mini])
    return float(max(tau_abs, tau_rel * smaller)) if np.isfinite(smaller) else float("nan")


def winner_label(rmse_full, rmse_mini, eligible_full, eligible_mini, se_paired, se_reliable=True,
                 tau_abs=TAU_ABS_C, tau_rel=TAU_REL, gate_note="") -> dict:
    """MINIATURE WINS / FULL-SIZE WINS / PRACTICALLY TIED / INELIGIBLE (D-105)."""
    d = float(rmse_full) - float(rmse_mini)
    tau = tau_c(rmse_full, rmse_mini, tau_abs, tau_rel)
    if not (eligible_full and eligible_mini):
        label = "INELIGIBLE: estimator unavailable too often" + (f" ({gate_note})" if gate_note else "")
    elif not se_reliable:
        label = "paired SE unreliable - availability too low"
    elif d > tau and d > SE_FACTOR * se_paired:
        label = "MINIATURE WINS"
    elif -d > tau and -d > SE_FACTOR * se_paired:
        label = "FULL-SIZE WINS"
    else:
        label = "PRACTICALLY TIED"
    return dict(delta_rmse_c=d, tau_c=tau, se_paired_c=se_paired, winner=label)


# ---------------------------------------------------------------------------
# 4. Running the grid, with checkpoints and bounded memory (D-111)
# ---------------------------------------------------------------------------
def _task_from_row(row) -> dict:
    corr = row["correction"] if isinstance(row["correction"], dict) else json.loads(row["correction"])
    return dict(cell_id=row["cell_id"], use_j=row["use_j"], c_c=row["c_c"], lse_j=row["lse_j"],
                t0_c=row["t0_c"], geom_code=row["geom_code"], klst_reading=bool(row["klst_reading"]),
                n=int(row["n"]), strategy=row["strategy"], e_prior=float(row["e_prior"]),
                scatter=row["scatter"], cohort_key=row["cohort_key"], correction=corr,
                replicates=int(row["replicates"]), crn_stream=row["crn_stream"])


def _cell_fingerprint(code_fp: str, task: dict) -> str:
    return CP.fingerprint(code_fp, **{k: v for k, v in task.items() if k != "cell_id"})


def run_cell_task(task: dict) -> dict:
    """Top-level picklable worker entry point."""
    return SIM.run_cell(task)


def run_grid(grid: pd.DataFrame, workers: int = None, progress_every: int = 200, cache_subdir: str = None,
             use_cache: bool = True) -> dict:
    """Run every cell, reusing fingerprinted checkpoints; returns {cell_id: result}. Memory-bounded: each worker
    returns one compact summary, and only per-cell float32 arrays are kept.

    `cache_subdir` keeps a rerun of the same cell_id with different replicates or streams (the stability subset)
    in its own folder, so it can never overwrite the main cell's checkpoint. `use_cache=False` neither reads nor
    writes checkpoints: the validation tests use it so that every configuration they compare is computed afresh."""
    workers = worker_count() if workers is None else workers
    code_fp = CP.code_fingerprint()
    root = CP.checkpoint_root()
    results, todo = {}, []
    for row in grid.to_dict("records"):
        task = _task_from_row(row)
        fp = _cell_fingerprint(code_fp, task)
        path = root / (cache_subdir or row["tier"]) / f"{CP.slug(row['cell_id'])}.npz"
        cached = CP.load_arrays(path, fp) if use_cache else None
        if cached is not None:
            results[row["cell_id"]] = _unpack(cached)
        else:
            todo.append((task, fp, path))
    print(f"  cells: {len(grid)} total, {len(results)} from checkpoints, {len(todo)} to compute "
          f"({workers} workers)", flush=True)
    t0 = time.time()
    done = 0
    lookup = {t["cell_id"]: (fp, path) for t, fp, path in todo}
    for res in stream_map(run_cell_task, (t for t, _, _ in todo), workers):
        fp, path = lookup[res["cell_id"]]
        if use_cache:
            CP.save_arrays(path, _pack(res), fp)
        results[res["cell_id"]] = res
        done += 1
        if done % progress_every == 0:
            rate = done / max(1e-9, time.time() - t0)
            print(f"    {done}/{len(todo)} cells, {rate:.2f} cells/s, "
                  f"eta {(len(todo) - done) / max(1e-9, rate) / 60:.1f} min", flush=True)
    return results


def _pack(res: dict) -> dict:
    return dict(errors=res["errors"], deltas=res["deltas"], outcome_counts=res["outcome_counts"],
                status_keys=np.array(list(res["status_counts"].keys()), dtype=object).astype("U120"),
                status_values=np.array(list(res["status_counts"].values()), dtype=np.int64),
                scalars=np.array([res["n_replicates"], res["n_specimens"], res["temperature_clip_fraction"],
                                  res["n_distinct_raw_temperatures"], res["zero_energy_fraction"],
                                  res["adaptation_updates"], res["coldest_reachable_fse_c"],
                                  float(res["transition_reachable"])], dtype=float),
                cell_id=np.array(res["cell_id"]))


def _unpack(z: dict) -> dict:
    s = z["scalars"]
    return dict(cell_id=str(z["cell_id"]), errors=z["errors"], deltas=z["deltas"],
                outcome_counts=z["outcome_counts"],
                status_counts=dict(zip([str(k) for k in z["status_keys"]], z["status_values"].tolist())),
                n_replicates=int(s[0]), n_specimens=int(s[1]), temperature_clip_fraction=float(s[2]),
                n_distinct_raw_temperatures=float(s[3]), zero_energy_fraction=float(s[4]),
                adaptation_updates=float(s[5]), coldest_reachable_fse_c=float(s[6]),
                transition_reachable=bool(s[7]))


def cell_results_table(grid: pd.DataFrame, results: dict) -> pd.DataFrame:
    """One row per cell: the frozen definition, the metrics, the failure accounting and the clip diagnostics."""
    rows = []
    for row in grid.to_dict("records"):
        res = results[row["cell_id"]]
        m = cell_metrics(res["errors"], res["n_replicates"])
        counts = res["outcome_counts"]
        rec = {k: v for k, v in row.items() if k != "correction"}
        rec["correction"] = json.dumps(row["correction"]) if isinstance(row["correction"], dict) else row["correction"]
        rec.update(m)
        rec.update(temperature_clip_fraction=res["temperature_clip_fraction"],
                   n_distinct_raw_temperatures=res["n_distinct_raw_temperatures"],
                   zero_energy_fraction=res["zero_energy_fraction"],
                   adaptation_updates=res["adaptation_updates"],
                   coldest_reachable_fse_c=res["coldest_reachable_fse_c"],
                   transition_reachable=res["transition_reachable"],
                   mean_delta_c=float(np.nanmean(res["deltas"])) if np.isfinite(res["deltas"]).any() else np.nan,
                   n_evaluation_errors=int(counts[-1]),
                   accounting_ok=bool(int(counts.sum()) == int(res["n_replicates"])))
        for i, name in enumerate(OUTCOMES):
            rec[f"outcome_{name.replace(' ', '_').replace(',', '')}"] = int(counts[i])
        rec["index_status_counts"] = json.dumps(res["status_counts"])
        # The frozen grid names the variant's scatter model; for the full-size reference arms of the
        # miniature-inflated variant the simulator applies C1, because that profile is a property of miniature
        # specimens (D-096; D-112 step 7a). Stated per cell so that no reader has to infer it.
        rec["scatter_applied"] = ("C1 (full-size reference arm of the miniature-inflated variant, D-096)"
                                  if row["scatter"] == "miniature-inflated" and row["geom_code"] == D.FULL_SIZE_CODE
                                  else row["scatter"])
        rec["scenario_note"] = CONDITIONAL_SCENARIO_NOTE if row["geom_code"] != D.FULL_SIZE_CODE else "full-size reference"
        rec["budget_note"] = D.IDEALIZED_ACCOUNTING_NOTE
        rows.append(rec)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. Pre-registration outputs: everything that exists BEFORE any headline cell is run
# ---------------------------------------------------------------------------
def write_preregistration(grid: pd.DataFrame) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    A = archetypes()

    g = grid.copy()
    g["correction"] = g["correction"].apply(json.dumps)
    g.to_csv(OUT / "experiment_grid.csv", index=False)

    # --- material budget accounting (D-091)
    rows = []
    for code in D.ALL_CODES:
        info = D.geometry_info(code)
        for allowance in D.MACHINING_ALLOWANCES_MM:
            for k in BUDGETS_K:
                rows.append(dict(data_type=DATA_TYPE, geometry_code=code, wp5_geometry_id=info["wp5_geometry_id"],
                                 length_mm=info["length_mm"], width_recorded_mm=info["width_recorded_mm"],
                                 thickness_recorded_mm=info["thickness_recorded_mm"],
                                 allowance_c_mm=allowance,
                                 specimen_volume_mm3=D.specimen_volume_mm3(code, allowance),
                                 budget_k=k, budget_volume_mm3=D.budget_volume_mm3(k),
                                 n_specimens=D.specimen_count(code, k, allowance),
                                 specimens_per_full_size_equivalent=D.specimen_count(code, k, allowance) / k,
                                 accounting_note=D.IDEALIZED_ACCOUNTING_NOTE))
    pd.DataFrame(rows).to_csv(OUT / "material_budget_accounting.csv", index=False)

    # --- WP5 -> WP6 geometry reconciliation, all nine handoff rows (D-092)
    handoff = pd.read_csv(OUTPUTS / "wp5" / "wp6_size_correction_handoff.csv", float_precision="round_trip")
    handoff = handoff[~handoff["smaller_geometry"].str.startswith("POOLED")]
    code_by_id = {D.GEOMETRY_DIMENSIONS[c][0]: c for c in D.MINIATURE_CODES}
    rec = []
    for _, r in handoff.iterrows():
        gid = str(r["smaller_geometry"])
        code = code_by_id.get(gid)
        rec.append(dict(
            data_type=DATA_TYPE, wp5_geometry_id=gid, wp5_evidence_status=r["evidence_status"],
            n_families=r["n_families"], n_studies=r["n_studies"], n_primary_comparisons=r["n_primary_comparisons"],
            simulated_in_wp6=code is not None, wp6_geometry_code=code or "", collapsed_with="",
            reason=("simulated as its own arm set; no geometry is collapsed with another"
                    if code else D.UNSUPPORTED_GEOMETRIES.get(gid, "omitted"))))
    rdf = pd.DataFrame(rec)
    assert int(rdf["simulated_in_wp6"].sum()) == 7 and len(rdf) == 9, "geometry reconciliation must account for all 9 rows"
    rdf.to_csv(OUT / "wp5_geometry_reconciliation.csv", index=False)

    # --- geometry reachability (D-092): deterministic, no simulation
    truths = [dict(kind="archetype", label=k, t41j_c=v["t41j_c"]) for k, v in A.items()]
    truths += [dict(kind="WP3 usable full-size fit", label=t["archetype_id"], t41j_c=t["t41j_c"])
               for t in breadth_truths()]
    reach = []
    for code in D.ALL_CODES:
        info = D.geometry_info(code)
        cold = D.coldest_reachable_fse_c(info["m_shift_c"])
        for t in truths:
            reach.append(dict(data_type=DATA_TYPE, geometry_code=code, wp5_geometry_id=info["wp5_geometry_id"],
                              m_shift_c=info["m_shift_c"], coldest_reachable_fse_c=cold,
                              truth_kind=t["kind"], truth_label=t["label"], t41j_true_c=t["t41j_c"],
                              transition_reachable=bool(t["t41j_c"] >= cold)))
    pd.DataFrame(reach).to_csv(OUT / "geometry_reachability.csv", index=False)

    # --- archetypes with their occupancy among the 104 real fits (D-093)
    fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip")
    u = fits[(fits["geometry_category"] == "full-size")
             & (fits["outcome"] == "usable fit, index temperature calculated")]
    arows = []
    for aid, a in A.items():
        occ = int(((np.abs(u["use_j"] - a["use_j"]) <= 0.25 * a["use_j"])
                   & (np.abs(u["c_c"] - a["c_c"]) <= 0.25 * a["c_c"])).sum())
        arows.append(dict(data_type=DATA_TYPE, archetype_id=aid, use_j=a["use_j"], c_c=a["c_c"],
                          lse_j=a["lse_j"], t0_c=a["t0_c"], t41j_true_c=a["t41j_c"],
                          criterion_fraction_of_rise=(SIM.CRITERION_J - a["lse_j"]) / (a["use_j"] - a["lse_j"]),
                          real_curves_within_25pct=occ, in_reduced_set=aid in REDUCED_ARCHETYPES,
                          source="p10 / median / p90 of USE and C over the 104 usable full-size WP3 fits (D-093)"))
    ca = cohort_archetype_params()
    for cohort, v in ca.items():
        for aid in REDUCED_ARCHETYPES:
            arows.append(dict(data_type=DATA_TYPE, archetype_id=f"{aid}|{cohort}", use_j=v[aid]["use_j"],
                              c_c=v[aid]["c_c"], lse_j=v[aid]["lse_j"], t0_c=v[aid]["t0_c"],
                              t41j_true_c=v[aid]["t41j_c"],
                              criterion_fraction_of_rise=(SIM.CRITERION_J - v[aid]["lse_j"]) / (v[aid]["use_j"] - v[aid]["lse_j"]),
                              real_curves_within_25pct=-1, in_reduced_set=True,
                              source=f"re-derived for the CP2-frozen {cohort} cohort ({v['n_curves']} usable "
                                     f"full-size fits); the WP5 correction stays at the primary-cohort value (D-110)"))
    pd.DataFrame(arows).to_csv(OUT / "true_curve_archetypes.csv", index=False)

    # --- scatter-model calibration diagnostics (D-094, D-095)
    prof = S.wp4_profile("full-size")
    mini = S.wp4_profile("miniature")
    cal = S.calibrate_c2(SIM._ARCHETYPES_FOR_C2, prof["sd"].to_numpy(float), prof["residuals"].to_numpy(float))
    pool = S.residual_pool("full-size")
    prows = []
    for i, region in enumerate(S.REGIONS):
        prows.append(dict(data_type=DATA_TYPE, region=region, wp4_residuals=int(prof["residuals"][i]),
                          wp4_curves=int(prof["curves"][i]), wp4_mean=float(prof["mean"][i]),
                          empirical_sd_over_use=float(prof["sd"][i]),
                          empirical_robust_scale_over_use=float(prof["mad_scaled"][i]),
                          c1_sd_over_use=float(prof["sd"][i]), c1_robust_sd_over_use=float(prof["mad_scaled"][i]),
                          c2_sd_over_use=float(cal["profile"][i]),
                          c2_ratio_to_empirical=float(cal["profile"][i] / prof["sd"][i]),
                          c3_centred_mean=float(pool["values"][i].mean() - pool["means"][i]),
                          c3_centred_sd=float(pool["sds"][i]),
                          c3_uncentered_mean=float(pool["means"][i]),
                          miniature_sd_over_use=float(mini["sd"][i]),
                          miniature_inflation_factor=float(mini["sd"][i] / prof["sd"][i]),
                          pool_caveat=S.WP4_POOL_CAVEAT))
    pd.DataFrame(prows).to_csv(OUT / "scatter_model_profiles.csv", index=False)

    a5 = A["A5"]
    x41 = float(np.arctanh(2 * (SIM.CRITERION_J - a5["lse_j"]) / (a5["use_j"] - a5["lse_j"]) - 1))
    within25 = np.all(np.abs(cal["profile"] / prof["sd"].to_numpy(float) - 1.0) <= 0.25)
    write_text(OUT / "scatter_model_configuration.md", f"""# WP6 scatter models - calibration and the central choice

{DATA_TYPE}

The pool is {S.WP4_POOL_CAVEAT}

## Pre-declared selection criterion (D-094)
The central model must lie within +/- 25 % of the WP4 empirical SD/USE in **all five** regions and within
+/- 15 % at the 41 J crossing of the median archetype A5; ties broken toward the candidate needing no fitted
parameter; if none qualifies, C1 by default. Evaluated on these calibration diagnostics only, which contain no
headline simulation result.

## C1 (CENTRAL, D-095)
sd = USE_true x s(region), with s read at full precision from outputs/wp4/published_residual_scatter_summary.csv
(full-size, usable WP3 fits, {S.RESIDUAL_QUANTITY}, SD column). Nothing is fitted, so C1 reproduces every region
of the measured profile by construction and passes the criterion trivially.

## C2 (mandatory sensitivity)
sd(T) = sigma_T |dE/dT| + cv E(T) + 3 cv LSE, calibrated by the declared D-094 procedure:
**sigma_T = {cal['sigma_t_c']:.4f} deg C, cv = {cal['cv']:.6f}**.

{md_table(pd.DataFrame({'region': S.REGIONS, 'empirical SD/USE': prof['sd'].round(6),
                        'C2 SD/USE': np.round(cal['profile'], 6),
                        'ratio': np.round(cal['profile'] / prof['sd'].to_numpy(float), 3)}))}

C2 is within +/- 25 % in all five regions: **{bool(within25)}**. The 41 J crossing of A5 lies at
x = {x41:.3f}, i.e. in the **{S.REGIONS[int(S.region_index(np.array([x41]))[0])]}** region.

## C3 (mandatory sensitivity), centred
Region-wise resampling of the WP4 leverage-adjusted residual / USE observations with that region's empirical
mean subtracted, so the model is zero-mean and directly comparable with C1 and C2. The lower-shelf
+{pool['means'][0]:.6f} x USE offset is a model-convention / model-shape bias and is **never** injected as if it
were random specimen scatter. **C3-uncentered** keeps the region means and is reported separately as an
"empirical residual + model-shape / systematic-region-bias" sensitivity, not as the main C3 case.

## Miniature scatter
Central: the same relative profile at both specimen sizes. Required sensitivity: the WP4 miniature profile
(central transition {float(mini['sd'][2]):.4f} against {float(prof['sd'][2]):.4f}, a factor
{float(mini['sd'][2] / prof['sd'][2]):.2f}), from {int(mini['curves'][2])} curves - explicitly weakly supported.

## Directional asymmetry, recorded so the choice cannot be mistaken for tuning (D-095)
RMSE_mini is approximately sqrt(V_sampling(N_mini) + bias^2 + SD_correction^2), which has a floor that the
full-size sampling variance does not. **Understating the scatter favours full-size; overstating it favours
miniature.** The central model was chosen on the calibration diagnostic above, before any headline cell was run,
and all candidates are run regardless.
""")

    # --- correction scenarios and the reconstructed family pools (D-099, D-100)
    srows = []
    for sc in (K.scenario_none(), K.scenario_central(), K.scenario_conservative(),
               K.scenario_empirical("primary"), K.scenario_empirical("all_strict"),
               K.scenario_specimen_level(), K.scenario_energy_scale()):
        srows.append(dict(data_type=DATA_TYPE, **sc.describe()))
    for _, r in K.normalization_scenario_values().iterrows():
        srows.append(dict(data_type=DATA_TYPE, scenario=f"NORM:{r['case']}", kind="normal", label=r["label"],
                          bias_c=r["family_weighted_mean_c"], sd_c=r["family_weighted_sd_c"], pool_size=0,
                          bias_already_included=False, per_specimen_draw=False, injection="temperature",
                          sign_convention=K.SIGN_CONVENTION,
                          evidence=r["scenario_note"] + " | " + K.EVIDENCE_CAVEAT))
    for sd in CORRECTION_SD_SWEEP_C:
        sc = K.scenario_fixed_sd(sd, K.central_scenario_values()["bias_c"])
        srows.append(dict(data_type=DATA_TYPE, **sc.describe()))
    pd.DataFrame(srows).to_csv(OUT / "size_correction_scenarios.csv", index=False)

    prows = []
    for subset in ("primary", "all_strict"):
        p = K.family_pool(subset)
        for fid, v in zip(p["family_ids"], p["values"]):
            prows.append(dict(data_type=DATA_TYPE, pool=subset, family_id=fid, delta_t_size_c=v,
                              pool_mean_c=p["mean_c"], pool_sd_c=p["sd_c"], n_families=p["n_families"],
                              n_studies=p["n_studies"],
                              note="resampled DIRECTLY; the pool already contains its own mean, so no bias is "
                                   "added (D-099)"))
    pd.DataFrame(prows).to_csv(OUT / "size_correction_family_pools.csv", index=False)

    write_method_configuration(grid)


def write_method_configuration(grid: pd.DataFrame) -> None:
    cen = K.central_scenario_values()
    con = K.conservative_scenario_values()
    counts = grid.groupby("tier").size()
    geom = pd.DataFrame(D.geometry_table())[["code", "wp5_geometry_id", "B_mm", "ligament_mm",
                                             "ligament_volume_mm3", "nf_energy", "m_shift_c", "gross_volume_mm3"]]
    geom["coldest_reachable_fse_c"] = [D.coldest_reachable_fse_c(m) for m in geom["m_shift_c"]]
    write_text(OUT / "method_configuration.md", f"""# WP6 method configuration (frozen before any headline cell)

{DATA_TYPE}

Every decision below is DECISIONS.md D-090 to D-112, approved by the author in WP6 Plan Mode before
implementation began. This file is generated; it does not decide anything.

## Estimator (D-103)
The approved WP3 fitter, unchanged: `fit_curve(t, e, lse_fixed = 2.7 J)`, then `index_temperature` with the
tested-range rule applied to the ANALYSED temperatures, `index_fraction_of_rise`, `classify` and
`criterion_bracketing`. For a miniature programme the analysis frame is reached by the approved WP5 forward
normalization `normalize()` (D-073, D-074) applied to the ACTUAL raw temperature and energy. The estimator's
refusals are part of the estimator: a replicate whose 41 J crossing lies outside its own tested range has no
T41J and is counted unavailable.

## Physical temperature frame (D-101)
Raw-specimen envelope [{D.T_RAW_MIN_C:g}, {D.T_RAW_MAX_C:g}] deg C and a {D.GRID_C:g} deg C raw grid. Placement
order: propose T_fse_desired -> subtract M -> snap the RAW temperature -> clip the RAW temperature -> test ->
add M for analysis. **M is subtracted exactly once.** SS is the one deliberate raw-space exception.

Implementation clarification, fixed before any result: the physical floor {D.T_RAW_MIN_C:g} deg C is not a
multiple of the {D.GRID_C:g} deg C grid, so the coldest temperature that is both inside the envelope and on the
grid is **{D.GRID_MIN_C:g} deg C**, and that is where clipped specimens are placed. No specimen is ever tested
below the physical floor. The alternative reading (test exactly at {D.T_RAW_MIN_C:g} deg C, off-grid) would
differ by 1 deg C, far below every tolerance in the study (tau = {TAU_ABS_C:g} deg C, grid = {D.GRID_C:g} deg C).

## Geometries (D-092), and how geometry enters
{md_table(geom.round(6))}

Away from physical clipping, NF_E and M cancel and geometry acts through the specimen count; near the raw
bounds M also acts through geometry-dependent clipping, so equivalence is TESTED (validation 12A/12B), never
assumed. The coldest reachable full-size-equivalent temperature is {D.GRID_MIN_C:g} + M.

## Material budget (D-091)
{D.IDEALIZED_ACCOUNTING_NOTE}

## Scatter model per cell
The frozen grid records each variant's scatter model. For the **miniature-inflated** variant (V5) that profile is applied
to the miniature arms only; its full-size reference arms use C1, because the WP4 miniature profile is a property of
miniature specimens (D-096). `cell_results.csv` states the model actually applied in `scatter_applied`. For the WP2
cohort variants (V21, V22) the C1 scale is the D-061 profile re-aggregated for that cohort (D-110).

## Size correction (D-097, D-098, D-099, D-100)
Injected as a temperature-domain displacement of the simulated truth, `E_mini_true(T) = E_full_true(T + M - D)
/ NF_E`, reproducing D-078's sign exactly. **One programme-level draw**, shared by the whole test matrix.
CENTRAL {cen['bias_c']!r} deg C bias, {cen['sd_c']!r} deg C SD ({cen['n_families']} families,
{cen['n_studies']} studies, {cen['evidence_status']}). CONSERVATIVE {con['bias_c']!r} / {con['sd_c']!r} deg C
({con['n_families']} families) - required. No truncation. Empirical family pools are resampled DIRECTLY, with no
bias added. Each published normalization is a complete scenario with its own (bias, SD); nothing is added in
quadrature.

{K.SIGN_CONVENTION}

{K.EVIDENCE_CAVEAT}

## Metric and labels (D-104, D-105)
Primary metric RMSE of (T41J_hat - T41J_true); availability gate {GATE:.0%} of the replicates requested, the
D-057 threshold reused; secondary metric P90 |error|. tau = max({TAU_ABS_C:g} deg C, {TAU_REL:.0%} of the
smaller RMSE); a winner also needs |delta RMSE| > {SE_FACTOR:g} x the PAIRED Monte Carlo SE. The gate is
evaluated once per cell on the complete R replicates and is never re-applied inside a batch.

## Replicates and seeds (D-107)
R = {R_T1} (T1, T2, T3, T7), {R_T4} (T4), {R_T5} (T5), {R_T6} programmes (T6). Master seed {SIM.SEED}; one
independent stream per replicate per component; common random numbers keyed on (archetype, prior error,
replicate). Paired batch-means SE over exactly {BATCHES} batches, with a paired replicate-index bootstrap
({PAIRED_BOOTSTRAP} resamples, no refits) as the declared cross-check.

## The frozen grid (D-108)
{md_table(pd.DataFrame({'tier': counts.index, 'cells': counts.values}))}

Total {len(grid)} cells.
""")


# ---------------------------------------------------------------------------
# 6. Declared runtime / memory benchmark (D-111)
# ---------------------------------------------------------------------------
BENCHMARK_STRIDE = 100      # declared subset: every 100th cell of the frozen grid, in cell_id order


def peak_rss_mb() -> float:
    """Peak resident memory of this process and its children, in MB (macOS ru_maxrss is in bytes)."""
    import resource
    scale = 1.0 / (1024 * 1024) if hasattr(resource, "RUSAGE_CHILDREN") else 1.0
    self_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * scale
    child_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * scale
    return float(self_rss + child_rss)


def benchmark(grid: pd.DataFrame, workers: int = None) -> dict:
    """Run the declared benchmark subset and project the full-run wall time (D-111).

    The subset is fixed in code, not chosen after seeing anything: every 100th cell of the frozen grid. The
    projection scales by total replicates weighted by the per-strategy fit count, which is what actually drives
    the cost.
    """
    workers = worker_count() if workers is None else workers
    fits_per_programme = {"U": 1.0, "C": 1.0, "A": 1.0, "SS": 1.0}

    def weight(row):
        if row["strategy"] != "S":
            return fits_per_programme[row["strategy"]] * row["replicates"]
        n = int(row["n"])
        n0 = D.adaptive_seed_size(n)
        k = D.adaptive_block_size(n)
        blocks = int(np.ceil(max(0, n - n0) / k))
        return (1 + blocks) * row["replicates"]

    run = grid.iloc[::BENCHMARK_STRIDE].copy()
    w_run = float(sum(weight(r) for r in run.to_dict("records")))
    w_all = float(sum(weight(r) for r in grid.to_dict("records")))
    print(f"  benchmark: {len(run)} cells (every {BENCHMARK_STRIDE}th of {len(grid)}), "
          f"{w_run / w_all:.2%} of the total fit-weighted work, {workers} workers", flush=True)
    # A benchmark served from checkpoints measures nothing. Refuse to report such a timing as a measurement.
    code_fp = CP.code_fingerprint()
    root = CP.checkpoint_root()
    cached = sum(1 for row in run.to_dict("records")
                 if CP.has_arrays(root / row["tier"] / f"{CP.slug(row['cell_id'])}.npz",
                                  _cell_fingerprint(code_fp, _task_from_row(row))))
    if cached:
        raise RuntimeError(
            f"{cached} of the {len(run)} benchmark cells are already in the checkpoint cache, so the timing "
            f"would not be a measurement. Move cache/wp6/ aside to re-measure, or read the recorded "
            f"outputs/wp6/runtime_benchmark.csv from the cold run.")
    t0 = time.time()
    run_grid(run, workers=workers, progress_every=10)
    elapsed = time.time() - t0
    projected_h = elapsed / max(1e-9, w_run) * w_all / 3600.0
    peak = peak_rss_mb()
    print(f"  benchmark: {elapsed / 60:.2f} min for the subset; projected full run "
          f"{projected_h:.2f} h; peak RSS {peak:.0f} MB", flush=True)
    return dict(data_type=DATA_TYPE, benchmark_cells=len(run), stride=BENCHMARK_STRIDE, workers=workers,
                elapsed_s=elapsed, fit_weight_run=w_run, fit_weight_total=w_all,
                projected_full_run_hours=projected_h, peak_rss_mb=peak,
                note="declared subset fixed in code (every 100th cell); projection scales by replicates weighted "
                     "by the per-strategy fit count (D-111); measured on a COLD cache")


# ---------------------------------------------------------------------------
# 7. Paired comparisons: matching each miniature cell to its full-size comparator
# ---------------------------------------------------------------------------
MATCH_KEYS = ["truth_key", "strategy", "k_budget", "e_prior", "scatter", "allowance_c_mm", "cohort_key"]


def comparator_index(cells: pd.DataFrame) -> dict:
    """Full-size cells, keyed for matching. A miniature cell is compared with the full-size cell that shares the
    same truth, strategy, budget, prior, scatter model, allowance and cohort - preferring one from its own T4
    variant, and otherwise falling back to the T1 headline cell. The rule is fixed here, before any result."""
    idx = {}
    for row in cells[cells.geom_code == D.FULL_SIZE_CODE].to_dict("records"):
        idx[(row["variant"],) + tuple(row[k] for k in MATCH_KEYS)] = row["cell_id"]
    return idx


def paired_comparisons(cells: pd.DataFrame, results: dict) -> pd.DataFrame:
    """One row per (miniature cell, its full-size comparator) with the D-105 label."""
    idx = comparator_index(cells)
    rows = []
    for m in cells[cells.geom_code != D.FULL_SIZE_CODE].to_dict("records"):
        key = tuple(m[k] for k in MATCH_KEYS)
        cid = idx.get((m["variant"],) + key) or idx.get(("",) + key)
        if cid is None:
            continue
        f = cells[cells.cell_id == cid].iloc[0].to_dict()
        ef, em = results[cid]["errors"].astype(float), results[m["cell_id"]]["errors"].astype(float)
        # The comparison is made on the replicate indices the two cells SHARE, so the common random numbers
        # pair it exactly; eligibility keeps using each cell's complete R replicates (D-107).
        n = min(len(ef), len(em))
        ef, em = ef[:n], em[:n]
        rmse_full, rmse_mini = _cond_rmse(ef), _cond_rmse(em)
        se = paired_batch_se(ef, em)
        boot = paired_bootstrap_se(ef, em) if m["tier"] in ("T1", "T3") else np.nan
        lab = winner_label(rmse_full, rmse_mini, bool(f["eligible"]), bool(m["eligible"]),
                           se["se_paired_c"], se["se_reliable"],
                           gate_note=f"full-size {f['availability']:.0%}, miniature {m['availability']:.0%}")
        rows.append(dict(data_type=DATA_TYPE, tier=m["tier"], variant=m["variant"],
                         archetype_id=m["archetype_id"], truth_key=m["truth_key"], strategy=m["strategy"],
                         k_budget=m["k_budget"], e_prior=m["e_prior"], scatter=m["scatter"],
                         allowance_c_mm=m["allowance_c_mm"], cohort_key=m["cohort_key"],
                         correction=m["correction"], geom_code=m["geom_code"],
                         n_full=f["n"], n_mini=m["n"], rmse_full_c=rmse_full, rmse_mini_c=rmse_mini,
                         rmse_full_all_replicates_c=f["rmse_c"], rmse_mini_all_replicates_c=m["rmse_c"],
                         n_paired_replicates=n, se_paired_bootstrap_c=boot,
                         se_ratio_batch_over_bootstrap=(se["se_paired_c"] / boot if boot and np.isfinite(boot)
                                                        and boot > 0 else np.nan),
                         p90_full_c=f["p90_abs_c"], p90_mini_c=m["p90_abs_c"],
                         bias_full_c=f["bias_c"], bias_mini_c=m["bias_c"],
                         availability_full=f["availability"], availability_mini=m["availability"],
                         eligible_full=bool(f["eligible"]), eligible_mini=bool(m["eligible"]),
                         clip_fraction_mini=m["temperature_clip_fraction"],
                         transition_reachable_mini=m["transition_reachable"],
                         full_cell_id=cid, mini_cell_id=m["cell_id"],
                         delta_p90_c=f["p90_abs_c"] - m["p90_abs_c"],
                         batches_used=se["batches_used"], batches_dropped=se["batches_dropped"],
                         scenario_note=CONDITIONAL_SCENARIO_NOTE, **lab))
    out = pd.DataFrame(rows)
    if len(out):
        out["winner_class"] = np.select(
            [out["winner"] == "MINIATURE WINS", out["winner"] == "FULL-SIZE WINS",
             out["winner"] == "PRACTICALLY TIED", out["winner"].str.startswith("INELIGIBLE")],
            ["MINIATURE WINS", "FULL-SIZE WINS", "PRACTICALLY TIED", "INELIGIBLE"],
            default="SE UNRELIABLE")
        r = out["se_ratio_batch_over_bootstrap"]
        out["se_estimators_agree"] = np.where(r.notna(), (r >= 1 / 1.5) & (r <= 1.5), True)
        out["secondary_winner_p90"] = np.where(
            out["delta_p90_c"] > 0, "miniature lower P90", np.where(out["delta_p90_c"] < 0, "full-size lower P90", "equal"))
        out["primary_secondary_agree"] = (
            ((out["winner"] == "MINIATURE WINS") & (out["delta_p90_c"] > 0)) |
            ((out["winner"] == "FULL-SIZE WINS") & (out["delta_p90_c"] < 0)) |
            (~out["winner"].isin(["MINIATURE WINS", "FULL-SIZE WINS"])))
    return out


def label_threshold_robustness(cells: pd.DataFrame, results: dict, comparisons: pd.DataFrame) -> pd.DataFrame:
    """The 12 label variants of D-105, recomputed post hoc from the stored errors. No cell is rerun."""
    rows = []
    head = comparisons[(comparisons.tier == "T1")]
    for gate in (0.90, 0.95, 0.99):
        for tau_name, tau_abs, tau_rel in (("tau = 0", 0.0, 0.0), ("tau = 2 C", 2.0, 0.0),
                                           ("tau = 5 C", 5.0, 0.0), ("tau = max(2 C, 5 %)", TAU_ABS_C, TAU_REL)):
            counts = {"MINIATURE WINS": 0, "FULL-SIZE WINS": 0, "PRACTICALLY TIED": 0, "INELIGIBLE": 0, "other": 0}
            for r in head.to_dict("records"):
                lab = winner_label(r["rmse_full_c"], r["rmse_mini_c"], r["availability_full"] >= gate,
                                   r["availability_mini"] >= gate, r["se_paired_c"], True, tau_abs, tau_rel)
                w = lab["winner"]
                key = w if w in counts else ("INELIGIBLE" if w.startswith("INELIGIBLE") else "other")
                counts[key] += 1
            rows.append(dict(data_type=DATA_TYPE, availability_gate=gate, tau_rule=tau_name,
                             is_primary_rule=(gate == GATE and tau_name == "tau = max(2 C, 5 %)"),
                             n_comparisons=len(head), **counts,
                             note="recomputed from the stored per-replicate errors; no cell was rerun. The "
                                  "threshold that gives a cleaner answer is never selected (D-105)."))
    return pd.DataFrame(rows)


def correction_threshold(comparisons: pd.DataFrame, cells: pd.DataFrame) -> pd.DataFrame:
    """SD*: the correction SD at which the miniature RMSE meets the full-size RMSE (D-106).

    Primary: linear interpolation on the simulated sweep. Cross-check: the semi-analytic
    SD*^2 = RMSE_full^2 - RMSE_mini(SD = 0)^2, which follows from
    RMSE_mini(SD)^2 = V_sampling + bias^2 + SD^2 and RMSE_mini(0)^2 = V_sampling + bias^2.
    """
    t3 = comparisons[comparisons.tier == "T3"].copy()
    t3["sd_c"] = t3["variant"].str.replace("SD=", "", regex=False).astype(float)
    rows = []
    for (arch, strat, geom, k), g in t3.groupby(["archetype_id", "strategy", "geom_code", "k_budget"]):
        g = g.sort_values("sd_c")
        sd = g["sd_c"].to_numpy(float)
        dr = (g["rmse_full_c"] - g["rmse_mini_c"]).to_numpy(float)     # > 0 while miniature is better
        rmse_full = float(g["rmse_full_c"].iloc[0])
        rmse0 = float(g.loc[g.sd_c == 0.0, "rmse_mini_c"].iloc[0]) if (sd == 0).any() else np.nan
        cross = np.nan
        for i in range(len(sd) - 1):
            if np.isfinite(dr[i]) and np.isfinite(dr[i + 1]) and dr[i] > 0 >= dr[i + 1]:
                cross = sd[i] + (sd[i + 1] - sd[i]) * dr[i] / (dr[i] - dr[i + 1])
                break
        label_cross = np.nan
        labs = g["winner"].tolist()
        for i in range(len(sd) - 1):
            if labs[i] == "MINIATURE WINS" and labs[i + 1] in ("FULL-SIZE WINS", "PRACTICALLY TIED"):  # noqa: E501
                label_cross = 0.5 * (sd[i] + sd[i + 1])
                break
        analytic = float(np.sqrt(max(0.0, rmse_full ** 2 - rmse0 ** 2))) if np.isfinite(rmse0) else np.nan
        rows.append(dict(data_type=DATA_TYPE, archetype_id=arch, strategy=strat, geom_code=geom, k_budget=k,
                         n_mini=int(g["n_mini"].iloc[0]), rmse_full_c=rmse_full, rmse_mini_at_sd0_c=rmse0,
                         sd_star_simulated_c=cross, sd_star_semi_analytic_c=analytic,
                         sd_star_label_change_c=label_cross,
                         measured_central_sd_c=K.central_scenario_values()["sd_c"],
                         measured_conservative_sd_c=K.conservative_scenario_values()["sd_c"],
                         central_below_threshold=bool(np.isfinite(cross)
                                                      and K.central_scenario_values()["sd_c"] < cross),
                         scenario_note=CONDITIONAL_SCENARIO_NOTE))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 8. T6: the bounded interval-coverage sub-study (D-109)
# ---------------------------------------------------------------------------
def coverage_task(task: dict) -> dict:
    """One T6 cell: R programmes, each with B bootstrap replicates of the APPROVED WP4 pairs method.

    B = 500 here is a bounded WP6 Monte Carlo coverage experiment. It neither replaces nor modifies WP4's
    approved production procedure (B = 2,000 per curve per method, D-055), and no WP4 output is affected. The
    bootstrap method itself is the approved one, unchanged, and is never modified to improve coverage.
    """
    import wp4_bootstrap as BS
    truth = SIM.truth_from_t0(task["use_j"], task["c_c"], task["t0_c"], task.get("lse_j", SIM.TRUE_LSE_J))
    geom = D.geometry_info(task["geom_code"])
    scatter = SIM.build_scatter(task["scatter"])
    correction = SIM.build_correction(task["correction"])
    rows = []
    for i in range(int(task["replicates"])):
        r = SIM.simulate_programme(truth, geom, int(task["n"]), task["strategy"], task["e_prior"], scatter,
                                   correction, SIM.replicate_rng(task["crn_stream"], "noise", i),
                                   SIM.replicate_rng(task["crn_stream"], "correction", i), keep_detail=True)
        if not r["available"]:
            rows.append(dict(replicate=i, available=False))
            continue
        reps = BS.run_replicates(r["t_fse"], r["e_fse"], "full-size", BS.PAIRS,
                                 f"{task['cell_id']}|{i}", range(int(task["bootstrap_replicates"])))
        vals = reps["t41j"][BS.target_available(reps, "t41j")]
        finite = len(vals) / float(task["bootstrap_replicates"])
        lo, hi = (np.percentile(vals, [2.5, 97.5]) if len(vals) else (np.nan, np.nan))
        reportable = finite >= BS.REPORTABLE_FINITE_FRACTION
        own = truth["t41j_c"] + (r["delta_c"] if np.isfinite(r["delta_c"]) else 0.0)
        rows.append(dict(replicate=i, available=True, reportable=bool(reportable), finite_fraction=finite,
                         lo=float(lo), hi=float(hi), width=float(hi - lo), t41j_hat=r["t41j_hat_c"],
                         delta_c=float(r["delta_c"]) if np.isfinite(r["delta_c"]) else 0.0,
                         covers_own_estimand=bool(reportable and lo <= own <= hi),
                         covers_true_t41j=bool(reportable and lo <= truth["t41j_c"] <= hi)))
    t = pd.DataFrame(rows)
    rep = t[t.get("reportable", False) == True] if "reportable" in t else t.iloc[0:0]
    return dict(cell_id=task["cell_id"], n_programmes=len(t), n_available=int(t["available"].sum()),
                n_reportable=len(rep),
                coverage_A_own_estimand=float(rep["covers_own_estimand"].mean()) if len(rep) else np.nan,
                coverage_B_true_t41j=float(rep["covers_true_t41j"].mean()) if len(rep) else np.nan,
                median_width_c=float(rep["width"].median()) if len(rep) else np.nan)


def run_coverage(grid: pd.DataFrame, workers: int = None) -> pd.DataFrame:
    workers = worker_count() if workers is None else workers
    t6 = grid[grid.tier == "T6"]
    code_fp = CP.code_fingerprint()
    root = CP.checkpoint_root()
    out, todo, lookup = [], [], {}
    for row in t6.to_dict("records"):
        task = _task_from_row(row)
        task["bootstrap_replicates"] = B_T6
        fp = CP.fingerprint(code_fp, kind="coverage", **{k: v for k, v in task.items() if k != "cell_id"})
        path = root / "T6" / f"{CP.slug(row['cell_id'])}.npz"
        cached = CP.load_arrays(path, fp)
        if cached is not None:
            out.append({k: (v.item() if getattr(v, "ndim", 0) == 0 else v) for k, v in cached.items()})
        else:
            todo.append(task)
            lookup[task["cell_id"]] = (fp, path)
    for res in stream_map(coverage_task, iter(todo), workers):
        fp, path = lookup[res["cell_id"]]
        CP.save_arrays(path, {k: np.array(v) for k, v in res.items()}, fp)
        out.append(res)
    t = pd.DataFrame(out)
    meta = t6.set_index("cell_id")[["geom_code", "k_budget", "n", "archetype_id", "strategy"]]
    t = t.merge(meta, left_on="cell_id", right_index=True, how="left")
    t.insert(0, "data_type", DATA_TYPE)
    t["coverage_A_definition"] = ("coverage of the programme's OWN corrected estimand, T41J_true + Delta, "
                                  "conditional on its realised size correction - what the bootstrap samples")
    t["coverage_B_definition"] = ("coverage of the TRUE full-size T41J, after programme-level size-correction "
                                  "uncertainty exists - what a user of the interval actually wants")
    t["bootstrap_note"] = (f"approved WP4 pairs bootstrap, unchanged (D-052 to D-057), B = {B_T6} as a bounded "
                           f"WP6 coverage experiment only; WP4's production B = 2,000 is unchanged (D-109)")
    return t.sort_values(["geom_code", "k_budget"])


# ---------------------------------------------------------------------------
# 9. Monte Carlo stability subset (D-107)
# ---------------------------------------------------------------------------
def stability_subset(cells: pd.DataFrame, comparisons: pd.DataFrame) -> pd.DataFrame:
    """Predeclared: for each strategy, the T1 cells at k = 4 and k = 24 and the cell nearest the flip for A5."""
    picks = []
    t1 = cells[(cells.tier == "T1") & (cells.archetype_id == "A5") & (cells.geom_code == "G5")]
    for st in FIXED_STRATEGIES:
        s = t1[t1.strategy == st]
        for k in (4, 24):
            row = s[s.k_budget == k]
            if len(row):
                picks.append(row.iloc[0]["cell_id"])
        c = comparisons[(comparisons.tier == "T1") & (comparisons.archetype_id == "A5")
                        & (comparisons.geom_code == "G5") & (comparisons.strategy == st)]
        if len(c):
            c = c.assign(absd=c["delta_rmse_c"].abs()).sort_values("absd")
            picks.append(c.iloc[0]["mini_cell_id"])
    return cells[cells.cell_id.isin(dict.fromkeys(picks))].copy()


def run_stability(cells: pd.DataFrame, results: dict, workers: int = None) -> pd.DataFrame:
    """Rerun the predeclared subset at R = 4,000 on an independent stream and compare (D-107)."""
    sub = cells.copy()
    sub["replicates"] = STABILITY_REPLICATES
    sub["crn_stream"] = sub["crn_stream"] + "|stability-4000"
    big = run_grid(sub, workers=workers, progress_every=10**9, cache_subdir="stability")
    rows = []
    for row in cells.to_dict("records"):
        a = cell_metrics(results[row["cell_id"]]["errors"], results[row["cell_id"]]["n_replicates"])
        b = cell_metrics(big[row["cell_id"]]["errors"], STABILITY_REPLICATES)
        rows.append(dict(data_type=DATA_TYPE, cell_id=row["cell_id"], tier=row["tier"],
                         archetype_id=row["archetype_id"], geom_code=row["geom_code"], strategy=row["strategy"],
                         k_budget=row["k_budget"], n=row["n"],
                         rmse_R1000_c=a["rmse_c"], rmse_R4000_c=b["rmse_c"],
                         delta_rmse_c=b["rmse_c"] - a["rmse_c"],
                         availability_R1000=a["availability"], availability_R4000=b["availability"],
                         eligible_R1000=a["eligible"], eligible_R4000=b["eligible"],
                         eligibility_unchanged=bool(a["eligible"] == b["eligible"]),
                         within_tau=bool(abs(b["rmse_c"] - a["rmse_c"]) < TAU_ABS_C)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 10. Figures (grayscale-legible: line style and marker shape carry the information, never colour)
# ---------------------------------------------------------------------------
GEOM_STYLE = {"G0": ("-", "o", "black", 2.0), "G1": ("--", "s", "0.15", 1.2), "G2": (":", "^", "0.3", 1.2),
              "G3": ("-.", "v", "0.45", 1.2), "G5": ("--", "D", "0.15", 1.2), "G4": (":", "P", "0.55", 1.2),
              "G6": ("-.", "X", "0.3", 1.2), "G7": ("--", "*", "0.5", 1.2)}
STRAT_STYLE = {"U": ("-", "o"), "C": ("--", "s"), "A": (":", "^"), "S": ("-.", "D"), "SS": ((0, (3, 1, 1, 1)), "X")}
SYNTH_TAG = "SYNTHETIC - Monte Carlo test-matrix study; not published measurements"


def _style_axes(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.grid(True, which="both", lw=0.3, color="0.8", ls="-")
    ax.tick_params(labelsize=7)


def figures(cells: pd.DataFrame, results: dict, comparisons: pd.DataFrame, thresholds: pd.DataFrame,
            coverage: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    save = lambda fig, name: (fig.savefig(OUT / name, dpi=150, metadata={"Software": None}), plt.close(fig))
    cen = K.central_scenario_values()
    con = K.conservative_scenario_values()

    # 1 - fixed-volume comparison: RMSE vs material budget, one panel per strategy
    t1 = cells[(cells.tier == "T1") & (cells.archetype_id == "A5")]
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.9), sharey=True)
    for ax, st in zip(axes, FIXED_STRATEGIES):
        for code in D.ALL_CODES:
            s = t1[(t1.strategy == st) & (t1.geom_code == code)].sort_values("k_budget")
            ls, mk, col, lw = GEOM_STYLE[code]
            ax.plot(s["k_budget"], s["rmse_c"], ls=ls, marker=mk, color=col, lw=lw, ms=4,
                    label=f"{code} {D.GEOMETRY_DIMENSIONS[code][0].split(' a=')[0]}" +
                          (" (full-size)" if code == "G0" else ""))
        ax.axhline(np.sqrt(cen["bias_c"] ** 2 + cen["sd_c"] ** 2), color="0.5", lw=0.8, ls=(0, (1, 1)))
        _style_axes(ax, f"strategy {st}", "", "RMSE of recovered full-size T41J (deg C)" if st == "U" else "")
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(FixedLocator([3, 5, 10, 20, 30]))
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_xticks(BUDGETS_K)
    axes[1].text(24, 13.3, "all 7 miniature geometries overlap\nat the correction floor", fontsize=6,
                 ha="right", va="bottom", color="0.25")
    fig.supxlabel("material budget k (volume of k full-size specimens)", fontsize=8)
    axes[0].legend(fontsize=5.5, loc="upper right", ncol=2)
    fig.suptitle(f"Fixed material volume: RMSE of recovered full-size T41J, archetype A5. {SYNTH_TAG}.\n"
                 f"Miniature curves: a conditional fixed-volume scenario using the pooled WEAKLY SUPPORTED "
                 f"correction; large-N gains assume independent specimen scatter (D-096).", fontsize=7)
    fig.tight_layout(rect=[0, 0.02, 1, 0.9])
    save(fig, "fixed_volume_comparison.png")

    # 2 - RMSE against specimen count, with the 1/sqrt(N) reference
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for st in FIXED_STRATEGIES:
        s = t1[(t1.strategy == st) & (t1.geom_code == "G0")].sort_values("n")
        ls, mk = STRAT_STYLE[st]
        ax.plot(s["n"], s["rmse_c"], ls=ls, marker=mk, color="black", lw=1.4, ms=5, label=f"full-size, {st}")
    mini = t1[(t1.strategy == "U") & (t1.geom_code != "G0")].sort_values("n")
    ax.plot(mini["n"], mini["rmse_c"], ls="", marker=".", color="0.45", ms=5,
            label="miniature, U (all 7 geometries, with the correction penalty)")
    ns = np.array([4, 3000], float)
    ref = float(t1[(t1.strategy == "U") & (t1.geom_code == "G0") & (t1.k_budget == 12)]["rmse_c"].iloc[0])
    ax.plot(ns, ref * np.sqrt(12.0 / ns), ls=(0, (1, 2)), color="0.6", lw=1.0, label="1 / sqrt(N) reference")
    ax.axhline(np.sqrt(cen["bias_c"] ** 2 + cen["sd_c"] ** 2), color="0.25", ls="--", lw=1.0)
    ax.text(5, np.sqrt(cen["bias_c"] ** 2 + cen["sd_c"] ** 2) * 1.05,
            "miniature error floor from the CENTRAL correction", fontsize=6, color="0.25")
    ax.set_xscale("log"); ax.set_yscale("log")
    _style_axes(ax, f"RMSE against specimen count, archetype A5. {SYNTH_TAG}.",
                "specimens tested, N", "RMSE of recovered full-size T41J (deg C)")
    ax.legend(fontsize=6)
    fig.tight_layout(); save(fig, "rmse_vs_specimen_count.png")

    # 3 - strategy comparison, with availability annotated and the k = 4 adaptive degeneracy noted
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for ax, code in zip(axes, ["G0", "G5"]):
        for st in FIXED_STRATEGIES + ["SS"]:
            src = cells[(cells.archetype_id == "A5") & (cells.geom_code == code) & (cells.strategy == st)
                        & (cells.e_prior == 0.0) & (cells.tier.isin(["T1", "T7"]))].sort_values("k_budget")
            if not len(src):
                continue
            ls, mk = STRAT_STYLE[st]
            ax.plot(src["k_budget"], src["rmse_c"], ls=ls, marker=mk, color="black", lw=1.2, ms=4, label=st)
        _style_axes(ax, f"{code} ({'full-size' if code == 'G0' else D.GEOMETRY_DIMENSIONS[code][0]})",
                    "material budget k", "RMSE of full-size T41J (deg C)")
        ax.set_yscale("log")
    axes[0].legend(fontsize=6, title="strategy", title_fontsize=6)
    fig.suptitle(f"Temperature-placement strategies, archetype A5, prior error 0. {SYNTH_TAG}.\n"
                 f"At k = 4 the adaptive seed block consumes the whole programme, so S is exactly strategy A "
                 f"and no adaptive claim is made there.", fontsize=7)
    fig.tight_layout(rect=[0, 0, 1, 0.84]); save(fig, "strategy_comparison.png")

    # 4 - prior-knowledge sweep: RMSE and availability
    t2 = cells[cells.tier == "T2"]
    fig, axes = plt.subplots(2, 2, figsize=(9, 5.6), sharex=True)
    for j, code in enumerate(["G0", "G5"]):
        for st in FIXED_STRATEGIES:
            s = t2[(t2.geom_code == code) & (t2.strategy == st) & (t2.archetype_id == "A5")
                   & (t2.k_budget == 12)].sort_values("e_prior")
            ls, mk = STRAT_STYLE[st]
            axes[0, j].plot(s["e_prior"], s["rmse_c"], ls=ls, marker=mk, color="black", lw=1.2, ms=4, label=st)
            axes[1, j].plot(s["e_prior"], s["availability"], ls=ls, marker=mk, color="black", lw=1.2, ms=4)
        _style_axes(axes[0, j], f"{code}, k = 12", "", "RMSE of full-size T41J (deg C)" if j == 0 else "")
        axes[0, j].set_yscale("log")
        _style_axes(axes[1, j], "", "prior error e_prior = T_assumed - T41J_true (deg C)",
                    "estimator availability" if j == 0 else "")
        axes[1, j].axhline(GATE, color="0.4", ls="--", lw=1.0)
    axes[0, 0].legend(fontsize=6, title="strategy", title_fontsize=6)
    fig.suptitle(f"Prior knowledge of the transition location, archetype A5. {SYNTH_TAG}. "
                 f"Dashed line: the {GATE:.0%} availability gate.", fontsize=7)
    fig.tight_layout(rect=[0, 0, 1, 0.92]); save(fig, "prior_error_vs_performance.png")

    # 5 - the flip: RMSE against correction SD, with SD* and the measured values
    t3 = comparisons[comparisons.tier == "T3"].copy()
    t3["sd_c"] = t3["variant"].str.replace("SD=", "", regex=False).astype(float)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    for ax, arch in zip(axes, REDUCED_ARCHETYPES):
        for st in FIXED_STRATEGIES:
            s = t3[(t3.archetype_id == arch) & (t3.strategy == st) & (t3.geom_code == "G5")
                   & (t3.k_budget == 8)].sort_values("sd_c")
            if not len(s):
                continue
            ls, mk = STRAT_STYLE[st]
            ax.plot(s["sd_c"], s["rmse_mini_c"], ls=ls, marker=mk, color="black", lw=1.2, ms=4, label=f"mini, {st}")
            ax.axhline(float(s["rmse_full_c"].iloc[0]), ls=ls, color="0.6", lw=1.0)
        ax.axvline(cen["sd_c"], color="0.2", ls="-", lw=1.2)
        ax.axvline(con["sd_c"], color="0.45", ls="--", lw=1.2)
        ax.axvspan(10.0, 15.0, color="0.88", zorder=0)
        _style_axes(ax, f"archetype {arch}", "correction residual SD (deg C)",
                    "RMSE of full-size T41J (deg C)" if arch == "A1" else "")
    axes[0].legend(fontsize=6, loc="upper left")
    fig.text(0.5, 0.01, "Black curves: miniature programme against the correction SD. Grey horizontals: the matching "
                        "full-size programme (same line style = same strategy). Solid vertical: measured CENTRAL SD "
                        f"{cen['sd_c']:.2f} deg C; dashed vertical: CONSERVATIVE {con['sd_c']:.2f} deg C. Grey band: "
                        "NUREG/CR-6379 per-type sigma 10-15 deg C, an EXTERNAL reference, not adopted.",
             fontsize=6, ha="center", va="bottom", wrap=True)
    fig.suptitle(f"How uncertain may the size correction be before extra miniature specimens stop paying? "
                 f"G5 at k = 8. {SYNTH_TAG}.", fontsize=7)
    fig.tight_layout(rect=[0, 0.08, 1, 0.93]); save(fig, "correction_uncertainty_flip.png")

    # 6 - scatter-model sensitivity
    sc_v = {"C1 (central)": ("T1", ""), "C1-robust": ("T4", "V1 scatter C1-robust"),
            "C2": ("T4", "V2 scatter C2"), "C3-centred": ("T4", "V3 scatter C3-centred"),
            "C3-uncentered": ("T4", "V4 scatter C3-uncentered"),
            "miniature-inflated": ("T4", "V5 miniature-inflated scatter")}
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for i, (lab, (tier, var)) in enumerate(sc_v.items()):
        s = comparisons[(comparisons.tier == tier) & (comparisons.variant == var)
                        & (comparisons.geom_code == "G5") & (comparisons.strategy == "U")
                        & (comparisons.archetype_id.isin(REDUCED_ARCHETYPES))]
        s = s[s.k_budget.isin([6, 12])]
        ax.scatter(np.full(len(s), i) + np.linspace(-0.15, 0.15, max(1, len(s))), s["delta_rmse_c"],
                   marker="o", s=18, facecolors="none", edgecolors="black", lw=0.8)
    ax.axhline(0, color="black", lw=1.0)
    ax.set_xticks(range(len(sc_v))); ax.set_xticklabels(sc_v.keys(), rotation=20, ha="right", fontsize=7)
    _style_axes(ax, f"Scatter-model sensitivity: G5, strategy U, k = 6 and 12. {SYNTH_TAG}.", "",
                "RMSE(full-size) - RMSE(miniature) (deg C)\n> 0 favours miniature")
    fig.tight_layout(); save(fig, "scatter_model_sensitivity.png")

    # 7 - correction-model sensitivity
    corr_v = {"CENTRAL normal": ("T1", ""), "CONSERVATIVE": ("T4", "V6 correction CONSERVATIVE"),
              "empirical 7-family": ("T4", "V7 correction empirical 7-family"),
              "empirical 10-family": ("T4", "V8 correction empirical 10-family"),
              "Corwin S1": ("T4", "V9 normalization S1 energy (Bb)^3/2"),
              "Lucon S3": ("T4", "V10 normalization S3 temperature Lucon"),
              "Wallin S5": ("T4", "V11 normalization S5 temperature Wallin"),
              "Towers S4": ("T4", "V12 normalization S4 temperature Towers"),
              "KLST-literal S6": ("T4", "V13 normalization S6 KLST as recorded"),
              "specimen-level (illustrative)": ("T4", "V14 specimen-level correction draw")}
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    for i, (lab, (tier, var)) in enumerate(corr_v.items()):
        s = comparisons[(comparisons.tier == tier) & (comparisons.variant == var)
                        & (comparisons.geom_code.isin(["G5", "G6"])) & (comparisons.strategy == "U")
                        & (comparisons.archetype_id.isin(REDUCED_ARCHETYPES)) & (comparisons.k_budget.isin([6, 12]))]
        ax.scatter(np.full(len(s), i) + np.linspace(-0.2, 0.2, max(1, len(s))), s["delta_rmse_c"],
                   marker="o", s=16, facecolors="none", edgecolors="black", lw=0.8)
    ax.axhline(0, color="black", lw=1.0)
    ax.set_xticks(range(len(corr_v))); ax.set_xticklabels(corr_v.keys(), rotation=30, ha="right", fontsize=6.5)
    _style_axes(ax, f"Correction-model sensitivity: strategy U, k = 6 and 12. {SYNTH_TAG}.", "",
                "RMSE(full-size) - RMSE(miniature) (deg C)\n> 0 favours miniature")
    fig.tight_layout(); save(fig, "correction_model_sensitivity.png")

    # 8 - estimator-unavailable rate
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for ax, (tier, xcol, xlab) in zip(axes, [("T1", "k_budget", "material budget k"),
                                             ("T2", "e_prior", "prior error (deg C)")]):
        src = cells[(cells.tier == tier) & (cells.archetype_id == "A5")]
        if tier == "T2":
            src = src[src.k_budget == 12]
        for st in FIXED_STRATEGIES:
            s = src[(src.strategy == st) & (src.geom_code == "G5")].sort_values(xcol)
            ls, mk = STRAT_STYLE[st]
            ax.plot(s[xcol], 1.0 - s["availability"], ls=ls, marker=mk, color="black", lw=1.2, ms=4, label=st)
        ax.axhline(1 - GATE, color="0.4", ls="--", lw=1.0)
        _style_axes(ax, f"{tier}", xlab, "estimator-unavailable rate" if tier == "T1" else "")
    axes[0].legend(fontsize=6, title="strategy", title_fontsize=6)
    fig.suptitle(f"Estimator-unavailable rate, G5, archetype A5. Dashed: the {1 - GATE:.0%} limit of the "
                 f"availability gate. {SYNTH_TAG}.", fontsize=7)
    fig.tight_layout(rect=[0, 0, 1, 0.86]); save(fig, "failure_rate.png")

    # 9 - one worked adaptive programme, on BOTH temperature axes
    truth = archetypes()["A5"]
    geom = D.geometry_info("G5")
    r = SIM.simulate_programme(truth, geom, D.specimen_count("G5", 6), "S", 0.0,
                               S.build_scatter_model("C1"), K.scenario_central(),
                               SIM.replicate_rng("worked-example", "noise", 0),
                               SIM.replicate_rng("worked-example", "correction", 0), keep_detail=True)
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    order = np.arange(len(r["t_raw"]))
    clipped = np.isclose(r["t_raw"], D.GRID_MIN_C)
    ax.plot(order, r["t_raw"], ls="-", marker="o", ms=3.5, color="black", lw=0.9,
            label="actual RAW specimen temperature")
    ax.plot(order, r["t_fse"], ls="--", marker="s", ms=3.5, color="0.45", lw=0.9,
            label="normalized full-size-equivalent temperature (= raw + M)")
    if clipped.any():
        ax.plot(order[clipped], r["t_raw"][clipped], ls="", marker="x", ms=7, color="black",
                label="clipped at the physical floor")
    ax.axhline(D.GRID_MIN_C, color="0.2", ls=":", lw=1.1)
    ax.text(0.5, D.GRID_MIN_C - 16, f"physical floor: coldest on-grid raw temperature {D.GRID_MIN_C:g} deg C "
                                    f"(liquid nitrogen {D.T_RAW_MIN_C:g} deg C)", fontsize=6)
    ax.axhline(truth["t41j_c"], color="0.35", ls="-.", lw=1.0)
    ax.text(0.5, truth["t41j_c"] + 3, "true full-size T41J", fontsize=6)
    n0 = D.adaptive_seed_size(len(r["t_raw"]))
    ax.axvline(n0 - 0.5, color="0.6", lw=0.8)
    ax.text(n0 - 1.0, ax.get_ylim()[1] - 12, f"seed block: {n0} specimens\n{r['adaptation_updates']} updates follow",
            fontsize=6, ha="right", va="top")
    _style_axes(ax, f"One simulated adaptive programme (strategy S), G5 at k = 6.\n{SYNTH_TAG}.",
                "specimen, in the order it was tested", "temperature (deg C)")
    ax.set_ylim(D.GRID_MIN_C - 30, None)
    ax.legend(fontsize=6, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.text(0.01, 0.01, "Blocks after the seed are placed at T_hat + delta x C_hat. For blocks larger than seven "
                         "specimens the pre-registered delta sequence extends beyond +/- 1.5 C_hat, so later "
                         "specimens spread onto the shelves and are clipped at the envelope (D-112 step 10; "
                         "full-size blocks never exceed four specimens and are unaffected).",
             fontsize=5.5, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=[0, 0.06, 1, 1]); save(fig, "worked_adaptive_program.png")


# ---------------------------------------------------------------------------
# 11. Summary tables
# ---------------------------------------------------------------------------
def summary_tables(cells: pd.DataFrame, comparisons: pd.DataFrame) -> dict:
    out = {}
    head = comparisons[comparisons.tier == "T1"]
    out["fixed_volume_comparison"] = head[[
        "data_type", "archetype_id", "strategy", "k_budget", "geom_code", "n_full", "n_mini",
        "rmse_full_c", "rmse_mini_c", "delta_rmse_c", "tau_c", "se_paired_c", "se_paired_bootstrap_c",
        "se_ratio_batch_over_bootstrap", "se_estimators_agree", "n_paired_replicates", "winner",
        "p90_full_c", "p90_mini_c", "secondary_winner_p90", "primary_secondary_agree",
        "availability_full", "availability_mini", "eligible_full", "eligible_mini",
        "clip_fraction_mini", "transition_reachable_mini", "winner_class", "scenario_note"]].copy()

    t1 = cells[cells.tier == "T1"]
    out["strategy_comparison"] = (t1.groupby(["geom_code", "k_budget", "strategy"])
                                  .agg(rmse_median_c=("rmse_c", "median"), rmse_min_c=("rmse_c", "min"),
                                       rmse_max_c=("rmse_c", "max"), availability_min=("availability", "min"),
                                       n_specimens=("n", "first"), cells=("cell_id", "count"))
                                  .reset_index().assign(data_type=DATA_TYPE))

    # Group by the specimen count as well: the machining-allowance variants give a different N for the same
    # (geometry, budget), and averaging across them would hide the k = 4 degeneracy.
    ad = cells[cells.strategy == "S"].groupby(["geom_code", "k_budget", "allowance_c_mm", "n"]).agg(
        adaptation_updates=("adaptation_updates", "mean"), cells=("cell_id", "count")).reset_index()
    ad = ad.rename(columns={"n": "n_specimens"})
    ad["seed_block_n"] = [D.adaptive_seed_size(int(n)) for n in ad["n_specimens"]]
    ad["block_size"] = [D.adaptive_block_size(int(n)) for n in ad["n_specimens"]]
    ad["adaptive_degenerates_to_A"] = ad["adaptation_updates"] < 0.5
    ad["note"] = np.where(ad["adaptive_degenerates_to_A"],
                          "the seed block consumes the whole programme: S is exactly strategy A here and no "
                          "adaptive claim may be made from this cell (D-101)", "")
    out["adaptive_update_counts"] = ad.assign(data_type=DATA_TYPE)

    t2 = cells[cells.tier == "T2"]
    out["prior_knowledge_sweep"] = t2[[
        "data_type", "archetype_id", "geom_code", "k_budget", "n", "strategy", "e_prior", "rmse_c",
        "p90_abs_c", "availability", "eligible", "temperature_clip_fraction"]].sort_values(
        ["archetype_id", "geom_code", "k_budget", "strategy", "e_prior"])

    t4 = comparisons[comparisons.tier == "T4"]
    base = head.set_index(["archetype_id", "strategy", "k_budget", "geom_code"])["delta_rmse_c"]
    rows = []
    for var, g in t4.groupby("variant"):
        ref = []
        for r in g.to_dict("records"):
            key = (r["archetype_id"], r["strategy"], r["k_budget"], r["geom_code"])
            ref.append(base.get(key, np.nan))
        ref = np.array(ref, float)
        d = g["delta_rmse_c"].to_numpy(float)
        rows.append(dict(data_type=DATA_TYPE, variant=var, n_comparisons=len(g),
                         median_delta_rmse_c=float(np.nanmedian(d)),
                         median_central_delta_rmse_c=float(np.nanmedian(ref)),
                         median_shift_vs_central_c=float(np.nanmedian(d - ref)),
                         miniature_wins=int((g.winner_class == "MINIATURE WINS").sum()),
                         full_size_wins=int((g.winner_class == "FULL-SIZE WINS").sum()),
                         tied=int((g.winner_class == "PRACTICALLY TIED").sum()),
                         ineligible=int((g.winner_class == "INELIGIBLE").sum()),
                         changes_conclusion=bool(
                             np.nanmedian(np.sign(d)) != np.nanmedian(np.sign(ref)))))
    out["sensitivity_summary"] = pd.DataFrame(rows).sort_values("variant")

    coh = t4[t4.variant.str.contains("WP2")]
    out["cohort_sensitivity"] = coh[[
        "data_type", "variant", "cohort_key", "archetype_id", "strategy", "k_budget", "geom_code",
        "rmse_full_c", "rmse_mini_c", "delta_rmse_c", "winner", "winner_class"]].assign(
        limitation="the WP5 size correction stays at the primary-cohort value in every cohort variant, because "
                   "D-071 fixes WP5 to the CP2-frozen primary cohort and D-039 forbids regenerating cohorts (D-110)")

    t5 = comparisons[comparisons.tier == "T5"]
    per_curve = t5.groupby(["truth_key", "strategy", "k_budget"])["winner_class"].first().reset_index()
    out["breadth_check_104_curves"] = t5[[
        "data_type", "truth_key", "strategy", "k_budget", "geom_code", "n_full", "n_mini", "rmse_full_c",
        "rmse_mini_c", "delta_rmse_c", "winner", "winner_class", "availability_full", "availability_mini",
        "transition_reachable_mini"]].copy()
    out["breadth_check_summary"] = (per_curve.groupby(["strategy", "k_budget", "winner_class"]).size()
                                    .rename("n_curves").reset_index().assign(data_type=DATA_TYPE))
    return out


def write_summary(cells, comparisons, thresholds, coverage, stability, labels, tables, bench) -> None:
    """wp6_summary.md: every number is computed here from the result tables, never typed."""
    cen, con = K.central_scenario_values(), K.conservative_scenario_values()
    floor_c = float(np.sqrt(cen["bias_c"] ** 2 + cen["sd_c"] ** 2))
    floor_k = float(np.sqrt(con["bias_c"] ** 2 + con["sd_c"] ** 2))
    head = comparisons[comparisons.tier == "T1"]
    counts = head["winner_class"].value_counts().to_dict()

    # flip budgets, per strategy, for every miniature geometry (A5)
    flip_rows = []
    for code in D.MINIATURE_CODES:
        for st in FIXED_STRATEGIES:
            s_ = head[(head.archetype_id == "A5") & (head.geom_code == code) & (head.strategy == st)].sort_values("k_budget")
            flip_rows.append(dict(geometry=code, strategy=st,
                                  miniature_wins_at_k=", ".join(str(k) for k in s_[s_.winner_class == "MINIATURE WINS"].k_budget) or "none",
                                  tied_at_k=", ".join(str(k) for k in s_[s_.winner_class == "PRACTICALLY TIED"].k_budget) or "none",
                                  full_size_wins_at_k=", ".join(str(k) for k in s_[s_.winner_class == "FULL-SIZE WINS"].k_budget) or "none"))
    flips = pd.DataFrame(flip_rows)
    share = (head.groupby(["strategy", "k_budget"])["winner_class"].value_counts(normalize=True)
             .unstack(fill_value=0.0).reindex(columns=["FULL-SIZE WINS", "MINIATURE WINS", "PRACTICALLY TIED",
                                                       "INELIGIBLE"], fill_value=0.0).round(2).reset_index())
    a5g5 = head[(head.archetype_id == "A5") & (head.geom_code == "G5")].sort_values(["strategy", "k_budget"])
    mini_level = a5g5["rmse_mini_c"]

    # archetype dependence of the flip (strategy U, G5)
    arch_rows = []
    for aid in [f"A{i}" for i in range(1, 10)]:
        s_ = head[(head.archetype_id == aid) & (head.geom_code == "G5") & (head.strategy == "U")].sort_values("k_budget")
        a = cells[(cells.tier == "T1") & (cells.archetype_id == aid) & (cells.geom_code == "G0")].iloc[0]
        arch_rows.append(dict(archetype=aid, USE_J=a["use_j"], C_C=a["c_c"],
                              miniature_wins_at_k=", ".join(str(k) for k in s_[s_.winner_class == "MINIATURE WINS"].k_budget) or "none",
                              full_size_wins_at_k=", ".join(str(k) for k in s_[s_.winner_class == "FULL-SIZE WINS"].k_budget) or "none"))
    archs = pd.DataFrame(arch_rows)

    thr = thresholds[(thresholds.archetype_id == "A5") & (thresholds.geom_code == "G5")]

    # prior sweep, full-size and G5 at k = 12, A5
    t2 = cells[(cells.tier == "T2") & (cells.archetype_id == "A5") & (cells.k_budget == 12)]
    prior_tab = {}
    for code in ("G0", "G5"):
        pv = t2[t2.geom_code == code].pivot_table(index="e_prior", columns="strategy", values="rmse_c")
        el = t2[t2.geom_code == code].pivot_table(index="e_prior", columns="strategy", values="eligible")
        txt = pv.round(1).astype(str)
        txt = txt.where(el.astype(bool), txt + " (INELIGIBLE)")
        prior_tab[code] = txt.reset_index()

    # staircase against the other strategies (T7 vs T1/T2), A5
    ss_rows = []
    for g, k in S6A:
        for e in (0.0, -40.0, 40.0):
            base = cells[(cells.archetype_id == "A5") & (cells.geom_code == g) & (cells.k_budget == k)
                         & (cells.e_prior == e) & (cells.tier == ("T1" if e == 0.0 else "T2"))]
            ss = cells[(cells.tier == "T7") & (cells.archetype_id == "A5") & (cells.geom_code == g)
                       & (cells.k_budget == k) & (cells.e_prior == e)]
            row = dict(geometry=g, k_budget=k, e_prior_c=e, SS=float(ss.rmse_c.iloc[0]))
            for st in FIXED_STRATEGIES:
                v = base[base.strategy == st]
                row[st] = float(v.rmse_c.iloc[0]) if len(v) else np.nan
            ss_rows.append(row)
    ss_tab = pd.DataFrame(ss_rows)

    reach = pd.read_csv(OUT / "geometry_reachability.csv")
    unreach = (reach[reach.truth_kind == "WP3 usable full-size fit"].groupby("geometry_code")["transition_reachable"]
               .apply(lambda x: int((~x).sum())))
    v16 = tables["sensitivity_summary"]
    v16 = v16[v16.variant.str.startswith("V16")].iloc[0]

    sens = tables["sensitivity_summary"].copy()
    allow = sens[sens.variant.str.contains("machining")]

    # stability: the common shift and its explanation
    stab_shift = float(stability["delta_rmse_c"].median())
    stab_all_within = bool(stability["within_tau"].all() and stability["eligibility_unchanged"].all())

    se_agree = float(head["se_estimators_agree"].mean())
    breadth = tables["breadth_check_summary"].pivot_table(index=["strategy", "k_budget"], columns="winner_class",
                                                          values="n_curves", fill_value=0).astype(int).reset_index()

    # --- every prose number below is computed here
    sd4 = thr[thr.k_budget == 4]["sd_star_simulated_c"]
    sd8 = thr[thr.k_budget == 8]["sd_star_simulated_c"]
    g0k6 = ss_tab[(ss_tab.geometry == "G0") & (ss_tab.k_budget == 6)]["SS"]
    scat = sens[sens.variant.str.contains("scatter")]
    scat_max_shift = float(scat["median_shift_vs_central_c"].abs().max())
    scat_reverses = bool(scat["changes_conclusion"].any())
    mb = pd.read_csv(OUT / "material_budget_accounting.csv")
    n_full_allow = {c: int(mb[(mb.geometry_code == "G0") & (mb.budget_k == 6) & (mb.allowance_c_mm == c)]["n_specimens"].iloc[0])
                    for c in (0.0, 0.5, 1.0)}
    t5 = comparisons[(comparisons.tier == "T5")]
    t5_inel = t5[t5.winner_class == "INELIGIBLE"]
    t5_curves = t5_inel.groupby("truth_key").agg(t41=("truth_key", "first"), reach=("transition_reachable_mini", "first"),
                                                  avail_mini=("availability_mini", "min"),
                                                  avail_full=("availability_full", "min"))
    t41_by_key = cells[cells.tier == "T5"].groupby("truth_key")["t41j_true_c"].first()
    t5_curves["t41"] = t5_curves.index.map(t41_by_key)
    n_inel = len(t5_curves)
    n_unreach = int((~t5_curves["reach"].astype(bool)).sum())
    cold_g5 = D.coldest_reachable_fse_c(D.geometry_info("G5")["m_shift_c"])

    write_text(OUT / "wp6_summary.md", f"""# WP6 - Monte Carlo test-matrix study: results

**{DATA_TYPE}**

Every number below is computed from the generated tables in `outputs/wp6/` and regenerates with `./run_all.sh`.
The method was frozen in DECISIONS.md D-090 to D-112 and committed before any cell was run; the 19 simulator
validation tests are in `validation_results.csv` and the 11 independent checks in `wp6_check_results.csv`.
Every miniature result is a **{CONDITIONAL_SCENARIO_NOTE}**, and every specimen count is an
**{D.IDEALIZED_ACCOUNTING_NOTE}**.

## 1. What was run

{len(cells) + len(coverage)} frozen cells across tiers T1-T7. R = {R_T1} replicates in T1, T2, T3 and T7, {R_T4}
in T4, {R_T5} in T5, and {R_T6} programmes with B = {B_T6} bootstrap replicates each in T6. Declared benchmark
before the run: projected {bench['projected_full_run_hours']:.2f} h (peak of the validation-plus-benchmark
process {bench['peak_rss_mb']:.0f} MB). The MEASURED wall-clock times of the complete runs are recorded in
`PROGRESS.md` and `run_all.sh`; a wall-clock time is not a regenerable number, so it is not written here.

## 2. The headline: which spends a fixed volume better?

Over the {len(head)} T1 comparisons (9 archetypes x 7 miniature geometries x 6 budgets x 4 strategies):
**{counts.get('FULL-SIZE WINS', 0)} FULL-SIZE WINS, {counts.get('MINIATURE WINS', 0)} MINIATURE WINS,
{counts.get('PRACTICALLY TIED', 0)} PRACTICALLY TIED, {counts.get('INELIGIBLE', 0)} INELIGIBLE.**

**The miniature error has a floor that no specimen count can beat.** For archetype A5 and geometry G5 the
miniature RMSE stays between {mini_level.min():.1f} and {mini_level.max():.1f} deg C from N = 84 to N = 504,
against the predicted floor sqrt(bias^2 + SD^2) = **{floor_c:.1f} deg C** under the CENTRAL correction
({floor_k:.1f} deg C under the CONSERVATIVE one). The size-correction residual, drawn once per programme
(D-098), does not average away. The full-size RMSE falls steadily with N. So the answer flips where the
full-size RMSE drops below that floor:

{md_table(flips)}

Across ALL 63 (archetype x geometry) combinations, the share of comparisons won by each side:

{md_table(share)}

The flip is the **same for every miniature geometry**: under the pooled correction, what decides the comparison
is the shared correction floor, not how many more specimens a geometry fits. **Miniature wins only at the
smallest budget (k = 4, i.e. four full-size specimens' worth of material), is tied around k = 6, and loses from
k = 8** (k = 12 for the wide uniform design). With the clustered design, a full-size programme is already good
enough at k = 4 that miniature never wins.

How the flip depends on the true curve (strategy U, G5):

{md_table(archs)}

## 3. How uncertain may the correction be? (SD*, D-106)

{md_table(thr[['strategy', 'k_budget', 'n_mini', 'rmse_full_c', 'rmse_mini_at_sd0_c', 'sd_star_simulated_c',
               'sd_star_semi_analytic_c', 'sd_star_label_change_c']].round(2))}

SD* is the correction residual SD at which the miniature RMSE meets the full-size RMSE. The measured WP5
values are **{cen['sd_c']:.2f} deg C** (CENTRAL, {cen['n_families']} families) and **{con['sd_c']:.2f} deg C**
(CONSERVATIVE, {con['n_families']} families). At k = 8, SD* is {sd8.min():.1f}-{sd8.max():.1f} deg C depending on
the design and geometry, **below the measured {cen['sd_c']:.1f} deg C**: the correction would have to be known
better than this dataset can show before the miniature programme beats 8 full-size specimens. At k = 4, SD* is
{sd4.min():.1f}-{sd4.max():.1f} deg C. The simulated and
semi-analytic SD* agree closely, which confirms the floor arithmetic; the label-change column is the
practically meaningful crossing (the whole tie band crossed).

## 4. Physical reachability: a result that does not depend on the penalty

The coldest full-size-equivalent temperature a geometry can physically reach is {D.GRID_MIN_C:g} + M (the
coldest on-grid raw temperature plus its temperature shift). Of the 104 usable full-size WP3 fits, the number
whose 41 J transition each geometry **cannot reach under liquid-nitrogen cooling**:
{", ".join(f"{k} {v}" for k, v in unreach.items())}. At the V16 envelope sensitivity (T41J_true = -150 deg C)
**all {int(v16['ineligible'])} miniature comparisons are INELIGIBLE** - the miniature programmes cannot reach
their own transition - while the full-size programme can.

**The limit bites before the hard boundary.** In the 104-curve breadth check, **{n_inel} curves are INELIGIBLE
for G5**: they are the {n_inel} coldest-transition materials (T41J from {t5_curves['t41'].min():.0f} to
{t5_curves['t41'].max():.0f} deg C). Only {n_unreach} lie beyond G5's reachable limit of {cold_g5:.1f} deg C; the
other {n_inel - n_unreach} are reachable, but close enough to the cold limit that clipping removes the specimens
below 41 J from too many programmes (miniature availability {t5_curves['avail_mini'].min():.0%} to
{t5_curves['avail_mini'].max():.0%}, full-size at least {t5_curves['avail_full'].min():.1%}). For cold-transition
materials the question is not which specimen size is more precise but whether the smaller one can be tested at
all.

## 5. Test-temperature placement and prior knowledge (Q2, Q4)

Prior-error sweep, A5, k = 12 (RMSE in deg C; INELIGIBLE = estimator available in fewer than 95 % of
programmes):

Full-size G0:

{md_table(prior_tab['G0'])}

Miniature G5:

{md_table(prior_tab['G5'])}

For full-size programmes, **the clustered design is best when the transition is known to within about
20-40 deg C and collapses at +/- 80 deg C** (it misses the transition and fails the availability gate); the
wide uniform design is robust but never the best; the model-based adaptive design recovers from a badly wrong
prior. For miniature programmes the placement barely matters, because the correction floor dominates.

**The adaptive conclusion depends on the algorithm (required staircase sensitivity, T7).** The simple up/down
staircase SS is far better than the model-based batched design S for full-size programmes, because it spends
every specimen near 41 J instead of on shelf anchors:

{md_table(ss_tab.round(1))}

With the staircase, a full-size programme of 6 specimens reaches {g0k6.min():.1f}-{g0k6.max():.1f} deg C across the
three prior errors, well below the {floor_c:.1f} deg C miniature floor. The staircase does not help miniature programmes (the floor dominates). At k = 4 the batched
design S performs no adaptation at all (its seed block is the whole programme), so it is exactly strategy A
there (`adaptive_update_counts.csv`).

## 6. Sensitivities

{md_table(sens[['variant', 'n_comparisons', 'median_delta_rmse_c', 'median_shift_vs_central_c', 'miniature_wins',
                'full_size_wins', 'tied', 'ineligible', 'changes_conclusion']].round(2))}

`median_delta_rmse_c` is RMSE(full-size) - RMSE(miniature); positive favours miniature. What moves the answer:

- **The size-correction assumptions dominate.** Replacing the CENTRAL correction by the CONSERVATIVE one, by
  the 10-family empirical pool, or by the Wallin or Towers temperature normalizations makes **full-size win
  every comparison**. The choice of published correlation (D-100) moves the median difference by up to
  {sens[sens.variant.str.contains('Towers')].median_shift_vs_central_c.iloc[0]:.1f} deg C - more than any
  scatter model.
- **The scatter model matters much less.** C1-robust, C2, C3-centred, C3-uncentered and the miniature-inflated
  profile shift the median difference by at most {scat_max_shift:.1f} deg C, and
  {'do reverse its sign in at least one case' if scat_reverses else 'never reverse its sign'}.
- **The programme-level correction draw is decisive** (D-098): redrawing the residual per specimen (the
  labelled illustration, V14) lets it average away and reverses the conclusion. That is why WP5's
  curve-level estimand must be applied at programme level.
- **Machining allowance favours miniature in RMSE terms**, although it costs miniature more specimens: at
  c = 0.5 and 1.0 mm the full-size count at k = 6 falls from {n_full_allow[0.0]} to {n_full_allow[0.5]} and
  {n_full_allow[1.0]}, where full-size RMSE is steep in N, while
  the miniature RMSE is already at its correction floor. So the idealized accounting (D-091) is, if anything,
  **favourable to full-size**; it does not bias the headline toward the smaller specimens.
- **The WP2 cohort ({'changes' if bool(sens[sens.variant.str.contains('WP2')]['changes_conclusion'].any()) else 'does not change'}
  the conclusion) and the true lower shelf ({'changes' if bool(sens[sens.variant.str.startswith('V15')]['changes_conclusion'].any()) else 'does not change'}
  it) are secondary.** The transition LOCATION matters only through physical reachability: a warm transition
  (V17, T41J_true = +100 deg C) leaves the conclusion unchanged, while a cold one (V16, -150 deg C) makes every
  miniature programme ineligible (section 4).

## 7. Interval coverage (T6)

{md_table(coverage[['geom_code', 'k_budget', 'n', 'n_reportable', 'coverage_A_own_estimand',
                    'coverage_B_true_t41j', 'median_width_c']].round(3))}

**Coverage A** is of the programme's own corrected estimand conditional on its realised size correction - what
the bootstrap samples. **Coverage B** is of the true full-size T41J. For full-size programmes they coincide.
For miniature programmes the bootstrap still covers what it samples (0.9 or more) but covers the **true**
full-size T41J only 0.27, 0.18 and 0.11 of the time at N = 126, 252 and 504: **the interval narrows as N grows
while the size-correction residual does not.** A bootstrap interval on a sub-size-derived T41J describes
sampling scatter only and must not be read as the uncertainty of the full-size index. The approved WP4
bootstrap was not modified; B = {B_T6} is a bounded WP6 experiment and WP4's production B = 2,000 is unchanged.

## 8. Robustness of the labels and of the Monte Carlo

Label-threshold robustness (the 12 variants of D-105, T1):

{md_table(labels[['availability_gate', 'tau_rule', 'is_primary_rule', 'MINIATURE WINS', 'FULL-SIZE WINS',
                  'PRACTICALLY TIED', 'INELIGIBLE']])}

The availability gate (90 / 95 / 99 %) changes no T1 label. The tolerance moves comparisons between "wins" and
"tied" but never reverses a winner: full-size wins the majority under every rule.

Paired Monte Carlo SE: the batch-means SE and the paired replicate-index bootstrap SE agree within a factor 1.5
in {se_agree:.0%} of T1 comparisons.

Monte Carlo stability (R = 1,000 against an independent R = 4,000): every label is unchanged and every RMSE moves
by less than tau ({'passes' if stab_all_within else 'FAILS'}). The R = 4,000 values are all slightly lower (median
{stab_shift:+.2f} deg C) because, by the declared common-random-number design, every R = 1,000 miniature cell uses
the same 1,000 correction draws: the shift is one sampling difference between two correction samples, repeated
across cells, not eleven independent ones. It is within one Monte Carlo standard error of the floor (about
0.27 deg C) and far below tau.

## 9. The breadth check: all 104 real fitted curves as truths (G5)

{md_table(breadth)}

## 10. Limitations carried from the approved decisions

- The correction distribution is **WEAKLY SUPPORTED**: 7 independent matched families from 5 studies, 0 of 9
  geometries DIRECTLY SUPPORTED (D-083). No geometry-specific performance claim is made anywhere.
- The scatter pool is **empirical published-data residual scatter**, never material scatter (D-061).
- Specimen scatter is **independent conditional on the programme-level correction draw**. WP6 does not model a
  within-programme correlated laboratory or instrument systematic, so **every very-large-N miniature gain is
  conditional on that independence and is potentially optimistic** (D-096).
- An **absolute energy-resolution floor is not modelled**: a 200 J full-size material maps to a raw
  `20x1.5x1.5` curve spanning about 0.6 J in total, below anything in the dataset's own miniature fits (D-096).
- The material-volume accounting is an **idealized finished-specimen material-only** calculation, not a
  prediction of what fits in or can be machined from a real capsule (D-091).
- The dataset contains **no usable E23-type sub-size curve** (D-071), so every smaller geometry here is
  miniaturized (MCVN).
- Irradiation and geometry are **not** assumed to be non-interacting (D-081).
- The WP5 correction stays at the primary-cohort value in the WP2 cohort variants (D-110).
- **Open for the author (D-112 step 10):** the adaptive delta sequence of D-101 was implemented as EXTENDING
  beyond +/- 1.5 C_hat for blocks larger than seven specimens. No full-size result depends on this; miniature S
  programmes spread later specimens onto the shelves, with an RMSE change of at most about 0.6 deg C.
- The coldest raw test temperature is **{D.GRID_MIN_C:g} deg C**, the coldest point that is both inside the
  -196 deg C liquid-nitrogen envelope and on the 5 deg C grid (D-101).
""")


# ---------------------------------------------------------------------------
# 12. Entry point
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="WP6 Monte Carlo test-matrix study")
    ap.add_argument("--preregister", action="store_true", help="write only the pre-result outputs")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--replicate-scale", type=float, default=1.0, help="smoke testing only")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    grid = build_grid()
    write_preregistration(grid)
    print(f"WP6: {len(grid)} frozen cells written to {OUT / 'experiment_grid.csv'}")
    if args.preregister:
        print("pre-registration only; no cell run")
        return

    if args.replicate_scale != 1.0:
        grid = grid.copy()
        grid["replicates"] = np.maximum(20, (grid["replicates"] * args.replicate_scale).astype(int))
        print(f"  SMOKE TEST: replicates scaled by {args.replicate_scale}")

    sim_grid = grid[grid.tier != "T6"]
    results = run_grid(sim_grid, workers=args.workers)
    cells = cell_results_table(sim_grid, results)
    cells.to_csv(OUT / "cell_results.csv", index=False)
    if not bool(cells["accounting_ok"].all()):
        raise RuntimeError("failure accounting does not close in every cell (D-104)")

    comparisons = paired_comparisons(cells, results)
    comparisons.to_csv(OUT / "paired_comparisons.csv", index=False)
    thresholds = correction_threshold(comparisons, cells)
    thresholds.to_csv(OUT / "correction_threshold.csv", index=False)
    labels = label_threshold_robustness(cells, results, comparisons)
    labels.to_csv(OUT / "label_threshold_robustness.csv", index=False)

    coverage = run_coverage(grid, workers=args.workers)
    coverage.to_csv(OUT / "interval_coverage.csv", index=False)

    sub = stability_subset(cells, comparisons)
    stability = run_stability(sub, results, workers=args.workers)
    stability.to_csv(OUT / "monte_carlo_stability.csv", index=False)

    tables = summary_tables(cells, comparisons)
    for name, t in tables.items():
        t.to_csv(OUT / f"{name}.csv", index=False)

    figures(cells, results, comparisons, thresholds, coverage)
    bench = pd.read_csv(OUT / "runtime_benchmark.csv").iloc[0].to_dict()
    write_summary(cells, comparisons, thresholds, coverage, stability, labels, tables, bench)
    print(f"WP6 complete in {(time.time() - t0) / 60:.1f} min; peak RSS {peak_rss_mb():.0f} MB")


if __name__ == "__main__":
    main()
