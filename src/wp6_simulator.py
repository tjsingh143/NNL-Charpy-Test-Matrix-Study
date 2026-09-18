"""WP6 - The simulator: one synthetic test programme from a known truth to a recovered T41J, and the worker
entry point that runs one cell of the frozen grid.

SYNTHETIC ONLY. Nothing here reads a published measurement; the published inputs are calibrated parameters
(WP3 curve parameters, the WP4 scatter profile, the WP5 correction), supplied by wp6_scatter and wp6_correction.

Twelve steps (DECISIONS.md D-090, D-101, D-103):
   1 truth (full-size tanh, LSE 2.7 J)                    7 no censoring, no re-test
   2 geometry                                             8 approved WP5 forward normalization (miniature)
   3 budget -> specimen count                             9 approved WP3 fit, LSE fixed at 2.7 J
   4 prior, in the FULL-SIZE-EQUIVALENT frame            10 approved index temperature, tested-range rule
   5 design -> raw temperature (snap, clip in raw)       11 record the error and the diagnostics
   6 specimens from the true curve + scatter             12 aggregate; nothing specimen-level is retained

The estimator is the approved one, including its refusals: a replicate whose 41 J crossing lies outside its own
tested range has NO T41J and is counted as unavailable (D-044, D-103).
"""
from __future__ import annotations

import hashlib

import numpy as np

import wp6_correction as K
import wp6_design as D
import wp6_scatter as S
import wp5_normalization as NZ
from wp3_fitter import (OUTCOMES, classify, criterion_bracketing, criterion_temperature, fit_curve,
                        index_fraction_of_rise, index_temperature, tanh_energy)

SEED = 20260918                       # WP6 master seed (WP3 used 20260913, WP4 20260914)
TRUE_LSE_J = 2.7                      # the approved full-size lower-shelf convention (D-042)
CRITERION_J = 41.0
DATA_TYPE = "SYNTHETIC (Monte Carlo test-matrix study; not published measurements)"
OUTCOME_CODES = {o: i for i, o in enumerate(OUTCOMES)}
EVALUATION_ERROR = -1                 # a replicate whose evaluation raised: counted, never skipped (D-104)


# ---------------------------------------------------------------------------
# 1. Seeds (D-107): one independent stream per replicate per component
# ---------------------------------------------------------------------------
def int_hash(text: str) -> int:
    return int(hashlib.sha256(str(text).encode()).hexdigest()[:15], 16)


def replicate_rng(stream: str, component: str, replicate: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([SEED, int_hash(stream), int_hash(component), int(replicate)]))


# ---------------------------------------------------------------------------
# 2. The truth
# ---------------------------------------------------------------------------
def truth_from_t41j(use_j: float, c_c: float, t41j_c: float, lse_j: float = TRUE_LSE_J) -> dict:
    """A true full-size tanh whose 41 J crossing is exactly at t41j_c."""
    frac = 2.0 * (CRITERION_J - lse_j) / (use_j - lse_j) - 1.0
    t0 = float(t41j_c) - float(c_c) * np.arctanh(frac)
    return truth_from_t0(use_j, c_c, t0, lse_j)


def truth_from_t0(use_j: float, c_c: float, t0_c: float, lse_j: float = TRUE_LSE_J) -> dict:
    value, status = criterion_temperature(float(lse_j), float(use_j), float(t0_c), float(c_c), CRITERION_J)
    if status != "defined":
        raise ValueError(f"true curve has no 41 J crossing: USE {use_j}, LSE {lse_j} ({status})")
    return dict(use_j=float(use_j), c_c=float(c_c), lse_j=float(lse_j), t0_c=float(t0_c), t41j_c=float(value))


def true_energy_fse(t_fse, truth: dict) -> np.ndarray:
    return tanh_energy(np.asarray(t_fse, float), truth["lse_j"], truth["use_j"], truth["t0_c"], truth["c_c"])


# ---------------------------------------------------------------------------
# 3. One simulated programme
# ---------------------------------------------------------------------------
def energy_scale_factor(truth: dict, delta) -> np.ndarray:
    """The energy factor that moves the true curve's 41 J crossing by exactly `delta` (D-097, optional V20).

    f = 41 J / E_true(T41J_true + delta): scaling the true energies by f puts the crossing at T41J_true + delta,
    so the injected discrepancy has the same calibrated magnitude as the temperature form and nothing is added.
    """
    e_at = true_energy_fse(np.asarray(truth["t41j_c"], float) + np.asarray(delta, float), truth)
    return np.where(e_at > 0.0, CRITERION_J / np.where(e_at > 0.0, e_at, 1.0), np.inf)


