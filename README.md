# Charpy Transition Temperature Uncertainty and Test Matrix Study

An analysis of published Charpy V-notch test data for reactor pressure vessel (RPV) steels. No Charpy tests were performed for
this project; all measurements come from the published dataset credited below.

## Research question

A reactor pressure vessel surveillance capsule holds a small, fixed volume of irradiated material. It can be spent on a few
full-size Charpy specimens or on many miniature ones. **Which choice gives a better-determined ductile-to-brittle transition
temperature once both curve-fitting uncertainty and sub-size-to-full-size correction uncertainty are counted?**
Full requirements: `PROJECT_BRIEF.md`.

This is a test-programme *design* question. It is not an attempt to predict full-size properties from sub-size specimens.

## Status

| Work package | State |
|---|---|
| WP0 Acquisition and data dictionary | done (CP1 approved; regenerated for the 2025.30 primary release) |
| WP1 Cleaning and normalization | done (CP1 approved; corrections surfaced in WP2 approved at CP2) |
| WP2 Curve grouping and inclusion criteria | done (CP2 approved; cohorts frozen) |
| WP3 Transition curve fitting | done (CP3 approved; merged into `main`) |
| WP4 Per-curve uncertainty | done (internal review approved; merged into `main`) |
| WP5 Specimen size effect | done (CP4 approved; merged into `main`) |
| WP6 Monte Carlo test matrix study | done (CP5 approved; merged into `main`) |
| WP7 Report and repository | done (final author review approved; merged in `e752c7e`; post-audit remediation recorded in D-127) |

Progress and open issues: `PROGRESS.md`. Every judgement call: `DECISIONS.md`. WP4 intervals are nominal 95 % percentile bootstrap intervals,
not intervals calibrated to exactly 95 % coverage (`DECISIONS.md` D-056).

The project and the author-authorized post-audit remediation are complete (D-127). The final warm run passed
in 9 minutes 51.63 seconds; the accepted scientific results are unchanged. The report has 114 registered numeric
claims and 20 registered constants. An explicit reuse license for the project's own code/report remains an author choice.

WP5 finding, in one line: the classical ligament-volume normalization plus a published temperature correction removes most of
the specimen-size difference (median |T0 difference| 67 → 16 °C) but leaves a residual index-temperature disagreement with a
family-weighted standard deviation of about 11 °C, and the dataset contains too few genuinely matched families (7 in the primary
analysis set, 10 in total) to establish a size-correction uncertainty for any individual specimen geometry
(`outputs/wp5/wp5_summary.md`).

WP6 finding, in one line (SYNTHETIC Monte Carlo; CP5 approved, stated in the conditional form the author approved): a miniature-specimen programme carries an
error floor of about 12 deg C in the recovered full-size T41J - the size-correction residual, which does not average away
with specimen count - with 189 miniature wins at k = 4 and 45 at k = 6 (and none with a clustered design);
at tested budgets from eight full-size specimens' worth they win no comparison under any
placement strategy, true curve or geometry, and from eighteen full-size specimens win every one. Under the conservative
correction, the empirical all-STRICT pool or the Wallin or Towers normalizations, full-size wins every sensitivity
comparison run (budgets of six and twelve) (`outputs/wp6/wp6_summary.md`).

## The finding, in plain language

A reactor surveillance capsule holds a fixed, irreplaceable volume of irradiated steel. It can be
machined into a few full-size Charpy specimens or into many miniature ones.

Fitting a transition curve gets more accurate as specimens are added, roughly as one over the square
root of the count. Correcting a miniature result back to full-size behaviour does not: that error
depends on how well the published correlation suits the material, and testing more specimens does
not improve it. A miniature programme's total error therefore falls with specimen count only until
it reaches the correction error, and then stops. Under this project's central assumptions that floor
is about 12 °C.

