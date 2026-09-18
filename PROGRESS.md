# PROGRESS

## Checkpoint state
- WP0 (acquisition and data dictionary) complete — CP1 approved.
- WP1 (cleaning and normalization) complete — CP1 approved. The WP1 corrections surfaced during WP2 were approved at CP2 (D-019, D-029, D-031).
- WP2 (curve grouping and inclusion criteria) complete — CP2 approved (author, 2026-09-13). Merged into `main`; branch `wp2` is kept.
- WP3 (transition curve fitting) complete — CP3 approved (final approval of D-040 to D-051 by the author, 2026-09-14) and merged into `main`
  (merge commit `b47d08e`); branch `wp3` is kept.
- **WP4 (per-curve uncertainty, PROJECT_BRIEF.md §5) complete — INTERNAL REVIEW APPROVED** (author, 2026-09-15): D-052 to D-065 and D-067
  FINAL APPROVED; D-066 APPROVED AS CANDIDATE SET ONLY (the final WP6 scatter model is not chosen). The internal review was a stop the author set
  before WP5 because the WP4 uncertainty and scatter decisions affect WP6; it is not one of the official checkpoints. Merged into `main` with an
  explicit merge commit; branch `wp4` is kept.
- **WP5 (specimen size effect, PROJECT_BRIEF.md §5) complete — CP4 APPROVED** (author, 2026-09-17): D-068 to D-088 FINAL
  APPROVED (D-075 as a sensitivity set, D-085 as a chronology, D-087 as the record of results); D-089 deliberately left OPEN as a
  WP6 planning decision. Merged into `main` with an explicit merge commit; branch `wp5` is kept. The CP4 approval session changed
  documentation and status only — no code, number, generated table or generated figure moved (D-088).
- **WP6 (Monte Carlo test matrix study) is the next permitted work package.**
- **WP6 has NOT started.** No Monte Carlo simulator, no fixed-material-volume comparison, no external size-correction number
  adopted, and no WP6 scatter model chosen or calibrated.

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
- WP4 (internal WP4 review, 2026-09-15: D-052 to D-065 and D-067 FINAL APPROVED, D-066 a candidate set only; approval record at the head of the
  WP4 section of DECISIONS.md): the pairs (case) bootstrap is the PRIMARY uncertainty method (D-052); the fixed-design wild bootstrap is a
  SENSITIVITY ONLY, never promoted and never a silent replacement because it is narrower (D-053); every replicate is refitted with the approved
  WP3 method, the 2.7 J full-size shelf is never varied inside the bootstrap, and model-choice and sampling uncertainty stay separate (D-054);
  B = 2,000 per curve per method, per-replicate seeds, the B = 4,000 stability subset, 3 worker processes as an execution change only (D-055);
  nominal 95 % percentile bootstrap intervals (D-056); a reportable interval needs finite target values in >= 95 % of the replicates requested,
  never lowered, failures kept in the denominator, conditional quantiles audit only (D-057); primary / diagnostic / unavailable labels, a narrow
  diagnostic interval never upgrades a weak WP3 fit (D-058); T41J support diagnostics carried, 33-153 retained and warned, not excluded (D-059);
  synthetic validation with its full history (D-060); *empirical published-data residual scatter*, characterization only, never pure material
  scatter (D-061); sampling associations descriptive only (D-062); Marini (2020) SD comparison, nuanced (D-063); pairs against fixed design as
  diagnostic evidence (D-064); worked-example and diagnostic figures (D-065); WP6 scatter-model candidates C1-C3, not chosen (D-066); method and
  system history (D-067).
