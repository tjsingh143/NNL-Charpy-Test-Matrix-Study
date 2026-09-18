# WP6 - Monte Carlo test-matrix study: results

**SYNTHETIC (Monte Carlo test-matrix study; not published measurements)**

Every number below is computed from the generated tables in `outputs/wp6/` and regenerates with `./run_all.sh`.
The method was frozen in DECISIONS.md D-090 to D-112 and committed before any cell was run; the 19 simulator
validation tests are in `validation_results.csv` and the 11 independent checks in `wp6_check_results.csv`.
Every miniature result is a **conditional fixed-volume scenario using the pooled, WEAKLY SUPPORTED WP5 correction distribution (D-083, D-092); not a geometry-specific claim**, and every specimen count is an
**idealized finished-specimen material-only accounting (D-091): gross rectangular volume L*W*B, integer floor, unused remainder discarded, notch volume not recovered; NOT a prediction of how many specimens fit in or can be machined from a real surveillance capsule**.

## 1. What was run

6188 frozen cells across tiers T1-T7. R = 1000 replicates in T1, T2, T3 and T7, 500
in T4, 400 in T5, and 200 programmes with B = 500 bootstrap replicates each in T6. Declared benchmark
before the run: projected 4.89 h (peak of the validation-plus-benchmark
process 509 MB). The MEASURED wall-clock times of the complete runs are recorded in
`PROGRESS.md` and `run_all.sh`; a wall-clock time is not a regenerable number, so it is not written here.

## 2. The headline: which spends a fixed volume better?

Over the 1512 T1 comparisons (9 archetypes x 7 miniature geometries x 6 budgets x 4 strategies):
**1038 FULL-SIZE WINS, 234 MINIATURE WINS,
240 PRACTICALLY TIED, 0 INELIGIBLE.**

**The miniature error has a floor that no specimen count can beat.** For archetype A5 and geometry G5 the
miniature RMSE stays between 11.9 and 12.6 deg C from N = 84 to N = 504,
against the predicted floor sqrt(bias^2 + SD^2) = **12.0 deg C** under the CENTRAL correction
(23.7 deg C under the CONSERVATIVE one). The size-correction residual, drawn once per programme
(D-098), does not average away. The full-size RMSE falls steadily with N. So the answer flips where the
full-size RMSE drops below that floor:

| geometry | strategy | miniature_wins_at_k | tied_at_k | full_size_wins_at_k |
| --- | --- | --- | --- | --- |
| G1 | U | 4 | 6, 8 | 12, 18, 24 |
| G1 | C | none | 4 | 6, 8, 12, 18, 24 |
| G1 | A | 4 | 6 | 8, 12, 18, 24 |
| G1 | S | 4 | 6 | 8, 12, 18, 24 |
| G2 | U | 4 | 6, 8 | 12, 18, 24 |
| G2 | C | none | 4 | 6, 8, 12, 18, 24 |
| G2 | A | 4 | 6 | 8, 12, 18, 24 |
| G2 | S | 4 | 6 | 8, 12, 18, 24 |
| G3 | U | 4 | 6, 8 | 12, 18, 24 |
| G3 | C | none | 4 | 6, 8, 12, 18, 24 |
| G3 | A | 4 | 6 | 8, 12, 18, 24 |
| G3 | S | 4 | 6 | 8, 12, 18, 24 |
| G5 | U | 4 | 6, 8 | 12, 18, 24 |
| G5 | C | none | 4 | 6, 8, 12, 18, 24 |
| G5 | A | 4 | 6 | 8, 12, 18, 24 |
| G5 | S | 4 | 6 | 8, 12, 18, 24 |
| G4 | U | 4 | 6, 8 | 12, 18, 24 |
| G4 | C | none | 4 | 6, 8, 12, 18, 24 |
| G4 | A | 4 | 6 | 8, 12, 18, 24 |
| G4 | S | 4 | 6 | 8, 12, 18, 24 |
| G6 | U | 4 | 6, 8 | 12, 18, 24 |
| G6 | C | none | 4 | 6, 8, 12, 18, 24 |
| G6 | A | 4 | 6 | 8, 12, 18, 24 |
| G6 | S | 4 | 6 | 8, 12, 18, 24 |
| G7 | U | 4 | 6, 8 | 12, 18, 24 |
| G7 | C | none | 4 | 6, 8, 12, 18, 24 |
| G7 | A | 4 | 6 | 8, 12, 18, 24 |
| G7 | S | 4 | 6 | 8, 12, 18, 24 |