def _generate(t_raw, truth: dict, m_shift: float, nf_energy: float, delta, scatter: S.ScatterModel, rng,
              injection: str = "temperature"):
    """Specimen energies in RAW units for specimens tested at t_raw (step 6, D-096).

    The true full-size-equivalent position of a specimen is T_equiv_true = T_raw + M - Delta, and the scatter is
    evaluated there, in the full-size-equivalent frame, then divided by NF_E before being added to the raw
    energy. Draws below 0 J are set to 0 J in raw units and counted.
    """
    t_raw = np.asarray(t_raw, float)
    if injection == "energy_scale":
        # The discrepancy is carried by the energy scale, so the specimen sits at its nominal position.
        t_equiv_true = t_raw + m_shift
        scale = energy_scale_factor(truth, delta)
    else:
        t_equiv_true = t_raw + m_shift - np.asarray(delta, float)
        scale = 1.0
    x_true = (t_equiv_true - truth["t0_c"]) / truth["c_c"]
    e_true_fse = true_energy_fse(t_equiv_true, truth) * scale
    dev_fse = scatter.draw_fse(x_true, truth["use_j"], truth["lse_j"], truth["c_c"], rng)
    e_raw = (e_true_fse + dev_fse) / float(nf_energy)
    n_clipped_zero = int(np.sum(e_raw < 0.0))
    return np.where(e_raw < 0.0, 0.0, e_raw), n_clipped_zero


def _analyse(t_raw, e_raw, geom: dict):
    """Steps 8-10: the approved WP5 normalization and the approved WP3 estimator, both unchanged.

    ONE code path for both specimen sizes: T_fse = T_raw + M, E_fse = E_raw * NF_E, with NF_E and M taken from
    the geometry. They are the approved WP5 quantities - geometry_info() computes them with
    wp5_normalization.nf_energy_ligament_volume and shift_sokolov - except that the full-size geometry carries
    the approved convention NF_E = 1, M = 0 exactly, so full-size analysis is an exact identity (D-074: the
    published fit "was forced to give a correction factor of 0 for the full-size specimen"; evaluating the
    rounded Eq. 22 there returns +0.43 deg C, which WP5 self-check 2 records as the rounding residue).
    Validation test 2 asserts that this path equals wp5_normalization.normalize() exactly for every miniature
    geometry, and that the full-size case is the exact identity.
    """
    t_fse = np.asarray(t_raw, float) + float(geom["m_shift_c"])
    e_fse = np.asarray(e_raw, float) * float(geom["nf_energy"])
    fit = fit_curve(t_fse, e_fse, TRUE_LSE_J)
    t41, status = index_temperature(fit, t_fse, CRITERION_J)
    fraction = index_fraction_of_rise(fit, CRITERION_J)
    cls = classify(fit, status, fraction)
    brack = criterion_bracketing(e_fse, CRITERION_J, status)
    return t_fse, e_fse, fit, t41, status, cls, brack


