"""WP7 - Technical report: number registry, substitution, lint, claim map and PDF.

The report's prose lives in `report/report.md` and contains NO literal result numbers
(DECISIONS.md D-114). Every numeric claim is a placeholder resolved here from a table that
WP0-WP6 regenerated, so that PROJECT_BRIEF.md 6.1 ("every numeric claim traceable to code")
and 10 ("no number appears that the repository cannot regenerate") hold mechanically rather
than by promise.

Outputs, all into `report/`:
  report_filled.md            the prose with every number substituted (a readable diff target)
  claim_source_map.csv        one row per numeric claim: value, file, row selector, column
  charpy_test_matrix_study.pdf  the deliverable (D-113)

The build FAILS, with a non-zero exit, on: an unresolved placeholder; a registry entry that
the prose never uses; a row selector matching other than exactly one row; a figure or table
without an evidence class (D-117); a forbidden phrase (D-116); or a digit in the prose outside
a placeholder, a rendered table or a marked protected span (D-114).

WP7 changes no WP0-WP6 code, output, cohort or decision (D-118); this module only reads them.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from common import OUTPUTS, ROOT

REPORT = ROOT / "report"
SOURCE = REPORT / "report.md"

# --------------------------------------------------------------------------------------
# 1. The registry: one entry per numeric claim (D-114)
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Lookup:
    """One value read from one cell of one generated table."""
    file: str                       # relative to outputs/
    where: dict                     # column -> value; must select exactly one row
    col: str
    fmt: str = "{:g}"
    note: str = ""


@dataclass(frozen=True)
class Derived:
    """A value computed from other registry keys. The expression and the inputs are printed
    in claim_source_map.csv so the arithmetic is auditable (D-114, D-123)."""
    expr: str                       # python expression over the names in `inputs`
    inputs: dict = field(default_factory=dict)   # name -> registry key
    fmt: str = "{:g}"
    note: str = ""


@dataclass(frozen=True)
class Agg:
    """A count or simple statistic over the rows of one generated table that match `where`."""
    file: str
    where: dict                     # column -> value, or column -> list of accepted values
    op: str                         # count | sum | min | max | median | nunique
    col: str = ""                   # ignored for count
    fmt: str = "{:g}"
    note: str = ""


@dataclass(frozen=True)
class Calc:
    """A named, whitelisted function of one generated table, for structural questions a
    filter cannot express (for example: the smallest budget at which one side wins every
    comparison). The function's source is printed in claim_source_map.csv."""
    file: str
    fn: str                         # key into CALCS
    fmt: str = "{:g}"
    note: str = ""


# Whitelisted table functions. Each is one readable expression so the claim map can print it.
CALCS: dict[str, tuple[str, object]] = {
    "min_k_full_size_sweeps": (
        "smallest k at which every T1 comparison is FULL-SIZE WINS",
        lambda d: min(k for k, g in d.groupby("k_budget") if (g.winner == "FULL-SIZE WINS").all())),
    "min_k_no_miniature_win": (
        "smallest k at which no T1 comparison is MINIATURE WINS",
        lambda d: min(k for k, g in d.groupby("k_budget") if not (g.winner == "MINIATURE WINS").any())),
    "n_geometries": ("distinct miniature geometries compared", lambda d: d.geom_code.nunique()),
    "n_archetypes": ("distinct true-curve archetypes", lambda d: d.archetype_id.nunique()),
}


def L(file, where, col, fmt="{:g}", note=""):
    return Lookup(file, where, col, fmt, note)


def D(expr, inputs, fmt="{:g}", note=""):
    return Derived(expr, inputs, fmt, note)


def A(file, where, op, col="", fmt="{:g}", note=""):
    return Agg(file, where, op, col, fmt, note)


def C(file, fn, fmt="{:g}", note=""):
    return Calc(file, fn, fmt, note)


RECON = "wp1/reconciliation_table.csv"
POP = "wp2/population_accounting.csv"
COH = "wp2/cohort_manifest.csv"
OUTC = "wp3/fit_outcomes.csv"
IDXAV = "wp3/index_availability_by_geometry.csv"
BRACK = "wp3/t41j_empirical_bracketing_summary.csv"
LSESENS = "wp3/lse_sensitivity_published_summary.csv"
IACC = "wp4/interval_curve_accounting.csv"
T41D = "wp4/t41j_uncertainty_distributions.csv"
XCHK = "wp4/published_uncertainty_crosscheck.csv"
SCAT = "wp4/published_residual_scatter_summary.csv"
COV = "wp4/synthetic_bootstrap_coverage_summary.csv"
W5SUM = "wp5/size_correction_summary_overall.csv"
W5FORM = "wp5/size_correction_summary_by_product_form.csv"
W5IRR = "wp5/size_correction_summary_by_irradiation.csv"
W5BA = "wp5/before_after_normalization_metrics.csv"
W5NS = "wp5/normalization_sensitivity_comparison.csv"
W5SUF = "wp5/pair_data_sufficiency.csv"
W6FV = "wp6/fixed_volume_comparison.csv"
W6TH = "wp6/correction_threshold.csv"
W6SENS = "wp6/sensitivity_summary.csv"
W6COV = "wp6/interval_coverage.csv"
W6VAL = "wp6/validation_results.csv"
W6CHK = "wp6/wp6_check_results.csv"
W5CHK = "wp5/wp5_check_results.csv"

F1 = "{:.1f}"
F2 = "{:.2f}"
INT = "{:,.0f}"

PRIMARY_FW = dict(subset="PRIMARY analysis set",
                  weighting="family-weighted (each family's mean counts once)")
ALLSTRICT_FW = dict(subset="all STRICT comparisons with a residual (primary + held as sensitivity)",
                    weighting="family-weighted (each family's mean counts once)")

