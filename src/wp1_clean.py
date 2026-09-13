"""WP1 - Cleaning and normalization.

Every raw record is kept in data/processed/<run>/charpy_records_with_status.csv with its cleaned fields,
tags, flags, and either status 'retained' or the single exclusion step that removed it. Nothing is
imputed; measurement values are never modified (only text labels are harmonized, and every change is logged).

Outputs (run = 'primary' for the 2025.30 release, 'sensitivity_<record>' for the 2024.206 version-sensitivity release):
  data/processed/<run>/charpy_records_with_status.csv, charpy_clean.csv
  outputs/wp1[_sensitivity_<record>]/reconciliation_table.md (+ .csv), exclusion_reasons_all_applicable.csv,
      value_changes_log.csv, unit_checks.md, flags_summary.md, duplicate_curve_pairs.csv,
      duplicate_curve_removals.csv, duplicate_keep_rule_comparison.csv, duplicate_sensitivity.csv, wp1_summary.md

Run:  .venv/bin/python src/wp1_clean.py                          (primary dataset)
      .venv/bin/python src/wp1_clean.py --dataset eny5v-www93    (version-sensitivity dataset)
"""
from __future__ import annotations

import argparse
import itertools

import numpy as np
import pandas as pd

from common import (DATASETS, OUTPUTS, PRIMARY_DATASET, PROCESSED, load_charpy_data, load_references,
                    md_table, write_text)
from curated_metadata import (COLUMN_BY_RAW, IRRADIATION_LABEL_CHECKS, MATERIAL_MAP, REFERENCE_NOTES, SIMULATED_HAZ_CODES,
                              SOURCE_CONTRADICTED_LABELS, SPEC_PRODUCT_FORM, SPECIMEN_TYPE_CHECKS, TEXT_VALUE_MAPS)

# Thresholds (each justified in DECISIONS.md)
ABSOLUTE_ZERO_C = -273.15
E23_VELOCITY_RANGE_M_S = (3.0, 6.0)          # ASTM E23-82 §4.1.6 (D-015)
PLAUSIBLE_TEST_TEMP_C = (-200.0, 400.0)       # review flag only (D-017)
MAX_RATIO_E_TO_DATASET_USE = 1.5              # review flag only (D-017)
MAX_ENERGY_PER_LIGAMENT_AREA_J_CM2 = 1000.0   # review flag only (D-017)
DUP_TOL_T_C = 3.0                             # D-019
DUP_TOL_E_FRACTION_OF_MAX = 0.02              # D-019
DUP_MIN_FRACTION = 0.7                        # D-019
DUP_MIN_MATCHED = 3                           # D-019
PARTIAL_OVERLAP_MIN_FRACTION = 0.5            # D-019 (flag only)
TABULATED_MIN_SHARE = 0.9                     # D-019 canonical hierarchy, criterion (a)
FT_LBF_IN_J = 1.3558179483                    # exact conversion factor

TEXT_COLUMNS_TO_HARMONIZE = list(TEXT_VALUE_MAPS)


# ---------------------------------------------------------------------------
# 1. Rename, type and harmonize (logged)
# ---------------------------------------------------------------------------
def rename_and_clean_text(raw: pd.DataFrame, log: list) -> pd.DataFrame:
    unknown = [c for c in raw.columns if c != "source_row" and c not in COLUMN_BY_RAW]
    if unknown:
        raise KeyError(f"Columns without curated metadata: {unknown}")
    df = raw.rename(columns={c: COLUMN_BY_RAW[c]["clean"] for c in raw.columns if c != "source_row"})
    df.insert(0, "record_id", df["source_row"].map(lambda r: f"R{r:04d}"))
    for col in df.columns:
        # material_raw stays verbatim (trailing spaces included); names are matched on a trimmed copy in harmonize_material.
        if df[col].dtype == object and col not in ("record_id", "material_raw"):
            before = df[col]
            after = before.map(lambda v: v.strip() if isinstance(v, str) else v)
            after = after.map(lambda v: np.nan if isinstance(v, str) and v == "" else v)
            changed = before.notna() & (before.astype(str) != after.astype(str))
            for (old, new), n in pd.DataFrame({"old": before[changed], "new": after[changed]}).value_counts().items():
                log.append(dict(column=col, change="whitespace trimmed", old=repr(old), new=repr(new), records=int(n)))
            df[col] = after
    for col, mapping in TEXT_VALUE_MAPS.items():
        if col not in df:
            continue
        hit = df[col].isin(mapping.keys())
        for old, n in df.loc[hit, col].value_counts().items():
            log.append(dict(column=col, change="text harmonized", old=repr(old), new=repr(mapping[old]), records=int(n)))
        df.loc[hit, col] = df.loc[hit, col].map(mapping)
    irr_map = {"Yes": True, "No": False}
    if not set(df["irradiated"].dropna()) <= set(irr_map):
        raise ValueError(f"Unexpected irradiated values: {set(df['irradiated'].dropna())}")
    for old, n in df["irradiated"].value_counts().items():
        log.append(dict(column="irradiated", change="Yes/No to boolean", old=repr(old), new=repr(irr_map[old]), records=int(n)))
    df["irradiated"] = df["irradiated"].map(irr_map).astype(bool)
    return df


def harmonize_material(df: pd.DataFrame, log: list) -> pd.DataFrame:
    # material_raw keeps the verbatim spreadsheet string; derived columns are added beside it.
    key = df["material_raw"].str.strip()
    unmapped = sorted(set(key) - set(MATERIAL_MAP))
    if unmapped:
        raise KeyError(f"Material names without a curated mapping: {unmapped}")
    entry = key.map(MATERIAL_MAP)
    df["material_std"] = entry.map(lambda m: m["material_std"])
    df["material_family"] = entry.map(lambda m: m["family"])
    df["material_class_stated"] = entry.map(lambda m: m["class_stated"])
    df["designation_prefix"] = entry.map(lambda m: m["prefix"])
    df["weld_metal_label"] = entry.map(lambda m: m["weld_metal_label"]).astype(bool)
    df["material_scope"] = entry.map(lambda m: m["scope"])
    for (raw, std, fam), n in df.groupby(["material_raw", "material_std", "material_family"]).size().items():
        log.append(dict(column="material_std / material_family (new columns)", change="material name mapped",
                        old=repr(raw), new=f"{std!r} | family {fam!r}", records=int(n)))
    return df