Across ALL 63 (archetype x geometry) combinations, the share of comparisons won by each side:

| strategy | k_budget | FULL-SIZE WINS | MINIATURE WINS | PRACTICALLY TIED | INELIGIBLE |
| --- | --- | --- | --- | --- | --- |
| A | 4 | 0 | 1 | 0 | 0 |
| A | 6 | 0.46 | 0 | 0.54 | 0 |
| A | 8 | 0.76 | 0 | 0.24 | 0 |
| A | 12 | 1 | 0 | 0 | 0 |
| A | 18 | 1 | 0 | 0 | 0 |
| A | 24 | 1 | 0 | 0 | 0 |
| C | 4 | 0.41 | 0 | 0.59 | 0 |
| C | 6 | 0.78 | 0 | 0.22 | 0 |
| C | 8 | 0.89 | 0 | 0.11 | 0 |
| C | 12 | 1 | 0 | 0 | 0 |
| C | 18 | 1 | 0 | 0 | 0 |
| C | 24 | 1 | 0 | 0 | 0 |
| S | 4 | 0 | 1 | 0 | 0 |
| S | 6 | 0 | 0.46 | 0.54 | 0 |
| S | 8 | 0.86 | 0 | 0.14 | 0 |
| S | 12 | 0.65 | 0 | 0.35 | 0 |
| S | 18 | 1 | 0 | 0 | 0 |
| S | 24 | 1 | 0 | 0 | 0 |
| U | 4 | 0 | 1 | 0 | 0 |
| U | 6 | 0.22 | 0.25 | 0.52 | 0 |
| U | 8 | 0.56 | 0 | 0.44 | 0 |
| U | 12 | 0.89 | 0 | 0.11 | 0 |
| U | 18 | 1 | 0 | 0 | 0 |
| U | 24 | 1 | 0 | 0 | 0 |

