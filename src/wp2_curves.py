"""WP2 - Curve grouping and inclusion criteria.

Assigns every record retained by WP1 to one transition curve, describes how each curve samples its energy range WITHOUT
fitting anything, applies looser / primary / stricter pre-fit screening rules, and writes cohort memberships so later work
packages can propagate every sensitivity case. Nothing is fitted here (WP3). Passing a screening rule means only that a curve
appears sufficiently sampled to attempt a fit (D-038). The dataset's own USE, DBTT and curve IDs are provenance only (D-022).

Outputs (run = 'primary' for the 2025.30 release, 'sensitivity_<record>' for the 2024.206 release):
  data/processed/<run>/charpy_records_with_curves.csv   every WP1-retained record with its curve, population and cohorts
  outputs/wp2[_sensitivity_<record>]/curve_inventory.csv  one row per curve: descriptors, rule outcomes, cohorts
  outputs/wp2[...]/cohort_membership.csv, cohort_manifest.csv   the cohorts frozen at CP2, as explicit files (D-039)
  outputs/wp2[...]/population_accounting.csv, rule_outcomes.csv, rule_outcomes_by_group.csv, dataset_series_splits.csv,
      fluence_treatments.csv, fluence_by_source.csv, screening_upper_reference_diagnostic.csv, wp2_summary.md
  outputs/wp2/version_sensitivity_comparison.md (+ .csv), outputs/wp2/example_curves.png   (primary run, after both runs)
Every run ends by checking each cohort's membership against data/FROZEN_COHORTS_CP2.csv and stops on any difference.

Run:  .venv/bin/python src/wp2_curves.py      (both releases, then the comparison, the figure and the frozen-cohort check)
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from common import DATA, DATASETS, OUTPUTS, PRIMARY_DATASET, PROCESSED, SENSITIVITY_DATASET, md_table, write_text

# ---------------------------------------------------------------------------
# 1. Definitions (each justified in DECISIONS.md)
# ---------------------------------------------------------------------------
# D-033. Records belong to one transition curve only if they agree on every field below. A curve never spans two source
# publications or two dataset series (D-032); within a series it is split wherever any other field differs.
SOURCE_FIELDS = ["ref_id", "curve_id_dataset"]
MATERIAL_FIELDS = ["material_std", "composition_signature", "product_form"]
GEOMETRY_FIELDS = ["length_mm", "width_mm", "thickness_mm", "notch_depth_mm", "notch_angle_deg", "notch_root_radius_mm", "orientation"]
IRRADIATION_FIELDS = ["irradiated_resolved", "fluence_level", "irradiation_temp_c", "irradiation_time_h"]
CONDITION_FIELDS = ["treatment", "post_treatment_temp_c", "post_treatment_time_h", "cooling_method", "cooling_rate_c_per_min",
                    "test_condition_statement"]
CURVE_KEY_FIELDS = SOURCE_FIELDS + MATERIAL_FIELDS + GEOMETRY_FIELDS + IRRADIATION_FIELDS + CONDITION_FIELDS
COMPOSITION_FIELDS = ["c_wt_pct", "si_wt_pct", "mn_wt_pct", "p_wt_pct", "s_wt_pct", "ni_wt_pct", "cr_wt_pct", "mo_wt_pct", "al_wt_pct",
                      "n_wt_pct", "ti_wt_pct", "fe_wt_pct", "nb_wt_pct", "b_wt_pct", "cu_wt_pct", "v_wt_pct", "zr_wt_pct", "w_wt_pct",
                      "sn_wt_pct", "co_wt_pct", "o_wt_pct", "ta_wt_pct", "as_wt_pct", "sb_wt_pct"]

# D-036. Fluence: the reported value (primary). Alternative: levels within a factor of 1.2 (about the 20 % fluence
# uncertainty quoted by Jendrich & Tricot 2003) are one level; applied inside the same source and dataset series.
FLUENCE_TOLERANCE_FACTOR = 1.2

# D-037. Pre-fit sampling descriptors. Test temperatures closer than 2 °C are one test temperature (about twice the 95th percentile of
# the digitization difference between copies of the same point, D-019).
# Screening references, without fitting: lower = the lowest measured energy; SCREENING UPPER REFERENCE = the mean of the three highest
# measured energies, so that no single high point sets the scale (ASTM E185-82 §4.18 likewise averages normally three upper-shelf
# specimens). It is a screening quantity, NOT the upper-shelf energy (USE): nothing here shows that those three points lie on a flat
# shelf. USE is estimated in WP3 by its own, separately justified method.
# Energy bands: each point's position between the two references, 0 to 1. The transition band 0.12-0.88 is a PROJECT-DEFINED,
# MODEL-BASED screening convention, not an ASTM requirement: for the normalized tanh y = (1 + tanh x) / 2 with x = (T - T0) / C,
# y = 0.119 at x = -1 and y = 0.881 at x = +1, so the band is the central characteristic interval T0 - C to T0 + C. An approximately
# 0.10-0.85 transition-region convention is preserved as a later sensitivity option; its literature basis is not yet documented (D-037).
DISTINCT_TEMPERATURE_GAP_C = 2.0
BAND_LOWER, BAND_UPPER = 0.12, 0.88
UPPER_REFERENCE_POINTS = 3

# D-038. Pre-fit screening rules. Passing one means only that a curve appears sufficiently sampled to ATTEMPT a transition-curve fit in
# WP3. It does not show that a tanh fit will converge, be well conditioned or give physically reasonable parameters, and a curve whose
# WP3 fit fails must be reported, never silently removed. min_points_* : number of records; min_T_* : distinct test temperatures in that
# energy band; max_energy_ratio : lowest energy / screening upper reference.
RULES = {
    "looser": dict(min_points_unirradiated=5, min_points_irradiated=5, min_T_transition=1, min_T_upper=1, min_points_upper=1,
                   min_T_lower=1, max_energy_ratio=0.30),
    "primary": dict(min_points_unirradiated=6, min_points_irradiated=6, min_T_transition=2, min_T_upper=2, min_points_upper=2,
                    min_T_lower=1, max_energy_ratio=0.20),
    "stricter": dict(min_points_unirradiated=15, min_points_irradiated=12, min_T_transition=3, min_T_upper=2, min_points_upper=3,
                     min_T_lower=2, max_energy_ratio=0.15),
}
RULE_BASIS = {
    "points": "5 = fewest that leave one residual degree of freedom for a 4-parameter tanh; 6 = two; 15 unirradiated / 12 irradiated = "
              "historical ASTM E185-82 §6.3 surveillance-programme specimen minimums (baseline curve / irradiated capsule), used as a "
              "deliberately conservative comparison, not as a statistical law that fewer points make a curve unusable",
    "transition temperatures": "transition band = 0.12-0.88 of the rise between the screening references, i.e. T0 - C to T0 + C of a "
                               "normalized tanh (project-defined, model-based, not an ASTM requirement); 1 temperature locates the "
                               "transition; 2 fix location and width (T0 and C); 3 add one check on the shape",
    "upper band": "1 = no requirement; 2 distinct temperatures show the rise has stopped; 3 specimens mirrors the normally three "
                  "specimens ASTM E185-82 §4.18 averages for upper-shelf energy (a screening count only; USE is estimated in WP3)",
    "energy ratio": "lowest energy / screening upper reference: the coldest point lies at or below the lower band edge (T0 - C) whenever "
                    "the true lower-to-upper shelf ratio is at most 0.20 (limit 0.30), 0.09 (limit 0.20), 0.03 (limit 0.15)",
}

# D-034, D-035. Analysis populations, evaluated in this order; each record is assigned to the first that applies.
POPULATION_STEPS = [
    ("P1", "excluded: specimen type not supported as ordinary Charpy V-notch", "CP1 decision 2; D-020"),
    ("P2", "excluded: condition label contradicted by the source", "D-031 (approved at CP2)"),
    ("P3", "excluded: irradiation status unresolved between releases", "CP1 decision 1; D-021; D-035 (approved at CP2)"),
    ("P4", "secondary: SA508 Gr.1A main-steam-line piping steel", "CP1 decision 3; D-027"),
    ("P5", "secondary: additively manufactured SA508 Gr.3 (manufacturing route differs from conventional RPV material)",
     "D-034 (approved at CP2)"),
]
PRIMARY_POPULATION = "primary RPV population"

# Cohorts carried to later work packages (D-039): (role, definition). Each is the primary cohort with one thing changed. Membership is
# frozen at CP2: every run compares it with FROZEN_COHORTS and stops on any difference.
COHORTS = {
    "primary": ("primary analysis", "primary population, primary rule, canonical keep rule"),
    "looser": ("inclusion-rule sensitivity", "primary population, looser rule"),
    "stricter": ("inclusion-rule sensitivity", "primary population, stricter rule"),
    "alt_keep_rule": ("duplicate keep-rule sensitivity", "primary population, primary rule, alternative duplicate keep rule (most records first)"),
    "plus_unresolved_irradiation": ("population sensitivity", "primary population plus records with unresolved irradiation labels "
                                                              "(this release's labels), primary rule"),
    "plus_additively_manufactured": ("population sensitivity (secondary material)", "primary population plus additively manufactured "
                                                                                    "SA508 Gr.3, primary rule"),
    "piping_secondary": ("secondary group", "SA508 Gr.1A piping steel only, primary rule"),
}
FROZEN_COHORTS = DATA / "FROZEN_COHORTS_CP2.csv"


# ---------------------------------------------------------------------------
# 2. Populations and derived grouping fields
# ---------------------------------------------------------------------------
def load_records(run: str) -> pd.DataFrame:
    df = pd.read_csv(PROCESSED / run / "charpy_records_with_status.csv", low_memory=False)
    for col in ["irradiated", "irradiated_resolved", "weld_metal_label", "tag_reconstituted_specimen",
                "flag_point_not_corroborated_by_duplicate_copies", "flag_title_reports_weld_or_haz_not_identified_in_records"]:
        df[col] = df[col].astype(bool)
    for col in ["flag_condition_label_contradicted_by_source", "flag_dataset_curve_id_mixes", "ref_grade_title"]:
        df[col] = df[col].fillna("")
    # Records that later stages may use under either duplicate keep rule (D-019); everything else left in WP1.
    keep = df["status"].eq("retained") | df["status_under_alt_keep_rule"].eq("retained")
    df = df[keep].copy()
    df["retained_chosen_keep_rule"] = df["status"].eq("retained")
    df["retained_alt_keep_rule"] = df["status_under_alt_keep_rule"].eq("retained")
    return df


def assign_population(df: pd.DataFrame) -> pd.DataFrame:
    masks = {
        "P1": ~df["specimen_type_check"].isin(["no concern raised", "source-checked: ordinary CVN"]),
        "P2": df["flag_condition_label_contradicted_by_source"].ne(""),
        "P3": df["irradiation_label_check"].eq("unresolved"),
        "P4": df["ref_grade_title"].eq("SA508 Gr.1A"),
        "P5": df["product_form"].eq("additively manufactured"),
    }
    df["population"], df["population_step"] = PRIMARY_POPULATION, ""
    for step, text, _ in POPULATION_STEPS:
        hit = df["population_step"].eq("") & masks[step]
        df.loc[hit, "population"], df.loc[hit, "population_step"] = text, step
    df["population_all_applicable"] = pd.DataFrame(masks).apply(lambda r: ", ".join(k for k in masks if r[k]), axis=1)
    return df


def fluence_levels(df: pd.DataFrame, treatment: str, respect_series: bool = True) -> pd.Series:
    """Fluence level used for grouping. 'exact' = reported value; 'tolerance' = values within FLUENCE_TOLERANCE_FACTOR of the
    next lower value (single linkage) are one level, inside each source and dataset series (or each source, if respect_series is False)."""
    level = df["fluence_n_per_cm2"].copy()
    if treatment == "exact":
        return level
    series = df["ref_id"].astype(str) + ("|" + df["curve_id_dataset"].astype(str) if respect_series else "")
    for _, idx in df[df["fluence_n_per_cm2"].notna()].groupby(series).groups.items():
        values = np.sort(df.loc[idx, "fluence_n_per_cm2"].unique())
        cluster_start, mapping = values[0], {}
        for prev, v in zip(np.r_[values[0], values[:-1]], values):
            if v / prev > FLUENCE_TOLERANCE_FACTOR:
                cluster_start = v
            mapping[v] = cluster_start
        level.loc[idx] = df.loc[idx, "fluence_n_per_cm2"].map(mapping)
    return level


def geometry_class(r) -> str:
    if r.length_mm == 55 and r.width_mm == 10 and r.thickness_mm == 10:
        return "full-size (55x10x10 mm)"
    if r.length_mm == 55:
        return "sub-size, standard length (55 mm, reduced thickness)"
    return "miniature (reduced length)"


def product_form_group(r) -> str:
    if r.product_form in ("HAZ", "simulated HAZ"):
        return "HAZ (incl. simulated)"
    return r.product_form


def assign_curves(df: pd.DataFrame, fluence_treatment: str = "exact", respect_series: bool = True) -> pd.Series:
    """Curve ID for every record. IDs read '<ref>-<dataset series>[.<k>]' (k numbers the pieces of a split series in spreadsheet order)."""
    work = df.copy()
    work["fluence_level"] = fluence_levels(work, fluence_treatment, respect_series)
    work["composition_signature"] = work[COMPOSITION_FIELDS].round(6).astype(str).agg("|".join, axis=1)
    fields = CURVE_KEY_FIELDS if respect_series else [f for f in CURVE_KEY_FIELDS if f != "curve_id_dataset"]
    key = work[fields].astype(str).agg("||".join, axis=1)
    first_row = work.groupby(key)["source_row"].transform("min")
    series = work["curve_id_dataset"].map(lambda v: "none" if pd.isna(v) else f"{v:g}")
    base = work["ref_id"].astype(str) + "-" + (series if respect_series else "any")
    pieces = pd.DataFrame({"base": base, "key": key, "first_row": first_row}).drop_duplicates(["base", "key"])
    pieces = pieces.sort_values(["base", "first_row"])
    pieces["k"] = pieces.groupby("base").cumcount() + 1
    pieces["n_pieces"] = pieces.groupby("base")["k"].transform("max")
    pieces["curve_id"] = np.where(pieces["n_pieces"] > 1, pieces["base"] + "." + pieces["k"].astype(str), pieces["base"])
    return pd.Series(key.map(pieces.set_index("key")["curve_id"]).values, index=df.index)


# ---------------------------------------------------------------------------
# 3. Sampling descriptors (no fitting) and inclusion rules
# ---------------------------------------------------------------------------
def n_distinct_temperatures(t: np.ndarray) -> int:
    if len(t) == 0:
        return 0
    t = np.sort(t)
    return int(1 + np.sum(np.diff(t) > DISTINCT_TEMPERATURE_GAP_C))


def screening_references(e: np.ndarray, upper_points: int = UPPER_REFERENCE_POINTS) -> tuple:
    """(lowest measured energy, screening upper reference = mean of the highest `upper_points` measured energies). Screening quantities
    only: the screening upper reference is not an upper-shelf energy (D-037)."""
    return float(e.min()), float(np.sort(e)[-upper_points:].mean())


def describe_curve(s: pd.DataFrame, upper_points: int = UPPER_REFERENCE_POINTS) -> dict:
    t, e = s["test_temp_c"].to_numpy(float), s["energy_j"].to_numpy(float)
    e_lo, e_hi = screening_references(e, upper_points)
    pos = (e - e_lo) / (e_hi - e_lo) if e_hi > e_lo else np.zeros_like(e)
    lower, upper = pos <= BAND_LOWER, pos >= BAND_UPPER
    trans = ~lower & ~upper
    rho = float(pd.Series(t).rank().corr(pd.Series(e).rank())) if len(t) > 2 and np.ptp(t) > 0 and np.ptp(e) > 0 else np.nan
    return dict(n_points=len(s), n_temperatures=n_distinct_temperatures(t), T_min_c=t.min(), T_max_c=t.max(), T_span_c=np.ptp(t),
                E_min_j=e_lo, E_max_j=float(e.max()), E_screening_upper_reference_j=e_hi,
                energy_ratio_min_to_screening_upper=(e_lo / e_hi) if e_hi > 0 else np.nan,
                n_points_lower_band=int(lower.sum()), n_points_transition_band=int(trans.sum()), n_points_upper_band=int(upper.sum()),
                n_T_lower_band=n_distinct_temperatures(t[lower]), n_T_transition_band=n_distinct_temperatures(t[trans]),
                n_T_upper_band=n_distinct_temperatures(t[upper]), spearman_rho_T_E=rho,
                n_points_uncorroborated=int(s["flag_point_not_corroborated_by_duplicate_copies"].sum()))


def rule_failures(c: pd.Series, rule: dict) -> list:
    min_points = rule["min_points_irradiated"] if c["irradiated"] else rule["min_points_unirradiated"]
    fails = []
    if c["n_points"] < min_points:
        fails.append(f"points {c['n_points']} (needs >= {min_points})")
    if c["n_T_transition_band"] < rule["min_T_transition"]:
        fails.append(f"transition-band temperatures {c['n_T_transition_band']} (needs >= {rule['min_T_transition']})")
    if c["n_T_upper_band"] < rule["min_T_upper"] or c["n_points_upper_band"] < rule["min_points_upper"]:
        fails.append(f"upper band {c['n_points_upper_band']} points at {c['n_T_upper_band']} temperatures "
                     f"(needs >= {rule['min_points_upper']} points at >= {rule['min_T_upper']})")
    if c["n_T_lower_band"] < rule["min_T_lower"]:
        fails.append(f"lower-band temperatures {c['n_T_lower_band']} (needs >= {rule['min_T_lower']})")
    if not c["energy_ratio_min_to_screening_upper"] <= rule["max_energy_ratio"]:
        fails.append(f"lowest energy / screening upper reference {c['energy_ratio_min_to_screening_upper']:.2f} "
                     f"(needs <= {rule['max_energy_ratio']:.2f})")
    return fails


def sampling_class(c: pd.Series) -> str:
    """Plain description of what the points cover, using the primary thresholds (screening bands, not fitted shelves)."""
    r = RULES["primary"]
    if c["n_points"] < 3:
        return "too few points to describe"
    lower_ok = c["energy_ratio_min_to_screening_upper"] <= r["max_energy_ratio"]
    upper_ok = c["n_T_upper_band"] >= r["min_T_upper"]
    trans_ok = c["n_T_transition_band"] >= r["min_T_transition"]
    if lower_ok and upper_ok and trans_ok:
        return "brackets the transition in the screening bands (lower side, transition band and upper band sampled)"
    missing = [name for ok, name in [(lower_ok, "lower shelf not approached"), (trans_ok, "fewer than 2 transition-band temperatures"),
                                     (upper_ok, "upper band not sampled at 2 temperatures")] if not ok]
    return "; ".join(missing)


def build_inventory(df: pd.DataFrame) -> pd.DataFrame:
    steps_per_curve = df.groupby("curve_id")["population_step"].nunique()
    if (steps_per_curve > 1).any():
        raise AssertionError(f"Curves spanning more than one population: {sorted(steps_per_curve[steps_per_curve > 1].index)}")
    rows = []
    for cid, s in df.groupby("curve_id", sort=False):
        first = s.iloc[0]
        row = dict(curve_id=cid, ref_id=int(first.ref_id), ref_year=int(first.ref_year),
                   dataset_series=("none" if pd.isna(first.curve_id_dataset) else f"{first.curve_id_dataset:g}"),
                   population=first.population, population_step=first.population_step,
                   condition_label_contradicted_by_source=first.flag_condition_label_contradicted_by_source,
                   material_family=first.material_family, material_std=first.material_std, product_form=first.product_form,
                   product_form_group=product_form_group(first), product_form_basis=first.product_form_basis,
                   product_form_uncertain=bool(s["flag_title_reports_weld_or_haz_not_identified_in_records"].any()),
                   geometry=first.geometry_label, geometry_class=geometry_class(first),
                   notch_reported=bool(pd.notna(first.notch_depth_mm)), orientation=first.orientation,
                   irradiated=bool(first.irradiated_resolved), fluence_n_per_cm2=first.fluence_n_per_cm2,
                   irradiation_temp_c=first.irradiation_temp_c, treatment=first.treatment,
                   test_condition_statement=first.test_condition_statement,
                   reconstituted=bool(first.tag_reconstituted_specimen),
                   irradiation_label_check=first.irradiation_label_check, irradiated_in_other_release=first.irradiated_in_other_release,
                   specimen_type_check=first.specimen_type_check,
                   retained_chosen_keep_rule=bool(first.retained_chosen_keep_rule), retained_alt_keep_rule=bool(first.retained_alt_keep_rule),
                   dataset_use_j=first.use_j_dataset, dataset_dbtt_c=first.dbtt_c_dataset,
                   first_source_row=int(s["source_row"].min()), record_ids=" ".join(s["record_id"]))
        row.update(describe_curve(s))
        rows.append(row)
    inv = pd.DataFrame(rows)
    inv["sampling_class"] = inv.apply(sampling_class, axis=1)
    for name, rule in RULES.items():
        fails = inv.apply(lambda c: rule_failures(c, rule), axis=1)
        inv[f"passes_{name}"] = fails.map(len).eq(0)
        inv[f"fails_{name}"] = fails.map("; ".join)
    primary_pop = inv["population"].eq(PRIMARY_POPULATION)
    chosen, alt = inv["retained_chosen_keep_rule"], inv["retained_alt_keep_rule"]
    inv["cohort_primary"] = primary_pop & chosen & inv["passes_primary"]
    inv["cohort_looser"] = primary_pop & chosen & inv["passes_looser"]
    inv["cohort_stricter"] = primary_pop & chosen & inv["passes_stricter"]
    inv["cohort_alt_keep_rule"] = primary_pop & alt & inv["passes_primary"]
    inv["cohort_plus_unresolved_irradiation"] = (primary_pop | inv["population_step"].eq("P3")) & chosen & inv["passes_primary"]
    inv["cohort_plus_additively_manufactured"] = (primary_pop | inv["population_step"].eq("P5")) & chosen & inv["passes_primary"]
    inv["cohort_piping_secondary"] = inv["population_step"].eq("P4") & chosen & inv["passes_primary"]
    return inv.sort_values(["ref_id", "first_source_row"]).reset_index(drop=True)


# ---------------------------------------------------------------------------
# 4. Accounting tables
# ---------------------------------------------------------------------------
def population_accounting(df: pd.DataFrame, wp1: pd.DataFrame) -> pd.DataFrame:
    chosen = df[df["retained_chosen_keep_rule"]]
    rows = [dict(step="Start", criterion="Records retained by WP1 (canonical keep rule)", basis="outputs/wp1*/reconciliation_table.md",
                 records=len(chosen), curves=chosen["curve_id"].nunique(), references=chosen["ref_id"].nunique())]
    for step, text, basis in POPULATION_STEPS:
        s = chosen[chosen["population_step"] == step]
        rows.append(dict(step=step, criterion=text, basis=basis, records=len(s), curves=s["curve_id"].nunique(),
                         references=s["ref_id"].nunique()))
    p = chosen[chosen["population"] == PRIMARY_POPULATION]
    rows.append(dict(step="End", criterion=PRIMARY_POPULATION, basis="", records=len(p), curves=p["curve_id"].nunique(),
                     references=p["ref_id"].nunique()))
    out = pd.DataFrame(rows)
    if out.loc[1:5, "records"].sum() + out.loc[6, "records"] != out.loc[0, "records"]:
        raise AssertionError("Population accounting does not close")
    if len(wp1[wp1["status"] == "retained"]) != out.loc[0, "records"]:
        raise AssertionError("WP2 start count differs from WP1 retained count")
    return out


def rule_outcomes(inv: pd.DataFrame) -> pd.DataFrame:
    base = inv[inv["population"].eq(PRIMARY_POPULATION) & inv["retained_chosen_keep_rule"]]
    rows = [dict(rule="before inclusion filtering", curves=len(base), records=int(base["n_points"].sum()), curves_lost=0, records_lost=0,
                 median_points=float(base["n_points"].median()), median_T_span_c=float(base["T_span_c"].median()),
                 median_transition_temperatures=float(base["n_T_transition_band"].median()))]
    for name in RULES:
        k = base[base[f"passes_{name}"]]
        rows.append(dict(rule=name, curves=len(k), records=int(k["n_points"].sum()), curves_lost=len(base) - len(k),
                         records_lost=int(base["n_points"].sum() - k["n_points"].sum()), median_points=float(k["n_points"].median()),
                         median_T_span_c=float(k["T_span_c"].median()), median_transition_temperatures=float(k["n_T_transition_band"].median())))
    return pd.DataFrame(rows)


def outcomes_by_group(inv: pd.DataFrame) -> pd.DataFrame:
    base = inv[inv["population"].eq(PRIMARY_POPULATION) & inv["retained_chosen_keep_rule"]].copy()
    base["irradiation"] = np.where(base["irradiated"], "irradiated", "unirradiated")
    frames = []
    for dim in ["material_family", "product_form_group", "irradiation", "geometry_class"]:
        g = base.groupby(dim)
        t = pd.DataFrame({"curves_before": g.size(), "records_before": g["n_points"].sum()})
        for name in RULES:
            t[f"curves_{name}"] = g[f"passes_{name}"].sum()
            t[f"records_{name}"] = base[base[f"passes_{name}"]].groupby(dim)["n_points"].sum()
        t = t.fillna(0).astype(int).reset_index().rename(columns={dim: "group"})
        t.insert(0, "dimension", dim)
        frames.append(t)
    return pd.concat(frames, ignore_index=True)


def criterion_failures(inv: pd.DataFrame) -> pd.DataFrame:
    base = inv[inv["population"].eq(PRIMARY_POPULATION) & inv["retained_chosen_keep_rule"]]
    rows = []
    for name, rule in RULES.items():
        min_pts = np.where(base["irradiated"], rule["min_points_irradiated"], rule["min_points_unirradiated"])
        checks = {"points": base["n_points"] < min_pts,
                  "transition temperatures": base["n_T_transition_band"] < rule["min_T_transition"],
                  "upper band": (base["n_T_upper_band"] < rule["min_T_upper"]) | (base["n_points_upper_band"] < rule["min_points_upper"]),
                  "lower band temperatures": base["n_T_lower_band"] < rule["min_T_lower"],
                  "energy ratio": ~(base["energy_ratio_min_to_screening_upper"] <= rule["max_energy_ratio"])}
        for crit, hit in checks.items():
            rows.append(dict(rule=name, criterion=crit, curves_failing=int(hit.sum()),
                             curves_failing_only_this=int((hit & (sum(v.astype(int) for v in checks.values()) == 1)).sum())))
    return pd.DataFrame(rows)


def series_splits(df: pd.DataFrame) -> pd.DataFrame:
    chosen = df[df["retained_chosen_keep_rule"] & df["curve_id_dataset"].notna()]
    fields = [f for f in CURVE_KEY_FIELDS if f not in SOURCE_FIELDS]
    rows = []
    for (ref, series), s in chosen.groupby(["ref_id", "curve_id_dataset"]):
        if s["curve_id"].nunique() < 2:
            continue
        work = s.assign(fluence_level=s["fluence_n_per_cm2"],
                        composition_signature=s[COMPOSITION_FIELDS].round(6).astype(str).agg("|".join, axis=1))
        varying = [f for f in fields if work[f].astype(str).nunique() > 1]
        rows.append(dict(ref_id=int(ref), dataset_series=f"{series:g}", records=len(s), curves=s["curve_id"].nunique(),
                         split_by=", ".join(varying),
                         pieces="; ".join(f"{cid} ({n})" for cid, n in s.groupby("curve_id").size().items())))
    return pd.DataFrame(rows, columns=["ref_id", "dataset_series", "records", "curves", "split_by", "pieces"])


def screening_upper_reference_diagnostic(df: pd.DataFrame, inv: pd.DataFrame) -> pd.DataFrame:
    """D-037 history: rule outcomes if the screening upper reference were the single highest energy (the first definition tried in WP2)."""
    base = inv[inv["population"].eq(PRIMARY_POPULATION) & inv["retained_chosen_keep_rule"]]
    rows = []
    for label, k in [("mean of the three highest energies (adopted)", UPPER_REFERENCE_POINTS), ("single highest energy (superseded)", 1)]:
        desc = pd.DataFrame([dict(curve_id=cid, irradiated=bool(g["irradiated_resolved"].iloc[0]), **describe_curve(g, k))
                             for cid, g in df[df["curve_id"].isin(base["curve_id"])].groupby("curve_id")])
        for name, rule in RULES.items():
            ok = desc.apply(lambda c: not rule_failures(c, rule), axis=1)
            rows.append(dict(screening_upper_reference=label, rule=name, curves=int(ok.sum()), records=int(desc.loc[ok, "n_points"].sum())))
    return pd.DataFrame(rows)


def cohort_tables(inv: pd.DataFrame) -> tuple:
    """Explicit cohort files (D-039): membership (one row per cohort and curve, with the tags later work packages must carry and the
    record IDs) and a manifest whose SHA-256 fingerprint covers each cohort's curve IDs and their record IDs."""
    members, manifest = [], []
    for c, (role, definition) in COHORTS.items():
        m = inv[inv[f"cohort_{c}"]]
        lines = sorted(f"{cid}:{' '.join(sorted(recs.split()))}" for cid, recs in zip(m["curve_id"], m["record_ids"]))
        manifest.append(dict(cohort=c, role=role, definition=definition, curves=len(m), records=int(m["n_points"].sum()),
                             membership_sha256=hashlib.sha256("\n".join(lines).encode()).hexdigest()))
        members.append(m[["curve_id", "ref_id", "population_step", "product_form", "reconstituted", "irradiated", "irradiation_label_check",
                          "geometry_class", "n_points", "record_ids"]].assign(cohort=c))
    membership = pd.concat(members, ignore_index=True)
    return membership[["cohort"] + [col for col in membership.columns if col != "cohort"]], pd.DataFrame(manifest)