REGISTRY: dict[str, Lookup | Derived | Agg | Calc] = {
    # -- 2 Data ------------------------------------------------------------------------
    "data.publications": A("wp0/references_summary.csv", {}, "count", fmt=INT),
    "data.records_total": L(RECON, dict(step="Start"), "records_remaining", INT),

    # -- 3 Cleaning and inclusion ------------------------------------------------------
    "clean.retained": L(RECON, dict(step="End"), "records_remaining", INT),
    "clean.removed_total": L(RECON, dict(step="End"), "records_removed", INT),
    "clean.e1_ss316": L(RECON, dict(step="E1"), "records_removed", INT),
    "clean.e8_dupes": L(RECON, dict(step="E8"), "records_removed", INT),
    "pop.primary_records": L(POP, dict(step="End"), "records", INT),
    "pop.primary_curves": L(POP, dict(step="End"), "curves", INT),
    "pop.primary_refs": L(POP, dict(step="End"), "references", INT),
    "coh.primary_curves": L(COH, dict(cohort="primary"), "curves", INT),
    "coh.primary_records": L(COH, dict(cohort="primary"), "records", INT),
    "coh.looser_curves": L(COH, dict(cohort="looser"), "curves", INT),
    "coh.stricter_curves": L(COH, dict(cohort="stricter"), "curves", INT),

    # -- 6.1 Fits ----------------------------------------------------------------------
    "fit.total": L(OUTC, dict(outcome="TOTAL"), "curves", INT),
    "fit.full_size": L(OUTC, dict(outcome="TOTAL"), "full-size_curves", INT),
    "fit.miniature": L(OUTC, dict(outcome="TOTAL"), "miniature_curves", INT),
    "fit.optimizer_failure": L(OUTC, dict(outcome="optimizer failure"), "curves", INT),
    "fit.nonphysical": L(OUTC, dict(outcome="non-physical (inadmissible)"), "curves", INT),
    "fit.boundary": L(OUTC, dict(outcome="boundary-limited"), "curves", INT),
    "fit.weak": L(OUTC, dict(outcome="weakly identified"), "curves", INT),
    "fit.usable_no_index": L(OUTC, dict(outcome="usable fit, index temperature unavailable"), "curves", INT),
    "fit.usable_index": L(OUTC, dict(outcome="usable fit, index temperature calculated"), "curves", INT),

    # -- 6.2 Per-curve uncertainty -----------------------------------------------------
    "unc.t41j_all": L(IACC, dict(method="pairs", geometry_category="full-size",
                                 target="t41j", original_wp3_outcome="ALL"), "curves", INT),
    "unc.t41j_primary_ci": L(IACC, dict(method="pairs", geometry_category="full-size",
                                        target="t41j", original_wp3_outcome="ALL"),
                             "primary_bootstrap_ci", INT),
    "unc.t41j_diagnostic": L(IACC, dict(method="pairs", geometry_category="full-size",
                                        target="t41j", original_wp3_outcome="ALL"),
                             "diagnostic_bootstrap_interval", INT),
    "unc.t41j_unavailable": L(IACC, dict(method="pairs", geometry_category="full-size",
                                         target="t41j", original_wp3_outcome="ALL"),
                              "interval_unavailable", INT),
    "unc.t41j_unavail_fixed": L(IACC, dict(method="wild", geometry_category="full-size",
                                           target="t41j", original_wp3_outcome="ALL"),
                                "interval_unavailable", INT),
    "unc.sd_median": L(T41D, dict(method="pairs", group="original WP3 outcome: usable fit",
                                  quantity="bootstrap SD of T41J (°C), reportable intervals"),
                       "median", F1),
    "unc.sd_p10": L(T41D, dict(method="pairs", group="original WP3 outcome: usable fit",
                               quantity="bootstrap SD of T41J (°C), reportable intervals"), "p10", F1),
    "unc.sd_p90": L(T41D, dict(method="pairs", group="original WP3 outcome: usable fit",
                               quantity="bootstrap SD of T41J (°C), reportable intervals"), "p90", F1),
    "unc.width_median": L(T41D, dict(method="pairs", group="original WP3 outcome: usable fit",
                                     quantity="95 % interval width of T41J (°C), reportable intervals"),
                          "median", F1),

    # -- 6.3 Size effect ---------------------------------------------------------------
    "size.strict_comparisons": L(W5SUF, dict(subset="STRICT matches"), "comparisons", INT),
    "size.strict_families": L(W5SUF, dict(subset="STRICT matches"), "families", INT),
    "size.strict_studies": L(W5SUF, dict(subset="STRICT matches"), "studies", INT),
    "size.primary_comparisons": L(W5SUM, dict(subset="PRIMARY analysis set",
                                              weighting="comparison-weighted"), "n", INT),
    "size.primary_families": L(W5SUM, PRIMARY_FW, "n_families", INT),
    "size.primary_studies": L(W5SUM, PRIMARY_FW, "n_studies", INT),
    "size.bias": L(W5SUM, PRIMARY_FW, "mean_c", F2),
    "size.sd": L(W5SUM, PRIMARY_FW, "sd_c", F2),
    "size.robust": L(W5SUM, PRIMARY_FW, "robust_scale_1p4826_mad_c", F2),
    "size.cons_families": L(W5SUM, ALLSTRICT_FW, "n_families", INT),
    "size.cons_bias": L(W5SUM, ALLSTRICT_FW, "mean_c", F2),
    "size.cons_sd": L(W5SUM, ALLSTRICT_FW, "sd_c", F2),
    "size.plate_families": L(W5FORM, dict(stratum="product form: plate",
                                          weighting="family-weighted"), "n_families", INT),
    "size.plate_studies": L(W5FORM, dict(stratum="product form: plate",
                                         weighting="family-weighted"), "n_studies", INT),
    "size.plate_bias": L(W5FORM, dict(stratum="product form: plate",
                                      weighting="family-weighted"), "mean_c", F2),
    "size.plate_sd": L(W5FORM, dict(stratum="product form: plate",
                                    weighting="family-weighted"), "sd_c", F2),
    "size.forging_families": L(W5FORM, dict(stratum="product form: forging",
                                            weighting="not summarized"), "n_families", INT),
    "size.weld_families": L(W5FORM, dict(stratum="product form: weld metal",
                                         weighting="not summarized"), "n_families", INT),
    "size.unirr_families": L(W5IRR, dict(stratum="irradiation state: unirradiated",
                                         weighting="family-weighted"), "n_families", INT),
    "size.unirr_bias": L(W5IRR, dict(stratum="irradiation state: unirradiated",
                                     weighting="family-weighted"), "mean_c", F2),
    "size.unirr_sd": L(W5IRR, dict(stratum="irradiation state: unirradiated",
                                   weighting="family-weighted"), "sd_c", F2),
    "size.irr_families": L(W5IRR, dict(stratum="irradiation state: irradiated",
                                       weighting="not summarized"), "n_families", INT),
    "size.min": L(W5SUM, dict(subset="PRIMARY analysis set", weighting="comparison-weighted"), "min_c", F1),
    "size.max": L(W5SUM, dict(subset="PRIMARY analysis set", weighting="comparison-weighted"), "max_c", F1),

    # -- 6.4 The test-matrix study -----------------------------------------------------
    "w6.t1_comparisons": A(W6FV, {}, "count", fmt=INT),
    "w6.full_wins": A(W6FV, dict(winner="FULL-SIZE WINS"), "count", fmt=INT),
    "w6.mini_wins": A(W6FV, dict(winner="MINIATURE WINS"), "count", fmt=INT),
    "w6.tied": A(W6FV, dict(winner="PRACTICALLY TIED"), "count", fmt=INT),
    "w6.ineligible": A(W6FV, dict(winner_class="INELIGIBLE"), "count", fmt=INT),
    "w6.geometries": C(W6FV, "n_geometries", INT),
    "w6.archetypes": C(W6FV, "n_archetypes", INT),
    "w6.mini_win_max_k": A(W6FV, dict(winner="MINIATURE WINS"), "max", "k_budget", INT),
    "w6.no_mini_win_from_k": C(W6FV, "min_k_no_miniature_win", INT),
    "w6.full_sweep_from_k": C(W6FV, "min_k_full_size_sweeps", INT),
    "w6.sdstar_k8_min": A(W6TH, dict(k_budget=8), "min", "sd_star_simulated_c", F1),
    "w6.sdstar_k8_max": A(W6TH, dict(k_budget=8), "max", "sd_star_simulated_c", F1),
    "w6.sdstar_k4_min": A(W6TH, dict(k_budget=4), "min", "sd_star_simulated_c", F1),
    "w6.sdstar_k4_max": A(W6TH, dict(k_budget=4), "max", "sd_star_simulated_c", F1),
    # wp6_summary.md section 3 quotes the median archetype A5 AT GEOMETRY G5; the CP5 record
    # quotes both that range and the wider one over all three archetypes. Both are carried, each
    # with its filter visible in claim_source_map.csv, so neither can be quoted as the other.
    "w6.sdstar_k8_a5g5_min": A(W6TH, dict(k_budget=8, archetype_id="A5", geom_code="G5"),
                               "min", "sd_star_simulated_c", F1),
    "w6.sdstar_k8_a5g5_max": A(W6TH, dict(k_budget=8, archetype_id="A5", geom_code="G5"),
                               "max", "sd_star_simulated_c", F1),
    "w6.sdstar_k4_a5g5_min": A(W6TH, dict(k_budget=4, archetype_id="A5", geom_code="G5"),
                               "min", "sd_star_simulated_c", F1),
    "w6.sdstar_k4_a5g5_max": A(W6TH, dict(k_budget=4, archetype_id="A5", geom_code="G5"),
                               "max", "sd_star_simulated_c", F1),
    "w6.sens_variants": A(W6SENS, {}, "count", fmt=INT),
    "w6.sens_changes": A(W6SENS, dict(changes_conclusion=True), "count", fmt=INT),
    "w6.cov_a_g5_k24": L(W6COV, dict(geom_code="G5", k_budget=24), "coverage_A_own_estimand", F2),
    "w6.cov_b_g5_k6": L(W6COV, dict(geom_code="G5", k_budget=6), "coverage_B_true_t41j", F2),
    "w6.cov_b_g5_k12": L(W6COV, dict(geom_code="G5", k_budget=12), "coverage_B_true_t41j", F2),
    "w6.cov_b_g5_k24": L(W6COV, dict(geom_code="G5", k_budget=24), "coverage_B_true_t41j", F2),
    "w6.cov_n_g5_k6": L(W6COV, dict(geom_code="G5", k_budget=6), "n", INT),
    "w6.cov_n_g5_k12": L(W6COV, dict(geom_code="G5", k_budget=12), "n", INT),
    "w6.cov_n_g5_k24": L(W6COV, dict(geom_code="G5", k_budget=24), "n", INT),
    "w6.val_rows": A(W6VAL, {}, "count", fmt=INT),
    "w6.val_passed": A(W6VAL, dict(passed=True), "count", fmt=INT),
    "w6.checks": A(W6CHK, {}, "count", fmt=INT),
    "w5.checks": A(W5CHK, {}, "count", fmt=INT),

    # -- 5 Fitter validation -----------------------------------------------------------
    "val.cov_well_t41j": L(COV, dict(scenario="well sampled", method="pairs", target="t41j"),
                           "coverage_of_reportable_intervals", F2),
    "val.cov_high_t41j": L(COV, dict(scenario="high scatter", method="pairs", target="t41j"),
                           "coverage_of_reportable_intervals", F2),
    "val.cov_weak_t41j": L(COV, dict(scenario="weakly sampled", method="pairs", target="t41j"),
                           "coverage_of_reportable_intervals", F2),
    "val.cov_wild_weak": L(COV, dict(scenario="weakly sampled", method="wild", target="t41j"),
                           "coverage_of_reportable_intervals", F2),
    "val.cov_se": L(COV, dict(scenario="well sampled", method="pairs", target="t41j"),
                    "coverage_monte_carlo_se", "{:.3f}"),

    # -- published cross-check (D-063) --------------------------------------------------
    "xchk.curves": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                     "curves", INT),
    "xchk.median_n": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                       "median_specimens", INT),
    "xchk.median_sd": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                        "median_bootstrap_sd_c", F2),
    "xchk.marini_sigma": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                           "marini_rccm_sigma_c", F2),
    "xchk.ratio": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                    "ratio_median_sd_to_marini_rccm_sigma", F2),
    "xchk.slope": L(XCHK, dict(method="pairs", subset="C1: usable full-size fits with a primary T41J CI"),
                    "theil_sen_slope_log_sd_vs_log_n", F2),

    # -- before / after normalization (D-084) -------------------------------------------
    "ba.t0_before": A(W5BA, {}, "median", "t0_abs_difference_before_c", F1),
    "ba.t0_after": A(W5BA, {}, "median", "t0_abs_difference_after_c", F1),
    "ba.improved_t0": A(W5BA, dict(t0_improved=True), "count", fmt=INT),
    "ba.improved_use": A(W5BA, dict(use_improved=True), "count", fmt=INT),
    "ba.comparisons": A(W5BA, {}, "count", fmt=INT),

    # -- normalization-method bias sensitivity (D-089, D-100) ---------------------------
    "ns.bias_min": A(W5NS, dict(case=["primary", "S1 energy (Bb)^3/2", "S3 temperature Lucon",
                                      "S4 temperature Towers", "S5 temperature Wallin",
                                      "S6 KLST as recorded"]), "min", "family_weighted_mean_c", F1),
    "ns.bias_max": A(W5NS, dict(case=["primary", "S1 energy (Bb)^3/2", "S3 temperature Lucon",
                                      "S4 temperature Towers", "S5 temperature Wallin",
                                      "S6 KLST as recorded"]), "max", "family_weighted_mean_c", F1),
    # D-089 quotes the stable-SD range over the volume-type energy conventions paired with the
    # four published temperature corrections. S6 varies the KLST geometry reading, not the
    # correlation, so it is not part of that set.
    "ns.sd_min": A(W5NS, dict(case=["primary", "S1 energy (Bb)^3/2", "S3 temperature Lucon",
                                    "S4 temperature Towers", "S5 temperature Wallin"]),
                   "min", "family_weighted_sd_c", F1),
    "ns.sd_max": A(W5NS, dict(case=["primary", "S1 energy (Bb)^3/2", "S3 temperature Lucon",
                                    "S4 temperature Towers", "S5 temperature Wallin"]),
                   "max", "family_weighted_sd_c", F1),

    # -- physical reachability (D-092, D-093) -------------------------------------------
    "reach.g1_unreachable": A("wp6/geometry_reachability.csv",
                              dict(geometry_code="G1", truth_kind="WP3 usable full-size fit",
                                   transition_reachable=False), "count", fmt=INT),
    "reach.g5_unreachable": A("wp6/geometry_reachability.csv",
                              dict(geometry_code="G5", truth_kind="WP3 usable full-size fit",
                                   transition_reachable=False), "count", fmt=INT),
    "reach.real_curves": A("wp6/geometry_reachability.csv",
                           dict(geometry_code="G0", truth_kind="WP3 usable full-size fit"), "count", fmt=INT),

    # -- floors (derived; D-123) --------------------------------------------------------
    "floor.central": D("(b**2 + s**2) ** 0.5", dict(b="size.bias", s="size.sd"), F2,
                       "sqrt(bias^2 + SD^2) of the CENTRAL pooled WP5 correction"),
    "floor.conservative": D("(b**2 + s**2) ** 0.5", dict(b="size.cons_bias", s="size.cons_sd"), F2,
                            "sqrt(bias^2 + SD^2) of the CONSERVATIVE all-STRICT correction"),
    "floor.plate": D("(b**2 + s**2) ** 0.5", dict(b="size.plate_bias", s="size.plate_sd"), F2,
                     "ARITHMETIC ONLY (D-123): sqrt(bias^2 + SD^2) with the plate stratum's own "
                     "family-weighted bias and SD substituted for the pooled ones. Product form was "
                     "never simulated; this is not a WP6 result."),
}

