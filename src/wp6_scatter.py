"""WP6 - The specimen-scatter models C1, C2 and C3, their calibration and their diagnostics.

Every model is a ZERO-MEAN stochastic scatter model in the FULL-SIZE-EQUIVALENT energy frame, evaluated at the
TRUE transition coordinate x_true = (T_equiv_true - T0_true) / C_true (DECISIONS.md D-096). For a miniature
programme the simulator divides the drawn deviation by NF_E before adding it to the raw specimen energy, so that
multiplying by NF_E during the approved normalization recovers the intended full-size-equivalent distribution.

  C1  (CENTRAL, D-095)  sd = USE_true * s(region), s read from the WP4 empirical profile. Nothing is fitted.
  C1-robust             the same with the 1.4826 * MAD scale: the low-scatter sensitivity.
  C2                    sd(T) = sigma_T |dE/dT| + cv E(T) + 3 cv LSE, calibrated by the D-094 procedure.
  C3-centred            region-wise resampling of the leverage-adjusted residual / USE observations with that
                        region's empirical MEAN SUBTRACTED, so the model is zero-mean and comparable with C1/C2.
  C3-uncentered         the same WITHOUT centring: a labelled "empirical residual + model-shape / systematic
                        region-bias" sensitivity, NOT the main C3 scatter case (D-094).
  miniature-inflated    C1 with the WP4 MINIATURE profile (13 curves, 6 references; weakly supported).

The pool is EMPIRICAL PUBLISHED-DATA RESIDUAL SCATTER (D-061): specimen-to-specimen variation plus
between-laboratory, machine, calibration and reporting differences across 109 publications, digitization error
and tanh model-shape error. It is never called material scatter.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

from common import OUTPUTS
from wp3_fitter import tanh_energy

# ---------------------------------------------------------------------------
# 1. Regions (D-061, D-094): evaluated on the TRUE curve
# ---------------------------------------------------------------------------
REGIONS = ["lower shelf (x <= -1.5)", "lower transition (-1.5 < x <= -0.5)", "central transition (-0.5 < x < 0.5)",
           "upper transition (0.5 <= x < 1.5)", "upper shelf (x >= 1.5)"]
REGION_X_RANGE = [(-3.0, -1.5), (-1.5, -0.5), (-0.5, 0.5), (0.5, 1.5), (1.5, 3.0)]   # shelves truncated at |x| = 3
N_REGIONS = len(REGIONS)
RESIDUAL_QUANTITY = "leverage-adjusted residual / fitted USE"
WP4_POOL_CAVEAT = ("empirical published-data residual scatter (D-061): specimen-to-specimen variation plus "
                   "between-laboratory, machine, calibration and reporting differences, digitization error and "
                   "tanh model-shape error. NOT material scatter.")


def region_index(x) -> np.ndarray:
    """0..4 for the five WP4 regions, from x = (T - T0_true) / C_true.

    Boundary membership follows D-061 exactly: lower shelf x <= -1.5; lower transition -1.5 < x <= -0.5; central
    -0.5 < x < 0.5; upper transition 0.5 <= x < 1.5; upper shelf x >= 1.5. The two negative boundaries belong to
    the colder region and the two positive ones to the warmer region, so a single searchsorted cannot express it.
    """
    x = np.asarray(x, float)
    idx = np.full(x.shape, 2, dtype=np.int64)
    idx[x <= -1.5] = 0
    idx[(x > -1.5) & (x <= -0.5)] = 1
    idx[(x >= 0.5) & (x < 1.5)] = 3
    idx[x >= 1.5] = 4
    return idx


# ---------------------------------------------------------------------------
# 2. The WP4 empirical profile, read at full precision from the approved output
# ---------------------------------------------------------------------------
def wp4_profile(geometry_category: str = "full-size", curve_set: str = "usable") -> pd.DataFrame:
    """One row per region: the WP4 SD, robust scale, mean and count of the leverage-adjusted residual / USE."""
    path = OUTPUTS / "wp4" / "published_residual_scatter_summary.csv"
    t = pd.read_csv(path, float_precision="round_trip")
    t = t[(t["curve_set"].str.startswith(curve_set)) & (t["geometry_category"] == geometry_category)
          & (t["quantity"] == RESIDUAL_QUANTITY)]
    t = t.set_index("region").loc[REGIONS].reset_index()
    return t[["region", "residuals", "curves", "mean", "sd", "mad_scaled"]].copy()


def residual_pool(geometry_category: str = "full-size", cohort_curve_ids=None) -> dict:
    """The per-region pools of leverage-adjusted residual / USE observations behind C3 (usable WP3 fits).

    `cohort_curve_ids`, when given, restricts the pool to those curves (D-110 cohort propagation).
    Returns {'values': [array per region], 'means': array, 'sds': array, 'counts': array}.
    """
    path = OUTPUTS / "wp4" / "published_residual_scatter_dataset.csv"
    t = pd.read_csv(path, float_precision="round_trip")
    t = t[(t["geometry_category"] == geometry_category) & (t["wp3_fit_usable"].astype(str).str.lower() == "true")]
    if cohort_curve_ids is not None:
        t = t[t["curve_id"].astype(str).isin(set(map(str, cohort_curve_ids)))]
    col = "leverage_adjusted_residual_over_fitted_use"
    values, means, sds, counts = [], [], [], []
    for region in REGIONS:
        v = t.loc[t["region"] == region, col].to_numpy(float)
        v = v[np.isfinite(v)]
        values.append(v)
        means.append(float(v.mean()) if len(v) else np.nan)
        sds.append(float(v.std(ddof=1)) if len(v) > 1 else np.nan)
        counts.append(int(len(v)))
    return dict(values=values, means=np.array(means), sds=np.array(sds), counts=np.array(counts))


# ---------------------------------------------------------------------------
# 3. C2 calibration (D-094), declared before it was run
# ---------------------------------------------------------------------------
def c2_region_profile(sigma_t: float, cv: float, archetypes) -> np.ndarray:
    """Mean of sd(T)/USE over a 201-point uniform x-grid inside each region, averaged with equal weight over the
    archetypes. `archetypes` is a sequence of (use, c, lse)."""
    out = np.zeros(N_REGIONS, float)
    for r, (lo, hi) in enumerate(REGION_X_RANGE):
        x = np.linspace(lo, hi, 201)
        vals = []
        for use, c, lse in archetypes:
            e = lse + (use - lse) / 2.0 * (1.0 + np.tanh(x))
            slope = 0.5 * (use - lse) / c * (1.0 - np.tanh(x) ** 2)
            sd = sigma_t * slope + cv * e + 3.0 * cv * lse
            vals.append(np.mean(sd) / use)
        out[r] = float(np.mean(vals))
    return out


def calibrate_c2(archetypes, target: np.ndarray, counts: np.ndarray) -> dict:
    """(sigma_T, cv) by bounded least squares with weights sqrt(n_r / sum n), exactly as D-094 declares."""
    w = np.sqrt(np.asarray(counts, float) / float(np.sum(counts)))
    res = least_squares(lambda p: w * (c2_region_profile(p[0], p[1], archetypes) - np.asarray(target, float)),
                        x0=[5.0, 0.06], bounds=([0.0, 0.0], [100.0, 1.0]), xtol=1e-12, ftol=1e-12, gtol=1e-12)
    sigma_t, cv = float(res.x[0]), float(res.x[1])
    return dict(sigma_t_c=sigma_t, cv=cv, profile=c2_region_profile(sigma_t, cv, archetypes),
                optimizer_success=bool(res.success), cost=float(res.cost))


# ---------------------------------------------------------------------------
# 4. The scatter models
# ---------------------------------------------------------------------------
SCATTER_MODELS = ["C1", "C1-robust", "C2", "C3-centred", "C3-uncentered", "miniature-inflated"]
SCATTER_LABELS = {
    "C1": "C1 region-wise normal scaled by USE, WP4 SD scale (CENTRAL, D-095)",
    "C1-robust": "C1 with the 1.4826 * MAD robust scale (low-scatter sensitivity)",
    "C2": "C2 smooth form sd = sigma_T |dE/dT| + cv E + 3 cv LSE, calibrated to the WP4 profile",
    "C3-centred": "C3 region-wise resampling of the WP4 residual pool, region means SUBTRACTED (zero-mean)",
    "C3-uncentered": "empirical residual + model-shape / systematic-region-bias sensitivity (NOT the main C3)",
    "miniature-inflated": "C1 with the WP4 MINIATURE profile (13 curves, 6 references; weakly supported)",
}


class ScatterModel:
    """Draws zero-mean (or, for C3-uncentered, deliberately non-zero-mean) energy deviations in the
    FULL-SIZE-EQUIVALENT frame at the true transition coordinate."""

    def __init__(self, name: str, scale=None, pool=None, sigma_t=None, cv=None, label=None):
        self.name = name
        self.scale = None if scale is None else np.asarray(scale, float)   # sd / USE per region
        self.pool = pool                                                   # list of arrays, per region
        self.sigma_t = sigma_t
        self.cv = cv
        self.label = label or SCATTER_LABELS.get(name, name)

    def sd_fse(self, x_true, use_true, lse_true, c_true) -> np.ndarray:
        """The full-size-equivalent scatter magnitude (C1-type and C2 only); C3 draws directly."""
        x_true = np.asarray(x_true, float)
        if self.scale is not None:
            return self.scale[region_index(x_true)] * float(use_true)
        e = tanh_energy(x_true * float(c_true) + 0.0, float(lse_true), float(use_true), 0.0, float(c_true))
        slope = 0.5 * (float(use_true) - float(lse_true)) / float(c_true) * (1.0 - np.tanh(x_true) ** 2)
        return self.sigma_t * slope + self.cv * e + 3.0 * self.cv * float(lse_true)

    def draw_fse(self, x_true, use_true, lse_true, c_true, rng) -> np.ndarray:
        """Energy deviations in the full-size-equivalent frame, one per specimen."""
        x_true = np.asarray(x_true, float)
        if self.pool is not None:
            idx = region_index(x_true)
            out = np.empty(len(x_true), float)
            for r in range(N_REGIONS):
                sel = idx == r
                k = int(np.sum(sel))
                if k:
                    out[sel] = rng.choice(self.pool[r], size=k, replace=True)
            return out * float(use_true)
        return self.sd_fse(x_true, use_true, lse_true, c_true) * rng.standard_normal(len(x_true))


COHORTS = ("primary", "looser", "stricter")


def cohort_curves(cohort: str):
    """The usable full-size WP3 fits of a CP2-frozen cohort, with their measured points (D-110).

    No cohort is regenerated: the memberships come from the approved WP3 outputs, which carry the frozen CP2
    cohort flags. Returns (list of (t, e, fit_dict), n_curves).
    """
    from common import ROOT
    recs = pd.read_csv(ROOT / "data" / "processed" / "primary" / "charpy_records_with_curves.csv",
                       float_precision="round_trip")
    if cohort == "looser":
        fits = pd.read_csv(OUTPUTS / "wp3" / "fits_looser_cohort_curves.csv", float_precision="round_trip")
    else:
        fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv", float_precision="round_trip")
        if cohort == "stricter":
            fits = fits[fits["in_stricter"].astype(str).str.lower() == "true"]
    u = fits[(fits["geometry_category"] == "full-size")
             & (fits["outcome"] == "usable fit, index temperature calculated")]
    by = {k: v for k, v in recs.groupby("curve_id")}
    out = []
    for _, f in u.iterrows():
        r = by[f["curve_id"]]
        out.append((r["test_temp_c"].to_numpy(float), r["energy_j"].to_numpy(float), f.to_dict()))
    return out, list(u["curve_id"].astype(str))


_COHORT_PROFILE_CACHE: dict = {}


def cohort_profile(cohort: str) -> dict:
    """The D-061 residual profile re-aggregated for a cohort (D-110). For 'primary' this reproduces the WP4
    summary table exactly, which validation test 13 asserts."""
    if cohort not in _COHORT_PROFILE_CACHE:
        curves, ids = cohort_curves(cohort)
        prof = profile_from_curves(curves)
        prof["curve_ids"] = ids
        _COHORT_PROFILE_CACHE[cohort] = prof
    return _COHORT_PROFILE_CACHE[cohort]


def build_scatter_model(name: str, archetypes=None, cohort_curve_ids=None, cohort: str = "primary") -> ScatterModel:
    """Construct a model from the approved WP4 outputs. `archetypes` is needed only to calibrate C2."""
    if name == "zero":
        return ScatterModel("zero", scale=np.zeros(N_REGIONS), label="zero scatter (validation only)")
    if name in ("C1", "C1-robust"):
        if cohort != "primary":
            cp = cohort_profile(cohort)
            scale = cp["sds"] if name == "C1" else cp["mad_scaled"]
            return ScatterModel(name, scale=scale,
                                label=f"{SCATTER_LABELS[name]} - re-aggregated for the CP2-frozen {cohort} cohort")
        prof = wp4_profile("full-size")
        col = "sd" if name == "C1" else "mad_scaled"
        return ScatterModel(name, scale=prof[col].to_numpy(float))
    if name == "miniature-inflated":
        prof = wp4_profile("miniature")
        return ScatterModel(name, scale=prof["sd"].to_numpy(float))
    if name == "C2":
        prof = wp4_profile("full-size")
        cal = calibrate_c2(archetypes, prof["sd"].to_numpy(float), prof["residuals"].to_numpy(float))
        return ScatterModel(name, sigma_t=cal["sigma_t_c"], cv=cal["cv"])
    if name in ("C3-centred", "C3-uncentered"):
        if cohort != "primary" and cohort_curve_ids is None:
            cohort_curve_ids = cohort_profile(cohort)["curve_ids"]
        pool = residual_pool("full-size", cohort_curve_ids)
        vals = [v.copy() for v in pool["values"]]
        if name == "C3-centred":
            vals = [v - m for v, m in zip(vals, pool["means"])]
        return ScatterModel(name, pool=vals)
    raise ValueError(f"unknown scatter model {name!r}")


def profile_from_curves(curves) -> dict:
    """Re-aggregate the D-061 residual profile from scratch for a set of usable full-size curves (D-110).

    `curves` is a sequence of (t, e, fit_dict) for usable full-size WP3 fits. The definitions are the unchanged
    D-061 ones - leverage-adjusted (HC2) residual divided by the fitted USE, binned into the five regions on
    x = (T - T0_fit) / C_fit - and the leverage adjustment is the approved WP4 function, imported unchanged.
    Returns the same structure as residual_pool() plus the per-region SD, robust scale and counts.
    """
    from wp4_bootstrap import leverage_adjusted_residuals
    buckets = [[] for _ in range(N_REGIONS)]
    n_curves = np.zeros(N_REGIONS, dtype=int)
    for t, e, fit in curves:
        t = np.asarray(t, float)
        e = np.asarray(e, float)
        adj = leverage_adjusted_residuals(t, e, fit)["adjusted"] / float(fit["use_j"])
        idx = region_index((t - float(fit["t0_c"])) / float(fit["c_c"]))
        for r in range(N_REGIONS):
            sel = idx == r
            if np.any(sel):
                buckets[r].extend(adj[sel].tolist())
                n_curves[r] += 1
    values = [np.array(b, float) for b in buckets]
    mad = lambda v: 1.4826 * float(np.median(np.abs(v - np.median(v)))) if len(v) else np.nan
    return dict(values=values,
                means=np.array([float(v.mean()) if len(v) else np.nan for v in values]),
                sds=np.array([float(v.std(ddof=1)) if len(v) > 1 else np.nan for v in values]),
                mad_scaled=np.array([mad(v) for v in values]),
                counts=np.array([len(v) for v in values]),
                curves=n_curves)