So **miniature specimens help only while the material budget is very small, and full-size specimens
dominate as the budget rises** — a conditional result, using a pooled and weakly supported
correction, under the assumptions tested. It is **not** a finding that full-size specimens are
preferable in general. Three limits travel with it: the correction rests on a handful of
independently matched material families and **no individual miniature geometry is supported on its
own**; the evidence is miniaturized (MCVN), not conventional ASTM E23 sub-size, which this dataset
cannot address at all; and the volume accounting is idealised finished-specimen accounting, not a
capsule machining-yield model. For a material whose transition is very cold, a miniature specimen
may not be testable cold enough to see its own transition at any budget.

The longer explanation, written for a reader meeting this for the first time, is
`report/PLAIN_LANGUAGE.md`. The full argument and its evidence are in
`report/charpy_test_matrix_study.pdf`.

## Reproduce every figure and every number

`./run_all.sh` regenerates everything, then rebuilds the report from the regenerated tables. No
number is typed into the report: each is substituted at build time from a named file, row and
column, and the build fails on an unresolved, unused or stale placeholder, on any literal number
that is not a registered constant, or on a forbidden phrase.

| Report figure | Regenerated by | File |
|---|---|---|
| 1 Fitter validation against known truth | `src/wp3_validation.py` | `outputs/wp3/synthetic_error_vs_specimens.png` |
| 2 Worked example with its bootstrap band | `src/wp4_uncertainty.py` | `outputs/wp4/worked_example_t41j_bootstrap.png` |
| 3(a) Before and after the size normalization | `src/wp5_size_effect.py` | `outputs/wp5/before_after_normalization.png` |
| 3(b) The residual, by geometry and product form | `src/wp5_size_effect.py` | `outputs/wp5/size_correction_residuals.png` |
| 4 The fixed-material-volume comparison | `src/wp6_experiment.py` | `outputs/wp6/fixed_volume_comparison.png` |
| 5 Uncertainty against specimen count | `src/wp6_experiment.py` | `outputs/wp6/rmse_vs_specimen_count.png` |
| 6 How uncertain the correction may be | `src/wp6_experiment.py` | `outputs/wp6/correction_uncertainty_flip.png` |
| 7 Prior knowledge and estimator availability | `src/wp6_experiment.py` | `outputs/wp6/prior_error_vs_performance.png` |

Where every number came from: `report/claim_source_map.csv` (one row per numeric claim, with its
file, row selector and column) and `report/constant_source_map.csv` (every literal constant, with
its provenance category and source).

## Definition of done

The eleven requirements of `PROJECT_BRIEF.md` section 10, each with the file that evidences it.

| Requirement | Evidence |
|---|---|
| Every figure and number regenerates from raw data with one command | `run_all.sh`, `report/claim_source_map.csv` |
| The main research question has a direct, quantitative, conditioned answer | `report/report.md` section 8 |
| Q1 through Q4 are each answered | `report/report.md` sections 6.1 to 6.4 |
| Fitter validation recovers known truth and names where it fails | `outputs/wp3/wp3_summary.md` |
| Per-curve uncertainties are cross-checked against published values | `outputs/wp4/published_uncertainty_crosscheck.csv` |
| The limitations section addresses every required item | `report/report.md` section 7 |
| `DECISIONS.md` covers every required judgement call | `DECISIONS.md` |
| Attribution and license appear in README, report and data directory | `data/README.md`, `data/LICENSE-CC-BY-4.0.txt` |
| The relationship to the 2026 sub-size ML paper is stated explicitly | `report/report.md` section 7.7 |
| Nothing in the repository implies the author ran physical tests | `report/PLAIN_LANGUAGE.md` |
| All checkpoints were reached, presented and approved | `PROGRESS.md`, `DECISIONS.md` |

## Checkpoint history