# --------------------------------------------------------------------------------------
# 2. Resolution
# --------------------------------------------------------------------------------------
_CACHE: dict[str, pd.DataFrame] = {}


def _table(rel: str) -> pd.DataFrame:
    if rel not in _CACHE:
        path = OUTPUTS / rel
        if not path.exists():
            raise SystemExit(f"WP7: registry names a file that does not exist: outputs/{rel}")
        _CACHE[rel] = pd.read_csv(path)
    return _CACHE[rel]


def _select(rel: str, where: dict) -> pd.Series:
    df = _table(rel)
    for col in where:
        if col not in df.columns:
            raise SystemExit(f"WP7: outputs/{rel} has no column {col!r}; it has {list(df.columns)}")
    mask = np.ones(len(df), bool)
    for col, val in where.items():
        mask &= (df[col].astype(str).str.strip() == str(val).strip()).to_numpy()
    hit = df[mask]
    if len(hit) != 1:
        raise SystemExit(f"WP7: selector {where} matched {len(hit)} rows in outputs/{rel}; exactly 1 required")
    return hit.iloc[0]


def resolve() -> tuple[dict, list[dict]]:
    """Resolve every registry entry. Returns {key: rendered string} and the claim-map rows."""
    values, rendered, rows = {}, {}, []
    for key, spec in REGISTRY.items():
        if isinstance(spec, Lookup):
            row = _select(spec.file, spec.where)
            if spec.col not in row.index:
                raise SystemExit(f"WP7: outputs/{spec.file} has no column {spec.col!r} (key {key})")
            raw = row[spec.col]
            values[key] = float(raw)
            rendered[key] = spec.fmt.format(float(raw))
            rows.append(dict(key=key, value=rendered[key], kind="table lookup",
                             file=f"outputs/{spec.file}",
                             row_selector="; ".join(f"{k} = {v}" for k, v in spec.where.items()),
                             column=spec.col, raw_value=repr(raw), expression="", inputs="",
                             note=spec.note))
        elif isinstance(spec, Agg):
            df = _table(spec.file)
            mask = np.ones(len(df), bool)
            for col, val in spec.where.items():
                if col not in df.columns:
                    raise SystemExit(f"WP7: outputs/{spec.file} has no column {col!r} (key {key})")
                accept = val if isinstance(val, (list, tuple, set)) else [val]
                mask &= df[col].astype(str).str.strip().isin([str(v).strip() for v in accept]).to_numpy()
            hit = df[mask]
            # A count of zero is a legitimate result (T1 has no INELIGIBLE comparison); a
            # min/max/median over an empty selection is not.
            if not len(hit) and spec.op != "count":
                raise SystemExit(f"WP7: aggregate {key} ({spec.op}) selected 0 rows of outputs/{spec.file}")
            val = float(len(hit)) if spec.op == "count" else float(getattr(hit[spec.col], spec.op)())
            values[key] = val
            rendered[key] = spec.fmt.format(val)
            rows.append(dict(key=key, value=rendered[key], kind=f"aggregate ({spec.op})",
                             file=f"outputs/{spec.file}",
                             row_selector="; ".join(f"{k} = {v}" for k, v in spec.where.items()) or "all rows",
                             column=spec.col, raw_value=repr(val),
                             expression=f"{spec.op}({spec.col or 'rows'}) over {len(hit)} of {len(df)} rows",
                             inputs="", note=spec.note))
        elif isinstance(spec, Calc):
            desc, fn = CALCS[spec.fn]
            val = float(fn(_table(spec.file)))
            values[key] = val
            rendered[key] = spec.fmt.format(val)
            rows.append(dict(key=key, value=rendered[key], kind="calculated",
                             file=f"outputs/{spec.file}", row_selector="all rows", column="",
                             raw_value=repr(val), expression=f"{spec.fn}: {desc}", inputs="",
                             note=spec.note))

    for key, spec in REGISTRY.items():
        if isinstance(spec, Derived):
            env = {}
            for name, ref in spec.inputs.items():
                if ref not in values:
                    raise SystemExit(f"WP7: derived key {key} refers to unknown key {ref!r}")
                env[name] = values[ref]
            val = float(eval(spec.expr, {"__builtins__": {}}, dict(env)))  # noqa: S307 - fixed expressions
            values[key] = val
            rendered[key] = spec.fmt.format(val)
            rows.append(dict(key=key, value=rendered[key], kind="derived",
                             file="; ".join(sorted({f"outputs/{REGISTRY[r].file}" for r in spec.inputs.values()
                                                    if isinstance(REGISTRY[r], Lookup)})),
                             row_selector="", column="", raw_value=repr(val),
                             expression=spec.expr,
                             inputs="; ".join(f"{n} = {spec.inputs[n]} = {values[spec.inputs[n]]!r}"
                                              for n in spec.inputs),
                             note=spec.note))
    return rendered, rows

# --------------------------------------------------------------------------------------
# 3. Figures and tables (D-115, D-117). Every entry carries exactly one evidence class.
# --------------------------------------------------------------------------------------
# Evidence classes (D-126 item 1). A float may carry MORE THAN ONE; the caption must say which
# visual component carries which provenance. The retired labels "MEASURED (published)",
# "FITTED / DERIVED FROM PUBLISHED DATA" and "TRANSFORMED ESTIMATE / DERIVED RESIDUAL" must not
# reappear: the first implies the measuring happened here, the other two were inconsistently defined.
PUBLISHED = "PUBLISHED SOURCE DATA"
DERIVED = "ANALYSIS-DERIVED FROM PUBLISHED DATA"
TRANSFORMED = "TRANSFORMED ESTIMATE FROM PUBLISHED DATA"
SYNTHETIC = "SYNTHETIC"
EVIDENCE_CLASSES = (PUBLISHED, DERIVED, TRANSFORMED, SYNTHETIC)

# Combinations the WP7 tests assert explicitly, because these are the floats a reader is most
# likely to misread (D-126 item 1).
REQUIRED_COMBINATIONS = {
    "2": {PUBLISHED, DERIVED},          # the worked example: published points plus a fitted curve
    "3": {PUBLISHED, DERIVED, TRANSFORMED},   # before/after normalization and its residual
    "T5": {DERIVED, TRANSFORMED},       # the residual summary table
}

# Presentation-only crops applied when embedding an approved figure (D-118 keeps the source file
# untouched). Keyed by the path under outputs/; the value is the number of top rows masked.
CROPS: dict[str, int] = {"wp6/rmse_vs_specimen_count.png": 44}