def verify_frozen_cohorts(manifests: dict) -> None:
    """Stop if any cohort's membership differs from the one frozen at CP2 (FROZEN_COHORTS). Changing a frozen cohort requires an approved,
    logged decision and an edit of that file in the same commit (D-039)."""
    if not FROZEN_COHORTS.exists():
        raise RuntimeError(f"{FROZEN_COHORTS.relative_to(DATA.parent)} is missing: the CP2-frozen cohorts cannot be verified.")
    frozen = pd.read_csv(FROZEN_COHORTS, dtype={"membership_sha256": str})
    now = pd.concat([m.assign(release=key) for key, m in manifests.items()], ignore_index=True)
    merged = frozen.merge(now, on=["release", "cohort"], how="outer", suffixes=("_frozen", "_now"), indicator=True)
    differs = merged[(merged["_merge"] != "both") | (merged["curves_frozen"] != merged["curves_now"])
                     | (merged["records_frozen"] != merged["records_now"]) | (merged["membership_sha256_frozen"] != merged["membership_sha256_now"])]
    if len(differs):
        raise RuntimeError("WP2 cohort membership differs from the CP2-frozen cohorts in data/FROZEN_COHORTS_CP2.csv: "
                           + "; ".join(f"{r.release} {r.cohort}: frozen {r.curves_frozen}/{r.records_frozen}, now {r.curves_now}/{r.records_now}"
                                       for r in differs.itertuples(index=False))
                           + ". A frozen cohort changes only through an approved decision logged in DECISIONS.md.")
    print(f"Frozen-cohort check passed: {len(now)} cohorts match data/FROZEN_COHORTS_CP2.csv")


