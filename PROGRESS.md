# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Merged into `main`; branch `wp2` is kept.
- WP3 (transition curve fitting) complete — CP3 approved (final approval of D-040 to D-051 by the author, 2026-09-14) and merged into `main`
  (merge commit `b47d08e`); branch `wp3` is kept.
- **WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5) complete — INTERNAL REVIEW awaiting the author.** Work on branch `wp4`, not merged. The
  internal review stop before WP5 was set by the author because the WP4 uncertainty and scatter decisions affect WP6; every WP4 decision
  (D-052 to D-067) is provisional until that review.
- **WP5 (specimen size effect) NOT started.**
- The official checkpoint CP4 (PROJECT_BRIEF.md §9) will occur after WP5.

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

## WP4 results (internal review; regenerate with `./run_all.sh`; summary `outputs/wp4/wp4_summary.md`)
- Methods (D-052 to D-056): PRIMARY nonparametric pairs (case) bootstrap and a fixed-design wild bootstrap SENSITIVITY (Rademacher signs, HC2
  leverage-adjusted residuals); every replicate refitted with the unchanged approved WP3 functions (full-size LSE fixed at 2.7 J, miniature LSE
  fitted); B = 2,000 per curve and method for all 170 primary curves; per-replicate seeds from 20260914; 95 % percentile intervals; a reportable
  interval needs finite target values in >= 95 % of the replicates requested (project rule); primary CI for usable original fits, diagnostic
  interval for weakly identified or boundary-limited ones (D-057, D-058).
- SYNTHETIC checks (`synthetic_bootstrap_validation.md`): zero scatter, determinism (1, 2, 3 and 8 worker processes) and failure accounting all
  pass. Coverage of 95 % intervals over 200 WP3 data sets per scenario: pairs 89.5 % (T41J) well sampled, 93 % high scatter, 97 % weakly sampled,
  96.5 % (T0) miniature; fixed-design 80 %, 75 %, 38.5 % and 75.5 % (anti-conservative).
- Curve accounting, pairs (D-058): full-size T41J 66 primary CIs + 14 diagnostic + 54 unavailable (134); full-size USE and T0 104 + 30 + 0;
  miniature T0 and USE 13 + 23 + 0 (36). Fixed-design: full-size T41J 97 + 29 + 8. No miniature index criterion. Every unavailable T41J interval
  comes from replicates whose 41 J crossing falls below their own tested range; availability follows the number of measured energies below 41 J
  (Spearman 0.89; reportable 0 of 12 curves with 0-1 such energies, 3 of 30 with 2, 47 of 61 with 3-4, 30 of 31 with 5 or more).
- Full-size T41J, pairs, usable fits with a primary CI (66): SD median 4.9 °C (10th-90th percentile 2.9-9.1 °C), 95 % width median 19.4 °C
  (11.7-35.7 °C). Index-position-warned curves larger (SD median 8.3 °C, 4 reportable of 9). Curve 33-153: T41J finite in 44 % of pairs
  replicates (interval unavailable), no replicate energy bracketing 41 J; fixed-design 76 % finite, synthetic energies bracket 41 J in 51 %.
- Miniature T0, pairs (36 reportable): SD median 12.2 °C (10th-90th 3.9-51 °C); USE 95 % width / USE median 20 % (full-size) and 30 %
  (miniature), heavy upper tails where upper-shelf specimens are few.
- Drivers (Spearman, association only): full-size T41J SD with specimens inside T0 ± C (-0.32), upper-shelf specimens (-0.30), N (-0.28);
  availability with lower-shelf specimens (0.57) and N (0.46); USE width with upper-shelf specimens (-0.70); miniature T0 SD with N (-0.57).
- Published cross-check (D-063): pairs SD of usable full-size T41J with a primary CI, median 4.87 °C at median N 14 (4.43 °C for the 23 curves
  with 15-25 specimens) against Marini's (2020) sigma(T41) 3.52 °C for the 18-specimen RCC-M matrix; median SD × sqrt(N) 20.4 against his Eq. 6
  best-estimate amplitude 12.4-19.6 (12 % below, 35 % within, 41 % above his upper-bound maximum 23.1); Theil-Sen slope of log SD on log N
  -0.32 (95 % CI -0.59 to -0.10). Broadly comparable, typically 25-40 % larger, and far more heterogeneous.
- Pairs against fixed-design SD (both reportable): full-size T41J median ratio 1.06 (10th-90th 0.93-1.48); miniature T0 1.56 (1.13-4.30); USE
  about 2-2.5; largest where 1-4 influential transition specimens carry the fit.
- Monte Carlo stability (16 predeclared curves, independent B = 4,000): T41J percentiles moved by at most 5.9 % of the interval width; one
  multimodal T0 (104-none.3) by 51 %; no reportability change.
