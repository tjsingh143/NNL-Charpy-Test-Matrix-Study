# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Merged into `main`; branch `wp2` is kept.
- **WP3 (transition curve fitting) complete — CP3 approved in principle by the author (2026-09-14), with amendments to D-042 (lower shelf),
  D-046 (zero-LSE classification) and D-044 (notch-metadata caveat, index-support diagnostic). The amendments are implemented and the revised
  results await final CP3 approval.** Work is on branch `wp3` (not merged into `main`).
- **WP4 (per-curve uncertainty) NOT started.** It begins only after final CP3 approval and the author's authorization.

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

## WP3 results (revised after the CP3 review; awaiting final CP3 approval; all regenerate with `./run_all.sh`; summary `outputs/wp3/wp3_summary.md`)
- Final primary method: E(T) = LSE + (USE − LSE)/2 [1 + tanh((T − T0)/C)] (D-040), bounded least squares (SciPy `least_squares`, trf, six fixed
  starts; D-041); **full-size LSE fixed at 2.7 J, miniature LSE fitted >= 0 J** (CP3 amendment of D-042, not pre-registered); USE = fitted
  asymptote with support diagnostics (D-043); T41J analytic for full-size specimens only, with the notch-metadata flag and index-support
  diagnostic (D-044); no index for miniature specimens (D-045); a fitted LSE at its 0 J bound is boundary-limited (D-046 amended); D-047 flags.
- Sensitivity case: the pre-registered all-fitted method (the rule's outcome, presented at CP3), regenerated in `outputs/wp3/sensitivity_all_fitted_lse/`;
  under the pre-CP3 classification it reproduces the CP3 counts exactly (0 / 71 / 3 / 47 / 13 / 36; the pipeline stops otherwise).
- Synthetic validation (SYNTHETIC; 774 scenarios, 148,432 fits, seed 20260913): Block L and its pre-registered rule unchanged (still selects `fitted`);
  Blocks A–E run with both methods on identical synthetic data; no scenario added or changed (D-048).
- Primary cohort, 170 curves, mutually exclusive: optimizer failure 0; non-physical (inadmissible) 0; boundary-limited 18 (15 miniature with LSE at
  0 J, 2 miniature with C at 1 °C, 1 full-size: 49-206); weakly identified 35; usable fit without index 13 (miniature); usable fit with T41J 104.
  T41J calculated for 134 of 134 full-size curves (74 with exact notch dimensions unreported); 9 carry the index-support warning.
- Full-size, all fitted against final: |ΔT41J| median 0.29 °C, 90th percentile 1.89 °C; |ΔT0| median 0.73 °C, 90th percentile 5.34 °C; |ΔUSE| median
  0.24 %; outcome category differs for 89 of 134 curves, index availability for 2 (`method_change_before_after.csv`).
- Found in the amended run, reported and not tuned: curve 33-153 gets a usable-fit T41J with no measured energy below 41 J (audit columns only);
  with the full-size shelf fixed, lower-shelf diagnostics cannot fire for full-size curves (D-042, D-047).
- Method evolution, including every change after results existed: D-051 (step 5 = the CP3 amendment). Pre-CP3 commits `11daf72`, `0d5e548`,
  `20481dd`, `a2ce7f2` are kept.
- Reproducibility check of the original CP3 state (kept for the record): a fresh clone of commit `20481dd` with a newly created `.venv` ran
  `./run_all.sh` in 6 min 9 s and left 0 tracked files changed; single-process synthetic reruns matched the 8-worker results bit for bit (4 scenarios).

## Decisions awaiting the author at final CP3 approval
- Final approval of the amended WP3 method and results, and of the proposed CP3 statuses of D-040 to D-051.
- Whether a T41J with no measured energy below 41 J (published: 33-153 only) should also carry the index-support warning; audit columns exist,
  no rule is attached (D-042, D-044).
- The author's CP3 reading of Wallin & Baer (2023) on a fixed lower shelf could not be verified: the accessible abstract does not discuss the lower
  shelf and the full text is closed-access (DECISIONS.md, WP3 sources, citation check).

## Next permitted work package
- None until CP3 is finally approved. WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5) is next once authorized. Not started. `wp3` is not merged.

## Open questions WP4 inherits from WP3 (listed only)
- Which fit outcomes and flags make a curve eligible for a WP4 confidence interval (boundary-limited and weakly identified fits included or not).
- The resampling scheme, and whether the fixed full-size lower shelf (D-042) stays fixed inside it or is varied as a sensitivity.
- How to treat T41J values with the index-support warning (9 full-size curves) and the one T41J not bracketed by measured energies (33-153).
- Whether miniature curves get intervals on T0 and USE only (no index temperature, D-045).

## Unresolved data issues carried forward
- WP3 sources read only in part: Wallin & Baer (2023) and Miura et al. (2025), abstracts only (full texts not accessible; the Wallin & Baer abstract
  was re-read at the CP3 amendment and does not contain the statements attributed to it); the CVGRAPH lower-shelf convention of US surveillance
  reports could not be retrieved and is not used (DECISIONS.md, WP3 sources).
- Refs 7, 8, 9, 53: irradiation status unresolved without full texts (excluded from the primary population, D-035).
- Ref 21's series being HSST Plate 02 is inferred from provenance evidence and the point pattern, not read from its full text (D-019).
- The approximately 0.10–0.85 transition-band alternative has no documented source; one must be cited before it is used (D-037).