def fluence_by_source(df: pd.DataFrame) -> tuple:
    """Inspection table for D-036: every reported irradiation condition, by source."""
    irr = df[df["retained_chosen_keep_rule"] & df["irradiated_resolved"]]
    table = (irr.groupby(["ref_id", "irradiation_label_check", "fluence_n_per_cm2", "irradiation_temp_c", "irradiation_time_h"], dropna=False)
             .agg(records=("record_id", "size"),
                  dataset_series=("curve_id_dataset", lambda v: ", ".join("none" if pd.isna(x) else f"{x:g}" for x in pd.unique(v))),
                  curves=("curve_id", lambda v: ", ".join(pd.unique(v))),
                  populations=("population_step", lambda v: ", ".join(sorted({x or "primary" for x in v}))))
             .reset_index())
    per_series = irr[irr["curve_id_dataset"].notna()].groupby(["ref_id", "curve_id_dataset"])["fluence_n_per_cm2"].nunique(dropna=False)
    facts = dict(irradiated_records=len(irr), with_fluence=int(irr["fluence_n_per_cm2"].notna().sum()),
                 with_irradiation_temperature=int(irr["irradiation_temp_c"].notna().sum()),
                 series_with_more_than_one_fluence_value=int((per_series > 1).sum()),
                 fluence_min=float(irr["fluence_n_per_cm2"].min()), fluence_max=float(irr["fluence_n_per_cm2"].max()))
    return table, facts