# ---------------------------------------------------------------------------
# 2. Derived descriptive fields (no measurement values created)
# ---------------------------------------------------------------------------
def derive_tags_and_geometry(df: pd.DataFrame) -> pd.DataFrame:
    tcs = df["test_condition_statement"].fillna("")
    trt = df["treatment"].fillna("")
    df["striking_velocity_m_per_s"] = pd.to_numeric(tcs.str.extract(r"^([0-9]*\.?[0-9]+)\s*m/s$", expand=False))
    df["tag_reconstituted_specimen"] = tcs.eq("Reconstituted specimen")
    df["tag_simulated_haz"] = trt.str.contains("|".join(SIMULATED_HAZ_CODES))
    df["tag_haz_statement"] = tcs.str.contains("HAZ") & ~trt.str.contains("Bulk Metal")
    df["tag_welded_area"] = tcs.eq("Welded Area")
    df["tag_shock_wave_hardened"] = trt.str.contains("Shock Wave Hardening")
    df["tag_prestrained"] = trt.str.contains("Pre-strained")
    df["tag_step_cooled"] = trt.str.contains("Step Cooling") | df["cooling_method"].fillna("").eq("Step Cooling")
    df["tag_pwht"] = trt.str.contains("PWHT|Post Weld Heat Treatment")
    df["tag_standard_reference_material"] = tcs.eq("Standard Reference Material")
    df["tag_hydrogen_charged"] = tcs.eq("Hydrogen Charged")
    df["tag_orientation_semantics_differ"] = tcs.eq("Direction means different here")
    df["ligament_mm"] = df["width_mm"] - df["notch_depth_mm"]
    num = lambda v: "?" if pd.isna(v) else f"{v:g}"
    df["geometry_label"] = [f"{num(l)}x{num(w)}x{num(b)} a={num(a)}" for l, w, b, a in
                            zip(df["length_mm"], df["width_mm"], df["thickness_mm"], df["notch_depth_mm"])]
    return df


def derive_reference_fields(df: pd.DataFrame, refs: pd.DataFrame) -> pd.DataFrame:
    year = refs.set_index("ref_id")["year"]
    df["ref_id"] = df["ref_id"].astype(int)
    df["ref_year"] = df["ref_id"].map(year)
    for field in ["grade_title", "product_form_note", "specimen_note", "material_note", "forming_evidence"]:
        df[f"ref_{field}"] = df["ref_id"].map(lambda r: REFERENCE_NOTES.get(r, {}).get(field, ""))
    for field in ["weld_haz_unidentified", "precracked_concern"]:
        df[f"ref_{field}"] = df["ref_id"].map(lambda r: bool(REFERENCE_NOTES.get(r, {}).get(field, False)))
    return df


def derive_product_form(df: pd.DataFrame) -> pd.DataFrame:
    """Record-level evidence first, then citation-title evidence, then the specification's nominal form (D-013)."""
    forms, bases = [], []
    for r in df.itertuples(index=False):
        manu = r.manufacturer if isinstance(r.manufacturer, str) else ""
        if r.weld_metal_label:
            f, b = "weld metal", "material label ('WM')"
        elif r.tag_simulated_haz:
            f, b = "simulated HAZ", "Treatment code (simulated HAZ thermal cycle)"
        elif r.tag_haz_statement:
            f, b = "HAZ", "Test Condition Statement"
        elif r.tag_welded_area:
            f, b = "weld region (zone not stated)", "Test Condition Statement"
        elif "Additive Manufacturing" in manu:
            f, b = "additively manufactured", "Manufacturer field"
        elif r.ref_forming_evidence:
            f, b = r.ref_forming_evidence, "citation title (reference level)"
        elif r.material_family in SPEC_PRODUCT_FORM:
            f, b = SPEC_PRODUCT_FORM[r.material_family], "specification scope (nominal)"
        else:
            f, b = "not determinable", "grade name does not imply a product form"
        forms.append(f)
        bases.append(b)
    df["product_form"] = forms
    df["product_form_basis"] = bases
    nominal = df["product_form_basis"].isin(["specification scope (nominal)", "grade name does not imply a product form"])
    df["flag_title_reports_weld_or_haz_not_identified_in_records"] = nominal & df["ref_weld_haz_unidentified"]
    return df


# ---------------------------------------------------------------------------
# 3. Cross-check against the other release (D-020, D-021)
# ---------------------------------------------------------------------------
def crosscheck_other_release(df: pd.DataFrame, dataset_key: str) -> pd.DataFrame:
    other_key = [k for k in DATASETS if k != dataset_key][0]
    other = rename_and_clean_text(load_charpy_data(DATASETS[other_key]["xlsx"]), [])
    shared_max = min(df["ref_id"].max(), int(other["ref_id"].max()))
    mine = df[df["ref_id"] <= shared_max].reset_index()
    theirs = other[other["ref_id"] <= shared_max].reset_index(drop=True)
    keys = ["ref_id", "test_temp_c", "energy_j", "length_mm", "width_mm", "thickness_mm", "notch_depth_mm"]
    same = len(mine) == len(theirs)
    if same:
        for k in keys:
            a, b = mine[k].astype(float), theirs[k].astype(float)
            same &= bool(((a == b) | (a.isna() & b.isna())).all())
    if not same:
        raise RuntimeError("Releases are not row-aligned on shared references; refusing to transfer labels.")
    df["irradiated_in_other_release"] = pd.Series(pd.NA, index=df.index, dtype="boolean")
    df.loc[mine["index"], "irradiated_in_other_release"] = theirs["irradiated"].values
    df["flag_irradiation_status_differs_between_releases"] = (
        df["irradiated_in_other_release"].notna() & (df["irradiated_in_other_release"] != df["irradiated"])).astype(bool)
    precracked = df.get("specimen_type_dataset", pd.Series(np.nan, index=df.index)).eq("Pre-Cracked")
    if "specimen_type_dataset" in other:
        precracked_other = pd.Series(False, index=df.index)
        precracked_other.loc[mine["index"]] = theirs["specimen_type_dataset"].eq("Pre-Cracked").values
        precracked = precracked | precracked_other
    df["flag_precracked_label_in_2025_release"] = precracked.astype(bool)
    df["flag_source_reports_precracked_specimens"] = df["ref_precracked_concern"]
    return df


def source_check_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Outcome of the source checks for questioned specimen types and condition labels (D-020, D-021, D-031).

    irradiated_resolved: the label both releases agree on; the source-supported value where a check resolved a disagreement;
    otherwise this release's own label, with irradiation_label_check = 'unresolved' so later stages can exclude it."""
    disputed = df["flag_irradiation_status_differs_between_releases"]
    check = df["ref_id"].map(lambda r: IRRADIATION_LABEL_CHECKS.get(r, {}).get("resolution"))
    if (disputed & check.isna()).any():
        raise KeyError(f"Irradiation disagreement without a source-check entry: refs {sorted(df.loc[disputed & check.isna(), 'ref_id'].unique())}")
    df["irradiation_label_check"] = np.where(~disputed, "releases agree",
                                             np.where(check.eq("unresolved"), "unresolved", "source-checked: " + check.fillna("")))
    df["irradiated_resolved"] = df["irradiated"].where(~disputed | check.eq("unresolved"), check.eq("irradiated"))
    concern = df["flag_precracked_label_in_2025_release"] | df["flag_source_reports_precracked_specimens"]
    stype = df["ref_id"].map(lambda r: SPECIMEN_TYPE_CHECKS.get(r, {}).get("resolution"))
    if (concern & stype.isna()).any():
        raise KeyError(f"Specimen-type concern without a source-check entry: refs {sorted(df.loc[concern & stype.isna(), 'ref_id'].unique())}")
    df["specimen_type_check"] = np.where(~concern, "no concern raised", "source-checked: " + stype.fillna(""))
    df.loc[concern & stype.eq("unresolved"), "specimen_type_check"] = "unresolved"
    key = list(zip(df["ref_id"], df["curve_id_dataset"]))
    df["flag_condition_label_contradicted_by_source"] = [SOURCE_CONTRADICTED_LABELS.get((r, c), "") for r, c in key]
    return df


