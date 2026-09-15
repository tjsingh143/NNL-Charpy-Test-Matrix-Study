"""WP4 - Per-curve bootstrap uncertainty: resampling schemes, the refit of every replicate with the approved WP3 method, and the
failure-aware summary of each bootstrap distribution.

Pure functions without file I/O. The SYNTHETIC bootstrap checks (src/wp4_validation.py) and the analysis of the published curves
(src/wp4_uncertainty.py) both call exactly this code. Every choice is recorded, with its source, in DECISIONS.md (D-052 to D-066).

Two resampling schemes (D-052, D-053):
  pairs  PRIMARY. One replicate draws N complete specimen records (temperature and energy together) with replacement from the curve's
         N records and refits them. It does not condition on the tested temperatures: it also resamples which temperatures happen to
         be available, so its spread includes sampling-plan (design) fragility as well as scatter (Efron & Tibshirani 1986 §5;
         MacKinnon 2012 §3).
  wild   FIXED-DESIGN SENSITIVITY. The tested temperatures are kept. Each replicate energy is the approved WP3 fitted curve at that
         temperature plus the curve's own leverage-adjusted residual there multiplied by a random sign (+1 or -1, each with
         probability 1/2: Rademacher weights); energies below 0 J are set to 0 J and counted (Davidson & Flachaire 2001; MacKinnon 2012
         eqs 8-9, transformation w2 = HC2).

Every replicate is refitted with the exact approved WP3 functions (wp3_fitter: lse_setting, fit_curve, index_temperature,
index_fraction_of_rise, classify, criterion_bracketing), in the same order as src/wp3_fit_curves.py::fit_all. Full-size LSE stays fixed at
2.7 J in every replicate; miniature LSE stays fitted >= 0 J (D-054). A replicate that fails, is inadmissible or loses its target is kept in
the denominator (D-057).
"""
from __future__ import annotations

import hashlib
import warnings

import numpy as np

import wp3_fitter as F

# ---------------------------------------------------------------------------
# 1. Constants (each justified in DECISIONS.md)
# ---------------------------------------------------------------------------
WP4_SEED = 20260914                      # D-055: global WP4 seed (the date WP4 began); WP3 used 20260913
B_REPLICATES = 2000                      # D-055: replicates per curve, both methods
B_STABILITY = 4000                       # D-055: Monte Carlo stability rerun of the predeclared subset (independent seed stream)
REPORTABLE_FINITE_FRACTION = 0.95        # D-057: project reporting rule, not an ASTM requirement
QUANTILE_LEVELS = (0.025, 0.1587, 0.5, 0.8413, 0.975)   # D-056: 95 % percentile interval; 16th/84th for a robust spread
LEVERAGE_ONE_TOLERANCE = 1e-8            # D-053: numerical guard; 1 - h below this means the fit passes through the point (residual 0)

PAIRS, WILD = "pairs", "wild"
METHOD_LABELS = {
    PAIRS: "nonparametric pairs (case) bootstrap, PRIMARY",
    WILD: "fixed-design wild bootstrap (Rademacher signs, HC2 leverage-adjusted residuals), SENSITIVITY",
}

# Codes stored per replicate (compact arrays instead of strings).
OUTCOME_CODES = {o: i for i, o in enumerate(F.OUTCOMES)}          # 0 optimizer failure ... 5 usable fit, index temperature calculated
INDEX_STATUS_LABELS = ["calculated", "not calculated: no defensible criterion for this geometry", "not calculated: optimizer failure",
                       "undefined: 41 J outside the fitted shelves (no rise, at or below LSE, or at or above USE)",
                       "unsupported: crossing below the lowest test temperature", "unsupported: crossing above the highest test temperature",
                       "replicate evaluation error"]
EVALUATION_ERROR = -1                    # outcome code of a replicate whose evaluation raised an unexpected exception (counted, never skipped)

TARGETS = {"full-size": ["t41j", "use", "t0", "c"], "miniature": ["t0", "use", "lse", "c"]}   # D-056; C (and miniature LSE) diagnostic
TARGET_ROLE = {("full-size", "t41j"): "primary target", ("full-size", "use"): "target", ("full-size", "t0"): "target",
               ("full-size", "c"): "diagnostic", ("miniature", "t0"): "primary target", ("miniature", "use"): "target",
               ("miniature", "lse"): "diagnostic", ("miniature", "c"): "diagnostic"}