def fluence_treatment_comparison(df: pd.DataFrame) -> pd.DataFrame:
    chosen = df[df["retained_chosen_keep_rule"]].copy()
    variants = {"exact reported value (primary)": ("exact", True),
                "within a factor of 1.2 (alternative)": ("tolerance", True),
                "diagnostic: exact value, dataset series ignored": ("exact", False),
                "diagnostic: within a factor of 1.2, dataset series ignored": ("tolerance", False)}
    reference = chosen["curve_id"]  # the inventory's own curve IDs
    ref_partition = chosen.groupby(reference)["record_id"].apply(frozenset)
    rows = []
    for name, (treatment, respect) in variants.items():
        ids = assign_curves(chosen, treatment, respect)
        partition = chosen.groupby(ids)["record_id"].apply(frozenset)
        merged = [sorted(set(reference[chosen["record_id"].isin(p)])) for p in partition if len(set(reference[chosen["record_id"].isin(p)])) > 1]
        rows.append(dict(fluence_treatment=name, curves=len(partition),
                         identical_to_primary=set(partition) == set(ref_partition),
                         primary_curves_merged=" | ".join(" + ".join(m) for m in merged) or "none"))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 5. Driver
# ---------------------------------------------------------------------------
def summary_markdown(key, df, inv, pop, rules, bygroup, crit, splits, flu, wp1, flu_src, flu_facts) -> str:
    ds = DATASETS[key]
    base = inv[inv["population"].eq(PRIMARY_POPULATION) & inv["retained_chosen_keep_rule"]]
    e8 = wp1[wp1["exclusion_step"] == "E8"]
    L = [f"# WP2 summary ({key})", "", f"Dataset: {ds['label']}", "",
         "Analysis of published Charpy V-notch test data. Nothing is fitted in WP2; the dataset's USE, DBTT and curve IDs are provenance only.", "",
         "## 1. What one transition curve is (D-032, D-033)", "",
         "Records form one curve only if they come from the same source publication and the same dataset series, and agree on every field below; "
         "a dataset series is split wherever any of these fields differs. Blank values count as their own value (never filled in).", "",
         md_table(pd.DataFrame([
             dict(group="source", fields=", ".join(SOURCE_FIELDS), reason="different laboratories and figure series are never pooled into one curve"),
             dict(group="material and heat", fields=", ".join(MATERIAL_FIELDS), reason="specification/class, heat chemistry (heat proxy) and product form change toughness"),
             dict(group="specimen geometry", fields=", ".join(GEOMETRY_FIELDS), reason="size, notch and orientation change absorbed energy and the transition"),
             dict(group="irradiation", fields=", ".join(IRRADIATION_FIELDS), reason="neutron exposure and its temperature shift the transition"),
             dict(group="material / specimen condition", fields=", ".join(CONDITION_FIELDS), reason="heat treatment, HAZ zone, reconstitution, welded area, loading rate"),
         ])), "",
         "## 2. Population accounting (records retained by WP1 -> primary RPV population)", "",
         "Every record is counted once, at the first step that applies. Nothing is deleted: excluded and secondary records keep curve IDs.", "",
         md_table(pop), "",
         "## 3. Curve inventory before inclusion filtering (primary population)", "",
         f"- Curves: {len(base)}; records: {int(base['n_points'].sum())}; references: {base['ref_id'].nunique()}.",
         f"- Points per curve: median {base['n_points'].median():.0f}, 10th-90th percentile {base['n_points'].quantile(.1):.0f}-{base['n_points'].quantile(.9):.0f}, "
         f"range {base['n_points'].min()}-{base['n_points'].max()}.",
         f"- Temperature span per curve: median {base['T_span_c'].median():.0f} °C, 10th-90th percentile {base['T_span_c'].quantile(.1):.0f}-{base['T_span_c'].quantile(.9):.0f} °C.",
         f"- Distinct test temperatures in the transition band: median {base['n_T_transition_band'].median():.0f}; curves with none: {int((base['n_T_transition_band'] == 0).sum())}.",
         f"- Spearman rank correlation of energy with temperature below 0.7 (diagnostic only): {int((base['spearman_rho_T_E'] < 0.7).sum())} curves.", "",
         "What the points cover (primary thresholds):", "",
         md_table(base.groupby("sampling_class").agg(curves=("curve_id", "size"), records=("n_points", "sum")).reset_index()), "",
         "Points per curve:", "",
         md_table(pd.cut(base["n_points"], [0, 4, 5, 7, 9, 11, 14, 19, 29, 1000], labels=["1-4", "5", "6-7", "8-9", "10-11", "12-14", "15-19", "20-29", "30+"])
                  .value_counts().sort_index().rename_axis("points").reset_index(name="curves")), "",
         "## 4. Pre-fit screening rules (D-038)", "",
         "**What passing means.** A curve that passes a rule appears sufficiently sampled to *attempt* a transition-curve fit in WP3. "
         "Passing does not show that a tanh fit will converge, be well conditioned or give physically reasonable parameters, nor that the "
         "curve is scientifically valid; a curve whose WP3 fit fails is reported as a failure, never silently removed.", "",
         f"**Screening references and bands (D-037).** Lower reference = lowest measured energy; screening upper reference = mean of the "
         f"{UPPER_REFERENCE_POINTS} highest measured energies. The screening upper reference is not an upper-shelf energy (USE); USE is "
         f"estimated in WP3. Transition band = {BAND_LOWER:.2f}-{BAND_UPPER:.2f} of the rise between the references: for the normalized tanh "
         "y = (1 + tanh x) / 2, y = 0.119 at x = -1 and 0.881 at x = +1, so the band is T0 - C to T0 + C. This is a project-defined, "
         "model-based convention, not an ASTM requirement. The stricter rule's specimen counts are historical ASTM E185-82 surveillance "
         "guidance, used as a deliberately conservative comparison.", "",
         md_table(pd.DataFrame([dict(rule=name, **rule) for name, rule in RULES.items()])), "",
         md_table(pd.DataFrame([dict(criterion=k, basis=v) for k, v in RULE_BASIS.items()])), "",
         "## 5. What each rule keeps", "", md_table(rules), "",
         "Curves failing each criterion (a curve can fail several):", "", md_table(crit), "",
         "By material family, product form, irradiation status and geometry:", "", md_table(bygroup), "",
         "## 6. Cohorts carried forward (D-039)", "",
         "Membership is frozen at CP2: explicit files `cohort_membership.csv` and `cohort_manifest.csv`, checked on every run against "
         "`data/FROZEN_COHORTS_CP2.csv`. Later work packages read these cohorts; they do not regenerate them with other thresholds.", "",
         md_table(pd.DataFrame([dict(cohort=c, role=role, definition=d, curves=int(inv[f"cohort_{c}"].sum()),
                                     records=int(inv.loc[inv[f'cohort_{c}'], 'n_points'].sum())) for c, (role, d) in COHORTS.items()])), "",
         "## 7. Accounting of special cases", "",
         f"- Duplicated (WP1 E8, D-019): {e8['duplicate_comparison_unit'].nunique()} series, {len(e8)} records removed as republications. "
         f"Curves that exist under only one of the two keep rules: {int((inv['retained_chosen_keep_rule'] != inv['retained_alt_keep_rule']).sum())}; "
         f"primary-cohort curves replaced when the alternative keep rule is used: {sorted(set(inv.loc[inv['cohort_primary'], 'curve_id']) - set(inv.loc[inv['cohort_alt_keep_rule'], 'curve_id']))} "
         f"-> {sorted(set(inv.loc[inv['cohort_alt_keep_rule'], 'curve_id']) - set(inv.loc[inv['cohort_primary'], 'curve_id']))}.",
         f"- Out of scope (WP1): E1 austenitic stainless {int((wp1['exclusion_step'] == 'E1').sum())} records; E2 15Cr2MoV-A {int((wp1['exclusion_step'] == 'E2').sum())} records.",
         f"- Ambiguous or contradicted labels (population steps above): specimen type not supported {int(pop.loc[pop['step'] == 'P1', 'records'].iloc[0])} records; "
         f"condition label contradicted by source {int(pop.loc[pop['step'] == 'P2', 'records'].iloc[0])}; irradiation status unresolved "
         f"{int(pop.loc[pop['step'] == 'P3', 'records'].iloc[0])}.",
         f"- Piping (secondary): {int(pop.loc[pop['step'] == 'P4', 'records'].iloc[0])} records; additively manufactured (secondary): "
         f"{int(pop.loc[pop['step'] == 'P5', 'records'].iloc[0])} records.",
         "- Curves excluded because the source contradicts their condition labels (P2, D-031). Measurements and labels are unchanged; "
         "the exact reason is kept per record and per curve:", "",
         md_table(inv.loc[inv["population_step"].eq("P2") & inv["retained_chosen_keep_rule"],
                          ["curve_id", "n_points", "irradiated", "treatment", "test_condition_statement", "condition_label_contradicted_by_source"]]), "",
         f"- Mixed dataset series split into more than one curve: {len(splits)} series ({int(splits['records'].sum()) if len(splits) else 0} records):", "",
         md_table(splits), "",
         "Special conditions inside the primary cohort (each forms its own curves; none is excluded for being special):", "",
         md_table(special_conditions(df, inv)), "",
         "Primary-population curves rejected by the primary rule:", "",
         md_table(base.loc[~base["passes_primary"], ["curve_id", "material_family", "product_form", "geometry", "irradiated", "n_points",
                                                       "n_T_transition_band", "n_T_upper_band", "energy_ratio_min_to_screening_upper",
                                                       "fails_primary"]]
                  .round(2)), "",
         "## 8. Fluence treatment (D-036)", "",
         f"Irradiated records retained by WP1: {flu_facts['irradiated_records']}; with a fluence value: {flu_facts['with_fluence']}; with an "
         f"irradiation temperature: {flu_facts['with_irradiation_temperature']}; fluence range {flu_facts['fluence_min']:.3g} to "
         f"{flu_facts['fluence_max']:.3g} n/cm²; dataset series containing more than one fluence value: "
         f"{flu_facts['series_with_more_than_one_fluence_value']}.", "",
         "Fluence never varies within a dataset series and curves never cross series, so the fluence treatment can only matter where a "
         "source has no series IDs (ref 104, whose levels are at least 1.8x apart). The diagnostics show what would merge if the series "
         "boundary were ignored.", "", md_table(flu), "",
         "Every reported irradiation condition (population column: primary or the excluding step):", "", md_table(flu_src), ""]
    return "\n".join(L)