FIGURES: dict[str, dict] = {
    "2": dict(paths=["wp4/worked_example_t41j_bootstrap.png"], classes=(PUBLISHED, DERIVED),
              caption="A worked example of one fitted transition curve. The plotted energies are "
                      "PUBLISHED SOURCE DATA; the fitted curve, the pointwise bootstrap band of the "
                      "fitted mean curve and the index temperature with its interval are "
                      "ANALYSIS-DERIVED FROM PUBLISHED DATA. The band is a confidence band for the "
                      "mean curve, not a prediction interval for a new specimen. Curve 3-17, A533B "
                      "plate, irradiated."),
    # The approved WP6 PNG carries a title that is clipped at both edges in the source file
    # itself. D-118 forbids editing an approved output, so the top strip is masked HERE, at the
    # report layer, and the report's own caption serves as the figure's description. Rows 0-43 of
    # the source image contain only that clipped title: rows 42-48 are blank and the plot frame
    # begins at row 49, so no axis, tick, legend, annotation or data mark is removed. Verified by
    # src/wp7_tests.py, which re-checks that the masked strip contains no plot content.
    "5": dict(paths=["wp6/rmse_vs_specimen_count.png"], classes=(SYNTHETIC,), crop_top_px=44,
              caption="Index-temperature uncertainty against specimen count for the median true curve "
                      "(archetype A5), one series per test-temperature placement strategy, with the "
                      "square-root-of-N reference. "
                      "The horizontal line is the error floor implied by the central size "
                      "correction: a full-size programme keeps improving with specimen count, a "
                      "miniature programme stops at the floor. Simulated programmes throughout."),
    "3": dict(paths=["wp5/before_after_normalization.png", "wp5/size_correction_residuals.png"],
              classes=(PUBLISHED, DERIVED, TRANSFORMED),
              panels=["(a) Curves before and after the classical size normalization, for "
                      "four matched material-condition families.",
                      "(b) The residual disagreement that survives normalization, every comparison "
                      "shown individually, by smaller-specimen geometry and by product form."],
              caption="The specimen-size normalization and what it leaves behind. In panel (a) the "
                      "full-size and smaller-specimen points are PUBLISHED SOURCE DATA, the mapped "
                      "points are a TRANSFORMED ESTIMATE FROM PUBLISHED DATA, and both fitted "
                      "curves and the refit of the mapped points are ANALYSIS-DERIVED FROM "
                      "PUBLISHED DATA. In panel (b) each plotted residual is ANALYSIS-DERIVED: the "
                      "difference between a transformed estimate and a fitted full-size index "
                      "temperature. Individual points are shown rather than a fitted "
                      "distribution, because there are too few independent families to justify "
                      "smoothing."),
    "4": dict(paths=["wp6/fixed_volume_comparison.png"], classes=(SYNTHETIC,),
              callout="Conventional E23 sub-size: not estimated — insufficient included evidence.",
              caption="The fixed-material-volume comparison, one panel per placement strategy. "
                      "Full-size is simulated, and so are the seven approved smaller "
                      "MCVN/miniaturized geometry scenarios. Conventional ASTM E23-type sub-size "
                      "performance is NOT ESTIMABLE from this dataset under the approved rules, and "
                      "no external correction was invented to fill that gap, so no sub-size arm "
                      "appears here. Every miniature curve is a conditional fixed-volume scenario "
                      "using the pooled, WEAKLY SUPPORTED correction, not a geometry-specific "
                      "claim. Simulated programmes throughout."),
    "6": dict(paths=["wp6/correction_uncertainty_flip.png"], classes=(SYNTHETIC,),
              caption="How uncertain the size correction may be before extra miniature specimens "
                      "stop paying. Miniature programme error against the correction residual "
                      "standard deviation, against the matching full-size programme, with the "
                      "analysis-derived central and conservative values marked. Simulated programmes."),
    "7": dict(paths=["wp6/prior_error_vs_performance.png"], classes=(SYNTHETIC,),
              caption="Prior knowledge of the transition location. Error and estimator availability "
                      "against the error in the assumed transition temperature, with the "
                      "availability gate marked. Where a design misses the transition it is "
                      "declared unusable rather than merely imprecise. Simulated programmes."),
    "1": dict(paths=["wp3/synthetic_error_vs_specimens.png"], classes=(SYNTHETIC,),
              caption="Fitter validation against known truth: index-temperature error against the "
                      "number of specimens, at three scatter levels. Curves generated from known "
                      "parameters; no published measurement appears in this figure."),
}

TABLES: dict[str, dict] = {
    "1": dict(file=RECON, cols=["step", "criterion", "records_removed", "records_remaining"],
              classes=(DERIVED,),
              caption="Cleaning reconciliation. These counts are ANALYSIS-DERIVED: they are the "
                      "result of this project's exclusion rules applied to the published "
                      "compilation, not counts any source study reported. Every record that leaves "
                      "does so at the first step that applies, for a stated reason, and the "
                      "arithmetic closes."),
    "2": dict(file=COH, cols=["cohort", "role", "curves", "records"], classes=(DERIVED,),
              caption="The curve cohorts frozen at checkpoint CP2, ANALYSIS-DERIVED from the "
                      "published records by this project's grouping and screening rules. Each "
                      "differs from the primary cohort in exactly one judgement, so any later "
                      "change in a result is attributable to one decision. Membership is "
                      "fingerprinted and re-checked on every run."),
    "3": dict(file=OUTC, cols=["outcome", "curves", "full-size_curves", "miniature_curves"],
              classes=(DERIVED,),
              caption="Fit outcomes for every curve of the primary cohort, mutually exclusive and "
                      "exhaustive, ANALYSIS-DERIVED from the published measurements. No curve is "
                      "silently dropped: a curve the fitter cannot resolve is reported as such."),
    "4": dict(file=IACC, cols=["method", "geometry_category", "target", "curves",
                               "primary_bootstrap_ci", "diagnostic_bootstrap_interval",
                               "interval_unavailable"],
              where=dict(original_wp3_outcome="ALL"), classes=(DERIVED,),
              caption="Which curves received which kind of interval, ANALYSIS-DERIVED by "
                      "resampling the published measurements. Intervals are nominal percentile "
                      "bootstrap intervals, not intervals calibrated to exact coverage. The "
                      "unavailable intervals are a result about test-matrix fragility, not a gap "
                      "in the table."),
    "5": dict(file=W5SUM, cols=["subset", "weighting", "n", "n_families", "n_studies", "mean_c",
                                "sd_c", "min_c", "max_c"], classes=(DERIVED, TRANSFORMED),
              relabel={"subset": {"PRIMARY analysis set": "PRIMARY",
                                  "all STRICT comparisons with a residual "
                                  "(primary + held as sensitivity)": "ALL STRICT"},
                       "weighting": {"family-weighted (each family's mean counts once)":
                                     "family-weighted"}},
              caption="The residual index-temperature disagreement left by the classical size "
                      "normalization. Each residual is ANALYSIS-DERIVED from a TRANSFORMED "
                      "ESTIMATE: the difference between a mapped smaller-specimen index "
                      "temperature and the matched full-size one. Row labels are shortened for "
                      "the page: PRIMARY is the pre-registered primary analysis set, and ALL "
                      "STRICT is every strictly matched comparison with a residual, that is the "
                      "primary set together with those held as sensitivity; family-weighted means "
                      "each family contributes the mean of its own comparisons and then counts "
                      "once. The family is the unit of independence, so the family-weighted rows "
                      "are the ones carried forward."),
    "7": dict(file=W6SENS, cols=["variant", "median_delta_rmse_c", "miniature_wins",
                                 "full_size_wins", "tied", "ineligible", "changes_conclusion"],
              classes=(SYNTHETIC,),
              caption="The pre-registered sensitivity variants, all simulated. A positive median "
                      "difference favours miniature specimens. The size-correction assumptions "
                      "dominate; the scatter model does not."),
    "6": dict(file=W6TH, cols=["strategy", "k_budget", "n_mini", "rmse_full_c",
                               "sd_star_simulated_c", "sd_star_semi_analytic_c"],
              where=dict(archetype_id="A5", geom_code="G5"), classes=(SYNTHETIC,),
              caption="How well the size correction would have to be known for a miniature "
                      "programme to match a full-size one, for the median true curve at one "
                      "geometry. Simulated; compare with the analysis-derived correction "
                      "standard deviation reported in the text."),
    "8": dict(file=W6COV, cols=["geom_code", "k_budget", "n", "coverage_A_own_estimand",
                                "coverage_B_true_t41j", "median_width_c"], classes=(SYNTHETIC,),
              caption="Interval coverage on simulated programmes. Coverage A is of the programme's "
                      "own corrected estimand, which is what the bootstrap samples; coverage B is "
                      "of the true full-size index temperature. For full-size programmes they "
                      "coincide; for miniature ones they must not."),
}


# --------------------------------------------------------------------------------------
# 4. Lint (D-114, D-116, D-117)
# --------------------------------------------------------------------------------------
PLACEHOLDER = re.compile(r"\{\{=?([A-Za-z0-9_.]+)\}\}")
SLOT = re.compile(r"\[\[(FIG|TAB) ([0-9a-z]+)\]\]")
COMMENT = re.compile(r"<!--.*?-->", re.S)

# Unqualified claims the report may not make (D-116). Matched case-insensitively on the
# filled text, after tables and captions are in place.
FORBIDDEN = [
    (r"\bprove[sd]?\b", "'prove' overstates a simulation result"),
    (r"\bmini(ature)? specimens are worse\b", "unconditional claim about miniature specimens"),
    (r"\bfull[- ]size (is|are) better\b", "unconditional superiority claim (CP5 forbids it)"),
    (r"\buniversally better\b", "CP5 forbids this claim explicitly"),
    (r"\bwe (tested|measured|machined|irradiated)\b", "implies physical testing (brief 7)"),
    (r"\bour (tests|specimens|measurements)\b", "implies physical testing (brief 7)"),
    (r"\bcalibrated (95|confidence)\b", "WP4 intervals are nominal, not calibrated (D-056)"),
    (r"\bmeasured full-size-equivalent\b", "a transformed estimate is never a measurement (D-117)"),
    (r"FITTED / DERIVED FROM PUBLISHED DATA|MEASURED \(published\)"
     r"|TRANSFORMED ESTIMATE / DERIVED RESIDUAL"
     r"|TRANSFORMED ESTIMATE \(derived from published smaller-specimen measurements\)"
     r"|FITTED \(derived from published data\)"
     r"|carries exactly one of these labels", "retired evidence label or rule (D-126 item 1)"),
    # The size-correction bias and SD are ANALYSIS-DERIVED from matched published curves. This
    # project measured nothing, so "measured" may not describe them (D-126 item 1).
    (r"\bmeasured\b(?:(?!\.)[^.]){0,45}?\bcorrection\b"
     r"|\bcorrection\b(?:(?!\.)[^.]){0,35}?\bmeasured\b"
     r"|\bmeasured (?:value|central|conservative|residual|bias|SD|standard deviation)\b"
     r"|\bthe measured \d",
     "the size-correction bias and standard deviation are analysis-derived from matched published "
     "curves, not measured by this project (D-126 item 1); say analysis-derived or estimated"),
]

