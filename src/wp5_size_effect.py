"""WP5 (2 of 2) - Apply the classical specimen-size normalization to the matched pairs and quantify what it leaves behind.

Analysis of published Charpy V-notch test data. Nothing here is a new measurement: every mapped point is a TRANSFORMED ESTIMATE
of full-size-equivalent behaviour derived from published smaller-specimen measurements, and every output table says so in its
`data_type` column.

Method (pre-registered in DECISIONS.md D-072 to D-086, committed before this file existed):
  1. take the STRICT matched comparisons from src/wp5_pairs.py;
  2. map the smaller specimen's measured points into the full-size-equivalent domain with the primary energy normalization
     (ligament volume B b^2, Lucas et al.) and the primary temperature correction (M = 98 - 15.1 ln(B b^2), Sokolov & Alexander
     NUREG/CR-6379 Eq. 22) - both functions of that specimen's own published dimensions only;
  3. refit the mapped points with the unchanged approved WP3 fitter under the full-size convention (LSE fixed at 2.7 J, D-077);
  4. residual DT_size = T41J(mapped smaller specimen) - T41J(measured full-size curve), sign locked in D-078;
  5. summarize comparison-weighted and family-weighted, break out by product form, geometry and irradiation state under the
     D-079 evidence thresholds, run the seven pre-declared sensitivities, and hand WP6 an explicit evidence status per geometry.

Run:  .venv/bin/python src/wp5_size_effect.py      (after src/wp5_pairs.py)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                        # noqa: E402
import pandas as pd                       # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wp3_fitter as F                    # noqa: E402
import wp5_normalization as N             # noqa: E402
from common import OUTPUTS, PROCESSED, md_table  # noqa: E402
from wp5_pairs import STRICT, WP5, curve_table   # noqa: E402

MEASURED = "PUBLISHED MEASURED DATA"
FITTED = "FITTED PARAMETER from published measurements"
TRANSFORMED = "TRANSFORMED ESTIMATE of full-size-equivalent behaviour derived from published smaller-specimen measurements"

PRIMARY_CASE = "primary"
# The pre-declared method set of D-073 to D-075. Each case changes ONE thing from the primary, so any difference in the residual
# is attributable to that one change.
CASES = {
    PRIMARY_CASE: dict(energy=N.PRIMARY_ENERGY_METHOD, temperature=N.PRIMARY_TEMPERATURE_METHOD, klst=True,
                       label="PRIMARY: energy by ligament volume B b^2 (Lucas), temperature by M = 98 - 15.1 ln(B b^2) (Sokolov Eq. 22)"),
    "S1 energy (Bb)^3/2": dict(energy="fracture volume (B b)^3/2 (Corwin et al.)", temperature=N.PRIMARY_TEMPERATURE_METHOD,
                               klst=True, label="S1: energy by the (B b)^3/2 fracture volume of Corwin et al."),
    "S2 energy Bb (area)": dict(energy="fracture area B b (Corwin first factor; Sokolov NF_brittle)",
                                temperature=N.PRIMARY_TEMPERATURE_METHOD, klst=True,
                                label="S2: energy by fracture area B b, which is Sokolov's brittle (lower-shelf) factor"),
    "S3 temperature Lucon": dict(energy=N.PRIMARY_ENERGY_METHOD, temperature="M = 92.7 - 14.34 ln(B b^2) (Lucon et al.)",
                                 klst=True, label="S3: temperature by Lucon et al.'s refit of the same log form"),
    "S4 temperature Towers": dict(energy=N.PRIMARY_ENERGY_METHOD, temperature="M = 0.7 (10 - B)^2 (Towers)", klst=True,
                                  label="S4: temperature by Towers's thickness-only quadratic"),
    "S5 temperature Wallin": dict(energy=N.PRIMARY_ENERGY_METHOD, temperature="M = -51.4 ln(2 (B/10)^0.25 - 1) (Wallin)",
                                  klst=True, label="S5: temperature by Wallin's thickness-only logarithm"),
    "S6 KLST as recorded": dict(energy=N.PRIMARY_ENERGY_METHOD, temperature=N.PRIMARY_TEMPERATURE_METHOD, klst=False,
                                label="S6: the dataset's literal width/thickness for the KLST records (D-072 alternative)"),
}
SOKOLOV_TYPE_CASE = "S7 Sokolov per-type shift"


# ---------------------------------------------------------------------------
# 1. Geometry table
# ---------------------------------------------------------------------------
def geometry_table(curves: pd.DataFrame) -> pd.DataFrame:
    """Every distinct specimen geometry in the frozen primary cohort with its normalization factors and applicability flags."""
    cols = ["length_mm", "width_mm", "thickness_mm", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm"]
    rows = []
    for (geom, cat), g in curves.groupby(["geometry", "geometry_category"]):
        d = g.iloc[0]
        if not np.isfinite(d["notch_depth_mm"]):
            rows.append(dict(geometry=geom, geometry_category=cat, curves=len(g), studies=g["ref_id"].nunique(),
                             normalization_applicable=False,
                             applicability_note="notch depth not reported, so the ligament b = W - a is unknown and no "
                                                "ligament-based factor can be computed; nothing is assumed (D-009)"))
            continue
        for klst in (True, False):
            gg = N.geometry(*[d[c] for c in cols[:4]], apply_klst_correction=klst)
            stype, why = N.sokolov_type(gg, d["notch_angle_deg"], d["notch_root_radius_mm"])
            row = dict(geometry=geom, geometry_category=cat, curves=len(g), studies=g["ref_id"].nunique(),
                       klst_geometry_reading="standard KLST (D-072 primary)" if klst else "dataset literal (D-075 S6)",
                       length_mm=d["length_mm"], W_mm=gg["W_mm"], B_mm=gg["B_mm"], notch_depth_mm=gg["notch_depth_mm"],
                       notch_angle_deg=d["notch_angle_deg"], notch_root_radius_mm=d["notch_root_radius_mm"],
                       ligament_b_mm=gg["ligament_mm"], notch_depth_over_width=gg["notch_depth_over_width"],
                       fracture_area_Bb_mm2=gg["fracture_area_mm2"], ligament_volume_Bb2_mm3=gg["ligament_volume_mm3"],
                       notch_depth_over_root_radius=(gg["notch_depth_mm"] / d["notch_root_radius_mm"]
                                                     if np.isfinite(d["notch_root_radius_mm"]) and d["notch_root_radius_mm"] > 0
                                                     else np.nan),
                       sokolov_specimen_type=stype or "none", sokolov_type_basis=why,
                       sokolov_per_type_shift_c=N.SOKOLOV_TYPES[stype]["shift_c"] if stype else np.nan,
                       sokolov_per_type_two_sigma_c=N.SOKOLOV_TYPES[stype]["two_sigma_c"] if stype else np.nan,
                       normalization_applicable=True, applicability_note=gg["geometry_note"] or "")
            for name, fn in N.ENERGY_METHODS.items():
                row[f"NF_E [{name}]"] = fn(gg)
            for name, fn in N.TEMPERATURE_METHODS.items():
                row[f"M_degC [{name}]"] = fn(gg)
            rows.append(row)
            if cat == "full-size" or geom not in ("27x3x4 a=1",):
                break        # only the KLST records have two readings
    out = pd.DataFrame(rows).sort_values(["geometry_category", "ligament_volume_Bb2_mm3"], ascending=[True, False])
    out.insert(0, "data_type", MEASURED + " (published specimen dimensions) with derived geometric factors")
    return out


# ---------------------------------------------------------------------------
# 2. Map one smaller-specimen curve into the full-size-equivalent domain and refit it
# ---------------------------------------------------------------------------
def map_and_refit(t, e, geom_row: pd.Series, case: dict) -> dict:
    """Transform the measured points, then refit with the unchanged WP3 fitter under the full-size convention (D-077).

    `geom_row` supplies only the SMALLER specimen's own published dimensions. Nothing about the paired full-size curve is
    passed in, which is the structural half of the leakage check (D-086 check 8)."""
    g = N.geometry(geom_row["length_mm"], geom_row["width_mm"], geom_row["thickness_mm"], geom_row["notch_depth_mm"],
                   apply_klst_correction=case["klst"])
    t_fse, e_fse, nf, m = N.normalize(t, e, g, case["energy"], case["temperature"])
    if not np.isfinite(m):
        return dict(mapped=False, reason=f"the published shift is undefined for this geometry ({case['temperature']})",
                    nf_energy=nf, shift_c=m, **{f"geom_{k}": v for k, v in g.items()})

    lse_fixed = F.FIXED_LSE_CONVENTION_J["full-size"]           # 2.7 J, D-042 / D-077
    fit = F.fit_curve(t_fse, e_fse, lse_fixed=lse_fixed)
    index_c, index_status = F.index_temperature(fit, t_fse, F.FULL_SIZE_CRITERION_J)
    frac = F.index_fraction_of_rise(fit, F.FULL_SIZE_CRITERION_J)
    outcome = F.classify(fit, index_status, frac)
    bracket = F.criterion_bracketing(np.asarray(e_fse, float), F.FULL_SIZE_CRITERION_J, index_status)
    return dict(mapped=True, reason="", nf_energy=nf, shift_c=m,
                **{f"geom_{k}": v for k, v in g.items()},
                norm_lse_j=fit.get("lse_j", np.nan), norm_use_j=fit.get("use_j", np.nan), norm_t0_c=fit.get("t0_c", np.nan),
                norm_c_c=fit.get("c_c", np.nan), norm_rmse_j=fit.get("rmse_j", np.nan),
                norm_use_support=fit.get("use_support", ""), norm_optimizer_success=fit.get("optimizer_success", False),
                norm_t41j_c=index_c, norm_index_status=index_status,
                norm_index_fraction_of_rise=frac, norm_outcome=outcome["outcome"], norm_outcome_reason=outcome["outcome_reason"],
                norm_flag_index_near_fitted_shelf=outcome.get("flag_index_near_fitted_shelf", False),
                norm_criterion_bracketed=bracket.get("criterion_bracketed_by_measured_energy"),
                norm_index_empirical_bracketing=bracket.get("index_empirical_bracketing"),
                norm_T_min_c=float(np.min(t_fse)), norm_T_max_c=float(np.max(t_fse)))


def fitted_energy(row_prefix: dict, t) -> np.ndarray:
    return F.tanh_energy(t, row_prefix["lse"], row_prefix["use"], row_prefix["t0"], row_prefix["c"])


# ---------------------------------------------------------------------------
# 3. Run every matched comparison through every pre-declared case
# ---------------------------------------------------------------------------
def run_comparisons(pairs: pd.DataFrame, curves: pd.DataFrame, points: dict) -> tuple:
    idx = curves.set_index("curve_id")
    rows, mapped_points = [], []
    for p in pairs.itertuples(index=False):
        s, f = idx.loc[p.smaller_curve_id], idx.loc[p.full_size_curve_id]
        ts, es = points[p.smaller_curve_id]
        tf, ef = points[p.full_size_curve_id]
        for case_name, case in CASES.items():
            r = map_and_refit(ts, es, s, case)
            base = dict(
                data_type=TRANSFORMED, case=case_name, case_label=case["label"],
                pair_id=p.pair_id, family_id=p.family_id, match_class=p.match_class,
                study_ref_id=p.full_size_ref_id, material_std=p.material_std, product_form=f["product_form"],
                heat_proxy_composition=f["composition_signature"][:80],
                irradiated=bool(f["irradiated_resolved"]), fluence_n_per_cm2=f["fluence_n_per_cm2"],
                irradiation_temp_c=f["irradiation_temp_c"],
                smaller_curve_id=p.smaller_curve_id, smaller_geometry=p.smaller_geometry,
                full_size_curve_id=p.full_size_curve_id, full_size_geometry=p.full_size_geometry,
                smaller_n_points=int(s["n_points"]), full_size_n_points=int(f["n_points"]),
                smaller_wp3_outcome=s["outcome"], full_size_wp3_outcome=f["outcome"],
                smaller_wp3_lse_j=s["lse_j"], smaller_wp3_use_j=s["use_j"], smaller_wp3_t0_c=s["t0_c"], smaller_wp3_c_c=s["c_c"],
                full_size_use_j=f["use_j"], full_size_t0_c=f["t0_c"], full_size_c_c=f["c_c"],
                full_size_t41j_c=f["index_temperature_c"], full_size_index_status=f["index_status"],
                full_size_flag_index_near_fitted_shelf=f["flag_index_near_fitted_shelf"],
                full_size_flag_index_not_bracketed=f["flag_index_not_bracketed_by_measured_energy"],
                full_size_notch_dimensions_unreported=f["flag_full_size_notch_dimensions_unreported"],
                full_size_use_above_200J=bool(f["use_j"] > N.USE_APPLICABILITY_LIMIT_J),
                full_size_T_min_c=float(np.min(tf)), full_size_T_max_c=float(np.max(tf)),
                smaller_T_min_c=float(np.min(ts)), smaller_T_max_c=float(np.max(ts)),
            )
            base.update(r)
            if r["mapped"]:
                base["delta_t_size_c"] = (r["norm_t41j_c"] - f["index_temperature_c"]
                                          if np.isfinite(r["norm_t41j_c"]) and np.isfinite(f["index_temperature_c"]) else np.nan)
                base["delta_t0_c"] = r["norm_t0_c"] - f["t0_c"]
                base["observed_pair_shift_t0_c"] = f["t0_c"] - s["t0_c"]
                base["published_shift_minus_observed_c"] = r["shift_c"] - (f["t0_c"] - s["t0_c"])
                base["norm_use_over_full_size_use"] = r["norm_use_j"] / f["use_j"]
                if case_name == PRIMARY_CASE:
                    mapped_points.append(pd.DataFrame(dict(
                        data_type=TRANSFORMED, pair_id=p.pair_id, smaller_curve_id=p.smaller_curve_id,
                        measured_temperature_c=ts, measured_energy_j=es,
                        transformed_temperature_c=ts + r["shift_c"], transformed_energy_j=es * r["nf_energy"],
                        nf_energy=r["nf_energy"], shift_c=r["shift_c"])))
            else:
                base.update(delta_t_size_c=np.nan, delta_t0_c=np.nan, observed_pair_shift_t0_c=f["t0_c"] - s["t0_c"],
                            published_shift_minus_observed_c=np.nan, norm_use_over_full_size_use=np.nan)
            rows.append(base)
    return pd.DataFrame(rows), (pd.concat(mapped_points, ignore_index=True) if mapped_points else pd.DataFrame())


def sokolov_per_type(pairs: pd.DataFrame, curves: pd.DataFrame, points: dict, primary: pd.DataFrame) -> pd.DataFrame:
    """S7 (D-075): Sokolov's per-specimen-type shifts, applied ONLY where the geometry is one of the four types that report
    built. Where it is not, the row says the normalization is not defensibly established for that geometry, with no number."""
    idx = curves.set_index("curve_id")
    rows = []
    for p in pairs.itertuples(index=False):
        s, f = idx.loc[p.smaller_curve_id], idx.loc[p.full_size_curve_id]
        g = N.geometry(s["length_mm"], s["width_mm"], s["thickness_mm"], s["notch_depth_mm"])
        stype, why = N.sokolov_type(g, s["notch_angle_deg"], s["notch_root_radius_mm"])
        row = dict(data_type=TRANSFORMED, case=SOKOLOV_TYPE_CASE, pair_id=p.pair_id, family_id=p.family_id,
                   smaller_geometry=p.smaller_geometry, sokolov_specimen_type=stype or "none", basis=why)
        if stype is None:
            row.update(applicable=False, shift_c=np.nan, two_sigma_c=np.nan, delta_t_size_c=np.nan,
                       note="normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four "
                            "specimen types NUREG/CR-6379 built, and are not extrapolated")
        else:
            t = N.SOKOLOV_TYPES[stype]
            ts, es = points[p.smaller_curve_id]
            nf = N.nf_energy_ligament_volume(g)
            t_fse, e_fse = np.asarray(ts, float) + t["shift_c"], np.asarray(es, float) * nf
            fit = F.fit_curve(t_fse, e_fse, lse_fixed=F.FIXED_LSE_CONVENTION_J["full-size"])
            index_c, status = F.index_temperature(fit, t_fse, F.FULL_SIZE_CRITERION_J)
            row.update(applicable=True, shift_c=t["shift_c"], two_sigma_c=t["two_sigma_c"],
                       norm_t41j_c=index_c, norm_index_status=status,
                       delta_t_size_c=(index_c - f["index_temperature_c"]
                                       if np.isfinite(index_c) and np.isfinite(f["index_temperature_c"]) else np.nan),
                       note=f"Sokolov & Alexander Eq. for {stype}: +{t['shift_c']:.0f} (+/- {t['two_sigma_c']:.0f}) deg C")
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 4. Primary analysis set and summaries (D-079, D-080)
# ---------------------------------------------------------------------------
def in_primary_set(df: pd.DataFrame) -> pd.Series:
    """STRICT match, a usable full-size WP3 fit with a calculated T41J, and a usable transformed refit with a calculated T41J."""
    return (df["match_class"].eq(STRICT)
            & df["full_size_wp3_outcome"].str.startswith("usable fit").fillna(False)
            & df["full_size_index_status"].eq("calculated")
            & df["norm_outcome"].fillna("").str.startswith("usable fit")
            & df["norm_index_status"].fillna("").eq("calculated")
            & df["delta_t_size_c"].notna())


def summarize(values: pd.Series, n_families: int, n_studies: int, label: str, weighting: str) -> dict:
    v = values.dropna().to_numpy(float)
    out = dict(subset=label, weighting=weighting, n=len(v), n_families=n_families, n_studies=n_studies)
    if len(v) == 0:
        return {**out, "note": "no comparison in this subset"}
    out.update(mean_c=v.mean(), median_c=float(np.median(v)), mae_c=float(np.mean(np.abs(v))),
               rmse_c=float(np.sqrt(np.mean(v ** 2))), min_c=v.min(), max_c=v.max())
    if len(v) >= 4:
        out.update(sd_c=float(np.std(v, ddof=1)),
                   robust_scale_1p4826_mad_c=float(1.4826 * np.median(np.abs(v - np.median(v)))),
                   p10_c=float(np.percentile(v, 10)), p25_c=float(np.percentile(v, 25)),
                   p75_c=float(np.percentile(v, 75)), p90_c=float(np.percentile(v, 90)), note="")
    else:
        out["note"] = ("fewer than 4 observations: SD and percentiles suppressed (D-080); values "
                       + ", ".join(f"{x:+.1f}" for x in np.sort(v)) + " deg C")
    return out


def summary_block(df: pd.DataFrame, label: str) -> list:
    """Comparison-weighted and family-weighted summaries of one subset (D-070, D-080)."""
    fam = df.groupby("family_id")["delta_t_size_c"].mean()
    fam_studies = df.drop_duplicates("family_id")["study_ref_id"].nunique()
    return [summarize(df["delta_t_size_c"], df["family_id"].nunique(), df["study_ref_id"].nunique(), label, "comparison-weighted"),
            summarize(fam, len(fam), fam_studies, label, "family-weighted (each family's mean counts once)")]


def stratified(df: pd.DataFrame, by: str, label_prefix: str) -> pd.DataFrame:
    """Per-stratum summaries under the D-079 evidence thresholds: at least 3 independent families from at least 2 publications
    before a central value and a scale are reported at all."""
    rows = []
    for key, g in df.groupby(by, dropna=False):
        fam, stud = g["family_id"].nunique(), g["study_ref_id"].nunique()
        head = dict(stratum=f"{label_prefix}: {key}", n_comparisons=len(g), n_families=fam, n_studies=stud,
                    pair_ids="; ".join(sorted(g["pair_id"])),
                    values_c="; ".join(f"{x:+.1f}" for x in np.sort(g["delta_t_size_c"].dropna())))
        if fam >= 3 and stud >= 2:
            head["evidence"] = "sufficient (>= 3 families from >= 2 publications)"
            for w, series in [("comparison-weighted", g["delta_t_size_c"]),
                              ("family-weighted", g.groupby("family_id")["delta_t_size_c"].mean())]:
                st = summarize(series, fam, stud, "", w)
                rows.append({**head, "weighting": w, "n_summarized": st["n"],
                             **{k: v for k, v in st.items() if k not in ("subset", "weighting", "n", "n_families", "n_studies")}})
        else:
            head.update(weighting="not summarized", n_summarized=0,
                        evidence="insufficient matched evidence for a standalone estimate "
                                 f"({fam} independent famil{'y' if fam == 1 else 'ies'} from {stud} "
                                 f"publication{'' if stud == 1 else 's'}; D-079 requires >= 3 from >= 2). "
                                 "The individual comparisons are listed instead of a summary statistic.")
            rows.append(head)
    cols = ["stratum", "weighting", "evidence", "n_comparisons", "n_families", "n_studies", "n_summarized"]
    out = pd.DataFrame(rows)
    return out[cols + [c for c in out.columns if c not in cols]]


# ---------------------------------------------------------------------------
# 5. Before / after (D-084)
# ---------------------------------------------------------------------------
def before_after(df: pd.DataFrame, curves: pd.DataFrame, points: dict) -> pd.DataFrame:
    idx = curves.set_index("curve_id")
    rows = []
    for r in df.itertuples(index=False):
        s, f = idx.loc[r.smaller_curve_id], idx.loc[r.full_size_curve_id]
        ts, _ = points[r.smaller_curve_id]
        tf, _ = points[r.full_size_curve_id]
        full = dict(lse=f["lse_j"], use=f["use_j"], t0=f["t0_c"], c=f["c_c"])
        raw = dict(lse=s["lse_j"], use=s["use_j"], t0=s["t0_c"], c=s["c_c"])
        norm = dict(lse=r.norm_lse_j, use=r.norm_use_j, t0=r.norm_t0_c, c=r.norm_c_c)

        def curve_rms(sm_fit, lo, hi):
            """RMS difference between the smaller curve's fitted energy and the full-size fitted energy over the temperature
            interval where BOTH have measured support, as a fraction of the full-size fitted USE. Empty overlap -> no number."""
            lo, hi = max(lo, float(np.min(tf))), min(hi, float(np.max(tf)))
            if not (hi > lo):
                return np.nan, np.nan, ("no shared supported temperature range: the normalized curve is not evaluated "
                                        "where one member of the pair has no data")
            grid = np.linspace(lo, hi, 201)
            d = fitted_energy(sm_fit, grid) - fitted_energy(full, grid)
            return float(np.sqrt(np.mean(d ** 2)) / full["use"]), hi - lo, ""

        rms_b, span_b, note_b = curve_rms(raw, float(np.min(ts)), float(np.max(ts)))
        rms_a, span_a, note_a = curve_rms(norm, r.norm_T_min_c, r.norm_T_max_c)
        rows.append(dict(
            data_type=f"{FITTED} (before) and {TRANSFORMED} (after)", pair_id=r.pair_id, family_id=r.family_id,
            smaller_geometry=r.smaller_geometry, product_form=r.product_form, irradiated=r.irradiated,
            t0_abs_difference_before_c=abs(raw["t0"] - full["t0"]), t0_abs_difference_after_c=abs(norm["t0"] - full["t0"]),
            t0_improved=abs(norm["t0"] - full["t0"]) < abs(raw["t0"] - full["t0"]),
            t41j_abs_difference_after_c=abs(r.delta_t_size_c) if np.isfinite(r.delta_t_size_c) else np.nan,
            relative_use_difference_before=(raw["use"] - full["use"]) / full["use"],
            relative_use_difference_after=(norm["use"] - full["use"]) / full["use"],
            use_improved=abs(norm["use"] - full["use"]) < abs(raw["use"] - full["use"]),
            curve_rms_difference_over_shared_range_before=rms_b, shared_range_before_c=span_b, shared_range_note_before=note_b,
            curve_rms_difference_over_shared_range_after=rms_a, shared_range_after_c=span_a, shared_range_note_after=note_a,
            curve_rms_improved=(rms_a < rms_b) if np.isfinite(rms_a) and np.isfinite(rms_b) else None,
            observed_pair_shift_t0_c=r.observed_pair_shift_t0_c, published_shift_c=r.shift_c,
            published_minus_observed_shift_c=r.published_shift_minus_observed_c))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 6. WP6 handoff (D-083)
# ---------------------------------------------------------------------------
def handoff(primary: pd.DataFrame, all_strict: pd.DataFrame, geo: pd.DataFrame, curves: pd.DataFrame) -> pd.DataFrame:
    small_geoms = sorted(curves.loc[curves["geometry_category"] != "full-size", "geometry"].unique())
    gidx = geo[geo["klst_geometry_reading"].fillna("standard KLST (D-072 primary)").str.startswith("standard")].set_index("geometry")
    rows = []
    for geom in small_geoms:
        g = primary[primary["smaller_geometry"] == geom]
        s_all = all_strict[all_strict["smaller_geometry"] == geom]
        fam, stud = g["family_id"].nunique(), g["study_ref_id"].nunique()
        gi = gidx.loc[geom] if geom in gidx.index else None
        row = dict(smaller_geometry=geom,
                   B_mm=gi["B_mm"] if gi is not None else np.nan, ligament_b_mm=gi["ligament_b_mm"] if gi is not None else np.nan,
                   ligament_volume_Bb2_mm3=gi["ligament_volume_Bb2_mm3"] if gi is not None else np.nan,
                   NF_energy_primary=gi[f"NF_E [{N.PRIMARY_ENERGY_METHOD}]"] if gi is not None else np.nan,
                   temperature_shift_primary_c=gi[f"M_degC [{N.PRIMARY_TEMPERATURE_METHOD}]"] if gi is not None else np.nan,
                   sokolov_specimen_type=gi["sokolov_specimen_type"] if gi is not None else "unknown",
                   n_strict_comparisons=len(s_all), n_primary_comparisons=len(g), n_families=fam, n_studies=stud,
                   product_forms="; ".join(sorted(g["product_form"].unique())) or "none",
                   irradiation_states="; ".join(sorted({"irradiated" if x else "unirradiated" for x in g["irradiated"]})) or "none",
                   scale_definition="family-weighted standard deviation of DT_size about the family-weighted mean, in deg C "
                                    "(DT_size = T41J from the normalized smaller specimen minus the measured full-size T41J)",
                   applicability_notes="; ".join(filter(None, [
                       "full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in "
                       f"{int(g['full_size_use_above_200J'].sum())} of {len(g)} primary comparisons" if len(g) else "",
                       "not one of the four specimen types NUREG/CR-6379 built; its Eqs (18)-(21) do not apply"
                       if gi is not None and gi["sokolov_specimen_type"] == "none" else ""])))
        if len(g) == 0:
            row.update(central_bias_c=np.nan, residual_scale_sd_c=np.nan, residual_scale_robust_c=np.nan,
                       evidence_status="UNSUPPORTED BY THIS DATASET",
                       evidence_note="no matched comparison reaches the primary analysis set; WP6 may not treat this dataset as "
                                     "having measured a correction for this geometry and must use a clearly labelled external "
                                     "literature scenario if it is to be simulated at all")
        else:
            fam_means = g.groupby("family_id")["delta_t_size_c"].mean()
            supported = fam >= 3 and stud >= 2
            row.update(central_bias_c=float(fam_means.mean()),
                       family_delta_t_size_values_c="; ".join(f"{x:+.1f}" for x in np.sort(fam_means)),
                       # D-080: with fewer than 4 observations a standard deviation is not reported; the values are given instead.
                       residual_scale_sd_c=float(np.std(fam_means, ddof=1)) if len(fam_means) >= 4 else np.nan,
                       residual_scale_robust_c=float(1.4826 * np.median(np.abs(fam_means - np.median(fam_means))))
                       if len(fam_means) >= 4 else np.nan,
                       evidence_status="DIRECTLY SUPPORTED" if supported else "WEAKLY SUPPORTED",
                       evidence_note=("at least 3 independent matched families from at least 2 publications (D-079)" if supported
                                      else f"{fam} independent famil{'y' if fam == 1 else 'ies'} from {stud} "
                                           f"publication{'' if stud == 1 else 's'}: usable only as a sensitivity, with this "
                                           f"limitation stated wherever it is used. Fewer than 4 families, so no standard "
                                           f"deviation is reported for this geometry (D-080); the family values are listed."))
        rows.append(row)

    # Pooled row: one correction across every miniature geometry. It is the only scale this dataset can offer, and its own
    # evidence status is stated. Pooling is NOT established by the data - the between-geometry differences are of the same size
    # as the between-family differences within a geometry, and with these counts the two cannot be told apart.
    fam_means = primary.groupby("family_id")["delta_t_size_c"].mean()
    fam, stud = primary["family_id"].nunique(), primary["study_ref_id"].nunique()
    rows.append(dict(
        smaller_geometry="POOLED: all miniature geometries together", B_mm=np.nan, ligament_b_mm=np.nan,
        ligament_volume_Bb2_mm3=np.nan, NF_energy_primary=np.nan, temperature_shift_primary_c=np.nan,
        sokolov_specimen_type="mixed", n_strict_comparisons=len(all_strict), n_primary_comparisons=len(primary),
        n_families=fam, n_studies=stud,
        product_forms="; ".join(sorted(primary["product_form"].unique())),
        irradiation_states="; ".join(sorted({"irradiated" if x else "unirradiated" for x in primary["irradiated"]})),
        scale_definition="family-weighted standard deviation of DT_size about the family-weighted mean, in deg C "
                         "(DT_size = T41J from the normalized smaller specimen minus the measured full-size T41J)",
        central_bias_c=float(fam_means.mean()),
        family_delta_t_size_values_c="; ".join(f"{x:+.1f}" for x in np.sort(fam_means)),
        residual_scale_sd_c=float(np.std(fam_means, ddof=1)),
        residual_scale_robust_c=float(1.4826 * np.median(np.abs(fam_means - np.median(fam_means)))),
        evidence_status="WEAKLY SUPPORTED",
        evidence_note=f"{fam} independent matched families from {stud} publications, but only 1-3 families per geometry, so "
                      "pooling assumes one correction across geometries that differ in ligament volume by a factor of 44. The "
                      "data neither establish nor refute that assumption: the spread between geometries is the same size as the "
                      "spread between families within a geometry. Usable as a WP6 sensitivity with that stated; not a "
                      "geometry-resolved correction.",
        applicability_notes=f"full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in "
                            f"{int(primary['full_size_use_above_200J'].sum())} of {len(primary)} primary comparisons"))
    out = pd.DataFrame(rows)
    out.insert(0, "data_type", "size-correction estimate derived from published measured data via a transformed estimate")
    return out


# ---------------------------------------------------------------------------
# 7. Figures (grayscale-legible; individual points, never a smoothed distribution over so few observations)
# ---------------------------------------------------------------------------
GREY, DARK = "0.62", "0.15"


def by_ligament_volume(curves: pd.DataFrame, geoms) -> list:
    """Order geometries from the largest ligament volume to the smallest, so every figure reads in one direction."""
    vol = {}
    for g in geoms:
        d = curves[curves["geometry"] == g].iloc[0]
        vol[g] = N.geometry(d["length_mm"], d["width_mm"], d["thickness_mm"], d["notch_depth_mm"])["ligament_volume_mm3"]
    return sorted(geoms, key=lambda g: -vol[g])


def fig_inventory(pairs: pd.DataFrame, curves: pd.DataFrame, path: Path) -> None:
    """Which material-condition families were measured at which geometries."""
    geoms = by_ligament_volume(curves, list(curves.loc[curves["geometry_category"] != "full-size", "geometry"].unique()))
    fams = sorted(pairs["family_id"].unique())
    fig, ax = plt.subplots(figsize=(9.5, 0.42 * len(fams) + 2.6))
    for i, fam in enumerate(fams):
        g = pairs[pairs["family_id"] == fam]
        ax.plot([-0.6], [i], "s", ms=9, color=DARK)                       # the full-size curve of the family
        for _, r in g.iterrows():
            j = geoms.index(r["smaller_geometry"])
            ax.plot([j], [i], "o", ms=8, mfc="white", mec=DARK, mew=1.5)
        ax.plot([-0.6, max(geoms.index(x) for x in g["smaller_geometry"])], [i, i], "-", color=GREY, lw=0.8, zorder=0)
    ax.set_yticks(range(len(fams)))
    ax.set_yticklabels([f"{f}  [{pairs[pairs.family_id == f]['product_form_full'].iloc[0]}]" for f in fams], fontsize=8)
    ax.set_xticks([-0.6] + list(range(len(geoms))))
    ax.set_xticklabels(["full-size\n55x10x10\na=2"] + [g.replace(" a=", "\na=") for g in geoms], fontsize=7, rotation=38,
                       ha="right")
    ax.set_xlim(-1.2, len(geoms) - 0.4)
    ax.set_ylim(-0.8, len(fams) - 0.2)
    ax.grid(axis="x", color="0.9", lw=0.5)
    ax.set_axisbelow(True)
    ax.set_title("Matched material-condition families and the specimen geometries measured in each\n"
                 "filled square = full-size curve, open circle = matched smaller-specimen curve (published measured data)",
                 fontsize=9.5)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_before_after(primary: pd.DataFrame, curves: pd.DataFrame, points: dict, mapped: pd.DataFrame, path: Path) -> None:
    """Representative matched families: measured full-size data and fit, measured smaller-specimen data, and the normalized
    estimate. Measured published data and transformed estimates are drawn differently and said so in the legend."""
    idx = curves.set_index("curve_id")
    pick = primary.drop_duplicates("family_id").head(4)
    if pick.empty:
        pick = primary.head(4)
    n = max(1, len(pick))
    fig, axes = plt.subplots(1, n, figsize=(4.1 * n, 4.0), squeeze=False)
    for ax, (_, r) in zip(axes[0], pick.iterrows()):
        f, s = idx.loc[r["full_size_curve_id"]], idx.loc[r["smaller_curve_id"]]
        tf, ef = points[r["full_size_curve_id"]]
        ts, es = points[r["smaller_curve_id"]]
        mp = mapped[mapped["pair_id"] == r["pair_id"]]
        grid = np.linspace(min(np.min(tf), np.min(ts), r["norm_T_min_c"]) - 15,
                           max(np.max(tf), np.max(ts), r["norm_T_max_c"]) + 15, 400)
        ax.plot(tf, ef, "s", ms=5, color=DARK, label="full-size, measured (published)")
        ax.plot(grid, fitted_energy(dict(lse=f["lse_j"], use=f["use_j"], t0=f["t0_c"], c=f["c_c"]), grid), "-",
                color=DARK, lw=1.6, label="full-size WP3 fit")
        ax.plot(ts, es, "^", ms=5, color=GREY, label=f"{r['smaller_geometry']}, measured (published)")
        ax.plot(mp["transformed_temperature_c"], mp["transformed_energy_j"], "o", ms=5, mfc="white", mec=DARK, mew=1.2,
                label="normalized estimate (transformed)")
        ax.plot(grid, fitted_energy(dict(lse=r["norm_lse_j"], use=r["norm_use_j"], t0=r["norm_t0_c"], c=r["norm_c_c"]), grid),
                "--", color=DARK, lw=1.4, label="fit to the normalized estimate")
        ax.axhline(41, color="0.45", lw=0.8, ls=":")
        ax.annotate("41 J", (grid[2], 41), fontsize=7, va="bottom", color="0.35")
        for t41, mk, lab in [(f["index_temperature_c"], "v", "T41J full-size"), (r["norm_t41j_c"], "v", "T41J normalized")]:
            if np.isfinite(t41):
                ax.plot([t41], [41], mk, ms=8, color=DARK if "full" in lab else "white", mec=DARK, mew=1.2)
        ax.set_title(f"{r['family_id']}\n{r['product_form']}, "
                     f"{'irradiated' if r['irradiated'] else 'unirradiated'}   "
                     + (r"$\Delta T_{size}$ = " + f"{r['delta_t_size_c']:+.1f} " + r"$\degree$C"), fontsize=8.5)
        ax.set_xlabel("temperature (°C)", fontsize=8.5)
        ax.set_ylabel("absorbed energy (J)", fontsize=8.5)
        ax.tick_params(labelsize=7.5)
        ax.grid(color="0.92", lw=0.5)
        ax.set_axisbelow(True)
    axes[0][0].legend(fontsize=6.4, loc="upper left", framealpha=0.95, borderpad=0.35, labelspacing=0.3)
    fig.suptitle("Before and after the classical size normalization: measured published data against transformed estimates",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_residuals(primary: pd.DataFrame, sensitivity: pd.DataFrame, curves: pd.DataFrame, path: Path) -> None:
    """Every residual as an individual point, by geometry and by product form, with the family visible."""
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0))
    for ax, key, title in [(axes[0], "smaller_geometry", "by smaller-specimen geometry (largest ligament volume first)"),
                           (axes[1], "product_form", "by product form")]:
        cats = (by_ligament_volume(curves, list(primary[key].unique())) if key == "smaller_geometry"
                else sorted(primary[key].unique()))
        for i, cat in enumerate(cats):
            g = primary[primary[key] == cat]
            jitter = np.linspace(-0.16, 0.16, len(g)) if len(g) > 1 else np.zeros(1)
            ax.plot(i + jitter, g["delta_t_size_c"], "o", ms=7, mfc="white", mec=DARK, mew=1.4)
            for x, (_, r) in zip(i + jitter, g.iterrows()):
                ax.annotate(r["family_id"].split("-")[0] + "/" + r["family_id"].split("-")[2],
                            (x, r["delta_t_size_c"]), fontsize=6.2, xytext=(6, 3), textcoords="offset points", color="0.3")
        sg = sensitivity[sensitivity[key].isin(cats)] if key in sensitivity.columns else pd.DataFrame()
        if len(sg):
            for i, cat in enumerate(cats):
                gg = sg[sg[key] == cat]
                if len(gg):
                    ax.plot([i] * len(gg), gg["delta_t_size_c"], "x", ms=6, color=GREY)
        ax.axhline(0, color=DARK, lw=1.0)
        ax.set_xticks(range(len(cats)))
        ax.set_xlim(-0.6, len(cats) - 0.15)
        ax.set_xticklabels([c.replace(" a=", "\na=") for c in cats], fontsize=7, rotation=32, ha="right")
        ax.set_ylabel(r"$\Delta T_{size}$ = T41J(normalized) $-$ T41J(full-size)   (°C)", fontsize=8.5)
        ax.set_title(title + "\nopen circle = primary analysis set; x = comparison held as sensitivity", fontsize=9)
        ax.tick_params(labelsize=7.5)
        ax.grid(color="0.92", lw=0.5)
        ax.set_axisbelow(True)
    fig.suptitle("Residual specimen-size disagreement after the classical normalization (individual comparisons, not a fitted "
                 "distribution)", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_performance(ba: pd.DataFrame, path: Path) -> None:
    """Before against after: does the normalization reduce the disagreement? And how close is the published shift to the
    shift these matched pairs actually show?"""
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 4.7))
    for ax, before, after, name, unit in [
            (axes[0], "t0_abs_difference_before_c", "t0_abs_difference_after_c",
             "mid-transition temperature |T0 difference|", "°C"),
            (axes[1], "relative_use_difference_before", "relative_use_difference_after",
             "upper-shelf energy, relative difference", "")]:
        b, a = ba[before].abs(), ba[after].abs()
        lim = float(np.nanmax(np.concatenate([b, a]))) * 1.12 + 1e-9
        ax.plot([0, lim], [0, lim], "-", color=GREY, lw=1.0)
        ax.plot(b, a, "o", ms=7, mfc="white", mec=DARK, mew=1.4)
        for x, y, g in zip(b, a, ba["smaller_geometry"]):
            ax.annotate(g.split(" ")[0], (x, y), fontsize=5.8, xytext=(4, 2), textcoords="offset points", color="0.35")
        ax.set_xlim(0, lim)
        ax.set_ylim(0, lim)
        ax.set_xlabel(f"before normalization{(' (' + unit + ')') if unit else ''}", fontsize=8.5)
        ax.set_ylabel(f"after normalization{(' (' + unit + ')') if unit else ''}", fontsize=8.5)
        ax.set_title(f"{name}\npoints below the line improved; above it, worsened", fontsize=9)
        ax.tick_params(labelsize=7.5)
        ax.grid(color="0.92", lw=0.5)
        ax.set_axisbelow(True)

    ax = axes[2]
    obs, pub = ba["observed_pair_shift_t0_c"], ba["published_shift_c"]
    lo = min(float(obs.min()), float(pub.min())) - 12
    hi = max(float(obs.max()), float(pub.max())) + 12
    ax.plot([lo, hi], [lo, hi], "-", color=GREY, lw=1.0)
    ax.plot(obs, pub, "o", ms=7, mfc="white", mec=DARK, mew=1.4)
    for x, y, g in zip(obs, pub, ba["smaller_geometry"]):
        ax.annotate(g.split(" ")[0], (x, y), fontsize=5.8, xytext=(4, 2), textcoords="offset points", color="0.35")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("observed shift T0(full-size) $-$ T0(smaller), measured (\u00b0C)", fontsize=8.5)
    ax.set_ylabel("published shift M applied (\u00b0C)", fontsize=8.5)
    ax.set_title("the published correction against the shift\nthese matched pairs actually show", fontsize=9)
    ax.tick_params(labelsize=7.5)
    ax.grid(color="0.92", lw=0.5)
    ax.set_axisbelow(True)

    fig.suptitle("Does the classical normalization improve agreement with the matched full-size curve?", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 8. Method configuration and summary
# ---------------------------------------------------------------------------
def write_method_configuration(geo: pd.DataFrame, checks: pd.DataFrame) -> None:
    lines = [
        "# WP5 - specimen-size normalization: the method exactly as applied",
        "",
        "Pre-registered in DECISIONS.md D-072 to D-086 and committed before any residual existed. Implemented in "
        "`src/wp5_normalization.py`; the refits use the unchanged approved WP3 fitter `src/wp3_fitter.py`.",
        "",
        "## 1. Symbols",
        "",
        "| symbol | meaning | units |",
        "| --- | --- | --- |",
        "| W | specimen width: the dimension the notch is cut into and the crack grows through | mm |",
        "| B | specimen thickness: the dimension parallel to the notch root | mm |",
        "| a | notch depth | mm |",
        "| b = W - a | remaining ligament below the notch | mm |",
        "| B b | fracture area | mm^2 |",
        "| B b^2 | nominal fracture (ligament) volume | mm^3 |",
        "| E | absorbed energy | J |",
        "| T | test temperature | deg C |",
        "| NF_E | energy normalization factor, a ratio of like geometric quantities | dimensionless |",
        "| M | temperature correction added to the smaller specimen's test temperatures | deg C |",
        "",
        "Full-size reference (ASTM E23 standard Charpy V-notch): B = 10 mm, W = 10 mm, a = 2 mm, so b = 8 mm, "
        "B b = 80 mm^2 and B b^2 = 640 mm^3.",
        "",
        "## 2. Primary method (D-073, D-074)",
        "",
        "**Energy.**  E_full-size-equivalent = NF_E x E_measured,  with  NF_E = (B b^2)_full-size / (B b^2)_smaller "
        "= 640 / (B_s b_s^2).",
        "Source: Lucas et al. (1986), the nominal-fracture-volume normalization; quoted as B b^2 by NUREG/CR-6379 p.14, as NF3 "
        "by Lucon/NIST Eq. 10, as B(W-A)^2 by this dataset's own descriptor (Table 2), and in the 2026 ML paper's Table 1. "
        "PROJECT_BRIEF.md §5 and §6.4 name the ligament-volume convention, and this is it.",
        "",
        "**Temperature.**  T_full-size-equivalent = T_measured + M,  with  M = 98 - 15.1 x ln(B b^2)  [deg C, B b^2 in mm^3].",
        "Source: Sokolov & Alexander, NUREG/CR-6379 (ORNL-6888, 1997) Eq. (22) and Fig. 27, applied as their Eq. (17). Fitted "
        "through their four subsize specimen types and forced to give exactly zero for the full-size specimen. Developed on RPV "
        "steels (A533B plate, A508 class 2, 15Kh2MFA forging, HSSI weld 72W).",
        "",
        "**Both are functions of the smaller specimen's own published dimensions and fixed published constants only.** Nothing "
        "about the paired full-size curve enters either one, which is what makes the residual an out-of-sample test rather than "
        "a restatement of the pairing.",
        "",
        "**Refit.** The transformed points are refitted with the approved WP3 fitter under the FULL-SIZE convention (lower shelf "
        "fixed at 2.7 J; USE, T0 and C fitted), and T41J is taken from the analytic crossing under the unchanged D-044 rules, "
        "including the tested-range rule applied to the transformed temperatures (D-077).",
        "",
        "## 3. What is deliberately not run, and why (D-076)",
        "",
        "| method | why it cannot be run here |",
        "| --- | --- |",
        "| Sokolov & Alexander Eq. (11), their own proposed procedure: E = E_s [NF_brittle (100-SHEAR)/100 + NF_ductile SHEAR/100] "
        "| the dataset has **no shear-fracture-appearance column at all** (56 columns, none is shear area, fracture appearance or "
        "lateral expansion). Shear is absent for all 2,588 primary records, not partly missing. It is not imputed, not derived "
        "from temperature and not assumed to be 0 % or 100 %. Their Eq. (12) route from instrumented traces needs F_iu, F_a, "
        "F_gy and F_m, which the dataset also lacks. |",
        "| Louden B b^2/(L K_t); Kayano B b^2/K_t' | need an elastic stress-concentration factor K_t, tabulated in the sources "
        "for a handful of geometries only (five in the 2026 ML paper's Table 3, against nine miniature geometries here). Louden's "
        "DBTT form additionally needs the instrumented maximum force P_m. |",
        "| Kumar dUSE + USE_p | needs precracked-specimen energies; every retained curve here is ordinary Charpy V-notch (D-020). |",
        "| Uehira m(Bb)^n; Wallin (b_f/b_s)^m USE power law | their exponents must be calibrated against the full-size USE of the "
        "same material, which is in-sample calibration against the quantity the correction is then scored on. |",
        "",
        "## 4. Geometry and the normalization factors it gives",
        "",
        md_table(geo[[c for c in geo.columns if c not in ("data_type", "sokolov_type_basis", "applicability_note")]]),
        "",
        "## 5. Checks that must pass before any number is used (D-086)",
        "",
        md_table(checks),
        "",
        "A hand calculation for the 23.6 x 5 x 5 mm geometry, so it can be repeated with a calculator: the ligament is "
        "b = W - a = 5.00 - 0.76 = 4.24 mm; the nominal fracture volume is B b^2 = 5.00 x 4.24^2 = 89.888 mm^3; the energy factor "
        "is NF_E = 640 / 89.888 = 7.120; the temperature correction is M = 98 - 15.1 x ln(89.888) = 98 - 15.1 x 4.4986 = "
        "30.07 deg C. NUREG/CR-6379's own Table 2 gives 7.12 for the same ratio and its Eq. (18) gives +30 deg C for the same "
        "specimen, which is an end-to-end check of both the equations and the convention for which dimension is notched.",
    ]
    (WP5 / "normalization_method_configuration.md").write_text("\n".join(lines) + "\n")


def write_summary(res, primary, held, overall, by_form, by_geom, by_irr, ba, sens, hand, geo, s7) -> None:
    strict = res[res["case"] == PRIMARY_CASE]
    n_fam, n_stud = primary["family_id"].nunique(), primary["study_ref_id"].nunique()
    fam_means = primary.groupby("family_id")["delta_t_size_c"].mean()
    d = primary["delta_t_size_c"]
    pooled = hand[hand["smaller_geometry"].str.startswith("POOLED")].iloc[0]
    direct = (hand["evidence_status"] == "DIRECTLY SUPPORTED").sum()
    mini = geo[(geo["geometry_category"] == "miniature")
               & geo["klst_geometry_reading"].eq("standard KLST (D-072 primary)")]
    n_mini, n_typed = len(mini), int((mini["sokolov_specimen_type"] != "none").sum())
    lines = [
        "# WP5 - specimen size effect: results",
        "",
        "Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort, CP3-approved WP3 "
        "fits. Every mapped value is a TRANSFORMED ESTIMATE derived from published smaller-specimen measurements, never a new "
        "measurement. Method and every judgement call: DECISIONS.md D-068 to D-086, pre-registered and committed before any "
        "residual existed. **Status: WP5 complete - CP4 AWAITING AUTHOR APPROVAL.**",
        "",
        "## 1. Headline",
        "",
        f"The classical normalization **helps a great deal but does not collapse the curves**. Across the "
        f"{len(primary)} matched geometry comparisons of the primary analysis set, drawn from **{n_fam} independent "
        f"material-condition families in {n_stud} publications**, the residual index-temperature disagreement after "
        f"normalization has a family-weighted mean of **{fam_means.mean():+.1f} \u00b0C** and a family-weighted standard "
        f"deviation of **{np.std(fam_means, ddof=1):.1f} \u00b0C**, with individual comparisons spanning "
        f"{d.min():+.1f} to {d.max():+.1f} \u00b0C.",
        "",
        f"**No single smaller-specimen geometry reaches the pre-registered evidence threshold** of 3 independent matched "
        f"families from 2 publications (D-079): {direct} of {len(hand) - 1} geometry classes are DIRECTLY SUPPORTED. "
        "The dataset is therefore **not sufficient to establish a geometry-resolved size-correction uncertainty**, and the only "
        "scale it can offer WP6 is a pooled one across all miniature geometries, carried as WEAKLY SUPPORTED with that "
        "limitation attached.",
        "",
        "## 2. How much genuinely matched evidence exists",
        "",
        f"- **{len(strict)}** STRICT matched geometry comparisons, from **{strict['family_id'].nunique()}** independent "
        f"material-condition families in **{strict['study_ref_id'].nunique()}** publications (refs 53, 55, 59, 60 and 107), "
        "out of 4,824 enumerated candidate pairs (`pair_data_sufficiency.md`).",
        f"- **{len(primary)}** reach the pre-registered PRIMARY analysis set, from **{n_fam}** families in **{n_stud}** "
        f"publications; **{len(held)}** are held as sensitivity.",
        "- **0 PARTIAL and 0 cross-study comparisons.** Without a heat identifier the reported composition is the only heat "
        "proxy, and it never matches exactly across publications, so every cross-publication pair is rejected on a recorded "
        "composition difference.",
        "- **No ASTM E23-type sub-size curve exists in any cohort.** The only two such curves (ref 18, 55 x 10 x 6 mm) have "
        "4 points each and fail every WP2 screening rule. All the evidence here is miniaturized (MCVN) evidence (D-071).",
        "",
        "## 3. Residual size-correction disagreement",
        "",
        "DT_size = T41J(normalized smaller specimen) - T41J(measured full-size curve). **Positive** means the correction places "
        "the transition WARMER than the measured full-size curve, the conservative direction for a vessel integrity argument.",
        "",
        md_table(overall),
        "",
        "## 4. By product form",
        "",
        md_table(by_form),
        "",
        "## 5. By smaller-specimen geometry",
        "",
        md_table(by_geom),
        "",
        "## 6. By irradiation state",
        "",
        md_table(by_irr),
        "",
        "## 7. Does the normalization help? Before against after",
        "",
        f"Of the {len(ba)} primary comparisons: the mid-transition temperature agreed better after normalization in "
        f"**{int(ba['t0_improved'].sum())}** and worse in **{len(ba) - int(ba['t0_improved'].sum())}**; the upper-shelf energy "
        f"in **{int(ba['use_improved'].sum())}** and worse in **{len(ba) - int(ba['use_improved'].sum())}**; the curve-level "
        f"energy over the shared supported temperature range in **{int(ba['curve_rms_improved'].sum())}** and worse in "
        f"**{len(ba) - int(ba['curve_rms_improved'].sum())}**.",
        "",
        f"| quantity | median before | median after |",
        f"| --- | --- | --- |",
        f"| \\|T0 difference\\| (\u00b0C) | {ba['t0_abs_difference_before_c'].median():.1f} | "
        f"{ba['t0_abs_difference_after_c'].median():.1f} |",
        f"| \\|relative USE difference\\| | {ba['relative_use_difference_before'].abs().median():.3f} | "
        f"{ba['relative_use_difference_after'].abs().median():.3f} |",
        f"| curve RMS energy difference / full-size USE | "
        f"{ba['curve_rms_difference_over_shared_range_before'].median():.3f} | "
        f"{ba['curve_rms_difference_over_shared_range_after'].median():.3f} |",
        "",
        "**The two failures are both from ref 55**, the same severely embrittled low-toughness A533B plate (full-size USE 51-63 J). "
        "For those two pairs the measured shift runs the WRONG WAY: the miniature specimens showed a transition temperature "
        "at or ABOVE the full-size one (observed T0(full-size) - T0(smaller) = -35.5 and -2.2 \u00b0C), so adding a positive "
        "published shift of +30 to +49 \u00b0C makes the agreement worse. This is a genuine negative result and it is reported, "
        "not removed.",
        "",
        md_table(ba[["pair_id", "smaller_geometry", "t0_abs_difference_before_c", "t0_abs_difference_after_c", "t0_improved",
                     "relative_use_difference_before", "relative_use_difference_after", "use_improved",
                     "curve_rms_difference_over_shared_range_before", "curve_rms_difference_over_shared_range_after",
                     "observed_pair_shift_t0_c", "published_shift_c", "published_minus_observed_shift_c"]]),
        "",
        "## 8. The published temperature correction against the shift these pairs actually show",
        "",
        f"Excluding the two ref 55 pairs, the published shift M = 98 - 15.1 ln(B b^2) lands within "
        f"{ba[~ba['pair_id'].str.startswith('55-')]['published_minus_observed_shift_c'].abs().max():.0f} \u00b0C of the shift "
        "the matched pair actually shows, over observed shifts of 35 to 90 \u00b0C. Including them, the largest miss is "
        f"{ba['published_minus_observed_shift_c'].abs().max():.0f} \u00b0C. This comparison is an OUTCOME: the observed pair "
        "shift is never used to correct the curve it was measured from (D-074, D-078).",
        "",
        "## 9. How much the answer depends on the normalization convention",
        "",
        md_table(sens),
        "",
        "**The central bias moves a lot; the scatter barely moves.** Across the four published temperature corrections the "
        "family-weighted mean residual runs from -3.5 to -23.2 \u00b0C, while the family-weighted standard deviation stays "
        "between 11.1 and 11.9 \u00b0C. The two volume-type energy normalizations (B b^2 and (B b)^{3/2}) are almost "
        "indistinguishable. Pure fracture-area scaling (S2) is far worse, mean +42.9 \u00b0C with a standard deviation of "
        "42.1 \u00b0C, which is the expected consequence of applying Sokolov's BRITTLE (lower-shelf) factor to a whole "
        "transition curve, and is exactly why his own procedure weights two factors by percent shear - a procedure this "
        "dataset cannot support (D-076).",
        "",
        "Sokolov & Alexander's per-specimen-type shifts (S7) are applied only where the geometry is one of the four types that "
        "report built, and are not extrapolated elsewhere:",
        "",
        md_table(s7[["pair_id", "smaller_geometry", "sokolov_specimen_type", "applicable", "shift_c", "two_sigma_c",
                     "delta_t_size_c", "note"]]),
        "",
        "## 10. How this compares with published estimates",
        "",
        "| source | quantity | value |",
        "| --- | --- | --- |",
        "| NUREG/CR-6379 Eqs (18)-(21) | +/- 2 sigma on its own per-type DBTT shifts | 20-30 \u00b0C, i.e. sigma 10-15 \u00b0C |",
        "| 2026 ML paper, Table 5 (27 SA533B sub-size sets, DBTT) | RMSE of Sokolov's correction | 45.8 \u00b0C |",
        "| 2026 ML paper, Table 5 | RMSE of the best analytical correction (Towers) | 35.5 \u00b0C |",
        "| 2026 ML paper, Table 7 | RMSE of its best trained ML model | 24.9-27.2 \u00b0C |",
        f"| **this work**, primary analysis set | family-weighted SD of DT_size | **{np.std(fam_means, ddof=1):.1f} \u00b0C** "
        f"({n_fam} families) |",
        f"| **this work**, all STRICT comparisons | family-weighted SD of DT_size | "
        f"**{float(overall.loc[overall['subset'].str.startswith('all STRICT') & overall['weighting'].str.startswith('family'), 'sd_c'].iloc[0]):.1f} \u00b0C** (10 families) |",
        "",
        "The scale found here sits between Sokolov's own quoted sigma and the RMSE the 2026 paper reports for classical methods, "
        "which is the expected place for it: fewer but more strictly matched comparisons than the ML paper used, and a "
        "different index (T41J here, the tanh midpoint there).",
        "",
        "## 11. Why a scalar volume factor cannot remove the specimen-size effect",
        "",
        "1. **Less material means less energy.** A miniature specimen breaks a smaller piece of steel, so less plastic work is "
        "done and less energy is absorbed. That is the part a geometric factor can capture, and it is why the ligament volume "
        "B b^2 works as well as it does.",
        "2. **But thickness also changes the constraint at the notch.** In a thick specimen the material beside the notch root "
        "is held by the material around it and cannot contract sideways, so it sits close to plane strain: the stress becomes "
        "strongly three-dimensional (high triaxiality), which favours cleavage and pushes the transition to a higher "
        "temperature. A thin specimen has more of its cross-section near plane stress, can deform out of plane, and behaves "
        "more ductilely at the same temperature. Its transition therefore sits LOWER, and no energy scale factor can express "
        "that: it is a temperature effect, not an energy effect, which is why a second, separate temperature correction is "
        "needed at all.",
        "3. **The weakest-link effect points the same way.** Cleavage starts at the worst microstructural defect in the stressed "
        "volume. A bigger specimen samples more volume, so it is more likely to contain a bad one and fails in a brittle way "
        "sooner. This is the Weibull argument Sokolov & Alexander build their log form on.",
        "4. **The parts of the absorbed energy do not scale together.** Crack initiation energy, crack propagation energy and "
        "the energy that forms the shear lips at the specimen sides each depend differently on thickness, ligament, notch depth "
        "and notch root radius. As a specimen gets thinner the shear lips take up a larger share of the fracture surface, which "
        "raises the measured energy on the lower shelf and lowers it on the upper shelf relative to a single scale factor.",
        "5. **Notch geometry is not scaled with the specimen here.** The cohort's miniature specimens have 30\u00b0 notches with "
        "a 0.08 mm root radius (refs 52, 53, 55, 59, 60) or 60\u00b0 with 0.1 mm (KLST, refs 107, 109), against the full-size "
        "45\u00b0 and 0.25 mm; and their notch depth to width ratios are 0.15-0.33 against the standard 0.20. They are not "
        "photographic reductions of a full-size specimen. NUREG/CR-6379's own conclusion 2 reports that a sharper notch root "
        "lowers USE and RAISES the transition temperature, an effect no B b^2 ratio contains.",
        "",
        "**Therefore: smaller specimen is not full-size specimen times one volume factor.** No scalar geometry correction is "
        "exact physics, and this one is not described as such anywhere in this work.",
        "",
        "## 12. What the standards do and do not support",
        "",
        "ASTM E2248-18 §5.2 states that transition-region data from miniaturized Charpy specimens \"are not directly "
        "comparable to those obtained from full-size standard Charpy V-notch specimens and suitable correlation procedures have "
        "to be employed\", and that \"in all instances, correlations will have to be developed to relate upper shelf energy "
        "(USE) data from MCVN test to CVN comparable energy levels\". §1.3 leaves the comparison with CVN data to the user. "
        "**ASTM provides no universal transformation from any miniature geometry to a full-size T41J**, and nothing here should "
        "be read as one. §5.2 also warns that MCVN data should not be used directly to set a lowest allowable operating "
        "temperature. Where a geometry falls outside a correlation's validated domain it is flagged rather than corrected "
        f"(`geometry_normalization_factors.csv`): **{n_typed} of the {n_mini} miniature geometries in this cohort ARE one of the "
        "four specimen types NUREG/CR-6379 built**, on cross-section, notch depth and notch root radius - the 5 x 5 mm "
        "geometries are its type 1, the 3.33 x 3.33 mm geometries its type 2, and the KLST its type 4. The remaining "
        f"{n_mini - n_typed} (27.5 x 3.33 x 3.33 mm a = 0.6 mm, 20 x 2.5 x 2.5 mm and 20 x 1.5 x 1.5 mm) are not, and for those "
        "the primary correction rests on Eq. (22)'s own statement that its form may be used as guidance beyond its four types.",
        "",
        "## 13. Relationship to the 2026 machine-learning paper",
        "",
        "Kasala Sreenivasulu et al. (2026), *Scientific Reports* 16:16202 - by the authors of this project's own dataset.",
        "",
        "| | their work | this work |",
        "| --- | --- | --- |",
        "| question | PREDICT full-size USE and DBTT from sub-size data | DESIGN a test matrix: is the size-correction penalty "
        "small enough that more small specimens beat fewer large ones? |",
        "| data | 389 records, 27 sub-size sets, SA533B only, from 4 publications of the same dataset | "
        f"{len(strict)} matched comparisons, {strict['family_id'].nunique()} families, A533B plate and weld and A508 forging, "
        "from 5 publications of the same dataset |",
        "| matching | sub-size sets whose publications also report full-size results under the same processing and test protocol "
        "| the same principle, applied field by field and audited for all 4,824 candidate pairs |",
        "| method | temperature shift plus scaled residual projection, targets built from the matched full-size curve, then "
        "gradient-boosted trees over 37 input variables | one published geometry normalization and one published temperature "
        "correction, both functions of the smaller specimen's own dimensions only |",
        "| headline | R^2 0.942 (USE) and 0.892 (DBTT); better than the analytical methods they benchmarked | "
        f"a residual size-correction scale of {np.std(fam_means, ddof=1):.1f} \u00b0C from {n_fam} families, and the finding "
        "that no single geometry has enough matched evidence to support its own correction |",
        "",
        "**Overlap:** the same published dataset, the same size-effect problem, the same tanh curve description, and largely the "
        "same matched sub-population (their refs 5, 40-42 are this dataset's refs 52, 53, 55, 59).",
        "",
        "**Difference that matters for the uncertainty.** Their transformation builds each training target from the paired "
        "full-size curve (their Eqs 5-7: shift by DBTT_f - DBTT_s, scale residuals by USE_f/USE_s). That is legitimate and "
        "necessary for supervised learning, and their cross-validation correctly holds out whole specimen sets, so their R^2 is "
        "an honest measure of PREDICTION accuracy. It is not, and is not claimed by them to be, an independent estimate of how "
        "much uncertainty a classical correction adds. This project needs that second quantity, so its correction is not allowed "
        "to see the paired full-size curve at all.",
        "",
        "**No novelty is claimed beyond this.** Their analytical benchmarks are a larger and more systematic comparison of "
        "classical methods than anything here. What this work adds is a strictly matched, fully audited pairing, an out-of-sample "
        "correction, an explicit residual-uncertainty estimate with its evidence status, and a statement of where the dataset is "
        "too thin to support one. This project trains no model and does not attempt prediction.",
        "",
        "## 14. Three uncertainties that are not the same thing (D-082)",
        "",
        "1. **Per-curve fit uncertainty (WP4).** How well one curve's own T41J is pinned down by its own specimens: median "
        "pairs-bootstrap SD 4.9 \u00b0C over the 66 full-size curves with a primary interval.",
        f"2. **Size-correction residual disagreement (WP5).** The spread of DT_size across matched comparisons after the "
        f"classical correction: family-weighted SD {np.std(fam_means, ddof=1):.1f} \u00b0C. **This is what WP6 needs, and it is "
        f"about {np.std(fam_means, ddof=1) / 4.9:.1f} times the per-curve fit uncertainty.**",
        "3. **Between-material and between-study variation.** Differences among matched families, which here cannot be separated "
        "from (2): each DT_size is a difference of two independently fitted curves, and a 109-publication compilation carries "
        "laboratory, machine, calibration and digitization differences (brief §3).",
        "",
        "No WP4 interval width is used as a size penalty, and no variance deconvolution is attempted: the WP4 intervals are "
        "nominal rather than calibrated (D-056), so subtracting their variance from the residual variance would be a false "
        "precision (D-082).",
        "",
        "## 15. What WP6 is handed",
        "",
        md_table(hand[[c for c in hand.columns if c not in ("data_type", "scale_definition")]]),
        "",
        "Scale definition: " + hand["scale_definition"].dropna().iloc[0],
        "",
        "## 16. Limitations",
        "",
        f"1. **Very few independent matched families.** {n_fam} in the primary set, {strict['family_id'].nunique()} in total. "
        "Every summary statistic here rests on single digits.",
        "2. **Comparisons within a family are not independent.** Ref 59 alone contributes 5 of the 10 matched families and "
        "9 of the 18 STRICT comparisons; every summary is therefore given family-weighted as well as comparison-weighted.",
        "3. **No heat or lot identifier anywhere in the dataset.** The reported composition is the only heat proxy, which is "
        "what empties the cross-study class and confines the analysis to five publications.",
        "4. **Cross-study heterogeneity.** 109 source publications, different machines, calibrations and reporting conventions; "
        "most of these curves are digitized from published figures (WebPlotDigitizer, per the descriptor).",
        "5. **No shear-fracture data at all**, so the fracture-mode-dependent procedure that NUREG/CR-6379 actually recommends "
        "cannot be run, and a single scalar factor must serve a curve that spans brittle and ductile fracture.",
        f"6. **Geometry applicability.** {n_typed} of the {n_mini} miniature geometries are one of the four specimen types "
        f"NUREG/CR-6379 built; the other {n_mini - n_typed} rely on Eq. (22)'s own statement that its form may be used as "
        "guidance beyond those four types, with its caveat that deviations reflect notch-constraint effects the formula does "
        "not contain.",
        f"7. **The 200 J upper-shelf limit is exceeded.** {int(primary['full_size_use_above_200J'].sum())} of {len(primary)} "
        "primary comparisons have a full-size USE above the 200 J limit NUREG/CR-6379 sets on its upper-shelf analysis; they are "
        "flagged, not dropped.",
        "8. **WP3 fit quality.** 8 of 18 STRICT comparisons are held out of the primary set because either the full-size fit or "
        "the transformed refit is weakly identified or boundary-limited; the held set is more scattered than the primary set, "
        "which is itself a warning that the primary set is the better-behaved subset rather than a random one.",
        "9. **WP4 interval limitations.** The full-size T41J intervals carried here are nominal 95 % percentile bootstrap "
        "intervals with known calibration limits (D-056), and 54 of 134 full-size curves have no reportable interval at all.",
        "10. **Product-form and irradiation imbalance.** Weld metal is one family from one publication; forging is two families; "
        "irradiated is two families. None supports a standalone estimate.",
        "11. **Scalar normalization cannot capture constraint.** Section 11 above.",
    ]
    (WP5 / "wp5_summary.md").write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# 9. Driver
# ---------------------------------------------------------------------------
def main() -> None:
    WP5.mkdir(parents=True, exist_ok=True)
    checks = pd.DataFrame(N.self_checks())          # D-086 checks 1-6; raises on failure

    curves = curve_table()                          # verifies the CP2 freeze before reading anything
    records = pd.read_csv(PROCESSED / "primary" / "charpy_records_with_curves.csv", low_memory=False)
    records = records[records["curve_id"].isin(set(curves["curve_id"]))]
    points = {cid: (g["test_temp_c"].to_numpy(float), g["energy_j"].to_numpy(float))
              for cid, g in records.groupby("curve_id")}

    wp4 = pd.read_csv(OUTPUTS / "wp4" / "t41j_uncertainty_full_size.csv")[
        ["curve_id", "pairs_interval_label", "pairs_sd", "pairs_interval_width", "pairs_finite_target_fraction"]]
    wp4 = wp4.rename(columns={c: f"full_size_wp4_{c}" for c in wp4.columns if c != "curve_id"}).set_index("curve_id")

    pairs = pd.read_csv(WP5 / "strict_matched_family_inventory.csv")
    if pairs.empty:
        raise RuntimeError("no STRICT matched pairs: run src/wp5_pairs.py first")

    geo = geometry_table(curves)
    geo.to_csv(WP5 / "geometry_normalization_factors.csv", index=False)
    checks.to_csv(WP5 / "normalization_self_checks.csv", index=False)
    write_method_configuration(geo, checks)

    res, mapped = run_comparisons(pairs, curves, points)
    res["in_primary_analysis_set"] = in_primary_set(res)
    res = res.join(wp4, on="full_size_curve_id")      # WP4 labels carried for reporting only, never used as a size penalty (D-082)
    res.to_csv(WP5 / "matched_pair_fit_results.csv", index=False)
    mapped.to_csv(WP5 / "normalized_curve_points.csv", index=False)

    # D-086 check 8: recompute the factors from geometry alone and require an exact match with what was applied.
    idx = curves.set_index("curve_id")
    for r in res[res["mapped"]].itertuples(index=False):
        s = idx.loc[r.smaller_curve_id]
        case = CASES[r.case]
        g = N.geometry(s["length_mm"], s["width_mm"], s["thickness_mm"], s["notch_depth_mm"], apply_klst_correction=case["klst"])
        if not (np.isclose(N.ENERGY_METHODS[case["energy"]](g), r.nf_energy, rtol=0, atol=1e-12)
                and np.isclose(N.TEMPERATURE_METHODS[case["temperature"]](g), r.shift_c, rtol=0, atol=1e-12)):
            raise RuntimeError(f"leakage check failed for {r.pair_id} ({r.case}): the applied factors are not reproducible "
                               "from the smaller specimen's geometry alone")

    primary_case = res[res["case"] == PRIMARY_CASE]
    primary = primary_case[primary_case["in_primary_analysis_set"]].copy()
    held = primary_case[~primary_case["in_primary_analysis_set"]].copy()
    primary_case.to_csv(WP5 / "size_correction_residuals.csv", index=False)

    overall = pd.DataFrame(summary_block(primary, "PRIMARY analysis set")
                           + summary_block(primary_case[primary_case["delta_t_size_c"].notna()],
                                           "all STRICT comparisons with a residual (primary + held as sensitivity)"))
    overall.to_csv(WP5 / "size_correction_summary_overall.csv", index=False)
    by_form = stratified(primary, "product_form", "product form")
    by_form.to_csv(WP5 / "size_correction_summary_by_product_form.csv", index=False)
    by_geom = stratified(primary, "smaller_geometry", "geometry")
    by_geom.to_csv(WP5 / "size_correction_summary_by_geometry.csv", index=False)
    by_irr = stratified(primary.assign(irradiation=np.where(primary["irradiated"], "irradiated", "unirradiated")),
                        "irradiation", "irradiation state")
    by_irr.to_csv(WP5 / "size_correction_summary_by_irradiation.csv", index=False)

    ba = before_after(primary, curves, points)
    ba.to_csv(WP5 / "before_after_normalization_metrics.csv", index=False)

    # Sensitivity comparison: the same comparisons under every pre-declared case (D-075).
    keep = set(primary["pair_id"])
    sens_rows = []
    for case_name in CASES:
        g = res[(res["case"] == case_name) & res["pair_id"].isin(keep) & res["delta_t_size_c"].notna()]
        fam = g.groupby("family_id")["delta_t_size_c"].mean()
        sens_rows.append(dict(case=case_name, label=CASES[case_name]["label"], n_comparisons=len(g), n_families=len(fam),
                              mean_c=g["delta_t_size_c"].mean() if len(g) else np.nan,
                              median_c=g["delta_t_size_c"].median() if len(g) else np.nan,
                              mae_c=g["delta_t_size_c"].abs().mean() if len(g) else np.nan,
                              rmse_c=float(np.sqrt(np.mean(g["delta_t_size_c"] ** 2))) if len(g) else np.nan,
                              family_weighted_mean_c=float(fam.mean()) if len(fam) else np.nan,
                              family_weighted_sd_c=float(np.std(fam, ddof=1)) if len(fam) >= 2 else np.nan,
                              min_c=g["delta_t_size_c"].min() if len(g) else np.nan,
                              max_c=g["delta_t_size_c"].max() if len(g) else np.nan))
    sens = pd.DataFrame(sens_rows)
    s7 = sokolov_per_type(pairs[pairs["pair_id"].isin(keep)], curves, points, primary)
    s7.to_csv(WP5 / "sokolov_per_type_shift_comparison.csv", index=False)
    sens.to_csv(WP5 / "normalization_sensitivity_comparison.csv", index=False)

    hand = handoff(primary, primary_case, geo, curves)
    hand.to_csv(WP5 / "wp6_size_correction_handoff.csv", index=False)

    fig_inventory(pairs, curves, WP5 / "matched_pair_inventory.png")
    fig_before_after(primary, curves, points, mapped, WP5 / "before_after_normalization.png")
    fig_residuals(primary, held, curves, WP5 / "size_correction_residuals.png")
    fig_performance(ba, WP5 / "normalization_performance.png")

    write_summary(res, primary, held, overall, by_form, by_geom, by_irr, ba, sens, hand, geo, s7)
    print(f"WP5 size effect: {len(primary_case)} STRICT comparisons, {len(primary)} in the primary analysis set "
          f"({primary['family_id'].nunique()} families, {primary['study_ref_id'].nunique()} publications)")
    print(f"  DT_size comparison-weighted: mean {primary['delta_t_size_c'].mean():+.1f} deg C, "
          f"median {primary['delta_t_size_c'].median():+.1f}, MAE {primary['delta_t_size_c'].abs().mean():.1f}, "
          f"range {primary['delta_t_size_c'].min():+.1f} to {primary['delta_t_size_c'].max():+.1f}")
    print(f"Wrote outputs/wp5/ results, figures and wp5_summary.md")


if __name__ == "__main__":
    main()
