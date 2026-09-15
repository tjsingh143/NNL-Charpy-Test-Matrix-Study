# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Merged into `main`; branch `wp2` is kept.
- **WP3 (transition curve fitting) complete — CP3 approved and merged.** Approved in principle at the CP3 review with amendments to D-042, D-044
  and D-046; final approval of D-040 to D-051 by the author on 2026-09-14, with one additional support diagnostic (D-044: empirical bracketing
  of 41 J by the measured energies). Merged into `main` with an explicit merge commit; branch `wp3` is kept.
- **WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5) is in progress on branch `wp4`** (authorized by the author, 2026-09-14): method
  pre-registered in DECISIONS.md D-052 to D-065 before any bootstrap result existed. Internal WP4 review stop before WP5 (set by the author).

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
- Passing the WP2 rule means only that a curve appears sufficiently sampled to ATTEMPT a fit; every WP3 fit outcome is accounted for and no curve
  is silently removed (D-038, D-046).
- Later work packages read the cohorts from `outputs/wp2*/cohort_membership.csv` and never regenerate them with other thresholds; the
  pipeline stops if membership drifts from `data/FROZEN_COHORTS_CP2.csv` (D-039).
- The WP2 "screening upper reference" (mean of the three highest energies) is not the upper-shelf energy; USE is the WP3 fitted asymptote with
  support diagnostics (D-037, D-043). The 0.12–0.88 transition band is a project-defined, model-based convention (D-037).
- Tags carried through WP3–WP6: reconstituted specimens are separate curves, never combined with conventional specimens without an
  approved analysis (D-033); additively manufactured SA508 is secondary only and must not affect the primary headline without an approved
  sensitivity analysis (D-034); unresolved irradiation labels stay outside the primary analysis and are never guessed (D-035);
  source-contradicted labels stay outside it (D-031); SA508 Gr.1A piping is a secondary group (D-027).
- Duplicates: canonical-source hierarchy, with the alternative keep rule as a sensitivity cohort; an offset-based duplicate needs
  documented provenance and all five CP2 safeguards (D-019).
- Pre-cracked concerns: all questioned energy curves are ordinary Charpy V-notch data (D-020). 15Cr2MoV-A out of scope (D-012).
  Dataset curve IDs are provenance; mixed series are split (D-022, D-028).
- WP3 (FINAL APPROVED at CP3): symmetric tanh (D-040); deterministic bounded `least_squares`, not tuned per curve (D-041); full-size LSE fixed at
  2.7 J, miniature LSE fitted >= 0 J, all-fitted method kept as the named sensitivity case (D-042); USE = fitted asymptote (D-043); T41J for
  full-size V-notch curves only, including the 74 with exact notch dimensions unreported (flagged), with two separate index-support warnings that
  never withhold a value and are never outcomes: index position on the fitted rise and empirical bracketing by the measured energies (D-044);
  no miniature index criterion, cross-size correlation is WP5 work (D-045); outcome precedence with zero-LSE fits boundary-limited (D-046); the
  validated identifiability flags, no condition-number threshold (D-047); synthetic validation as run (D-048); dataset USE/DBTT diagnostic only
  (D-049); frozen cohorts unchanged (D-050); method history D-051 steps 1–6.

## WP3 final results (CP3 approved; all regenerate with `./run_all.sh`; summary `outputs/wp3/wp3_summary.md`)
- Final primary method: E(T) = LSE + (USE − LSE)/2 [1 + tanh((T − T0)/C)]; full-size LSE fixed at 2.7 J; miniature LSE fitted >= 0 J; USE, T0 and
  C fitted; T41J analytic for full-size curves only; no miniature index (`method_configuration.md`).
- Primary cohort, 170 curves, mutually exclusive (`fit_outcomes.csv`): optimizer failure 0; non-physical (inadmissible) 0; boundary-limited 18
  (15 miniature with LSE at 0 J, 2 miniature with C at 1 °C, 1 full-size: 49-206); weakly identified 35; usable fit without index 13 (miniature);
  usable fit with T41J 104.
- Full-size T41J (134 curves): calculated 134; usable-fit 104; index-position warning 9; empirically bracketed by the measured energies 133;
  not bracketed 1 (33-153, a usable fit; no overlap with the index-position warning or with the 74 notch-unreported curves);
  from curves with exact notch dimensions unreported 74 (`index_availability_by_geometry.csv`, `t41j_empirical_bracketing_summary.csv`).