- **Interval wording and calibration caveat (D-056).** Every WP4 interval is a *nominal 95 % percentile bootstrap interval* ("95 % percentile
  bootstrap CI" where space is limited), not an interval calibrated to exactly 95 % coverage. SYNTHETIC coverage of the primary pairs intervals was
  about 89.5 % (well-sampled full-size T41J), 93 % (high-scatter full-size T41J), 97 % (weakly sampled full-size design) and 96.5 % (miniature T0).
  Generated tables and figures keep their generated labels (for example "primary bootstrap CI", or "95 % CI" in the worked-example caption) and are
  read this way; the generated status line of `outputs/wp4/wp4_summary.md` still says the internal review is awaited, and this file is the
  authoritative status (D-067 step 9).
- **The 54 unavailable pairs full-size T41J intervals stay the primary result** (author decision, 2026-09-15): no alternative reporting threshold,
  their conditional quantiles audit only; the fixed-design result (8 unavailable) is a separate sensitivity showing that fixing the test
  temperatures makes many more intervals available (D-057; DECISIONS.md WP4 approval record).
- WP5 may consume the approved WP3 fits and the WP4 uncertainty labels where relevant; it must not treat a bootstrap interval width as
  specimen-size correction uncertainty and must determine the size effect independently, from genuinely comparable specimen-size pairs.
  *Implemented as D-082: the WP4 labels are carried on every comparison for reporting only, no interval width is used as a size
  penalty, and no variance deconvolution is attempted.*
- WP6 (later): primary uncertainty and scatter basis = the pairs-bootstrap results where appropriate, with the empirical published-data residual
  profile as calibration evidence; sensitivities = the fixed-design bootstrap and scatter models C1, C2 and C3. Between-curve spread, bootstrap
  interval widths, conditional ranges, synthetic-validation outputs and the published residual scatter are never treated as pure material scatter
  without qualification.

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

## WP4 final results (internal review approved 2026-09-15; regenerate with `./run_all.sh`; summary `outputs/wp4/wp4_summary.md`)
- Methods (D-052 to D-056): PRIMARY nonparametric pairs (case) bootstrap and a fixed-design wild bootstrap SENSITIVITY (Rademacher signs, HC2
  leverage-adjusted residuals); every replicate refitted with the unchanged approved WP3 functions (full-size LSE fixed at 2.7 J, miniature LSE
  fitted); B = 2,000 per curve and method for all 170 primary curves; per-replicate seeds from 20260914; nominal 95 % percentile bootstrap
  intervals; a reportable interval needs finite target values in >= 95 % of the replicates requested (project rule); primary CI for usable
  original fits, diagnostic interval for weakly identified or boundary-limited ones (D-057, D-058).
- SYNTHETIC checks (`synthetic_bootstrap_validation.md`): zero scatter, determinism (1, 2, 3 and 8 worker processes) and failure accounting all
  pass. Coverage of the nominal 95 % percentile bootstrap intervals over 200 WP3 data sets per scenario (not exactly 95 %; D-056): pairs 89.5 %
  (T41J) well sampled, 93 % high scatter, 97 % weakly sampled, 96.5 % (T0) miniature; fixed-design 80 %, 75 %, 38.5 % and 75.5 % (anti-conservative).
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
  shelf); no product-form stratification supported; WP6 candidates C1-C3 approved as a candidate set only, not chosen.
- Worked example (D-065): curve 3-17, A533B plate, irradiated, 18 specimens: T41J 120.4 °C, pairs 95 % percentile bootstrap CI 112.0-129.7 °C,
  SD 4.4 °C.
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
- Checks of the internal-review approval (2026-09-15; documentation-only change, so no bootstrap or pipeline step was rerun): only DECISIONS.md,
  PROGRESS.md and README.md differ from `a806d93`; the other 178 tracked files, including all 41 `outputs/wp4/` files and the WP4 code, are
  byte-identical; data and every WP0–WP3 output and source file are identical to `main` (`b47d08e`); raw-data SHA-256 checksums verified; the 14
  CP2 cohort fingerprints recomputed and matching (primary 170 / 2,588); an independent scratch recomputation from the per-curve WP4 tables
  reproduced every interval count (D-067 step 9).

## Decisions WP4 inherited from WP3 (resolved in WP4; final approved at the internal WP4 review, 2026-09-15)
- Eligibility for intervals: all 170 curves bootstrapped; primary CI for usable fits, diagnostic interval otherwise (D-058).
- Resampling scheme: pairs bootstrap primary, fixed-design wild bootstrap sensitivity (D-052, D-053); the 2.7 J full-size shelf held fixed (D-054).
- T41J support warnings carried into the replicates (D-059); miniature curves: T0 and USE intervals only, LSE and C diagnostic (D-056).
- Published cross-check: Marini (2020) sigma(T41) and Eq. 6 amplitudes against the bootstrap SD (D-063).

## WP4 internal-review decisions (author, 2026-09-15)
- D-052 to D-065: FINAL APPROVED (D-053 as sensitivity only; D-056 with the terminology clarification; D-057 exactly as pre-registered; D-061 as
  characterization only). D-067: FINAL APPROVED as a chronological record, extended with step 9 (this approval session).
- D-066: APPROVED AS CANDIDATE SET ONLY; the final WP6 scatter model is NOT chosen. Planning preference only: C2 central, C1 (robust scale) a
  lower-scatter sensitivity, C3 an empirical heavy-tail sensitivity; WP6 must calibrate and test all three and report whether the headline
  full-size-versus-miniature conclusion changes across them.
- The 54 unavailable full-size T41J intervals: kept as the primary result under the unchanged 95 % rule. No alternative threshold or
  analytic-crossing sensitivity was added or run.
- The fixed-design bootstrap in WP5 and WP6: a sensitivity only, always cited with its demonstrated synthetic under-coverage (D-053, D-064).