The flip is the **same for every miniature geometry**: under the pooled correction, what decides the comparison
is the shared correction floor, not how many more specimens a geometry fits. **Miniature wins only at the
smallest budget (k = 4, i.e. four full-size specimens' worth of material), is tied around k = 6, and loses from
k = 8** (k = 12 for the wide uniform design). With the clustered design, a full-size programme is already good
enough at k = 4 that miniature never wins.

How the flip depends on the true curve (strategy U, G5):

| archetype | USE_J | C_C | miniature_wins_at_k | full_size_wins_at_k |
| --- | --- | --- | --- | --- |
| A1 | 100 | 28 | 4 | 8, 12, 18, 24 |
| A2 | 100 | 46 | 4 | 6, 8, 12, 18, 24 |
| A3 | 100 | 60 | 4 | 6, 8, 12, 18, 24 |
| A4 | 200 | 28 | 4 | 8, 12, 18, 24 |
| A5 | 200 | 46 | 4 | 12, 18, 24 |
| A6 | 200 | 60 | 4, 6 | 12, 18, 24 |
| A7 | 270 | 28 | 4 | 8, 12, 18, 24 |
| A8 | 270 | 46 | 4, 6 | 12, 18, 24 |
| A9 | 270 | 60 | 4, 6 | 18, 24 |

## 3. How uncertain may the correction be? (SD*, D-106)

| strategy | k_budget | n_mini | rmse_full_c | rmse_mini_at_sd0_c | sd_star_simulated_c | sd_star_semi_analytic_c | sd_star_label_change_c |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 4 | 84 | 30.86 | 4.46 | 31.08 | 30.54 | 27.5 |
| A | 8 | 168 | 8.88 | 4.17 | 7.77 | 7.84 | 7.5 |
| C | 4 | 84 | 11.69 | 4.29 | 10.79 | 10.87 | 7.5 |
| C | 8 | 168 | 6.71 | 4.07 | 5.33 | 5.34 | 2.5 |
| S | 4 | 84 | 30.86 | 4.81 | 30.71 | 30.48 | 27.5 |
| S | 8 | 168 | 7.49 | 4.57 | 5.94 | 5.93 | 2.5 |
| U | 4 | 84 | 18.28 | 4.84 | 17.55 | 17.63 | 17.5 |
| U | 8 | 168 | 10.61 | 4.41 | 9.72 | 9.64 | 7.5 |

SD* is the correction residual SD at which the miniature RMSE meets the full-size RMSE. The measured WP5
values are **11.43 deg C** (CENTRAL, 7 families) and **21.09 deg C**
(CONSERVATIVE, 10 families). At k = 8, SD* is 5.3-9.7 deg C depending on
the design and geometry, **below the measured 11.4 deg C**: the correction would have to be known
better than this dataset can show before the miniature programme beats 8 full-size specimens. At k = 4, SD* is
10.8-31.1 deg C. The simulated and
semi-analytic SD* agree closely, which confirms the floor arithmetic; the label-change column is the
practically meaningful crossing (the whole tie band crossed).

## 4. Physical reachability: a result that does not depend on the penalty

The coldest full-size-equivalent temperature a geometry can physically reach is -195 + M (the
coldest on-grid raw temperature plus its temperature shift). Of the 104 usable full-size WP3 fits, the number
whose 41 J transition each geometry **cannot reach under liquid-nitrogen cooling**:
G0 0, G1 22, G2 7, G3 2, G4 2, G5 2, G6 2, G7 0. At the V16 envelope sensitivity (T41J_true = -150 deg C)
**all 36 miniature comparisons are INELIGIBLE** - the miniature programmes cannot reach
their own transition - while the full-size programme can.

**The limit bites before the hard boundary.** In the 104-curve breadth check, **11 curves are INELIGIBLE
for G5**: they are the 11 coldest-transition materials (T41J from -165 to
-125 deg C). Only 2 lie beyond G5's reachable limit of -146.5 deg C; the
other 9 are reachable, but close enough to the cold limit that clipping removes the specimens
below 41 J from too many programmes (miniature availability 4% to
92%, full-size at least 99.5%). For cold-transition
materials the question is not which specimen size is more precise but whether the smaller one can be tested at
all.

## 5. Test-temperature placement and prior knowledge (Q2, Q4)

Prior-error sweep, A5, k = 12 (RMSE in deg C; INELIGIBLE = estimator available in fewer than 95 % of
programmes):

Full-size G0:

| e_prior | A | C | S | U |
| --- | --- | --- | --- | --- |
| -80 | 16.4 | 24.6 (INELIGIBLE) | 8.2 | 7.8 |
| -40 | 6.7 | 7.0 | 4.9 | 8.6 |
| -20 | 6.3 | 5.9 | 6.2 | 8.8 |
| -10 | 5.4 | 5.5 | 6.5 | 7.7 |
| 0 | 6.1 | 5.6 | 7.6 | 9.0 |
| 10 | 6.3 | 5.6 | 7.6 | 8.4 |
| 20 | 6.6 | 5.7 | 8.1 | 7.6 |
| 40 | 6.9 | 6.6 | 9.6 | 7.6 |
| 80 | 11.3 | 21.0 (INELIGIBLE) | 5.7 | 8.4 |

Miniature G5:

| e_prior | A | C | S | U |
| --- | --- | --- | --- | --- |
| -80 | 12.6 | 24.9 (INELIGIBLE) | 12.8 | 12.6 |
| -40 | 12.6 | 11.9 | 12.5 | 12.4 |
| -20 | 12.3 | 12.3 | 12.4 | 12.3 |
| -10 | 12.2 | 12.3 | 12.4 | 12.3 |
| 0 | 12.1 | 12.0 | 12.4 | 12.1 |
| 10 | 12.3 | 12.3 | 12.7 | 12.4 |
| 20 | 11.9 | 11.9 | 12.1 | 12.0 |
| 40 | 11.8 | 9.8 (INELIGIBLE) | 12.2 | 11.9 |
| 80 | 12.0 | 25.9 (INELIGIBLE) | 12.2 | 11.7 |

For full-size programmes, **the clustered design is best when the transition is known to within about
20-40 deg C and collapses at +/- 80 deg C** (it misses the transition and fails the availability gate); the
wide uniform design is robust but never the best; the model-based adaptive design recovers from a badly wrong
prior. For miniature programmes the placement barely matters, because the correction floor dominates.

**The adaptive conclusion depends on the algorithm (required staircase sensitivity, T7).** The simple up/down
staircase SS is far better than the model-based batched design S for full-size programmes, because it spends
every specimen near 41 J instead of on shelf anchors:

| geometry | k_budget | e_prior_c | SS | U | C | A | S |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G0 | 6 | 0 | 7.2 | 13.5 | 9.4 | 11.8 | 13.8 |
| G0 | 6 | -40 | 8.1 | 13.6 | 11.2 | 12 | 9.8 |
| G0 | 6 | 40 | 6.4 | 12 | 8.9 | 11.7 | 13.2 |
| G0 | 12 | 0 | 4.7 | 9 | 5.6 | 6.1 | 7.6 |
| G0 | 12 | -40 | 4.9 | 8.6 | 7 | 6.7 | 4.9 |
| G0 | 12 | 40 | 4.1 | 7.6 | 6.6 | 6.9 | 9.6 |
| G5 | 6 | 0 | 12.1 | 12.3 | 12.1 | 12.2 | 12.3 |
| G5 | 6 | -40 | 12.2 | 12.5 | 12 | 12.6 | 12.6 |
| G5 | 6 | 40 | 11.9 | 12 | 9.8 | 12 | 12.2 |
| G5 | 12 | 0 | 12.1 | 12.1 | 12 | 12.1 | 12.4 |
| G5 | 12 | -40 | 12.2 | 12.4 | 11.9 | 12.6 | 12.5 |
| G5 | 12 | 40 | 11.9 | 11.9 | 9.8 | 11.8 | 12.2 |
| G6 | 6 | 0 | 12.2 | 12.5 | 12.1 | 12.3 | 12.5 |
| G6 | 6 | -40 | 12.2 | 12.6 | 12 | 12.8 | 12.7 |
| G6 | 6 | 40 | 11.9 | 12.1 | 9.9 | 12.1 | 12.2 |
| G6 | 12 | 0 | 12.1 | 12.2 | 12 | 12.1 | 12.4 |
| G6 | 12 | -40 | 12.2 | 12.4 | 11.8 | 12.6 | 12.6 |
| G6 | 12 | 40 | 11.9 | 11.9 | 9.9 | 11.9 | 12.3 |

With the staircase, a full-size programme of 6 specimens reaches 6.4-8.1 deg C across the
three prior errors, well below the 12.0 deg C miniature floor. The staircase does not help miniature programmes (the floor dominates). At k = 4 the batched
design S performs no adaptation at all (its seed block is the whole programme), so it is exactly strategy A
there (`adaptive_update_counts.csv`).

## 6. Sensitivities

| variant | n_comparisons | median_delta_rmse_c | median_shift_vs_central_c | miniature_wins | full_size_wins | tied | ineligible | changes_conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V1 scatter C1-robust | 48 | -3.67 | -1.23 | 0 | 33 | 15 | 0 | False |
| V10 normalization S3 temperature Lucon | 48 | -3.49 | -1.29 | 0 | 34 | 14 | 0 | False |
| V11 normalization S5 temperature Wallin | 48 | -11.28 | -9.12 | 0 | 48 | 0 | 0 | False |
| V12 normalization S4 temperature Towers | 48 | -16.14 | -14 | 0 | 48 | 0 | 0 | False |
| V13 normalization S6 KLST as recorded | 48 | -2.88 | -0.52 | 2 | 30 | 16 | 0 | False |
| V14 specimen-level correction draw | 48 | 3.36 | 6.24 | 34 | 0 | 14 | 0 | True |
| V15 true LSE 6 J, analysed at 2.7 J | 48 | -3.73 | 0.19 | 6 | 30 | 12 | 0 | False |
| V16 T41J_true = -150 deg C | 36 | -4.68 | 0.15 | 0 | 0 | 0 | 36 | False |
| V17 T41J_true = 100 deg C | 36 | -4.15 | 0.45 | 0 | 30 | 6 | 0 | False |
| V18 machining allowance c = 0.5 mm | 48 | 0.55 | 2.63 | 20 | 16 | 12 | 0 | True |
| V19 machining allowance c = 1.0 mm | 48 | -0.38 | 2.85 | 18 | 16 | 14 | 0 | True |
| V2 scatter C2 | 48 | -4.59 | -1.3 | 0 | 36 | 12 | 0 | False |
| V20 energy-scale injection (optional) | 48 | -2.24 | 0.31 | 3 | 26 | 19 | 0 | False |
| V21 WP2 looser cohort | 48 | -2.71 | 0.36 | 4 | 30 | 14 | 0 | False |
| V22 WP2 stricter cohort | 48 | -3.18 | 0 | 6 | 29 | 13 | 0 | False |
| V3 scatter C3-centred | 48 | -2.99 | -0.1 | 3 | 26 | 19 | 0 | False |
| V4 scatter C3-uncentered | 48 | -2.67 | 0.58 | 4 | 28 | 16 | 0 | False |
| V5 miniature-inflated scatter | 48 | -2.73 | -0.51 | 0 | 27 | 21 | 0 | False |
| V6 correction CONSERVATIVE | 48 | -13.59 | -11.11 | 0 | 48 | 0 | 0 | False |
| V7 correction empirical 7-family | 48 | -2 | 0.84 | 5 | 24 | 19 | 0 | False |
| V8 correction empirical 10-family | 48 | -13.31 | -10.04 | 0 | 48 | 0 | 0 | False |
| V9 normalization S1 energy (Bb)^3/2 | 48 | -2.96 | -0.66 | 1 | 30 | 17 | 0 | False |

`median_delta_rmse_c` is RMSE(full-size) - RMSE(miniature); positive favours miniature. What moves the answer:

- **The size-correction assumptions dominate.** Replacing the CENTRAL correction by the CONSERVATIVE one, by
  the 10-family empirical pool, or by the Wallin or Towers temperature normalizations makes **full-size win
  every comparison**. The choice of published correlation (D-100) moves the median difference by up to
  -14.0 deg C - more than any
  scatter model.
- **The scatter model matters much less.** C1-robust, C2, C3-centred, C3-uncentered and the miniature-inflated
  profile shift the median difference by at most 1.3 deg C, and
  never reverse its sign.
- **The programme-level correction draw is decisive** (D-098): redrawing the residual per specimen (the
  labelled illustration, V14) lets it average away and reverses the conclusion. That is why WP5's
  curve-level estimand must be applied at programme level.
- **Machining allowance favours miniature in RMSE terms**, although it costs miniature more specimens: at
  c = 0.5 and 1.0 mm the full-size count at k = 6 falls from 6 to 4 and
  4, where full-size RMSE is steep in N, while
  the miniature RMSE is already at its correction floor. So the idealized accounting (D-091) is, if anything,
  **favourable to full-size**; it does not bias the headline toward the smaller specimens.
- **The WP2 cohort (does not change
  the conclusion) and the true lower shelf (does not change
  it) are secondary.** The transition LOCATION matters only through physical reachability: a warm transition
  (V17, T41J_true = +100 deg C) leaves the conclusion unchanged, while a cold one (V16, -150 deg C) makes every
  miniature programme ineligible (section 4).

## 7. Interval coverage (T6)

| geom_code | k_budget | n | n_reportable | coverage_A_own_estimand | coverage_B_true_t41j | median_width_c |
| --- | --- | --- | --- | --- | --- | --- |
| G0 | 6 | 6 | 180 | 0.961 | 0.961 | 85.66 |
| G0 | 12 | 12 | 200 | 0.925 | 0.925 | 34.61 |
| G0 | 24 | 24 | 200 | 0.895 | 0.895 | 19.82 |
| G5 | 6 | 126 | 200 | 0.915 | 0.265 | 8.882 |
| G5 | 12 | 252 | 200 | 0.965 | 0.175 | 6.265 |
| G5 | 24 | 504 | 200 | 0.935 | 0.105 | 4.429 |

**Coverage A** is of the programme's own corrected estimand conditional on its realised size correction - what
the bootstrap samples. **Coverage B** is of the true full-size T41J. For full-size programmes they coincide.
For miniature programmes the bootstrap still covers what it samples (0.9 or more) but covers the **true**
full-size T41J only 0.27, 0.18 and 0.11 of the time at N = 126, 252 and 504: **the interval narrows as N grows
while the size-correction residual does not.** A bootstrap interval on a sub-size-derived T41J describes
sampling scatter only and must not be read as the uncertainty of the full-size index. The approved WP4
bootstrap was not modified; B = 500 is a bounded WP6 experiment and WP4's production B = 2,000 is unchanged.

## 8. Robustness of the labels and of the Monte Carlo

Label-threshold robustness (the 12 variants of D-105, T1):

| availability_gate | tau_rule | is_primary_rule | MINIATURE WINS | FULL-SIZE WINS | PRACTICALLY TIED | INELIGIBLE |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9 | tau = 0 | False | 257 | 1108 | 147 | 0 |
| 0.9 | tau = 2 C | False | 234 | 1038 | 240 | 0 |
| 0.9 | tau = 5 C | False | 189 | 703 | 620 | 0 |
| 0.9 | tau = max(2 C, 5 %) | False | 234 | 1038 | 240 | 0 |
| 0.95 | tau = 0 | False | 257 | 1108 | 147 | 0 |
| 0.95 | tau = 2 C | False | 234 | 1038 | 240 | 0 |
| 0.95 | tau = 5 C | False | 189 | 703 | 620 | 0 |
| 0.95 | tau = max(2 C, 5 %) | True | 234 | 1038 | 240 | 0 |
| 0.99 | tau = 0 | False | 257 | 1108 | 147 | 0 |
| 0.99 | tau = 2 C | False | 234 | 1038 | 240 | 0 |
| 0.99 | tau = 5 C | False | 189 | 703 | 620 | 0 |
| 0.99 | tau = max(2 C, 5 %) | False | 234 | 1038 | 240 | 0 |

The availability gate (90 / 95 / 99 %) changes no T1 label. The tolerance moves comparisons between "wins" and
"tied" but never reverses a winner: full-size wins the majority under every rule.

Paired Monte Carlo SE: the batch-means SE and the paired replicate-index bootstrap SE agree within a factor 1.5
in 97% of T1 comparisons.

Monte Carlo stability (R = 1,000 against an independent R = 4,000): every label is unchanged and every RMSE moves
by less than tau (passes). The R = 4,000 values are all slightly lower (median
-0.26 deg C) because, by the declared common-random-number design, every R = 1,000 miniature cell uses
the same 1,000 correction draws: the shift is one sampling difference between two correction samples, repeated
across cells, not eleven independent ones. It is within one Monte Carlo standard error of the floor (about
0.27 deg C) and far below tau.

## 9. The breadth check: all 104 real fitted curves as truths (G5)

| strategy | k_budget | FULL-SIZE WINS | INELIGIBLE | MINIATURE WINS | PRACTICALLY TIED |
| --- | --- | --- | --- | --- | --- |
| A | 6 | 32 | 11 | 4 | 57 |
| A | 12 | 92 | 11 | 0 | 1 |
| C | 6 | 81 | 11 | 1 | 11 |
| C | 12 | 92 | 11 | 0 | 1 |
| S | 6 | 0 | 11 | 41 | 52 |
| S | 12 | 49 | 11 | 0 | 44 |
| U | 6 | 11 | 11 | 17 | 65 |
| U | 12 | 90 | 11 | 0 | 3 |

## 10. Limitations carried from the approved decisions

- The correction distribution is **WEAKLY SUPPORTED**: 7 independent matched families from 5 studies, 0 of 9
  geometries DIRECTLY SUPPORTED (D-083). No geometry-specific performance claim is made anywhere.
- The scatter pool is **empirical published-data residual scatter**, never material scatter (D-061).
- Specimen scatter is **independent conditional on the programme-level correction draw**. WP6 does not model a
  within-programme correlated laboratory or instrument systematic, so **every very-large-N miniature gain is
  conditional on that independence and is potentially optimistic** (D-096).
- An **absolute energy-resolution floor is not modelled**: a 200 J full-size material maps to a raw
  `20x1.5x1.5` curve spanning about 0.6 J in total, below anything in the dataset's own miniature fits (D-096).
- The material-volume accounting is an **idealized finished-specimen material-only** calculation, not a
  prediction of what fits in or can be machined from a real capsule (D-091).
- The dataset contains **no usable E23-type sub-size curve** (D-071), so every smaller geometry here is
  miniaturized (MCVN).
- Irradiation and geometry are **not** assumed to be non-interacting (D-081).
- The WP5 correction stays at the primary-cohort value in the WP2 cohort variants (D-110).
- **Open for the author (D-112 step 10):** the adaptive delta sequence of D-101 was implemented as EXTENDING
  beyond +/- 1.5 C_hat for blocks larger than seven specimens. No full-size result depends on this; miniature S
  programmes spread later specimens onto the shelves, with an RMSE change of at most about 0.6 deg C.
- The coldest raw test temperature is **-195 deg C**, the coldest point that is both inside the
  -196 deg C liquid-nitrogen envelope and on the 5 deg C grid (D-101).
