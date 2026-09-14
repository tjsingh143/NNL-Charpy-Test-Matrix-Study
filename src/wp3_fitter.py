"""WP3 - Hyperbolic-tangent transition-curve fitter: model, bounded least-squares fit, diagnostics, index temperature.

Pure functions without file I/O. The synthetic validation (src/wp3_validation.py) and the fits to the published Charpy data
(src/wp3_fit_curves.py) both call exactly this code, so what is validated is what is applied. Every choice is recorded, with its
source, in DECISIONS.md (D-040 to D-051; the CP3 amendments of D-042, D-044 and D-046 are marked where they apply).

Model (D-040):  E(T) = LSE + (USE - LSE) / 2 * [1 + tanh((T - T0) / C)]
    LSE  lower-shelf energy (J)             USE  upper-shelf energy (J)
    T0   mid-transition temperature (°C)    C    transition half-width (°C): between T0 - C and T0 + C the curve rises from
                                                 11.9 % to 88.1 % of (USE - LSE)
Equivalent form E = A + B tanh((T - D) / C) with A = (USE + LSE) / 2, B = (USE - LSE) / 2, D = T0 (Switzner et al. 2023 Eqs 1-3;
Sokolov & Nanstad 1995 Eq. 1). The solver works on (LSE, RISE = USE - LSE, T0, C), so box bounds keep USE >= LSE and C > 0.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares
from scipy.stats import linregress

from wp2_curves import BAND_LOWER, DISTINCT_TEMPERATURE_GAP_C, screening_references

# ---------------------------------------------------------------------------
# 1. Constants (each justified in DECISIONS.md)
# ---------------------------------------------------------------------------
# D-041. Bounds. Physical: LSE >= 0 J (absorbed energy cannot be negative), USE - LSE >= 0 (energy does not fall as temperature
# rises in this model), T0 >= -273.15 °C. Numerical safety, deliberately wide so that a fit resting on one of them signals that
# the data do not constrain that parameter: C >= 1 °C (below the 2 °C test-temperature resolution of D-037), C <= the tested
# temperature span, T0 within one span of the tested range, USE - LSE <= 10 x the highest measured energy, LSE <= the highest
# measured energy. A parameter counts as on a bound if least_squares reports the bound active or it lies within 0.1 % of the
# bound interval of it.
ABSOLUTE_ZERO_C = -273.15
C_MIN_C = 1.0
RISE_MAX_FACTOR = 10.0
NEAR_BOUND_FRACTION = 1e-3

# D-041. Optimizer: scipy.optimize.least_squares, trust-region reflective ('trf', the SciPy method for box bounds), analytic
# Jacobian, parameters scaled to order one, ordinary (unweighted) least squares, six predefined deterministic starts.
MAX_NFEV = 2000
TOLERANCE = 1e-10

# D-047. Identifiability diagnostics, defined on the fitted curve with x = (T - T0) / C.
X_TRANSITION = 1.0           # -1 < x < 1: the central characteristic interval (11.9-88.1 % of the rise; D-037)
X_SHELF = 1.5                # |x| >= 1.5: fitted curve within 4.7 % of the rise from a shelf (upper: >= 95.3 % of the rise)
MIN_TRANSITION_TEMPERATURES = 2
MIN_SHELF_POINTS = 2
TREND_P_VALUE = 0.05         # residual trend on the upper shelf (two-sided t-test on the regression slope)

# D-044, D-045. Index criterion per geometry category. Only standard full-size specimens have a defensible criterion.
FULL_SIZE_CRITERION_J = 41.0
CRITERION_J = {"full-size": FULL_SIZE_CRITERION_J, "sub-size (E23 type)": None, "miniature": None}

# D-044, index-support diagnostic (added at the author's CP3 instruction, 2026-09-14): a calculated index whose criterion lies outside
# the central characteristic interval of the fitted rise (x = -1...+1, 11.9-88.1 % of USE - LSE; the interval of D-037 and D-047) sits
# on a flat part of the fitted curve, where the curve is less steep and the index less firmly anchored. Reported beside the value; the
# value is never withheld because of it, and it is not part of the outcome.
INDEX_RISE_FRACTION_LOW = 0.5 * (1.0 + np.tanh(-X_TRANSITION))    # 0.1192
INDEX_RISE_FRACTION_HIGH = 0.5 * (1.0 + np.tanh(X_TRANSITION))    # 0.8808

# D-044, empirical-bracketing support diagnostic (added at the author's final CP3 approval, 2026-09-14, after published curve 33-153 showed
# that the index-position diagnostic above cannot see it). A different question from the index position: not where the criterion lies on
# the fitted curve, but whether the measured energies themselves lie on both sides of it, min(E) <= criterion <= max(E). A calculated
# index whose criterion is not bracketed is supplied by the fitted curve (its shape and its fixed or fitted shelf) rather than by
# observations on both sides. A project support diagnostic, not an ASTM requirement: the value is kept, and the diagnostic is computed
# outside classify(), so it cannot change a fit outcome. Only the full-size 41 J criterion exists (CRITERION_J), hence the wording.
INDEX_NOT_BRACKETED_TEXT = "T41J calculated from fitted curve; 41 J not empirically bracketed by measured energies."

# D-042. Lower-shelf strategies.
# The four candidates pre-registered for synthetic Block L (commit 11daf72). fixed_convention: 2.7 J for full-size and 0.1 J for
# sub-size specimens, Sokolov & Nanstad (1995), ASTM STP 1270, p. 7.
FIXED_LSE_CONVENTION_J = {"full-size": 2.7, "miniature": 0.1}
LSE_STRATEGIES = ["fitted", "fixed_convention", "fixed_zero", "hybrid"]
HYBRID_MIN_LOWER_BAND_TEMPERATURES = 2
# The pre-registered rule selected `fitted` for every geometry; that method was presented at CP3. At CP3 the author amended D-042
# (2026-09-14): the FINAL PRIMARY method is `geometry_specific`, LSE fixed at 2.7 J for full-size 55 x 10 x 10 mm specimens
# (Sokolov & Nanstad 1995 p. 7) and fitted, bounded below by 0 J, for miniature specimens (no 0.1 J miniature convention). It is not
# a Block L candidate and was not selected by the pre-registered rule. The all-fitted method stays as an explicit sensitivity case.
PRIMARY_LSE_STRATEGY = "geometry_specific"
SENSITIVITY_LSE_STRATEGY = "fitted"
LSE_STRATEGY_LABELS = {
    "geometry_specific": "geometry-specific: LSE fixed at 2.7 J (full-size), fitted >= 0 J (miniature)",
    "fitted": "all fitted: LSE fitted >= 0 J for every geometry (pre-registered rule outcome)",
    "fixed_convention": "fixed convention: 2.7 J (full-size), 0.1 J (miniature)",
    "fixed_zero": "fixed at 0 J",
    "hybrid": "hybrid: fitted if >= 2 lower-band temperatures, else the fixed convention",
}


# ---------------------------------------------------------------------------
# 2. Model and small helpers
# ---------------------------------------------------------------------------
def tanh_energy(t, lse: float, use: float, t0: float, c: float) -> np.ndarray:
    return lse + 0.5 * (use - lse) * (1.0 + np.tanh((np.asarray(t, float) - t0) / c))


def temperature_groups(t: np.ndarray) -> tuple:
    """Distinct test temperatures as in D-037: after sorting, a gap larger than 2 °C starts a new temperature.
    Returns (mean temperature of each group, group label of every point)."""
    t = np.asarray(t, float)
    order = np.argsort(t, kind="mergesort")
    ts = t[order]
    group_sorted = np.cumsum(np.r_[True, np.diff(ts) > DISTINCT_TEMPERATURE_GAP_C]) - 1
    labels = np.empty(len(t), dtype=int)
    labels[order] = group_sorted
    means = np.array([ts[group_sorted == g].mean() for g in range(group_sorted[-1] + 1)])
    return means, labels


def criterion_temperature(lse: float, use: float, t0: float, c: float, e_crit: float) -> tuple:
    """Temperature at which the fitted curve equals e_crit, solved analytically:
    T = T0 + C * artanh(2 (e_crit - LSE) / (USE - LSE) - 1). Defined only if LSE < e_crit < USE (D-044)."""
    if not np.all(np.isfinite([lse, use, t0, c])) or use - lse <= 0:
        return np.nan, "undefined: no rise between the fitted shelves"
    if e_crit <= lse:
        return np.nan, f"undefined: {e_crit:g} J at or below the fitted LSE"
    if e_crit >= use:
        return np.nan, f"undefined: {e_crit:g} J at or above the fitted USE"
    q = 2.0 * (e_crit - lse) / (use - lse) - 1.0
    return float(t0 + c * np.arctanh(q)), "defined"


def prefit_lower_band_temperatures(t: np.ndarray, e: np.ndarray) -> int:
    """WP2 pre-fit descriptor n_T_lower_band (D-037): distinct temperatures whose energy lies at or below 12 % of the way from
    the lowest measured energy to the screening upper reference. Uses no fitted quantity (used by the hybrid lower-shelf rule)."""
    e_lo, e_hi = screening_references(np.asarray(e, float))
    pos = (e - e_lo) / (e_hi - e_lo) if e_hi > e_lo else np.zeros_like(e)
    lower = np.asarray(t, float)[pos <= BAND_LOWER]
    if len(lower) == 0:
        return 0
    return len(temperature_groups(lower)[0])


def lse_setting(strategy: str, geometry_category: str, t: np.ndarray, e: np.ndarray):
    """None = LSE is fitted; a number = LSE fixed at that value (J). geometry_category: 'full-size' or 'miniature' (D-042)."""
    convention = FIXED_LSE_CONVENTION_J["full-size" if geometry_category == "full-size" else "miniature"]
    if strategy == "geometry_specific":
        return FIXED_LSE_CONVENTION_J["full-size"] if geometry_category == "full-size" else None
    if strategy == "fitted":
        return None
    if strategy == "fixed_convention":
        return convention
    if strategy == "fixed_zero":
        return 0.0
    if strategy == "hybrid":
        return None if prefit_lower_band_temperatures(t, e) >= HYBRID_MIN_LOWER_BAND_TEMPERATURES else convention
    raise ValueError(f"unknown lower-shelf strategy {strategy!r}")


# ---------------------------------------------------------------------------
# 3. The fit
# ---------------------------------------------------------------------------
def _starts(t: np.ndarray, e: np.ndarray, lse_fixed, bounds: dict) -> list:
    """Six predefined deterministic starting points (D-041): LSE = lowest energy (or the fixed value); USE = mean of the three
    highest energies (the WP2 screening upper reference, used here only as a starting value); T0 in {temperature where the
    per-temperature mean energy first crosses the midpoint between those two, lower quartile, upper quartile of the distinct test
    temperatures}; C in {span / 12, span / 4}."""
    groups, labels = temperature_groups(t)
    mean_e = np.array([e[labels == g].mean() for g in range(len(groups))])
    lse0 = float(e.min()) if lse_fixed is None else float(lse_fixed)
    use0 = float(screening_references(e)[1])
    mid = 0.5 * (lse0 + use0)
    above = np.nonzero(mean_e >= mid)[0]
    if len(above) == 0:
        t_cross = groups[-1]
    elif above[0] == 0:
        t_cross = groups[0]
    else:
        k = above[0]
        t_cross = groups[k - 1] + (mid - mean_e[k - 1]) * (groups[k] - groups[k - 1]) / (mean_e[k] - mean_e[k - 1])
    span = t.max() - t.min()
    t0_starts = [t_cross, float(np.quantile(groups, 0.25)), float(np.quantile(groups, 0.75))]
    c_starts = [span / 12.0, span / 4.0]
    clip = lambda v, name: float(np.clip(v, bounds[name][0], bounds[name][1]))
    rise0 = max(use0 - lse0, 0.05 * e.max())
    starts = []
    for t0 in t0_starts:
        for c in c_starts:
            s = dict(rise=clip(rise0, "rise"), t0=clip(t0, "t0"), c=clip(c, "c"))
            if lse_fixed is None:
                s["lse"] = clip(lse0, "lse")
            starts.append(s)
    return starts


def fit_curve(t, e, lse_fixed=None) -> dict:
    """Bounded ordinary least-squares tanh fit of absorbed energy e (J) against test temperature t (°C).
    lse_fixed: None to fit LSE, or the fixed LSE value (J). Returns estimates, bounds, optimizer metadata and diagnostics."""
    t, e = np.asarray(t, float), np.asarray(e, float)
    names = (["lse"] if lse_fixed is None else []) + ["rise", "t0", "c"]
    n, p = len(t), len(names)
    out = dict(n_points=n, n_parameters=p, lse_mode="fitted" if lse_fixed is None else "fixed",
               lse_fixed_j=np.nan if lse_fixed is None else float(lse_fixed))
    if n <= p or np.ptp(t) <= 0 or e.max() <= 0:
        return {**out, "optimizer_success": False, "optimizer_status": np.nan,
                "optimizer_message": "not attempted: fewer points than parameters, one test temperature, or no positive energy"}
    e_max, t_min, t_max = float(e.max()), float(t.min()), float(t.max())
    span = t_max - t_min
    bounds = dict(lse=(0.0, e_max), rise=(0.0, RISE_MAX_FACTOR * e_max),
                  t0=(max(ABSOLUTE_ZERO_C, t_min - span), t_max + span), c=(C_MIN_C, max(span, 2.0 * C_MIN_C)))
    # Scale to order one: energies by the highest measured energy, temperatures about the middle of the tested range.
    e_s, t_ref, t_s = e_max, 0.5 * (t_min + t_max), 0.5 * span
    to_scaled = dict(lse=lambda v: v / e_s, rise=lambda v: v / e_s, t0=lambda v: (v - t_ref) / t_s, c=lambda v: v / t_s)
    to_phys = dict(lse=lambda v: v * e_s, rise=lambda v: v * e_s, t0=lambda v: v * t_s + t_ref, c=lambda v: v * t_s)
    tau = (t - t_ref) / t_s
    lse_s_fixed = None if lse_fixed is None else float(lse_fixed) / e_s

    def unpack(z):
        if lse_fixed is None:
            return z[0], z[1], z[2], z[3]
        return lse_s_fixed, z[0], z[1], z[2]

    def residuals(z):
        lse_s, rise_s, t0_s, c_s = unpack(z)
        return lse_s + 0.5 * rise_s * (1.0 + np.tanh((tau - t0_s) / c_s)) - e / e_s

    def jacobian(z):
        lse_s, rise_s, t0_s, c_s = unpack(z)
        u = (tau - t0_s) / c_s
        th = np.tanh(u)
        sech2 = 1.0 - th * th
        cols = [0.5 * (1.0 + th), -0.5 * rise_s * sech2 / c_s, -0.5 * rise_s * sech2 * u / c_s]
        if lse_fixed is None:
            cols = [np.ones_like(tau)] + cols
        return np.column_stack(cols)

    lb = np.array([to_scaled[k](bounds[k][0]) for k in names])
    ub = np.array([to_scaled[k](bounds[k][1]) for k in names])
    trials = []
    for i, s in enumerate(_starts(t, e, lse_fixed, bounds)):
        z0 = np.clip(np.array([to_scaled[k](s[k]) for k in names]), lb, ub)
        try:
            r = least_squares(residuals, z0, jac=jacobian, bounds=(lb, ub), method="trf", x_scale=1.0,
                              ftol=TOLERANCE, xtol=TOLERANCE, gtol=TOLERANCE, max_nfev=MAX_NFEV)
            ok = bool(r.status > 0 and np.all(np.isfinite(r.x)) and np.isfinite(r.cost))
            trials.append(dict(start=i, z0=z0, result=r, ok=ok, cost=float(r.cost) if np.isfinite(r.cost) else np.inf))
        except (ValueError, FloatingPointError) as exc:  # recorded, never silently skipped
            trials.append(dict(start=i, z0=z0, result=None, ok=False, cost=np.inf, error=str(exc)))
    good = [tr for tr in trials if tr["ok"]]
    out.update(n_starts=len(trials), n_starts_success=len(good))
    for k in names:
        out[f"bound_{k}_low"], out[f"bound_{k}_high"] = bounds[k]
    if not good:
        last = trials[-1]
        msg = last["result"].message if last.get("result") is not None else last.get("error", "")
        return {**out, "optimizer_success": False, "optimizer_status": getattr(last.get("result"), "status", np.nan),
                "optimizer_message": f"no start reached an admissible solution; last message: {msg}"}
    best_cost = min(tr["cost"] for tr in good)
    best = next(tr for tr in good if tr["cost"] <= best_cost * (1.0 + 1e-9) + 1e-15)  # earliest start among equal-cost optima
    r = best["result"]
    est = {k: to_phys[k](v) for k, v in zip(names, r.x)}
    lse = float(lse_fixed) if lse_fixed is not None else est["lse"]
    use, t0, c = lse + est["rise"], est["t0"], est["c"]
    near = [tr for tr in good if tr["cost"] <= best_cost * 1.01 + 1e-15]
    near_t0 = [to_phys["t0"](tr["result"].x[names.index("t0")]) for tr in near]
    at_low, at_high = {}, {}
    for j, k in enumerate(names):
        width = ub[j] - lb[j]
        at_low[k] = bool(r.active_mask[j] == -1 or r.x[j] - lb[j] <= NEAR_BOUND_FRACTION * width)
        at_high[k] = bool(r.active_mask[j] == 1 or ub[j] - r.x[j] <= NEAR_BOUND_FRACTION * width)
    sv = np.linalg.svd(r.jac, compute_uv=False)
    rank = int(np.sum(sv > sv.max() * max(r.jac.shape) * np.finfo(float).eps)) if sv.max() > 0 else 0
    fitted = tanh_energy(t, lse, use, t0, c)
    sse = float(np.sum((e - fitted) ** 2))
    out.update(optimizer_success=True, optimizer_status=int(r.status), optimizer_message=str(r.message),
               best_start=int(best["start"]), start_values=" | ".join(
                   ", ".join(f"{k}={to_phys[k](v):.4g}" for k, v in zip(names, tr["z0"])) for tr in trials),
               nfev=int(r.nfev), n_starts_within_1pct_of_best_cost=len(near),
               t0_spread_within_1pct_of_best_cost_c=float(np.ptp(near_t0)),
               lse_j=lse, use_j=use, t0_c=t0, c_c=c, sse=sse, rmse_j=float(np.sqrt(sse / n)),
               residual_sd_j=float(np.sqrt(sse / (n - p))), jacobian_rank=rank, jacobian_condition_number=
               float(sv.max() / sv.min()) if sv.min() > 0 else np.inf)
    for k in names:
        out[f"at_lower_bound_{k}"], out[f"at_upper_bound_{k}"] = at_low[k], at_high[k]
    out.update(coverage_diagnostics(t, e, lse, use, t0, c))
    return out


# ---------------------------------------------------------------------------
# 4. Diagnostics, index temperature and outcome
# ---------------------------------------------------------------------------
def coverage_diagnostics(t: np.ndarray, e: np.ndarray, lse: float, use: float, t0: float, c: float) -> dict:
    """Where the tested temperatures sit on the fitted curve (D-043, D-047). x = (T - T0) / C."""
    groups, _ = temperature_groups(t)
    x_point, x_group = (t - t0) / c, (groups - t0) / c
    n_upper, n_lower = int(np.sum(x_point >= X_SHELF)), int(np.sum(x_point <= -X_SHELF))
    support = lambda k: "supported" if k >= MIN_SHELF_POINTS else ("single specimen" if k == 1 else "extrapolated")
    d = dict(x_lowest_test=float(x_point.min()), x_highest_test=float(x_point.max()),
             fraction_of_rise_at_highest_test=float(0.5 * (1.0 + np.tanh(x_point.max()))),
             n_T_transition_fit=int(np.sum(np.abs(x_group) < X_TRANSITION)),
             n_points_upper_shelf_fit=n_upper, n_points_lower_shelf_fit=n_lower,
             use_support=support(n_upper), lse_support=support(n_lower))
    # USE as ASTM E185-82 §4.18 defines it (average of the specimens above the transition), approximated with the fitted curve
    # because the dataset has no shear-fracture data: mean energy of the specimens at x >= 1.5. Diagnostic only; not the estimate.
    upper = x_point >= X_SHELF
    d["use_plateau_mean_j"] = float(e[upper].mean()) if n_upper >= MIN_SHELF_POINTS else np.nan
    # Upper-shelf trend: do the residuals on the fitted upper shelf drift with temperature (a rising or falling "shelf")?
    d.update(upper_shelf_trend_j_per_100c=np.nan, upper_shelf_trend_p_value=np.nan)
    if n_upper >= 3 and len(temperature_groups(t[upper])[0]) >= 2:
        reg = linregress(t[upper], (e - tanh_energy(t, lse, use, t0, c))[upper])
        d.update(upper_shelf_trend_j_per_100c=float(100.0 * reg.slope), upper_shelf_trend_p_value=float(reg.pvalue))
    return d


def index_temperature(fit: dict, t: np.ndarray, criterion_j) -> tuple:
    """Index temperature and its status (D-044, D-045). Never extrapolated beyond the tested temperatures."""
    if criterion_j is None:
        return np.nan, "not calculated: no defensible criterion for this geometry"
    if not fit.get("optimizer_success", False):
        return np.nan, "not calculated: optimizer failure"
    value, status = criterion_temperature(fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"], criterion_j)
    if status != "defined":
        return np.nan, status
    if value < np.min(t):
        return np.nan, "unsupported: crossing below the lowest test temperature"
    if value > np.max(t):
        return np.nan, "unsupported: crossing above the highest test temperature"
    return value, "calculated"


def index_fraction_of_rise(fit: dict, criterion_j) -> float:
    """Where the criterion sits on the fitted rise, (E_crit - LSE) / (USE - LSE). The synthetic validation showed that T41J is less
    precise when 41 J lies near a shelf (Block C, USE 44 J); since CP3 a calculated index outside the central 11.9-88.1 % of the rise
    carries flag_index_near_fitted_shelf (index-support diagnostic, D-044), which never withholds the value."""
    if criterion_j is None or not fit.get("optimizer_success", False) or fit["use_j"] <= fit["lse_j"]:
        return np.nan
    return float((criterion_j - fit["lse_j"]) / (fit["use_j"] - fit["lse_j"]))


def criterion_bracketing(e: np.ndarray, criterion_j, index_status: str) -> dict:
    """Empirical-bracketing support diagnostic (D-044, final CP3 approval): the measured energies below, exactly at and above the
    criterion, whether they bracket it, min(E) <= criterion <= max(E), and for a calculated index a warning when they do not. Uses the
    measurements only; never withholds or changes the index and is not an input to classify(), so no outcome depends on it."""
    e = np.asarray(e, float)
    out = dict(measured_energy_min_j=float(e.min()), measured_energy_max_j=float(e.max()))
    calculated = index_status == "calculated"
    if criterion_j is None:
        return {**out, "n_points_below_criterion": np.nan, "n_points_at_criterion": np.nan, "n_points_above_criterion": np.nan,
                "criterion_bracketed_by_measured_energy": np.nan, "flag_index_not_bracketed_by_measured_energy": False,
                "index_empirical_bracketing": "no index calculated"}
    bracketed = bool(e.min() <= criterion_j <= e.max())
    return {**out, "n_points_below_criterion": int(np.sum(e < criterion_j)), "n_points_at_criterion": int(np.sum(e == criterion_j)),
            "n_points_above_criterion": int(np.sum(e > criterion_j)), "criterion_bracketed_by_measured_energy": bracketed,
            "flag_index_not_bracketed_by_measured_energy": calculated and not bracketed,
            "index_empirical_bracketing": ("no index calculated" if not calculated else
                                           f"{criterion_j:g} J bracketed by measured energies" if bracketed else INDEX_NOT_BRACKETED_TEXT)}


OUTCOMES = ["optimizer failure", "non-physical (inadmissible)", "boundary-limited", "weakly identified",
            "usable fit, index temperature unavailable", "usable fit, index temperature calculated"]

# Fit diagnostics (describe the fit) and index diagnostics (describe the index temperature). Only fit diagnostics other than
# flag_nonflat_upper_shelf take part in the outcome; flag_nonflat_upper_shelf (model adequacy, D-043) and both index diagnostics are
# reported beside it. The empirical-bracketing flag (flag_index_not_bracketed_by_measured_energy, D-044) is set by criterion_bracketing(),
# deliberately outside classify(): it needs the measured energies, and keeping it out of classify() guarantees it cannot move an outcome.
FIT_FLAGS = ["flag_optimizer_failure", "flag_nonphysical_no_rise", "flag_nonphysical_t0_at_absolute_zero", "flag_lse_at_lower_bound",
             "flag_boundary_c_min", "flag_boundary_c_max", "flag_boundary_t0_limit", "flag_boundary_rise_max", "flag_boundary_lse_max",
             "flag_weak_transition", "flag_weak_upper_shelf", "flag_nonflat_upper_shelf", "flag_weak_lower_shelf",
             "flag_numerically_singular"]
INDEX_FLAGS = ["flag_index_unavailable", "flag_index_near_fitted_shelf"]
OUTCOME_FLAG_GROUPS = [
    # Non-physical (inadmissible): even the constrained best fit has no admissible transition. A zero rise means no ductile-to-brittle
    # transition at all (T0 and C lose their meaning); T0 at absolute zero places the transition at the physical temperature limit.
    ("non-physical (inadmissible)", ["flag_nonphysical_no_rise", "flag_nonphysical_t0_at_absolute_zero"]),
    # Boundary-limited: the fit rests on a bound. flag_lse_at_lower_bound (fitted LSE at 0 J) belongs here since the CP3 amendment of
    # D-046: the constrained fit wants the lower asymptote at its allowed boundary, meaning the lower shelf is not independently supported
    # or the symmetric tanh is compensating for a curve-shape mismatch. A 0 J lower shelf is an admissible value (Marini 2020 fixes it),
    # and the measured energies are physical; the pre-registered version counted it as non-physical.
    ("boundary-limited", ["flag_lse_at_lower_bound", "flag_boundary_c_min", "flag_boundary_c_max", "flag_boundary_t0_limit",
                          "flag_boundary_rise_max", "flag_boundary_lse_max"]),
    ("weakly identified", ["flag_weak_transition", "flag_weak_upper_shelf", "flag_weak_lower_shelf", "flag_numerically_singular"]),
]


def classify(fit: dict, index_status: str, index_fraction: float = np.nan) -> dict:
    """Diagnostic flags (may overlap) and one mutually exclusive outcome, assigned in the precedence order of OUTCOMES (D-046, as amended
    at CP3). flag_nonflat_upper_shelf is a model-adequacy flag reported beside the outcome, not part of it (D-047, changed after the
    synthetic validation: on correctly specified synthetic curves it fired only by chance and flagged fits were no less accurate).
    index_fraction = index_fraction_of_rise(); it sets the index-support diagnostic flag_index_near_fitted_shelf (D-044)."""
    f = {k: False for k in FIT_FLAGS + INDEX_FLAGS}
    f["flag_index_unavailable"] = index_status != "calculated"
    f["flag_index_near_fitted_shelf"] = bool(index_status == "calculated" and np.isfinite(index_fraction) and not
                                             INDEX_RISE_FRACTION_LOW <= index_fraction <= INDEX_RISE_FRACTION_HIGH)
    if not fit.get("optimizer_success", False):
        f["flag_optimizer_failure"] = True
        return {**f, "outcome": OUTCOMES[0], "outcome_reason": fit.get("optimizer_message", "")}
    fitted_lse = fit["lse_mode"] == "fitted"
    physical_t0_floor = fit["bound_t0_low"] <= ABSOLUTE_ZERO_C + 1e-9
    f["flag_nonphysical_no_rise"] = fit["at_lower_bound_rise"]
    f["flag_nonphysical_t0_at_absolute_zero"] = fit["at_lower_bound_t0"] and physical_t0_floor
    f["flag_lse_at_lower_bound"] = fitted_lse and fit["at_lower_bound_lse"]
    f["flag_boundary_c_min"] = fit["at_lower_bound_c"]
    f["flag_boundary_c_max"] = fit["at_upper_bound_c"]
    f["flag_boundary_t0_limit"] = fit["at_upper_bound_t0"] or (fit["at_lower_bound_t0"] and not physical_t0_floor)
    f["flag_boundary_rise_max"] = fit["at_upper_bound_rise"]
    f["flag_boundary_lse_max"] = fitted_lse and fit["at_upper_bound_lse"]
    f["flag_weak_transition"] = fit["n_T_transition_fit"] < MIN_TRANSITION_TEMPERATURES
    f["flag_weak_upper_shelf"] = fit["use_support"] != "supported"
    f["flag_nonflat_upper_shelf"] = bool(fit["upper_shelf_trend_p_value"] < TREND_P_VALUE)
    f["flag_weak_lower_shelf"] = fitted_lse and fit["lse_support"] != "supported"
    f["flag_numerically_singular"] = fit["jacobian_rank"] < fit["n_parameters"]
    for outcome, keys in OUTCOME_FLAG_GROUPS:
        hit = [k.replace("flag_", "") for k in keys if f[k]]
        if hit:
            return {**f, "outcome": outcome, "outcome_reason": ", ".join(hit)}
    if f["flag_index_unavailable"]:
        return {**f, "outcome": OUTCOMES[4], "outcome_reason": index_status}
    return {**f, "outcome": OUTCOMES[5], "outcome_reason": ""}


PRE_CP3_OUTCOMES = ["optimizer failure", "non-physical", "boundary-limited", "weakly identified",
                    "usable fit, index temperature unavailable", "usable fit, index temperature calculated"]


def pre_cp3_outcome(flags) -> str:
    """The outcome precedence as pre-registered and presented at CP3 before the author's amendment (D-046 history), applied to the flags of
    classify(): a fitted LSE at 0 J counted as non-physical. Used only to reproduce the earlier CP3 counts; never for a current result."""
    if flags["flag_optimizer_failure"]:
        return PRE_CP3_OUTCOMES[0]
    if flags["flag_lse_at_lower_bound"] or flags["flag_nonphysical_no_rise"] or flags["flag_nonphysical_t0_at_absolute_zero"]:
        return PRE_CP3_OUTCOMES[1]
    if any(flags[k] for k in ["flag_boundary_c_min", "flag_boundary_c_max", "flag_boundary_t0_limit", "flag_boundary_rise_max",
                              "flag_boundary_lse_max"]):
        return PRE_CP3_OUTCOMES[2]
    if any(flags[k] for k in ["flag_weak_transition", "flag_weak_upper_shelf", "flag_weak_lower_shelf", "flag_numerically_singular"]):
        return PRE_CP3_OUTCOMES[3]
    return PRE_CP3_OUTCOMES[4] if flags["flag_index_unavailable"] else PRE_CP3_OUTCOMES[5]