TARGET_LABELS = {"t41j": "T41J (°C)", "t0": "T0 (°C)", "use": "USE (J)", "lse": "LSE (J)", "c": "C (°C)"}
ORIGINAL_COLUMN = {"t41j": "index_temperature_c", "t0": "t0_c", "use": "use_j", "lse": "lse_j", "c": "c_c"}

INTERVAL_PRIMARY = "primary bootstrap CI"
INTERVAL_DIAGNOSTIC = "diagnostic bootstrap interval"
INTERVAL_UNAVAILABLE = "interval unavailable: bootstrap-unstable (finite-target fraction below 95 %)"


# ---------------------------------------------------------------------------
# 2. Seeds (D-055): one independent stream per (global seed, curve or data set, method, replicate), so results never depend on the number
# of worker processes, the chunking or the execution order.
# ---------------------------------------------------------------------------
def int_hash(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest()[:15], 16)


def replicate_rng(stream: str, seed_method: str, replicate: int) -> np.random.Generator:
    """stream: curve ID (published) or synthetic data-set key; seed_method: method name, with a suffix for an independent stream (e.g. the
    Monte Carlo stability rerun)."""
    return np.random.default_rng(np.random.SeedSequence([WP4_SEED, int_hash(stream), int_hash(seed_method), int(replicate)]))


# ---------------------------------------------------------------------------
# 3. The approved WP3 estimate for one data set (the same calls, in the same order, as wp3_fit_curves.fit_all)
# ---------------------------------------------------------------------------
def wp3_estimate(t: np.ndarray, e: np.ndarray, category: str) -> dict:
    """Fit, index temperature, index position, outcome and empirical bracketing exactly as the final approved WP3 method (D-054)."""
    lse_fixed = F.lse_setting(F.PRIMARY_LSE_STRATEGY, "full-size" if category == "full-size" else "miniature", t, e)
    fit = F.fit_curve(t, e, lse_fixed)
    criterion = F.CRITERION_J[category]
    t41, status = F.index_temperature(fit, t, criterion)
    fraction = F.index_fraction_of_rise(fit, criterion)
    cls = F.classify(fit, status, fraction)
    bracket = F.criterion_bracketing(e, criterion, status)
    return dict(fit=fit, criterion=criterion, t41=t41, index_status=status, index_fraction=fraction, cls=cls, bracketing=bracket)


def index_status_code(status: str) -> int:
    if status == "calculated":
        return 0
    if status.startswith("not calculated: no defensible"):
        return 1
    if status.startswith("not calculated: optimizer"):
        return 2
    if status.startswith("undefined"):
        return 3
    if "below the lowest" in status:
        return 4
    if "above the highest" in status:
        return 5
    raise ValueError(f"unknown index status {status!r}")


# ---------------------------------------------------------------------------
# 4. Fixed-design wild bootstrap ingredients (D-053)
# ---------------------------------------------------------------------------
def free_parameter_jacobian(t: np.ndarray, fit: dict) -> np.ndarray:
    """Jacobian of the fitted curve at the WP3 solution with respect to the parameters that are free there, in the scaled parameterization
    of wp3_fitter.fit_curve (energies / highest energy, temperatures about the middle of the tested range / half the span). A parameter at
    one of its bounds (the WP3 at_*_bound_* definition) is treated as fixed; a fixed LSE (full-size) has no column."""
    t = np.asarray(t, float)
    e_s = float(fit["bound_rise_high"]) / F.RISE_MAX_FACTOR          # the highest energy used by the fit (rise bound = 10 x highest energy)
    t_min, t_max = float(t.min()), float(t.max())
    t_ref, t_s = 0.5 * (t_min + t_max), 0.5 * (t_max - t_min)
    rise_s, t0_s, c_s = (fit["use_j"] - fit["lse_j"]) / e_s, (fit["t0_c"] - t_ref) / t_s, fit["c_c"] / t_s
    u = ((t - t_ref) / t_s - t0_s) / c_s
    th = np.tanh(u)
    sech2 = 1.0 - th * th
    at_bound = lambda k: bool(fit.get(f"at_lower_bound_{k}", False) or fit.get(f"at_upper_bound_{k}", False))
    cols = []
    if fit["lse_mode"] == "fitted" and not at_bound("lse"):
        cols.append(np.ones_like(t))
    if not at_bound("rise"):
        cols.append(0.5 * (1.0 + th))
    if not at_bound("t0"):
        cols.append(-0.5 * rise_s * sech2 / c_s)
    if not at_bound("c"):
        cols.append(-0.5 * rise_s * sech2 * u / c_s)
    return np.column_stack(cols) if cols else np.zeros((len(t), 0))