`main` holds only checkpoint-approved states, one merge commit per checkpoint:
`9bc28fc` CP1 (WP0, WP1) · `dc2b840` CP2 (WP2) · `b47d08e` CP3 (WP3) · `0b5dad6` internal WP4
review · `c6be3ae` CP4 (WP5) · `6746f4d` CP5 (WP6) · `e752c7e` final author-approved WP7 merge.
That merge is the approved baseline for the bounded post-audit remediation in D-127. Branches `wp2` to `wp7`
are kept. There is no remote.

## A convention worth knowing before reading the generated summaries

Each work package's generated summary carries the approval status it had **when it was written**,
because changing that text would mean editing and rerunning an approved analysis. `DECISIONS.md`
and `PROGRESS.md` are authoritative for approval status. Three such lines remain, all true when
generated and all since decided: `outputs/wp4/wp4_summary.md` describes its review as awaiting the
author; `outputs/wp5/wp5_summary.md` describes CP4 as awaiting approval; `outputs/wp6/wp6_summary.md`
lists the adaptive-algorithm wording as open. For the same reason `outputs/wp5/wp5_summary.md` also
carries a magnitude comparison with the 2026 machine-learning paper which the report deliberately
does **not** carry forward, because the two studies' metrics are not commensurable (`DECISIONS.md`
D-125).

D-127 explicitly authorizes correction of the WP6 summary's k=4-only and universal-stability claims. Its
accepted scientific tables remain unchanged; separately named paired-stability tables record the bounded
verification. The previous summary remains available in the approved `e752c7e` Git tree.

One further wording rule, recorded as D-126: the plate-only arithmetic gives a larger
correction-error floor than the pooled central case, and **no simulated winner or tie labels were
recomputed for this plate-only scenario** — it was never part of the frozen experiment grid.

One presentation-only rendering operation is declared, recorded as D-124 step 7a. The title of
`outputs/wp6/rmse_vs_specimen_count.png` is clipped at both edges **in the approved WP6 file
itself**. That file is not edited; instead the report masks its top 44 rows when embedding it, and
a check verifies the masked strip contains no plot structure and that the plot frame survives. The
source file and its digest are unchanged and remain the provenance.

## Data attribution (required)