def special_conditions(df: pd.DataFrame, inv: pd.DataFrame) -> pd.DataFrame:
    cohort = df[df["curve_id"].isin(inv.loc[inv["cohort_primary"], "curve_id"])]
    conditions = {"reconstituted specimens": cohort["tag_reconstituted_specimen"], "simulated HAZ": cohort["tag_simulated_haz"],
                  "HAZ (test condition statement)": cohort["tag_haz_statement"], "post-weld heat treatment": cohort["tag_pwht"],
                  "step cooled": cohort["tag_step_cooled"], "pre-strained": cohort["tag_prestrained"],
                  "standard reference material": cohort["tag_standard_reference_material"],
                  "deliberately embrittled JSPS steel (refs 43, 44)": cohort["ref_id"].isin([43, 44]) & cohort["material_family"].eq("A533B"),
                  "laboratory heats / model alloys (title)": cohort["ref_material_note"].fillna("").str.contains("lab|model", case=False),
                  "product form uncertain (title reports weld/HAZ)": cohort["flag_title_reports_weld_or_haz_not_identified_in_records"],
                  "notch dimensions not reported": cohort["flag_notch_dimensions_not_reported"].astype(bool)}
    return pd.DataFrame([dict(condition=k, curves=cohort.loc[v.astype(bool), "curve_id"].nunique(), records=int(v.astype(bool).sum()))
                         for k, v in conditions.items()])