# D-125 item 1: the 2026 study's prediction accuracy and this project's correction residual are not
# commensurable. Any sentence that names that study and also reaches for a magnitude comparison
# fails the build.
ML_STUDY = re.compile(r"machine[- ]learning|Kasala|correlation paper|prediction problem", re.I)
MAGNITUDE = re.compile(r"\bsits? (inside|within|between|in that range)\b|\b(inside|within) the range\b"
                       r"|\bcomparable (in )?magnitude\b|\bof the same order\b|\bbroadly comparable\b"
                       r"|\bthe expected place for it\b", re.I)

# D-126 item 2: the plate-only floor is arithmetic on approved WP5 values. No WP6 winner, tie or
# favouring label exists for it, so no sentence may attach one.
PLATE_VERDICT = re.compile(
    r"\bplate-only\b[^.]{0,140}?\b(wins?|won|favours?|favors?|favouring|favoring|beats?|verdict|"
    r"better than)\b|\b(wins?|won|favours?|favors?|favouring|favoring|beats?)\b[^.]{0,140}?"
    r"\bplate-only\b", re.I)

# An explicit full-size-versus-miniature verdict must carry the conditional wording in the same
# paragraph (D-116). Deliberately narrow: "the staircase outperforms the batched design" is a
# statement about placement strategies, not about specimen size, and must not be caught.
WIN_CLAIM = re.compile(r"\b(miniature|full-size)\b[^.]{0,60}?\b(wins?|beats?|loses?)\b", re.I)
CONDITION = "conditional fixed-volume scenario"

# D-061 forbids calling this project's empirical residual scatter "material scatter". It does NOT
# forbid saying that the two cannot be separated, or that the pool is never pure material scatter -
# those are the honest statements the decision asks for. An occurrence is therefore acceptable only
# when a qualifier makes clear it is not a claim about this project's own pool.
SCATTER_OK = re.compile(r"(real|pure|physical|genuine|separated from|not|never|nor)\s+"
                        r"(\w+\s+){0,2}material scatter", re.I)


# Literals that are conventions, identifiers or citations rather than results of this analysis,
# and may therefore appear in the prose (D-114). The list is deliberately explicit and reviewable:
# anything not matched here must be a placeholder resolved from a generated table.
@dataclass(frozen=True)
class Constant:
    """A literal number that legitimately appears in the authored content because it is a method
    constant or an externally cited value rather than a result of this analysis (D-126 item 3).

    The registry replaces the bare regular-expression whitelist used during early implementation,
    which could have become a loophole admitting an uncited external number. Every entry states a
    provenance category and a source, and the build fails on any literal number not matched here.
    """
    name: str           # symbolic identifier, printed in constant_source_map.csv
    pattern: str        # regex matching how the constant appears in the authored content
    value: str          # the value as written
    category: str       # A method/configuration | B externally cited | M document metadata
    source: str         # DECISIONS.md entry and/or external citation


A = "A: method/configuration constant"
B = "B: externally cited value"
M = "M: document metadata (numbering)"

CONSTANTS: list[Constant] = [
    # --- A: method and configuration constants, each traceable to a decision -------------------
    Constant("criterion_energy", r"\b41 J\b", "41 J", B,
             "10 CFR 50 App. G II.E and ASTM E185-82 4.15, adopted in D-044"),
    Constant("full_size_lower_shelf", r"\b2\.7 J\b", "2.7 J", A,
             "D-042; value from Sokolov & Nanstad (1995) p. 7"),
    Constant("subsize_lower_shelf_cited", r"\b0\.1 J\b", "0.1 J", B,
             "Sokolov & Nanstad (1995) p. 7; cited in D-042 and deliberately NOT adopted"),
    Constant("nominal_level_and_gate", r"\b95 ?%", "95 %", A,
             "D-056 interval level; D-057 finite-target rule; D-104 availability gate"),
    Constant("digest_algorithms", r"\bSHA-?256\b|\bMD5\b", "SHA-256, MD5", A,
             "D-005 checksum regime"),
    # --- B: externally cited values ------------------------------------------------------------
    Constant("full_size_specimen", r"\b55 ?[x\u00d7] ?10 ?[x\u00d7] ?10 ?mm\b|\b10 mm\b|\b8 mm\b|\b2 mm\b",
             "55x10x10 mm, ligament 8 mm, notch 2 mm", B, "ASTM E23; ISO 148-1; convention fixed in D-008"),
    Constant("ligament_volume", r"\bB b\^?2\b|\bB\(W ?[-\u2212] ?A\)\^?2\b", "B b^2", B,
             "Lucas et al. (1986) via NUREG/CR-6379 p. 14 and the dataset descriptor Table 2; adopted in D-073"),
    Constant("sokolov_coefficients", r"\b98 ?[-\u2212] ?15\.1\b|\b15\.1\b|\bM = 98\b", "98, 15.1", B,
             "NUREG/CR-6379 Eq. (22); adopted in D-074"),
    Constant("marini_matrix_size", r"\beighteen-specimen\b", "N = 18", B,
             "Marini (2020) Table 6, the RCC-M matrix; used in the D-063 cross-check"),
    Constant("curve_identifiers", r"\b[Cc]urve \d{1,3}-\d{1,3}(\.\d+)?\b", "e.g. curve 3-17", B,
             "dataset curve identifiers; record identity D-006, curve definition D-033"),
    Constant("standards", r"\b(ASTM )?(E23|E185|E2248|E1921|E900)(-\d+)?\b|\bISO 148-1(:\d+)?\b"
                          r"|\bISO 14556\b|\bDIN 50115\b|\b10 CFR (Part )?50(\.61a?)?\b",
             "standard and regulation designations", B, "cited clause recorded with each use in DECISIONS.md"),
    Constant("report_numbers", r"\bNUREG/CR-\d{4}\b|\bORNL-\d{4}\b|\bEPRI NP-\d{4}\b|\bBLG-\d{4}\b"
                               r"|\b(ASTM )?STP \d{4}\b|\b(Technical )?Note \d{4}\b",
             "report and publication numbers", B, "WP3-WP6 source lists in DECISIONS.md"),
    Constant("material_designations", r"\bS?A-?(533|508|302)[A-Z]?(-\d)?\b|\b20MnMoNi55\b"
                                      r"|\bSS316\b|\b15Cr2MoV-A\b|\bGr\.? ?(1A|3|4N)\b",
             "specification designations", B, "ASTM A533/A508/A302; D-012 harmonization"),
    Constant("dataset_records", r"\bMaterials Cloud (2024\.206|2025\.30)\b|\b(q4x6v-dyt25|eny5v-www93)\b",
             "Materials Cloud record identifiers", B, "D-001; data/README.md"),
    Constant("dois_and_preprints", r"\b10\.\d{4,5}/[^\s)]+|\barXiv \d{4}\.\d{4,5}\b",
             "DOIs and preprint identifiers", B, "reference list"),
    Constant("licence", r"\bCC BY 4\.0\b", "CC BY 4.0", B, "dataset licence; data/LICENSE-CC-BY-4.0.txt"),
    Constant("citation_years", r"\b(19|20)\d{2}\b", "publication years", B, "reference list"),
    # --- M: unavoidable document metadata ------------------------------------------------------
    Constant("cross_references", r"\bsections? \d(\.\d)*\b|\b(Figure|Table|Appendix) \d[ab]?\b"
                                 r"|\bpanel \([ab]\)",
             "section, figure, table and appendix numbering", M, "document structure"),
    Constant("project_identifiers", r"\bD-\d{3}\b|\bWP[0-7]\b|\bCP[1-5]\b|\bQ[1-4]\b"
                                    r"|\bA[1-9]\b|\bG[0-7]\b|\bV\d{1,2}\b",
             "decision, work-package, checkpoint, question, archetype, geometry and variant ids", M,
             "DECISIONS.md and the WP6 frozen grid"),
    Constant("sqrt_n_notation", r"1 ?/ ?sqrt\(N\)", "1/sqrt(N)", M, "mathematical notation"),
]


def constant_rows() -> list[dict]:
    return [dict(name=c.name, value=c.value, provenance_category=c.category, source=c.source,
                 pattern=c.pattern) for c in CONSTANTS]