- Curve 33-153: T41J −114.5 °C from a usable fit, but all 7 measured energies are above 41 J (lowest 42.8 J at −120.1 °C); retained unchanged,
  with the warning "T41J calculated from fitted curve; 41 J not empirically bracketed by measured energies." (D-044, `wp3_summary.md` §3.2).
- Miniature (36 curves): usable 13; boundary-limited 17 (15 with LSE at 0 J, 2 with C at 1 °C); weakly identified 6; no index criterion.
- All-fitted sensitivity case (`sensitivity_all_fitted_lse/`, `lse_sensitivity_published_summary.csv`): full-size |ΔT41J| median 0.29 °C,
  90th percentile 1.89 °C; |ΔT0| median 0.73 °C, 90th percentile 5.34 °C; |ΔUSE| median 0.24 %; outcome category differs for 89 of 134 full-size
  curves and 0 miniature curves; index availability differs for 2. Under the pre-CP3 classification it reproduces the CP3 counts
  (0 / 71 / 3 / 47 / 13 / 36; the pipeline stops otherwise).
- Synthetic validation (SYNTHETIC; 774 scenarios, 148,432 fits, seed 20260913): Block L's pre-registered rule still selects `fitted`; Blocks A–E
  run with both methods on identical data (D-048).
- Method evolution, including every change after results existed: D-051 steps 1–6. Pre-CP3 commits `11daf72`, `0d5e548`, `20481dd`, `a2ce7f2`
  and the amended states `5bd4c2c`, `76b9f87` are kept on `wp3`.
- Reproducibility check of the final CP3 state (branch `wp3`, before the merge): `./run_all.sh` in 7 min 22 s (exit 0; raw-data checksums verified;
  frozen-cohort check passed in WP2 and WP3). Compared with commit `76b9f87`: every pre-existing column of the three WP3 fit tables identical
  (170, 182 and 170 rows); the only other changed outputs are the D-044 additions (`fit_flags.csv` and its sensitivity copy,
  `index_availability_by_geometry.csv`, `method_change_before_after.csv`, `method_configuration.md`, `wp3_summary.md`, two new tables); every
  WP0–WP2 output and every synthetic output and figure byte-identical; the new flag matches an independent recomputation from the processed records.
- Earlier reproducibility checks (kept for the record): a fresh clone of `5bd4c2c` with a newly created `.venv` (CPython 3.9.6, numpy 2.0.2,
  pandas 2.2.3, scipy 1.13.1, matplotlib 3.9.4, openpyxl 3.1.5) ran `./run_all.sh` in 6 min 29 s and left 0 tracked files changed and 0 untracked
  files; single-process synthetic reruns matched the 8-worker results exactly (4 scenarios). A fresh clone of `20481dd` ran in 6 min 9 s and left
  0 tracked files changed.

## Next permitted work package
- WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5). Not started.

## Open decisions WP4 inherits from WP3 (listed only; none is decided)
- Which fit outcomes make a curve eligible for a WP4 confidence interval (whether boundary-limited and weakly identified fits are included).
- The resampling scheme, given that Charpy scatter is not constant along the curve (D-041), and whether the fixed 2.7 J full-size lower shelf
  stays fixed inside it or is varied as a sensitivity (D-042).
- How T41J values carrying either index-support warning are treated: index position (9 curves) and empirical bracketing (33-153) (D-044).
- Whether miniature curves get intervals on T0 and USE only (no index temperature, D-045).
- Which published uncertainty estimates the brief's WP4 cross-check uses, and on which comparable quantity.

## Unresolved data issues carried forward
- WP3 sources read only in part: Wallin & Baer (2023) and Miura et al. (2025), abstracts only (full texts not accessible). The accessible
  Wallin & Baer abstract does not contain the statements attributed to it before CP3, nor the author's CP3 reading on a fixed lower shelf, which
  remains the author's basis and is not verified in this repository (DECISIONS.md, WP3 sources). The CVGRAPH lower-shelf convention of US
  surveillance reports could not be retrieved and is not used.
- Refs 7, 8, 9, 53: irradiation status unresolved without full texts (excluded from the primary population, D-035).
- Ref 21's series being HSST Plate 02 is inferred from provenance evidence and the point pattern, not read from its full text (D-019).
- The approximately 0.10–0.85 transition-band alternative has no documented source; one must be cited before it is used (D-037).
