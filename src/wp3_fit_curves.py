"""WP3 - Apply the locked transition-curve fitter to the published Charpy data of the CP2-frozen cohorts.

Analysis of published test data. Reads the frozen cohorts (outputs/wp2*/cohort_membership.csv, checked against
data/FROZEN_COHORTS_CP2.csv before anything is fitted) and the records (data/processed/primary/charpy_records_with_curves.csv).
Every curve of the looser cohort (which contains the primary and stricter cohorts) is fitted once with the method locked by the
synthetic validation (src/wp3_validation.py, D-042); every primary curve gets one row with its estimates, bounds, starting values,
solver status, diagnostics, flags, outcome and index temperature. Nothing is removed. The dataset's own USE and DBTT are read only
after fitting, for comparison (D-049).

Outputs (outputs/wp3/): method_configuration.md, fits_primary.csv, fits_looser_cohort_curves.csv, fit_outcomes.csv,
fit_flags.csv, fit_outcomes_by_group.csv, fit_outcomes_by_wp2_sampling.csv, index_availability_by_geometry.csv,
parameter_summary.csv, parameter_extremes.csv, dataset_value_comparison.csv, dataset_value_comparison_summary.csv,
fits_published_examples.png, fits_outcome_by_sampling.png, wp3_summary.md

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
DATA_TYPE = "published measurements (analysis of published test data)"
LSE_STRATEGY = V.LOCKED_LSE_STRATEGY
GEOMETRY_CATEGORY = {"full-size (55x10x10 mm)": "full-size", "sub-size, standard length (55 mm, reduced thickness)": "sub-size (E23 type)",
                     "miniature (reduced length)": "miniature"}


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
def fit_all(curves: pd.DataFrame, rec: pd.DataFrame) -> pd.DataFrame:
    by_id = rec.set_index("record_id")
    rows = []
    for c in curves.itertuples(index=False):
        ids = c.record_ids.split()
        s = by_id.loc[ids].sort_values("source_row")
        if len(s) != c.n_points:
            raise AssertionError(f"curve {c.curve_id}: {len(s)} records found, {c.n_points} expected")
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        category = GEOMETRY_CATEGORY[c.geometry_class]
        lse_fixed = F.lse_setting(LSE_STRATEGY, "full-size" if category == "full-size" else "miniature", t, e)
        fit = F.fit_curve(t, e, lse_fixed)
        criterion = F.CRITERION_J[category]
        t41, index_status = F.index_temperature(fit, t, criterion)
        cls = F.classify(fit, index_status)
        rows.append(dict(data_type=DATA_TYPE, curve_id=c.curve_id, ref_id=c.ref_id, in_primary=c.in_primary, in_looser=c.in_looser,
                         in_stricter=c.in_stricter, material_family=c.material_family, product_form=c.product_form,
                         product_form_group=c.product_form_group, irradiated=bool(c.irradiated), geometry=c.geometry,
                         geometry_class=c.geometry_class, geometry_category=category, notch_reported=bool(c.notch_reported),
                         reconstituted=bool(c.reconstituted), lse_strategy=LSE_STRATEGY,
                         prefit_n_T_lower_band=F.prefit_lower_band_temperatures(t, e),
                         criterion_j=np.nan if criterion is None else criterion, index_temperature_c=t41, index_status=index_status,
                         index_fraction_of_rise=F.index_fraction_of_rise(fit, criterion),
                         outcome=cls["outcome"], outcome_reason=cls["outcome_reason"],
                         **{k: v for k, v in cls.items() if k.startswith("flag_")},
                         **{k: v for k, v in fit.items() if k not in ("n_points",)},
                         n_points=c.n_points, n_temperatures=c.n_temperatures, T_min_c=c.T_min_c, T_max_c=c.T_max_c, T_span_c=c.T_span_c,
                         wp2_n_T_lower_band=c.n_T_lower_band, wp2_n_T_transition_band=c.n_T_transition_band,
                         wp2_n_T_upper_band=c.n_T_upper_band, wp2_energy_ratio=c.energy_ratio_min_to_screening_upper,
                         wp2_sampling_class=c.sampling_class, wp2_E_screening_upper_reference_j=c.E_screening_upper_reference_j))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 3. Accounting tables
# ---------------------------------------------------------------------------
FIT_OUTCOME = {F.OUTCOMES[0]: "optimizer failure", F.OUTCOMES[1]: "non-physical", F.OUTCOMES[2]: "boundary-limited",
               F.OUTCOMES[3]: "weakly identified", F.OUTCOMES[4]: "usable fit", F.OUTCOMES[5]: "usable fit"}
FLAG_LABELS = {
    "flag_optimizer_failure": "optimizer failure (no start converged)",
    "flag_nonphysical_lse_at_zero": "non-physical: fitted LSE at 0 J",
    "flag_nonphysical_no_rise": "non-physical: no rise (USE = LSE)",
    "flag_nonphysical_t0_at_absolute_zero": "non-physical: T0 at absolute zero",
    "flag_boundary_c_min": "boundary: C at 1 °C (width unresolved)",
    "flag_boundary_c_max": "boundary: C at the tested span",
    "flag_boundary_t0_limit": "boundary: T0 at a range limit",
    "flag_boundary_rise_max": "boundary: USE - LSE at 10x highest energy",
    "flag_boundary_lse_max": "boundary: LSE at highest energy",
    "flag_weak_transition": "weak: < 2 test temperatures inside T0 ± C",
    "flag_weak_upper_shelf": "weak: upper shelf not supported (< 2 specimens at >= 95 % of rise)",
    "flag_nonflat_upper_shelf": "model adequacy (not an outcome): upper-shelf residual trend (p < 0.05)",
    "flag_weak_lower_shelf": "weak: lower shelf not supported (< 2 specimens at <= 5 % of rise; LSE fitted)",
    "flag_numerically_singular": "ill-conditioned: Jacobian rank-deficient",
    "flag_index_unavailable": "index temperature not calculated (any reason)",
}


def outcome_table(fits: pd.DataFrame) -> pd.DataFrame:
    counts = fits["outcome"].value_counts().reindex(F.OUTCOMES, fill_value=0)
    t = pd.DataFrame({"outcome": counts.index, "curves": counts.values})
    t["fit_quality_group"] = t["outcome"].map(FIT_OUTCOME)
    t["share"] = t["curves"] / len(fits)
    total = pd.DataFrame([dict(outcome="TOTAL", curves=int(counts.sum()), fit_quality_group="", share=1.0)])
    out = pd.concat([t, total], ignore_index=True)
    if int(counts.sum()) != len(fits):
        raise AssertionError("Mutually exclusive outcomes do not add up to the number of curves")
    return out


def flag_table(fits: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([dict(flag=k, meaning=v, curves=int(fits[k].sum())) for k, v in FLAG_LABELS.items()])


def index_reasons(fits: pd.DataFrame) -> pd.DataFrame:
    return fits.groupby(["index_status"]).size().rename("curves").reset_index().sort_values("curves", ascending=False)


def geometry_label(r) -> str:
    if r.geometry_category == "full-size":
        return "full-size 55x10x10 mm, notch reported" if r.notch_reported else "full-size 55x10x10 mm, notch not reported"
    return f"{r.geometry_category}: {r.geometry}"


def index_availability(fits: pd.DataFrame) -> pd.DataFrame:
    f = fits.assign(geometry_group=fits.apply(geometry_label, axis=1))
    rows = []
    for g, h in f.groupby("geometry_group", sort=True):
        cat = h["geometry_category"].iloc[0]
        rows.append(dict(geometry_group=g, curves=len(h),
                         criterion="41 J" if cat == "full-size" else "none established",
                         basis=("10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044)" if cat == "full-size" else
                                "ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045)"),
                         index_calculated=int((h["index_status"] == "calculated").sum()),
                         index_calculated_and_fit_usable=int((h["outcome"] == F.OUTCOMES[5]).sum()),
                         not_calculated=int((h["index_status"] != "calculated").sum()),
                         not_calculated_reasons="; ".join(f"{k} ({v})" for k, v in h.loc[h["index_status"] != "calculated", "index_status"]
                                                          .value_counts().items())))
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
        for col, label in [("lse_j", "LSE (J)"), ("use_j", "USE (J)"), ("t0_c", "T0 (°C)"), ("c_c", "C (°C)"),
                           ("index_temperature_c", "T41J (°C)")]:
            v = h[col].dropna()
            if len(v) == 0:
                continue
            rows.append(dict(geometry_category=cat, parameter=label, curves=len(v), minimum=v.min(), p10=v.quantile(0.1),
                             median=v.median(), p90=v.quantile(0.9), maximum=v.max()))
    summary = pd.DataFrame(rows)
    extremes = []
    for col in ["use_j", "t0_c", "c_c", "index_temperature_c", "lse_j"]:
        v = fits[col]
        for idx in [v.idxmin(), v.idxmax()] if v.notna().any() else []:
            r = fits.loc[idx]
            extremes.append(dict(parameter=col, which="minimum" if idx == v.idxmin() else "maximum", curve_id=r["curve_id"], value=r[col],
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
    was locked and all fits made; nothing here feeds back into the fit."""
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
    weak = weakly identified primary curve with a weak transition if any (else any weak flag), most points;
    failed = optimizer failure if any, else non-physical, else boundary-limited; most points."""
    p = fits[fits["in_primary"]]
    out = []
    ok = p[(p["outcome"] == F.OUTCOMES[5]) & p["n_points"].between(10, 20)]
    if len(ok):
        out.append(("clearly successful fit", ok.assign(k=ok["rmse_j"] / ok["use_j"]).sort_values(["k", "curve_id"]).iloc[0]))
    weak = p[p["outcome"] == F.OUTCOMES[3]]
    if len(weak):
        pool = weak[weak["flag_weak_transition"]] if weak["flag_weak_transition"].any() else weak
        out.append(("converged but weakly identified", pool.sort_values(["n_points", "curve_id"], ascending=[False, True]).iloc[0]))
    for outcome in F.OUTCOMES[:3]:
        bad = p[p["outcome"] == outcome]
        if len(bad):
            out.append((outcome, bad.sort_values(["n_points", "curve_id"], ascending=[False, True]).iloc[0]))
            break
    # Added after the published fits existed (D-051), for teaching only: also show a boundary-limited fit when the panel above is not one.
    shown = {title for title, _ in out}
    lim = p[p["outcome"] == F.OUTCOMES[2]]
    if "boundary-limited" not in shown and len(lim):
        out.append(("boundary-limited", lim.sort_values(["n_points", "curve_id"], ascending=[False, True]).iloc[0]))
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
            lse_txt = "0 J (at the 0 J bound)" if r["flag_nonphysical_lse_at_zero"] else f"{r['lse_j']:.3g} J"
            lines += [f"LSE {lse_txt}, fitted; USE {r['use_j']:.3g} J ({r['use_support']})",
                      f"T0 {r['t0_c']:.0f} °C; C {r['c_c']:.0f} °C; test temperatures inside T0 ± C: {r['n_T_transition_fit']}",
                      f"index: {r['index_status']}"]
        ax.text(0.0, -0.2, "\n".join(textwrap.fill(x, 72) for x in lines), transform=ax.transAxes, fontsize=6.8, va="top", color=INK2)
    handles, labels = {}, {}
    for ax in axes[0]:
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), loc="upper center", ncol=4, fontsize=7.5, frameon=False,
               bbox_to_anchor=(0.5, 0.955))
    fig.suptitle("WP3 transition-curve fits to published Charpy V-notch data (examples)", fontsize=10, color=INK)
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
# 4b. Characterizing the lower-shelf weakness (added after the published fits existed; describes, changes nothing; D-051)
# ---------------------------------------------------------------------------
def residual_pattern(primary: pd.DataFrame, rec: pd.DataFrame) -> pd.DataFrame:
    """Mean residual (measured - fitted, as % of fitted USE) in four regions of the fitted curve, by geometry and by whether the fitted
    LSE rests at 0 J. A symmetric tanh that cannot follow the measured shape leaves systematic residuals of opposite sign."""
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
        row = dict(curve_id=r.curve_id, geometry_category=r.geometry_category, lse_at_zero=bool(r.flag_nonphysical_lse_at_zero), c_c=r.c_c)
        for name, in_region in regions.items():
            m = in_region(x)
            row[name] = res[m].mean() if m.any() else np.nan
        rows.append(row)
    d = pd.DataFrame(rows)
    g = d.groupby(["geometry_category", "lse_at_zero"])
    out = g.size().rename("curves").to_frame()
    for name in regions:
        out[f"mean residual, {name}, % of USE"] = g[name].mean()
        out[f"curves with points, {name}"] = g[name].count()
    out["median C (°C)"] = g["c_c"].median()
    return out.reset_index()


def index_position(primary: pd.DataFrame) -> pd.DataFrame:
    """Where 41 J lies on the fitted rise for full-size curves with a calculated index (audit column of D-047)."""
    f = primary[(primary["geometry_category"] == "full-size") & (primary["index_status"] == "calculated")]
    bins = pd.cut(f["index_fraction_of_rise"], [-np.inf, 0.119, 0.881, np.inf],
                  labels=["below 11.9 % (flat lower part of the fit)", "11.9-88.1 % (inside T0 ± C)", "above 88.1 % (flat upper part)"])
    t = pd.crosstab(bins, f["outcome"]).reindex(columns=F.OUTCOMES, fill_value=0)
    t = t.loc[:, t.sum() > 0]
    t.insert(0, "curves", t.sum(axis=1))
    return t.reset_index().rename(columns={"index_fraction_of_rise": "41 J position on the fitted rise"})


# ---------------------------------------------------------------------------
# 5b. Lower-shelf sensitivity on published data (declared in D-042 before any published curve was fitted)
# ---------------------------------------------------------------------------
def lse_sensitivity(primary: pd.DataFrame, rec: pd.DataFrame) -> tuple:
    """Refit every primary curve with the alternative lower-shelf strategy `fixed_convention` (2.7 J full-size, 0.1 J miniature) and
    report only the differences in T41J, T0 and USE. Outcome counts are deliberately not compared: a fixed shelf cannot trigger the
    lower-shelf flags, so its counts would look better for a mechanical reason (D-042)."""
    by_id = rec.set_index("record_id")
    rows = []
    for r in primary.itertuples(index=False):
        s = by_id.loc[r.record_ids.split()].sort_values("source_row")  # same record order as fit_all
        t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
        scale = "full-size" if r.geometry_category == "full-size" else "miniature"
        alt = F.fit_curve(t, e, F.lse_setting("fixed_convention", scale, t, e))
        t41_alt, status_alt = F.index_temperature(alt, t, F.CRITERION_J[r.geometry_category])
        rows.append(dict(data_type=DATA_TYPE, curve_id=r.curve_id, geometry_category=r.geometry_category, outcome_locked_method=r.outcome,
                         lse_fitted_j=r.lse_j, lse_fixed_j=alt.get("lse_fixed_j", np.nan),
                         t41_fitted_lse_c=r.index_temperature_c, t41_fixed_lse_c=t41_alt, index_status_fixed_lse=status_alt,
                         t0_fitted_lse_c=r.t0_c, t0_fixed_lse_c=alt.get("t0_c", np.nan),
                         use_fitted_lse_j=r.use_j, use_fixed_lse_j=alt.get("use_j", np.nan)))
    d = pd.DataFrame(rows)
    d["t41_difference_c"] = d["t41_fixed_lse_c"] - d["t41_fitted_lse_c"]
    d["t0_difference_c"] = d["t0_fixed_lse_c"] - d["t0_fitted_lse_c"]
    d["use_difference_rel"] = d["use_fixed_lse_j"] / d["use_fitted_lse_j"] - 1.0
    summary = []
    for cat, h in d.groupby("geometry_category"):
        for col, label in [("t41_difference_c", "T41J (fixed - fitted), °C"), ("t0_difference_c", "T0 (fixed - fitted), °C"),
                           ("use_difference_rel", "USE (fixed / fitted - 1)")]:
            v = h[col].dropna()
            if len(v):
                summary.append(dict(geometry_category=cat, quantity=label, curves_compared=len(v), median=v.median(),
                                    median_abs=v.abs().median(), p90_abs=v.abs().quantile(0.9), max_abs=v.abs().max()))
    return d, pd.DataFrame(summary)


# ---------------------------------------------------------------------------
# 6. Method configuration (generated from the constants actually used)
# ---------------------------------------------------------------------------
def method_configuration() -> str:
    L = ["# WP3 method configuration (generated from src/wp3_fitter.py and src/wp3_validation.py)", "",
         "| item | setting | decision |", "| --- | --- | --- |",
         "| model | E(T) = LSE + (USE - LSE)/2 [1 + tanh((T - T0)/C)]; solver parameters (LSE, USE - LSE, T0, C) | D-040 |",
         f"| lower shelf | `{LSE_STRATEGY}` (LSE a free parameter, >= 0 J) | D-042 |",
         "| upper shelf | fitted asymptote LSE + (USE - LSE); supported if >= 2 specimens where the fit is >= 95.3 % of the rise (x >= 1.5); residual trend test (p < 0.05) reported as a model-adequacy flag outside the outcome | D-043 |",
         f"| index temperature, full-size 55x10x10 mm | T at {F.FULL_SIZE_CRITERION_J:g} J, analytic; only if LSE < 41 J < USE and inside the tested range | D-044 |",
         "| index temperature, miniature / E23 sub-size | not calculated (no defensible criterion) | D-045 |",
         f"| optimizer | scipy.optimize.least_squares, method trf, analytic Jacobian, scaled parameters, ftol = xtol = gtol = {F.TOLERANCE:g}, max_nfev = {F.MAX_NFEV} per start | D-041 |",
         "| weighting | ordinary (unweighted) least squares on energy | D-041 |",
         "| starts (6, deterministic) | LSE = lowest energy; USE = mean of 3 highest; T0 in {midpoint crossing, lower quartile, upper quartile of distinct temperatures}; C in {span/12, span/4} | D-041 |",
         f"| bounds | LSE [0, highest energy]; USE - LSE [0, {F.RISE_MAX_FACTOR:g} x highest energy]; T0 [max(-273.15, T_min - span), T_max + span]; C [{F.C_MIN_C:g} °C, span]; on a bound = active or within {100 * F.NEAR_BOUND_FRACTION:g} % of the interval | D-041 |",
         f"| weak transition | < {F.MIN_TRANSITION_TEMPERATURES} distinct temperatures with -1 < x < 1 | D-047 |",
         f"| weak shelves | < {F.MIN_SHELF_POINTS} specimens with x >= {F.X_SHELF:g} (upper) or x <= -{F.X_SHELF:g} (lower, fitted LSE only) | D-047 |",
         "| numerically singular | Jacobian rank < number of parameters (NumPy default tolerance) | D-047 |",
         "| outcome precedence | " + " > ".join(F.OUTCOMES) + " | D-046 |",
         f"| synthetic validation | seed {V.SEED}; {V.REPLICATES} replicates per scenario with scatter; scatter levels (sigma_T, cv): "
         + "; ".join(f"{k} ({a:g} °C, {b:g})" for k, (a, b) in V.NOISE.items()) + " | D-048 |",
         f"| reference scales (summaries only) | {V.REF_TEMPERATURE_C:g} °C for T41J and T0; {100 * V.REF_USE_REL:g} % for USE; {100 * V.REF_C_REL:g} % for C | D-048 |"]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 7. Summary document (every number below is read from a generated table)
# ---------------------------------------------------------------------------
def _pct(x) -> str:
    return "" if pd.isna(x) else f"{100 * x:.0f} %"


def synthetic_sections() -> list:
    design = pd.read_csv(OUT / "synthetic_validation_design.csv")
    metrics = pd.read_csv(OUT / "synthetic_validation_metrics.csv")
    lse = pd.read_csv(OUT / "synthetic_lse_strategy_comparison.csv")
    checks = pd.read_csv(OUT / "synthetic_flag_check.csv")
    limits = pd.read_csv(OUT / "synthetic_trust_limits.csv")
    shelf = pd.read_csv(OUT / "synthetic_nonflat_upper_shelf_check.csv")
    usable_cols = [f"share_{o}" for o in F.OUTCOMES[4:]]
    metrics["share_usable"] = metrics[usable_cols].sum(axis=1)

    def block(b, noise=None):
        m = metrics[metrics["block"] == b]
        return m if noise is None else m[m["noise"] == noise]

    def table(m, extra=()):
        t = pd.DataFrame({"design": m["design"], "scatter": m["noise"], "fits": m["replicates"],
                          "T41J P90 |err| °C": m["all_t41_analytic_p90_abs"].round(1), "T0 P90 |err| °C": m["all_t0_p90_abs"].round(1),
                          "USE P90 |err|": m["all_use_rel_p90_abs"].map(_pct), "C P90 |err|": m["all_c_rel_p90_abs"].map(_pct),
                          "usable": m["share_usable"].map(_pct),
                          "T41J P90 usable fits °C": m["usable_t41_p90_abs"].round(1), "USE P90 usable fits": m["usable_use_rel_p90_abs"].map(_pct)})
        return md_table(t)

    only = checks[checks["kind"] == "only this flag"]
    only_t = pd.DataFrame({"fits carrying": only["group"].str.replace("flag_", ""), "fits": only["fits"],
                           "T0 P90 |err| °C": only["t0_p90_abs"].round(1), "T41J P90 |err| °C": only["t41_analytic_p90_abs"].round(1),
                           "USE P90 |err|": only["use_rel_p90_abs"].map(_pct), "C P90 |err|": only["c_rel_p90_abs"].map(_pct)})
    outcome_rows = checks[checks["kind"].isin(["outcome", "outcome group"])]
    outcome_t = pd.DataFrame({"outcome": outcome_rows["group"], "fits": outcome_rows["fits"], "share": outcome_rows["share_of_fits"].map(_pct),
                              "T0 P90 |err| °C": outcome_rows["t0_p90_abs"].round(1),
                              "T41J P90 |err| °C": outcome_rows["t41_analytic_p90_abs"].round(1),
                              "USE P90 |err|": outcome_rows["use_rel_p90_abs"].map(_pct)})
    audit = checks[checks["kind"].str.startswith("audit")]
    audit_t = pd.DataFrame({"audit diagnostic": audit["group"], "fits": audit["fits"], "T0 P90 |err| °C": audit["t0_p90_abs"].round(1),
                            "T41J P90 |err| °C": audit["t41_analytic_p90_abs"].round(1)})
    fail_all = limits[~limits["all_fits_within_reference_p90"]]
    protected = fail_all[fail_all["usable_fits_within_reference_p90"]]
    refused = fail_all[~fail_all["usable_fits_within_reference_p90"] & (fail_all["share_usable"] < 0.05)]
    unprotected = fail_all[~fail_all["usable_fits_within_reference_p90"] & (fail_all["share_usable"] >= 0.05)]

    def listing(frame):
        t = frame.assign(scenario=frame["design"] + " [" + frame["noise"] + "]")
        num = lambda v: v.map(lambda x: "–" if pd.isna(x) else f"{x:.1f}")
        pct = lambda v: v.map(lambda x: "–" if pd.isna(x) else f"{100 * x:.0f} %")
        return md_table(pd.DataFrame({"scenario (block B/C/D designs, [scatter])": t["scenario"], "usable": t["share_usable"].map(_pct),
                                      "T41J P90 all / usable °C": num(t["all_t41_analytic_p90_abs"]) + " / " + num(t["usable_t41_p90_abs"]),
                                      "T0 P90 all / usable °C": num(t["all_t0_p90_abs"]) + " / " + num(t["usable_t0_p90_abs"]),
                                      "USE P90 all / usable": pct(t["all_use_rel_p90_abs"]) + " / " + pct(t["usable_use_rel_p90_abs"])}))
    rule_text = (OUT / "synthetic_lse_strategy_rule.md").read_text().split("**Rule outcome:")[1].split("\n")[0].replace("**", "")
    shelf_t = shelf.drop(columns=["data_type"]).copy()
    for c in ["share_trend_test_applicable", "share_trend_flagged", "share_trend_flagged_when_applicable", "share_usable",
              "use_error_rel_median", "use_error_rel_p90_abs"]:
        shelf_t[c] = shelf_t[c].map(_pct)
    for c in ["t41_error_p90_abs_c", "t0_error_p90_abs_c"]:
        shelf_t[c] = shelf_t[c].round(1)
    L = ["## 2. Fitter validation on SYNTHETIC curves (not published data)", "",
         f"All tables in this section come from synthetic curves with known truth ({len(design)} scenarios, "
         f"{int(design['replicates'].sum())} fits, seed {V.SEED}; `synthetic_*` files). Errors are fitted minus true. P90 |err| = the "
         "value 90 % of fits stay within. 'usable' = no optimizer failure, non-physical, boundary or weak-identification flag. T41J errors "
         "use the analytic crossing of every fit that returned estimates, including crossings outside the tested range that the method "
         "would not report. Reference scales (for reading, not acceptance): 10 °C for T41J and T0, 10 % for USE.", "",
         "### 2.1 Lower shelf: fitted or fixed (Block L, D-042)", "",
         md_table(lse.drop(columns=["data_type"]).round(2)), "", f"Pre-registered rule outcome:{rule_text}", "",
         "### 2.2 Specimen count and scatter (Block A: uniform over x = -3...3; truth LSE 5 J, USE 150 J, T0 0 °C, C 30 °C)", "",
         table(block("A")), "", "### 2.3 Sampling patterns (Block B)", "", table(block("B")), "",
         "### 2.4 Parameter values (Block C, moderate scatter)", "", table(block("C")), "",
         "### 2.5 Fixed test windows planned without knowing T0 (Block D, moderate scatter)", "", table(block("D")), "",
         "### 2.6 What the outcome categories and flags mean (Blocks A-D with scatter)", "", md_table(outcome_t), "",
         "Fits carrying exactly one flag, against fits carrying none (flags overlap, so this is the clean comparison):", "",
         md_table(only_t), "", "Audit diagnostics (recorded, not used to classify):", "", md_table(audit_t), "",
         "### 2.7 Upper shelves that are not flat (Block E, added after Blocks A-D; D-047, D-051)", "", md_table(shelf_t), "",
         "### 2.8 Where the fitter stops being trustworthy", "",
         f"Of {len(limits)} scenarios with scatter in Blocks A-D: in {len(limits) - len(fail_all)}, 90 % of all fits recover T41J, T0 and USE "
         f"within the reference scales (10 °C, 10 °C, 10 %). In {len(protected)} more, only the fits that pass the flags do. In {len(refused)}, "
         f"fewer than 5 % of fits pass the flags: the method declines to report, which is the intended behaviour. In {len(unprotected)}, "
         "5 % or more of fits pass the flags yet the passing fits still miss at least one reference scale; these are where the fitter "
         "stops being trustworthy even with its diagnostics:", "", listing(unprotected.sort_values(["block", "design", "noise"])), "",
         "Scenarios in which the method declines (fewer than 5 % of fits pass):", "", listing(refused.sort_values(["block", "design", "noise"])), ""]
    return L


def summary_markdown(primary, outcomes, flags, availability, by_group, params, extremes, comparison_summary, cohorts, examples,
                     sensitivity_summary, residuals, positions) -> str:
    L = ["# WP3 summary: transition-curve fitting (q4x6v-dyt25)", "",
         "Analysis of published Charpy V-notch test data (Materials Cloud 2025.30). Section 2 is SYNTHETIC fitter validation; every other "
         "section concerns the published measurements of the CP2-frozen cohorts. Decisions: DECISIONS.md D-040 to D-051.", "",
         "## 1. Method", "", method_configuration().split("\n", 2)[2], ""]
    L += synthetic_sections()
    geo = primary.groupby("geometry_category").size()
    L += ["## 3. Published data: primary cohort outcomes", "",
          f"Primary cohort: {len(primary)} curves, {int(primary['n_points'].sum())} records ({int(geo.get('full-size', 0))} full-size, "
          f"{int(geo.get('miniature', 0))} miniature). Every curve was fitted; none was removed.", "",
          "Mutually exclusive outcomes (first applicable category, D-046):", "", md_table(outcomes.assign(share=outcomes["share"].map(_pct))), "",
          "Diagnostic flags (a curve can carry several):", "", md_table(flags), "",
          "Index temperature by geometry (D-044, D-045):", "", md_table(availability), "",
          "Where 41 J lies on the fitted rise (full-size curves with a calculated index; audit only, D-047):", "", md_table(positions), "",
          "## 4. Where fits fail or are weak, against the WP2 sampling descriptors", "", md_table(by_group), "",
          "Residual pattern behind the lower shelf at 0 J (measured minus fitted, % of fitted USE; added after the fits existed, D-051):", "",
          md_table(residuals.round(2)), "",
          "## 5. Fitted parameters (usable fits)", "", md_table(params.round(3)), "", "Extremes (all primary fits):", "", md_table(extremes.round(3)), "",
          "## 6. Lower-shelf sensitivity on the published curves (declared in D-042 before fitting)", "",
          "Refit with LSE fixed at 2.7 J (full-size) or 0.1 J (miniature); differences only, outcome counts are not compared.", "",
          md_table(sensitivity_summary.round(3)), "",
          "## 7. Dataset-provided USE and DBTT (diagnostic only, D-049)", "", md_table(comparison_summary.round(3)), "",
          "## 8. Looser and stricter cohorts (diagnostic, D-050)", "", md_table(cohorts.assign(share=cohorts["share"].map(_pct))), "",
          "## 9. Example figures", "", "- `synthetic_examples.png`: SYNTHETIC good versus poor sampling (spread of 40 replicate fits).",
          "- `synthetic_error_vs_specimens.png`, `synthetic_sampling_patterns.png`: SYNTHETIC validation summaries.",
          "- `fits_published_examples.png`: published curves: " + "; ".join(f"{t} ({c})" for t, c in examples) + ".",
          "- `fits_outcome_by_sampling.png`: outcome shares against WP2 sampling descriptors.", ""]
    return "\n".join(L)


def main():
    if LSE_STRATEGY is None:
        raise RuntimeError("The lower-shelf strategy is not locked: run src/wp3_validation.py and record D-042 first.")
    OUT.mkdir(parents=True, exist_ok=True)
    membership = check_frozen_cohorts()
    curves, rec = load_curves(membership)
    fits = fit_all(curves, rec)
    frozen = pd.read_csv(DATA / "FROZEN_COHORTS_CP2.csv").set_index(["release", "cohort"])
    for cohort in ["primary", "looser", "stricter"]:
        f = fits[fits[f"in_{cohort}"]]
        exp = frozen.loc[(PRIMARY_DATASET, cohort)]
        if len(f) != exp["curves"] or int(f["n_points"].sum()) != exp["records"]:
            raise AssertionError(f"{cohort}: fitted {len(f)} curves / {int(f['n_points'].sum())} records, frozen {exp['curves']} / {exp['records']}")
    primary = fits[fits["in_primary"]].reset_index(drop=True)
    write_text(OUT / "method_configuration.md", method_configuration())
    primary.to_csv(OUT / "fits_primary.csv", index=False)
    fits.to_csv(OUT / "fits_looser_cohort_curves.csv", index=False)
    outcomes = outcome_table(primary)
    outcomes.to_csv(OUT / "fit_outcomes.csv", index=False)
    flags = flag_table(primary)
    flags.to_csv(OUT / "fit_flags.csv", index=False)
    availability = index_availability(primary)
    availability.to_csv(OUT / "index_availability_by_geometry.csv", index=False)
    by_group = outcomes_by_group(primary)
    by_group.to_csv(OUT / "fit_outcomes_by_group.csv", index=False)
    params, extremes = parameter_summary(primary)
    params.to_csv(OUT / "parameter_summary.csv", index=False)
    extremes.to_csv(OUT / "parameter_extremes.csv", index=False)
    sensitivity, sensitivity_summary = lse_sensitivity(primary.merge(curves[["curve_id", "record_ids"]], on="curve_id"), rec)
    sensitivity.to_csv(OUT / "lse_sensitivity_published.csv", index=False)
    sensitivity_summary.to_csv(OUT / "lse_sensitivity_published_summary.csv", index=False)
    residuals = residual_pattern(primary.merge(curves[["curve_id", "record_ids"]], on="curve_id"), rec)
    residuals.to_csv(OUT / "residual_pattern_by_lower_shelf_outcome.csv", index=False)
    positions = index_position(primary)
    positions.to_csv(OUT / "index_position_on_fitted_rise.csv", index=False)
    comparison, comparison_summary = dataset_comparison(fits, rec)
    comparison.to_csv(OUT / "dataset_value_comparison.csv", index=False)
    comparison_summary.to_csv(OUT / "dataset_value_comparison_summary.csv", index=False)
    cohorts = pd.concat([outcome_table(fits[fits[f"in_{c}"]]).assign(cohort=c) for c in ["looser", "primary", "stricter"]], ignore_index=True)
    cohorts.to_csv(OUT / "cohort_sensitivity_outcomes.csv", index=False)
    examples = example_figure(fits, rec)
    sampling_figure(fits)
    write_text(OUT / "wp3_summary.md", summary_markdown(primary, outcomes, flags, availability, by_group, params, extremes,
                                                       comparison_summary, cohorts, examples, sensitivity_summary, residuals, positions))
    print(f"WP3 fits: {len(fits)} curves fitted; primary cohort {len(primary)} curves -> {OUT}")
    print(outcomes.to_string(index=False))


if __name__ == "__main__":
    main()