def blank_comments(text: str) -> str:
    """Replace every block comment with the same number of blank lines, so the comment cannot be
    parsed as content while report.md line numbers in lint messages stay correct."""
    return re.sub(r"<!--(?:(?!-->).)*?-->",
                  lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def strip_protected(text: str) -> str:
    """Remove everything a digit is allowed to appear in, so what remains can be checked."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith(("|", "<!--", "-->")) or line.strip().startswith("#"):
            continue
        if line.strip().startswith("[[") or "lint:allow-digits" in line:
            continue
        out.append(line)
    text = "\n".join(out)
    text = COMMENT.sub("", text)
    text = PLACEHOLDER.sub("", text)
    text = SLOT.sub("", text)
    for c in CONSTANTS:
        text = re.sub(c.pattern, "", text)
    return text


def lint_source(src: str) -> list[str]:
    """No literal result number may appear in the prose (D-114)."""
    problems, allow_next = [], False
    for i, line in enumerate(src.splitlines(), 1):
        if "lint:allow-digits" in line:
            allow_next = True
            continue
        checkable = strip_protected(line)
        if checkable.strip() and re.search(r"\d", checkable) and not allow_next:
            problems.append(f"report.md line {i}: literal digit in prose, use a placeholder: {line.strip()[:90]}")
        allow_next = False
    return problems


def lint_filled(text: str) -> list[str]:
    problems = []
    for pattern, why in FORBIDDEN:
        for m in re.finditer(pattern, text, re.I):
            line = text[:m.start()].count("\n") + 1
            problems.append(f"report_filled.md line {line}: forbidden phrase {m.group(0)!r} - {why}")
    for m in re.finditer(r"material scatter", text, re.I):
        window = text[max(0, m.start() - 60):m.end()]
        if not SCATTER_OK.search(window):
            line = text[:m.start()].count("\n") + 1
            problems.append(f"report_filled.md line {line}: 'material scatter' is unqualified; this "
                            "project's pool is empirical published-data residual scatter (D-061)")
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if ML_STUDY.search(sentence) and MAGNITUDE.search(sentence):
            line = text[:text.find(sentence)].count("\n") + 1
            problems.append(f"report_filled.md line {line}: a sentence about the 2026 study reaches "
                            f"for a magnitude comparison, which D-125 item 1 forbids as invalid: "
                            f"{sentence.strip()[:110]}")
        if PLATE_VERDICT.search(sentence):
            line = text[:text.find(sentence)].count("\n") + 1
            problems.append(f"report_filled.md line {line}: the plate-only scenario was never in the "
                            f"frozen WP6 grid, so no win/favouring label may attach to it "
                            f"(D-126 item 2): {sentence.strip()[:110]}")
    for para in re.split(r"\n\s*\n", text):
        if WIN_CLAIM.search(para) and CONDITION not in para:
            if "[[" in para or para.lstrip().startswith("|"):
                continue
            problems.append("a win/loss claim about miniature specimens omits the phrase "
                            f"{CONDITION!r} (D-116): {para.strip()[:110]}")
    return problems


# --------------------------------------------------------------------------------------
# 5. Expanding the figure and table slots into the filled Markdown
# --------------------------------------------------------------------------------------
def table_markdown(num: str) -> str:
    """Render report table `num` from its generated file as a Markdown table."""
    spec = TABLES[num]
    df = _table(spec["file"]).copy()
    for col, val in spec.get("where", {}).items():
        df = df[df[col].astype(str).str.strip() == str(val).strip()]
    missing = [c for c in spec["cols"] if c not in df.columns]
    if missing:
        raise SystemExit(f"WP7: table {num}: outputs/{spec['file']} lacks columns {missing}")
    df = df[spec["cols"]]
    # Concise display labels, applied ONLY here, at the report-layout layer. The generated CSV is
    # untouched and the full definitions are carried in the caption and the surrounding prose.
    for col, mapping in spec.get("relabel", {}).items():
        df[col] = df[col].astype(str).str.strip().map(lambda v, m=mapping: m.get(v, v))
    from common import md_table
    return md_table(df)


def expand_slots(text: str) -> str:
    """Replace [[FIG n]] / [[TAB n]] / [[BOX]] with concrete Markdown, so report_filled.md is a
    complete readable document and the PDF is typeset from exactly that document.

    A figure with two source files becomes ONE numbered figure with panels (a) and (b) under one
    caption (D-125 item 3); the panels are composed here and stacked by the typesetter, so no new
    generated file is created and no WP5 source is touched."""
    def fig(num: str) -> str:
        if num not in FIGURES:
            raise SystemExit(f"WP7: report.md references figure {num}, which is not in FIGURES")
        spec = FIGURES[num]
        paths, multi = spec["paths"], len(spec["paths"]) > 1
        imgs = "\n\n".join(
            f"![Figure {num}{'(' + chr(97 + i) + ')' if multi else ''}](outputs/{path})"
            for i, path in enumerate(paths))
        callout = f"\n\n> **{spec['callout']}**" if spec.get("callout") else ""
        panels = ("  " + "  ".join(spec["panels"]) + " ") if spec.get("panels") else " "
        classes = " + ".join(spec["classes"])
        srcs = "; ".join(f"`outputs/{path}`" for path in paths)
        # Panel descriptions read best straight after the caption's lead sentence, ahead of the
        # provenance attribution.
        head = spec["caption"].split(". ", 1)
        body = (f"{head[0]}.{panels}{head[1]}" if spec.get("panels") and len(head) == 2
                else f"{spec['caption']}{panels}")
        note = ""
        if spec.get("crop_top_px"):
            note = (f" The top {spec['crop_top_px']} pixels of the source image, which contain "
                    f"only a title clipped in the source file itself, are masked at the report "
                    f"layer; the approved file is unchanged and no plot content is removed.")
        return (f"{imgs}{callout}\n\n*Figure {num}. {body.strip()}* "
                f"**[{classes}]** *Source: {srcs}.{note}*")

    def tab(num: str) -> str:
        if num not in TABLES:
            raise SystemExit(f"WP7: report.md references table {num}, which is not in TABLES")
        md, spec = table_markdown(num), TABLES[num]
        classes = " + ".join(spec["classes"])
        return (f"*Table {num}. {spec['caption']}* **[{classes}]** "
                f"*Source: `outputs/{spec['file']}`.*\n\n{md}")

    text = SLOT.sub(lambda m: fig(m.group(2)) if m.group(1) == "FIG" else tab(m.group(2)), text)
    text = re.sub(r"\[\[BOX ([^\]]+)\]\]\s*\n(.*?)\n\s*\[\[/BOX\]\]",
                  lambda m: "> **In plain terms — " + m.group(1).strip() + ".** "
                            + " ".join(m.group(2).split()),
                  text, flags=re.S)
    return text


def authored_strings() -> dict[str, str]:
    """Every authored string outside report.md prose: captions, panel descriptions, callouts and
    table captions. D-126 item 4 applies the provenance rules to these too - a numerical assertion
    may not bypass provenance merely because it sits in a caption."""
    out = {}
    for num, spec in FIGURES.items():
        out[f"figure {num} caption"] = spec["caption"]
        for i, panel in enumerate(spec.get("panels", [])):
            out[f"figure {num} panel {chr(97 + i)}"] = panel
        if spec.get("callout"):
            out[f"figure {num} callout"] = spec["callout"]
    for num, spec in TABLES.items():
        out[f"table {num} caption"] = spec["caption"]
    return out


# --------------------------------------------------------------------------------------
# 6. PDF typesetting (D-113): matplotlib PdfPages, deterministic metadata
# --------------------------------------------------------------------------------------
PAGE_W, PAGE_H = 8.27, 11.69            # A4 portrait, inches
MARGIN_X, MARGIN_TOP, MARGIN_BOT = 0.82, 0.68, 0.60
COL_W = PAGE_W - 2 * MARGIN_X
SIZES = dict(title=17, h1=13, h2=10.5, h3=9.0, body=8.4, caption=7.0, table=6.1, foot=6.2)
TABLE_MIN_PT = 5.8                      # a table shrinks no further than this
FIG_MIN_SCALE = 0.82                    # a figure may shrink at most this much to avoid
                                        # blanking the rest of a page
MIN_TABLE_ROWS = 4                      # a continued table carries at least this many rows
CAPTION_KEEP_LINES = 3                  # caption lines that must start beside the figure
TABLE_LEAD = 1.18                       # tighter than prose; a monospace grid needs less air
LEAD = 1.30                             # line spacing, multiples of the font size
CHAR_W = 0.520                          # mean glyph width of DejaVu Sans, in units of font
                                        # size; deliberately a little conservative, so that a
                                        # line carrying an unbreakable path still stays inside
                                        # the text column


def _effective_size(text: str, size: float) -> float:
    """Capitals are markedly wider than lower case in DejaVu Sans, so a caption carrying an
    all-capital evidence label overflows a column width estimated from the average glyph. Widen
    the estimate in proportion to how many capitals the text actually contains."""
    letters = sum(1 for c in text if c.isalpha())
    if not letters:
        return size
    caps = sum(1 for c in text if c.isupper())
    return size * (1.0 + 0.30 * caps / letters)


def wrap(text: str, size: float, width_in: float = COL_W, indent: str = "",
         bold: bool = False) -> list[str]:
    import textwrap
    eff = _effective_size(text, size) * (1.08 if bold else 1.0)
    cols = max(12, int(width_in * 72.0 / (CHAR_W * eff)))
    lines: list[str] = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, cols, subsequent_indent=indent) or [""])
    return lines


def parse_blocks(md: str) -> list[tuple]:
    """Parse the expanded Markdown into a flat block list for the layout engine."""
    blocks, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        if not stripped:
            i += 1
            continue
        if stripped == "<!--pagebreak-->":
            blocks.append(("pb",)); i += 1; continue
        if re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped):
            paths = []                      # consecutive images are panels of ONE figure
            while i < len(lines):
                mm = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", lines[i].strip())
                if mm:
                    paths.append(mm.group(2)); i += 1
                elif not lines[i].strip():
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].strip().startswith("!["):
                        i = j
                        continue
                    break
                else:
                    break
            blocks.append(("figs", paths))
            continue
        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("tab", rows)); continue
        if stripped.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:]); i += 1
            blocks.append(("box", " ".join(buf))); continue
        if stripped.startswith("- "):
            buf = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                buf.append(lines[i].strip()[2:]); i += 1
            blocks.append(("bul", buf)); continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            blocks.append((f"h{min(level, 3)}", stripped.lstrip("# ").strip())); i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(("#", "|", "- ", "> ", "![", "<!--")):
            buf.append(lines[i].strip()); i += 1
        blocks.append(("p", " ".join(buf)))
    return blocks


def _clean(text: str) -> str:
    """Markdown emphasis and code marks are not rendered as styling; strip the syntax so the
    printed page does not show asterisks and backticks."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def layout_units(blocks: list[tuple]) -> list[list[tuple]]:
    """Group blocks into units that must not be split: a figure travels with its callout and its
    caption, so moving a figure never orphans its caption."""
    units, i = [], 0
    while i < len(blocks):
        if blocks[i][0] == "figs":
            unit, i = [blocks[i]], i + 1
            while i < len(blocks) and blocks[i][0] in ("box", "p"):
                if blocks[i][0] == "box":
                    unit.append(blocks[i]); i += 1
                elif re.match(r"\*?Figure \d", _clean(blocks[i][1])):
                    unit.append(blocks[i]); i += 1
                    break
                else:
                    break
            units.append(unit)
        else:
            units.append([blocks[i]]); i += 1
    return units


def _block_height(block: tuple) -> float:
    """Simulated height of one block, mirroring what typeset() lays out. Used only to decide
    ordering; the renderer measures again, so a small discrepancy costs at most a page break."""
    import matplotlib.image as mpimg
    kind = block[0]
    if kind in ("h1", "h2", "h3"):
        size = SIZES["title"] if kind == "h1" else SIZES[kind]
        gap = {"h1": 0.26, "h2": 0.21, "h3": 0.155}[kind]
        return len(wrap(_clean(block[1]), size, bold=True)) * size * LEAD / 72.0 + gap
    if kind == "p":
        return len(wrap(_clean(block[1]), SIZES["body"])) * SIZES["body"] * LEAD / 72.0 + 0.055
    if kind == "bul":
        return sum(len(wrap(_clean(i), SIZES["body"], COL_W - 0.12)) for i in block[1]) \
            * SIZES["body"] * LEAD / 72.0 + 0.03 * len(block[1]) + 0.05
    if kind == "box":
        return len(wrap(_clean(block[1]), SIZES["body"], COL_W - 0.34)) \
            * SIZES["body"] * LEAD / 72.0 + 0.27
    if kind == "tab":
        return (len(block[1]) + 1) * SIZES["table"] * TABLE_LEAD / 72.0 + 0.23
    if kind == "figs":
        h = 0.0
        for path in block[1]:
            img = mpimg.imread(str(ROOT / path))
            crop = CROPS.get(path.replace("outputs/", ""), 0)
            if crop:
                img = img[crop:]
            h += COL_W * (img.shape[0] / img.shape[1])
        return h + 0.10 * (len(block[1]) - 1) + 0.12
    return 0.0


def reorder_floats(blocks: list[tuple]) -> list[tuple]:
    """A tall figure that cannot fit the space left would blank the rest of the page. Move it past
    the following paragraphs that DO fit, carrying its callout and caption with it, so the page
    fills and nothing is orphaned. Reading order is preserved except that a figure may appear
    slightly after the paragraph that introduces it, which is ordinary practice for a float."""
    units = layout_units(blocks)
    out, y, i = [], PAGE_H - MARGIN_TOP, 0
    floor = MARGIN_BOT
    while i < len(units):
        unit = units[i]
        need = sum(_block_height(b) for b in unit)
        if unit[0][0] == "pb":
            y = PAGE_H - MARGIN_TOP
            out.extend(unit); i += 1
            continue
        if unit[0][0] == "figs" and need > y - floor and y < PAGE_H - MARGIN_TOP - 1e-9:
            moved = False
            for j in range(i + 1, min(i + 5, len(units))):
                cand = units[j]
                if cand[0][0] != "p":
                    break
                ch = sum(_block_height(b) for b in cand)
                if ch <= y - floor:                      # this paragraph fills the gap
                    out.extend(cand)
                    y -= ch
                    units.pop(j)
                    moved = True
                    break
            if moved:
                continue                                  # try the figure again in the new space
        if need > y - floor:
            y = PAGE_H - MARGIN_TOP
        out.extend(unit)
        y -= need
        i += 1
    return out


def typeset(blocks: list[tuple], path: Path, footer: str) -> int:
    """Flow the blocks onto A4 pages and write a deterministic PDF."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.image as mpimg

    state = {"fig": None, "y": 0.0, "n": 0}

    # Page images for the mandatory visual QA gate (D-125 item 8). Written only when
    # WP7_PAGE_PNGS names a directory OUTSIDE the repository; never part of a normal build.
    png_dir = os.environ.get("WP7_PAGE_PNGS", "").strip()

    def new_page(pdf):
        if state["fig"] is not None:
            state["n"] += 1
            state["fig"].text(0.5, MARGIN_BOT / PAGE_H * 0.55, f"{footer}   ·   page {state['n']}",
                              ha="center", va="center", fontsize=SIZES["foot"], color="0.35")
            pdf.savefig(state["fig"])
            if png_dir:
                state["fig"].savefig(f"{png_dir}/p{state['n']:02d}.png", dpi=110)
            plt.close(state["fig"])
        state["fig"] = plt.figure(figsize=(PAGE_W, PAGE_H))
        state["y"] = PAGE_H - MARGIN_TOP

    def space(h: float, pdf) -> None:
        if state["y"] - h < MARGIN_BOT:
            new_page(pdf)

    def put(lines: list[str], size: float, gap_before=0.0, gap_after=0.06, color="0.05",
            weight="normal", x=MARGIN_X, pdf=None, width=None):
        h = len(lines) * size * LEAD / 72.0
        space(h + gap_before + gap_after, pdf)
        state["y"] -= gap_before
        state["fig"].text(x / PAGE_W, state["y"] / PAGE_H, "\n".join(lines),
                          ha="left", va="top", fontsize=size, color=color, weight=weight,
                          linespacing=LEAD, family="DejaVu Sans")
        state["y"] -= h + gap_after

    with PdfPages(path, metadata={"Creator": None, "Producer": None, "CreationDate": None,
                                  "ModDate": None}) as pdf:
        new_page(pdf)
        for bi, block in enumerate(blocks):
            kind = block[0]
            if kind == "pb":
                new_page(pdf)
            elif kind == "h1":
                title = _clean(block[1])
                size = SIZES["title"] if title.startswith("Charpy Transition") else SIZES["h1"]
                put(wrap(title, size, bold=True), size, gap_before=0.16, gap_after=0.10, weight="bold", pdf=pdf)
            elif kind in ("h2", "h3"):
                key = "h2" if kind == "h2" else "h3"
                gb, ga = (0.15, 0.06) if kind == "h2" else (0.11, 0.045)
                head_lines = wrap(_clean(block[1]), SIZES[key], bold=True)
                # keep a heading with the opening lines of what follows it
                follow = blocks[bi + 1] if bi + 1 < len(blocks) else None
                lead_h = 0.0
                if follow and follow[0] == "p":
                    lead_h = min(3, len(wrap(_clean(follow[1]), SIZES["body"]))) \
                        * SIZES["body"] * LEAD / 72.0
                space(len(head_lines) * SIZES[key] * LEAD / 72.0 + gb + ga + lead_h, pdf)
                put(head_lines, SIZES[key], gap_before=gb, gap_after=ga, weight="bold",
                    color="0.05" if kind == "h2" else "0.15", pdf=pdf)
            elif kind == "p":
                lines_p = wrap(_clean(block[1]), SIZES["body"])
                extra = 0.0
                nxt = blocks[bi + 1] if bi + 1 < len(blocks) else None
                if nxt and nxt[0] == "tab" and re.match(r"\*?Table \d", _clean(block[1])):
                    # keep a table caption with the first rows of its own table
                    extra = min(6, len(nxt[1]) + 1) * SIZES["table"] * TABLE_LEAD / 72.0 + 0.12
                if extra:
                    space(len(lines_p) * SIZES["body"] * LEAD / 72.0 + extra + 0.06, pdf)
                put(lines_p, SIZES["body"], gap_after=0.055, pdf=pdf)
            elif kind == "bul":
                for item in block[1]:
                    put(["• " + l if j == 0 else "  " + l
                         for j, l in enumerate(wrap(_clean(item), SIZES["body"], COL_W - 0.12))],
                        SIZES["body"], gap_after=0.03, x=MARGIN_X + 0.10, pdf=pdf)
                state["y"] -= 0.05
            elif kind == "box":
                body = wrap(_clean(block[1]), SIZES["body"], COL_W - 0.34)
                h = len(body) * SIZES["body"] * LEAD / 72.0 + 0.14
                space(h + 0.14, pdf)
                state["y"] -= 0.06
                state["fig"].patches.append(plt.Rectangle(
                    ((MARGIN_X - 0.09) / PAGE_W, (state["y"] - h + 0.02) / PAGE_H),
                    (COL_W + 0.18) / PAGE_W, h / PAGE_H, transform=state["fig"].transFigure,
                    facecolor="0.955", edgecolor="0.75", linewidth=0.5, zorder=0))
                put(body, SIZES["body"], gap_before=0.07, gap_after=0.14,
                    x=MARGIN_X + 0.08, pdf=pdf)
            elif kind == "tab":
                rows = [[_clean(c) for c in r] for r in block[1]]
                ncol = max(len(r) for r in rows)
                rows = [r + [""] * (ncol - len(r)) for r in rows]
                widths = [max(len(r[c]) for r in rows) for c in range(ncol)]
                # Shrink the type to fit before truncating anything; truncate only as a last
                # resort, and mark it, so a clipped cell is never mistaken for a short value.
                # Shrink the type a little to fit, but never past TABLE_MIN_PT, and NEVER
                # truncate a cell: a table that still does not fit is a layout error the author
                # must resolve with a shorter display label (see `relabel`), not something the
                # build may quietly clip mid-word.
                size = SIZES["table"]
                need = sum(widths) + 2 * ncol
                while size > TABLE_MIN_PT and need > int(COL_W * 72.0 / (0.60 * size)):
                    size -= 0.1
                if need > int(COL_W * 72.0 / (0.60 * size)):
                    widest = widths.index(max(widths))
                    raise SystemExit(
                        f"WP7: a table does not fit the text column even at {size:.1f} pt and "
                        f"would have to truncate column {widest} ({max(widths)} characters wide). "
                        f"Add a concise display label for it via the table's `relabel` map rather "
                        f"than clipping a cell mid-word.")
                text = []
                for j, r in enumerate(rows):
                    text.append("  ".join(c.ljust(w) for c, w in zip(r, widths)))
                    if j == 0:
                        text.append("  ".join("-" * w for w in widths))
                # A long table may continue on the next page with its header repeated, rather
                # than moving wholesale and leaving a third of a page blank.
                line_h = size * TABLE_LEAD / 72.0
                head, rest = text[:2], text[2:]
                while rest:
                    avail_lines = int((state["y"] - MARGIN_BOT - 0.12) / line_h) - len(head)
                    if avail_lines < MIN_TABLE_ROWS and len(rest) > MIN_TABLE_ROWS:
                        new_page(pdf)
                        avail_lines = int((state["y"] - MARGIN_BOT - 0.12) / line_h) - len(head)
                    take = rest if len(rest) <= avail_lines else rest[:max(avail_lines, 1)]
                    chunk = head + list(take)
                    h = len(chunk) * line_h
                    space(h + 0.12, pdf)
                    state["fig"].text(MARGIN_X / PAGE_W, state["y"] / PAGE_H, "\n".join(chunk),
                                      ha="left", va="top", fontsize=size, color="0.05",
                                      linespacing=TABLE_LEAD, family="DejaVu Sans Mono")
                    state["y"] -= h + 0.11
                    rest = rest[len(take):]
                    if rest:
                        new_page(pdf)
            elif kind == "figs":
                imgs = []
                for path in block[1]:
                    img = mpimg.imread(str(ROOT / path))
                    crop = CROPS.get(path.replace("outputs/", ""), 0)
                    imgs.append(img[crop:] if crop else img)
                avail = PAGE_H - MARGIN_TOP - MARGIN_BOT - 0.45
                sizes = []
                for img in imgs:
                    ar = img.shape[0] / img.shape[1]
                    w = COL_W
                    sizes.append([w, w * ar, ar])
                total = sum(h for _, h, _ in sizes) + 0.10 * (len(sizes) - 1)
                # A figure must never be separated from its own caption, so reserve the caption's
                # height as part of the group before deciding whether the group fits this page.
                # Reserve the figure, any callout, and the OPENING LINES of its caption. A caption
                # that begins on the figure's page is not orphaned; reserving all of a seven-line
                # caption would push whole figures onto fresh pages and waste a third of a page.
                cap_h = 0.0
                for look in blocks[bi + 1:bi + 3]:      # a callout box may sit between the two
                    if look[0] == "box":
                        cap_h += (len(wrap(_clean(look[1]), SIZES["body"], COL_W - 0.34))
                                  * SIZES["body"] * LEAD / 72.0 + 0.20)
                    elif look[0] == "p" and re.match(r"\*?Figure \d", _clean(look[1])):
                        n_cap = min(CAPTION_KEEP_LINES,
                                    len(wrap(_clean(look[1]), SIZES["body"])))
                        cap_h += n_cap * SIZES["body"] * LEAD / 72.0
                        break
                    else:
                        break
                if total + cap_h > avail:               # scale the whole group down together
                    k = max(0.45, (avail - cap_h) / total)
                    for sz in sizes:
                        sz[0] *= k; sz[1] *= k
                    total = sum(h for _, h, _ in sizes) + 0.10 * (len(sizes) - 1)
                room = state["y"] - MARGIN_BOT - cap_h - 0.12
                if total > room >= FIG_MIN_SCALE * total:
                    # it misses by a little: shrink within a declared bound rather than blank the
                    # rest of the page. Never below FIG_MIN_SCALE of the natural size.
                    k = room / total
                    for sz in sizes:
                        sz[0] *= k; sz[1] *= k
                    total = sum(h for _, h, _ in sizes) + 0.10 * (len(sizes) - 1)
                space(total + cap_h + 0.12, pdf)        # panels and caption start on one page
                for img, (w, h, _ar) in zip(imgs, sizes):
                    ax = state["fig"].add_axes([(MARGIN_X + (COL_W - w) / 2) / PAGE_W,
                                                (state["y"] - h) / PAGE_H, w / PAGE_W, h / PAGE_H])
                    ax.imshow(img, interpolation="antialiased")
                    ax.axis("off")
                    state["y"] -= h + 0.10
                state["y"] -= 0.02
        new_page(pdf)                                   # flush the last page
        plt.close(state["fig"])
    return state["n"]


# --------------------------------------------------------------------------------------
# 7. Build
# --------------------------------------------------------------------------------------
FOOTER = ("Charpy transition temperature uncertainty and test-matrix design · "
          "analysis of published test data · regenerate with ./run_all.sh")


def _class_problems(what: str, classes) -> list[str]:
    if not classes:
        return [f"{what} carries no evidence class (D-126 item 1)"]
    bad = [c for c in classes if c not in EVIDENCE_CLASSES]
    return [f"{what} carries an unknown evidence class {c!r} (D-126 item 1)" for c in bad]


def build() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"WP7: {SOURCE} is missing")
    src = SOURCE.read_text()
    # The source's header comment documents the markup contract and therefore contains example
    # placeholders and slots; blank it out before anything lints or resolves it.
    body = blank_comments(src)
    problems = lint_source(body)

    rendered, claim_rows = resolve()
    used: set[str] = set()

    def substitute(m):
        key = m.group(1)
        used.add(key)
        if key not in rendered:
            problems.append(f"report.md uses {{{{{key}}}}}, which is not in the registry")
            return f"<<UNRESOLVED:{key}>>"
        return rendered[key]

    filled = PLACEHOLDER.sub(substitute, body)
    for key in sorted(set(REGISTRY) - used):
        problems.append(f"registry key {key!r} is never used by the report (D-114)")

    filled = expand_slots(filled)
    problems += lint_filled(filled)

    # Evidence classes: at least one, possibly several, all valid (D-125 item 2, D-126 item 1).
    for num, spec in FIGURES.items():
        for path in spec["paths"]:
            if not (OUTPUTS / path).exists():
                problems.append(f"figure {num} names outputs/{path}, which does not exist")
        problems += _class_problems(f"figure {num}", spec["classes"])
        if num in REQUIRED_COMBINATIONS and not REQUIRED_COMBINATIONS[num] <= set(spec["classes"]):
            problems.append(f"figure {num} must carry at least "
                            f"{sorted(REQUIRED_COMBINATIONS[num])} (D-126 item 1)")
    for num, spec in TABLES.items():
        problems += _class_problems(f"table {num}", spec["classes"])
        key = f"T{num}"
        if key in REQUIRED_COMBINATIONS and not REQUIRED_COMBINATIONS[key] <= set(spec["classes"]):
            problems.append(f"table {num} must carry at least "
                            f"{sorted(REQUIRED_COMBINATIONS[key])} (D-126 item 1)")

    # Provenance applies to captions, panels and callouts too, not only body prose (D-126 item 4).
    for where, authored in authored_strings().items():
        residue = strip_protected(PLACEHOLDER.sub("", authored))
        if re.search(r"\d", residue):
            problems.append(f"{where}: literal number without provenance - use a placeholder or "
                            f"register the constant (D-126 items 3, 4): {residue.strip()[:90]}")
    # Internal cross-references must point at something that exists (author review, item 3).
    headings = set()
    for line in body.splitlines():
        m = re.match(r"#{2,3}\s+([0-9]+(?:\.[0-9]+)?)[.\s]", line.strip())
        if m:
            headings.add(m.group(1).rstrip("."))
    for m in re.finditer(r"\bsections?\s+([0-9]+(?:\.[0-9]+)?)", body):
        if m.group(1) not in headings:
            line = body[:m.start()].count("\n") + 1
            problems.append(f"report.md line {line}: cross-reference to section {m.group(1)}, "
                            f"which is not a heading in this document")
    for m in re.finditer(r"\b(Figure|Table)\s+([0-9]+)", body):
        reg = FIGURES if m.group(1) == "Figure" else TABLES
        if m.group(2) not in reg:
            line = body[:m.start()].count("\n") + 1
            problems.append(f"report.md line {line}: reference to {m.group(1)} {m.group(2)}, "
                            f"which is not defined")

    used_figs = set(re.findall(r"\[\[FIG ([0-9a-z]+)\]\]", body))
    used_tabs = set(re.findall(r"\[\[TAB ([0-9a-z]+)\]\]", body))
    for num in sorted(set(FIGURES) - used_figs):
        problems.append(f"figure {num} is defined but never referenced by the report (D-115)")
    for num in sorted(set(TABLES) - used_tabs):
        problems.append(f"table {num} is defined but never referenced by the report (D-115)")

    if "<<UNRESOLVED:" in filled:
        problems.append("the filled report still contains unresolved placeholders")

    if problems:
        print("WP7 report build FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    REPORT.mkdir(exist_ok=True)
    (REPORT / "report_filled.md").write_text(filled)
    pd.DataFrame(claim_rows).to_csv(REPORT / "claim_source_map.csv", index=False)
    pd.DataFrame(constant_rows()).to_csv(REPORT / "constant_source_map.csv", index=False)
    pages = typeset(reorder_floats(parse_blocks(filled)),
                    REPORT / "charpy_test_matrix_study.pdf", FOOTER)
    print(f"WP7 report: {len(rendered)} numeric claims from "
          f"{len({r['file'] for r in claim_rows if r['file']})} generated files; "
          f"{len(CONSTANTS)} registered constants; {len(FIGURES)} figures, {len(TABLES)} tables; "
          f"{pages} pages")
    print("  report/charpy_test_matrix_study.pdf, report/report_filled.md,")
    print("  report/claim_source_map.csv, report/constant_source_map.csv")


if __name__ == "__main__":
    build()
