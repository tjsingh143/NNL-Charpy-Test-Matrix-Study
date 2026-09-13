# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Approved for merge into `main` with an explicit
  merge commit (see `git log`); branch `wp2` is kept.
- **WP3 (transition curve fitting) is the next permitted work package. WP3 has NOT started.** It begins only when the author authorizes it.

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

## Next permitted work package
- WP3 — transition curve fitting (PROJECT_BRIEF.md §5), stopping at CP3. Not started.

## Open decisions WP3 must resolve (listed only; none resolved)
- Lower shelf fixed or fitted, and at what value.
- Parameterization and parameter bounds of the tanh model.
- Exact definition and extraction of the index temperature.
- Criterion energy for each specimen geometry (full-size, sub-size, miniature) and its basis.
- How the upper-shelf energy is estimated (the WP2 screening upper reference is not USE).
- Treatment of curves with non-flat or poorly sampled upper shelves (e.g. ref 104, where energy falls above about 250 °C; still-rising top ends such as 54-247).
- Fitter validation design using synthetic curves with known truth (sampling densities, noise levels, where it stops working).
- Definition and handling of failed, non-physical and ill-conditioned fits, and how they are reported for each cohort.

## Unresolved data issues carried forward
- Refs 7, 8, 9, 53: irradiation status unresolved without full texts (excluded from the primary population, D-035).
- Ref 21's series being HSST Plate 02 is inferred from provenance evidence and the point pattern, not read from its full text (D-019).
- The approximately 0.10–0.85 transition-band alternative has no documented source; one must be cited before it is used (D-037).