def run(key: str):
    tag = "" if key == PRIMARY_DATASET else f"_sensitivity_{key}"
    run_name = "primary" if key == PRIMARY_DATASET else f"sensitivity_{key}"
    out = OUTPUTS / f"wp2{tag}"
    out.mkdir(parents=True, exist_ok=True)
    wp1 = pd.read_csv(PROCESSED / run_name / "charpy_records_with_status.csv", low_memory=False)
    df = assign_population(load_records(run_name))
    df["curve_id"] = assign_curves(df)
    inv = build_inventory(df)
    cohort_cols = [c for c in inv.columns if c.startswith("cohort_")]
    df = df.merge(inv[["curve_id", "sampling_class", "passes_looser", "passes_primary", "passes_stricter"] + cohort_cols], on="curve_id", how="left")
    record_cols = (["record_id", "source_row", "curve_id", "population", "population_step", "population_all_applicable",
                    "retained_chosen_keep_rule", "retained_alt_keep_rule", "sampling_class", "passes_looser", "passes_primary", "passes_stricter"]
                   + cohort_cols)
    df[record_cols + [c for c in df.columns if c not in record_cols]].to_csv(PROCESSED / run_name / "charpy_records_with_curves.csv", index=False)
    inv.to_csv(out / "curve_inventory.csv", index=False)
    pop = population_accounting(df, wp1)
    pop.to_csv(out / "population_accounting.csv", index=False)
    rules = rule_outcomes(inv)
    rules.to_csv(out / "rule_outcomes.csv", index=False)
    bygroup = outcomes_by_group(inv)
    bygroup.to_csv(out / "rule_outcomes_by_group.csv", index=False)
    crit = criterion_failures(inv)
    splits = series_splits(df)
    splits.to_csv(out / "dataset_series_splits.csv", index=False)
    flu = fluence_treatment_comparison(df)
    flu.to_csv(out / "fluence_treatments.csv", index=False)
    flu_src, flu_facts = fluence_by_source(df)
    screening_upper_reference_diagnostic(df, inv).to_csv(out / "screening_upper_reference_diagnostic.csv", index=False)
    flu_src.to_csv(out / "fluence_by_source.csv", index=False)
    membership, manifest = cohort_tables(inv)
    membership.to_csv(out / "cohort_membership.csv", index=False)
    manifest.to_csv(out / "cohort_manifest.csv", index=False)
    write_text(out / "wp2_summary.md", summary_markdown(key, df, inv, pop, rules, bygroup, crit, splits, flu, wp1, flu_src, flu_facts))
    print(f"WP2 ({key}): {len(inv)} curves; primary cohort {int(inv['cohort_primary'].sum())} curves -> {out}")
    return df, inv, manifest


