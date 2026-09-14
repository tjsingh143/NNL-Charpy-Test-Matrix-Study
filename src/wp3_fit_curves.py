"""WP3 - Apply the transition-curve fitter to the published Charpy data of the CP2-frozen cohorts.

Analysis of published test data. Reads the frozen cohorts (outputs/wp2*/cohort_membership.csv, checked against
data/FROZEN_COHORTS_CP2.csv before anything is fitted) and the records (data/processed/primary/charpy_records_with_curves.csv).
Every curve of the looser cohort (which contains the primary and stricter cohorts) is fitted once with the FINAL PRIMARY method: the
author's CP3 amendment of D-042 (LSE fixed at 2.7 J for full-size, fitted >= 0 J for miniature specimens), classified as amended in
D-046. Every primary curve gets one row with its estimates, bounds, starting values, solver status, diagnostics, flags, outcome and
index temperature. Nothing is removed. The primary cohort is also fitted with the pre-registered all-fitted method, kept as the explicit
sensitivity case; under the pre-CP3 classification it must reproduce the outcome counts presented at CP3. The dataset's own USE and DBTT
are read only after fitting, for comparison (D-049).

Outputs (outputs/wp3/): method_configuration.md, fits_primary.csv, fits_looser_cohort_curves.csv, fit_outcomes.csv,
fit_outcome_reasons.csv, fit_flags.csv, fit_outcomes_by_group.csv, index_availability_by_geometry.csv, index_position_on_fitted_rise.csv,
t41j_notch_metadata_sensitivity.csv, parameter_summary.csv, parameter_extremes.csv, lse_sensitivity_published.csv,
lse_sensitivity_published_summary.csv, lse_sensitivity_outcome_changes.csv, method_change_before_after.csv,
residual_pattern_by_lower_shelf_outcome.csv, dataset_value_comparison.csv, dataset_value_comparison_summary.csv,
cohort_sensitivity_outcomes.csv, fits_published_examples.png, fits_outcome_by_sampling.png, wp3_summary.md.
outputs/wp3/sensitivity_all_fitted_lse/: fits_primary.csv, fit_outcomes.csv, fit_outcomes_pre_cp3_classification.csv, fit_flags.csv,
residual_pattern_by_lower_shelf_outcome.csv (beside the synthetic tables written there by src/wp3_validation.py).

Run:  .venv/bin/python src/wp3_fit_curves.py      (after src/wp3_validation.py)
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

import wp3_fitter as F
import wp3_validation as V
from common import DATA, OUTPUTS, PROCESSED, PRIMARY_DATASET, SENSITIVITY_DATASET, md_table, write_text
from wp2_curves import verify_frozen_cohorts

OUT = OUTPUTS / "wp3"
SENSITIVITY_OUT = V.SENSITIVITY_OUT
DATA_TYPE = "published measurements (analysis of published test data)"
LSE_STRATEGY = F.PRIMARY_LSE_STRATEGY
SENSITIVITY_STRATEGY = F.SENSITIVITY_LSE_STRATEGY
GEOMETRY_CATEGORY = {"full-size (55x10x10 mm)": "full-size", "sub-size, standard length (55 mm, reduced thickness)": "sub-size (E23 type)",
                     "miniature (reduced length)": "miniature"}
# Primary-cohort outcome counts as presented at CP3 (commit 20481dd): all-fitted method, pre-CP3 classification. The sensitivity run must
# reproduce them, which shows that the sensitivity case is exactly the method presented then (D-042, D-051).
PRE_CP3_PRIMARY_OUTCOME_COUNTS = {"optimizer failure": 0, "non-physical": 71, "boundary-limited": 3, "weakly identified": 47,
                                  "usable fit, index temperature unavailable": 13, "usable fit, index temperature calculated": 36}


# ---------------------------------------------------------------------------
# 1. Frozen cohorts and records
# ---------------------------------------------------------------------------
def check_frozen_cohorts() -> pd.DataFrame:
    """Recompute every cohort fingerprint from the membership files and stop on any difference from the CP2 freeze (D-039)."""
    manifests = {}
    for key, folder in [(PRIMARY_DATASET, "wp2"), (SENSITIVITY_DATASET, f"wp2_sensitivity_{SENSITIVITY_DATASET}")]:
        mem = pd.read_csv(OUTPUTS / folder / "cohort_membership.csv")
        rows = []
        for cohort, g in mem.groupby("cohort", sort=False):
            lines = sorted(f"{cid}:{' '.join(sorted(r.split()))}" for cid, r in zip(g["curve_id"], g["record_ids"]))
            rows.append(dict(cohort=cohort, curves=len(g), records=int(g["n_points"].sum()),
                             membership_sha256=hashlib.sha256("\n".join(lines).encode()).hexdigest()))
        manifests[key] = pd.DataFrame(rows)
    verify_frozen_cohorts(manifests)
    return pd.read_csv(OUTPUTS / "wp2" / "cohort_membership.csv")


def load_curves(membership: pd.DataFrame) -> tuple:
    inv = pd.read_csv(OUTPUTS / "wp2" / "curve_inventory.csv", low_memory=False)
    rec = pd.read_csv(PROCESSED / "primary" / "charpy_records_with_curves.csv", low_memory=False)
    looser = membership[membership["cohort"] == "looser"]
    for cohort in ["primary", "stricter"]:
        if not set(membership.loc[membership["cohort"] == cohort, "curve_id"]) <= set(looser["curve_id"]):
            raise AssertionError(f"{cohort} cohort is not contained in the looser cohort")
    curves = inv.set_index("curve_id").loc[looser["curve_id"]].reset_index()
    for cohort in ["primary", "looser", "stricter"]:
        curves[f"in_{cohort}"] = curves["curve_id"].isin(membership.loc[membership["cohort"] == cohort, "curve_id"])
    return curves, rec


# ---------------------------------------------------------------------------
# 2. Fitting every curve
# ---------------------------------------------------------------------------
def geometry_description(category: str, geometry: str, notch_reported: bool) -> str:
    """D-044 (CP3 metadata caveat): a full-size curve whose records give no notch depth, angle or radius is described as a full-size
    V-notch specimen with exact notch dimensions unreported; it is not described as a confirmed standard notch."""
    if category == "full-size":
        return ("full-size 55x10x10 mm V-notch, notch dimensions reported" if notch_reported
                else "full-size 55x10x10 mm V-notch, exact notch dimensions unreported")
    return f"{category}: {geometry}"


def index_support(index_status: str, fraction: float) -> str:
    """Where a calculated index sits on the fitted rise (index-support diagnostic, D-044)."""
    if index_status != "calculated":
        return "no index calculated"
    if fraction < F.INDEX_RISE_FRACTION_LOW:
        return "41 J on the flat lower part of the fitted curve (below 11.9 % of the rise)"
    if fraction > F.INDEX_RISE_FRACTION_HIGH:
        return "41 J on the flat upper part of the fitted curve (above 88.1 % of the rise)"
    return "41 J inside the central 11.9-88.1 % of the fitted rise"


NUMERICAL_BOUND_FLAGS = ["flag_boundary_c_min", "flag_boundary_c_max", "flag_boundary_t0_limit", "flag_boundary_rise_max",
                         "flag_boundary_lse_max"]


def outcome_detail(outcome: str, flags: dict) -> str:
    """Which bound controls a boundary-limited outcome (D-046 as amended at CP3)."""
    if outcome != "boundary-limited":
        return ""
    lse, other = flags["flag_lse_at_lower_bound"], any(flags[k] for k in NUMERICAL_BOUND_FLAGS)
    if lse and other:
        return "fitted LSE at its 0 J bound, and a numerical-safety bound"
    return "fitted LSE at its 0 J bound (lower-shelf-bound-limited)" if lse else "numerical-safety bound"


def fit_all(curves: pd.DataFrame, rec: pd.DataFrame, strategy: str) -> pd.DataFrame:
    by_id = rec.set_index("record_id")
    rows = []
    for c in curves.itertuples(index=False):
        ids = c.record_ids.split()
        s = by_id.loc[ids].sort_values("source_row")
        if len(s) != c.n_points:
            raise AssertionError(f"curve {c.curve_id}: {len(s)} records found, {c.n_points} expected")
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        category = GEOMETRY_CATEGORY[c.geometry_class]
        lse_fixed = F.lse_setting(strategy, "full-size" if category == "full-size" else "miniature", t, e)
        fit = F.fit_curve(t, e, lse_fixed)
        criterion = F.CRITERION_J[category]
        t41, index_status = F.index_temperature(fit, t, criterion)
        fraction = F.index_fraction_of_rise(fit, criterion)
        cls = F.classify(fit, index_status, fraction)
        flags = {k: v for k, v in cls.items() if k.startswith("flag_")}
        rows.append(dict(data_type=DATA_TYPE, curve_id=c.curve_id, ref_id=c.ref_id, in_primary=c.in_primary, in_looser=c.in_looser,
                         in_stricter=c.in_stricter, material_family=c.material_family, product_form=c.product_form,
                         product_form_group=c.product_form_group, irradiated=bool(c.irradiated), geometry=c.geometry,
                         geometry_class=c.geometry_class, geometry_category=category, notch_reported=bool(c.notch_reported),
                         geometry_description=geometry_description(category, c.geometry, bool(c.notch_reported)),
                         flag_full_size_notch_dimensions_unreported=category == "full-size" and not bool(c.notch_reported),
                         reconstituted=bool(c.reconstituted), lse_strategy=strategy,
                         prefit_n_T_lower_band=F.prefit_lower_band_temperatures(t, e),
                         criterion_j=np.nan if criterion is None else criterion, index_temperature_c=t41, index_status=index_status,
                         index_fraction_of_rise=fraction, index_support=index_support(index_status, fraction),
                         # Audit only (added at the CP3 amendment, no rule attached; D-051): measured energies on each side of the criterion.
                         n_points_below_criterion=int(np.sum(e < criterion)) if criterion else np.nan,
                         n_points_above_criterion=int(np.sum(e > criterion)) if criterion else np.nan,
                         outcome=cls["outcome"], outcome_reason=cls["outcome_reason"], outcome_detail=outcome_detail(cls["outcome"], flags),
                         **flags,
                         **{k: v for k, v in fit.items() if k not in ("n_points",)},
                         n_points=c.n_points, n_temperatures=c.n_temperatures, T_min_c=c.T_min_c, T_max_c=c.T_max_c, T_span_c=c.T_span_c,
                         wp2_n_T_lower_band=c.n_T_lower_band, wp2_n_T_transition_band=c.n_T_transition_band,
                         wp2_n_T_upper_band=c.n_T_upper_band, wp2_energy_ratio=c.energy_ratio_min_to_screening_upper,
                         wp2_sampling_class=c.sampling_class, wp2_E_screening_upper_reference_j=c.E_screening_upper_reference_j,
                         record_ids=c.record_ids))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 3. Accounting tables
# ---------------------------------------------------------------------------
FIT_OUTCOME = {F.OUTCOMES[0]: "optimizer failure", F.OUTCOMES[1]: "non-physical (inadmissible)", F.OUTCOMES[2]: "boundary-limited",
               F.OUTCOMES[3]: "weakly identified", F.OUTCOMES[4]: "usable fit", F.OUTCOMES[5]: "usable fit"}
PRE_CP3_FIT_OUTCOME = {F.PRE_CP3_OUTCOMES[0]: "optimizer failure", F.PRE_CP3_OUTCOMES[1]: "non-physical", F.PRE_CP3_OUTCOMES[2]:
                       "boundary-limited", F.PRE_CP3_OUTCOMES[3]: "weakly identified", F.PRE_CP3_OUTCOMES[4]: "usable fit",
                       F.PRE_CP3_OUTCOMES[5]: "usable fit"}
FLAG_LABELS = {
    "flag_optimizer_failure": "optimizer failure (no start converged)",
    "flag_nonphysical_no_rise": "non-physical (inadmissible): no rise (USE = LSE)",
    "flag_nonphysical_t0_at_absolute_zero": "non-physical (inadmissible): T0 at absolute zero",
    "flag_lse_at_lower_bound": "boundary: fitted LSE at its 0 J lower bound (lower shelf not independently supported, or the symmetric "
                               "tanh compensating for a curve-shape mismatch; LSE fitted only)",
    "flag_boundary_c_min": "boundary: C at 1 °C (width unresolved)",
    "flag_boundary_c_max": "boundary: C at the tested span",
    "flag_boundary_t0_limit": "boundary: T0 at a range limit",
    "flag_boundary_rise_max": "boundary: USE - LSE at 10x highest energy",
    "flag_boundary_lse_max": "boundary: LSE at highest energy",
    "flag_weak_transition": "weak: < 2 test temperatures inside T0 ± C",
    "flag_weak_upper_shelf": "weak: upper shelf not supported (< 2 specimens at >= 95 % of rise)",
    "flag_weak_lower_shelf": "weak: lower shelf not supported (< 2 specimens at <= 5 % of rise; LSE fitted only)",
    "flag_numerically_singular": "ill-conditioned: Jacobian rank-deficient",
    "flag_nonflat_upper_shelf": "model adequacy (not an outcome): upper-shelf residual trend (p < 0.05)",
    "flag_index_unavailable": "index temperature not calculated (any reason)",
    "flag_index_near_fitted_shelf": "index support (not an outcome): T41J calculated, but 41 J outside the central 11.9-88.1 % of the "
                                    "fitted rise",
    "flag_full_size_notch_dimensions_unreported": "metadata (not a fit diagnostic): full-size V-notch, exact notch dimensions "
                                                  "unreported; T41J still calculated (D-044)",
}


def outcome_table(fits: pd.DataFrame, outcomes=F.OUTCOMES, column: str = "outcome", groups=FIT_OUTCOME) -> pd.DataFrame:
    counts = fits[column].value_counts().reindex(outcomes, fill_value=0)
    if int(counts.sum()) != len(fits):
        raise AssertionError("Mutually exclusive outcomes do not add up to the number of curves")
    t = pd.DataFrame({"outcome": counts.index, "curves": counts.values})
    t["fit_quality_group"] = t["outcome"].map(groups)
    for cat in ["full-size", "miniature"]:
        t[f"{cat}_curves"] = fits.loc[fits["geometry_category"] == cat, column].value_counts().reindex(outcomes, fill_value=0).values
    t["share"] = t["curves"] / len(fits)
    total = pd.DataFrame([{"outcome": "TOTAL", "curves": int(counts.sum()), "fit_quality_group": "",
                           "full-size_curves": int((fits["geometry_category"] == "full-size").sum()),
                           "miniature_curves": int((fits["geometry_category"] == "miniature").sum()), "share": 1.0}])
    return pd.concat([t, total], ignore_index=True)


def outcome_reasons(fits: pd.DataFrame) -> pd.DataFrame:
    """Mutually exclusive outcome, split by its recorded reason (sums to the number of curves)."""
    f = fits.assign(order=fits["outcome"].map({o: i for i, o in enumerate(F.OUTCOMES)}), reason=fits["outcome_reason"].fillna(""))
    t = (f.groupby(["order", "outcome", "outcome_detail", "reason"]).agg(
        curves=("curve_id", "size"), full_size_curves=("geometry_category", lambda v: int((v == "full-size").sum())),
        miniature_curves=("geometry_category", lambda v: int((v == "miniature").sum())))
         .reset_index().sort_values(["order", "curves", "reason"], ascending=[True, False, True]).drop(columns="order"))
    if int(t["curves"].sum()) != len(fits):
        raise AssertionError("Outcome reasons do not add up to the number of curves")
    return t.rename(columns={"reason": "outcome_reason"})


def flag_table(fits: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([dict(flag=k, meaning=v, curves=int(fits[k].sum()),
                              full_size_curves=int(fits.loc[fits["geometry_category"] == "full-size", k].sum()),
                              miniature_curves=int(fits.loc[fits["geometry_category"] == "miniature", k].sum()))
                         for k, v in FLAG_LABELS.items()])


def index_availability(fits: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for g, h in fits.groupby("geometry_description", sort=True):
        cat = h["geometry_category"].iloc[0]
        calc = h["index_status"] == "calculated"
        rows.append(dict(geometry_group=g, curves=len(h),
                         criterion="41 J" if cat == "full-size" else "none established",
                         basis=("10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044)" if cat == "full-size" else
                                "ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045)"),
                         index_calculated=int(calc.sum()),
                         index_calculated_and_fit_usable=int((h["outcome"] == F.OUTCOMES[5]).sum()),
                         index_calculated_with_index_support_warning=int((calc & h["flag_index_near_fitted_shelf"]).sum()),
                         not_calculated=int((~calc).sum()),
                         not_calculated_reasons="; ".join(f"{k} ({v})" for k, v in h.loc[~calc, "index_status"].value_counts().items())))
    return pd.DataFrame(rows)


def outcomes_by_group(fits: pd.DataFrame) -> pd.DataFrame:
    f = fits.assign(irradiation=np.where(fits["irradiated"], "irradiated", "unirradiated"),
                    n_points_bin=pd.cut(fits["n_points"], [0, 8, 11, 14, 19, 1000], labels=["6-8", "9-11", "12-14", "15-19", "20+"]),
                    wp2_transition_temperatures=pd.cut(fits["wp2_n_T_transition_band"], [0, 2, 3, 5, 100], labels=["2", "3", "4-5", "6+"]),
                    wp2_lower_band_temperatures=pd.cut(fits["wp2_n_T_lower_band"], [0, 1, 2, 100], labels=["1", "2", "3+"]),
                    wp2_upper_band_temperatures=pd.cut(fits["wp2_n_T_upper_band"], [0, 2, 3, 100], labels=["2", "3", "4+"]),
                    temperature_span=pd.cut(fits["T_span_c"], [0, 150, 250, 350, 1000], labels=["<=150 °C", "150-250 °C", "250-350 °C", ">350 °C"]))
    frames = []
    for dim in ["material_family", "product_form_group", "irradiation", "geometry_class", "n_points_bin", "wp2_transition_temperatures",
                "wp2_lower_band_temperatures", "wp2_upper_band_temperatures", "temperature_span"]:
        t = pd.crosstab(f[dim], f["outcome"]).reindex(columns=F.OUTCOMES, fill_value=0)
        t.insert(0, "curves", t.sum(axis=1))
        t["share_not_usable"] = (t[F.OUTCOMES[:4]].sum(axis=1) / t["curves"]).round(3)
        t = t.reset_index().rename(columns={dim: "group"})
        t.insert(0, "dimension", dim)
        frames.append(t)
    return pd.concat(frames, ignore_index=True)


def parameter_summary(fits: pd.DataFrame) -> tuple:
    usable = fits[fits["outcome"].isin(F.OUTCOMES[4:])]
    rows = []
    for cat, h in [("full-size", usable[usable["geometry_category"] == "full-size"]),
                   ("miniature", usable[usable["geometry_category"] == "miniature"])]:
        for col, label in [("lse_j", "LSE (J), fitted values only"), ("use_j", "USE (J)"), ("t0_c", "T0 (°C)"), ("c_c", "C (°C)"),
                           ("index_temperature_c", "T41J (°C)")]:
            v = (h.loc[h["lse_mode"] == "fitted", col] if col == "lse_j" else h[col]).dropna()
            if len(v) == 0:
                continue
            rows.append(dict(geometry_category=cat, parameter=label, curves=len(v), minimum=v.min(), p10=v.quantile(0.1),
                             median=v.median(), p90=v.quantile(0.9), maximum=v.max()))
    summary = pd.DataFrame(rows)
    extremes = []
    for col in ["use_j", "t0_c", "c_c", "index_temperature_c", "lse_j"]:
        v = fits[col] if col != "lse_j" else fits[col].where(fits["lse_mode"] == "fitted")
        for idx in [v.idxmin(), v.idxmax()] if v.notna().any() else []:
            r = fits.loc[idx]
            extremes.append(dict(parameter=col if col != "lse_j" else "lse_j (fitted values only)",
                                 which="minimum" if idx == v.idxmin() else "maximum", curve_id=r["curve_id"], value=r[col],
                                 outcome=r["outcome"], outcome_reason=r["outcome_reason"], material_family=r["material_family"],
                                 product_form=r["product_form"], irradiated=r["irradiated"], geometry=r["geometry"],
                                 n_points=r["n_points"], T_min_c=r["T_min_c"], T_max_c=r["T_max_c"]))
    return summary, pd.DataFrame(extremes)


# ---------------------------------------------------------------------------
# 4. Comparison with the dataset's own USE and DBTT (after fitting; diagnostic only, D-049)
# ---------------------------------------------------------------------------
def _q(v: pd.Series, q: float = 0.5) -> float:
    v = v.dropna()
    return float(v.quantile(q)) if len(v) else np.nan


def dataset_comparison(fits: pd.DataFrame, rec: pd.DataFrame) -> tuple:
    """The dataset's USE and DBTT have no documented definition (D-022). They are compared with our estimates only after the method
    was fixed and all fits made; nothing here feeds back into the fit."""
    p = fits[fits["in_primary"]].copy()
    per_curve = rec[rec["curve_id"].isin(p["curve_id"])].groupby("curve_id").agg(
        dataset_use_j=("use_j_dataset", "first"), dataset_dbtt_c=("dbtt_c_dataset", "first"),
        dataset_use_distinct_values=("use_j_dataset", lambda v: v.dropna().nunique()),
        dataset_dbtt_distinct_values=("dbtt_c_dataset", lambda v: v.dropna().nunique()))
    p = p.merge(per_curve, left_on="curve_id", right_index=True, how="left")
    p["use_ratio_ours_to_dataset"] = p["use_j"] / p["dataset_use_j"]
    p["t41_minus_dataset_dbtt_c"] = p["index_temperature_c"] - p["dataset_dbtt_c"]
    p["t0_minus_dataset_dbtt_c"] = p["t0_c"] - p["dataset_dbtt_c"]
    both = p["t41_minus_dataset_dbtt_c"].notna() & p["t0_minus_dataset_dbtt_c"].notna()
    p["dataset_dbtt_closer_to"] = np.where(~both, "",
                                           np.where(p["t41_minus_dataset_dbtt_c"].abs() <= p["t0_minus_dataset_dbtt_c"].abs(), "T41J", "T0"))
    p["dataset_use_below_41j"] = p["dataset_use_j"] < F.FULL_SIZE_CRITERION_J
    cols = ["curve_id", "ref_id", "geometry_category", "geometry", "outcome", "use_support", "use_j", "use_plateau_mean_j", "dataset_use_j",
            "use_ratio_ours_to_dataset", "t0_c", "index_temperature_c", "index_status", "dataset_dbtt_c", "t41_minus_dataset_dbtt_c",
            "t0_minus_dataset_dbtt_c", "dataset_dbtt_closer_to", "dataset_use_below_41j", "dataset_use_distinct_values",
            "dataset_dbtt_distinct_values"]
    table = p[cols]
    rows = []
    for (cat, usable), h in p.groupby(["geometry_category", p["outcome"].isin(F.OUTCOMES[4:])]):
        r = dict(geometry_category=cat, fit_usable=bool(usable), curves=len(h), with_dataset_use=int(h["dataset_use_j"].notna().sum()),
                 with_dataset_dbtt=int(h["dataset_dbtt_c"].notna().sum()),
                 use_ratio_median=_q(h["use_ratio_ours_to_dataset"]),
                 use_ratio_p10=_q(h["use_ratio_ours_to_dataset"], 0.1), use_ratio_p90=_q(h["use_ratio_ours_to_dataset"], 0.9),
                 share_use_within_10pct=float((h["use_ratio_ours_to_dataset"].sub(1).abs() <= 0.10).mean()),
                 t41_minus_dbtt_median_c=_q(h["t41_minus_dataset_dbtt_c"]),
                 t41_minus_dbtt_median_abs_c=_q(h["t41_minus_dataset_dbtt_c"].abs()),
                 share_t41_within_10c=(float((h["t41_minus_dataset_dbtt_c"].abs() <= 10).sum() / h["t41_minus_dataset_dbtt_c"].notna().sum())
                                      if h["t41_minus_dataset_dbtt_c"].notna().any() else np.nan),
                 t0_minus_dbtt_median_c=_q(h["t0_minus_dataset_dbtt_c"]),
                 t0_minus_dbtt_median_abs_c=_q(h["t0_minus_dataset_dbtt_c"].abs()),
                 share_t0_within_10c=float((h["t0_minus_dataset_dbtt_c"].abs() <= 10).sum() / max(h["t0_minus_dataset_dbtt_c"].notna().sum(), 1)),
                 dbtt_closer_to_t41j=int((h["dataset_dbtt_closer_to"] == "T41J").sum()),
                 dbtt_closer_to_t0=int((h["dataset_dbtt_closer_to"] == "T0").sum()),
                 dataset_use_below_41j=int(h["dataset_use_below_41j"].sum()))
        rows.append(r)
    return table, pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. Figures (published data)
# ---------------------------------------------------------------------------
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE = "#2a78d6", "#eb6834"
RAMP = {"usable": "#86b6ef", "weak": "#2a78d6", "failed": "#0d366b"}


def _style(ax):
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color("#c3c2b7")
    ax.tick_params(colors=INK2, labelsize=8)


def select_examples(fits: pd.DataFrame) -> list:
    """Illustration only; no number in any analysis depends on the choice. Rules fixed before looking at any fitted curve:
    success = usable full-size fit with an index temperature, 10-20 points, smallest RMSE relative to USE;
    weak = weakly identified primary curve with a weak transition if any (else any weak flag), most points.
    Then, each if any, most points: optimizer failure; non-physical (inadmissible); boundary-limited with the fitted LSE at its 0 J bound;
    boundary-limited by a numerical-safety bound only. (Re-specified at the CP3 amendment of D-046, before the amended fits were run, so
    that both kinds of boundary-limited fit are shown; D-051.)"""
    p = fits[fits["in_primary"]]
    out = []
    ok = p[(p["outcome"] == F.OUTCOMES[5]) & p["n_points"].between(10, 20)]
    if len(ok):
        out.append(("clearly successful fit", ok.assign(k=ok["rmse_j"] / ok["use_j"]).sort_values(["k", "curve_id"]).iloc[0]))
    weak = p[p["outcome"] == F.OUTCOMES[3]]
    if len(weak):
        pool = weak[weak["flag_weak_transition"]] if weak["flag_weak_transition"].any() else weak
        out.append(("converged but weakly identified", pool.sort_values(["n_points", "curve_id"], ascending=[False, True]).iloc[0]))
    boundary = p[p["outcome"] == F.OUTCOMES[2]]
    for title, pool in [(F.OUTCOMES[0], p[p["outcome"] == F.OUTCOMES[0]]), (F.OUTCOMES[1], p[p["outcome"] == F.OUTCOMES[1]]),
                        ("boundary-limited: fitted LSE at its 0 J bound", boundary[boundary["flag_lse_at_lower_bound"]]),
                        ("boundary-limited: numerical-safety bound", boundary[~boundary["flag_lse_at_lower_bound"]])]:
        if len(pool):
            out.append((title, pool.sort_values(["n_points", "curve_id"], ascending=[False, True]).iloc[0]))
    return out


def example_figure(fits: pd.DataFrame, rec: pd.DataFrame) -> list:
    import textwrap

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    examples = select_examples(fits)
    fig, axes = plt.subplots(1, len(examples), figsize=(4.1 * len(examples), 4.9), squeeze=False)
    for ax, (title, r) in zip(axes[0], examples):
        s = rec[rec["curve_id"] == r["curve_id"]]
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        grid_t = np.linspace(t.min() - 0.05 * np.ptp(t), t.max() + 0.05 * np.ptp(t), 400)
        _style(ax)
        if r["optimizer_success"]:
            lo, hi = r["t0_c"] - r["c_c"], r["t0_c"] + r["c_c"]
            ax.axvspan(max(lo, grid_t[0]), min(hi, grid_t[-1]), color="#f0efec", zorder=0, label="fitted T0 ± C (11.9-88.1 % of rise)")
            ax.plot(grid_t, F.tanh_energy(grid_t, r["lse_j"], r["use_j"], r["t0_c"], r["c_c"]), color=BLUE, lw=2, zorder=2,
                    label="tanh fit")
        ax.scatter(t, e, s=26, facecolor=INK, edgecolor="white", linewidth=0.6, zorder=3, label="published test data")
        if r["geometry_category"] == "full-size":
            ax.axhline(F.FULL_SIZE_CRITERION_J, color=MUTED, lw=0.8, zorder=1)
            ax.text(grid_t[0], F.FULL_SIZE_CRITERION_J, " 41 J", color=INK2, fontsize=7, va="bottom")
            if np.isfinite(r["index_temperature_c"]):
                ax.plot([r["index_temperature_c"]], [F.FULL_SIZE_CRITERION_J], marker="D", ms=6, color=ORANGE, mec="white", zorder=4,
                        label="T41J (index temperature)", ls="none")
        ax.set_xlabel("Test temperature (°C)", fontsize=8.5, color=INK)
        ax.set_ylabel("Absorbed energy (J)", fontsize=8.5, color=INK)
        ax.set_title(f"{title}\ncurve {r['curve_id']}: {r['material_family']} {r['product_form']}, {r['geometry']}, {r['n_points']} points",
                     fontsize=8.5, color=INK)
        reason = r["outcome_reason"] if isinstance(r["outcome_reason"], str) and r["outcome_reason"] else ""
        lines = [f"outcome: {r['outcome']}" + (f" ({reason})" if reason else "")]
        if r["optimizer_success"]:
            if r["lse_mode"] == "fixed":
                lse_txt = f"LSE fixed at {r['lse_j']:.3g} J (full-size convention)"
            elif r["flag_lse_at_lower_bound"]:
                lse_txt = "LSE 0 J (fitted, at its 0 J lower bound)"
            else:
                lse_txt = f"LSE {r['lse_j']:.3g} J (fitted)"
            lines += [f"{lse_txt}; USE {r['use_j']:.3g} J ({r['use_support']})",
                      f"T0 {r['t0_c']:.0f} °C; C {r['c_c']:.0f} °C; test temperatures inside T0 ± C: {r['n_T_transition_fit']}",
                      f"index: {r['index_status']}"]
        ax.text(0.0, -0.2, "\n".join(textwrap.fill(x, 72) for x in lines), transform=ax.transAxes, fontsize=6.8, va="top", color=INK2)
    handles, labels = {}, {}
    for ax in axes[0]:
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), loc="upper center", ncol=4, fontsize=7.5, frameon=False,
               bbox_to_anchor=(0.5, 0.955))
    fig.suptitle("WP3 transition-curve fits to published Charpy V-notch data (examples; final method: full-size LSE fixed at 2.7 J, "
                 "miniature LSE fitted)", fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0.02, 1, 0.9))
    fig.subplots_adjust(bottom=0.3)
    fig.savefig(OUT / "fits_published_examples.png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    return [(title, r["curve_id"]) for title, r in examples]


def sampling_figure(fits: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    p = fits[fits["in_primary"]].copy()
    p["group"] = np.where(p["outcome"].isin(F.OUTCOMES[4:]), "usable",
                          np.where(p["outcome"] == F.OUTCOMES[3], "weak", "failed"))
    dims = [("wp2_n_T_transition_band", "WP2 transition-band temperatures", [0, 2, 3, 5, 100], ["2", "3", "4-5", "6+"]),
            ("wp2_n_T_upper_band", "WP2 upper-band temperatures", [0, 2, 3, 100], ["2", "3", "4+"]),
            ("wp2_n_T_lower_band", "WP2 lower-band temperatures", [0, 1, 2, 100], ["1", "2", "3+"])]
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6))
    labels = {"usable": "usable fit", "weak": "weakly identified", "failed": "optimizer failure, non-physical or boundary-limited"}
    for ax, (col, title, bins, names) in zip(axes, dims):
        p["bin"] = pd.cut(p[col], bins, labels=names)
        tab = pd.crosstab(p["bin"], p["group"]).reindex(index=names, columns=["usable", "weak", "failed"], fill_value=0)
        share = tab.div(tab.sum(axis=1), axis=0)
        left = np.zeros(len(tab))
        _style(ax)
        ax.grid(False)
        for grp in ["usable", "weak", "failed"]:
            ax.barh(range(len(tab)), share[grp], left=left, color=RAMP[grp], edgecolor="white", linewidth=1.5, height=0.62, label=labels[grp])
            left += share[grp].to_numpy()
        ax.set_yticks(range(len(tab)))
        ax.set_yticklabels([f"{n}  (n={int(tab.loc[n].sum())})" for n in names], fontsize=8)
        ax.set_xlim(0, 1)
        ax.set_xlabel("Share of primary-cohort curves", fontsize=8.5, color=INK)
        ax.set_title(title, fontsize=9, color=INK)
    handles, lab = axes[0].get_legend_handles_labels()
    fig.legend(handles, lab, loc="upper center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.99))
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT / "fits_outcome_by_sampling.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5b. Characterizing curve shape and index position (describe, change nothing)
# ---------------------------------------------------------------------------
def residual_pattern(primary: pd.DataFrame, rec: pd.DataFrame) -> pd.DataFrame:
    """Mean residual (measured - fitted, as % of fitted USE) in four regions of the fitted curve, by geometry and lower-shelf treatment.
    A symmetric tanh that cannot follow the measured shape leaves systematic residuals of opposite sign. Added after the pre-CP3 fits
    existed, to characterize the fitted LSE at 0 J (D-051); regenerated for both methods at the CP3 amendment."""
    by_id = rec.set_index("record_id")
    regions = {"x <= -1.5 (fitted lower shelf)": lambda x: x <= -1.5,
               "-1.5 < x <= -0.5 (lower transition)": lambda x: (x > -1.5) & (x <= -0.5),
               "-0.5 < x < 0.5 (middle)": lambda x: (x > -0.5) & (x < 0.5),
               "0.5 <= x < 1.5 (upper transition)": lambda x: (x >= 0.5) & (x < 1.5)}
    rows = []
    for r in primary[primary["optimizer_success"]].itertuples(index=False):
        s = by_id.loc[r.record_ids.split()]
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        x = (t - r.t0_c) / r.c_c
        res = 100.0 * (e - F.tanh_energy(t, r.lse_j, r.use_j, r.t0_c, r.c_c)) / r.use_j
        treatment = (f"LSE fixed at {r.lse_j:g} J" if r.lse_mode == "fixed" else
                     "LSE fitted, at its 0 J bound" if r.flag_lse_at_lower_bound else "LSE fitted, above 0 J")
        row = dict(curve_id=r.curve_id, geometry_category=r.geometry_category, lower_shelf_treatment=treatment, c_c=r.c_c)
        for name, in_region in regions.items():
            m = in_region(x)
            row[name] = res[m].mean() if m.any() else np.nan
        rows.append(row)
    d = pd.DataFrame(rows)
    g = d.groupby(["geometry_category", "lower_shelf_treatment"])
    out = g.size().rename("curves").to_frame()
    for name in regions:
        out[f"mean residual, {name}, % of USE"] = g[name].mean()
        out[f"curves with points, {name}"] = g[name].count()
    out["median C (°C)"] = g["c_c"].median()
    return out.reset_index()


INDEX_POSITION_BINS = [-np.inf, F.INDEX_RISE_FRACTION_LOW, F.INDEX_RISE_FRACTION_HIGH, np.inf]
INDEX_POSITION_LABELS = ["below 11.9 % (flat lower part of the fit)", "11.9-88.1 % (inside T0 ± C)", "above 88.1 % (flat upper part)"]


def index_position(primary: pd.DataFrame) -> pd.DataFrame:
    """Where 41 J lies on the fitted rise for full-size curves with a calculated index (index-support diagnostic, D-044). The bins match
    flag_index_near_fitted_shelf: a value exactly on a limit counts as inside."""
    f = primary[(primary["geometry_category"] == "full-size") & (primary["index_status"] == "calculated")].copy()
    frac = f["index_fraction_of_rise"]
    f["position"] = np.where(frac < F.INDEX_RISE_FRACTION_LOW, INDEX_POSITION_LABELS[0],
                             np.where(frac > F.INDEX_RISE_FRACTION_HIGH, INDEX_POSITION_LABELS[2], INDEX_POSITION_LABELS[1]))
    t = pd.crosstab(f["position"], f["outcome"]).reindex(index=INDEX_POSITION_LABELS, columns=F.OUTCOMES, fill_value=0)
    t = t.loc[:, t.sum() > 0]
    t.insert(0, "curves", t.sum(axis=1))
    t.insert(1, "notch dimensions unreported", f[~f["notch_reported"]].groupby("position").size().reindex(INDEX_POSITION_LABELS, fill_value=0))
    t.index.name = "41 J position on the fitted rise"
    return t.reset_index()


def notch_metadata_sensitivity(primary: pd.DataFrame, rec: pd.DataFrame) -> tuple:
    """D-044 metadata caveat: T41J-based counts with and without the full-size curves whose exact notch dimensions are unreported. A
    diagnostic only: the primary cohort and the primary T41J results keep those curves."""
    fs = primary[primary["geometry_category"] == "full-size"]
    cases = [("primary: all full-size curves", fs),
             ("sensitivity: excluding curves with exact notch dimensions unreported", fs[fs["notch_reported"]]),
             ("the excluded curves: full-size V-notch, exact notch dimensions unreported", fs[~fs["notch_reported"]])]
    rows = []
    for label, h in cases:
        calc = h["index_status"] == "calculated"
        usable = h["outcome"] == F.OUTCOMES[5]
        rows.append({"case": label, "full-size curves": len(h), "records": int(h["n_points"].sum()), "T41J calculated": int(calc.sum()),
                     "T41J with a usable fit": int(usable.sum()),
                     "T41J with a usable fit and no index-support warning": int((usable & ~h["flag_index_near_fitted_shelf"]).sum()),
                     "T41J with an index-support warning": int((calc & h["flag_index_near_fitted_shelf"]).sum()),
                     "T41J in a weakly identified or boundary-limited fit": int((calc & h["outcome"].isin(F.OUTCOMES[1:4])).sum()),
                     "stricter-cohort curves with a usable-fit T41J": int((usable & h["in_stricter"]).sum()),
                     "irradiated curves with a usable-fit T41J": int((usable & h["irradiated"]).sum()),
                     "median T41J, usable fits (°C)": _q(h.loc[usable, "index_temperature_c"])})
    # What the records of the full-size curves say about their notches (reported as found; nothing is filled in).
    curve_of = {rid: cid for cid, rids in zip(fs["curve_id"], fs["record_ids"]) for rid in rids.split()}
    r = rec[rec["record_id"].isin(curve_of)].copy()
    if len(r) != int(fs["n_points"].sum()):
        raise AssertionError("record lookup for the notch description failed")
    r["cohort_curve"] = r["record_id"].map(curve_of)
    r["curve_notch_reported"] = r["cohort_curve"].map(fs.set_index("curve_id")["notch_reported"])
    notch = (r.groupby(["curve_notch_reported", "notch_shape", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm"], dropna=False)
             .agg(records=("record_id", "size"), curves=("cohort_curve", "nunique")).reset_index())
    return pd.DataFrame(rows), notch


# ---------------------------------------------------------------------------
# 5c. Lower-shelf sensitivity on published data: final primary method versus the pre-registered all-fitted method (CP3 amendment)
# ---------------------------------------------------------------------------
def lse_sensitivity(final: pd.DataFrame, alt: pd.DataFrame) -> tuple:
    """Per primary curve, the final method (A) against the all-fitted sensitivity case (B): differences in T41J, T0 and USE, and whether
    the outcome and index availability change. A sensitivity comparison, not a method selection: part of any outcome change is mechanical,
    because a fixed lower shelf cannot trigger the lower-shelf diagnostics."""
    keep = ["curve_id", "lse_mode", "lse_j", "use_j", "t0_c", "c_c", "index_temperature_c", "index_status", "index_support", "outcome",
            "outcome_reason", "outcome_detail", "flag_lse_at_lower_bound", "flag_weak_lower_shelf", "flag_index_near_fitted_shelf"]
    d = final[["curve_id", "geometry_category", "notch_reported"] + keep[1:]].merge(alt[keep], on="curve_id", suffixes=("_final", "_all_fitted"),
                                                                                    validate="one_to_one")
    if len(d) != len(final):
        raise AssertionError("the sensitivity fits do not cover every primary curve")
    d.insert(0, "data_type", DATA_TYPE)
    d["t41_difference_all_fitted_minus_final_c"] = d["index_temperature_c_all_fitted"] - d["index_temperature_c_final"]
    d["t0_difference_all_fitted_minus_final_c"] = d["t0_c_all_fitted"] - d["t0_c_final"]
    d["use_difference_all_fitted_minus_final_j"] = d["use_j_all_fitted"] - d["use_j_final"]
    d["use_ratio_all_fitted_to_final_minus_1"] = d["use_j_all_fitted"] / d["use_j_final"] - 1.0
    d["c_ratio_all_fitted_to_final_minus_1"] = d["c_c_all_fitted"] / d["c_c_final"] - 1.0
    d["outcome_changed"] = d["outcome_final"] != d["outcome_all_fitted"]
    d["index_available_final"] = d["index_status_final"] == "calculated"
    d["index_available_all_fitted"] = d["index_status_all_fitted"] == "calculated"
    d["index_availability_changed"] = d["index_available_final"] != d["index_available_all_fitted"]
    summary = []
    for cat, h in d.groupby("geometry_category"):
        for col, label in [("t41_difference_all_fitted_minus_final_c", "T41J (all fitted - final), °C"),
                           ("t0_difference_all_fitted_minus_final_c", "T0 (all fitted - final), °C"),
                           ("use_difference_all_fitted_minus_final_j", "USE (all fitted - final), J"),
                           ("use_ratio_all_fitted_to_final_minus_1", "USE (all fitted / final - 1)"),
                           ("c_ratio_all_fitted_to_final_minus_1", "C (all fitted / final - 1)")]:
            v = h[col].dropna()
            if len(v):
                worst = h.loc[v.abs().idxmax()] if v.abs().max() > 0 else None
                summary.append(dict(geometry_category=cat, quantity=label, curves_compared=len(v), median=v.median(),
                                    median_abs=v.abs().median(), p90_abs=v.abs().quantile(0.9), max_abs=v.abs().max(),
                                    curve_with_max_abs="" if worst is None else worst["curve_id"],
                                    all_fitted_lse_of_that_curve_j=np.nan if worst is None else worst["lse_j_all_fitted"]))
    changes = []
    for cat, h in d.groupby("geometry_category"):
        changes.append({"geometry_category": cat, "change": "curves compared", "curves": len(h)})
        changes.append({"geometry_category": cat, "change": "outcome category differs", "curves": int(h["outcome_changed"].sum())})
        for (a, b), n in h[h["outcome_changed"]].groupby(["outcome_final", "outcome_all_fitted"]).size().items():
            changes.append({"geometry_category": cat, "change": f"outcome: final '{a}' / all fitted '{b}'", "curves": int(n)})
        changes.append({"geometry_category": cat, "change": "index availability differs", "curves": int(h["index_availability_changed"].sum())})
        for (a, b), n in h[h["index_availability_changed"]].groupby(["index_status_final", "index_status_all_fitted"]).size().items():
            changes.append({"geometry_category": cat, "change": f"index: final '{a}' / all fitted '{b}'", "curves": int(n)})
        changes.append({"geometry_category": cat, "change": "index-support warning differs (both calculated)",
                        "curves": int((h["index_available_final"] & h["index_available_all_fitted"] &
                                       (h["flag_index_near_fitted_shelf_final"] != h["flag_index_near_fitted_shelf_all_fitted"])).sum())})
    return d, pd.DataFrame(summary), pd.DataFrame(changes)


def method_change_table(final: pd.DataFrame, alt: pd.DataFrame) -> pd.DataFrame:
    """Before / after at CP3: the counts presented at CP3 (all-fitted method, pre-CP3 classification), the same fits under the amended
    classification (the terminology change alone), and the final primary method (amended lower shelf and classification)."""
    columns = [("previous CP3 presentation (all fitted; pre-CP3 classification)", alt, "outcome_pre_cp3_classification", F.PRE_CP3_OUTCOMES),
               ("all fitted; amended classification (terminology change only)", alt, "outcome", F.OUTCOMES),
               ("FINAL PRIMARY (geometry-specific lower shelf; amended classification)", final, "outcome", F.OUTCOMES)]
    rows = {}

    def put(label, values):
        rows[label] = values

    put("lower-shelf strategy", [F.LSE_STRATEGY_LABELS[SENSITIVITY_STRATEGY], F.LSE_STRATEGY_LABELS[SENSITIVITY_STRATEGY],
                                 F.LSE_STRATEGY_LABELS[LSE_STRATEGY]])
    for i, name in enumerate(["optimizer failure", "non-physical", "boundary-limited", "weakly identified",
                              "usable fit, index temperature unavailable", "usable fit, index temperature calculated"]):
        put(name, [int((f[col] == outs[i]).sum()) for _, f, col, outs in columns])
        if i == 2:
            put("  boundary-limited: fitted LSE at its 0 J bound (alone or with another bound)",
                ["counted as non-physical"] + [int(((f["outcome"] == F.OUTCOMES[2]) & f["flag_lse_at_lower_bound"]).sum())
                                               for _, f, _c, _o in columns[1:]])
            put("  boundary-limited: numerical-safety bound only",
                [int(((f[col] == outs[2])).sum()) if col == "outcome_pre_cp3_classification" else
                 int(((f["outcome"] == F.OUTCOMES[2]) & ~f["flag_lse_at_lower_bound"]).sum()) for _, f, col, outs in columns])
    put("usable fits (both usable categories)", [int(f[col].isin(outs[4:]).sum()) for _, f, col, outs in columns])
    put("TOTAL curves", [len(f) for _, f, _c, _o in columns])
    put("full-size curves with T41J calculated (of 134)", [int(((f["geometry_category"] == "full-size") & (f["index_status"] == "calculated")).sum())
                                                         for _, f, _c, _o in columns])
    put("full-size T41J with a usable fit", [int(((f["geometry_category"] == "full-size") & (f[col] == outs[5])).sum())
                                             for _, f, col, outs in columns])
    put("T41J with the index-support warning (41 J outside 11.9-88.1 % of the fitted rise)",
        [int(f["flag_index_near_fitted_shelf"].sum()) for _, f, _c, _o in columns])
    put("flag: fitted LSE at its 0 J bound (overlapping)", [int(f["flag_lse_at_lower_bound"].sum()) for _, f, _c, _o in columns])
    put("flag: weak lower shelf (overlapping)", [int(f["flag_weak_lower_shelf"].sum()) for _, f, _c, _o in columns])
    put("miniature curves with a usable fit (of 36)", [int(((f["geometry_category"] == "miniature") & f[col].isin(outs[4:])).sum())
                                                       for _, f, col, outs in columns])
    t = pd.DataFrame(rows, index=[c[0] for c in columns]).T.reset_index().rename(columns={"index": "quantity"})
    return t


# ---------------------------------------------------------------------------
# 6. Method configuration (generated from the constants actually used)
# ---------------------------------------------------------------------------
def method_configuration() -> str:
    L = ["# WP3 method configuration (generated from src/wp3_fitter.py and src/wp3_validation.py)", "",
         "| item | setting | decision |", "| --- | --- | --- |",
         "| model | E(T) = LSE + (USE - LSE)/2 [1 + tanh((T - T0)/C)]; solver parameters (LSE, USE - LSE, T0, C); a symmetric, empirical form that does not describe every measured transition | D-040 |",
         f"| lower shelf, FINAL PRIMARY | `{LSE_STRATEGY}`: full-size 55x10x10 mm LSE fixed at {F.FIXED_LSE_CONVENTION_J['full-size']:g} J (Sokolov & Nanstad 1995 p. 7); miniature LSE fitted, >= 0 J (no fixed miniature value). CP3 amendment by the author, not the pre-registered rule's outcome | D-042 |",
         f"| lower shelf, sensitivity case | `{SENSITIVITY_STRATEGY}`: LSE fitted (>= 0 J) for every geometry; the pre-registered rule's outcome, presented at CP3 | D-042 |",
         "| upper shelf | fitted asymptote LSE + (USE - LSE); supported if >= 2 specimens where the fit is >= 95.3 % of the rise (x >= 1.5); residual trend test (p < 0.05) reported as a model-adequacy flag outside the outcome | D-043 |",
         f"| index temperature, full-size 55x10x10 mm V-notch | T at {F.FULL_SIZE_CRITERION_J:g} J, analytic; only if LSE < 41 J < USE and inside the tested range; also for full-size V-notch curves whose exact notch dimensions are unreported (flagged) | D-044 |",
         "| index support (not an outcome) | calculated T41J with 41 J outside the central 11.9-88.1 % of the fitted rise (x = -1...+1): flag_index_near_fitted_shelf; the value is kept | D-044 |",
         "| index temperature, miniature / E23 sub-size | not calculated (no defensible criterion) | D-045 |",
         f"| optimizer | scipy.optimize.least_squares, method trf, analytic Jacobian, scaled parameters, ftol = xtol = gtol = {F.TOLERANCE:g}, max_nfev = {F.MAX_NFEV} per start | D-041 |",
         "| weighting | ordinary (unweighted) least squares on energy | D-041 |",
         "| starts (6, deterministic) | LSE = lowest energy (fitted LSE only); USE = mean of 3 highest; T0 in {midpoint crossing, lower quartile, upper quartile of distinct temperatures}; C in {span/12, span/4} | D-041 |",
         f"| bounds | LSE [0, highest energy] (fitted LSE only); USE - LSE [0, {F.RISE_MAX_FACTOR:g} x highest energy]; T0 [max(-273.15, T_min - span), T_max + span]; C [{F.C_MIN_C:g} °C, span]; on a bound = active or within {100 * F.NEAR_BOUND_FRACTION:g} % of the interval | D-041 |",
         f"| weak transition | < {F.MIN_TRANSITION_TEMPERATURES} distinct temperatures with -1 < x < 1 | D-047 |",
         f"| weak shelves | < {F.MIN_SHELF_POINTS} specimens with x >= {F.X_SHELF:g} (upper) or x <= -{F.X_SHELF:g} (lower, fitted LSE only) | D-047 |",
         "| numerically singular | Jacobian rank < number of parameters (NumPy default tolerance) | D-047 |",
         "| outcome precedence | " + " > ".join(F.OUTCOMES) + " | D-046 |",
         "| outcome groups (CP3 amendment) | non-physical (inadmissible) = no rise or T0 at absolute zero; boundary-limited = fitted LSE at its 0 J bound or a numerical-safety bound; weakly identified = weak transition, weak upper shelf, weak lower shelf (fitted LSE), rank-deficient Jacobian | D-046 |",
         f"| synthetic validation | seed {V.SEED}; {V.REPLICATES} replicates per scenario with scatter; scatter levels (sigma_T, cv): "
         + "; ".join(f"{k} ({a:g} °C, {b:g})" for k, (a, b) in V.NOISE.items()) + "; Blocks A-E run with the final method and with the all-fitted sensitivity method | D-048 |",
         f"| reference scales (summaries only) | {V.REF_TEMPERATURE_C:g} °C for T41J and T0; {100 * V.REF_USE_REL:g} % for USE; {100 * V.REF_C_REL:g} % for C | D-048 |"]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 7. Summary document (every number below is read from a generated table)
# ---------------------------------------------------------------------------
def _pct(x) -> str:
    return "" if pd.isna(x) else f"{100 * x:.0f} %"


def _num(v):
    return v.map(lambda x: "–" if pd.isna(x) else f"{x:.1f}")


def _pcts(v):
    return v.map(lambda x: "–" if pd.isna(x) else f"{100 * x:.0f} %")


def trust_classes(limits: pd.DataFrame) -> dict:
    fail_all = limits[~limits["all_fits_within_reference_p90"]]
    return {"within reference (all fits)": limits[limits["all_fits_within_reference_p90"]],
            "within reference only after the flags": fail_all[fail_all["usable_fits_within_reference_p90"]],
            "method declines (< 5 % usable)": fail_all[~fail_all["usable_fits_within_reference_p90"] & (fail_all["share_usable"] < 0.05)],
            "usable fits still miss a reference scale": fail_all[~fail_all["usable_fits_within_reference_p90"] & (fail_all["share_usable"] >= 0.05)]}


def synthetic_sections() -> list:
    design = pd.read_csv(OUT / "synthetic_validation_design.csv")
    metrics = pd.read_csv(OUT / "synthetic_validation_metrics.csv")
    lse = pd.read_csv(OUT / "synthetic_lse_strategy_comparison.csv")
    per = pd.read_csv(OUT / "synthetic_lse_strategy_per_dataset.csv")
    checks = pd.read_csv(OUT / "synthetic_flag_check.csv")
    limits = pd.read_csv(OUT / "synthetic_trust_limits.csv")
    shelf = pd.read_csv(OUT / "synthetic_nonflat_upper_shelf_check.csv")
    block_l = pd.read_csv(OUT / "synthetic_final_method_block_l.csv")
    s_checks = pd.read_csv(SENSITIVITY_OUT / "synthetic_flag_check.csv")
    s_limits = pd.read_csv(SENSITIVITY_OUT / "synthetic_trust_limits.csv")
    usable_cols = [f"share_{o}" for o in F.OUTCOMES[4:]]
    metrics["share_usable"] = metrics[usable_cols].sum(axis=1)
    final_ae = metrics[(metrics["block"] != "L") & (metrics["lse_strategy"] == LSE_STRATEGY)]

    def block(b, noise=None):
        m = final_ae[final_ae["block"] == b]
        return m if noise is None else m[m["noise"] == noise]

    def table(m):
        t = pd.DataFrame({"design": m["design"], "scatter": m["noise"], "fits": m["replicates"],
                          "T41J P90 |err| °C": m["all_t41_analytic_p90_abs"].round(1), "T0 P90 |err| °C": m["all_t0_p90_abs"].round(1),
                          "USE P90 |err|": m["all_use_rel_p90_abs"].map(_pct), "C P90 |err|": m["all_c_rel_p90_abs"].map(_pct),
                          "usable": m["share_usable"].map(_pct),
                          "T41J P90 usable fits °C": m["usable_t41_p90_abs"].round(1), "USE P90 usable fits": m["usable_use_rel_p90_abs"].map(_pct)})
        return md_table(t)

    def only_table(c):
        only = c[c["kind"] == "only this flag"]
        return md_table(pd.DataFrame({"fits carrying": only["group"].str.replace("flag_", ""), "fits": only["fits"],
                                      "T0 P90 |err| °C": only["t0_p90_abs"].round(1), "T41J P90 |err| °C": only["t41_analytic_p90_abs"].round(1),
                                      "USE P90 |err|": only["use_rel_p90_abs"].map(_pct), "C P90 |err|": only["c_rel_p90_abs"].map(_pct)}))

    outcome_rows = checks[checks["kind"].isin(["outcome", "outcome group"])]
    outcome_t = pd.DataFrame({"outcome": outcome_rows["group"], "fits": outcome_rows["fits"], "share": outcome_rows["share_of_fits"].map(_pct),
                              "T0 P90 |err| °C": outcome_rows["t0_p90_abs"].round(1),
                              "T41J P90 |err| °C": outcome_rows["t41_analytic_p90_abs"].round(1),
                              "USE P90 |err|": outcome_rows["use_rel_p90_abs"].map(_pct)})
    index_rows = checks[checks["kind"] == "index support"]
    index_t = pd.DataFrame({"usable fits with a calculated T41J": index_rows["group"], "fits": index_rows["fits"],
                            "T41J median |err| °C": index_rows["t41_analytic_median_abs"].round(1),
                            "T41J P90 |err| °C": index_rows["t41_analytic_p90_abs"].round(1),
                            "share beyond 10 °C": index_rows["t41_analytic_share_beyond_reference"].map(_pct)})
    audit = checks[checks["kind"].str.startswith("audit")]
    audit_t = pd.DataFrame({"audit diagnostic": audit["group"], "fits": audit["fits"], "T0 P90 |err| °C": audit["t0_p90_abs"].round(1),
                            "T41J P90 |err| °C": audit["t41_analytic_p90_abs"].round(1)})
    classes, s_classes = trust_classes(limits), trust_classes(s_limits)

    def listing(frame, t41=True):
        t = frame.assign(scenario=frame["design"] + " [" + frame["noise"] + "]")
        cols = {"scenario (design, [scatter])": t["scenario"], "usable": t["share_usable"].map(_pct)}
        if t41:
            cols["T41J P90 all / usable °C"] = _num(t["all_t41_analytic_p90_abs"]) + " / " + _num(t["usable_t41_p90_abs"])
        cols["T0 P90 all / usable °C"] = _num(t["all_t0_p90_abs"]) + " / " + _num(t["usable_t0_p90_abs"])
        cols["USE P90 all / usable"] = _pcts(t["all_use_rel_p90_abs"]) + " / " + _pcts(t["usable_use_rel_p90_abs"])
        return md_table(pd.DataFrame(cols))

    rule_md = (OUT / "synthetic_lse_strategy_rule.md").read_text()
    rule_text = rule_md.split("**Rule outcome:")[1].split("\n")[0].replace("**", "")
    lse_t = lse.drop(columns=["data_type"]).round(2)

    # Full-size Block L: fitted against the 2.7 J convention, by scatter level and data set (the evidence cited for the CP3 amendment).
    parts = per["data_key"].str.split("|")
    per = per.assign(design=parts.str[1], noise=parts.str[3], lse_true=parts.str[4].astype(float))
    fs = per[per["scale"] == "full-size"]
    by_noise = fs.pivot_table(index="noise", columns="lse_strategy", values="p90_abs_key_temperature_c", aggfunc="mean")
    by_noise = by_noise.reindex(index=["low", "moderate", "high"], columns=V.LSE_STRATEGIES).round(2).reset_index()
    wide = fs.pivot_table(index=["design", "noise", "lse_true"], columns="lse_strategy", values="p90_abs_key_temperature_c")
    fixed_better = int((wide["fixed_convention"] < wide["fitted"]).sum())
    fixed_better_by_noise = (wide["fixed_convention"] < wide["fitted"]).groupby(level="noise").agg(["sum", "size"])
    worse = wide[wide["fixed_convention"] >= wide["fitted"]].reset_index()

    # Block L under the final method.
    bl = block_l
    mini = bl[bl["scale"] == "miniature"]
    mini_t = (mini.groupby(["design", "noise"], sort=False)
              .agg(truths=("scenario_id", "size"), usable_mean=("share_usable", "mean"), lse_at_bound_mean=("share_flag_lse_at_lower_bound", "mean"),
                   weak_lower_mean=("share_flag_weak_lower_shelf", "mean"), t0_p90_all_mean=("all_t0_p90_abs", "mean"),
                   t0_p90_all_max=("all_t0_p90_abs", "max"), t0_p90_usable_mean=("usable_t0_p90_abs", "mean"),
                   use_p90_all_mean=("all_use_rel_p90_abs", "mean"), use_p90_usable_mean=("usable_use_rel_p90_abs", "mean"),
                   usable_within_reference=("usable_fits_within_reference_p90", "sum"))
              .reset_index())
    mini_md = md_table(pd.DataFrame({"design (miniature truths, USE 1 or 8 J; LSE 1, 6, 12 % of USE)": mini_t["design"],
                                     "scatter": mini_t["noise"], "truths": mini_t["truths"], "usable": mini_t["usable_mean"].map(_pct),
                                     "LSE at 0 J bound": mini_t["lse_at_bound_mean"].map(_pct),
                                     "weak lower shelf": mini_t["weak_lower_mean"].map(_pct),
                                     "T0 P90 all °C (mean / worst truth)": _num(mini_t["t0_p90_all_mean"]) + " / " + _num(mini_t["t0_p90_all_max"]),
                                     "T0 P90 usable °C": _num(mini_t["t0_p90_usable_mean"]),
                                     "USE P90 all / usable": _pcts(mini_t["use_p90_all_mean"]) + " / " + _pcts(mini_t["use_p90_usable_mean"]),
                                     "truths whose usable fits meet the references": mini_t["usable_within_reference"].astype(int)}))
    full_l = bl[bl["scale"] == "full-size"]
    full_t = (full_l.groupby(["design", "noise"], sort=False)
              .agg(truths=("scenario_id", "size"), usable_mean=("share_usable", "mean"), t41_all=("all_t41_analytic_p90_abs", "mean"),
                   t41_usable=("usable_t41_p90_abs", "mean"), t0_all=("all_t0_p90_abs", "mean"), use_all=("all_use_rel_p90_abs", "mean"))
              .reset_index())
    full_md = md_table(pd.DataFrame({"design (full-size truths, LSE 2, 5, 10 J; USE 150 J)": full_t["design"], "scatter": full_t["noise"],
                                     "truths": full_t["truths"], "usable": full_t["usable_mean"].map(_pct),
                                     "T41J P90 all / usable °C": _num(full_t["t41_all"]) + " / " + _num(full_t["t41_usable"]),
                                     "T0 P90 all °C": _num(full_t["t0_all"]), "USE P90 all": _pcts(full_t["use_all"])}))
    bl_classes = {s: trust_classes(bl[bl["scale"] == s]) for s in ["full-size", "miniature"]}
    bl_full_alt = trust_classes(V.trust_limits(metrics[(metrics["block"] == "L") & (metrics["scale"] == "full-size")
                                                       & (metrics["lse_strategy"] == SENSITIVITY_STRATEGY)], blocks=("L",)))
    bl_class_t = pd.DataFrame({"class": list(bl_classes["full-size"].keys()),
                               "full-size data sets, final method (LSE 2.7 J)": [len(v) for v in bl_classes["full-size"].values()],
                               "full-size data sets, all fitted (sensitivity)": [len(v) for v in bl_full_alt.values()],
                               "miniature data sets (LSE fitted under both)": [len(v) for v in bl_classes["miniature"].values()]})
    mini_unprotected = bl_classes["miniature"]["usable fits still miss a reference scale"].copy()
    mini_unprotected["design"] = (mini_unprotected["design"] + "; USE " + mini_unprotected["use_true"].map("{:g} J".format) + ", LSE "
                                  + (mini_unprotected["lse_true"] / mini_unprotected["use_true"]).map(lambda x: f"{100 * x:.0f} %") + " of USE")

    # All-fitted sensitivity case: trust classes side by side, and the scenarios whose class differs.
    class_t = pd.DataFrame({"class (Blocks A-D with scatter)": list(classes.keys()),
                            "final method": [len(v) for v in classes.values()],
                            "all fitted (sensitivity)": [len(v) for v in s_classes.values()]})
    key = ["block", "design", "noise"]
    label_of = lambda cl: pd.concat([v[key].assign(trust_class=k) for k, v in cl.items()], ignore_index=True)
    moved = label_of(classes).merge(label_of(s_classes), on=key, suffixes=("_final", "_all_fitted"))
    moved = moved[moved["trust_class_final"] != moved["trust_class_all_fitted"]]
    compare_ae = final_ae[final_ae["block"].isin(["A", "B", "C", "D"]) & (final_ae["noise"] != "zero")][key + [
        "all_t41_analytic_p90_abs", "all_t0_p90_abs", "all_use_rel_p90_abs", "share_usable"]].merge(
        metrics[(metrics["block"].isin(["A", "B", "C", "D"])) & (metrics["noise"] != "zero") & (metrics["lse_strategy"] == SENSITIVITY_STRATEGY)][
            key + ["all_t41_analytic_p90_abs", "all_t0_p90_abs", "all_use_rel_p90_abs", "share_usable"]], on=key, suffixes=("_final", "_all_fitted"))
    d41 = compare_ae["all_t41_analytic_p90_abs_final"] - compare_ae["all_t41_analytic_p90_abs_all_fitted"]
    d0 = compare_ae["all_t0_p90_abs_final"] - compare_ae["all_t0_p90_abs_all_fitted"]
    s_only = s_checks[(s_checks["kind"] == "only this flag") & s_checks["group"].isin(
        ["no flag", "only flag_lse_at_lower_bound", "only flag_weak_lower_shelf"])]

    n_scen, n_fits = len(design), int(design["replicates"].sum())
    n_ae_final = int((design["block"].ne("L") & design["lse_strategy"].eq(LSE_STRATEGY)).sum())
    L = ["## 2. Fitter validation on SYNTHETIC curves (not published data)", "",
         f"All tables in this section come from synthetic curves with known truth ({n_scen} scenarios, {n_fits} fits, seed {V.SEED}; "
         "`synthetic_*` files). Errors are fitted minus true. P90 |err| = the value 90 % of fits stay within. 'usable' = no optimizer "
         "failure, non-physical, boundary or weak-identification flag. T41J errors use the analytic crossing of every fit that returned "
         "estimates, including crossings outside the tested range that the method would not report. Reference scales (for reading, not "
         "acceptance): 10 °C for T41J and T0, 10 % for USE.", "",
         f"Sections 2.2-2.8 describe the FINAL PRIMARY method ({n_ae_final} scenarios of Blocks A-E). Every Block A-E truth is full-size "
         f"(true LSE 5 J, or 2 and 10 J in Block C), so there the final method fixes LSE at {F.FIXED_LSE_CONVENTION_J['full-size']:g} J, "
         "a deliberately imperfect value, as it would be for a real steel. The same Blocks A-E, on identical synthetic data, were also fitted "
         "with the pre-registered all-fitted method (sensitivity and history case, scenario IDs as before CP3; section 2.10 and "
         "`sensitivity_all_fitted_lse/`). The final method's miniature behaviour rests on Block L only (section 2.9). No scenario was added "
         "or changed at CP3.", "",
         "### 2.1 Lower shelf (Block L): the pre-registered rule and the CP3 amendment (D-042)", "",
         md_table(lse_t), "", f"Pre-registered rule outcome:{rule_text}", "",
         "The final method's row is assembled from the fits it reproduces exactly (full-size data sets: `fixed_convention`; miniature data "
         "sets: `fitted`); it is descriptive, not a candidate of the rule. Full-size data sets, key temperature T41J, mean P90 |error| (°C) "
         "by scatter level:", "",
         md_table(by_noise), "",
         f"The 2.7 J convention gave a lower T41J P90 than the fitted lower shelf in {fixed_better} of {len(wide)} full-size data sets ("
         + ", ".join(f"{n}: {int(r['sum'])} of {int(r['size'])}" for n, r in fixed_better_by_noise.reindex(["low", "moderate", "high"]).iterrows())
         + ")" + ("." if len(worse) == 0 else "; where it did not: " + "; ".join(
             f"{r.design}, {r.noise} scatter, true LSE {r.lse_true:g} J ({r.fixed_convention:.2f} against {r.fitted:.2f} °C)"
             for r in worse.itertuples(index=False)) + "."), "",
         "### 2.2 Specimen count and scatter (Block A, final method: uniform over x = -3...3; truth LSE 5 J, USE 150 J, T0 0 °C, C 30 °C)", "",
         table(block("A")), "", "### 2.3 Sampling patterns (Block B, final method)", "", table(block("B")), "",
         "### 2.4 Parameter values (Block C, final method, moderate scatter)", "", table(block("C")), "",
         "### 2.5 Fixed test windows planned without knowing T0 (Block D, final method, moderate scatter)", "", table(block("D")), "",
         "### 2.6 What the outcome categories and flags mean (Blocks A-D with scatter, final method)", "", md_table(outcome_t), "",
         "Fits carrying exactly one fit flag, against fits carrying none (flags overlap, so this is the clean comparison). With LSE fixed, "
         "the lower-shelf diagnostics cannot fire here; section 2.10 shows them for the fitted lower shelf:", "",
         only_table(checks), "", "Index-support diagnostic (D-044): usable fits with a calculated T41J, by where 41 J lies on the fitted rise:", "",
         md_table(index_t), "", "Audit diagnostics (recorded, not used to classify):", "", md_table(audit_t), "",
         "### 2.7 Upper shelves that are not flat (Block E, final method; added after Blocks A-D, D-047, D-051)", "",
         md_table(shelf.drop(columns=["data_type"]).assign(**{c: shelf[c].map(_pct) for c in [
             "share_trend_test_applicable", "share_trend_flagged", "share_trend_flagged_when_applicable", "share_usable",
             "use_error_rel_median", "use_error_rel_p90_abs"]}, t41_error_p90_abs_c=shelf["t41_error_p90_abs_c"].round(1),
             t0_error_p90_abs_c=shelf["t0_error_p90_abs_c"].round(1))), "",
         "### 2.8 Where the fitter stops being trustworthy (final method)", "",
         f"Of {len(limits)} scenarios with scatter in Blocks A-D: in {len(classes['within reference (all fits)'])}, 90 % of all fits recover "
         "T41J, T0 and USE within the reference scales (10 °C, 10 °C, 10 %). In "
         f"{len(classes['within reference only after the flags'])} more, only the fits that pass the flags do. In "
         f"{len(classes['method declines (< 5 % usable)'])}, fewer than 5 % of fits pass the flags: the method declines to report, which is "
         f"the intended behaviour. In {len(classes['usable fits still miss a reference scale'])}, 5 % or more of fits pass the flags yet the "
         "passing fits still miss at least one reference scale; these are where the fitter stops being trustworthy even with its diagnostics:", "",
         listing(classes["usable fits still miss a reference scale"].sort_values(["block", "design", "noise"])), "",
         "Scenarios in which the method declines (fewer than 5 % of fits pass):", "",
         listing(classes["method declines (< 5 % usable)"].sort_values(["block", "design", "noise"])), "",
         "### 2.9 Block L under the final method: the only miniature evidence (and full-size with LSE fixed)", "",
         "Miniature truths (final method = fitted LSE): means over the truths of each design and scatter level. No index exists for these "
         "specimens (D-045), so T0 and USE are judged:", "", mini_md, "",
         "Full-size truths (final method = LSE fixed at 2.7 J; true LSE 2, 5 or 10 J):", "", full_md, "",
         "Trust classes per Block L data set under the final method (T41J judged for full-size truths only):", "", md_table(bl_class_t), "",
         "Miniature data sets whose usable fits still miss a reference scale (the diagnostics do not protect these):", "",
         listing(mini_unprotected.sort_values(["design", "noise"]), t41=False) if len(mini_unprotected) else "None.", "",
         "### 2.10 All-fitted sensitivity case (pre-registered method) on the same Blocks A-D", "",
         md_table(class_t), "",
         f"Across the {len(compare_ae)} scenarios, final minus all-fitted T41J P90 |error|: median {d41.median():.2f} °C (range "
         f"{d41.min():.1f} to {d41.max():.1f} °C); T0 P90 |error|: median {d0.median():.2f} °C (range {d0.min():.1f} to {d0.max():.1f} °C). "
         "Scenarios whose trust class differs between the two methods:", "",
         md_table(moved) if len(moved) else "None.", "",
         "What the lower-shelf diagnostics mean when LSE is fitted (all-fitted case; this is the method applied to miniature curves):", "",
         md_table(pd.DataFrame({"fits carrying": s_only["group"].str.replace("flag_", ""), "fits": s_only["fits"],
                                "T0 P90 |err| °C": s_only["t0_p90_abs"].round(1), "T41J P90 |err| °C": s_only["t41_analytic_p90_abs"].round(1),
                                "USE P90 |err|": s_only["use_rel_p90_abs"].map(_pct), "C P90 |err|": s_only["c_rel_p90_abs"].map(_pct)})), ""]
    return L


def summary_markdown(primary, outcomes, reasons, flags, availability, by_group, params, extremes, comparison_summary, cohorts,
                     examples, sens_summary, sens_changes, before_after, residuals, residuals_alt, positions, notch, notch_records,
                     pre_cp3) -> str:
    geo = primary.groupby("geometry_category").size()
    fs = primary[primary["geometry_category"] == "full-size"]
    mini = primary[primary["geometry_category"] == "miniature"]
    calc = fs["index_status"] == "calculated"
    mini_usable = mini["outcome"].isin(F.OUTCOMES[4:])
    t41_row = lambda q: sens_summary[(sens_summary["geometry_category"] == "full-size") & (sens_summary["quantity"] == q)].iloc[0]
    t41s, t0s, uses, usej = (t41_row("T41J (all fitted - final), °C"), t41_row("T0 (all fitted - final), °C"),
                             t41_row("USE (all fitted / final - 1)"), t41_row("USE (all fitted - final), J"))
    change = lambda cat, what: int(sens_changes[(sens_changes["geometry_category"] == cat) & (sens_changes["change"] == what)]["curves"].sum())
    L = ["# WP3 summary: transition-curve fitting (q4x6v-dyt25)", "",
         "Analysis of published Charpy V-notch test data (Materials Cloud 2025.30). Section 2 is SYNTHETIC fitter validation; every other "
         "section concerns the published measurements of the CP2-frozen cohorts. Decisions: DECISIONS.md D-040 to D-051.", "",
         "**Method status (CP3 review by the author, 2026-09-14).** WP3 approved in principle, with amendments implemented here and awaiting "
         f"final CP3 approval. D-042 amended: the FINAL PRIMARY method fixes the lower shelf at {F.FIXED_LSE_CONVENTION_J['full-size']:g} J "
         "for full-size specimens and fits it (>= 0 J) for miniature specimens. It replaces the pre-registered rule's outcome (LSE fitted "
         "for every geometry), which was presented at CP3 and is kept as an explicit sensitivity case (sections 2.10 and 6, "
         "`sensitivity_all_fitted_lse/`). D-046 amended: a fitted LSE at its 0 J bound is a boundary-limited fit, not a non-physical one. "
         "D-044: exact-notch-unreported full-size curves keep T41J with an explicit flag; an index-support diagnostic and a notch-metadata "
         "sensitivity are reported.", "",
         "## 1. Method", "", method_configuration().split("\n", 2)[2], ""]
    L += synthetic_sections()
    L += ["## 3. Published data: primary cohort outcomes (final primary method)", "",
          f"Primary cohort: {len(primary)} curves, {int(primary['n_points'].sum())} records ({int(geo.get('full-size', 0))} full-size, "
          f"{int(geo.get('miniature', 0))} miniature). Every curve was fitted; none was removed.", "",
          "Mutually exclusive outcomes (first applicable category, D-046 as amended at CP3):", "",
          md_table(outcomes.assign(share=outcomes["share"].map(_pct))), "",
          "The same outcomes split by the recorded reason (also mutually exclusive):", "", md_table(reasons), "",
          "Diagnostic flags (overlapping; a curve can carry several):", "", md_table(flags), "",
          "Index temperature by geometry (D-044, D-045):", "", md_table(availability), "",
          "Where 41 J lies on the fitted rise (full-size curves with a calculated index; index-support diagnostic, D-044):", "",
          md_table(positions), "",
          f"Summary: T41J calculated for {int(calc.sum())} of {len(fs)} full-size curves; not calculated for {int((~calc).sum())} ("
          + ("; ".join(f"{k}: {v}" for k, v in fs.loc[~calc, "index_status"].value_counts().items()) or "none") + "). "
          f"{int((calc & ~fs['notch_reported']).sum())} of the calculated values come from full-size V-notch curves with exact notch "
          f"dimensions unreported; {int(fs['flag_index_near_fitted_shelf'].sum())} carry the index-support warning. "
          f"Miniature curves with a usable fit (T0, C, LSE and USE reported, no index temperature): {int(mini_usable.sum())} of {len(mini)}.", "",
          "### 3.1 Notch-metadata sensitivity (D-044; a diagnostic, the primary cohort is unchanged)", "",
          md_table(notch), "", "Notch fields of the full-size records, as reported (nothing filled in):", "", md_table(notch_records), "",
          "## 4. Where fits fail or are weak, against the WP2 sampling descriptors (final method)", "", md_table(by_group), "",
          "Residual pattern by lower-shelf treatment (measured minus fitted, % of fitted USE), final method:", "",
          md_table(residuals.round(2)), "",
          "The same for the all-fitted sensitivity case (the table that explained the fitted LSE at 0 J before CP3, D-042):", "",
          md_table(residuals_alt.round(2)), "",
          "## 5. Fitted parameters (usable fits, final method)", "", md_table(params.round(3)), "", "Extremes (all primary fits):", "",
          md_table(extremes.round(3)), "",
          "## 6. Lower-shelf sensitivity on the published curves: FINAL PRIMARY against ALL FITTED (CP3 amendment of D-042)", "",
          "A sensitivity comparison, not a second method selection. Miniature curves are fitted identically by both (LSE fitted), so every "
          "difference comes from the full-size lower shelf. Part of any outcome change is mechanical: a fixed lower shelf cannot trigger the "
          "lower-shelf diagnostics.", "",
          md_table(sens_summary.round(3)), "",
          f"Full-size headline: |T41J difference| median {t41s['median_abs']:.2f} °C, 90th percentile {t41s['p90_abs']:.2f} °C "
          f"({int(t41s['curves_compared'])} curves with T41J under both); |T0 difference| median {t0s['median_abs']:.2f} °C, 90th percentile "
          f"{t0s['p90_abs']:.2f} °C; |USE difference| median {100 * uses['median_abs']:.2f} % ({usej['median_abs']:.2f} J), 90th percentile "
          f"{100 * uses['p90_abs']:.2f} %. Outcome category differs for {change('full-size', 'outcome category differs')} of "
          f"{change('full-size', 'curves compared')} full-size curves and {change('miniature', 'outcome category differs')} miniature "
          f"curves; index availability differs for {change('full-size', 'index availability differs')} full-size curves.", "",
          "Outcome and index-availability changes (curves):", "", md_table(sens_changes), "",
          "Before and after (the previous CP3 presentation is reproduced exactly from the all-fitted run):", "", md_table(before_after), "",
          "Check: the all-fitted run under the pre-CP3 classification reproduces the counts presented at CP3:", "",
          md_table(pre_cp3.assign(share=pre_cp3["share"].map(_pct))), "",
          "## 7. Dataset-provided USE and DBTT (diagnostic only, D-049; final method)", "", md_table(comparison_summary.round(3)), "",
          "## 8. Looser and stricter cohorts (diagnostic, D-050; final method)", "", md_table(cohorts.assign(share=cohorts["share"].map(_pct))), "",
          "## 9. Example figures", "",
          "- `synthetic_examples.png`: SYNTHETIC good versus poor sampling (spread of 40 replicate fits), final method.",
          "- `synthetic_error_vs_specimens.png`, `synthetic_sampling_patterns.png`: SYNTHETIC validation summaries, final method.",
          "- `fits_published_examples.png`: published curves, final method: " + "; ".join(f"{t} ({c})" for t, c in examples) + ".",
          "- `fits_outcome_by_sampling.png`: outcome shares against WP2 sampling descriptors, final method.", ""]
    return "\n".join(L)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SENSITIVITY_OUT.mkdir(parents=True, exist_ok=True)
    membership = check_frozen_cohorts()
    curves, rec = load_curves(membership)
    fits = fit_all(curves, rec, LSE_STRATEGY)
    frozen = pd.read_csv(DATA / "FROZEN_COHORTS_CP2.csv").set_index(["release", "cohort"])
    for cohort in ["primary", "looser", "stricter"]:
        f = fits[fits[f"in_{cohort}"]]
        exp = frozen.loc[(PRIMARY_DATASET, cohort)]
        if len(f) != exp["curves"] or int(f["n_points"].sum()) != exp["records"]:
            raise AssertionError(f"{cohort}: fitted {len(f)} curves / {int(f['n_points'].sum())} records, frozen {exp['curves']} / {exp['records']}")
    primary = fits[fits["in_primary"]].reset_index(drop=True)
    # Sensitivity case: the pre-registered all-fitted method on the primary cohort. Under the pre-CP3 classification it must reproduce
    # the counts presented at CP3, which ties the sensitivity case to that presentation.
    alt = fit_all(curves[curves["in_primary"]], rec, SENSITIVITY_STRATEGY).reset_index(drop=True)
    alt.insert(alt.columns.get_loc("outcome") + 1, "outcome_pre_cp3_classification", alt.apply(F.pre_cp3_outcome, axis=1))
    pre_cp3 = outcome_table(alt, F.PRE_CP3_OUTCOMES, "outcome_pre_cp3_classification", PRE_CP3_FIT_OUTCOME)
    got = dict(zip(pre_cp3["outcome"], pre_cp3["curves"]))
    if any(got[k] != v for k, v in PRE_CP3_PRIMARY_OUTCOME_COUNTS.items()):
        raise AssertionError(f"The all-fitted sensitivity run no longer reproduces the CP3 presentation: {got}")
    write_text(OUT / "method_configuration.md", method_configuration())
    primary.drop(columns=["record_ids"]).to_csv(OUT / "fits_primary.csv", index=False)
    fits.drop(columns=["record_ids"]).to_csv(OUT / "fits_looser_cohort_curves.csv", index=False)
    outcomes = outcome_table(primary)
    outcomes.to_csv(OUT / "fit_outcomes.csv", index=False)
    reasons = outcome_reasons(primary)
    reasons.to_csv(OUT / "fit_outcome_reasons.csv", index=False)
    flags = flag_table(primary)
    flags.to_csv(OUT / "fit_flags.csv", index=False)
    availability = index_availability(primary)
    availability.to_csv(OUT / "index_availability_by_geometry.csv", index=False)
    positions = index_position(primary)
    positions.to_csv(OUT / "index_position_on_fitted_rise.csv", index=False)
    notch, notch_records = notch_metadata_sensitivity(primary, rec)
    notch.to_csv(OUT / "t41j_notch_metadata_sensitivity.csv", index=False)
    by_group = outcomes_by_group(primary)
    by_group.to_csv(OUT / "fit_outcomes_by_group.csv", index=False)
    params, extremes = parameter_summary(primary)
    params.to_csv(OUT / "parameter_summary.csv", index=False)
    extremes.to_csv(OUT / "parameter_extremes.csv", index=False)
    sensitivity, sens_summary, sens_changes = lse_sensitivity(primary, alt)
    sensitivity.to_csv(OUT / "lse_sensitivity_published.csv", index=False)
    sens_summary.to_csv(OUT / "lse_sensitivity_published_summary.csv", index=False)
    sens_changes.to_csv(OUT / "lse_sensitivity_outcome_changes.csv", index=False)
    before_after = method_change_table(primary, alt)
    before_after.to_csv(OUT / "method_change_before_after.csv", index=False)
    residuals = residual_pattern(primary, rec)
    residuals.to_csv(OUT / "residual_pattern_by_lower_shelf_outcome.csv", index=False)
    comparison, comparison_summary = dataset_comparison(fits, rec)
    comparison.to_csv(OUT / "dataset_value_comparison.csv", index=False)
    comparison_summary.to_csv(OUT / "dataset_value_comparison_summary.csv", index=False)
    cohorts = pd.concat([outcome_table(fits[fits[f"in_{c}"]]).assign(cohort=c) for c in ["looser", "primary", "stricter"]], ignore_index=True)
    cohorts.to_csv(OUT / "cohort_sensitivity_outcomes.csv", index=False)
    # Sensitivity-case tables.
    alt.drop(columns=["record_ids"]).to_csv(SENSITIVITY_OUT / "fits_primary.csv", index=False)
    outcome_table(alt).to_csv(SENSITIVITY_OUT / "fit_outcomes.csv", index=False)
    pre_cp3.to_csv(SENSITIVITY_OUT / "fit_outcomes_pre_cp3_classification.csv", index=False)
    flag_table(alt).to_csv(SENSITIVITY_OUT / "fit_flags.csv", index=False)
    residuals_alt = residual_pattern(alt, rec)
    residuals_alt.to_csv(SENSITIVITY_OUT / "residual_pattern_by_lower_shelf_outcome.csv", index=False)
    examples = example_figure(fits, rec)
    sampling_figure(fits)
    write_text(OUT / "wp3_summary.md", summary_markdown(primary, outcomes, reasons, flags, availability, by_group, params, extremes,
                                                       comparison_summary, cohorts, examples, sens_summary, sens_changes, before_after,
                                                       residuals, residuals_alt, positions, notch, notch_records, pre_cp3))
    print(f"WP3 fits: {len(fits)} curves fitted (final primary method); primary cohort {len(primary)} curves -> {OUT}")
    print(outcomes.to_string(index=False))
    print(f"All-fitted sensitivity case: {len(alt)} curves -> {SENSITIVITY_OUT}; pre-CP3 classification reproduced: {got}")


if __name__ == "__main__":
    main()