## WP5 final results (CP4 approved 2026-09-17; regenerate with `./run_all.sh`; summary `outputs/wp5/wp5_summary.md`)
- Method, pre-registered and committed (`e160fe3`) before any residual existed: PRIMARY energy normalization = the ligament
  (nominal fracture) volume B b² of Lucas et al., NF_E = 640 mm³ / (B_s b_s²), the convention PROJECT_BRIEF.md §5 and §6.4 name
  and the descriptor writes B(W−A)² (D-073); PRIMARY temperature correction = M = 98 − 15.1 ln(B b²) °C, Sokolov & Alexander
  NUREG/CR-6379 Eq. 22 (D-074). Both depend only on the smaller specimen's own published dimensions, so no full-size answer
  enters its own correction. Transformed points are refitted with the unchanged WP3 fitter under the full-size convention
  (LSE fixed 2.7 J, D-077). ΔT_size = T41J(normalized) − T41J(measured full-size), positive = warmer = conservative (D-078).
- Matched evidence: 4,824 candidate pairs enumerated; **18 STRICT comparisons, 10 independent material-condition families,
  5 publications** (refs 53, 55, 59, 60, 107); 0 PARTIAL, 0 cross-study. **10 comparisons from 7 families** reach the
  pre-registered primary analysis set (D-079).
- Residual: family-weighted mean **−3.5 °C**, SD **11.4 °C**, MAE 9.5, range of individual comparisons −33.8 to +18.3 °C;
  over all 17 STRICT residuals, family-weighted mean −10.8 °C, SD 21.1 °C.
- **No geometry class reaches the D-079 evidence threshold**: 0 DIRECTLY SUPPORTED, 7 WEAKLY SUPPORTED, 2 UNSUPPORTED. Only
  plate (4 families, 3 publications) and unirradiated (5 families, 4 publications) meet it as strata; forging (2), weld metal
  (1) and irradiated (2) do not.
- Before/after: median |T0 difference| 66.9 → 16.2 °C, median |relative USE difference| 0.96 → 0.24, median curve-level RMS
  energy difference 0.46 → 0.26 of the full-size USE; 8 of 10 improved on T0, 9 of 10 on USE, 8 of 10 on the curve metric. The
  two that worsen are both ref 55, where the measured shift runs the wrong way.
- Sensitivity: the central bias moves from −3.5 to −23.2 °C across the four published temperature corrections while the
  family-weighted SD stays 11.1–11.9 °C; fracture-area energy scaling is far worse (mean +42.9 °C, SD 42.1 °C).
- Sokolov & Alexander's shear-weighted Eq. (11), the procedure that report actually recommends, **cannot be run**: the dataset
  has no shear-fracture column at all, for any record. Nothing is imputed (D-076).
- Checks: 12 normalization self-checks (including reproducing NUREG/CR-6379's Table 2 ratios for all four of its specimen types
  to 0.3 %) and 9 independent checks in `src/wp5_tests.py`, all passing.

- Reproducibility check of the WP5 state (branch `wp5`): `./run_all.sh` exit 0 in **10 min 18 s** (WP4's two scripts reused their
  fingerprint-verified checkpoints in the git-ignored `cache/`, 0.4 min; the last full WP4 recomputation from raw data was the
  3 h 01 min run recorded under WP4, and no WP4 code, parameter or input has changed since). Raw-data SHA-256 checksums verified
  (7 of 7); the 14 CP2 cohort fingerprints recomputed and matching (primary 170 curves / 2,588 records); the frozen-cohort check
  passed in WP2, WP3, WP4 and both WP5 scripts. **0 tracked output or processed-data files changed by the run.** Every file in
  `data/`, `outputs/wp0`–`outputs/wp4` and every WP0–WP4 source file is byte-identical to `main` (`0b5dad6`); the only tracked
  differences from `main` are `DECISIONS.md`, `PROGRESS.md`, `run_all.sh` and the new WP5 sources and outputs. An independent
  recomputation that imports no project code reproduced the cohort counts and the WP3 outcome counts (0 / 0 / 18 / 35 / 13 / 104).
- Untracked file: `AGENTS.md` (inherited from earlier work, a near-copy of `CLAUDE.md`). It was not modified, not deleted, not
  committed and not added to `.gitignore`; it is the only untracked file in the tree.

## WP5 CP4 approval decisions (author, 2026-09-17)
- D-073, D-074 FINAL APPROVED: the primary normalization stands as pre-registered — energy by the ligament-volume ratio
  (B b²)_full / (B b²)_small with b = W − a, temperature by M = 98 − 15.1 ln(B b²) °C with B b² in mm³. The caveats are kept
  verbatim: a classical geometry-based approximation; developed from specific RPV steels and geometries; **neither equation is
  exact physics**; geometry, notch and constraint effects remain; applicability outside the studied geometries is weaker. The
  primary method is not changed because a post-hoc sensitivity had a different residual.