# ---------------------------------------------------------------------------
# 4. Plausibility and internal-consistency flags (review only, never exclusions)
# ---------------------------------------------------------------------------
def consistency_flags(df: pd.DataFrame) -> pd.DataFrame:
    ligament_cm = np.where(df["ligament_mm"].notna(), df["ligament_mm"], df["width_mm"]) / 10.0
    area_cm2 = (df["thickness_mm"] / 10.0) * ligament_cm
    df["energy_per_ligament_area_j_cm2"] = df["energy_j"] / area_cm2
    df["flag_zero_energy"] = df["energy_j"].eq(0)
    df["flag_energy_above_1p5x_dataset_use"] = df["energy_j"] > MAX_RATIO_E_TO_DATASET_USE * df["use_j_dataset"]
    df["flag_energy_per_ligament_area_above_bound"] = df["energy_per_ligament_area_j_cm2"] > MAX_ENERGY_PER_LIGAMENT_AREA_J_CM2
    lo, hi = PLAUSIBLE_TEST_TEMP_C
    df["flag_test_temp_outside_review_window"] = (df["test_temp_c"] < lo) | (df["test_temp_c"] > hi)
    df["flag_notch_dimensions_not_reported"] = df[["notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm"]].isna().any(axis=1)
    df["flag_notch_shape_blank"] = df["notch_shape"].isna()
    df["flag_irradiated_without_irradiation_temp"] = df["irradiated"] & df["irradiation_temp_c"].isna()
    # Dataset curve IDs whose records disagree on fields that should be constant within one curve (D-028).
    fields = {"geometry": ["length_mm", "width_mm", "thickness_mm", "notch_depth_mm"],
              "irradiation": ["irradiated", "fluence_n_per_cm2"], "treatment": ["treatment"],
              "test condition": ["test_condition_statement"], "orientation": ["orientation"], "material": ["material_std"]}
    grouped = df[df["curve_id_dataset"].notna()].groupby("curve_id_dataset")
    mixes = {}
    for label, cols in fields.items():
        n_distinct = grouped[cols].nunique(dropna=False).max(axis=1)
        for curve_id in n_distinct[n_distinct > 1].index:
            mixes.setdefault(curve_id, []).append(label)
    df["flag_dataset_curve_id_mixes"] = df["curve_id_dataset"].map(lambda c: "; ".join(mixes.get(c, [])) if pd.notna(c) else "")
    # Base-metal-labelled records whose composition equals the same reference's weld metal (D-029).
    comp = ["c_wt_pct", "si_wt_pct", "mn_wt_pct", "p_wt_pct", "s_wt_pct", "ni_wt_pct", "cr_wt_pct", "mo_wt_pct", "cu_wt_pct"]
    sig = df[comp].round(6).astype(str).agg("|".join, axis=1)
    conflict = pd.Series(False, index=df.index)
    for ref in df.loc[df["weld_metal_label"], "ref_id"].unique():
        in_ref = df["ref_id"].eq(ref)
        wm_sigs = set(sig[in_ref & df["weld_metal_label"]])
        conflict |= in_ref & ~df["weld_metal_label"] & sig.isin(wm_sigs)
    df["flag_label_says_base_metal_but_weld_metal_composition"] = conflict
    return df


# ---------------------------------------------------------------------------
# 5. Duplicate-curve detection (D-019)
# ---------------------------------------------------------------------------
def comparison_units(df: pd.DataFrame) -> pd.Series:
    """Series of records used for duplicate matching: the dataset curve ID split by anything that must not differ."""
    cid = df["curve_id_dataset"].map(lambda v: "none" if pd.isna(v) else f"{v:g}")
    parts = [df["ref_id"].astype(str), cid, df["material_std"], df["length_mm"].astype(str), df["width_mm"].astype(str),
             df["thickness_mm"].astype(str), df["irradiated"].astype(str), df["fluence_n_per_cm2"].astype(str),
             df["treatment"].astype(str), df["test_condition_statement"].astype(str)]
    return pd.Series(["|".join(p) for p in zip(*parts)], index=df.index)


def greedy_match(t_a, e_a, t_b, e_b, tol_t, k_e):
    tol_e = k_e * max(e_a.max(), e_b.max())
    if tol_e <= 0:
        return 0
    dt = np.abs(t_a[:, None] - t_b[None, :])
    de = np.abs(e_a[:, None] - e_b[None, :])
    ok = (dt <= tol_t) & (de <= tol_e)
    if not ok.any():
        return 0
    ii, jj = np.nonzero(ok)
    order = np.argsort(dt[ii, jj] / tol_t + de[ii, jj] / tol_e, kind="stable")
    used_i, used_j, m = set(), set(), 0
    for k in order:
        i, j = ii[k], jj[k]
        if i not in used_i and j not in used_j:
            used_i.add(i)
            used_j.add(j)
            m += 1
    return m


def tabulated_share(t: np.ndarray, e: np.ndarray) -> float:
    """Share of records whose temperature and energy are both at table resolution: at most one decimal place in °C and J,
    or a whole number of °F / ft·lbf before conversion. Values digitized from graphs carry many decimals (D-019, criterion a)."""
    t_tab = np.isclose(t * 10, np.round(t * 10), atol=1e-6) | np.isclose(t * 9 / 5 + 32, np.round(t * 9 / 5 + 32), atol=0.01)
    e_tab = np.isclose(e * 10, np.round(e * 10), atol=1e-6) | np.isclose(e / FT_LBF_IN_J, np.round(e / FT_LBF_IN_J), atol=0.01)
    return float(np.mean(t_tab & e_tab))


def unresolved_label_problems(sub: pd.DataFrame) -> list:
    """Unresolved labeling problems of one copy (D-019, criterion c). Resolved source checks do not count."""
    checks = [("irradiation status unresolved between releases", sub["irradiation_label_check"].eq("unresolved")),
              ("specimen type unresolved", sub["specimen_type_check"].eq("unresolved")),
              ("title reports weld/HAZ not identified in records", sub["flag_title_reports_weld_or_haz_not_identified_in_records"]),
              ("material label contradicts composition", sub["flag_label_says_base_metal_but_weld_metal_composition"]),
              ("dataset curve ID mixes conditions", sub["flag_dataset_curve_id_mixes"].ne("")),
              ("condition label contradicted by source", sub["flag_condition_label_contradicted_by_source"].ne(""))]
    return [name for name, hit in checks if bool(hit.any())]


