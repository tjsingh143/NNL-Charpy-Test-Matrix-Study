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


def run_grid(grid: pd.DataFrame, workers: int = None, progress_every: int = 200) -> dict:
    """Run every cell, reusing fingerprinted checkpoints; returns {cell_id: result}. Memory-bounded: each worker
    returns one compact summary, and only per-cell float32 arrays are kept."""
    workers = worker_count() if workers is None else workers
    code_fp = CP.code_fingerprint()
    root = CP.checkpoint_root()
    results, todo = {}, []
    for row in grid.to_dict("records"):
        task = _task_from_row(row)
        fp = _cell_fingerprint(code_fp, task)
        path = root / row["tier"] / f"{CP.slug(row['cell_id'])}.npz"
        cached = CP.load_arrays(path, fp)
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