- Empirical published-data residual scatter (D-061, D-066): full-size SD / fitted USE 0.036 (lower shelf), 0.073, 0.105, 0.100, 0.062 (upper
  shelf); no product-form stratification supported; WP6 candidates C1-C3 proposed, not chosen.
- Worked example (D-065): curve 3-17, A533B plate, irradiated, 18 specimens: T41J 120.4 °C, pairs 95 % CI 112.0-129.7 °C, SD 4.4 °C.
- Execution: the first synthetic validation run was stopped by the environment for low memory (8 GB machine); rerun with a memory-safe,
  checkpointed implementation and identical results (D-067 steps 3-5). Published-data run 40.5 min, peak 300 MB.
- Reproducibility check of the WP4 state (branch `wp4`, D-067 step 8): `./run_all.sh` in the repository with the bootstrap checkpoint cache moved
  aside, so every bootstrap was recomputed from the raw data: exit 0 in 3 h 01 min while other applications loaded the 8 GB machine heavily (WP4
  synthetic validation 59.6 min, published data 75.5 min); raw-data checksums verified; frozen-cohort check passed in WP2, WP3 and WP4; the WP4
  refits reproduced all 170 WP3 point fits; peak memory of the Python processes 813 MB. All 151 tracked output and processed-data files were
  rewritten and 0 changed (every WP4 table and figure and the gzip audit file byte-identical); data, WP0–WP3 outputs and WP0–WP3 code are
  identical to `main` (`b47d08e`). A fresh clone of `ea1ec97` with a newly created `.venv` (CPython 3.9.6, numpy 2.0.2, pandas 2.2.3, scipy
  1.13.1, matplotlib 3.9.4, openpyxl 3.1.5) regenerated all 151 files with 0 tracked files changed and 0 untracked files. The environment
  stopped that run once for low memory during the synthetic coverage study (other applications held most of the memory; 26 of 32 coverage blocks
  written, each byte-identical to the repository run's); the two remaining WP4 scripts were resumed in the same clone from its own verified
  checkpoints (WP0–WP3 6 min 43 s including the environment set-up; WP4 about 81 min; peak 414 MB after the resume).

## Open decisions WP4 inherited from WP3 (resolved provisionally in WP4, for the author's review)
- Eligibility for intervals: all 170 curves bootstrapped; primary CI for usable fits, diagnostic interval otherwise (D-058).
- Resampling scheme: pairs bootstrap primary, fixed-design wild bootstrap sensitivity (D-052, D-053); the 2.7 J full-size shelf held fixed (D-054).
- T41J support warnings carried into the replicates (D-059); miniature curves: T0 and USE intervals only, LSE and C diagnostic (D-056).
- Published cross-check: Marini (2020) sigma(T41) and Eq. 6 amplitudes against the bootstrap SD (D-063).

## Decisions awaiting the author's internal WP4 review (none is final)
- D-052 to D-065 as pre-registered, and D-067 (method history, including the memory fix).
- Whether the 54 unavailable full-size T41J intervals under the 95 % rule stay the reported result, or a clearly labelled sensitivity (for example
  intervals from the analytic crossing that ignore the tested-range rule) is added; nothing of the kind was run.
- How WP5 and WP6 treat the fixed-design sensitivity, given its demonstrated under-coverage.
- D-066: which WP6 scatter-model candidates are carried into WP6.

## Next permitted work package
- None until the author completes the internal WP4 review. WP5 (specimen size effect) has NOT started.

## Unresolved data issues carried forward
- WP4 sources: Miura et al. was read as the non-peer-reviewed SSRN preprint; the published IJPVP version was not accessible. Marini (2020) and
  Switzner et al. (2023) were read from Internet Archive copies of the publishers' open-access PDFs; the scanned Efron & Tibshirani (1986) pages
  were read as images. Freedman (1981), Wu (1986), Liu (1988), Mammen (1993) are cited only through MacKinnon (2012) and Davidson & Flachaire
  (2001).
- WP3 sources read only in part: Wallin & Baer (2023) and Miura et al. (2025), abstracts only (full texts not accessible) [WP4: the Miura preprint's full text was read]. The accessible
  Wallin & Baer abstract does not contain the statements attributed to it before CP3, nor the author's CP3 reading on a fixed lower shelf, which
  remains the author's basis and is not verified in this repository (DECISIONS.md, WP3 sources). The CVGRAPH lower-shelf convention of US
  surveillance reports could not be retrieved and is not used.
- Refs 7, 8, 9, 53: irradiation status unresolved without full texts (excluded from the primary population, D-035).
- Ref 21's series being HSST Plate 02 is inferred from provenance evidence and the point pattern, not read from its full text (D-019).
- The approximately 0.10–0.85 transition-band alternative has no documented source; one must be cited before it is used (D-037).