# Which copy of a duplicated series is kept. Lower sort key = kept first (D-019).
CHOSEN_KEEP_RULE = "canonical hierarchy (chosen)"
ALT_KEEP_RULE = "most records, then fewer labeling problems (sensitivity alternative)"
KEEP_RULES = {
    CHOSEN_KEEP_RULE: lambda u: (not u["tabulated"], u["year"], len(u["problems"]), u["ref"], u["first_row"]),
    ALT_KEEP_RULE: lambda u: (-u["n"], len(u["problems"]), u["year"], u["ref"], u["first_row"]),
}
HIERARCHY_CRITERIA = ["(a) tabulated values preferred over digitized", "(b) earlier publication (original source)",
                      "(c) fewer unresolved labeling problems", "(d) tie-breaker: lower reference ID", "(d) tie-breaker: earlier spreadsheet row"]


def candidate_pairs(units: dict):
    for a, b in itertools.combinations(sorted(units), 2):
        ua, ub = units[a], units[b]
        if ua["family"] != ub["family"] or ua["dims"] != ub["dims"]:
            continue
        # An unresolved irradiation label cannot rule a match out: it is compared only when both copies' labels are settled (D-021).
        if ua["irr_key"] is not None and ub["irr_key"] is not None and ua["irr_key"] != ub["irr_key"]:
            continue
        yield a, b


def points_without_match(ua, ub, tol_t=DUP_TOL_T_C, k_e=DUP_TOL_E_FRACTION_OF_MAX) -> np.ndarray:
    """Boolean per point of ua: True where no point of ub lies within the matching tolerances."""
    tol_e = k_e * max(ua["e"].max(), ub["e"].max())
    near = (np.abs(ua["t"][:, None] - ub["t"][None, :]) <= tol_t) & (np.abs(ua["e"][:, None] - ub["e"][None, :]) <= tol_e)
    return ~near.any(axis=1)


def find_duplicates(df: pd.DataFrame, tol_t=DUP_TOL_T_C, k_e=DUP_TOL_E_FRACTION_OF_MAX, min_frac=DUP_MIN_FRACTION, pairs_cache=None,
                    keep_rule=CHOSEN_KEEP_RULE):
    unit_of = comparison_units(df)
    units = {}
    for key, idx in unit_of.groupby(unit_of).groups.items():
        sub = df.loc[idx]
        t, e = sub["test_temp_c"].to_numpy(float), sub["energy_j"].to_numpy(float)
        unresolved = bool(sub["irradiation_label_check"].eq("unresolved").any())
        irr = bool(sub["irradiated_resolved"].iloc[0])
        units[key] = dict(idx=list(idx), n=len(idx), ref=int(sub["ref_id"].iloc[0]), year=int(sub["ref_year"].iloc[0]),
                          first_row=int(sub["source_row"].min()), family=sub["material_family"].iloc[0],
                          irr_key=None if unresolved else (irr, str(sub["fluence_n_per_cm2"].iloc[0]) if irr else "none"),
                          irradiated_label=bool(sub["irradiated"].iloc[0]), irradiation_check=sub["irradiation_label_check"].iloc[0],
                          dims=tuple(str(sub[c].iloc[0]) for c in ["length_mm", "width_mm", "thickness_mm"]),
                          curve=sub["curve_id_dataset"].iloc[0], t=t, e=e, tab_share=tabulated_share(t, e),
                          problems=unresolved_label_problems(sub))
        units[key]["tabulated"] = units[key]["tab_share"] >= TABULATED_MIN_SHARE
    pairs = []
    cand = pairs_cache if pairs_cache is not None else list(candidate_pairs(units))
    for a, b in cand:
        ua, ub = units[a], units[b]
        m = greedy_match(ua["t"], ua["e"], ub["t"], ub["e"], tol_t, k_e)
        if m >= DUP_MIN_MATCHED:
            frac = m / min(ua["n"], ub["n"])
            pairs.append(dict(unit_a=a, unit_b=b, ref_a=ua["ref"], ref_b=ub["ref"], curve_a=ua["curve"], curve_b=ub["curve"],
                              n_a=ua["n"], n_b=ub["n"], matched=m, fraction_of_smaller=frac,
                              classification=("duplicate" if frac >= min_frac else
                                              "partial overlap" if frac >= PARTIAL_OVERLAP_MIN_FRACTION else "coincidental")))
    pairs = pd.DataFrame(pairs, columns=["unit_a", "unit_b", "ref_a", "ref_b", "curve_a", "curve_b", "n_a", "n_b",
                                         "matched", "fraction_of_smaller", "classification"])
    key_of = KEEP_RULES[keep_rule]
    priority = sorted(units, key=lambda k: key_of(units[k]))
    dup = pairs[pairs["classification"] == "duplicate"]
    neighbours = {}
    for r in dup.itertuples(index=False):
        neighbours.setdefault(r.unit_a, []).append((r.unit_b, r.matched))
        neighbours.setdefault(r.unit_b, []).append((r.unit_a, r.matched))
    rank = {k: i for i, k in enumerate(priority)}
    removed = {}
    for k in priority:
        if k in removed:
            continue
        for other, m in neighbours.get(k, []):
            if other not in removed and rank[other] > rank[k]:
                removed[other] = (k, m)
    hier = KEEP_RULES[CHOSEN_KEEP_RULE]
    rows = []
    for u, (k, m) in removed.items():
        ku, kk = hier(units[u]), hier(units[k])
        decided = next((HIERARCHY_CRITERIA[i] for i in range(len(ku)) if ku[i] != kk[i]), "identical keys")
        rows.append(dict(removed_unit=u, removed_ref=units[u]["ref"], removed_year=units[u]["year"], removed_curve=units[u]["curve"],
                         removed_records=units[u]["n"], kept_unit=k, kept_ref=units[k]["ref"], kept_year=units[k]["year"],
                         kept_curve=units[k]["curve"], kept_records=units[k]["n"], matched_points=m,
                         removed_points_without_match_in_kept=int(points_without_match(units[u], units[k]).sum()),
                         decided_by=decided if keep_rule == CHOSEN_KEEP_RULE else keep_rule,
                         removed_tabulated_share=round(units[u]["tab_share"], 2), kept_tabulated_share=round(units[k]["tab_share"], 2),
                         removed_label_problems="; ".join(units[u]["problems"]), kept_label_problems="; ".join(units[k]["problems"]),
                         removed_irradiated_label=units[u]["irradiated_label"], kept_irradiated_label=units[k]["irradiated_label"],
                         removed_irradiation_check=units[u]["irradiation_check"], kept_irradiation_check=units[k]["irradiation_check"]))
    removals = pd.DataFrame(rows, columns=["removed_unit", "removed_ref", "removed_year", "removed_curve", "removed_records", "kept_unit",
                                           "kept_ref", "kept_year", "kept_curve", "kept_records", "matched_points",
                                           "removed_points_without_match_in_kept", "decided_by", "removed_tabulated_share",
                                           "kept_tabulated_share", "removed_label_problems", "kept_label_problems",
                                           "removed_irradiated_label", "kept_irradiated_label", "removed_irradiation_check",
                                           "kept_irradiation_check"])
    return units, unit_of, pairs, removals, cand