def simulate_programme(truth: dict, geom: dict, n: int, strategy: str, e_prior: float,
                       scatter: S.ScatterModel, correction: K.CorrectionScenario,
                       rng_noise, rng_corr, c_assumed: float = D.C_ASSUMED_C,
                       snap: bool = True, keep_detail: bool = False) -> dict:
    """One replicate: design, test, correct, fit, estimate. Returns the error and the diagnostics.

    `snap` False is a declared TEST-ONLY configuration (validation test 17) that disables the raw grid so that
    two geometries can be given exactly equal full-size-equivalent temperatures.
    """
    m_shift, nf = float(geom["m_shift_c"]), float(geom["nf_energy"])
    t_assumed_fse = float(truth["t41j_c"]) + float(e_prior)      # the prior, in the equivalent frame (D-101)
    n = int(n)

    def place(t_fse_desired):
        t_fse_desired = np.atleast_1d(np.asarray(t_fse_desired, float))
        if snap:
            return D.place_raw(t_fse_desired, m_shift)
        raw = t_fse_desired - m_shift
        return raw, raw, np.zeros(len(raw), bool)

    def delta_for(k: int):
        return correction.draw(rng_corr, size=k) if correction.per_specimen else delta_programme

    delta_programme = 0.0 if correction.per_specimen else float(correction.draw(rng_corr))

    n_clipped = 0
    n_zero = 0
    updates = 0
    if strategy in ("U", "C", "A"):
        desired = D.place_temperatures(strategy, t_assumed_fse, c_assumed, n)
        t_raw, t_raw_desired, clipped = place(desired)
        n_clipped = int(np.sum(clipped))
        e_raw, n_zero = _generate(t_raw, truth, m_shift, nf, delta_for(n), scatter, rng_noise,
                                  correction.injection)
    elif strategy == "S":
        n0 = D.adaptive_seed_size(n)
        k_blk = D.adaptive_block_size(n)
        desired = D.place_temperatures("A", t_assumed_fse, c_assumed, n0)
        t_raw, _, clipped = place(desired)
        n_clipped = int(np.sum(clipped))
        e_raw, n_zero = _generate(t_raw, truth, m_shift, nf, delta_for(n0), scatter, rng_noise,
                                  correction.injection)
        while len(t_raw) < n:
            t_fse_hist = D.to_fse(t_raw, m_shift) if snap else t_raw + m_shift
            e_fse_hist = e_raw * nf
            try:
                fit_so_far = fit_curve(t_fse_hist, e_fse_hist, TRUE_LSE_J)
            except Exception:
                fit_so_far = None
            k = min(k_blk, n - len(t_raw))
            targets = D.adaptive_block_targets(fit_so_far, t_fse_hist, e_fse_hist, t_assumed_fse, c_assumed, k)
            updates += 1
            new_raw, _, new_clipped = place(targets)
            new_e, new_zero = _generate(new_raw, truth, m_shift, nf, delta_for(k), scatter, rng_noise,
                                        correction.injection)
            t_raw = np.concatenate([t_raw, new_raw])
            e_raw = np.concatenate([e_raw, new_e])
            n_clipped += int(np.sum(new_clipped))
            n_zero += new_zero
    elif strategy == "SS":
        cur = D.staircase_start_raw(t_assumed_fse, c_assumed, m_shift)
        raws, es = [], []
        for i in range(n):
            e_i, z_i = _generate(np.array([cur]), truth, m_shift, nf, delta_for(1), scatter, rng_noise,
                                 correction.injection)
            raws.append(cur)
            es.append(float(e_i[0]))
            n_zero += z_i
            if i + 1 < n:
                cur, clipped_i = D.staircase_next_raw(cur, float(e_i[0]) * nf, c_assumed)
                n_clipped += int(clipped_i)
        t_raw, e_raw = np.array(raws, float), np.array(es, float)
    else:
        raise ValueError(f"unknown strategy {strategy!r}")

    t_fse, e_fse, fit, t41, status, cls, brack = _analyse(t_raw, e_raw, geom)
    error = float(t41 - truth["t41j_c"]) if status == "calculated" else np.nan
    out = dict(error_c=error, available=status == "calculated", t41j_hat_c=float(t41) if np.isfinite(t41) else np.nan,
               delta_c=float(delta_programme) if not correction.per_specimen else np.nan,
               outcome_code=OUTCOME_CODES[cls["outcome"]], index_status=status,
               n_clipped=n_clipped, n_specimens=len(t_raw), n_distinct_raw=int(len(np.unique(t_raw))),
               n_zero_energy=n_zero, adaptation_updates=updates,
               index_near_shelf=bool(cls.get("flag_index_near_fitted_shelf", False)),
               bracketed=bool(brack["criterion_bracketed_by_measured_energy"]))
    if keep_detail:
        out.update(t_raw=t_raw, e_raw=e_raw, t_fse=t_fse, e_fse=e_fse, fit=fit)
    return out


# ---------------------------------------------------------------------------
# 4. Model construction inside a worker, memoized per process
# ---------------------------------------------------------------------------
_SCATTER_CACHE: dict = {}
_CORRECTION_CACHE: dict = {}
_ARCHETYPES_FOR_C2 = [(u, c, TRUE_LSE_J) for u in (100.0, 200.0, 270.0) for c in (28.0, 46.0, 60.0)]


def build_scatter(name: str, cohort_key: str = "primary", is_full_size: bool = False):
    """The scatter model for one cell.

    Two rules the approved plan fixes:
      - the WP4 MINIATURE profile is a property of miniature specimens, so the 'miniature-inflated' sensitivity
        applies to the miniature arms only; the full-size arms of that variant keep C1 as the reference (D-096);
      - a WP2 cohort variant re-derives BOTH the archetypes and the scatter profile (D-110).
    """
    if name == "miniature-inflated" and is_full_size:
        name = "C1"
    key = (name, cohort_key)
    if key not in _SCATTER_CACHE:
        _SCATTER_CACHE[key] = S.build_scatter_model(name, archetypes=_ARCHETYPES_FOR_C2, cohort=cohort_key)
    return _SCATTER_CACHE[key]


