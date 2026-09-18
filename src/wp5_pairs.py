"""WP5 (1 of 2) - Specimen-size pair inventory and data-sufficiency assessment.

This script runs BEFORE any size normalization exists. Its only job is to answer, from provenance alone:
*which published smaller-specimen curves and full-size curves describe the same material in the same condition?*
Match quality is decided here, from metadata, and is never revised after looking at how well a normalization works
(PROJECT_BRIEF.md §7; DECISIONS.md D-068, D-069).

Inputs (all read-only):
  outputs/wp2/cohort_membership.csv, outputs/wp2/curve_inventory.csv   the CP2-frozen primary cohort (D-039)
  data/processed/primary/charpy_records_with_curves.csv                 the cleaned records
  outputs/wp3/fits_primary.csv                                          the CP3-approved point fits
  outputs/wp4/*                                                         the WP4 interval labels, carried for reporting only

Outputs (outputs/wp5/):
  candidate_pair_inventory.csv      every ordered (smaller geometry, full-size) curve pair with its field-by-field comparison
  strict_matched_family_inventory.csv / partial_match_inventory.csv     the two matched classes, by material-condition family
  unmatched_reason_summary.csv      why the rest were rejected
  pair_data_sufficiency.md          the Section E gate: counts, dependence and the explicit sufficiency verdict

Run:  .venv/bin/python src/wp5_pairs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUTPUTS, PROCESSED, md_table  # noqa: E402
from wp2_curves import COMPOSITION_FIELDS  # noqa: E402
from wp3_fit_curves import check_frozen_cohorts  # noqa: E402

WP5 = OUTPUTS / "wp5"

# ---------------------------------------------------------------------------
# 1. What must agree before two curves are called the same material and condition (D-068)
# ---------------------------------------------------------------------------
# Ordered by how badly a disagreement would confound a specimen-size comparison; the FIRST disagreeing field is the
# recorded rejection reason, so unmatched_reason_summary.csv reads as a priority list.
#
# `label` is what the reason string says. `critical` fields are the ones whose value must be present on both sides for a
# STRICT match: a blank on one side only means the provenance does not establish the match, and the pair is PARTIAL.
MATCH_FIELDS = [
    ("material_family", "material family", True),
    ("material_std", "material designation (specification, type/grade, class, weld-metal label)", True),
    ("product_form", "product form", True),
    ("composition_signature", "heat chemistry (the heat/lot proxy; the dataset has no heat identifier)", True),
    ("irradiated_resolved", "irradiation status", True),
    ("fluence_n_per_cm2", "fluence", True),
    ("irradiation_temp_c", "irradiation temperature", False),
    ("irradiation_time_h", "irradiation time", False),
    ("treatment", "heat treatment", False),
    ("post_treatment_temp_c", "post-treatment temperature", False),
    ("post_treatment_time_h", "post-treatment time", False),
    ("cooling_method", "cooling method", False),
    ("cooling_rate_c_per_min", "cooling rate", False),
    ("test_condition_statement", "test-condition statement (HAZ location, reconstituted, welded area, striking velocity)", True),
    ("tag_reconstituted_specimen", "reconstituted-specimen status", True),
    ("orientation", "specimen orientation", False),
]
# Orientation is not `critical` because the dataset leaves it blank for whole publications (refs 55, 60), which is a
# reporting gap, not a conflict. A recorded DISAGREEMENT in orientation still rejects the pair, like any other field.

AGREE, MISSING, CONFLICT = "agree", "one side not reported", "conflict"

# Match classes, fixed before any normalization result exists (D-069).
STRICT = "STRICT (same study, no conflict, no one-sided gap)"
PARTIAL = "PARTIAL (same study, no conflict, provenance gap)"
CROSS = "CROSS-STUDY (no recorded conflict, different publication)"
NOT_MATCHED = "NOT MATCHED (a recorded field disagrees)"


def compare(a, b) -> str:
    """AGREE / MISSING / CONFLICT for one field of two curves. Both blank counts as AGREE: within one publication it means the
    publication reported the field for neither curve, which is consistent, not contradictory."""
    a_blank = a is None or (isinstance(a, float) and np.isnan(a)) or (isinstance(a, str) and a.strip() == "")
    b_blank = b is None or (isinstance(b, float) and np.isnan(b)) or (isinstance(b, str) and b.strip() == "")
    if a_blank and b_blank:
        return AGREE
    if a_blank or b_blank:
        return MISSING
    if isinstance(a, float) and isinstance(b, float):
        return AGREE if np.isclose(a, b, rtol=0, atol=1e-9) else CONFLICT
    return AGREE if str(a).strip() == str(b).strip() else CONFLICT


# ---------------------------------------------------------------------------
# 2. Curve-level table
# ---------------------------------------------------------------------------
def curve_table() -> pd.DataFrame:
    """One row per curve of the CP2-frozen primary cohort, with every field the pair matching needs and the WP3 fit."""
    members = check_frozen_cohorts()
    primary = members.loc[members["cohort"] == "primary", "curve_id"].tolist()

    records = pd.read_csv(PROCESSED / "primary" / "charpy_records_with_curves.csv", low_memory=False)
    records = records[records["curve_id"].isin(primary)].copy()
    records["composition_signature"] = records[COMPOSITION_FIELDS].round(6).astype(str).agg("|".join, axis=1)

    fields = [f for f, _, _ in MATCH_FIELDS] + [
        "ref_id", "length_mm", "width_mm", "thickness_mm", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm",
    ]
    grouped = records.groupby("curve_id")
    for f in fields:
        if f not in records.columns:
            raise KeyError(f"field {f!r} is not in the processed records")
        n_values = grouped[f].nunique(dropna=False)
        if (n_values > 1).any():
            bad = n_values[n_values > 1].index.tolist()
            raise RuntimeError(f"field {f!r} is not constant within curves {bad}: the WP2 curve key should make it constant")

    curves = grouped[fields].first().reset_index()
    inv = pd.read_csv(OUTPUTS / "wp2" / "curve_inventory.csv", low_memory=False)
    curves = curves.merge(inv[["curve_id", "ref_id", "ref_year", "geometry", "geometry_class", "product_form_group",
                               "n_points", "n_temperatures", "T_min_c", "T_max_c", "E_min_j", "E_max_j"]],
                          on=["curve_id", "ref_id"], how="left", validate="1:1")

    fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv")
    keep = ["curve_id", "geometry_category", "outcome", "outcome_reason", "index_temperature_c", "index_status", "index_support",
            "index_empirical_bracketing", "flag_index_near_fitted_shelf", "flag_index_not_bracketed_by_measured_energy",
            "flag_full_size_notch_dimensions_unreported", "notch_reported", "lse_j", "use_j", "t0_c", "c_c", "use_support"]
    curves = curves.merge(fits[keep], on="curve_id", how="left", validate="1:1")
    if curves["outcome"].isna().any():
        raise RuntimeError("some primary-cohort curves have no WP3 fit row")

    curves["wp3_usable"] = curves["outcome"].str.startswith("usable fit")
    return curves


# ---------------------------------------------------------------------------
# 3. Candidate pairs
# ---------------------------------------------------------------------------
def candidate_pairs(curves: pd.DataFrame) -> pd.DataFrame:
    """Every ordered (smaller-geometry curve, full-size curve) pair in the frozen primary cohort, classified.

    All of them are enumerated, not a pre-filtered shortlist, so that every rejection is auditable and the reason summary is
    complete (PROJECT_BRIEF.md §7: nothing leaves without a stated reason)."""
    small = curves[curves["geometry_category"] != "full-size"]
    full = curves[curves["geometry_category"] == "full-size"]

    rows = []
    for s in small.itertuples(index=False):
        for f in full.itertuples(index=False):
            outcome, first_conflict, first_missing = {}, None, None
            for field, label, critical in MATCH_FIELDS:
                verdict = compare(getattr(s, field), getattr(f, field))
                outcome[f"cmp_{field}"] = verdict
                if verdict == CONFLICT and first_conflict is None:
                    first_conflict = label
                if verdict == MISSING and critical and first_missing is None:
                    first_missing = label
            same_study = s.ref_id == f.ref_id

            if first_conflict is not None:
                match_class, reason = NOT_MATCHED, f"recorded disagreement in {first_conflict}"
            elif not same_study:
                match_class, reason = CROSS, "no recorded disagreement, but the two curves come from different publications"
            elif first_missing is not None:
                match_class, reason = PARTIAL, f"same publication, but {first_missing} is reported for only one of the two curves"
            else:
                match_class, reason = STRICT, "same publication; every compared material and condition field agrees"

            rows.append(dict(
                pair_id=f"{s.curve_id}|{f.curve_id}",
                smaller_curve_id=s.curve_id, full_size_curve_id=f.curve_id,
                smaller_ref_id=s.ref_id, full_size_ref_id=f.ref_id, same_study=same_study,
                smaller_geometry=s.geometry, full_size_geometry=f.geometry,
                material_std=s.material_std, product_form_smaller=s.product_form, product_form_full=f.product_form,
                irradiated_smaller=s.irradiated_resolved, irradiated_full=f.irradiated_resolved,
                fluence_smaller=s.fluence_n_per_cm2, fluence_full=f.fluence_n_per_cm2,
                match_class=match_class, match_reason=reason,
                smaller_wp3_outcome=s.outcome, full_size_wp3_outcome=f.outcome,
                smaller_wp3_usable=s.wp3_usable, full_size_wp3_usable=f.wp3_usable,
                full_size_t41j_c=f.index_temperature_c, full_size_index_status=f.index_status,
                smaller_n_points=s.n_points, full_size_n_points=f.n_points,
                **outcome))
    return pd.DataFrame(rows)


def family_id(row) -> str:
    """A matched material-condition family: one publication, one material designation, one product form, one heat chemistry,
    one irradiation condition, one test-condition statement. Several smaller geometries of one family are NOT independent
    material observations, which is why families, not pairs, are the unit of independence (D-070)."""
    fluence = "unirradiated" if not row["irradiated_full"] or pd.isna(row["fluence_full"]) else f"{row['fluence_full']:.3g} n/cm2"
    return f"R{row['full_size_ref_id']}-{row['full_size_curve_id']}-{fluence}"


# ---------------------------------------------------------------------------
# 4. Data-sufficiency assessment (PROJECT_BRIEF.md §5 WP5: say so immediately if the pairs are too few)
# ---------------------------------------------------------------------------
def sufficiency(pairs: pd.DataFrame, curves: pd.DataFrame) -> tuple:
    pairs["both_wp3_usable"] = pairs["smaller_wp3_usable"] & pairs["full_size_wp3_usable"]
    matched = pairs[pairs["match_class"].isin([STRICT, PARTIAL])].copy()
    matched["family_id"] = matched.apply(family_id, axis=1)

    def block(df: pd.DataFrame, name: str) -> dict:
        if df.empty:
            return dict(subset=name, comparisons=0, families=0, studies=0, heats=0, geometry_combinations=0,
                        both_wp3_usable=0, product_forms="", irradiation_states="")
        return dict(
            subset=name,
            comparisons=len(df),
            families=df["family_id"].nunique(),
            studies=df["full_size_ref_id"].nunique(),
            heats=df[["full_size_ref_id", "material_std", "product_form_full"]].drop_duplicates().shape[0],
            geometry_combinations=df["smaller_geometry"].nunique(),
            both_wp3_usable=int(df["both_wp3_usable"].sum()),
            product_forms="; ".join(f"{k}: {v}" for k, v in sorted(df["product_form_full"].value_counts().items())),
            irradiation_states="; ".join(f"{'irradiated' if k else 'unirradiated'}: {v}"
                                         for k, v in sorted(df["irradiated_full"].value_counts().items())),
        )

    strict = matched[matched["match_class"] == STRICT]
    usable = strict[strict["both_wp3_usable"]]
    table = pd.DataFrame([
        block(strict, "STRICT matches"),
        block(matched[matched["match_class"] == PARTIAL], "PARTIAL matches"),
        block(matched, "STRICT + PARTIAL"),
        block(usable, "STRICT and both WP3 fits usable (candidate PRIMARY analysis set)"),
    ])

    per_family = (matched.groupby(["match_class", "family_id"])
                  .agg(comparisons=("pair_id", "size"),
                       smaller_geometries=("smaller_geometry", lambda v: "; ".join(sorted(set(v)))),
                       study=("full_size_ref_id", "first"),
                       material=("material_std", "first"),
                       product_form=("product_form_full", "first"),
                       irradiated=("irradiated_full", "first"),
                       fluence_n_per_cm2=("fluence_full", "first"),
                       full_size_curve=("full_size_curve_id", "first"),
                       full_size_wp3_outcome=("full_size_wp3_outcome", "first"),
                       full_size_t41j_c=("full_size_t41j_c", "first"),
                       smaller_curves=("smaller_curve_id", lambda v: "; ".join(sorted(set(v)))),
                       comparisons_both_wp3_usable=("both_wp3_usable", "sum"))
                  .reset_index().sort_values(["match_class", "family_id"]))

    reasons = (pairs.groupby(["match_class", "match_reason"]).size().rename("pairs").reset_index()
               .sort_values(["match_class", "pairs"], ascending=[True, False]))
    return matched, table, per_family, reasons


def unpartnered(curves: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    """Smaller-specimen curves with no STRICT full-size partner, and why. Naming them keeps the losses visible: a geometry can be
    absent from the size analysis because its study published no full-size curve, because the full-size copy was removed as a
    republication at WP1 step E8 (D-019), or because a material or condition field disagrees."""
    strict_small = set(pairs.loc[pairs["match_class"] == STRICT, "smaller_curve_id"])
    e8 = pd.read_csv(OUTPUTS / "wp1" / "duplicate_curve_removals.csv")
    e8["removed_full_size"] = e8["removed_unit"].astype(str).str.contains("|55.0|10.0|10.0|", regex=False)
    e8["removed_ref"] = e8["removed_ref"].astype(str)
    small = curves[(curves["geometry_category"] != "full-size") & (~curves["curve_id"].isin(strict_small))]
    rows = []
    for c in small.itertuples(index=False):
        same_study_full = pairs[(pairs["smaller_curve_id"] == c.curve_id) & pairs["same_study"]]
        if same_study_full.empty:
            why = "the publication contributes no full-size curve to the frozen primary cohort"
            removed = e8[(e8["removed_ref"] == str(c.ref_id)) & e8["removed_full_size"]]
            if len(removed):
                why += (f" (its full-size curves left at WP1 step E8 as republications of ref "
                        + "/".join(sorted(set(removed["kept_ref"].astype(str)))) + "'s tests, D-019)")
        else:
            why = "; ".join(sorted(set(same_study_full["match_reason"])))
        rows.append(dict(curve_id=c.curve_id, ref_id=c.ref_id, geometry=c.geometry, material_std=c.material_std,
                         product_form=c.product_form, irradiated=c.irradiated_resolved, n_points=c.n_points,
                         wp3_outcome=c.outcome, same_study_full_size_candidates=len(same_study_full),
                         reason_no_strict_partner=why))
    return pd.DataFrame(rows)


def write_report(curves, pairs, matched, table, per_family, unmatched_small) -> None:
    strict = matched[matched["match_class"] == STRICT]
    usable = strict[strict["both_wp3_usable"]]
    small = curves[curves["geometry_category"] != "full-size"]

    geo = (small.groupby("geometry")
           .agg(curves=("curve_id", "size"), studies=("ref_id", "nunique"))
           .reset_index())
    matched_by_geo = strict.groupby("smaller_geometry").agg(strict_comparisons=("pair_id", "size"),
                                                            families=("family_id", "nunique")).reset_index()
    geo = geo.merge(matched_by_geo, left_on="geometry", right_on="smaller_geometry", how="left").drop(columns="smaller_geometry")
    geo[["strict_comparisons", "families"]] = geo[["strict_comparisons", "families"]].fillna(0).astype(int)

    lines = [
        "# WP5 - specimen-size pair inventory and data sufficiency",
        "",
        "Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort "
        f"({curves.shape[0]} curves). Every row here describes PUBLISHED MEASURED DATA and FITTED PARAMETERS from it; nothing is "
        "normalized or transformed in this file. Pair matching rules: DECISIONS.md D-068; match classes: D-069; families: D-070.",
        "",
        "**This inventory was produced before any size-normalization result existed.** Match classes are decided from provenance "
        "metadata alone and are not revised after seeing how well a normalization works.",
        "",
        "## 1. What had to agree",
        "",
        "Two curves are treated as the same material and condition measured at two specimen geometries only if every field below "
        "agrees. A field blank on both sides counts as agreement (the publication reported it for neither curve); a field blank on "
        "one side only is a provenance gap; a recorded disagreement rejects the pair.",
        "",
        md_table(pd.DataFrame([dict(field=f, meaning=label, **{"required present for STRICT": "yes" if c else "no"})
                               for f, label, c in MATCH_FIELDS])),
        "",
        "## 2. Candidate pairs and why they were rejected",
        "",
        f"All {len(pairs)} ordered (smaller-geometry curve, full-size curve) pairs of the frozen primary cohort were enumerated "
        f"({len(small)} smaller-specimen curves x {(curves['geometry_category'] == 'full-size').sum()} full-size curves).",
        "",
        md_table(pairs.groupby("match_class").size().rename("pairs").reset_index()),
        "",
        "## 3. How much matched evidence there is",
        "",
        md_table(table),
        "",
        "## 4. Independence: comparisons are not independent material observations",
        "",
        "One full-size curve paired with several smaller geometries gives several comparisons of ONE material in ONE condition. "
        "The family is the unit of independence.",
        "",
        md_table(per_family[per_family["match_class"] == STRICT].drop(columns="match_class")),
        "",
        "## 5. Smaller-specimen geometries: how many reach a matched full-size partner",
        "",
        md_table(geo),
        "",
        "## 5b. Smaller-specimen curves with no STRICT full-size partner",
        "",
        md_table(unmatched_small),
        "",
        "## 6. Sufficiency verdict",
        "",
        f"- STRICT matched geometry comparisons: **{len(strict)}**, from **{strict['family_id'].nunique()}** independent "
        f"material-condition families in **{strict['full_size_ref_id'].nunique()}** publications.",
        f"- Of those, **{len(usable)}** comparisons ({usable['family_id'].nunique()} families) have a usable WP3 fit on BOTH curves.",
        f"- Smaller-specimen geometries represented among STRICT comparisons: **{strict['smaller_geometry'].nunique()}** of "
        f"{small['geometry'].nunique()} in the cohort.",
        f"- Product forms among STRICT families: "
        + "; ".join(f"{k} ({v})" for k, v in sorted(strict.drop_duplicates('family_id')['product_form_full'].value_counts().items()))
        + ".",
        f"- Irradiation states among STRICT families: "
        + "; ".join(f"{'irradiated' if k else 'unirradiated'} ({v})"
                    for k, v in sorted(strict.drop_duplicates('family_id')['irradiated_full'].value_counts().items()))
        + ".",
        "",
        "The size-correction analysis proceeds on this evidence, and every summary it produces is reported with these counts "
        "beside it. Whether the counts support a general size-correction uncertainty is answered in `wp5_summary.md` against the "
        "pre-registered evidence thresholds of DECISIONS.md D-079.",
    ]
    (WP5 / "pair_data_sufficiency.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    WP5.mkdir(parents=True, exist_ok=True)
    curves = curve_table()          # check_frozen_cohorts() runs inside, before anything is read

    pairs = candidate_pairs(curves)
    matched, table, per_family, reasons = sufficiency(pairs, curves)

    pairs.insert(0, "data_type", "PUBLISHED MEASURED DATA (provenance comparison only; nothing normalized)")
    pairs.to_csv(WP5 / "candidate_pair_inventory.csv", index=False)
    matched[matched["match_class"] == STRICT].assign(family_id=matched["family_id"]).to_csv(
        WP5 / "strict_matched_family_inventory.csv", index=False)
    matched[matched["match_class"] == PARTIAL].to_csv(WP5 / "partial_match_inventory.csv", index=False)
    reasons.to_csv(WP5 / "unmatched_reason_summary.csv", index=False)
    unmatched_small = unpartnered(curves, pairs)
    unmatched_small.to_csv(WP5 / "smaller_curves_without_matched_partner.csv", index=False)
    per_family.to_csv(WP5 / "matched_family_summary.csv", index=False)
    table.to_csv(WP5 / "pair_data_sufficiency.csv", index=False)
    write_report(curves, pairs, matched, table, per_family, unmatched_small)

    strict = matched[matched["match_class"] == STRICT]
    print(f"WP5 pair inventory: {len(pairs)} candidate pairs; "
          f"{len(strict)} STRICT comparisons in {strict['family_id'].nunique()} families; "
          f"{(matched['match_class'] == PARTIAL).sum()} PARTIAL; "
          f"{(pairs['match_class'] == CROSS).sum()} cross-study; {(pairs['match_class'] == NOT_MATCHED).sum()} not matched")
    print(f"Wrote {WP5.relative_to(OUTPUTS.parent)}/ pair inventory and sufficiency report")


if __name__ == "__main__":
    main()