- D-075 FINAL APPROVED AS SENSITIVITY SET. D-072 FINAL APPROVED (KLST 3 mm ligament direction primary, dataset-literal kept as
  S6, raw dataset not rewritten, all readings auditable). D-068, D-069 FINAL APPROVED (same-study primary evidence; the rule is
  not loosened to increase N; the empty cross-study class is an honest result; STRICT / PARTIAL / NOT MATCHED and the per-pair
  rejection reasons preserved). D-070 FINAL APPROVED (family = unit of independence; family-weighted summaries preferred for the
  WP6 handoff). D-079, D-080 FINAL APPROVED as pre-registered — the ≥ 3 families from ≥ 2 publications threshold was **not**
  lowered after seeing that no geometry satisfies it, and that negative evidence is part of the result.
- **WP6 CENTRAL size-correction scenario (D-083): pooled family-weighted bias −3.5 °C, SD 11.4 °C, 7 independent families,
  5 studies, status WEAKLY SUPPORTED.** Sign convention unchanged: ΔT_size = T41J(normalized smaller-specimen estimate) −
  T41J(matched full-size curve); WP6 must not silently reverse it. It is not a geometry-specific law, not pure material scatter,
  not an ASTM uncertainty and not directly supported for every geometry.
- **WP6 CONSERVATIVE sensitivity REQUIRED (D-083): the all-STRICT family-weighted mean ≈ −10.8 °C and SD ≈ 21.1 °C from 10
  independent families.** WP6 reads the exact regenerated values from the WP5 outputs, not rounded prose, and must report whether
  the headline full-size-versus-miniature conclusion changes when the central penalty is replaced by it. Neither is chosen
  because it gives a preferred answer.
- D-089 OPEN: the residual spread is stable across the pre-declared normalization methods (family-weighted SD 11.1–11.9 °C)
  while the central bias moves materially (−3.5 to −23.2 °C). WP6 planning must decide how to represent that bias sensitivity
  **without double-counting the residual SD**. Not resolved at CP4.
- Product form (D-081): plate has enough matched evidence for its own descriptive result; forging and weld metal do not, and no
  standalone forging or weld correction distribution is created. The plate-only result may be a WP6 sensitivity or diagnostic
  but must not replace the pooled central result without explicit justification.
- Irradiation (D-081): the dataset does **not** support a reliable separate irradiated size correction; none is estimated from
  two families, and it is **not** assumed that irradiation and geometry do not interact.
- Unsupported geometries (D-083): `20x5x5 a=0.76` and `23.6x5x5 a=0.78` are excluded from the central WP6 comparison. WP6 may
  omit them, or include them only in a clearly labelled EXTERNAL/LITERATURE SCENARIO after verifying the external number and its
  applicability. **No external correction number is approved**; whether such a scenario is useful is a WP6 Plan Mode decision.
- D-085 FINAL APPROVED AS CHRONOLOGY, precisely because it is transparent: the normalized upper-shelf ratios were seen during
  the feasibility and literature-review stage before D-073 and D-074 were pre-registered. History is not rewritten; the
  safeguards stand (primary formulas from the brief, the literature and applicability reasoning; alternatives fixed before any
  residual comparison; the primary method not selected by minimizing the final residual).
- D-088 records the CP4 verification: documentation-only changes, 0 of 206 tracked files under `data/`, `outputs/`, `src/` and
  `run_all.sh` altered, `src/wp5_tests.py` 9 of 9 passing, raw checksums and the 14 CP2 cohort fingerprints verified.

## What a WP6 session must read first
`PROJECT_BRIEF.md` §5 WP6, §6.2 figure 4 and §9 CP5; `DECISIONS.md` (the WP4 and WP5 sections in full, especially D-066, D-070,
D-078, D-079, D-082, D-083, D-089); this file; then `outputs/wp5/wp6_size_correction_handoff.csv`,
`outputs/wp5/size_correction_summary_overall.csv`, `outputs/wp5/wp5_summary.md`,
`outputs/wp4/published_residual_scatter_summary.csv`, `outputs/wp4/t41j_uncertainty_full_size.csv`,
`outputs/wp4/uncertainty_vs_sampling_by_curve.csv`, `outputs/wp3/fits_primary.csv` and `outputs/wp3/method_configuration.md`.

## Next permitted work package
- **WP6 (Monte Carlo test matrix study, PROJECT_BRIEF.md §5).** CP4 is approved and `wp5` is merged, so WP6 is now permitted.
  It has **NOT started**. The official checkpoint CP5 follows WP6, before the report is written.

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