def build_correction(spec: dict) -> K.CorrectionScenario:
    key = tuple(sorted((k, str(v)) for k, v in spec.items()))
    if key in _CORRECTION_CACHE:
        return _CORRECTION_CACHE[key]
    kind = spec["kind"]
    if kind == "none":
        sc = K.scenario_none()
    elif kind == "central":
        sc = K.scenario_central()
    elif kind == "conservative":
        sc = K.scenario_conservative()
    elif kind == "empirical":
        sc = K.scenario_empirical(spec["subset"])
    elif kind == "fixed_sd":
        sc = K.scenario_fixed_sd(float(spec["sd_c"]), float(spec["bias_c"]))
    elif kind == "normalization":
        sc = K.scenario_normalization(spec["case"])
    elif kind == "specimen_level":
        sc = K.scenario_specimen_level()
    elif kind == "energy_scale":
        sc = K.scenario_energy_scale()
    else:
        raise ValueError(f"unknown correction spec {spec!r}")
    _CORRECTION_CACHE[key] = sc
    return sc


# ---------------------------------------------------------------------------
# 5. One cell of the frozen grid (the picklable worker entry point)
# ---------------------------------------------------------------------------
def run_cell(task: dict) -> dict:
    """Run every replicate of one cell and return compact per-cell arrays and counts.

    Workers return summaries and a float32 error array - never specimen-level data (D-111).

    Common random numbers (D-107): the noise and correction streams are keyed on
    (archetype, prior error, replicate), so the same replicate index in two cells that differ only in strategy,
    geometry or correction SD sees the same underlying draws. That is what makes the paired comparison of
    D-105 legitimate.
    """
    truth = truth_from_t0(task["use_j"], task["c_c"], task["t0_c"], task.get("lse_j", TRUE_LSE_J))
    geom = D.geometry_info(task["geom_code"], task.get("klst_reading", True))
    scatter = build_scatter(task["scatter"], task.get("cohort_key", "primary"), geom["is_full_size"])
    correction = build_correction(task["correction"])
    n = int(task["n"])
    r = int(task["replicates"])
    crn = task["crn_stream"]

    errors = np.full(r, np.nan, dtype=np.float32)
    deltas = np.full(r, np.nan, dtype=np.float32)
    outcome_counts = np.zeros(len(OUTCOMES) + 1, dtype=np.int64)   # last slot = evaluation errors
    status_counts: dict = {}
    clipped_total = 0
    specimens_total = 0
    distinct_total = 0
    zero_total = 0
    updates_total = 0

    for i in range(r):
        rng_noise = replicate_rng(crn, "noise", i)
        rng_corr = replicate_rng(crn, "correction", i)
        try:
            res = simulate_programme(truth, geom, n, task["strategy"], task["e_prior"], scatter, correction,
                                     rng_noise, rng_corr, task.get("c_assumed", D.C_ASSUMED_C))
        except Exception as exc:                                   # counted, never skipped
            outcome_counts[-1] += 1
            status_counts["evaluation error: " + type(exc).__name__] = \
                status_counts.get("evaluation error: " + type(exc).__name__, 0) + 1
            continue
        if res["available"]:
            errors[i] = res["error_c"]
        deltas[i] = res["delta_c"]
        outcome_counts[res["outcome_code"]] += 1
        status_counts[res["index_status"]] = status_counts.get(res["index_status"], 0) + 1
        clipped_total += res["n_clipped"]
        specimens_total += res["n_specimens"]
        distinct_total += res["n_distinct_raw"]
        zero_total += res["n_zero_energy"]
        updates_total += res["adaptation_updates"]

    return dict(cell_id=task["cell_id"], errors=errors, deltas=deltas,
                outcome_counts=outcome_counts, status_counts=status_counts,
                n_replicates=r, n_specimens=n,
                temperature_clip_fraction=clipped_total / max(1, specimens_total),
                n_distinct_raw_temperatures=distinct_total / max(1, r),
                zero_energy_fraction=zero_total / max(1, specimens_total),
                adaptation_updates=updates_total / max(1, r),
                coldest_reachable_fse_c=D.coldest_reachable_fse_c(geom["m_shift_c"]),
                transition_reachable=bool(truth["t41j_c"] >= D.coldest_reachable_fse_c(geom["m_shift_c"])))