def hat_diagonal(jac: np.ndarray) -> np.ndarray:
    """Leverages h_i: diagonal of the projection onto the column space of the Jacobian (linearized hat matrix), from its singular value
    decomposition with the rank tolerance WP3 uses for the numerically-singular flag (NumPy's default: s > s_max * max(n, p) * eps)."""
    n = jac.shape[0]
    if jac.shape[1] == 0:
        return np.zeros(n)
    u, s, _ = np.linalg.svd(jac, full_matrices=False)
    if s.size == 0 or s.max() <= 0:
        return np.zeros(n)
    keep = s > s.max() * max(jac.shape) * np.finfo(float).eps
    return np.sum(u[:, keep] ** 2, axis=1)


def leverage_adjusted_residuals(t: np.ndarray, e: np.ndarray, fit: dict) -> dict:
    """Residuals of the approved WP3 fit and their HC2 transformation r_i / (1 - h_i)^(1/2) (MacKinnon 2012 eq. 9). Where 1 - h_i is
    numerically zero the fit passes through the point (its residual is 0 at a least-squares solution) and the transformed residual is set
    to 0 and counted."""
    fitted = F.tanh_energy(t, fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"])
    resid = np.asarray(e, float) - fitted
    h = hat_diagonal(free_parameter_jacobian(t, fit))
    one = (1.0 - h) <= LEVERAGE_ONE_TOLERANCE
    adjusted = np.where(one, 0.0, resid / np.sqrt(np.clip(1.0 - h, LEVERAGE_ONE_TOLERANCE, None)))
    return dict(fitted=fitted, residual=resid, leverage=h, adjusted=adjusted, n_leverage_one=int(one.sum()))


# ---------------------------------------------------------------------------
# 5. Replicates
# ---------------------------------------------------------------------------
REPLICATE_FIELDS = ["outcome_code", "index_status_code", "t41j", "t41j_analytic", "t0", "use", "lse", "c", "index_fraction",
                    "index_near_shelf", "bracketed", "n_below_criterion", "n_distinct_temperatures", "n_unique_records", "lost_lowest_temperature",
                    "lost_highest_temperature", "n_clipped_at_zero"]


def _empty_replicate() -> dict:
    return dict(outcome_code=EVALUATION_ERROR, index_status_code=6, t41j=np.nan, t41j_analytic=np.nan, t0=np.nan, use=np.nan, lse=np.nan,
                c=np.nan, index_fraction=np.nan, index_near_shelf=False, bracketed=np.nan, n_below_criterion=-1, n_distinct_temperatures=-1,
                n_unique_records=-1, lost_lowest_temperature=False, lost_highest_temperature=False, n_clipped_at_zero=0)


def evaluate_replicate(t: np.ndarray, e: np.ndarray, category: str) -> dict:
    """Refit one replicate data set with the approved method and reduce it to the stored per-replicate record."""
    est = wp3_estimate(t, e, category)
    fit, cls = est["fit"], est["cls"]
    rec = _empty_replicate()
    rec.update(outcome_code=OUTCOME_CODES[cls["outcome"]], index_status_code=index_status_code(est["index_status"]),
               t41j=est["t41"], index_fraction=est["index_fraction"], index_near_shelf=bool(cls["flag_index_near_fitted_shelf"]),
               n_distinct_temperatures=len(F.temperature_groups(t)[0]))
    if est["criterion"] is not None:
        rec.update(bracketed=float(est["bracketing"]["criterion_bracketed_by_measured_energy"]),
                   n_below_criterion=int(est["bracketing"]["n_points_below_criterion"]))
    if fit.get("optimizer_success", False):
        rec.update(t0=fit["t0_c"], use=fit["use_j"], lse=fit["lse_j"], c=fit["c_c"])
        if est["criterion"] is not None:
            rec["t41j_analytic"] = F.criterion_temperature(fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"], est["criterion"])[0]
    return rec


def run_replicates(t: np.ndarray, e: np.ndarray, category: str, method: str, stream: str, replicates, seed_method: str | None = None,
                   original: dict | None = None) -> dict:
    """Bootstrap replicates `replicates` (an iterable of replicate indices) of one data set. Returns a dict of arrays in replicate order.
    t, e must be in the order WP3 fits them (records sorted by spreadsheet row). original: the WP3 estimate of the data set (computed if
    missing; the wild bootstrap needs its fit)."""
    t, e = np.asarray(t, float), np.asarray(e, float)
    n = len(t)
    replicates = [int(b) for b in replicates]
    seed_method = seed_method or method
    groups, labels = F.temperature_groups(t)
    lowest_group, highest_group = 0, len(groups) - 1
    if method == WILD:
        original = original or wp3_estimate(t, e, category)
        if not original["fit"].get("optimizer_success", False):
            raise ValueError("the fixed-design wild bootstrap needs a converged WP3 fit of the original data")
        adj = leverage_adjusted_residuals(t, e, original["fit"])
    elif method != PAIRS:
        raise ValueError(f"unknown bootstrap method {method!r}")
    rows = []
    for b in replicates:
        rng = replicate_rng(stream, seed_method, b)
        if method == PAIRS:
            idx = np.sort(rng.integers(0, n, size=n))
            tb, eb, clipped = t[idx], e[idx], 0
            drawn = labels[idx]
            unique, lost_low, lost_high = len(np.unique(idx)), bool(not np.any(drawn == lowest_group)), bool(not np.any(drawn == highest_group))
        else:
            signs = np.where(rng.integers(0, 2, size=n) == 1, 1.0, -1.0)
            raw = adj["fitted"] + adj["adjusted"] * signs
            clipped = int(np.sum(raw < 0.0))
            tb, eb = t, np.where(raw < 0.0, 0.0, raw)
            unique, lost_low, lost_high = n, False, False
        try:
            with warnings.catch_warnings():
                # Degenerate resamples (e.g. identical upper-shelf residuals) can make scipy/numpy emit RuntimeWarnings inside the WP3
                # diagnostics; the values they produce are handled by the approved code (a NaN p-value never sets a flag).
                warnings.simplefilter("ignore", RuntimeWarning)
                rec = evaluate_replicate(tb, eb, category)
        except Exception as exc:  # counted as an evaluation error in the denominator, never skipped (D-057)
            rec = _empty_replicate()
            rec["error"] = f"{type(exc).__name__}: {exc}"
        rec.update(n_unique_records=unique, lost_lowest_temperature=lost_low, lost_highest_temperature=lost_high, n_clipped_at_zero=clipped)
        rows.append(rec)
    out = {k: np.array([r[k] for r in rows]) for k in REPLICATE_FIELDS}
    out["replicate"] = np.array(replicates, dtype=int)
    out["errors"] = [r["error"] for r in rows if "error" in r]
    return out


def concatenate(parts: list) -> dict:
    """Join chunks of run_replicates() output in the order given."""
    out = {k: np.concatenate([p[k] for p in parts]) for k in REPLICATE_FIELDS + ["replicate"]}
    out["errors"] = [msg for p in parts for msg in p["errors"]]
    return out


CHUNK_REPLICATES = 250   # replicates per worker task; any value gives identical results (per-replicate seeds)


def make_tasks(key, t, e, category, method, stream, n_replicates, seed_method=None, first_replicate=0, chunk=CHUNK_REPLICATES) -> list:
    """Split one bootstrap run into worker tasks. key identifies the run when the chunks are reassembled."""
    starts = range(first_replicate, first_replicate + n_replicates, chunk)
    return [(key, np.asarray(t, float), np.asarray(e, float), category, method, stream, seed_method,
             range(s, min(s + chunk, first_replicate + n_replicates))) for s in starts]


def run_task(task) -> tuple:
    """Top-level (picklable) worker entry point: (key, chunk result)."""
    key, t, e, category, method, stream, seed_method, replicates = task
    return key, run_replicates(t, e, category, method, stream, replicates, seed_method)


def run_tasks(tasks: list, workers: int) -> dict:
    """Run tasks in worker processes (or in this process if workers == 1) and reassemble each run's chunks in replicate order. Keeps every
    result in memory: only for small jobs (the determinism checks). Large jobs use stream_map()."""
    parts = {}
    for key, part in stream_map(run_task, tasks, workers):
        parts.setdefault(key, []).append(part)
    merged = {}
    for key, chunks in parts.items():
        chunks.sort(key=lambda p: int(p["replicate"][0]))
        merged[key] = concatenate(chunks)
    return merged


# ---------------------------------------------------------------------------
# 7. Memory-bounded parallel execution (systems choice only; results do not depend on it, D-055, D-067)
# ---------------------------------------------------------------------------
# The first synthetic validation run (8 worker processes, every task submitted at once, every replicate array kept by the parent) was
# stopped by the operating environment for low memory on the 8 GB project machine. Each spawned worker imports numpy, scipy and pandas
# (about 110 MB), so the worker count is kept small, workers are recycled, tasks are fed lazily and results are consumed one at a time.
DEFAULT_WORKERS = 3              # conservative for the project machine (Apple M1, 4 performance cores, 8 GB); override with WP4_WORKERS
MAX_TASKS_PER_CHILD = 200        # recycle worker processes so that no allocator growth accumulates over a long run


def worker_count() -> int:
    import os
    env = os.environ.get("WP4_WORKERS", "").strip()
    return max(1, int(env)) if env else max(1, min(DEFAULT_WORKERS, os.cpu_count() or 1))


def stream_map(func, tasks, workers: int):
    """Yield func(task) for each task, in task order, while holding only a few results in memory. `tasks` may be a generator; func must be a
    top-level (picklable) function. With workers <= 1 everything runs in this process. Per-replicate seeds make the results identical for
    any worker count, chunking or order (checked in src/wp4_validation.py)."""
    if workers <= 1:
        for task in tasks:
            yield func(task)
        return
    import multiprocessing
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(processes=workers, maxtasksperchild=MAX_TASKS_PER_CHILD) as pool:
        for result in pool.imap(func, tasks, chunksize=1):
            yield result


# ---------------------------------------------------------------------------
# 6. Target availability, accounting and summaries (D-056, D-057, D-058)
# ---------------------------------------------------------------------------
def target_available(reps: dict, target: str) -> np.ndarray:
    """A target value exists for a replicate when the approved method produced it: T41J when its index status is 'calculated'; T0, C, USE
    and LSE when the fit converged and is not non-physical (inadmissible), because such a fit has no admissible transition (D-046)."""
    if target == "t41j":
        return reps["index_status_code"] == 0
    return (reps["outcome_code"] >= OUTCOME_CODES["boundary-limited"])


def accounting(reps: dict, category: str) -> dict:
    """Mutually exclusive replicate outcomes (they sum to the replicates requested) and the support diagnostics of the replicates."""
    oc = reps["outcome_code"]
    requested = len(oc)
    d = dict(replicates_requested=requested, replicate_evaluation_errors=int(np.sum(oc == EVALUATION_ERROR)))
    for outcome, code in OUTCOME_CODES.items():
        d[f"replicates_{outcome}"] = int(np.sum(oc == code))
    if sum(v for k, v in d.items() if k.startswith("replicates_") and k != "replicates_requested") != requested:
        raise AssertionError("replicate outcome counts do not add up to the replicates requested")
    d["replicates_optimizer_success"] = int(np.sum(oc >= OUTCOME_CODES["non-physical (inadmissible)"]))
    d["replicates_admissible"] = int(np.sum(oc >= OUTCOME_CODES["boundary-limited"]))
    d["replicates_usable_outcome"] = int(np.sum(oc >= OUTCOME_CODES["usable fit, index temperature unavailable"]))
    d["replicates_with_lost_lowest_temperature"] = int(np.sum(reps["lost_lowest_temperature"]))
    d["replicates_with_lost_highest_temperature"] = int(np.sum(reps["lost_highest_temperature"]))
    d["median_distinct_temperatures"] = float(np.median(reps["n_distinct_temperatures"]))
    d["median_unique_records"] = float(np.median(reps["n_unique_records"]))
    d["energies_set_to_zero_per_replicate"] = float(np.mean(reps["n_clipped_at_zero"]))
    if category == "full-size":
        calc = reps["index_status_code"] == 0
        for code, label in enumerate(INDEX_STATUS_LABELS):
            d[f"t41j_status_{code}"] = int(np.sum(reps["index_status_code"] == code))
        d["replicates_energies_bracket_41j"] = int(np.nansum(reps["bracketed"] == 1.0))
        d["t41j_calculated_not_bracketed"] = int(np.sum(calc & (reps["bracketed"] == 0.0)))
        d["t41j_calculated_index_position_warning"] = int(np.sum(calc & reps["index_near_shelf"]))
        d["t41j_calculated_from_usable_replicate_fit"] = int(np.sum(calc & (reps["outcome_code"] == OUTCOME_CODES[F.OUTCOMES[5]])))
        d["t41j_calculated_from_weak_or_boundary_replicate_fit"] = int(np.sum(calc & np.isin(reps["outcome_code"], [2, 3])))
    return d


def interval_label(original_outcome: str, finite_fraction: float) -> str:
    """D-058: a reportable interval (finite-target fraction >= 95 % of the replicates requested, D-057) is a primary bootstrap CI when the
    original WP3 fit is usable and a diagnostic bootstrap interval otherwise; the bootstrap never upgrades the WP3 outcome."""
    if not finite_fraction >= REPORTABLE_FINITE_FRACTION:
        return INTERVAL_UNAVAILABLE
    return INTERVAL_PRIMARY if original_outcome in F.OUTCOMES[4:] else INTERVAL_DIAGNOSTIC


def summarise_target(reps: dict, target: str, original_value: float, original_outcome: str) -> dict:
    """Bootstrap distribution of one target. Quantiles use NumPy's default linear interpolation and are always computed from the finite
    values (conditional quantiles, kept for audit); whether they form a reportable interval is decided by the finite-target fraction of
    ALL replicates requested (D-057)."""
    requested = len(reps["outcome_code"])
    avail = target_available(reps, target)
    v = reps[target][avail]
    v = v[np.isfinite(v)]
    n = len(v)
    fraction = n / requested
    d = dict(replicates_requested=requested, finite_target_values=n, target_unavailable=requested - n, finite_target_fraction=fraction,
             original_estimate=original_value)
    if n >= 2:
        q = np.quantile(v, QUANTILE_LEVELS)
        d.update(q025=q[0], q16=q[1], median=q[2], q84=q[3], q975=q[4], mean=float(v.mean()), sd=float(v.std(ddof=1)),
                 interval_width=q[4] - q[0], robust_sd_q84_minus_q16_over_2=0.5 * (q[3] - q[1]),
                 bias_mean_minus_original=float(v.mean()) - original_value if np.isfinite(original_value) else np.nan)
    else:
        d.update(q025=np.nan, q16=np.nan, median=np.nan, q84=np.nan, q975=np.nan, mean=np.nan, sd=np.nan, interval_width=np.nan,
                 robust_sd_q84_minus_q16_over_2=np.nan, bias_mean_minus_original=np.nan)
    d["interval_reportable"] = bool(fraction >= REPORTABLE_FINITE_FRACTION)
    d["interval_label"] = interval_label(original_outcome, fraction)
    return d


def summarise_run(reps: dict, category: str, originals: dict, original_outcome: str, targets=None) -> dict:
    """Everything later steps need from one bootstrap run except the replicate arrays: the accounting and one summary per target
    (original values by target; targets default to the geometry's list). Used by workers so that replicate arrays need not be kept."""
    targets = targets or TARGETS[category]
    return dict(accounting=accounting(reps, category), errors=sorted(set(reps["errors"])),
                targets={tg: summarise_target(reps, tg, originals.get(tg, np.nan), original_outcome) for tg in targets})


def mean_curve_band(reps: dict, grid_t: np.ndarray, levels=(0.025, 0.975)) -> tuple:
    """Pointwise percentile band of the fitted mean curve E_b(T) over the admissible replicates (a confidence band for the mean curve, not a
    prediction interval for a new specimen). Returns (lower, upper, number of replicates used)."""
    ok = reps["outcome_code"] >= OUTCOME_CODES["boundary-limited"]
    curves = np.array([F.tanh_energy(grid_t, l, u, t0, c) for l, u, t0, c in
                       zip(reps["lse"][ok], reps["use"][ok], reps["t0"][ok], reps["c"][ok])])
    if len(curves) < 2:
        return np.full_like(grid_t, np.nan), np.full_like(grid_t, np.nan), int(ok.sum())
    lo, hi = np.quantile(curves, levels, axis=0)
    return lo, hi, int(ok.sum())
