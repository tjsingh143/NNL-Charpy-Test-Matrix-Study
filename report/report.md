<!--
REPORT SOURCE — PRE-REGISTERED OUTLINE (WP7, DECISIONS.md D-113 to D-124)

This file is the hand-written source of the technical report. It is committed in outline form
BEFORE any prose, any build or any PDF exists (D-124 step 2).

MARKUP CONTRACT (fixed here; src/wp7_report.py implements it)
  {{key}}                  a numeric claim, resolved from the registry in src/wp7_report.py.
                           The registry names, per key: the generated file, the row selector,
                           the column and the print format. The build fails on an unresolved
                           key, a missing file, a selector matching != 1 row, or an unused
                           registry entry (D-114).
  {{=key}}                 a DERIVED numeric claim. The registry records the inputs and the
                           expression as well, and claim_source_map.csv prints them (D-114, D-123).
  [[FIG n]]                embed report figure n (see the FIGURES block below).
  [[TAB n]]                render report table n from its generated file (see TABLES below).
  [[BOX ...]] ... [[/BOX]] an "In plain terms" box (D-120).
  <!-- lint:allow-digits --> marks the NEXT line as a protected span, for dates, section and
                           equation numbers, citation years and dimensions quoted from a
                           standard. Everything else containing a digit must be a placeholder
                           or a rendered table, or the build fails (D-114).

EVIDENCE CLASSES (D-117). Every [[FIG]] and [[TAB]] carries exactly one; the build fails otherwise.
  MEASURED (published) | FITTED (derived from published data)
  TRANSFORMED ESTIMATE (derived from published smaller-specimen measurements) | SYNTHETIC

FIGURES (D-115; every file already exists and regenerates; WP7 creates no new figure)
  1   outputs/wp4/worked_example_t41j_bootstrap.png      FITTED          brief fig 1
  2   outputs/wp6/rmse_vs_specimen_count.png             SYNTHETIC       brief fig 2
  3a  outputs/wp5/before_after_normalization.png         TRANSFORMED     brief fig 3
  3b  outputs/wp5/size_correction_residuals.png          TRANSFORMED     brief fig 3
  4   outputs/wp6/fixed_volume_comparison.png            SYNTHETIC       brief fig 4
  5   outputs/wp6/correction_uncertainty_flip.png        SYNTHETIC
  6   outputs/wp6/prior_error_vs_performance.png         SYNTHETIC
  7   outputs/wp3/synthetic_error_vs_specimens.png       SYNTHETIC

TABLES (D-115)
  1  outputs/wp1/reconciliation_table.csv                                    MEASURED
  2  outputs/wp2/population_accounting.csv + outputs/wp2/cohort_manifest.csv MEASURED
  3  outputs/wp3/fit_outcomes.csv + outputs/wp3/index_availability_by_geometry.csv  FITTED
  4  outputs/wp4/interval_curve_accounting.csv + outputs/wp4/published_uncertainty_crosscheck.csv  FITTED
  5  outputs/wp5/size_correction_summary_overall.csv (+ _by_product_form, _by_irradiation)  TRANSFORMED
  6  outputs/wp6/fixed_volume_comparison.csv                                 SYNTHETIC
  7  outputs/wp6/correction_threshold.csv                                    SYNTHETIC
  8  outputs/wp6/sensitivity_summary.csv                                     SYNTHETIC

PAGE BUDGET (D-115, brief 6.1: roughly 10-15 pages of body)
  front 0.5 | 1: 1.5 | 2: 1.0 | 3: 1.5 | 4: 2.0 | 5: 1.5 | 6: 3.5 | 7: 2.5 | 8: 1.0 | 9: 1.0
  = 16.0 target, trimmed to 13-15 at build; appendices A and B sit outside the body count.
-->

# Charpy Transition Temperature Uncertainty and Test-Matrix Design for Reactor Pressure Vessel Steels

## Front matter
<!-- byline, date, abstract (150 words), honesty statement, dataset attribution + CC BY 4.0,
     descriptor citation, the four evidence classes defined once (D-117) -->

## 1. Objective and scope
### 1.1 The research question
### 1.2 [[BOX why a surveillance capsule makes this a real choice]]
### 1.3 Scope, and the relationship to published work

## 2. Data source, provenance and license

## 3. Data cleaning and inclusion criteria
### 3.1 Reconciliation  [[TAB 1]]
### 3.2 Republished tests
### 3.3 What defines one transition curve, and which curves are fittable  [[TAB 2]]

## 4. Methods
### 4.1 The transition-curve model and the lower shelf
### 4.2 Upper shelf, index temperature, and why miniature curves get no index
### 4.3 Per-curve uncertainty
### 4.4 The classical size normalization
### 4.5 The Monte Carlo test-programme simulator
### 4.6 [[BOX what a bootstrap is, and why one correction draw per programme]]

## 5. Fitter validation
<!-- SYNTHETIC throughout; where the method stops working -->  [[FIG 7]]

## 6. Results
### 6.1 Fitting the published curves (Q1)  [[TAB 3]]
### 6.2 Per-curve uncertainty and its cross-check (Q1, Q2)  [[FIG 1]] [[TAB 4]]
### 6.3 The specimen size effect (Q3)  [[FIG 3a]] [[FIG 3b]] [[TAB 5]]
### 6.4 The test-matrix study (Q2, Q4)  [[BOX the answer in plain terms]] [[FIG 2]] [[FIG 4]] [[FIG 5]] [[FIG 6]] [[TAB 6]] [[TAB 7]]
### 6.5 Sensitivities  [[TAB 8]]

## 7. Uncertainty and limitations
### 7.1 What the data are
### 7.2 What the model is
### 7.3 What the correction is
### 7.4 What the simulation assumes
### 7.5 Sensitivity to the inclusion criteria and the scatter model
### 7.6 Physical reachability
### 7.7 What the analysis could not determine
### 7.8 Relationship to the 2026 machine-learning correlation paper

## 8. Conclusions

## 9. References

## Appendix A — Claim-to-source map
## Appendix B — Reproducibility
