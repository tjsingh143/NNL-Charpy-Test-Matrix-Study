# WP6 method configuration (frozen before any headline cell)

SYNTHETIC (Monte Carlo test-matrix study; not published measurements)

Every decision below is DECISIONS.md D-090 to D-112, approved by the author in WP6 Plan Mode before
implementation began. This file is generated; it does not decide anything.

## Estimator (D-103)
The approved WP3 fitter, unchanged: `fit_curve(t, e, lse_fixed = 2.7 J)`, then `index_temperature` with the
tested-range rule applied to the ANALYSED temperatures, `index_fraction_of_rise`, `classify` and
`criterion_bracketing`. For a miniature programme the analysis frame is reached by the approved WP5 forward
normalization `normalize()` (D-073, D-074) applied to the ACTUAL raw temperature and energy. The estimator's
refusals are part of the estimator: a replicate whose 41 J crossing lies outside its own tested range has no
T41J and is counted unavailable.

## Physical temperature frame (D-101)
Raw-specimen envelope [-196, 300] deg C and a 5 deg C raw grid. Placement
order: propose T_fse_desired -> subtract M -> snap the RAW temperature -> clip the RAW temperature -> test ->
add M for analysis. **M is subtracted exactly once.** SS is the one deliberate raw-space exception.

Implementation clarification, fixed before any result: the physical floor -196 deg C is not a
multiple of the 5 deg C grid, so the coldest temperature that is both inside the envelope and on the
grid is **-195 deg C**, and that is where clipped specimens are placed. No specimen is ever tested
below the physical floor. The alternative reading (test exactly at -196 deg C, off-grid) would
differ by 1 deg C, far below every tolerance in the study (tau = 2 deg C, grid = 5 deg C).

## Geometries (D-092), and how geometry enters
| code | wp5_geometry_id | B_mm | ligament_mm | ligament_volume_mm3 | nf_energy | m_shift_c | gross_volume_mm3 | coldest_reachable_fse_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G0 | 55x10x10 a=2 (full-size) | 10 | 8 | 640 | 1 | 0 | 5500 | -195 |
| G1 | 20x1.5x1.5 a=0.33 | 1.5 | 1.17 | 2.053 | 311.7 | 87.14 | 45 | -107.9 |
| G2 | 20x2.5x2.5 a=0.38 | 2.5 | 2.12 | 11.24 | 56.96 | 61.47 | 125 | -133.5 |
| G3 | 20x3.33x3.33 a=0.51 | 3.33 | 2.82 | 26.48 | 24.17 | 48.53 | 221.8 | -146.5 |
| G5 | 23.6x3.33x3.33 a=0.51 | 3.33 | 2.82 | 26.48 | 24.17 | 48.53 | 261.7 | -146.5 |
| G4 | 27.5x3.33x3.33 a=0.6 | 3.33 | 2.73 | 24.82 | 25.79 | 49.51 | 304.9 | -145.5 |
| G6 | 27x3x4 a=1 | 3 | 3 | 27 | 23.7 | 48.23 | 324 | -146.8 |
| G7 | 23.6x5x5 a=0.76 | 5 | 4.24 | 89.89 | 7.12 | 30.07 | 590 | -164.9 |

Away from physical clipping, NF_E and M cancel and geometry acts through the specimen count; near the raw
bounds M also acts through geometry-dependent clipping, so equivalence is TESTED (validation 12A/12B), never
assumed. The coldest reachable full-size-equivalent temperature is -195 + M.

## Material budget (D-091)
idealized finished-specimen material-only accounting (D-091): gross rectangular volume L*W*B, integer floor, unused remainder discarded, notch volume not recovered; NOT a prediction of how many specimens fit in or can be machined from a real surveillance capsule

## Size correction (D-097, D-098, D-099, D-100)
Injected as a temperature-domain displacement of the simulated truth, `E_mini_true(T) = E_full_true(T + M - D)
/ NF_E`, reproducing D-078's sign exactly. **One programme-level draw**, shared by the whole test matrix.
CENTRAL -3.4941546891181936 deg C bias, 11.433714718421587 deg C SD (7 families,
5 studies, WEAKLY SUPPORTED). CONSERVATIVE -10.804718715572376 / 21.08698664047987 deg C
(10 families) - required. No truncation. Empirical family pools are resampled DIRECTLY, with no
bias added. Each published normalization is a complete scenario with its own (bias, SD); nothing is added in
quadrature.

DT_size = T41J(normalized smaller-specimen estimate) - T41J(matched full-size curve); positive = the correction places the transition warmer (D-078). Never reversed.

WEAKLY SUPPORTED pooled distribution (D-083): 7 independent matched families from 5 studies, 0 of 9 geometries DIRECTLY SUPPORTED. Not a geometry-specific law, not pure material scatter, not an ASTM uncertainty. Contains WP4 fit noise and between-study variation; no deconvolution is attempted (D-082).

## Metric and labels (D-104, D-105)
Primary metric RMSE of (T41J_hat - T41J_true); availability gate 95% of the replicates requested, the
D-057 threshold reused; secondary metric P90 |error|. tau = max(2 deg C, 5% of the
smaller RMSE); a winner also needs |delta RMSE| > 3 x the PAIRED Monte Carlo SE. The gate is
evaluated once per cell on the complete R replicates and is never re-applied inside a batch.

## Replicates and seeds (D-107)
R = 1000 (T1, T2, T3, T7), 500 (T4), 400 (T5), 200 programmes (T6). Master seed 20260918; one
independent stream per replicate per component; common random numbers keyed on (archetype, prior error,
replicate). Paired batch-means SE over exactly 20 batches, with a paired replicate-index bootstrap
(2000 resamples, no refits) as the declared cross-check.

## The frozen grid (D-108)
| tier | cells |
| --- | --- |
| T1 | 1728 |
| T2 | 864 |
| T3 | 576 |
| T4 | 1296 |
| T5 | 1664 |
| T6 | 6 |
| T7 | 54 |

Total 6188 cells.