Lee, I., Merickel, J. W., Kasala Sreenivasulu, Y., Xu, F., Tang, Y., Rittenhouse, J. E., Vakanski, A., & Song, R.
*Dataset of Charpy V-notch impact test records of nuclear structural materials.* Materials Cloud Archive 2025.30, record q4x6v-dyt25,
DOI [10.24435/materialscloud:p6-5y](https://doi.org/10.24435/materialscloud:p6-5y) (2025). License: CC BY 4.0. **Primary dataset.**

The earlier release, Materials Cloud Archive 2024.206, record eny5v-www93, DOI
[10.24435/materialscloud:gh-za](https://doi.org/10.24435/materialscloud:gh-za) (2024), CC BY 4.0, is used as the version-sensitivity dataset.

Descriptor paper: Lee, I. et al. (2025). Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy
V-Notch Impact Testing. *Scientific Data* 12, 543. [doi:10.1038/s41597-025-04823-1](https://doi.org/10.1038/s41597-025-04823-1)

Which release is primary, and why, is decision D-001 (approved at CP1); see also `data/README.md`.

The repository's own code and report do not yet have an explicit reuse license. Choosing one remains an author
decision; the dataset's CC BY 4.0 license does not supply a license for those original project materials (D-127).

## Reproduce

```bash
./run_all.sh
```

Creates `.venv/` with the pinned packages if it does not exist, verifies the raw-data checksums, and regenerates everything in
`outputs/` and `data/processed/` from `data/raw/` (WP0, WP1 for both dataset releases, WP2 including `outputs/wp2/example_curves.png`,
WP3 synthetic fitter validation and fits to the published curves, each with the final primary method and the all-fitted lower-shelf sensitivity case, WP4 bootstrap checks and per-curve uncertainty). WP2 ends by checking that every cohort still has the membership frozen
at checkpoint CP2 (`data/FROZEN_COHORTS_CP2.csv`) and stops if it does not; WP3 repeats that check before fitting anything.
WP3's synthetic validation uses a fixed seed and runs in parallel worker processes; its results do not depend on the number of workers. WP4 (bootstrap uncertainty) adds 1.5-2.5 hours with the default 3 worker processes on the 8 GB development Mac (87 min measured for its two scripts; 2 h 15 min while other applications loaded the machine heavily): its SYNTHETIC checks and the 2,000-replicate bootstraps of every primary curve use per-replicate seeds, so their results do not depend on the number of worker processes either. WP4 reuses fingerprinted checkpoints in the git-ignored `cache/` when the code, package versions, parameters and input data are unchanged, so a repeat run takes about a minute for WP4; delete `cache/` to force a full recomputation. WP5 (pair inventory, size normalization and its checks) adds seconds. WP6 (the Monte Carlo test-matrix study) adds
about 6.4 hours from a cold cache (381 min measured with 3 worker processes on the 8 GB development Mac, peak memory
321 MB); it reuses fingerprinted checkpoints in the git-ignored `cache/wp6/`, so a repeat run takes about 1.5 minutes.
The separately reported D-127 paired-stability verification adds 63 cached arms at R = 4,000; completing the 52
previously absent arms took 14.1 minutes. WP6 keys include resolved calibration/scatter inputs and source content.
Every WP6 number is SYNTHETIC and its per-replicate seeds make it independent of the worker count. On a laptop, keep
the machine awake for a cold WP6 run (for example `caffeinate -i ./run_all.sh` on macOS): system sleep does not change
any result, but it stretches the wall-clock time (one verified cold run took 21 h because the machine slept on battery).

## Repository layout

| Path | Contents |
|---|---|
| `PROJECT_BRIEF.md` | Requirements (with approved amendments listed at the top) |
| `DECISIONS.md` | Every judgement call, with alternatives and consequences |
| `PROGRESS.md` | Last checkpoint, decisions in force, next permitted work, open issues |
| `CLAUDE.md` | Persistent working rules for AI-assisted sessions on this repository |
| `data/` | Vendored raw data, license, checksums, processed data, CP2-frozen cohort fingerprints (see `data/README.md`) |
| `src/common.py` | Paths, checksum verification, spreadsheet loader |
| `src/curated_metadata.py` | All hand-curated inputs: column meanings, name maps, reference-level evidence |
| `src/wp0_data_dictionary.py` | WP0: checksums, workbook audit, data dictionary, version comparison |
| `src/wp1_clean.py` | WP1: cleaning, flags, exclusions, duplicate detection, reconciliation |
| `outputs/wp0/` | Data dictionary and WP0 reports |
| `outputs/wp1/` | Reconciliation table and WP1 reports (primary dataset, 2025.30) |
| `outputs/wp1_sensitivity_eny5v-www93/` | The same WP1 reports for the version-sensitivity dataset (2024.206) |
| `src/wp2_curves.py` | WP2: curve grouping, sampling descriptors (no fitting), pre-fit screening rules, cohorts, frozen-cohort check |
| `outputs/wp2/` | Curve inventory, population accounting, rule outcomes, cohort membership and manifest, version comparison, example figure (primary dataset) |
| `outputs/wp2_sensitivity_eny5v-www93/` | The same WP2 reports for the version-sensitivity dataset |
| `src/wp3_fitter.py` | WP3: tanh model, bounded least-squares fit, diagnostics, index temperature, outcome categories |
| `src/wp3_validation.py` | WP3: fitter validation on SYNTHETIC curves with known truth (lower-shelf decision rule, error vs sampling and scatter) |
| `src/wp3_fit_curves.py` | WP3: fits to the published curves of the frozen cohorts, outcome accounting, comparisons, `wp3_summary.md` |
| `outputs/wp3/` | `synthetic_*` = SYNTHETIC validation outputs; all other files = fits to published data (`wp3_summary.md` collects them); final primary method. `sensitivity_all_fitted_lse/` = the pre-registered all-fitted lower-shelf method, kept as a sensitivity case |
| `src/wp4_bootstrap.py` | WP4: pairs (primary) and fixed-design wild (sensitivity) bootstrap, refitting every replicate with the approved WP3 functions; failure-aware summaries |
| `src/wp4_validation.py` | WP4: SYNTHETIC checks of the bootstrap (zero scatter, determinism, failure accounting, coverage on WP3 scenarios) |
| `src/wp4_uncertainty.py` | WP4: per-curve bootstrap uncertainty of the published primary curves, residual scatter, sampling analysis, published cross-check, figures, `wp4_summary.md` |
| `outputs/wp4/` | `synthetic_*` = SYNTHETIC bootstrap checks; all other files = uncertainty of the published curves (`wp4_summary.md` collects them) |
| `src/wp5_normalization.py` | WP5: the classical size-normalization equations (ligament volume B b², Sokolov Eq. 22 and the pre-declared alternatives) with their self-checks |
| `src/wp5_pairs.py` | WP5: the specimen-size pair inventory and data-sufficiency assessment, run before any normalization exists |
| `src/wp5_size_effect.py` | WP5: mapping the matched smaller-specimen curves into the full-size-equivalent domain, the residual ΔT_size, sensitivities, figures, `wp5_summary.md` |
| `src/wp5_tests.py` | WP5: independent checks (pairing audit, leakage, sign convention, round trip, raw-data immutability, evidence thresholds) |
| `outputs/wp5/` | Pair inventory and sufficiency, normalization factors and method configuration, normalized points, residuals, summaries, sensitivities, the WP6 handoff and four figures (`wp5_summary.md` collects them). No synthetic data: every row is published measured data, a fitted parameter from it, or a transformed estimate derived from it |
| `src/wp6_design.py` | WP6: specimen geometries, the idealized fixed-volume accounting, the raw-specimen temperature frame and the five placement strategies (no access to the truth) |
| `src/wp6_scatter.py` | WP6: the scatter models C1 (central), C1-robust, C2, C3-centred, C3-uncentered and miniature-inflated, their calibration and the cohort re-aggregation |
| `src/wp6_correction.py` | WP6: the size-correction scenarios read from the WP5 outputs, the family-level pools and the normalization scenarios |
| `src/wp6_simulator.py` | WP6: one SYNTHETIC test programme from a known truth to a recovered T41J, and the per-cell worker |
| `src/wp6_checkpoint.py` | WP6: fingerprinted checkpoints in the git-ignored `cache/wp6/` |
| `src/wp6_validation.py` | WP6: the 19 simulator validation tests and the declared runtime/memory benchmark |
| `src/wp6_experiment.py` | WP6: the frozen 6,188-cell grid, the paired comparisons, the correction threshold, coverage, stability, tables, figures and `wp6_summary.md` |
| `src/wp6_tests.py` | WP6: independent checks of the generated outputs, importing no WP6 code path they check |
| `src/wp7_report.py` | WP7: the report's numeric-claim registry and constant registry, substitution, honesty lint, and the PDF typesetter |
| `src/wp7_tests.py` | WP7: independent checks of the built report, including the PDF delivery-integrity check |
| `report/` | The technical report and its source, the plain-language explanation, and the claim and constant source maps |
| `run_all.sh` | Regenerates every output and rebuilds the report from the raw data |
| `requirements.txt` | The pinned environment every result was produced in (`DECISIONS.md` D-002) |
| `cache/` | Git-ignored fingerprinted checkpoints for WP4 and WP6; delete to force full recomputation |
| `AGENTS.md` | A pointer to `CLAUDE.md`, so the working rules have a single source |
| `outputs/wp6/` | Every file SYNTHETIC (Monte Carlo test-matrix study; not published measurements): the frozen grid, per-cell results, paired comparisons, the fixed-volume headline, the correction threshold, sensitivities, coverage, stability, nine figures, `wp6_summary.md` |