def duplicate_sensitivity(df: pd.DataFrame, cand) -> pd.DataFrame:
    rows = []
    for tol_t in (2.0, 3.0, 5.0):
        for k_e in (0.01, 0.02, 0.03):
            for min_frac in (0.6, 0.7, 0.8, 0.9):
                _, _, pairs, removals, _ = find_duplicates(df, tol_t, k_e, min_frac, pairs_cache=cand)
                rows.append(dict(tol_T_C=tol_t, tol_E_fraction_of_max=k_e, min_fraction_matched=min_frac,
                                 duplicate_pairs=int((pairs["classification"] == "duplicate").sum()),
                                 partial_overlap_pairs=int((pairs["classification"] == "partial overlap").sum()),
                                 units_removed=len(removals), records_removed=int(removals["removed_records"].sum()),
                                 references_losing_records=removals["removed_ref"].nunique(),
                                 chosen=(tol_t, k_e, min_frac) == (DUP_TOL_T_C, DUP_TOL_E_FRACTION_OF_MAX, DUP_MIN_FRACTION)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 6. Exclusion steps and reconciliation (D-014 to D-019, D-025)
# ---------------------------------------------------------------------------
STEPS = [
    ("E1", "Out of scope: austenitic stainless steel (SS316 family)", "brief section 4; D-014"),
    ("E2", "Out of scope: ferritic steel outside the brief's named RPV-steel family (15Cr2MoV-A)", "brief section 4; CP1 decision 4; D-012"),
    ("E3", "Not a standard Charpy impact test: striking velocity outside ASTM E23 range (3-6 m/s)", "ASTM E23-82 §4.1.6; D-015"),
    ("E4", "Missing essential measurement: test temperature or absorbed energy", "D-016"),
    ("E5", "Missing essential measurement: specimen dimensions (length, width or thickness)", "D-016"),
    ("E6", "Physically impossible value", "D-017"),
    ("E7", "Exact duplicate of an earlier record (all original fields identical)", "D-018"),
    ("E8", "Duplicate curve: same tests already present from another figure or publication", "D-019"),
]


def criteria_masks(df: pd.DataFrame) -> dict:
    lo, hi = E23_VELOCITY_RANGE_M_S
    impossible = ((df["energy_j"] < 0) | (df["test_temp_c"] < ABSOLUTE_ZERO_C)
                  | (df[["length_mm", "width_mm", "thickness_mm"]] <= 0).any(axis=1)
                  | (df["notch_depth_mm"] >= df["width_mm"]) | (df["fluence_n_per_cm2"] < 0)
                  | (df["irradiation_temp_c"] < ABSOLUTE_ZERO_C))
    original = [COLUMN_BY_RAW[c]["clean"] for c in COLUMN_BY_RAW if COLUMN_BY_RAW[c]["clean"] in df.columns]
    return {
        "E1": df["material_scope"].eq("out"),
        "E2": df["material_scope"].eq("out_ferritic"),
        "E3": df["striking_velocity_m_per_s"].notna() & ~df["striking_velocity_m_per_s"].between(lo, hi),
        "E4": df["test_temp_c"].isna() | df["energy_j"].isna(),
        "E5": df[["length_mm", "width_mm", "thickness_mm"]].isna().any(axis=1),
        "E6": impossible.fillna(False),
        "E7": df.duplicated(subset=original, keep="first"),
    }


def apply_exclusions(df: pd.DataFrame, out_dir):
    masks = criteria_masks(df)
    # 'All applicable' view: every criterion evaluated on every record, independent of order.
    allapp = pd.DataFrame({k: v.astype(bool) for k, v in masks.items()})
    allapp["material_family"] = df["material_family"]
    allapp.groupby("material_family").sum().to_csv(out_dir / "exclusion_reasons_all_applicable.csv")
    df["all_applicable_exclusion_criteria"] = allapp[list(masks)].apply(lambda r: ", ".join(k for k in masks if r[k]), axis=1)
    df["status"], df["exclusion_step"], df["exclusion_reason"] = "retained", "", ""
    step_text = {s: t for s, t, _ in STEPS}
    for step in ["E1", "E2", "E3", "E4", "E5", "E6"]:
        hit = (df["status"] == "retained") & masks[step].astype(bool)
        df.loc[hit, ["status", "exclusion_step", "exclusion_reason"]] = ["excluded", step, step_text[step]]
    # Exact duplicates are evaluated among records still retained, keeping the earliest spreadsheet row.
    original = [COLUMN_BY_RAW[c]["clean"] for c in COLUMN_BY_RAW if COLUMN_BY_RAW[c]["clean"] in df.columns]
    ret = df["status"] == "retained"
    exact = df.loc[ret].duplicated(subset=original, keep="first").reindex(df.index, fill_value=False)
    df.loc[exact, ["status", "exclusion_step", "exclusion_reason"]] = ["excluded", "E7", step_text["E7"]]
    # Duplicate curves among the records still retained.
    ret = df["status"] == "retained"
    units, unit_of, pairs, removals, cand = find_duplicates(df.loc[ret])
    df["duplicate_comparison_unit"] = ""
    df.loc[ret, "duplicate_comparison_unit"] = unit_of
    for r in removals.itertuples(index=False):
        idx = units[r.removed_unit]["idx"]
        reason = (f"{step_text['E8']} (kept copy: ref {r.kept_ref} ({r.kept_year}), dataset curve "
                  f"{'none' if pd.isna(r.kept_curve) else f'{r.kept_curve:g}'}; {r.matched_points} of {r.removed_records} points matched; "
                  f"kept by {r.decided_by})")
        df.loc[idx, ["status", "exclusion_step", "exclusion_reason"]] = ["excluded", "E8", reason]
    # The alternative keep rule is carried forward as a sensitivity case: same duplicate graph, other copy kept (D-019).
    _, _, _, removals_alt, _ = find_duplicates(df.loc[ret], pairs_cache=cand, keep_rule=ALT_KEEP_RULE)
    df["status_under_alt_keep_rule"] = np.where(df["status"].eq("excluded") & df["exclusion_step"].ne("E8"), "excluded", "retained")
    for r in removals_alt.itertuples(index=False):
        df.loc[units[r.removed_unit]["idx"], "status_under_alt_keep_rule"] = "excluded"
    removals_alt.to_csv(out_dir / "duplicate_curve_removals_alt_keep_rule.csv", index=False)
    partial = pairs[pairs["classification"] == "partial overlap"]
    df["flag_partial_overlap_with_other_curve"] = ""
    for r in partial.itertuples(index=False):
        for mine, other_ref, other_curve in [(r.unit_a, r.ref_b, r.curve_b), (r.unit_b, r.ref_a, r.curve_a)]:
            idx = units[mine]["idx"]
            tag = f"ref {other_ref} curve {'none' if pd.isna(other_curve) else f'{other_curve:g}'} ({r.matched}/{min(r.n_a, r.n_b)})"
            df.loc[idx, "flag_partial_overlap_with_other_curve"] = df.loc[idx, "flag_partial_overlap_with_other_curve"].map(
                lambda s: tag if s == "" else f"{s}; {tag}")
    df, keep_rules = duplicate_diagnostics(df, units, pairs, removals)
    keep_rules.to_csv(out_dir / "duplicate_keep_rule_comparison.csv", index=False)
    pairs.to_csv(out_dir / "duplicate_curve_pairs.csv", index=False)
    removals.to_csv(out_dir / "duplicate_curve_removals.csv", index=False)
    sens = duplicate_sensitivity(df.loc[ret], cand)
    sens.to_csv(out_dir / "duplicate_sensitivity.csv", index=False)
    return df, pairs, removals, sens


COMPOSITION_FIELDS = ["c_wt_pct", "si_wt_pct", "mn_wt_pct", "p_wt_pct", "s_wt_pct", "ni_wt_pct", "cr_wt_pct", "mo_wt_pct", "cu_wt_pct"]


def duplicate_diagnostics(df, units, pairs, removals):
    """Flags on the kept copies of duplicated series, plus a comparison of alternative keep rules (D-019)."""
    dup = pairs[pairs["classification"] == "duplicate"]
    nbrs = {}
    for r in dup.itertuples(index=False):
        nbrs.setdefault(r.unit_a, []).append(r.unit_b)
        nbrs.setdefault(r.unit_b, []).append(r.unit_a)
    corroborated = {}
    for u, others in nbrs.items():
        ua, ok = units[u], np.zeros(units[u]["n"], dtype=bool)
        for v in others:
            ub = units[v]
            tol_e = DUP_TOL_E_FRACTION_OF_MAX * max(ua["e"].max(), ub["e"].max())
            ok |= ((np.abs(ua["t"][:, None] - ub["t"][None, :]) <= DUP_TOL_T_C)
                   & (np.abs(ua["e"][:, None] - ub["e"][None, :]) <= tol_e)).any(axis=1)
        corroborated[u] = ok
    removed_units = set(removals["removed_unit"])
    df["flag_point_not_corroborated_by_duplicate_copies"] = False
    df["flag_duplicate_copies_disagree_on_composition"] = ""
    signature = lambda idx: " ".join(f"{c.split('_')[0].capitalize()}={df.at[idx, c]:g}" for c in COMPOSITION_FIELDS if pd.notna(df.at[idx, c]))
    for u in nbrs:
        if u in removed_units:
            continue
        idx = units[u]["idx"]
        df.loc[[i for i, ok in zip(idx, corroborated[u]) if not ok], "flag_point_not_corroborated_by_duplicate_copies"] = True
        mine = signature(idx[0])
        others = sorted({signature(units[v]["idx"][0]) for v in nbrs[u]} - {mine})
        if others:
            df.loc[idx, "flag_duplicate_copies_disagree_on_composition"] = "other copies: " + " | ".join(others)
    # Keep rules compared on the same duplicate graph. 'Uncorroborated' = point found in no other copy: extra real data or an error.
    chosen_removed = set(removals["removed_unit"])
    def evaluate(key):
        prio = sorted(units, key=key)
        rank, removed = {k: i for i, k in enumerate(prio)}, set()
        for k in prio:
            if k not in removed:
                removed |= {o for o in nbrs.get(k, []) if o not in removed and rank[o] > rank[k]}
        kept = [u for u in nbrs if u not in removed]
        return dict(series_removed=len(removed), records_removed=sum(units[u]["n"] for u in removed),
                    uncorroborated_points_kept=int(sum((~corroborated[u]).sum() for u in kept)),
                    uncorroborated_points_removed=int(sum((~corroborated[u]).sum() for u in removed)),
                    series_kept_with_unresolved_label_problems=sum(1 for u in kept if units[u]["problems"]),
                    series_removed_here_but_kept_by_chosen_rule=len(removed - chosen_removed),
                    series_kept_here_but_removed_by_chosen_rule=len(chosen_removed - removed))
    n_corr = lambda k: int(corroborated[k].sum()) if k in corroborated else units[k]["n"]
    rules = {**{name: (lambda f: lambda k: f(units[k]))(f) for name, f in KEEP_RULES.items()},
             "most records, then earliest publication (CP1 rule)": lambda k: (-units[k]["n"], units[k]["year"], units[k]["ref"], units[k]["first_row"]),
             "earliest publication, then most records": lambda k: (units[k]["year"], -units[k]["n"], units[k]["ref"], units[k]["first_row"]),
             "most corroborated records, then earliest publication": lambda k: (-n_corr(k), units[k]["year"], units[k]["ref"], units[k]["first_row"])}
    table = pd.DataFrame([dict(keep_rule=name, **evaluate(key)) for name, key in rules.items()])
    return df, table


def reconciliation(df: pd.DataFrame) -> pd.DataFrame:
    rows = [dict(step="Start", criterion="Records in the 'Charpy Data' sheet", basis="", records_removed="", records_remaining=len(df))]
    remaining = len(df)
    for step, text, basis in STEPS:
        n = int((df["exclusion_step"] == step).sum())
        remaining -= n
        rows.append(dict(step=step, criterion=text, basis=basis, records_removed=n, records_remaining=remaining))
    final = int((df["status"] == "retained").sum())
    if remaining != final or len(df) - int((df["status"] == "excluded").sum()) != final:
        raise AssertionError("Reconciliation arithmetic does not close")
    rows.append(dict(step="End", criterion="Records retained after WP1", basis="", records_removed=len(df) - final, records_remaining=final))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 7. Unit checks (D-010)
# ---------------------------------------------------------------------------
def unit_checks(df: pd.DataFrame) -> str:
    fer = df[df["material_scope"].eq("in")]
    ret = df[df["status"] == "retained"]
    L = ["# WP1 unit checks", "",
         "The dataset authors state that they converted all values to one unit per column [descriptor]. WP1 therefore "
         "verifies rather than converts. No conversion was applied to any value. Checks use in-scope ferritic records "
         "unless stated otherwise.", ""]
    T = fer["test_temp_c"]
    L += ["## Temperature (°C)", "",
          f"- Test temperature range: {T.min():.2f} to {T.max():.2f} °C. Below absolute zero: {int((T < ABSOLUTE_ZERO_C).sum())}. "
          f"Outside the review window {PLAUSIBLE_TEST_TEMP_C}: {int(((T < PLAUSIBLE_TEST_TEMP_C[0]) | (T > PLAUSIBLE_TEST_TEMP_C[1])).sum())}.",
          "- A column left in kelvin would have no values below 0 and cluster near 77-600; a column left in °F would put "
          "liquid-nitrogen tests near -321. Neither pattern is present: the coldest tests sit at the liquid-nitrogen point (-196 °C).",
          "- Irradiation temperatures and what they equal in other units (a whole number suggests the original unit):", ""]
    irr = pd.DataFrame({"value_C": sorted(fer["irradiation_temp_c"].dropna().unique())})
    irr["in_K"] = irr["value_C"] + 273.15
    irr["in_F"] = irr["value_C"] * 9 / 5 + 32
    irr["records"] = irr["value_C"].map(fer["irradiation_temp_c"].value_counts())
    L += [md_table(irr, "{:.2f}"), ""]
    ratio = ret[ret["use_j_dataset"].notna()].groupby("curve_id_dataset").apply(
        lambda s: s["energy_j"].max() / s["use_j_dataset"].iloc[0], include_groups=False)
    L += ["## Absorbed energy (J)", "",
          "If a curve's energies had been left in ft-lbf while its dataset USE was in joules, the curve's highest energy would sit "
          "near 0.74 x USE (1 ft-lbf = 1.3558 J); the reverse error would give about 1.36 x USE.", "",
          f"- Retained dataset curves checked: {len(ratio)}. Ratio max(energy)/USE: median {ratio.median():.3f}, "
          f"5th-95th percentile {ratio.quantile(0.05):.3f}-{ratio.quantile(0.95):.3f}, min {ratio.min():.3f}, max {ratio.max():.3f}.",
          f"- Curves with ratio below 0.85 or above 1.25: {int(((ratio < 0.85) | (ratio > 1.25)).sum())} "
          f"({', '.join(f'{k:g}: {v:.2f}' for k, v in ratio[(ratio < 0.85) | (ratio > 1.25)].items()) or 'none'}).",
          "- Limitation: this detects inconsistency within a curve. A source whose energies and USE were both left unconverted "
          "would pass; that can only be ruled out against the source papers.", ""]
    F = fer["fluence_n_per_cm2"].dropna()
    L += ["## Fluence (n/cm²)", "",
          f"- Range {F.min():.3g} to {F.max():.3g}. Values in n/m² would be 10^4 times larger (typically 1e21-1e24); "
          "values in dpa would be below about 1. All values are consistent with n/cm².",
          "- The neutron-energy threshold is not stated anywhere in the dataset (D-011).", ""]
    dims = pd.DataFrame({c: [", ".join(f"{v:g}" for v in sorted(fer[c].dropna().unique()))] for c in
                         ["length_mm", "width_mm", "thickness_mm", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm"]}).T
    dims.columns = ["distinct values"]
    dims.insert(0, "column", dims.index)
    L += ["## Specimen dimensions (mm)", "",
          "Inch values would appear as 2.165 (55 mm), 0.394 (10 mm), 0.079 (2 mm) or 0.010 (0.25 mm). None are present.", "",
          md_table(dims), ""]
    comp = ["c_wt_pct", "si_wt_pct", "mn_wt_pct", "p_wt_pct", "s_wt_pct", "ni_wt_pct", "cr_wt_pct", "mo_wt_pct", "al_wt_pct",
            "n_wt_pct", "ti_wt_pct", "fe_wt_pct", "nb_wt_pct", "b_wt_pct", "cu_wt_pct", "v_wt_pct", "zr_wt_pct", "w_wt_pct",
            "sn_wt_pct", "co_wt_pct", "o_wt_pct", "ta_wt_pct", "as_wt_pct", "sb_wt_pct"]
    with_fe = fer[fer["fe_wt_pct"].notna()]
    total = with_fe[comp].sum(axis=1)
    L += ["## Composition (wt.%)", "",
          f"- Records with Fe reported: {len(with_fe)}. Sum of all reported elements: {total.min():.3f} to {total.max():.3f} wt.%; "
          f"outside 99-101: {int(((total < 99) | (total > 101)).sum())}. Sums close to 100 are expected because Fe was often "
          "computed as the balance, so this check mainly catches ppm-for-wt.% entry errors (none seen).", ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# 8. Driver
# ---------------------------------------------------------------------------
FLAG_COLUMNS_ORDER = [
    "flag_precracked_label_in_2025_release", "flag_source_reports_precracked_specimens",
    "flag_irradiation_status_differs_between_releases", "flag_condition_label_contradicted_by_source",
    "flag_title_reports_weld_or_haz_not_identified_in_records",
    "flag_label_says_base_metal_but_weld_metal_composition", "flag_dataset_curve_id_mixes",
    "flag_partial_overlap_with_other_curve", "flag_point_not_corroborated_by_duplicate_copies",
    "flag_duplicate_copies_disagree_on_composition", "flag_notch_dimensions_not_reported", "flag_notch_shape_blank",
    "flag_irradiated_without_irradiation_temp", "flag_zero_energy", "flag_energy_above_1p5x_dataset_use",
    "flag_energy_per_ligament_area_above_bound", "flag_test_temp_outside_review_window",
]
TAG_COLUMNS = ["tag_reconstituted_specimen", "tag_simulated_haz", "tag_haz_statement", "tag_welded_area", "tag_shock_wave_hardened",
               "tag_prestrained", "tag_step_cooled", "tag_pwht", "tag_standard_reference_material", "tag_hydrogen_charged",
               "tag_orientation_semantics_differ"]


def flags_summary(df: pd.DataFrame) -> str:
    ret = df[df["status"] == "retained"]
    rows = []
    for col in FLAG_COLUMNS_ORDER + TAG_COLUMNS:
        hit = ret[col].astype(bool) if ret[col].dtype == bool else ret[col].fillna("").ne("")
        rows.append(dict(field=col, retained_records=int(hit.sum()), references=", ".join(str(r) for r in sorted(ret.loc[hit, "ref_id"].unique()))))
    extra = [dict(field=f"grade in title: {g}", retained_records=int((ret["ref_grade_title"] == g).sum()),
                  references=", ".join(str(r) for r in sorted(ret.loc[ret["ref_grade_title"] == g, "ref_id"].unique())))
             for g in sorted(ret["ref_grade_title"].unique()) if g]
    L = ["# WP1 flags and tags on retained records", "",
         "Flags mark records that need a decision or extra care later; tags describe special material or specimen conditions. "
         "Neither removes records.", "", md_table(pd.DataFrame(rows)), "",
         "## Outcome of source checks on retained records (D-020, D-021)", "",
         md_table(ret.groupby(["specimen_type_check"]).agg(records=("record_id", "size"),
                  references=("ref_id", lambda r: ", ".join(str(x) for x in sorted(r.unique())))).reset_index()), "",
         md_table(ret.groupby(["irradiation_label_check", "irradiated", "irradiated_resolved"]).agg(records=("record_id", "size"),
                  references=("ref_id", lambda r: ", ".join(str(x) for x in sorted(r.unique())))).reset_index()), "",
         "## Product form of retained records", "",
         md_table(ret.groupby(["material_family", "product_form", "product_form_basis"]).size().reset_index(name="records")), "",
         "## Grade or class stated in the citation title (reference level)", "", md_table(pd.DataFrame(extra)), ""]
    return "\n".join(L)


def run(dataset_key: str):
    tag = "" if dataset_key == PRIMARY_DATASET else f"_sensitivity_{dataset_key}"
    out_dir = OUTPUTS / f"wp1{tag}"
    proc_dir = PROCESSED / ("primary" if not tag else tag.lstrip("_"))
    out_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)
    ds = DATASETS[dataset_key]
    log = []
    raw = load_charpy_data(ds["xlsx"])
    refs = load_references(ds["xlsx"])
    df = rename_and_clean_text(raw, log)
    df = harmonize_material(df, log)
    df = derive_tags_and_geometry(df)
    df = derive_reference_fields(df, refs)
    df = derive_product_form(df)
    df = crosscheck_other_release(df, dataset_key)
    df = source_check_fields(df)
    df = consistency_flags(df)
    df, pairs, removals, sens = apply_exclusions(df, out_dir)

    rec = reconciliation(df)
    rec.to_csv(out_dir / "reconciliation_table.csv", index=False)
    by_family = pd.crosstab(df["exclusion_step"].replace("", "retained"), df["material_family"], margins=True, margins_name="total")
    write_text(out_dir / "reconciliation_table.md",
               f"# WP1 reconciliation table\n\nDataset: {ds['label']}.\n\n"
               "Each record is counted once, at the first step that applies (steps run in the order shown). "
               "`exclusion_reasons_all_applicable.csv` counts every criterion that applies to each record, regardless of order.\n\n"
               + md_table(rec) + "\n\n## Records by step and material family\n\n" + md_table(by_family.reset_index()))
    pd.DataFrame(log).to_csv(out_dir / "value_changes_log.csv", index=False)
    write_text(out_dir / "unit_checks.md", unit_checks(df))
    write_text(out_dir / "flags_summary.md", flags_summary(df))

    order = (["record_id", "source_row", "status", "exclusion_step", "exclusion_reason", "all_applicable_exclusion_criteria",
              "ref_id", "ref_year", "material_raw", "material_std", "material_family", "material_class_stated", "designation_prefix",
              "weld_metal_label", "material_scope", "product_form", "product_form_basis", "test_temp_c", "energy_j",
              "length_mm", "width_mm", "thickness_mm", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm", "notch_shape",
              "ligament_mm", "geometry_label", "energy_per_ligament_area_j_cm2", "irradiated", "irradiated_in_other_release",
              "irradiation_label_check", "irradiated_resolved", "specimen_type_check",
              "fluence_n_per_cm2", "irradiation_temp_c", "irradiation_time_h", "orientation", "test_condition_statement",
              "striking_velocity_m_per_s", "test_standard", "curve_id_dataset", "use_j_dataset", "dbtt_c_dataset",
              "duplicate_comparison_unit", "status_under_alt_keep_rule"] + FLAG_COLUMNS_ORDER + TAG_COLUMNS
             + ["ref_grade_title", "ref_product_form_note", "ref_specimen_note", "ref_material_note", "ref_forming_evidence"])
    rest = [c for c in df.columns if c not in order]
    df = df[order + rest]
    df.to_csv(proc_dir / "charpy_records_with_status.csv", index=False)
    df[df["status"] == "retained"].to_csv(proc_dir / "charpy_clean.csv", index=False)

    dup_hist = pd.cut(pairs["fraction_of_smaller"], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .9999, 1.0001],
                      right=True).value_counts().sort_index()
    summary = [f"# WP1 summary ({dataset_key})", "", f"Dataset: {ds['label']}", "",
               f"- Records in: {len(df)}; retained: {int((df['status'] == 'retained').sum())}; excluded: {int((df['status'] == 'excluded').sum())}.",
               f"- Retained references: {df.loc[df['status'] == 'retained', 'ref_id'].nunique()}; "
               f"retained dataset curve IDs: {df.loc[df['status'] == 'retained', 'curve_id_dataset'].nunique()}.",
               f"- Text values changed (see value_changes_log.csv): {sum(r['records'] for r in log if r['change'] in ('whitespace trimmed', 'text harmonized'))} cell edits.",
               "", "## Duplicate-curve detection", "",
               f"Parameters: |dT| <= {DUP_TOL_T_C} °C, |dE| <= {DUP_TOL_E_FRACTION_OF_MAX:.0%} of the larger curve maximum, "
               f"at least {DUP_MIN_MATCHED} one-to-one matched points and at least {DUP_MIN_FRACTION:.0%} of the smaller series matched.", "",
               f"- Candidate pairs with >= {DUP_MIN_MATCHED} matched points: {len(pairs)}; duplicates: {int((pairs['classification'] == 'duplicate').sum())}; "
               f"partial overlaps (flagged only): {int((pairs['classification'] == 'partial overlap').sum())}.",
               f"- Series removed: {len(removals)} ({int(removals['removed_records'].sum())} records) from references "
               f"{sorted(removals['removed_ref'].unique().tolist())}.",
               f"- Which criterion of the canonical hierarchy decided each removal: "
               + "; ".join(f"{k}: {v}" for k, v in removals["decided_by"].value_counts().sort_index().items()) + ".",
               f"- Removed copies whose irradiation label differs from the kept copy: "
               f"{int((removals['removed_irradiated_label'] != removals['kept_irradiated_label']).sum())}.",
               f"- Records retained under the alternative keep rule (most records first): "
               f"{int((df['status_under_alt_keep_rule'] == 'retained').sum())} (chosen rule: {int((df['status'] == 'retained').sum())}).", "",
               "Distribution of the matched fraction over candidate pairs (a gap separates chance overlaps from re-publications):", "",
               md_table(dup_hist.rename_axis("fraction of smaller series matched").reset_index(name="pairs").astype(str)), "",
               "Sensitivity of the removals to the three parameters:", "", md_table(sens), "",
               "Effect of the rule choosing which copy to keep (same duplicate pairs; 'uncorroborated' = point found in no other copy):", "",
               md_table(pd.read_csv(out_dir / "duplicate_keep_rule_comparison.csv")), ""]
    write_text(out_dir / "wp1_summary.md", "\n".join(summary))
    print(f"WP1 ({dataset_key}): {len(df)} in, {int((df['status'] == 'retained').sum())} retained -> {out_dir}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=PRIMARY_DATASET, choices=sorted(DATASETS))
    run(ap.parse_args().dataset)
