# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Merged into `main`; branch `wp2` is kept.
- **WP3 (transition curve fitting) complete — CP3 awaiting approval.** Work is on branch `wp3` (not merged into `main`).
- **WP4 (per-curve uncertainty) NOT started.** It begins only after CP3 approval and the author's authorization.

## Final CP2 numbers (2025.30 primary release; all regenerate with `./run_all.sh`)
- WP1 retains 3,198 records (2024.206 sensitivity release: 3,050). E8 removes 69 duplicate series / 910 records, of which 2 series /
  116 records by the constant-offset test (`outputs/wp1/reconciliation_table.md`, `duplicate_curve_removals.csv`).
- WP2 primary RPV population before screening: 191 curves / 2,734 records; outside it P2 48, P3 138, P4 212, P5 66 records
  (`outputs/wp2/population_accounting.csv`).
- Frozen cohorts, curves / records (`data/FROZEN_COHORTS_CP2.csv`, `outputs/wp2/cohort_manifest.csv`): primary 170 / 2,588; looser
  182 / 2,692; stricter 60 / 1,333; alt_keep_rule 170 / 2,628; plus_unresolved_irradiation 179 / 2,704; plus_additively_manufactured
  175 / 2,654; piping_secondary 15 / 181.
- Changed from the CP2 presentation: the pre-screening population was 192 / 2,736 and P2 46 / 6 curves. The author extended the
  source-contradiction exclusion to curve 1-6.3 (2 records) when CP2 was finalized (D-031). No cohort changed.

## Approved decisions that affect future work
- Primary dataset Materials Cloud 2025.30; version-sensitivity dataset 2024.206 (D-001, brief amendment A1).
- Passing the WP2 rule means only that a curve appears sufficiently sampled to ATTEMPT a fit. WP3 must validate the fitter and account
  explicitly for every failed, non-physical or ill-conditioned fit; no curve is silently removed (D-038).
- Later work packages read the cohorts from `outputs/wp2*/cohort_membership.csv` and never regenerate them with other thresholds; the
  pipeline stops if membership drifts from `data/FROZEN_COHORTS_CP2.csv` (D-039).
- The WP2 "screening upper reference" (mean of the three highest energies) is not the upper-shelf energy; USE needs its own justified
  method in WP3 (D-037). The 0.12–0.88 transition band is a project-defined, model-based convention (D-037).
- Tags carried through WP3–WP6: reconstituted specimens are separate curves, never combined with conventional specimens without an
  approved analysis (D-033); additively manufactured SA508 is secondary only and must not affect the primary headline without an approved
  sensitivity analysis (D-034); unresolved irradiation labels stay outside the primary analysis and are never guessed (D-035);
  source-contradicted labels stay outside it (D-031); SA508 Gr.1A piping is a secondary group (D-027).
- Duplicates: canonical-source hierarchy, with the alternative keep rule as a sensitivity cohort; an offset-based duplicate needs
  documented provenance and all five CP2 safeguards (D-019).
- Pre-cracked concerns: all questioned energy curves are ordinary Charpy V-notch data (D-020). 15Cr2MoV-A out of scope (D-012).
  Dataset curve IDs are provenance; mixed series are split (D-022, D-028).

## WP3 results (awaiting CP3; all regenerate with `./run_all.sh`; summary `outputs/wp3/wp3_summary.md`)
- Method (D-040 to D-048): E(T) = LSE + (USE − LSE)/2 [1 + tanh((T − T0)/C)], bounded least squares (SciPy `least_squares`, trf, six fixed
  starts), LSE fitted (pre-registered rule, D-042), USE = fitted asymptote with support diagnostics (D-043), T41J analytic for full-size
  specimens only (D-044), no index for miniature specimens (D-045), outcome categories and identifiability flags (D-046, D-047).
- Synthetic validation (SYNTHETIC; 657 scenarios, 128,216 fits, seed 20260913): pre-registered lower-shelf rule, error versus specimen
  count, pattern, parameter values, test windows, non-flat shelves; flags validated by "fits carrying only this flag" (D-047, D-048).
- Primary cohort, 170 curves, mutually exclusive outcomes: optimizer failure 0; non-physical 71 (all: fitted LSE at 0 J); boundary-limited 3;
  weakly identified 47; usable fit without index 13 (miniature); usable fit with T41J 36. T41J calculated for 132 of 134 full-size curves.
- Method evolution, including every change after results existed: D-051. Method locked at commit `0d5e548` before any published curve was fitted.
- Reproducibility check for CP3: a fresh clone of commit `20481dd` with a newly created `.venv` (from `requirements.txt`) ran `./run_all.sh`
  in 6 min 9 s and left 0 tracked files changed (all WP0–WP3 outputs byte-identical). Synthetic scenarios rerun in a single process matched
  the 8-worker results bit for bit (spot check of 4 scenarios, compared with exact float parsing).

## Decisions awaiting the author at CP3
- D-042: keep the fitted lower shelf (pre-registered outcome) or approve LSE fixed at 2.7 J for full-size curves. Evidence both ways: synthetic
  full-size T41J error lower with a fixed shelf; the rule's unintended 2 : 1 weighting; 71 published curves with LSE at 0 J (a symmetric-tanh
  shape limitation), while the fixed-shelf refit moves T41J by a median 0.3 °C.
- D-043, D-046, D-047: the upper-shelf trend test moved out of the outcome after the synthetic validation.
- D-044: T41J for the 74 full-size curves whose notch dimensions are not reported.
- D-045: no index temperature for miniature specimens.
- D-049: the dataset's DBTT behaves like a mid-transition temperature (T0), not a 41 J temperature.

## Next permitted work package
- None until CP3 is approved. WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5) is next once authorized. Not started.

## Open questions WP4 inherits from WP3 (listed only)
- Which fit outcomes and flags make a curve eligible for a WP4 confidence interval (non-physical and weakly identified fits included or not).
- The resampling scheme, and whether the lower-shelf choice (D-042) is re-examined inside it.
- How to treat T41J values that lie on the flat lower part of the fitted curve (15 of 132 full-size curves).
- Whether miniature curves get intervals on T0 and USE only (no index temperature, D-045).

## Unresolved data issues carried forward
- WP3 sources read only in part: Wallin & Baer (2023) and Miura et al. (2025), abstracts only (full texts not accessible); the CVGRAPH
  lower-shelf convention of US surveillance reports could not be retrieved and is not used (DECISIONS.md, WP3 sources).
- Refs 7, 8, 9, 53: irradiation status unresolved without full texts (excluded from the primary population, D-035).
- Ref 21's series being HSST Plate 02 is inferred from provenance evidence and the point pattern, not read from its full text (D-019).
- The approximately 0.10–0.85 transition-band alternative has no documented source; one must be cited before it is used (D-037).