def version_comparison(inv_p: pd.DataFrame, inv_s: pd.DataFrame) -> None:
    """Match curves of the two releases by their record sets (spreadsheet rows are aligned for refs 1-106)."""
    def by_records(inv):
        return {frozenset(r.split()): row for r, row in zip(inv["record_ids"], inv.itertuples(index=False))}
    p, s = by_records(inv_p), by_records(inv_s)
    rows = []
    for recs in sorted(set(p) | set(s), key=lambda k: min(k)):
        a, b = p.get(recs), s.get(recs)
        ref = (a or b).ref_id
        if a is None or b is None:
            change = "curve only in 2025.30" if b is None else "curve only in 2024.206"
            if ref > 106 and b is None:
                change = "reference only in 2025.30 (refs 107-109)"
        else:
            diffs = [f for f in ["population", "irradiated", "treatment", "orientation", "product_form", "passes_primary", "cohort_primary"]
                     if str(getattr(a, f)) != str(getattr(b, f))]
            if not diffs:
                continue
            change = "differs: " + ", ".join(diffs)
        rows.append(dict(ref_id=ref, curve_2025=getattr(a, "curve_id", ""), curve_2024=getattr(b, "curve_id", ""), records=len(recs),
                         change=change, cohort_primary_2025=getattr(a, "cohort_primary", ""), cohort_primary_2024=getattr(b, "cohort_primary", "")))
    comp = pd.DataFrame(rows, columns=["ref_id", "curve_2025", "curve_2024", "records", "change", "cohort_primary_2025", "cohort_primary_2024"])
    comp.to_csv(OUTPUTS / "wp2" / "version_sensitivity_comparison.csv", index=False)
    cohorts = [c for c in inv_p.columns if c.startswith("cohort_")]
    totals = pd.DataFrame([dict(cohort=c.replace("cohort_", ""),
                                curves_2025=int(inv_p[c].sum()), records_2025=int(inv_p.loc[inv_p[c], "n_points"].sum()),
                                curves_2024=int(inv_s[c].sum()), records_2024=int(inv_s.loc[inv_s[c], "n_points"].sum())) for c in cohorts])
    summary = comp.groupby("change").agg(curves=("records", "size"), records=("records", "sum")).reset_index() if len(comp) else comp
    write_text(OUTPUTS / "wp2" / "version_sensitivity_comparison.md",
               "# WP2 version sensitivity: 2025.30 (primary) versus 2024.206\n\n"
               "Curves are matched by their exact record sets. Measurements are identical in the two releases for refs 1-106 (WP0); "
               "differences come from refs 107-109 and from metadata the releases label differently.\n\n"
               "## Cohort sizes\n\n" + md_table(totals) + "\n\n## Curves that differ\n\n" + md_table(summary) + "\n\n" + md_table(comp))


# Teaching examples for checkpoint CP2 (illustration only; no number in any analysis depends on this choice). Each was chosen by
# eye to show one outcome clearly, and the assertion below stops the run if a later change alters its rule outcome.
EXAMPLE_CURVES = [
    ("3-14", "valid: passes all three rules", (True, True, True)),
    ("54-247", "borderline: passes primary, fails stricter", (True, True, False)),
    ("11-47", "rejected: fails primary", (True, False, False)),
]


def example_figure(df: pd.DataFrame, inv: pd.DataFrame) -> None:
    import textwrap

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 5.0))
    for ax, (cid, title, expected) in zip(axes, EXAMPLE_CURVES):
        c = inv.set_index("curve_id").loc[cid]
        outcome = (bool(c["passes_looser"]), bool(c["passes_primary"]), bool(c["passes_stricter"]))
        if outcome != expected:
            raise AssertionError(f"Example curve {cid} no longer illustrates '{title}': (looser, primary, stricter) = {outcome}")
        s = df[df["curve_id"] == cid]
        e_lo, e_hi = c["E_min_j"], c["E_screening_upper_reference_j"]
        lo, hi = e_lo + BAND_LOWER * (e_hi - e_lo), e_lo + BAND_UPPER * (e_hi - e_lo)
        ax.axhspan(lo, hi, color="0.87", zorder=0, label="transition band (12-88 % of rise; T0 ± C of a tanh)")
        ax.axhline(e_hi, color="0.4", lw=0.8, ls="--", zorder=1, label="screening upper reference (mean of 3 highest; not USE)")
        ax.scatter(s["test_temp_c"], s["energy_j"], s=24, facecolor="white", edgecolor="black", zorder=2, label="published test data")
        ax.set_title(f"{title}\ncurve {cid}: ref {c['ref_id']}, {c['material_family']} {c['product_form']}, {c['n_points']} points", fontsize=8.5)
        ax.set_xlabel("Test temperature (°C)")
        ax.set_ylabel("Absorbed energy (J)")
        lines = [f"temperatures in lower/transition/upper band: {c['n_T_lower_band']}/{c['n_T_transition_band']}/{c['n_T_upper_band']}",
                 f"lowest energy / screening upper reference: {c['energy_ratio_min_to_screening_upper']:.2f}",
                 ("fails primary: " + c["fails_primary"] if isinstance(c["fails_primary"], str) and c["fails_primary"]
                  else "fails stricter: " + c["fails_stricter"] if isinstance(c["fails_stricter"], str) and c["fails_stricter"]
                  else "meets every criterion")]
        ax.text(0.0, -0.3, "\n".join(textwrap.fill(line, 50) for line in lines), transform=ax.transAxes, fontsize=7, va="top")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.93), ncol=3, fontsize=7.5, frameon=False)
    fig.suptitle("WP2 pre-fit screening rules illustrated on published Charpy V-notch data (no curve fitted)", fontsize=9.5)
    fig.tight_layout(rect=(0, 0.08, 1, 0.9))
    fig.savefig(OUTPUTS / "wp2" / "example_curves.png", dpi=150, metadata={"Software": None})
    plt.close(fig)


if __name__ == "__main__":
    df_p, inv_p, manifest_p = run(PRIMARY_DATASET)
    _, inv_s, manifest_s = run(SENSITIVITY_DATASET)
    version_comparison(inv_p, inv_s)
    example_figure(df_p, inv_p)
    verify_frozen_cohorts({PRIMARY_DATASET: manifest_p, SENSITIVITY_DATASET: manifest_s})
