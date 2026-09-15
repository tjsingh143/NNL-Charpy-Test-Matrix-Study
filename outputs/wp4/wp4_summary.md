# WP4 summary: per-curve bootstrap uncertainty (q4x6v-dyt25)

Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort (170 curves, 2,588 records), final approved WP3 fits (CP3). Files named `synthetic_*` are SYNTHETIC bootstrap checks; every other file concerns the published measurements. Decisions: DECISIONS.md D-052 to D-067. **Status: WP4 complete - internal review awaiting the author; WP5 not started.**

## Headline numbers (each read from a table below)

- pairs, full-size T41J: 134 curves = 66 primary bootstrap CIs + 14 diagnostic intervals + 54 unavailable.
- pairs, full-size USE: 134 curves = 104 primary bootstrap CIs + 30 diagnostic intervals + 0 unavailable.
- pairs, miniature T0: 36 curves = 13 primary bootstrap CIs + 23 diagnostic intervals + 0 unavailable.
- pairs, miniature USE: 36 curves = 13 primary bootstrap CIs + 23 diagnostic intervals + 0 unavailable.
- wild, full-size T41J: 134 curves = 97 primary bootstrap CIs + 29 diagnostic intervals + 8 unavailable.
- wild, full-size USE: 134 curves = 104 primary bootstrap CIs + 30 diagnostic intervals + 0 unavailable.
- wild, miniature T0: 36 curves = 13 primary bootstrap CIs + 23 diagnostic intervals + 0 unavailable.
- wild, miniature USE: 36 curves = 13 primary bootstrap CIs + 23 diagnostic intervals + 0 unavailable.
- pairs, full-size T41J, usable fits with a primary CI (66): SD median 4.9 °C (10th-90th percentile 2.9-9.1 °C); 95 % width median 19.4 °C (10th-90th 11.7-35.7 °C).
- wild, full-size T41J, usable fits with a primary CI (97): SD median 4.5 °C (10th-90th percentile 2.5-8.0 °C); 95 % width median 16.5 °C (10th-90th 9.6-29.3 °C).
- pairs, miniature T0, reportable intervals (36): SD median 12.2 °C, width median 46.2 °C.
- pairs, full-size USE, reportable intervals (134): 95 % width / USE median 20.1 % (10th-90th 6.9-202.5 %).
- pairs, miniature USE, reportable intervals (36): 95 % width / USE median 30.4 % (10th-90th 5.0-476.5 %).
- wild, miniature T0, reportable intervals (36): SD median 5.8 °C, width median 20.8 °C.
- wild, full-size USE, reportable intervals (134): 95 % width / USE median 12.1 % (10th-90th 6.2-35.2 %).
- wild, miniature USE, reportable intervals (36): 95 % width / USE median 21.0 % (10th-90th 4.1-42.1 %).
- cross-check, pairs, C1: usable full-size fits with a primary T41J CI: 66 curves, median N 14, median SD 4.87 °C (Marini RCC-M sigma 3.52 °C at N = 18); median SD × sqrt(N) 20.4 against Marini's 12.38-19.58 (best estimate) and <= 23.08 (upper bound); below / within / above: 12.1 % / 34.8 % / 40.9 %; Theil-Sen slope of log SD on log N -0.32 (95 % CI -0.59 to -0.10).
- cross-check, pairs, C2: C1 with 15-25 specimens (Marini's A matrices; RCC-M 18): 23 curves, median N 18, median SD 4.43 °C (Marini RCC-M sigma 3.52 °C at N = 18); median SD × sqrt(N) 20.3 against Marini's 12.38-19.58 (best estimate) and <= 23.08 (upper bound); below / within / above: 13.0 % / 34.8 % / 30.4 %; Theil-Sen slope of log SD on log N -0.06 (95 % CI -1.05 to 1.18).
- cross-check, pairs, C3: C1 in the stricter (E185-count) cohort: 28 curves, median N 22, median SD 4.62 °C (Marini RCC-M sigma 3.52 °C at N = 18); median SD × sqrt(N) 22.0 against Marini's 12.38-19.58 (best estimate) and <= 23.08 (upper bound); below / within / above: 7.1 % / 28.6 % / 46.4 %; Theil-Sen slope of log SD on log N -0.24 (95 % CI -0.57 to 0.18).
- pairs / fixed-design SD, full-size t41j (80 curves): median 1.06, 10th-90th 0.93-1.48, pairs wider for 68.8 %.
- pairs / fixed-design SD, miniature t0 (36 curves): median 1.56, 10th-90th 1.13-4.30, pairs wider for 100.0 %.
- pairs / fixed-design SD, full-size use (134 curves): median 2.46, 10th-90th 1.01-16.03, pairs wider for 90.3 %.
- pairs / fixed-design SD, miniature use (36 curves): median 2.00, 10th-90th 1.11-18.27, pairs wider for 97.2 %.
- full-size T41J, pairs: curves with a reportable interval / curves, by measured energies below 41 J: 0: 0 / 1; 1: 0 / 11; 2: 3 / 30; 3-4: 47 / 61; 5+: 30 / 31 (unavailable intervals arise when replicates lose every specimen below 41 J and the crossing falls below their tested range).
- Monte Carlo stability (B = 4,000 independent rerun): largest change of a 2.5th/50th/97.5th percentile = 51.2 % of the B = 2,000 interval width (median over curves and targets 1.6 %); reportability changed for 0 curve-target rows.
- empirical published-data residual scatter, full-size usable fits, leverage-adjusted residual / fitted USE, SD (robust scale) by region: lower shelf (x <= -1.5) 0.036 (0.023, n = 154); lower transition (-1.5 < x <= -0.5) 0.073 (0.054, n = 339); central transition (-0.5 < x < 0.5) 0.105 (0.099, n = 511); upper transition (0.5 <= x < 1.5) 0.100 (0.085, n = 286); upper shelf (x >= 1.5) 0.062 (0.051, n = 395).

## 1. Method

| item | setting | decision |
| --- | --- | --- |
| primary resampling | nonparametric pairs (case) bootstrap, PRIMARY: each replicate draws N complete specimen records (temperature and energy together) with replacement and refits them; it also resamples which test temperatures are present | D-052 |
| fixed-design sensitivity | fixed-design wild bootstrap (Rademacher signs, HC2 leverage-adjusted residuals), SENSITIVITY: tested temperatures kept; replicate energy = approved WP3 fit + r_i / (1 - h_i)^(1/2) × (±1, probability 1/2 each); h_i from the Jacobian of the free parameters at the WP3 solution; energies below 0 J set to 0 J and counted; 1 - h_i <= 1e-08 → transformed residual 0 (counted) | D-053 |
| fit inside every replicate | exact approved WP3 functions (lse_setting, fit_curve, index_temperature, index_fraction_of_rise, classify, criterion_bracketing); full-size LSE fixed at 2.7 J (never varied); miniature LSE fitted >= 0 J; the tested-range rule uses each replicate's own temperatures | D-054 |
| replicates | B = 2000 per curve and method (published curves); Monte Carlo stability rerun of a predeclared subset with B = 4000 on an independent seed stream | D-055 |
| seeds | numpy SeedSequence([20260914, sha256(curve ID or synthetic data-set key), sha256(method name, with a suffix for the stability stream), replicate index]); results independent of worker count, chunking and order | D-055 |
| interval | 95 % percentile bootstrap interval [2.5th, 97.5th percentile] (NumPy linear interpolation) of the finite target values; also median, mean, SD, width, bias = mean - original, 16th/84th percentiles; BCa not used | D-056 |
| targets | full-size: T41J (primary), USE, T0; C diagnostic. Miniature: T0 (primary), USE; LSE and C diagnostic; no miniature index criterion | D-056 |
| target available | T41J: index status 'calculated' in that replicate; T0, C, USE, LSE: optimizer converged and fit not non-physical (inadmissible) | D-057 |
| reporting rule | interval reportable only if finite target values >= 95 % of the replicates REQUESTED (a project rule, not an ASTM requirement); conditional quantiles always stored | D-057 |
| labels | reportable + original WP3 fit usable: 'primary bootstrap CI'; reportable + original boundary-limited or weakly identified: 'diagnostic bootstrap interval'; otherwise 'interval unavailable: bootstrap-unstable (finite-target fraction below 95 %)'; the bootstrap never changes a WP3 outcome | D-058 |
| T41J support in replicates | share of replicates whose energies bracket 41 J; among finite T41J: share not bracketed and share with the index-position warning; T41J unavailable by reason | D-059 |
| SYNTHETIC validation | zero scatter, determinism, failure accounting, coverage (WP3 scenarios; 200 data sets × 500 replicates) | D-060 |
| residual scatter | WP3 point-fit residuals of all 2,588 records; normalized by fitted USE; leverage-adjusted (HC2) version; five x-regions; primary summary on usable WP3 fits; strata shown only as interpretable with >= 10 curves and >= 30 residuals | D-061 |
| sampling analysis | Spearman rank correlations and binned medians against pre-existing sampling properties | D-062 |
| published cross-check | Marini 2020 (sigma(T41) 3.52 °C at N = 18; Eq. 6 amplitudes); Miura et al. preprint Eq. 13 (magnitude, scaling); Switzner et al. 2023 (not T41J) | D-063 |
| method comparison | ratios of pairs to wild SD and width where both are reportable | D-064 |
| worked example | selection rule declared before results; pointwise band of the fitted mean curve | D-065 |

## 2. SYNTHETIC checks of the bootstrap implementation (not published data)

Zero scatter (data exactly on the approved model):

| scale | method | replicates | replicates_admissible | share_key_target_within_tolerance | max_abs_key_target_deviation_c | median_abs_key_target_deviation_c | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | pairs | 2000 | 2000 | 0.999 | 0 | 0 | True |
| full-size | wild | 2000 | 2000 | 1 | 0 | 0 | True |
| miniature | pairs | 2000 | 2000 | 0.9995 | 30.57 | 0 | True |
| miniature | wild | 2000 | 2000 | 1 | 0 | 0 | True |

Determinism:

| method | run | per_replicate_arrays_identical | summaries_identical | passed |
| --- | --- | --- | --- | --- |
| pairs | single process, one chunk (run 1) | True | True | True |
| pairs | single process, one chunk (run 2) | True | True | True |
| pairs | 3 worker processes, chunks of 97 | True | True | True |
| pairs | 2 worker processes, chunks of 333 | True | True | True |
| wild | single process, one chunk (run 1) | True | True | True |
| wild | single process, one chunk (run 2) | True | True | True |
| wild | 3 worker processes, chunks of 97 | True | True | True |
| wild | 2 worker processes, chunks of 333 | True | True | True |

Failure accounting (difficult WP3 data sets; T41J rows):

| data_set | method | replicates_requested | finite_target_values | target_unavailable | finite_target_fraction | interval_label | passed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B\|x -0.5..3, n=12 (lower shelf missing)\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | pairs | 2000 | 299 | 1701 | 0.15 | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) | True |
| B\|x -0.5..3, n=12 (lower shelf missing)\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | wild | 2000 | 711 | 1289 | 0.356 | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) | True |
| B\|shelves + 1 transition point (n=7)\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | pairs | 2000 | 1960 | 40 | 0.98 | diagnostic bootstrap interval | True |
| B\|shelves + 1 transition point (n=7)\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | wild | 2000 | 2000 | 0 | 1 | diagnostic bootstrap interval | True |
| B\|clustered cold side: x -3..-0.5, n=12\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | pairs | 2000 | 0 | 2000 | 0 | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) | True |
| B\|clustered cold side: x -3..-0.5, n=12\|full-size\|moderate\|5.0\|150.0\|0.0\|30.0 (WP3 replicate 0) | wild | 2000 | 0 | 2000 | 0 | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) | True |

Coverage of 95 % percentile intervals (SYNTHETIC; 200 data sets per WP3 scenario, 500 replicates each):

| scenario | method | target | truth | share_datasets_interval_reportable | coverage_of_reportable_intervals | coverage_monte_carlo_se | share_truth_below_interval | share_truth_above_interval | median_bootstrap_sd | empirical_sd_of_original_estimates | ratio_median_bootstrap_sd_to_empirical_sd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| well sampled | pairs | t41j | -16.62 | 100.0 % | 89.5 % | 0.015 | 4.5 % | 6.0 % | 3.506 | 3.857 | 0.909 |
| well sampled | pairs | t0 | 0 | 100.0 % | 89.5 % | 0.015 | 6.5 % | 4.0 % | 3.964 | 4.021 | 0.986 |
| well sampled | pairs | use | 150 | 100.0 % | 90.5 % | 0.015 | 6.5 % | 3.0 % | 5.91 | 5.592 | 1.057 |
| well sampled | wild | t41j | -16.62 | 100.0 % | 80.0 % | 0.015 | 11.5 % | 8.5 % | 2.765 | 3.857 | 0.717 |
| well sampled | wild | t0 | 0 | 100.0 % | 83.5 % | 0.015 | 9.0 % | 7.5 % | 3.511 | 4.021 | 0.873 |
| well sampled | wild | use | 150 | 100.0 % | 88.5 % | 0.015 | 7.0 % | 4.5 % | 5.317 | 5.592 | 0.951 |
| weakly sampled | pairs | t41j | -16.62 | 100.0 % | 97.0 % | 0.015 | 0.0 % | 3.0 % | 13.82 | 6.694 | 2.064 |
| weakly sampled | pairs | t0 | 0 | 100.0 % | 96.0 % | 0.015 | 3.5 % | 0.5 % | 22.95 | 7.382 | 3.109 |
| weakly sampled | pairs | use | 150 | 100.0 % | 86.0 % | 0.015 | 13.0 % | 1.0 % | 149.3 | 7.837 | 19.05 |
| weakly sampled | wild | t41j | -16.62 | 100.0 % | 38.5 % | 0.015 | 35.5 % | 26.0 % | 2.066 | 6.694 | 0.309 |
| weakly sampled | wild | t0 | 0 | 100.0 % | 52.0 % | 0.015 | 17.5 % | 30.5 % | 2.413 | 7.382 | 0.327 |
| weakly sampled | wild | use | 150 | 100.0 % | 70.0 % | 0.015 | 16.0 % | 14.0 % | 4.723 | 7.837 | 0.603 |
| high scatter | pairs | t41j | -16.62 | 100.0 % | 93.0 % | 0.015 | 5.5 % | 1.5 % | 7.474 | 8.019 | 0.932 |
| high scatter | pairs | t0 | 0 | 100.0 % | 93.0 % | 0.015 | 3.5 % | 3.5 % | 8.9 | 8.053 | 1.105 |
| high scatter | pairs | use | 150 | 100.0 % | 90.0 % | 0.015 | 7.0 % | 3.0 % | 16.43 | 12.06 | 1.362 |
| high scatter | wild | t41j | -16.62 | 100.0 % | 75.0 % | 0.015 | 19.5 % | 5.5 % | 5.39 | 8.019 | 0.672 |
| high scatter | wild | t0 | 0 | 100.0 % | 82.5 % | 0.015 | 7.5 % | 10.0 % | 6.742 | 8.053 | 0.837 |
| high scatter | wild | use | 150 | 100.0 % | 90.0 % | 0.015 | 5.5 % | 4.5 % | 11.02 | 12.06 | 0.914 |
| miniature, fitted lower shelf | pairs | t0 | 0 | 100.0 % | 96.5 % | 0.015 | 3.5 % | 0.0 % | 8.367 | 5.348 | 1.565 |
| miniature, fitted lower shelf | pairs | use | 8 | 100.0 % | 91.5 % | 0.015 | 4.5 % | 4.0 % | 1.503 | 0.395 | 3.808 |
| miniature, fitted lower shelf | wild | t0 | 0 | 100.0 % | 75.5 % | 0.015 | 15.5 % | 9.0 % | 4.013 | 5.348 | 0.75 |
| miniature, fitted lower shelf | wild | use | 8 | 100.0 % | 84.5 % | 0.015 | 6.5 % | 9.0 % | 0.362 | 0.395 | 0.917 |

## 3. Reproduction of the approved WP3 point fits and determinism on published curves

| item | value |
| --- | --- |
| check | WP4 refit of every primary curve reproduces outputs/wp3/fits_primary.csv |
| curves | 170 |
| max_abs_difference_lse_j | 0 |
| max_abs_difference_use_j | 0 |
| max_abs_difference_t0_c | 0 |
| max_abs_difference_c_c | 0 |
| max_abs_difference_sse | 0 |
| max_abs_difference_index_temperature_c | 0 |
| all_identical_outcome | True |
| all_identical_index_status | True |
| all_identical_flag_index_near_fitted_shelf | True |
| all_identical_flag_index_not_bracketed | True |
| passed | True |

| curve_id | n_points | method | replicates_compared | compared | identical |
| --- | --- | --- | --- | --- | --- |
| 104-none.3 | 6 | pairs | 250 | single process, one chunk vs the pooled multi-process run | True |
| 104-none.3 | 6 | wild | 250 | single process, one chunk vs the pooled multi-process run | True |
| 1-6.1 | 95 | pairs | 250 | single process, one chunk vs the pooled multi-process run | True |
| 1-6.1 | 95 | wild | 250 | single process, one chunk vs the pooled multi-process run | True |

## 4. Curve accounting: which curves received which interval

| method | geometry_category | target | original_wp3_outcome | curves | primary_bootstrap_ci | diagnostic_bootstrap_interval | interval_unavailable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | full-size | t41j | boundary-limited | 1 | 0 | 1 | 0 |
| pairs | full-size | t41j | weakly identified | 29 | 0 | 13 | 16 |
| pairs | full-size | t41j | usable fit, index temperature calculated | 104 | 66 | 0 | 38 |
| pairs | full-size | t41j | ALL | 134 | 66 | 14 | 54 |
| pairs | full-size | use | boundary-limited | 1 | 0 | 1 | 0 |
| pairs | full-size | use | weakly identified | 29 | 0 | 29 | 0 |
| pairs | full-size | use | usable fit, index temperature calculated | 104 | 104 | 0 | 0 |
| pairs | full-size | use | ALL | 134 | 104 | 30 | 0 |
| pairs | full-size | t0 | boundary-limited | 1 | 0 | 1 | 0 |
| pairs | full-size | t0 | weakly identified | 29 | 0 | 29 | 0 |
| pairs | full-size | t0 | usable fit, index temperature calculated | 104 | 104 | 0 | 0 |
| pairs | full-size | t0 | ALL | 134 | 104 | 30 | 0 |
| pairs | miniature | t0 | boundary-limited | 17 | 0 | 17 | 0 |
| pairs | miniature | t0 | weakly identified | 6 | 0 | 6 | 0 |
| pairs | miniature | t0 | usable fit, index temperature unavailable | 13 | 13 | 0 | 0 |
| pairs | miniature | t0 | ALL | 36 | 13 | 23 | 0 |
| pairs | miniature | use | boundary-limited | 17 | 0 | 17 | 0 |
| pairs | miniature | use | weakly identified | 6 | 0 | 6 | 0 |
| pairs | miniature | use | usable fit, index temperature unavailable | 13 | 13 | 0 | 0 |
| pairs | miniature | use | ALL | 36 | 13 | 23 | 0 |
| wild | full-size | t41j | boundary-limited | 1 | 0 | 1 | 0 |
| wild | full-size | t41j | weakly identified | 29 | 0 | 28 | 1 |
| wild | full-size | t41j | usable fit, index temperature calculated | 104 | 97 | 0 | 7 |
| wild | full-size | t41j | ALL | 134 | 97 | 29 | 8 |
| wild | full-size | use | boundary-limited | 1 | 0 | 1 | 0 |
| wild | full-size | use | weakly identified | 29 | 0 | 29 | 0 |
| wild | full-size | use | usable fit, index temperature calculated | 104 | 104 | 0 | 0 |
| wild | full-size | use | ALL | 134 | 104 | 30 | 0 |
| wild | full-size | t0 | boundary-limited | 1 | 0 | 1 | 0 |
| wild | full-size | t0 | weakly identified | 29 | 0 | 29 | 0 |
| wild | full-size | t0 | usable fit, index temperature calculated | 104 | 104 | 0 | 0 |
| wild | full-size | t0 | ALL | 134 | 104 | 30 | 0 |
| wild | miniature | t0 | boundary-limited | 17 | 0 | 17 | 0 |
| wild | miniature | t0 | weakly identified | 6 | 0 | 6 | 0 |
| wild | miniature | t0 | usable fit, index temperature unavailable | 13 | 13 | 0 | 0 |
| wild | miniature | t0 | ALL | 36 | 13 | 23 | 0 |
| wild | miniature | use | boundary-limited | 17 | 0 | 17 | 0 |
| wild | miniature | use | weakly identified | 6 | 0 | 6 | 0 |
| wild | miniature | use | usable fit, index temperature unavailable | 13 | 13 | 0 | 0 |
| wild | miniature | use | ALL | 36 | 13 | 23 | 0 |

## 5. Full-size T41J uncertainty

| method | group | quantity | curves_in_group | curves_without_reportable_interval | curves | minimum | p10 | p25 | median | p75 | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | all full-size curves | bootstrap SD of T41J (°C), reportable intervals | 134 | 54 | 80 | 1.2 | 2.963 | 3.753 | 4.917 | 7.474 | 9.68 | 22.37 |
| pairs | all full-size curves | 95 % interval width of T41J (°C), reportable intervals | 134 | 54 | 80 | 4.769 | 11.85 | 14.09 | 19.82 | 29.02 | 38.67 | 81.54 |
| pairs | all full-size curves | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 134 | 54 | 134 | 0.777 | 2.87 | 3.788 | 4.967 | 7.301 | 9.66 | 22.37 |
| pairs | all full-size curves | finite-T41J fraction of the 2,000 replicates | 134 | 54 | 134 | 0.444 | 0.755 | 0.897 | 0.965 | 0.994 | 1 | 1 |
| pairs | original WP3 outcome: usable fit | bootstrap SD of T41J (°C), reportable intervals | 104 | 38 | 66 | 1.2 | 2.95 | 3.624 | 4.87 | 6.84 | 9.097 | 22.37 |
| pairs | original WP3 outcome: usable fit | 95 % interval width of T41J (°C), reportable intervals | 104 | 38 | 66 | 4.769 | 11.65 | 14.06 | 19.43 | 25.13 | 35.72 | 81.54 |
| pairs | original WP3 outcome: usable fit | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 104 | 38 | 104 | 1.2 | 2.943 | 3.747 | 4.87 | 6.598 | 8.817 | 22.37 |
| pairs | original WP3 outcome: usable fit | finite-T41J fraction of the 2,000 replicates | 104 | 38 | 104 | 0.444 | 0.761 | 0.901 | 0.968 | 0.996 | 1 | 1 |
| pairs | original WP3 outcome: weakly identified | bootstrap SD of T41J (°C), reportable intervals | 29 | 16 | 13 | 2.578 | 3.348 | 3.911 | 6.302 | 8.987 | 12.89 | 17.17 |
| pairs | original WP3 outcome: weakly identified | 95 % interval width of T41J (°C), reportable intervals | 29 | 16 | 13 | 10.62 | 12.7 | 15.53 | 26.98 | 37.25 | 50.37 | 62.4 |
| pairs | original WP3 outcome: weakly identified | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 29 | 16 | 29 | 0.777 | 2.71 | 3.911 | 6.302 | 9.656 | 12.22 | 17.17 |
| pairs | original WP3 outcome: weakly identified | finite-T41J fraction of the 2,000 replicates | 29 | 16 | 29 | 0.65 | 0.705 | 0.897 | 0.926 | 0.974 | 0.991 | 0.998 |
| pairs | original WP3 outcome: boundary-limited | bootstrap SD of T41J (°C), reportable intervals | 1 | 0 | 1 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 |
| pairs | original WP3 outcome: boundary-limited | 95 % interval width of T41J (°C), reportable intervals | 1 | 0 | 1 | 27.14 | 27.14 | 27.14 | 27.14 | 27.14 | 27.14 | 27.14 |
| pairs | original WP3 outcome: boundary-limited | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 1 | 0 | 1 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 | 6.938 |
| pairs | original WP3 outcome: boundary-limited | finite-T41J fraction of the 2,000 replicates | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pairs | notch dimensions reported | bootstrap SD of T41J (°C), reportable intervals | 60 | 24 | 36 | 1.514 | 3.177 | 3.753 | 4.917 | 6.816 | 9.853 | 22.37 |
| pairs | notch dimensions reported | 95 % interval width of T41J (°C), reportable intervals | 60 | 24 | 36 | 6.121 | 12.43 | 14.49 | 18.45 | 25.93 | 37.95 | 81.54 |
| pairs | notch dimensions reported | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 60 | 24 | 60 | 1.397 | 2.944 | 3.872 | 5.078 | 7.172 | 9.843 | 22.37 |
| pairs | notch dimensions reported | finite-T41J fraction of the 2,000 replicates | 60 | 24 | 60 | 0.444 | 0.75 | 0.898 | 0.963 | 0.994 | 1 | 1 |
| pairs | exact notch dimensions unreported | bootstrap SD of T41J (°C), reportable intervals | 74 | 30 | 44 | 1.2 | 3.008 | 3.783 | 4.961 | 8.039 | 9.117 | 14.25 |
| pairs | exact notch dimensions unreported | 95 % interval width of T41J (°C), reportable intervals | 74 | 30 | 44 | 4.769 | 11.55 | 14.09 | 20.26 | 30.95 | 38.09 | 54.05 |
| pairs | exact notch dimensions unreported | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 74 | 30 | 74 | 0.777 | 2.87 | 3.669 | 4.87 | 7.477 | 9.117 | 14.25 |
| pairs | exact notch dimensions unreported | finite-T41J fraction of the 2,000 replicates | 74 | 30 | 74 | 0.584 | 0.757 | 0.894 | 0.968 | 0.989 | 1 | 1 |
| pairs | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | bootstrap SD of T41J (°C), reportable intervals | 9 | 5 | 4 | 6.938 | 7.2 | 7.592 | 8.272 | 10.84 | 14.64 | 17.17 |
| pairs | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | 95 % interval width of T41J (°C), reportable intervals | 9 | 5 | 4 | 27.14 | 27.82 | 28.83 | 29.83 | 38.3 | 52.76 | 62.4 |
| pairs | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 9 | 5 | 9 | 5.045 | 6.559 | 7.278 | 8.733 | 11.33 | 12.93 | 17.17 |
| pairs | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | finite-T41J fraction of the 2,000 replicates | 9 | 5 | 9 | 0.812 | 0.88 | 0.898 | 0.926 | 0.962 | 0.996 | 1 |
| pairs | no index-position warning | bootstrap SD of T41J (°C), reportable intervals | 125 | 49 | 76 | 1.2 | 2.95 | 3.693 | 4.87 | 7.037 | 9.405 | 22.37 |
| pairs | no index-position warning | 95 % interval width of T41J (°C), reportable intervals | 125 | 49 | 76 | 4.769 | 11.65 | 14.07 | 19.43 | 27.18 | 37.95 | 81.54 |
| pairs | no index-position warning | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 125 | 49 | 125 | 0.777 | 2.783 | 3.728 | 4.747 | 6.605 | 9.107 | 22.37 |
| pairs | no index-position warning | finite-T41J fraction of the 2,000 replicates | 125 | 49 | 125 | 0.444 | 0.728 | 0.894 | 0.965 | 0.994 | 1 | 1 |
| pairs | empirically unbracketed T41J (33-153) | bootstrap SD of T41J (°C), reportable intervals | 1 | 1 | 0 |  |  |  |  |  |  |  |
| pairs | empirically unbracketed T41J (33-153) | 95 % interval width of T41J (°C), reportable intervals | 1 | 1 | 0 |  |  |  |  |  |  |  |
| pairs | empirically unbracketed T41J (33-153) | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 1 | 1 | 1 | 2.253 | 2.253 | 2.253 | 2.253 | 2.253 | 2.253 | 2.253 |
| pairs | empirically unbracketed T41J (33-153) | finite-T41J fraction of the 2,000 replicates | 1 | 1 | 1 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 |
| wild | all full-size curves | bootstrap SD of T41J (°C), reportable intervals | 134 | 8 | 126 | 0.768 | 2.539 | 3.345 | 4.537 | 6.213 | 8.687 | 18.75 |
| wild | all full-size curves | 95 % interval width of T41J (°C), reportable intervals | 134 | 8 | 126 | 2.783 | 9.828 | 12.4 | 17.13 | 23.32 | 30.65 | 67.72 |
| wild | all full-size curves | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 134 | 8 | 134 | 0.768 | 2.603 | 3.475 | 4.553 | 6.279 | 8.812 | 18.75 |
| wild | all full-size curves | finite-T41J fraction of the 2,000 replicates | 134 | 8 | 134 | 0.694 | 0.998 | 1 | 1 | 1 | 1 | 1 |
| wild | original WP3 outcome: usable fit | bootstrap SD of T41J (°C), reportable intervals | 104 | 7 | 97 | 0.768 | 2.496 | 3.304 | 4.466 | 6.013 | 7.965 | 18.75 |
| wild | original WP3 outcome: usable fit | 95 % interval width of T41J (°C), reportable intervals | 104 | 7 | 97 | 2.783 | 9.563 | 12.57 | 16.51 | 21.05 | 29.27 | 67.72 |
| wild | original WP3 outcome: usable fit | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 104 | 7 | 104 | 0.768 | 2.625 | 3.446 | 4.497 | 6.027 | 8.401 | 18.75 |
| wild | original WP3 outcome: usable fit | finite-T41J fraction of the 2,000 replicates | 104 | 7 | 104 | 0.694 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | original WP3 outcome: weakly identified | bootstrap SD of T41J (°C), reportable intervals | 29 | 1 | 28 | 0.79 | 2.587 | 3.387 | 5.322 | 7.975 | 12.27 | 16.68 |
| wild | original WP3 outcome: weakly identified | 95 % interval width of T41J (°C), reportable intervals | 29 | 1 | 28 | 2.959 | 9.952 | 12.15 | 19.55 | 29.08 | 46.65 | 60.66 |
| wild | original WP3 outcome: weakly identified | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 29 | 1 | 29 | 0.79 | 2.601 | 3.469 | 5.676 | 7.968 | 12.26 | 16.68 |
| wild | original WP3 outcome: weakly identified | finite-T41J fraction of the 2,000 replicates | 29 | 1 | 29 | 0.89 | 0.994 | 1 | 1 | 1 | 1 | 1 |
| wild | original WP3 outcome: boundary-limited | bootstrap SD of T41J (°C), reportable intervals | 1 | 0 | 1 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 |
| wild | original WP3 outcome: boundary-limited | 95 % interval width of T41J (°C), reportable intervals | 1 | 0 | 1 | 23.26 | 23.26 | 23.26 | 23.26 | 23.26 | 23.26 | 23.26 |
| wild | original WP3 outcome: boundary-limited | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 1 | 0 | 1 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 | 6.078 |
| wild | original WP3 outcome: boundary-limited | finite-T41J fraction of the 2,000 replicates | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | notch dimensions reported | bootstrap SD of T41J (°C), reportable intervals | 60 | 3 | 57 | 0.768 | 2.439 | 3.304 | 4.73 | 6.292 | 8.968 | 18.75 |
| wild | notch dimensions reported | 95 % interval width of T41J (°C), reportable intervals | 60 | 3 | 57 | 2.783 | 9.192 | 12.81 | 17.62 | 24.55 | 32.71 | 67.72 |
| wild | notch dimensions reported | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 60 | 3 | 60 | 0.768 | 2.554 | 3.604 | 4.671 | 6.397 | 8.665 | 18.75 |
| wild | notch dimensions reported | finite-T41J fraction of the 2,000 replicates | 60 | 3 | 60 | 0.694 | 0.996 | 1 | 1 | 1 | 1 | 1 |
| wild | exact notch dimensions unreported | bootstrap SD of T41J (°C), reportable intervals | 74 | 5 | 69 | 0.79 | 2.601 | 3.469 | 4.074 | 6.128 | 8.178 | 13.8 |
| wild | exact notch dimensions unreported | 95 % interval width of T41J (°C), reportable intervals | 74 | 5 | 69 | 2.959 | 9.859 | 12.23 | 15.63 | 22.44 | 29.53 | 51.44 |
| wild | exact notch dimensions unreported | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 74 | 5 | 74 | 0.79 | 2.649 | 3.475 | 4.42 | 6.129 | 8.812 | 13.8 |
| wild | exact notch dimensions unreported | finite-T41J fraction of the 2,000 replicates | 74 | 5 | 74 | 0.766 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | bootstrap SD of T41J (°C), reportable intervals | 9 | 1 | 8 | 5.97 | 6.045 | 7.157 | 7.635 | 10.27 | 12.79 | 13.8 |
| wild | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | 95 % interval width of T41J (°C), reportable intervals | 9 | 1 | 8 | 20.99 | 22.58 | 27.29 | 29.06 | 36.29 | 47.49 | 51.44 |
| wild | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 9 | 1 | 9 | 5.97 | 6.056 | 7.289 | 7.596 | 9.575 | 12.65 | 13.8 |
| wild | index-position warning (41 J outside 11.9-88.1 % of the fitted rise) | finite-T41J fraction of the 2,000 replicates | 9 | 1 | 9 | 0.89 | 0.976 | 0.998 | 1 | 1 | 1 | 1 |
| wild | no index-position warning | bootstrap SD of T41J (°C), reportable intervals | 125 | 7 | 118 | 0.768 | 2.446 | 3.221 | 4.401 | 6.054 | 8.026 | 18.75 |
| wild | no index-position warning | 95 % interval width of T41J (°C), reportable intervals | 125 | 7 | 118 | 2.783 | 9.626 | 12.2 | 16.26 | 21.95 | 29.61 | 67.72 |
| wild | no index-position warning | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 125 | 7 | 125 | 0.768 | 2.528 | 3.271 | 4.464 | 6.068 | 8.355 | 18.75 |
| wild | no index-position warning | finite-T41J fraction of the 2,000 replicates | 125 | 7 | 125 | 0.694 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | empirically unbracketed T41J (33-153) | bootstrap SD of T41J (°C), reportable intervals | 1 | 1 | 0 |  |  |  |  |  |  |  |
| wild | empirically unbracketed T41J (33-153) | 95 % interval width of T41J (°C), reportable intervals | 1 | 1 | 0 |  |  |  |  |  |  |  |
| wild | empirically unbracketed T41J (33-153) | bootstrap SD of T41J (°C), all curves (conditional on finite values) | 1 | 1 | 1 | 3.933 | 3.933 | 3.933 | 3.933 | 3.933 | 3.933 | 3.933 |
| wild | empirically unbracketed T41J (33-153) | finite-T41J fraction of the 2,000 replicates | 1 | 1 | 1 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 | 0.76 |

## 6. Miniature T0 and USE uncertainty (no miniature index criterion)

| method | target | group | quantity | curves_in_group | curves_reportable | curves | minimum | p10 | p25 | median | p75 | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | t0 | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 2.284 | 3.86 | 6.179 | 12.24 | 23.57 | 50.96 | 62.26 |
| pairs | t0 | all miniature curves | 95 % width (°C), reportable intervals | 36 | 36 | 36 | 8.339 | 15.17 | 20.97 | 46.19 | 95.71 | 231.7 | 260.8 |
| pairs | t0 | all miniature curves | finite-target fraction | 36 | 36 | 36 | 0.982 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| pairs | t0 | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 2.284 | 3.596 | 5.456 | 16.13 | 35.52 | 57.38 | 62.26 |
| pairs | t0 | original WP3 fit usable | 95 % width (°C), reportable intervals | 13 | 13 | 13 | 8.339 | 14.81 | 20.13 | 68.71 | 172.3 | 255.9 | 260.8 |
| pairs | t0 | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 0.995 | 0.9996 | 1 | 1 | 1 | 1 | 1 |
| pairs | t0 | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 2.83 | 4.575 | 6.291 | 9.216 | 15.49 | 19.11 | 23.06 |
| pairs | t0 | original boundary-limited | 95 % width (°C), reportable intervals | 17 | 17 | 17 | 10.28 | 14.79 | 20.89 | 34.67 | 56.99 | 83.41 | 91.71 |
| pairs | t0 | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 0.9985 | 0.9991 | 1 | 1 | 1 | 1 | 1 |
| pairs | t0 | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 7.164 | 9.705 | 14.77 | 23.72 | 45.34 | 53.93 | 55.77 |
| pairs | t0 | original weakly identified | 95 % width (°C), reportable intervals | 6 | 6 | 6 | 25.69 | 36.18 | 53.34 | 90.54 | 186.5 | 235.9 | 259.2 |
| pairs | t0 | original weakly identified | finite-target fraction | 6 | 6 | 6 | 0.982 | 0.991 | 1 | 1 | 1 | 1 | 1 |
| pairs | use | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 0.0235 | 0.1107 | 0.1833 | 0.9268 | 4.193 | 11.94 | 27.93 |
| pairs | use | all miniature curves | 95 % width / USE, reportable intervals | 36 | 36 | 36 | 0.0124 | 0.0501 | 0.1155 | 0.3041 | 0.696 | 4.764 | 9.867 |
| pairs | use | all miniature curves | finite-target fraction | 36 | 36 | 36 | 0.982 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| pairs | use | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 0.0281 | 0.0712 | 0.3818 | 3.474 | 9.948 | 26.32 | 27.93 |
| pairs | use | original WP3 fit usable | 95 % width / USE, reportable intervals | 13 | 13 | 13 | 0.0124 | 0.0347 | 0.0399 | 0.8583 | 3.909 | 9.796 | 9.867 |
| pairs | use | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 0.995 | 0.9996 | 1 | 1 | 1 | 1 | 1 |
| pairs | use | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 0.0235 | 0.1496 | 0.166 | 0.5536 | 1.342 | 6.889 | 13.72 |
| pairs | use | original boundary-limited | 95 % width / USE, reportable intervals | 17 | 17 | 17 | 0.0762 | 0.08 | 0.1184 | 0.1792 | 0.4511 | 0.5028 | 0.6419 |
| pairs | use | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 0.9985 | 0.9991 | 1 | 1 | 1 | 1 | 1 |
| pairs | use | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 0.1446 | 0.3016 | 0.4708 | 1.096 | 2.811 | 4.527 | 5.867 |
| pairs | use | original weakly identified | 95 % width / USE, reportable intervals | 6 | 6 | 6 | 0.0603 | 0.1392 | 0.2801 | 0.497 | 2.58 | 4.442 | 5.62 |
| pairs | use | original weakly identified | finite-target fraction | 6 | 6 | 6 | 0.982 | 0.991 | 1 | 1 | 1 | 1 | 1 |
| pairs | lse | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 0.1219 | 0.1902 | 0.269 | 0.58 | 0.9216 | 1.439 | 2.212 |
| pairs | lse | all miniature curves | 95 % width (J), reportable intervals | 36 | 36 | 36 | 0.4934 | 0.6177 | 0.895 | 2.027 | 3.615 | 4.647 | 8.381 |
| pairs | lse | all miniature curves | finite-target fraction | 36 | 36 | 36 | 0.982 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| pairs | lse | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 0.1494 | 0.1873 | 0.3367 | 0.5903 | 0.9064 | 1.073 | 2.212 |
| pairs | lse | original WP3 fit usable | 95 % width (J), reportable intervals | 13 | 13 | 13 | 0.6009 | 0.7712 | 1.333 | 2.053 | 3.409 | 4.08 | 8.381 |
| pairs | lse | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 0.995 | 0.9996 | 1 | 1 | 1 | 1 | 1 |
| pairs | lse | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 0.1219 | 0.1995 | 0.2307 | 0.5697 | 0.9548 | 1.409 | 2.088 |
| pairs | lse | original boundary-limited | 95 % width (J), reportable intervals | 17 | 17 | 17 | 0.5317 | 0.6115 | 0.7365 | 1.775 | 3.677 | 4.503 | 8.039 |
| pairs | lse | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 0.9985 | 0.9991 | 1 | 1 | 1 | 1 | 1 |
| pairs | lse | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 0.1823 | 0.2088 | 0.2671 | 0.5325 | 0.8586 | 1.35 | 1.789 |
| pairs | lse | original weakly identified | 95 % width (J), reportable intervals | 6 | 6 | 6 | 0.4934 | 0.7053 | 1.108 | 2.056 | 3.303 | 5.251 | 6.907 |
| pairs | lse | original weakly identified | finite-target fraction | 6 | 6 | 6 | 0.982 | 0.991 | 1 | 1 | 1 | 1 | 1 |
| pairs | c | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 2.779 | 7.5 | 9.407 | 13.32 | 22.66 | 42.04 | 46.35 |
| pairs | c | all miniature curves | 95 % width (°C), reportable intervals | 36 | 36 | 36 | 8.513 | 27.88 | 31.96 | 52.35 | 93.53 | 162.1 | 182.9 |
| pairs | c | all miniature curves | finite-target fraction | 36 | 36 | 36 | 0.982 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| pairs | c | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 3.071 | 6.834 | 8.933 | 13.64 | 39.06 | 44.73 | 46.35 |
| pairs | c | original WP3 fit usable | 95 % width (°C), reportable intervals | 13 | 13 | 13 | 11.85 | 24.67 | 32.96 | 53.41 | 157.8 | 162.6 | 169.5 |
| pairs | c | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 0.995 | 0.9996 | 1 | 1 | 1 | 1 | 1 |
| pairs | c | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 2.779 | 7.517 | 8.85 | 10.97 | 14.32 | 21.01 | 21.53 |
| pairs | c | original boundary-limited | 95 % width (°C), reportable intervals | 17 | 17 | 17 | 8.513 | 28.32 | 30.47 | 39.79 | 57.76 | 79.07 | 84.18 |
| pairs | c | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 0.9985 | 0.9991 | 1 | 1 | 1 | 1 | 1 |
| pairs | c | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 10.58 | 11.79 | 15.3 | 26.01 | 39.83 | 43.29 | 43.4 |
| pairs | c | original weakly identified | 95 % width (°C), reportable intervals | 6 | 6 | 6 | 32.99 | 42.61 | 65.1 | 108.7 | 158.7 | 178.3 | 182.9 |
| pairs | c | original weakly identified | finite-target fraction | 6 | 6 | 6 | 0.982 | 0.991 | 1 | 1 | 1 | 1 | 1 |
| wild | t0 | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 0.6368 | 2.254 | 3.792 | 5.812 | 11.47 | 15.9 | 31.31 |
| wild | t0 | all miniature curves | 95 % width (°C), reportable intervals | 36 | 36 | 36 | 2.684 | 7.631 | 13.24 | 20.81 | 41.8 | 58.45 | 121.8 |
| wild | t0 | all miniature curves | finite-target fraction | 36 | 36 | 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | t0 | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 1.688 | 2.013 | 4.167 | 6.537 | 14.98 | 16.67 | 31.31 |
| wild | t0 | original WP3 fit usable | 95 % width (°C), reportable intervals | 13 | 13 | 13 | 6.731 | 7.484 | 15.8 | 21.89 | 57.14 | 64.73 | 121.8 |
| wild | t0 | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | t0 | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 0.6368 | 2.284 | 3.864 | 5.304 | 9.934 | 10.77 | 16.27 |
| wild | t0 | original boundary-limited | 95 % width (°C), reportable intervals | 17 | 17 | 17 | 2.684 | 7.529 | 13.06 | 20.07 | 37.13 | 41.16 | 58.33 |
| wild | t0 | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | t0 | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 3.565 | 3.572 | 3.998 | 9.771 | 14.84 | 18.08 | 21.14 |
| wild | t0 | original weakly identified | 95 % width (°C), reportable intervals | 6 | 6 | 6 | 11.32 | 12.31 | 14.85 | 35.77 | 56.39 | 70.8 | 83.75 |
| wild | t0 | original weakly identified | finite-target fraction | 6 | 6 | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | use | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 0.0197 | 0.0385 | 0.1271 | 0.29 | 0.9155 | 1.873 | 5.898 |
| wild | use | all miniature curves | 95 % width / USE, reportable intervals | 36 | 36 | 36 | 0.0109 | 0.0414 | 0.1054 | 0.2104 | 0.3811 | 0.4214 | 1.165 |
| wild | use | all miniature curves | finite-target fraction | 36 | 36 | 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | use | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 0.0221 | 0.0425 | 0.0581 | 0.3467 | 1.395 | 1.778 | 3.852 |
| wild | use | original WP3 fit usable | 95 % width / USE, reportable intervals | 13 | 13 | 13 | 0.0109 | 0.0192 | 0.0304 | 0.2731 | 0.3855 | 0.4263 | 1.165 |
| wild | use | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | use | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 0.0197 | 0.0395 | 0.1305 | 0.2051 | 0.9121 | 2.927 | 5.898 |
| wild | use | original boundary-limited | 95 % width / USE, reportable intervals | 17 | 17 | 17 | 0.0524 | 0.0762 | 0.1123 | 0.1438 | 0.3197 | 0.3954 | 0.6056 |
| wild | use | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | use | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 0.0373 | 0.0905 | 0.1779 | 0.29 | 0.5944 | 0.7043 | 0.7161 |
| wild | use | original weakly identified | 95 % width / USE, reportable intervals | 6 | 6 | 6 | 0.063 | 0.0903 | 0.12 | 0.1902 | 0.3592 | 0.4558 | 0.517 |
| wild | use | original weakly identified | finite-target fraction | 6 | 6 | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | lse | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 0.0443 | 0.0685 | 0.1636 | 0.3797 | 0.8139 | 1.128 | 1.883 |
| wild | lse | all miniature curves | 95 % width (J), reportable intervals | 36 | 36 | 36 | 0.1053 | 0.2165 | 0.5158 | 1.331 | 2.087 | 3.567 | 6.69 |
| wild | lse | all miniature curves | finite-target fraction | 36 | 36 | 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | lse | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 0.0647 | 0.1228 | 0.2339 | 0.3444 | 0.4838 | 0.9533 | 1.299 |
| wild | lse | original WP3 fit usable | 95 % width (J), reportable intervals | 13 | 13 | 13 | 0.2393 | 0.4609 | 0.7729 | 1.301 | 1.988 | 2.905 | 5.647 |
| wild | lse | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | lse | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 0.0554 | 0.0658 | 0.159 | 0.4185 | 0.9596 | 1.405 | 1.883 |
| wild | lse | original boundary-limited | 95 % width (J), reportable intervals | 17 | 17 | 17 | 0.1731 | 0.1895 | 0.523 | 1.361 | 2.775 | 4.666 | 6.69 |
| wild | lse | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | lse | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 0.0443 | 0.0985 | 0.1558 | 0.3579 | 0.8166 | 0.9337 | 0.9622 |
| wild | lse | original weakly identified | 95 % width (J), reportable intervals | 6 | 6 | 6 | 0.1053 | 0.2889 | 0.4779 | 1.109 | 1.95 | 2.148 | 2.272 |
| wild | lse | original weakly identified | finite-target fraction | 6 | 6 | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | c | all miniature curves | bootstrap SD, reportable intervals | 36 | 36 | 36 | 1.261 | 4.784 | 6.468 | 11.23 | 20.74 | 31.01 | 43.24 |
| wild | c | all miniature curves | 95 % width (°C), reportable intervals | 36 | 36 | 36 | 4.856 | 15.8 | 24.19 | 36.42 | 78.81 | 123.7 | 164.1 |
| wild | c | all miniature curves | finite-target fraction | 36 | 36 | 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | c | original WP3 fit usable | bootstrap SD, reportable intervals | 13 | 13 | 13 | 2.587 | 4.588 | 6.537 | 12.28 | 29.76 | 35.02 | 43.24 |
| wild | c | original WP3 fit usable | 95 % width (°C), reportable intervals | 13 | 13 | 13 | 9.585 | 17.96 | 25.39 | 43 | 123.5 | 126.5 | 164.1 |
| wild | c | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | c | original boundary-limited | bootstrap SD, reportable intervals | 17 | 17 | 17 | 1.261 | 5.166 | 7.242 | 10.29 | 15.25 | 19.22 | 21.93 |
| wild | c | original boundary-limited | 95 % width (°C), reportable intervals | 17 | 17 | 17 | 4.856 | 16.88 | 24.85 | 35.28 | 60.99 | 74.61 | 84.41 |
| wild | c | original boundary-limited | finite-target fraction | 17 | 17 | 17 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | c | original weakly identified | bootstrap SD, reportable intervals | 6 | 6 | 6 | 4.543 | 5.365 | 6.822 | 17.57 | 30.18 | 32.67 | 33.91 |
| wild | c | original weakly identified | 95 % width (°C), reportable intervals | 6 | 6 | 6 | 13.96 | 18.09 | 25.11 | 60.71 | 111.5 | 122 | 124.5 |
| wild | c | original weakly identified | finite-target fraction | 6 | 6 | 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## 7. USE uncertainty (both geometries)

| method | geometry_category | group | quantity | curves_in_group | curves_reportable | curves | minimum | p10 | p25 | median | p75 | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | full-size | all | relative 95 % width (width / USE), reportable | 134 | 134 | 134 | 0.0142 | 0.0691 | 0.1131 | 0.2009 | 0.4684 | 2.025 | 9.034 |
| pairs | full-size | all | relative SD (SD / USE), reportable | 134 | 134 | 134 | 0.0036 | 0.0251 | 0.0431 | 0.1182 | 0.3582 | 0.9947 | 2.687 |
| pairs | full-size | all | finite-target fraction | 134 | 134 | 134 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pairs | full-size | original WP3 fit usable | relative 95 % width (width / USE), reportable | 104 | 104 | 104 | 0.0142 | 0.0656 | 0.1012 | 0.1564 | 0.2935 | 0.5694 | 8.132 |
| pairs | full-size | original WP3 fit usable | relative SD (SD / USE), reportable | 104 | 104 | 104 | 0.0036 | 0.0224 | 0.0364 | 0.0873 | 0.2322 | 0.4651 | 1.653 |
| pairs | full-size | original WP3 fit usable | finite-target fraction | 104 | 104 | 104 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pairs | full-size | original not usable | relative 95 % width (width / USE), reportable | 30 | 30 | 30 | 0.1036 | 0.2086 | 0.4338 | 0.6575 | 2.936 | 6.144 | 9.034 |
| pairs | full-size | original not usable | relative SD (SD / USE), reportable | 30 | 30 | 30 | 0.0354 | 0.0666 | 0.1817 | 0.4502 | 1.078 | 1.357 | 2.687 |
| pairs | full-size | original not usable | finite-target fraction | 30 | 30 | 30 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pairs | miniature | all | relative 95 % width (width / USE), reportable | 36 | 36 | 36 | 0.0124 | 0.0501 | 0.1155 | 0.3041 | 0.696 | 4.764 | 9.867 |
| pairs | miniature | all | relative SD (SD / USE), reportable | 36 | 36 | 36 | 0.0035 | 0.0185 | 0.039 | 0.1341 | 0.5537 | 1.611 | 2.353 |
| pairs | miniature | all | finite-target fraction | 36 | 36 | 36 | 0.982 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| pairs | miniature | original WP3 fit usable | relative 95 % width (width / USE), reportable | 13 | 13 | 13 | 0.0124 | 0.0347 | 0.0399 | 0.8583 | 3.909 | 9.796 | 9.867 |
| pairs | miniature | original WP3 fit usable | relative SD (SD / USE), reportable | 13 | 13 | 13 | 0.0035 | 0.009 | 0.0474 | 0.4365 | 1.511 | 2.183 | 2.353 |
| pairs | miniature | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 0.995 | 0.9996 | 1 | 1 | 1 | 1 | 1 |
| pairs | miniature | original not usable | relative 95 % width (width / USE), reportable | 23 | 23 | 23 | 0.0603 | 0.0778 | 0.1307 | 0.2537 | 0.4956 | 0.6191 | 5.62 |
| pairs | miniature | original not usable | relative SD (SD / USE), reportable | 23 | 23 | 23 | 0.0174 | 0.0209 | 0.0387 | 0.111 | 0.3045 | 0.6395 | 1.711 |
| pairs | miniature | original not usable | finite-target fraction | 23 | 23 | 23 | 0.982 | 0.9987 | 1 | 1 | 1 | 1 | 1 |
| wild | full-size | all | relative 95 % width (width / USE), reportable | 134 | 134 | 134 | 0.0131 | 0.0619 | 0.0873 | 0.1207 | 0.216 | 0.3516 | 4.394 |
| wild | full-size | all | relative SD (SD / USE), reportable | 134 | 134 | 134 | 0.0035 | 0.0165 | 0.0238 | 0.0325 | 0.0601 | 0.1035 | 1.046 |
| wild | full-size | all | finite-target fraction | 134 | 134 | 134 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | full-size | original WP3 fit usable | relative 95 % width (width / USE), reportable | 104 | 104 | 104 | 0.0131 | 0.0583 | 0.0847 | 0.1044 | 0.1566 | 0.2386 | 0.4276 |
| wild | full-size | original WP3 fit usable | relative SD (SD / USE), reportable | 104 | 104 | 104 | 0.0035 | 0.0152 | 0.0229 | 0.0287 | 0.0452 | 0.0654 | 0.1131 |
| wild | full-size | original WP3 fit usable | finite-target fraction | 104 | 104 | 104 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | full-size | original not usable | relative 95 % width (width / USE), reportable | 30 | 30 | 30 | 0.0614 | 0.0842 | 0.1741 | 0.2529 | 0.4207 | 0.8867 | 4.394 |
| wild | full-size | original not usable | relative SD (SD / USE), reportable | 30 | 30 | 30 | 0.0164 | 0.0234 | 0.0517 | 0.0752 | 0.1142 | 0.2638 | 1.046 |
| wild | full-size | original not usable | finite-target fraction | 30 | 30 | 30 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | miniature | all | relative 95 % width (width / USE), reportable | 36 | 36 | 36 | 0.0109 | 0.0414 | 0.1054 | 0.2104 | 0.3811 | 0.4214 | 1.165 |
| wild | miniature | all | relative SD (SD / USE), reportable | 36 | 36 | 36 | 0.0028 | 0.011 | 0.0277 | 0.0547 | 0.1012 | 0.1246 | 0.5554 |
| wild | miniature | all | finite-target fraction | 36 | 36 | 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | miniature | original WP3 fit usable | relative 95 % width (width / USE), reportable | 13 | 13 | 13 | 0.0109 | 0.0192 | 0.0304 | 0.2731 | 0.3855 | 0.4263 | 1.165 |
| wild | miniature | original WP3 fit usable | relative SD (SD / USE), reportable | 13 | 13 | 13 | 0.0028 | 0.005 | 0.0078 | 0.066 | 0.1091 | 0.126 | 0.5554 |
| wild | miniature | original WP3 fit usable | finite-target fraction | 13 | 13 | 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | miniature | original not usable | relative 95 % width (width / USE), reportable | 23 | 23 | 23 | 0.0524 | 0.0751 | 0.1139 | 0.1438 | 0.3497 | 0.4038 | 0.6056 |
| wild | miniature | original not usable | relative SD (SD / USE), reportable | 23 | 23 | 23 | 0.0141 | 0.0194 | 0.0293 | 0.0432 | 0.0962 | 0.1059 | 0.1706 |
| wild | miniature | original not usable | finite-target fraction | 23 | 23 | 23 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## 8. T41J support diagnostics in the bootstrap replicates

| method | group | quantity | curves | minimum | p10 | p25 | median | p75 | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | all full-size curves | share_replicate_energies_bracket_41j | 134 | 0 | 0.8751 | 0.8968 | 0.9735 | 0.9948 | 1 | 1 |
| pairs | all full-size curves | share_of_finite_t41j_not_bracketed | 134 | 0 | 0 | 0 | 0 | 0.0045 | 0.0214 | 1 |
| pairs | all full-size curves | share_of_finite_t41j_with_index_position_warning | 134 | 0 | 0 | 0 | 0.0015 | 0.0157 | 0.0749 | 0.9994 |
| pairs | all full-size curves | share_t41j_unsupported_below_lowest_temperature | 134 | 0 | 0 | 0.0055 | 0.0353 | 0.1028 | 0.2454 | 0.556 |
| pairs | all full-size curves | t41j_finite_fraction | 134 | 0.444 | 0.7546 | 0.8972 | 0.9648 | 0.9938 | 0.9998 | 1 |
| pairs | original T41J bracketed | share_replicate_energies_bracket_41j | 133 | 0.6195 | 0.8766 | 0.899 | 0.9735 | 0.995 | 1 | 1 |
| pairs | original T41J bracketed | share_of_finite_t41j_not_bracketed | 133 | 0 | 0 | 0 | 0 | 0.0045 | 0.0212 | 0.274 |
| pairs | original T41J bracketed | share_of_finite_t41j_with_index_position_warning | 133 | 0 | 0 | 0 | 0.0015 | 0.016 | 0.0754 | 0.9994 |
| pairs | original T41J bracketed | share_t41j_unsupported_below_lowest_temperature | 133 | 0 | 0 | 0.0055 | 0.035 | 0.102 | 0.2434 | 0.416 |
| pairs | original T41J bracketed | t41j_finite_fraction | 133 | 0.584 | 0.7566 | 0.898 | 0.965 | 0.9945 | 0.9999 | 1 |
| pairs | original T41J not bracketed (33-153) | share_replicate_energies_bracket_41j | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pairs | original T41J not bracketed (33-153) | share_of_finite_t41j_not_bracketed | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| pairs | original T41J not bracketed (33-153) | share_of_finite_t41j_with_index_position_warning | 1 | 0.0068 | 0.0068 | 0.0068 | 0.0068 | 0.0068 | 0.0068 | 0.0068 |
| pairs | original T41J not bracketed (33-153) | share_t41j_unsupported_below_lowest_temperature | 1 | 0.556 | 0.556 | 0.556 | 0.556 | 0.556 | 0.556 | 0.556 |
| pairs | original T41J not bracketed (33-153) | t41j_finite_fraction | 1 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 | 0.444 |
| pairs | original index-position warning | share_replicate_energies_bracket_41j | 9 | 0.8875 | 0.8935 | 0.9615 | 0.9815 | 0.9965 | 0.9984 | 1 |
| pairs | original index-position warning | share_of_finite_t41j_not_bracketed | 9 | 0 | 0 | 0 | 0.0015 | 0.0086 | 0.0137 | 0.0151 |
| pairs | original index-position warning | share_of_finite_t41j_with_index_position_warning | 9 | 0.3959 | 0.5885 | 0.9638 | 0.978 | 0.9916 | 0.9987 | 0.9994 |
| pairs | original index-position warning | share_t41j_unsupported_below_lowest_temperature | 9 | 0 | 0.004 | 0.0385 | 0.074 | 0.102 | 0.1199 | 0.1875 |
| pairs | original index-position warning | t41j_finite_fraction | 9 | 0.8125 | 0.8801 | 0.898 | 0.926 | 0.9615 | 0.996 | 1 |
| pairs | no original index-position warning | share_replicate_energies_bracket_41j | 125 | 0 | 0.8685 | 0.896 | 0.9735 | 0.994 | 1 | 1 |
| pairs | no original index-position warning | share_of_finite_t41j_not_bracketed | 125 | 0 | 0 | 0 | 0 | 0.004 | 0.024 | 1 |
| pairs | no original index-position warning | share_of_finite_t41j_with_index_position_warning | 125 | 0 | 0 | 0 | 0.001 | 0.0098 | 0.0317 | 0.3361 |
| pairs | no original index-position warning | share_t41j_unsupported_below_lowest_temperature | 125 | 0 | 0 | 0.0055 | 0.035 | 0.106 | 0.2718 | 0.556 |
| pairs | no original index-position warning | t41j_finite_fraction | 125 | 0.444 | 0.7282 | 0.894 | 0.965 | 0.9945 | 0.9998 | 1 |
| wild | all full-size curves | share_replicate_energies_bracket_41j | 134 | 0.5065 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | all full-size curves | share_of_finite_t41j_not_bracketed | 134 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3331 |
| wild | all full-size curves | share_of_finite_t41j_with_index_position_warning | 134 | 0 | 0 | 0 | 0 | 0 | 0.0307 | 1 |
| wild | all full-size curves | share_t41j_unsupported_below_lowest_temperature | 134 | 0 | 0 | 0 | 0 | 0 | 0.0018 | 0.306 |
| wild | all full-size curves | t41j_finite_fraction | 134 | 0.694 | 0.9982 | 1 | 1 | 1 | 1 | 1 |
| wild | original T41J bracketed | share_replicate_energies_bracket_41j | 133 | 0.7515 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | original T41J bracketed | share_of_finite_t41j_not_bracketed | 133 | 0 | 0 | 0 | 0 | 0 | 0 | 0.1297 |
| wild | original T41J bracketed | share_of_finite_t41j_with_index_position_warning | 133 | 0 | 0 | 0 | 0 | 0 | 0.0321 | 1 |
| wild | original T41J bracketed | share_t41j_unsupported_below_lowest_temperature | 133 | 0 | 0 | 0 | 0 | 0 | 0 | 0.306 |
| wild | original T41J bracketed | t41j_finite_fraction | 133 | 0.694 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | original T41J not bracketed (33-153) | share_replicate_energies_bracket_41j | 1 | 0.5065 | 0.5065 | 0.5065 | 0.5065 | 0.5065 | 0.5065 | 0.5065 |
| wild | original T41J not bracketed (33-153) | share_of_finite_t41j_not_bracketed | 1 | 0.3331 | 0.3331 | 0.3331 | 0.3331 | 0.3331 | 0.3331 | 0.3331 |
| wild | original T41J not bracketed (33-153) | share_of_finite_t41j_with_index_position_warning | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wild | original T41J not bracketed (33-153) | share_t41j_unsupported_below_lowest_temperature | 1 | 0.2405 | 0.2405 | 0.2405 | 0.2405 | 0.2405 | 0.2405 | 0.2405 |
| wild | original T41J not bracketed (33-153) | t41j_finite_fraction | 1 | 0.7595 | 0.7595 | 0.7595 | 0.7595 | 0.7595 | 0.7595 | 0.7595 |
| wild | original index-position warning | share_replicate_energies_bracket_41j | 9 | 0.9955 | 0.9991 | 1 | 1 | 1 | 1 | 1 |
| wild | original index-position warning | share_of_finite_t41j_not_bracketed | 9 | 0 | 0 | 0 | 0 | 0 | 0.0001 | 0.0006 |
| wild | original index-position warning | share_of_finite_t41j_with_index_position_warning | 9 | 0.4132 | 0.661 | 0.73 | 0.9915 | 1 | 1 | 1 |
| wild | original index-position warning | share_t41j_unsupported_below_lowest_temperature | 9 | 0 | 0 | 0 | 0 | 0.0025 | 0.0245 | 0.1105 |
| wild | original index-position warning | t41j_finite_fraction | 9 | 0.8895 | 0.9755 | 0.9975 | 1 | 1 | 1 | 1 |
| wild | no original index-position warning | share_replicate_energies_bracket_41j | 125 | 0.5065 | 1 | 1 | 1 | 1 | 1 | 1 |
| wild | no original index-position warning | share_of_finite_t41j_not_bracketed | 125 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3331 |
| wild | no original index-position warning | share_of_finite_t41j_with_index_position_warning | 125 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3747 |
| wild | no original index-position warning | share_t41j_unsupported_below_lowest_temperature | 125 | 0 | 0 | 0 | 0 | 0 | 0 | 0.306 |
| wild | no original index-position warning | t41j_finite_fraction | 125 | 0.694 | 1 | 1 | 1 | 1 | 1 | 1 |

Curve 33-153:

| item | 77 |
| --- | --- |
| curve_id | 33-153 |
| outcome | usable fit, index temperature calculated |
| index_temperature_c | -114.5 |
| criterion_bracketed_by_measured_energy | False |
| n_points_below_criterion | 0 |
| n_points_above_criterion | 7 |
| flag_index_not_bracketed_by_measured_energy | True |
| index_fraction_of_rise | 0.1643 |
| flag_index_near_fitted_shelf | False |
| flag_full_size_notch_dimensions_unreported | False |
| pairs_share_replicate_energies_bracket_41j | 0 |
| pairs_t41j_finite_fraction | 0.444 |
| pairs_share_of_finite_t41j_not_bracketed | 1 |
| pairs_share_of_finite_t41j_with_index_position_warning | 0.006757 |
| pairs_share_of_finite_t41j_from_usable_replicate_fit | 0.482 |
| pairs_share_t41j_unsupported_below_lowest_temperature | 0.556 |
| pairs_share_t41j_unsupported_above_highest_temperature | 0 |
| pairs_share_t41j_undefined | 0 |
| pairs_share_t41j_optimizer_failure | 0 |
| pairs_interval_label | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) |
| wild_share_replicate_energies_bracket_41j | 0.5065 |
| wild_t41j_finite_fraction | 0.7595 |
| wild_share_of_finite_t41j_not_bracketed | 0.3331 |
| wild_share_of_finite_t41j_with_index_position_warning | 0 |
| wild_share_of_finite_t41j_from_usable_replicate_fit | 0.973 |
| wild_share_t41j_unsupported_below_lowest_temperature | 0.2405 |
| wild_share_t41j_unsupported_above_highest_temperature | 0 |
| wild_share_t41j_undefined | 0 |
| wild_share_t41j_optimizer_failure | 0 |
| wild_interval_label | interval unavailable: bootstrap-unstable (finite-target fraction below 95 %) |

## 9. Bootstrap failures and target availability (every replicate counted)

| method | geometry_category | original_wp3_outcome | curves | replicates_requested | replicates_accounted | share_optimizer failure | share_non-physical (inadmissible) | share_boundary-limited | share_weakly identified | share_usable fit, index temperature unavailable | share_usable fit, index temperature calculated | share_evaluation_errors | share_t41j_calculated | share_t41j_not calculated: optimizer failure | share_t41j_undefined: 41 J outside the fitted shelves (no rise, at or below LSE, or at or above USE) | share_t41j_unsupported: crossing below the lowest test temperature | share_t41j_unsupported: crossing above the highest test temperature | share_t41j_replicate evaluation error | share_replicates_lost_lowest_temperature | share_replicates_lost_highest_temperature |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | full-size | boundary-limited | 1 | 2000 | 2000 | 0 | 0 | 0.9365 | 0.0635 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.035 | 0.121 |
| pairs | full-size | usable fit, index temperature calculated | 104 | 208000 | 208000 | 0 | 0 | 0.0095 | 0.2433 | 0.0604 | 0.6868 | 0 | 0.9205 | 0 | 0 | 0.0794 | 0.0001 | 0 | 0.3364 | 0.3076 |
| pairs | full-size | weakly identified | 29 | 58000 | 58000 | 0 | 0 | 0.0433 | 0.6622 | 0.0316 | 0.2628 | 0 | 0.893 | 0 | 0.0003 | 0.1062 | 0.0006 | 0 | 0.3285 | 0.3254 |
| pairs | miniature | boundary-limited | 17 | 34000 | 34000 | 0.0001 | 0.0001 | 0.6323 | 0.2462 | 0.1213 | 0 | 0 |  |  |  |  |  |  | 0.3538 | 0.218 |
| pairs | miniature | usable fit, index temperature unavailable | 13 | 26000 | 26000 | 0.0004 | 0 | 0.1296 | 0.4535 | 0.4164 | 0 | 0 |  |  |  |  |  |  | 0.3512 | 0.3342 |
| pairs | miniature | weakly identified | 6 | 12000 | 12000 | 0.003 | 0 | 0.404 | 0.4871 | 0.1059 | 0 | 0 |  |  |  |  |  |  | 0.3566 | 0.3498 |
| wild | full-size | boundary-limited | 1 | 2000 | 2000 | 0 | 0 | 0.532 | 0.468 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wild | full-size | usable fit, index temperature calculated | 104 | 208000 | 208000 | 0 | 0 | 0.0009 | 0.0684 | 0.0118 | 0.9188 | 0 | 0.9863 | 0 | 0 | 0.0137 | 0 | 0 | 0 | 0 |
| wild | full-size | weakly identified | 29 | 58000 | 58000 | 0 | 0 | 0.0092 | 0.7405 | 0 | 0.2503 | 0 | 0.9939 | 0 | 0 | 0.0061 | 0 | 0 | 0 | 0 |
| wild | miniature | boundary-limited | 17 | 34000 | 34000 | 0 | 0 | 0.4916 | 0.3353 | 0.1731 | 0 | 0 |  |  |  |  |  |  | 0 | 0 |
| wild | miniature | usable fit, index temperature unavailable | 13 | 26000 | 26000 | 0 | 0 | 0.0687 | 0.3341 | 0.5972 | 0 | 0 |  |  |  |  |  |  | 0 | 0 |
| wild | miniature | weakly identified | 6 | 12000 | 12000 | 0 | 0 | 0.2966 | 0.5723 | 0.1311 | 0 | 0 |  |  |  |  |  |  | 0 | 0 |

| method | curves | replicates_requested | replicates_in_outcome_categories | all_replicates_accounted |
| --- | --- | --- | --- | --- |
| pairs | 170 | 340000 | 340000 | True |
| wild | 170 | 340000 | 340000 | True |

## 10. Uncertainty against pre-existing sampling properties

Spearman rank correlations (descriptive; association, not causation; properties are correlated with one another):

| geometry_category | key_target | metric | curves_in_analysis | curve_scope | sampling_property | spearman_rho | p_value_descriptive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | specimens (N) | -0.275 | 0.013 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | distinct test temperatures | -0.164 | 0.146 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | tested temperature span (°C) | -0.049 | 0.664 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | -0.24 | 0.032 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | -0.318 | 0.004 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | 0.154 | 0.174 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.296 | 0.008 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | WP2 lower-band temperatures | -0.024 | 0.835 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | WP2 transition-band temperatures | -0.109 | 0.335 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | WP2 upper-band temperatures | -0.167 | 0.139 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | tested span / fitted C | 0.064 | 0.571 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | -0.102 | 0.367 |
| full-size | T41J | bootstrap SD of the key target | 80 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) | -0.186 | 0.098 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | specimens (N) | -0.276 | 0.013 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | distinct test temperatures | -0.18 | 0.111 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | tested temperature span (°C) | -0.07 | 0.539 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | -0.229 | 0.041 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | -0.302 | 0.006 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | 0.137 | 0.226 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.301 | 0.007 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | WP2 lower-band temperatures | -0.039 | 0.729 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | WP2 transition-band temperatures | -0.094 | 0.406 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | WP2 upper-band temperatures | -0.206 | 0.067 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | tested span / fitted C | 0.044 | 0.698 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | -0.082 | 0.469 |
| full-size | T41J | 95 % interval width of the key target | 80 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) | -0.179 | 0.113 |
| full-size | T41J | finite key-target fraction | 134 | all curves | specimens (N) | 0.456 | 0 |
| full-size | T41J | finite key-target fraction | 134 | all curves | distinct test temperatures | 0.44 | 0 |
| full-size | T41J | finite key-target fraction | 134 | all curves | tested temperature span (°C) | 0.139 | 0.109 |
| full-size | T41J | finite key-target fraction | 134 | all curves | distinct temperatures inside T0 ± C (WP3 fit) | 0.162 | 0.061 |
| full-size | T41J | finite key-target fraction | 134 | all curves | specimens inside T0 ± C (WP3 fit) | 0.257 | 0.003 |
| full-size | T41J | finite key-target fraction | 134 | all curves | specimens on the fitted lower shelf (x <= -1.5) | 0.566 | 0 |
| full-size | T41J | finite key-target fraction | 134 | all curves | specimens on the fitted upper shelf (x >= 1.5) | 0.211 | 0.014 |
| full-size | T41J | finite key-target fraction | 134 | all curves | WP2 lower-band temperatures | 0.539 | 0 |
| full-size | T41J | finite key-target fraction | 134 | all curves | WP2 transition-band temperatures | 0.334 | 0 |
| full-size | T41J | finite key-target fraction | 134 | all curves | WP2 upper-band temperatures | 0.068 | 0.436 |
| full-size | T41J | finite key-target fraction | 134 | all curves | tested span / fitted C | 0.142 | 0.101 |
| full-size | T41J | finite key-target fraction | 134 | all curves | fitted transition half-width C (°C; curve shape, not sampling) | 0.021 | 0.811 |
| full-size | T41J | finite key-target fraction | 134 | all curves | measured energies below 41 J (WP3 audit count; full-size only) | 0.886 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | specimens (N) | -0.238 | 0.006 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | distinct test temperatures | -0.303 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | tested temperature span (°C) | -0.436 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | 0.034 | 0.695 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | -0.045 | 0.603 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | -0.035 | 0.685 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.696 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | WP2 lower-band temperatures | 0.044 | 0.616 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | WP2 transition-band temperatures | -0.01 | 0.909 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | WP2 upper-band temperatures | -0.579 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | tested span / fitted C | -0.36 | 0 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | 0 | 0.997 |
| full-size | T41J | USE 95 % width / USE | 134 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) | 0.036 | 0.68 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | specimens (N) | -0.573 | 0 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | distinct test temperatures | -0.084 | 0.625 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | tested temperature span (°C) | 0.12 | 0.484 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | 0.114 | 0.51 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | -0.162 | 0.344 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | -0.008 | 0.965 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.52 | 0.001 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | WP2 lower-band temperatures | -0.247 | 0.146 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | WP2 transition-band temperatures | -0.025 | 0.884 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | WP2 upper-band temperatures | -0.382 | 0.021 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | tested span / fitted C | -0.336 | 0.045 |
| miniature | T0 | bootstrap SD of the key target | 36 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | 0.474 | 0.003 |
| miniature | T0 | bootstrap SD of the key target | 0 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) |  |  |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | specimens (N) | -0.564 | 0 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | distinct test temperatures | -0.105 | 0.541 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | tested temperature span (°C) | 0.142 | 0.408 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | 0.1 | 0.561 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | -0.158 | 0.356 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | -0.014 | 0.933 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.512 | 0.001 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | WP2 lower-band temperatures | -0.269 | 0.112 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | WP2 transition-band temperatures | -0.052 | 0.764 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | WP2 upper-band temperatures | -0.381 | 0.022 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | tested span / fitted C | -0.319 | 0.058 |
| miniature | T0 | 95 % interval width of the key target | 36 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | 0.471 | 0.004 |
| miniature | T0 | 95 % interval width of the key target | 0 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) |  |  |
| miniature | T0 | finite key-target fraction | 36 | all curves | specimens (N) | 0.236 | 0.165 |
| miniature | T0 | finite key-target fraction | 36 | all curves | distinct test temperatures | -0.065 | 0.707 |
| miniature | T0 | finite key-target fraction | 36 | all curves | tested temperature span (°C) | -0.394 | 0.017 |
| miniature | T0 | finite key-target fraction | 36 | all curves | distinct temperatures inside T0 ± C (WP3 fit) | 0.215 | 0.207 |
| miniature | T0 | finite key-target fraction | 36 | all curves | specimens inside T0 ± C (WP3 fit) | 0.298 | 0.078 |
| miniature | T0 | finite key-target fraction | 36 | all curves | specimens on the fitted lower shelf (x <= -1.5) | 0.265 | 0.118 |
| miniature | T0 | finite key-target fraction | 36 | all curves | specimens on the fitted upper shelf (x >= 1.5) | -0.447 | 0.006 |
| miniature | T0 | finite key-target fraction | 36 | all curves | WP2 lower-band temperatures | 0.408 | 0.013 |
| miniature | T0 | finite key-target fraction | 36 | all curves | WP2 transition-band temperatures | 0.293 | 0.083 |
| miniature | T0 | finite key-target fraction | 36 | all curves | WP2 upper-band temperatures | -0.443 | 0.007 |
| miniature | T0 | finite key-target fraction | 36 | all curves | tested span / fitted C | -0.411 | 0.013 |
| miniature | T0 | finite key-target fraction | 36 | all curves | fitted transition half-width C (°C; curve shape, not sampling) | 0.211 | 0.216 |
| miniature | T0 | finite key-target fraction | 0 | all curves | measured energies below 41 J (WP3 audit count; full-size only) |  |  |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | specimens (N) | -0.18 | 0.295 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | distinct test temperatures | -0.092 | 0.593 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | tested temperature span (°C) | -0.132 | 0.441 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | distinct temperatures inside T0 ± C (WP3 fit) | 0.223 | 0.191 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | specimens inside T0 ± C (WP3 fit) | 0.159 | 0.355 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | specimens on the fitted lower shelf (x <= -1.5) | 0.166 | 0.332 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | specimens on the fitted upper shelf (x >= 1.5) | -0.726 | 0 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | WP2 lower-band temperatures | 0.15 | 0.382 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | WP2 transition-band temperatures | 0.21 | 0.218 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | WP2 upper-band temperatures | -0.54 | 0.001 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | tested span / fitted C | -0.495 | 0.002 |
| miniature | T0 | USE 95 % width / USE | 36 | reportable pairs intervals only | fitted transition half-width C (°C; curve shape, not sampling) | 0.465 | 0.004 |
| miniature | T0 | USE 95 % width / USE | 0 | reportable pairs intervals only | measured energies below 41 J (WP3 audit count; full-size only) |  |  |

Binned medians:

| geometry_category | key_target | sampling_property | bin | curves | curves_with_reportable_pairs_interval | median_pairs_sd | p25_pairs_sd | p75_pairs_sd | median_pairs_width | median_pairs_finite_fraction | median_wild_sd | median_pairs_use_relative_width |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | T41J | n_points | 6-8 | 10 | 4 | 5.135 | 3.944 | 7.79 | 21.54 | 0.904 | 2.692 | 0.222 |
| full-size | T41J | n_points | 9-11 | 49 | 23 | 5.919 | 4.21 | 8.92 | 22.04 | 0.939 | 4.975 | 0.299 |
| full-size | T41J | n_points | 12-14 | 28 | 17 | 5.433 | 4.291 | 8.48 | 20.86 | 0.962 | 5.267 | 0.167 |
| full-size | T41J | n_points | 15-19 | 23 | 17 | 4.429 | 2.933 | 5.48 | 17.77 | 0.982 | 4.997 | 0.192 |
| full-size | T41J | n_points | 20+ | 24 | 19 | 4.087 | 3.486 | 5.421 | 16.19 | 1 | 4.068 | 0.111 |
| full-size | T41J | n_temperatures | <=5 | 0 | 0 |  |  |  |  |  |  |  |
| full-size | T41J | n_temperatures | 6-8 | 23 | 10 | 4.796 | 3.925 | 6.779 | 18.07 | 0.908 | 4.376 | 0.296 |
| full-size | T41J | n_temperatures | 9-11 | 70 | 36 | 5.485 | 3.962 | 8.886 | 21.02 | 0.952 | 4.751 | 0.287 |
| full-size | T41J | n_temperatures | 12+ | 41 | 34 | 4.826 | 3.545 | 5.9 | 17.52 | 0.99 | 4.325 | 0.135 |
| full-size | T41J | T_span_c | <=150 | 15 | 3 | 3.911 | 3.244 | 4.17 | 15.1 | 0.898 | 4.385 | 0.355 |
| full-size | T41J | T_span_c | 150-250 | 48 | 33 | 5.533 | 3.969 | 8.733 | 22.04 | 0.971 | 4.73 | 0.31 |
| full-size | T41J | T_span_c | 250-350 | 53 | 32 | 4.974 | 3.879 | 6.334 | 19.82 | 0.965 | 4.465 | 0.181 |
| full-size | T41J | T_span_c | >350 | 18 | 12 | 4.243 | 3.566 | 5.727 | 16.11 | 0.966 | 4.074 | 0.095 |
| full-size | T41J | n_points_transition_fit | 0-2 | 4 | 3 | 12.26 | 9.597 | 13.25 | 47.93 | 0.989 | 4.706 | 0.526 |
| full-size | T41J | n_points_transition_fit | 3-4 | 23 | 12 | 5.156 | 4.329 | 6.438 | 20.19 | 0.956 | 3.512 | 0.208 |
| full-size | T41J | n_points_transition_fit | 5-6 | 41 | 23 | 4.929 | 4.162 | 7.391 | 20.68 | 0.954 | 4.764 | 0.17 |
| full-size | T41J | n_points_transition_fit | 7+ | 66 | 42 | 4.244 | 3.392 | 7.283 | 16.73 | 0.974 | 4.555 | 0.206 |
| full-size | T41J | n_points_upper_shelf_fit | 0-1 | 29 | 14 | 6.62 | 3.925 | 8.86 | 27.06 | 0.93 | 5.77 | 0.716 |
| full-size | T41J | n_points_upper_shelf_fit | 2-3 | 63 | 39 | 5.236 | 4.339 | 8.275 | 20.48 | 0.964 | 4.916 | 0.208 |
| full-size | T41J | n_points_upper_shelf_fit | 4+ | 42 | 27 | 3.762 | 3.441 | 5.467 | 14.77 | 0.973 | 3.849 | 0.111 |
| full-size | T41J | n_points_lower_shelf_fit | 0-1 | 94 | 41 | 4.429 | 3.496 | 6.62 | 16.47 | 0.93 | 4.401 | 0.205 |
| full-size | T41J | n_points_lower_shelf_fit | 2-3 | 27 | 26 | 5.483 | 4.505 | 7.866 | 21.02 | 0.982 | 5.06 | 0.208 |
| full-size | T41J | n_points_lower_shelf_fit | 4+ | 13 | 13 | 4.929 | 3.531 | 6.938 | 19.13 | 1 | 4.555 | 0.123 |
| full-size | T41J | n_points_below_criterion | 0 | 1 | 0 |  |  |  |  | 0.444 |  | 0.236 |
| full-size | T41J | n_points_below_criterion | 1 | 11 | 0 |  |  |  |  | 0.65 | 4.027 | 0.15 |
| full-size | T41J | n_points_below_criterion | 2 | 30 | 3 | 7.487 | 6.409 | 8.237 | 28.98 | 0.884 | 4.586 | 0.2 |
| full-size | T41J | n_points_below_criterion | 3-4 | 61 | 47 | 4.747 | 3.897 | 7.734 | 19.25 | 0.969 | 4.551 | 0.205 |
| full-size | T41J | n_points_below_criterion | 5+ | 31 | 30 | 4.986 | 3.423 | 6.122 | 19.9 | 1 | 4.511 | 0.207 |
| miniature | T0 | n_points | 6-8 | 3 | 3 | 49.84 | 36.45 | 52.8 | 250.7 | 1 | 3.578 | 5.62 |
| miniature | T0 | n_points | 9-11 | 7 | 7 | 17.79 | 12.51 | 19.3 | 59.35 | 1 | 6.65 | 0.118 |
| miniature | T0 | n_points | 12-14 | 13 | 13 | 16.13 | 7.944 | 25.51 | 68.71 | 1 | 10.51 | 0.5 |
| miniature | T0 | n_points | 15-19 | 6 | 6 | 5.65 | 3.928 | 6.848 | 20.56 | 1 | 4.395 | 0.107 |
| miniature | T0 | n_points | 20+ | 7 | 7 | 7.624 | 4.372 | 8.606 | 24.54 | 1 | 5.304 | 0.337 |
| miniature | T0 | n_temperatures | <=5 | 0 | 0 |  |  |  |  |  |  |  |
| miniature | T0 | n_temperatures | 6-8 | 6 | 6 | 15.34 | 7.279 | 43.14 | 60.38 | 1 | 4.418 | 0.236 |
| miniature | T0 | n_temperatures | 9-11 | 13 | 13 | 11.58 | 7.944 | 17.79 | 41.95 | 1 | 6.571 | 0.271 |
| miniature | T0 | n_temperatures | 12+ | 17 | 17 | 15.49 | 5.75 | 25.51 | 56.99 | 1 | 6.537 | 0.466 |
| miniature | T0 | T_span_c | <=150 | 8 | 8 | 10.12 | 7.531 | 15.65 | 35.12 | 1 | 5.947 | 0.471 |
| miniature | T0 | T_span_c | 150-250 | 16 | 16 | 10.4 | 6.81 | 22.51 | 38.31 | 1 | 5.177 | 0.236 |
| miniature | T0 | T_span_c | 250-350 | 5 | 5 | 12.25 | 5.843 | 49.84 | 46.68 | 1 | 4.167 | 0.06 |
| miniature | T0 | T_span_c | >350 | 7 | 7 | 25.11 | 11.33 | 44.17 | 107.7 | 1 | 15.02 | 0.466 |
| miniature | T0 | n_points_transition_fit | 0-2 | 7 | 7 | 20.26 | 12.51 | 36.45 | 90.59 | 1 | 3.565 | 0.118 |
| miniature | T0 | n_points_transition_fit | 3-4 | 4 | 4 | 7.118 | 5.794 | 12.34 | 22.53 | 1 | 5.2 | 0.186 |
| miniature | T0 | n_points_transition_fit | 5-6 | 9 | 9 | 16.13 | 5.75 | 52.09 | 68.71 | 1 | 5.322 | 0.858 |
| miniature | T0 | n_points_transition_fit | 7+ | 16 | 16 | 10.4 | 6.848 | 17.93 | 38.31 | 1 | 9.354 | 0.433 |
| miniature | T0 | n_points_upper_shelf_fit | 0-1 | 6 | 6 | 15.02 | 11.74 | 23.28 | 52.53 | 1 | 10.52 | 0.486 |
| miniature | T0 | n_points_upper_shelf_fit | 2-3 | 11 | 11 | 25.51 | 15.81 | 42.68 | 110 | 1 | 12.52 | 2.701 |
| miniature | T0 | n_points_upper_shelf_fit | 4+ | 19 | 19 | 7.164 | 4.879 | 12.51 | 24.17 | 1 | 3.864 | 0.118 |
| miniature | T0 | n_points_lower_shelf_fit | 0-1 | 18 | 18 | 12.24 | 7.294 | 18.21 | 46.19 | 1 | 6.476 | 0.278 |
| miniature | T0 | n_points_lower_shelf_fit | 2-3 | 14 | 14 | 12.04 | 4.59 | 44.65 | 46.44 | 1 | 5.094 | 0.268 |
| miniature | T0 | n_points_lower_shelf_fit | 4+ | 4 | 4 | 16.75 | 6.705 | 28.01 | 67.27 | 1 | 5.921 | 1.739 |

## 11. Published uncertainty cross-check

Values read from the sources (DECISIONS.md, WP4 sources):

| source | quantity | value | unit | specimens | test_matrix | basis | comparable_with |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Marini 2020, EPJ Nucl. Sci. Technol. 6:57, Tables 6-7 | precision sigma of T41 (SD of T41 over 10,000 Monte Carlo data sets) | 3.52 | °C | 18 | RCC-M MC1222 matrix: 3 specimens at each of -60, -40, -20, 0, +20 °C (transition) and +100 °C (upper shelf) | one 16MND5 forging; per-temperature bimodal Weibull scatter fitted to 142 tests; tanh with LSE = 0; fixed test matrix | bootstrap SD of T41J (one standard deviation) |
| Marini 2020, Table 7 | accuracy (mean - reference) of T41 | -0.13 | °C | 18 | RCC-M matrix | reference values from a 600-specimen simulated matrix | bootstrap bias (loosely) |
| Marini 2020, Table 7, Eq. 3 | uncertainty u = sqrt(sigma^2 + accuracy^2) of T41 | 3.52 | °C | 18 | RCC-M matrix | as above | bootstrap SD (the accuracy term is negligible here) |
| Marini 2020, Table 7 | precision sigma of USE | 4.44 | J | 18 | RCC-M matrix | as above (USE 163.6 J, Table 2) | bootstrap SD of USE |
| Marini 2020, Tables 8 and 13, Eq. 6 | T41 uncertainty amplitude a S^2 + b S + c (best estimate, c = 12.5), over the shifts studied | 12.38 to 19.58 | °C × sqrt(specimens) | 15-25 (A matrices), 10-100 (B, C) | shift S from -0.23 to 1.33 | u = amplitude / sqrt(N), fitted to his simulations | bootstrap SD × sqrt(N) |
| Marini 2020, Table 13, Eq. 6 | T41 uncertainty amplitude, upper bound (c = 16.0), over the shifts studied | 15.88 to 23.08 | °C × sqrt(specimens) | as above | as above | upper envelope of his simulations | bootstrap SD × sqrt(N) |
| Marini 2020, Tables 10 and 12 | exponent beta of u = a N^-beta for T41 (B and C matrices) | 0.51 (B); 0.53 (C) | - | 10-100 | 5 or 6 temperatures, i specimens each | power-law fit to his simulations | slope of log(bootstrap SD) against log(N) |
| Miura, Shinko & Nomoto, SSRN preprint 4917170 (2024), Eq. 13, §4 standard parameters | SD of T41J by uncertainty propagation (our evaluation of Eq. 13) | 6.87 | °C | 2 lower shelf + 6 transition + 4 upper shelf | transition specimens at T41J; C and D assumed known | LSE 3 J, USE 200 J, C 50 °C, CV at 41 J 0.49 | order of magnitude and 1/sqrt(transition specimens) scaling only |
| Switzner et al. 2023, Metals 13:877, §3.2 | USE 95 % quantile half-range (four-parameter algorithm) | 8 | J | 12 | API-5L X52 pipe, 4.5 mm sub-size bars; EUS 46 J | Monte Carlo of an assumed measurement error (0.6 J + 2.6 % of the value), 1,000 sets | not T41J; USE only loosely (different scatter source, geometry and steel) |

This project's full-size T41J bootstrap distributions, compared like with like:

| method | subset | curves | median_specimens | median_bootstrap_sd_c | p25_bootstrap_sd_c | p75_bootstrap_sd_c | median_interval_width_c | median_sd_times_sqrt_n | p25_sd_times_sqrt_n | p75_sd_times_sqrt_n | share_amplitude_below_marini_best_range | share_amplitude_within_marini_best_range | share_amplitude_above_marini_upper_bound_max | marini_best_amplitude_range | marini_upper_bound_amplitude_max | marini_rccm_sigma_c | ratio_median_sd_to_marini_rccm_sigma | theil_sen_slope_log_sd_vs_log_n | slope_ci_low | slope_ci_high | spearman_rho_sd_vs_n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | C1: usable full-size fits with a primary T41J CI | 66 | 14 | 4.87 | 3.624 | 6.84 | 19.43 | 20.39 | 14.52 | 27.45 | 0.121 | 0.348 | 0.409 | 12.38-19.58 | 23.08 | 3.52 | 1.383 | -0.324 | -0.594 | -0.103 | -0.336 |
| pairs | C2: C1 with 15-25 specimens (Marini's A matrices; RCC-M 18) | 23 | 18 | 4.429 | 3.506 | 5.406 | 17.77 | 20.34 | 16.57 | 23.78 | 0.13 | 0.348 | 0.304 | 12.38-19.58 | 23.08 | 3.52 | 1.258 | -0.062 | -1.049 | 1.181 | -0.039 |
| pairs | C3: C1 in the stricter (E185-count) cohort | 28 | 22 | 4.617 | 3.481 | 5.483 | 17.15 | 22 | 16.98 | 27.71 | 0.071 | 0.286 | 0.464 | 12.38-19.58 | 23.08 | 3.52 | 1.312 | -0.243 | -0.573 | 0.182 | -0.226 |
| wild | C1: usable full-size fits with a primary T41J CI | 97 | 13 | 4.466 | 3.304 | 6.013 | 16.51 | 18.35 | 12.35 | 22.59 | 0.258 | 0.278 | 0.227 | 12.38-19.58 | 23.08 | 3.52 | 1.269 | -0.134 | -0.354 | 0.102 | -0.099 |
| wild | C2: C1 with 15-25 specimens (Marini's A matrices; RCC-M 18) | 30 | 18 | 4.598 | 3.556 | 5.351 | 16.97 | 20.26 | 15.91 | 22.59 | 0.1 | 0.367 | 0.2 | 12.38-19.58 | 23.08 | 3.52 | 1.306 | -0.413 | -1.097 | 0.478 | -0.137 |
| wild | C3: C1 in the stricter (E185-count) cohort | 33 | 21 | 4.555 | 3.552 | 5.478 | 16.45 | 21.85 | 17.11 | 25.26 | 0.091 | 0.273 | 0.333 | 12.38-19.58 | 23.08 | 3.52 | 1.294 | -0.287 | -0.618 | 0.058 | -0.256 |

## 12. Pairs (primary) against fixed-design wild (sensitivity)

| geometry_category | target | scope | ratio | curves | median | p10 | p90 | minimum | maximum | share_pairs_wider | curve_min | curve_max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | c | both methods reportable | ratio_sd_pairs_to_wild | 134 | 1.212 | 0.986 | 1.783 | 0.646 | 3.54 | 0.873 | 49-206 | 13-60 |
| full-size | c | both methods reportable | ratio_width_pairs_to_wild | 134 | 1.245 | 0.997 | 1.879 | 0.653 | 4.402 | 0.896 | 49-206 | 13-60 |
| full-size | c | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 104 | 1.175 | 0.978 | 1.779 | 0.888 | 3.54 | 0.856 | 41-187 | 13-60 |
| full-size | c | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 104 | 1.238 | 0.988 | 1.822 | 0.787 | 4.402 | 0.875 | 41-187 | 13-60 |
| full-size | t0 | both methods reportable | ratio_sd_pairs_to_wild | 134 | 1.428 | 1.006 | 3.419 | 0.412 | 9.817 | 0.903 | 49-206 | 104-none.3 |
| full-size | t0 | both methods reportable | ratio_width_pairs_to_wild | 134 | 1.335 | 0.978 | 2.945 | 0.599 | 9.544 | 0.873 | 49-206 | 13-60 |
| full-size | t0 | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 104 | 1.364 | 0.997 | 2.663 | 0.911 | 8.06 | 0.894 | 47-198 | 13-60 |
| full-size | t0 | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 104 | 1.22 | 0.977 | 2.433 | 0.82 | 9.544 | 0.856 | 48-200 | 13-60 |
| full-size | t41j | both methods reportable | ratio_sd_pairs_to_wild | 80 | 1.06 | 0.931 | 1.476 | 0.879 | 3.399 | 0.688 | 53-225 | 13-60 |
| full-size | t41j | both methods reportable | ratio_width_pairs_to_wild | 80 | 1.092 | 0.951 | 1.514 | 0.876 | 3.824 | 0.738 | 4-21 | 13-60 |
| full-size | t41j | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 66 | 1.04 | 0.93 | 1.522 | 0.879 | 3.399 | 0.636 | 53-225 | 13-60 |
| full-size | t41j | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 66 | 1.08 | 0.949 | 1.543 | 0.889 | 3.824 | 0.712 | 1-2 | 13-60 |
| full-size | use | both methods reportable | ratio_sd_pairs_to_wild | 134 | 2.459 | 1.012 | 16.03 | 0.517 | 71.44 | 0.903 | 49-206 | 59-267 |
| full-size | use | both methods reportable | ratio_width_pairs_to_wild | 134 | 1.377 | 0.986 | 5.917 | 0.775 | 78.08 | 0.873 | 12-48 | 59-267 |
| full-size | use | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 104 | 2.367 | 1.012 | 13.41 | 0.893 | 71.44 | 0.904 | 41-188 | 59-267 |
| full-size | use | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 104 | 1.29 | 0.986 | 3.594 | 0.878 | 78.08 | 0.865 | 41-187 | 59-267 |
| miniature | c | both methods reportable | ratio_sd_pairs_to_wild | 36 | 1.275 | 0.943 | 1.643 | 0.727 | 4.889 | 0.778 | 53-241 | 53-234 |
| miniature | c | both methods reportable | ratio_width_pairs_to_wild | 36 | 1.311 | 0.954 | 1.555 | 0.766 | 8.141 | 0.75 | 59-272 | 53-234 |
| miniature | c | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 13 | 1.367 | 1.087 | 1.496 | 0.808 | 1.575 | 0.923 | 59-272 | 59-271.1 |
| miniature | c | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 13 | 1.333 | 0.988 | 1.509 | 0.766 | 1.563 | 0.846 | 59-272 | 59-271.1 |
| miniature | lse | both methods reportable | ratio_sd_pairs_to_wild | 36 | 1.392 | 0.954 | 2.953 | 0.56 | 5.312 | 0.889 | 53-232 | 53-234 |
| miniature | lse | both methods reportable | ratio_width_pairs_to_wild | 36 | 1.658 | 0.891 | 3.59 | 0.57 | 8.71 | 0.833 | 53-232 | 53-234 |
| miniature | lse | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 13 | 1.749 | 1.174 | 2.318 | 1.032 | 2.402 | 1 | 59-270 | 107-283 |
| miniature | lse | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 13 | 1.954 | 1.049 | 2.51 | 1.012 | 2.62 | 1 | 59-271.1 | 55-256 |
| miniature | t0 | both methods reportable | ratio_sd_pairs_to_wild | 36 | 1.559 | 1.131 | 4.301 | 1.05 | 15.59 | 1 | 53-227 | 53-234 |
| miniature | t0 | both methods reportable | ratio_width_pairs_to_wild | 36 | 1.435 | 1.118 | 5.127 | 1.06 | 22.89 | 1 | 53-227 | 53-234 |
| miniature | t0 | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 13 | 1.715 | 1.149 | 3.964 | 1.121 | 4.157 | 1 | 53-228 | 52-221 |
| miniature | t0 | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 13 | 1.882 | 1.149 | 4.491 | 1.104 | 5.755 | 1 | 59-272 | 55-256 |
| miniature | use | both methods reportable | ratio_sd_pairs_to_wild | 36 | 1.995 | 1.11 | 18.27 | 0.853 | 45.09 | 0.972 | 53-230 | 53-234 |
| miniature | use | both methods reportable | ratio_width_pairs_to_wild | 36 | 1.44 | 0.983 | 19.35 | 0.876 | 44.21 | 0.861 | 59-271.2 | 53-234 |
| miniature | use | both reportable and original WP3 fit usable | ratio_sd_pairs_to_wild | 13 | 5.043 | 1.404 | 26.04 | 1.275 | 30.17 | 1 | 109-287 | 55-256 |
| miniature | use | both reportable and original WP3 fit usable | ratio_width_pairs_to_wild | 13 | 2.469 | 1.078 | 23.57 | 0.993 | 34.76 | 0.923 | 53-228 | 55-256 |

Largest disagreements (key targets):

| extreme | curve_id | geometry_category | target | outcome | n_points | n_temperatures | n_points_transition_fit | pairs_sd | wild_sd | ratio_sd_pairs_to_wild | max_leverage | points_with_leverage_numerically_one |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs much narrower than fixed design (lowest ratios) | 53-225 | full-size | t41j | usable fit, index temperature calculated | 17 | 7 | 12 | 4.159 | 4.73 | 0.879 | 0.29 | 0 |
| pairs much narrower than fixed design (lowest ratios) | 4-21 | full-size | t41j | weakly identified | 19 | 7 | 14 | 3.911 | 4.425 | 0.884 | 0.435 | 0 |
| pairs much narrower than fixed design (lowest ratios) | 59-275 | full-size | t41j | usable fit, index temperature calculated | 10 | 9 | 6 | 4.034 | 4.551 | 0.886 | 0.691 | 0 |
| pairs much wider (highest ratios) | 42-189 | full-size | t41j | usable fit, index temperature calculated | 11 | 11 | 2 | 14.25 | 5.035 | 2.83 | 0.739 | 0 |
| pairs much wider (highest ratios) | 2-9 | full-size | t41j | usable fit, index temperature calculated | 13 | 13 | 4 | 3.589 | 1.236 | 2.903 | 0.591 | 0 |
| pairs much wider (highest ratios) | 13-60 | full-size | t41j | usable fit, index temperature calculated | 9 | 9 | 3 | 7.998 | 2.353 | 3.399 | 0.692 | 0 |
| pairs much narrower than fixed design (lowest ratios) | 53-227 | miniature | t0 | boundary-limited | 24 | 10 | 18 | 9.217 | 8.774 | 1.05 | 0.234 | 0 |
| pairs much narrower than fixed design (lowest ratios) | 53-232 | miniature | t0 | boundary-limited | 22 | 9 | 15 | 5.387 | 5.095 | 1.057 | 0.536 | 0 |
| pairs much narrower than fixed design (lowest ratios) | 53-228 | miniature | t0 | usable fit, index temperature unavailable | 19 | 10 | 8 | 5.456 | 4.866 | 1.121 | 0.335 | 0 |
| pairs much wider (highest ratios) | 53-235 | miniature | t0 | boundary-limited | 11 | 11 | 2 | 20.26 | 2.459 | 8.239 | 0.796 | 0 |
| pairs much wider (highest ratios) | 53-244 | miniature | t0 | boundary-limited | 8 | 7 | 1 | 23.06 | 2.104 | 10.96 | 1 | 1 |
| pairs much wider (highest ratios) | 53-234 | miniature | t0 | weakly identified | 8 | 8 | 1 | 55.77 | 3.578 | 15.59 | 0.998 | 0 |

## 13. Monte Carlo stability (B = 2,000 against an independent B = 4,000 run)

| curve_id | method | target | b2000_q025 | b4000_q025 | b2000_median | b4000_median | b2000_q975 | b4000_q975 | b2000_sd | b4000_sd | max_abs_endpoint_or_median_change_as_share_of_b2000_width | reportable_status_changes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50-208 | pairs | t41j | 196.5 | 196.5 | 199.8 | 199.9 | 203.3 | 203.3 | 1.929 | 1.97 | 0.01 | False |
| 50-208 | pairs | use | 61.57 | 61.57 | 78.5 | 78.5 | 85.87 | 85.87 | 45.37 | 44.59 | 0 | False |
| 50-208 | pairs | t0 | 191.9 | 191.5 | 199.4 | 199.4 | 208.5 | 208.5 | 4.836 | 4.916 | 0.023 | False |
| 50-208 | wild | t41j | 196.9 | 196.9 | 200.1 | 200.1 | 203.9 | 203.9 | 2.086 | 2.113 | 0.01 | False |
| 50-208 | wild | use | 76.27 | 76.2 | 78.57 | 78.57 | 81.17 | 81.17 | 1.474 | 1.497 | 0.014 | False |
| 50-208 | wild | t0 | 196.4 | 196.4 | 199.8 | 199.9 | 204.1 | 204.1 | 2.337 | 2.369 | 0.01 | False |
| 54-252 | pairs | t41j | -98.7 | -99 | -91.92 | -91.81 | -84.65 | -83.82 | 4.157 | 4.314 | 0.059 | False |
| 54-252 | pairs | use | 185.5 | 185.3 | 193 | 193 | 203.6 | 203.9 | 6.097 | 5.485 | 0.016 | False |
| 54-252 | pairs | t0 | -77.97 | -78.15 | -72.55 | -72.63 | -66.57 | -65.06 | 3.273 | 3.725 | 0.133 | False |
| 54-252 | wild | t41j | -98.03 | -98 | -91.92 | -91.89 | -87.18 | -87.21 | 3.03 | 3.027 | 0.003 | False |
| 54-252 | wild | use | 185.2 | 185.2 | 193.8 | 193.6 | 202.3 | 202.2 | 4.888 | 4.923 | 0.013 | False |
| 54-252 | wild | t0 | -76.14 | -76.19 | -72.8 | -72.8 | -68.18 | -68.18 | 2.091 | 2.121 | 0.006 | False |
| 1-6.1 | pairs | t41j | -24.62 | -24.38 | -19.48 | -19.52 | -14.29 | -14.14 | 2.583 | 2.6 | 0.023 | False |
| 1-6.1 | pairs | use | 141.1 | 141.2 | 145.3 | 145.4 | 150.3 | 150 | 2.29 | 2.257 | 0.031 | False |
| 1-6.1 | pairs | t0 | 5.241 | 5.04 | 9.322 | 9.344 | 13.47 | 13.51 | 2.132 | 2.166 | 0.024 | False |
| 1-6.1 | wild | t41j | -24.38 | -24.44 | -19.4 | -19.37 | -14.54 | -14.23 | 2.592 | 2.591 | 0.032 | False |
| 1-6.1 | wild | use | 140.9 | 140.8 | 145.4 | 145.4 | 150.5 | 150.3 | 2.48 | 2.456 | 0.015 | False |
| 1-6.1 | wild | t0 | 5.06 | 4.959 | 9.237 | 9.276 | 14.06 | 13.92 | 2.305 | 2.294 | 0.015 | False |
| 104-none.3 | pairs | t41j | 20.75 | 20.74 | 25.89 | 25.92 | 29.73 | 29.73 | 3.973 | 4.975 | 0.003 | False |
| 104-none.3 | pairs | use | 137.8 | 137.8 | 171.9 | 171.9 | 194.4 | 194.4 | 16.5 | 16.24 | 0 | False |
| 104-none.3 | pairs | t0 | -0.443 | 21.21 | 30.01 | 30.31 | 41.83 | 42.03 | 26.61 | 22.77 | 0.512 | False |
| 104-none.3 | wild | t41j | 21.05 | 21.05 | 24.68 | 24.42 | 33.1 | 33.1 | 3.992 | 3.974 | 0.021 | False |
| 104-none.3 | wild | use | 139.2 | 139.2 | 169.3 | 168.4 | 202.1 | 202.1 | 17.93 | 17.54 | 0.015 | False |
| 104-none.3 | wild | t0 | 24 | 24 | 31.2 | 31.03 | 33.75 | 33.7 | 2.71 | 2.782 | 0.017 | False |
| 28-133 | pairs | t41j | -41.37 | -41.51 | -27.8 | -27.55 | -12.39 | -12.99 | 7.487 | 7.481 | 0.021 | False |
| 28-133 | pairs | use | 213.2 | 213.2 | 226.3 | 225.7 | 1806 | 1835 | 337 | 334.3 | 0.018 | False |
| 28-133 | pairs | t0 | 15.29 | 15.2 | 26.56 | 26.66 | 189.2 | 189.6 | 43.98 | 42.11 | 0.003 | False |
| 28-133 | wild | t41j | -38.34 | -38.35 | -24.96 | -25.18 | -15.9 | -16.04 | 5.676 | 5.799 | 0.01 | False |
| 28-133 | wild | use | 204.9 | 206.1 | 224.7 | 225 | 256.5 | 257.6 | 14.37 | 14.27 | 0.023 | False |
| 28-133 | wild | t0 | 11.39 | 11.6 | 25.6 | 25.64 | 45.73 | 46.27 | 8.768 | 8.753 | 0.016 | False |
| 4-22 | pairs | t41j | -60.19 | -60.43 | -50.26 | -50.34 | -42.19 | -42.2 | 4.659 | 4.802 | 0.013 | False |
| 4-22 | pairs | use | 203.5 | 204.3 | 245.8 | 246.4 | 320.2 | 326.6 | 30.46 | 31.37 | 0.055 | False |
| 4-22 | pairs | t0 | -27.65 | -27.54 | -18.85 | -18.75 | 0.896 | 1.509 | 7.471 | 7.626 | 0.021 | False |
| 4-22 | wild | t41j | -60.89 | -60.82 | -51.91 | -51.92 | -44.82 | -44.6 | 4.346 | 4.407 | 0.013 | False |
| 4-22 | wild | use | 215.4 | 216.9 | 245.4 | 245.2 | 320.5 | 317 | 27.23 | 26.45 | 0.033 | False |
| 4-22 | wild | t0 | -25.82 | -25.54 | -18.7 | -18.76 | -0.783 | -1.518 | 6.587 | 6.45 | 0.029 | False |
| 55-256 | pairs | t0 | 66.99 | 62.95 | 123.1 | 123.1 | 317.7 | 316.1 | 49.84 | 45.98 | 0.016 | False |
| 55-256 | pairs | use | 12.57 | 12.54 | 13.08 | 13.1 | 141.2 | 141.1 | 27.93 | 24.98 | 0.001 | False |
| 55-256 | wild | t0 | 104.1 | 104.5 | 119.6 | 122.1 | 147.7 | 147.7 | 12.52 | 12.37 | 0.058 | False |
| 55-256 | wild | use | 11.55 | 11.55 | 13.41 | 13.44 | 15.25 | 15.25 | 0.926 | 0.904 | 0.006 | False |
| 109-287 | pairs | t0 | -166.9 | -166.9 | -157.3 | -157.3 | -148.6 | -148.6 | 4.301 | 4.363 | 0.002 | False |
| 109-287 | pairs | use | 7.9 | 7.9 | 7.923 | 7.923 | 7.999 | 7.999 | 0.028 | 1.517 | 0.009 | False |
| 109-287 | wild | t0 | -160.6 | -160.3 | -157.6 | -157.6 | -153.6 | -153.6 | 1.689 | 1.655 | 0.042 | False |
| 109-287 | wild | use | 7.895 | 7.895 | 7.944 | 7.944 | 7.981 | 7.98 | 0.022 | 0.022 | 0.009 | False |
| 53-228 | pairs | t0 | -40.97 | -41.4 | -30.42 | -30.58 | -20.84 | -21.11 | 5.456 | 5.976 | 0.022 | False |
| 53-228 | pairs | use | 26.66 | 26.68 | 28.52 | 28.53 | 34.55 | 33.7 | 3.474 | 8.598 | 0.108 | False |
| 53-228 | wild | t0 | -40 | -39.98 | -31.56 | -31.85 | -22.14 | -21.96 | 4.866 | 4.912 | 0.016 | False |
| 53-228 | wild | use | 25.58 | 25.69 | 28.93 | 28.96 | 33.52 | 33.42 | 1.871 | 1.871 | 0.014 | False |
| 53-234 | pairs | t0 | -118.8 | -117.1 | -108 | -108 | 140.3 | 140.3 | 55.77 | 54.87 | 0.007 | False |
| 53-234 | pairs | use | 0.924 | 0.928 | 0.995 | 0.993 | 6.455 | 6.5 | 1.683 | 1.677 | 0.008 | False |
| 53-234 | wild | t0 | -112.2 | -112.2 | -107.9 | -108 | -100.9 | -100.9 | 3.578 | 3.522 | 0.011 | False |
| 53-234 | wild | use | 0.922 | 0.922 | 0.985 | 0.984 | 1.047 | 1.047 | 0.037 | 0.037 | 0.001 | False |
| 109-293 | pairs | t0 | 72.11 | 71.99 | 124.9 | 124.6 | 179.8 | 182.4 | 25.11 | 25.97 | 0.024 | False |
| 109-293 | pairs | use | 3.582 | 3.59 | 4.523 | 4.535 | 5.713 | 5.772 | 0.508 | 0.52 | 0.028 | False |
| 109-293 | wild | t0 | 100.1 | 98.12 | 125.7 | 125.6 | 158 | 158.4 | 15.02 | 15.13 | 0.035 | False |
| 109-293 | wild | use | 4.079 | 4.08 | 4.546 | 4.546 | 5.237 | 5.214 | 0.3 | 0.292 | 0.019 | False |
| 53-229 | pairs | t0 | -54.42 | -53.81 | -37.86 | -37.66 | -12.47 | -10.64 | 11.58 | 12.03 | 0.044 | False |
| 53-229 | pairs | use | 27.36 | 27.11 | 33.77 | 33.82 | 49.55 | 50.62 | 10.17 | 10.1 | 0.048 | False |
| 53-229 | wild | t0 | -51.38 | -51.21 | -37.6 | -37.52 | -13.54 | -14.77 | 9.934 | 9.465 | 0.032 | False |
| 53-229 | wild | use | 28.53 | 28.55 | 33.54 | 33.32 | 49.47 | 48.84 | 5.898 | 5.384 | 0.03 | False |
| 57-263 | pairs | t41j | 5.487 | 5.503 | 7.809 | 7.771 | 10.26 | 10.19 | 1.2 | 1.22 | 0.013 | False |
| 57-263 | pairs | use | 99.47 | 99.47 | 102.4 | 102.4 | 106.3 | 106.4 | 1.772 | 1.787 | 0.018 | False |
| 57-263 | pairs | t0 | 15.46 | 15.39 | 18.88 | 18.92 | 23.71 | 23.67 | 2.138 | 2.172 | 0.009 | False |
| 57-263 | wild | t41j | 5.473 | 5.484 | 7.764 | 7.717 | 10.37 | 10.25 | 1.275 | 1.25 | 0.025 | False |
| 57-263 | wild | use | 99.16 | 99.27 | 102.5 | 102.4 | 105.7 | 105.6 | 1.697 | 1.654 | 0.017 | False |
| 57-263 | wild | t0 | 14.9 | 14.89 | 18.9 | 18.85 | 23.44 | 23.3 | 2.33 | 2.285 | 0.015 | False |
| 55-255 | pairs | t41j | 161.8 | 162.3 | 209.9 | 209.7 | 243.3 | 242.6 | 22.37 | 24.02 | 0.009 | False |
| 55-255 | pairs | use | 45.97 | 45.72 | 50.91 | 50.89 | 60.87 | 62.6 | 19.96 | 28.09 | 0.116 | False |
| 55-255 | pairs | t0 | 147 | 143.9 | 172.2 | 173.6 | 202.9 | 204.7 | 21.05 | 24.02 | 0.055 | False |
| 55-255 | wild | t41j | 178 | 178 | 206.8 | 208.1 | 245.8 | 245.7 | 18.75 | 18.88 | 0.019 | False |
| 55-255 | wild | use | 44.31 | 44.75 | 51.07 | 51.2 | 58.5 | 58.96 | 3.46 | 3.433 | 0.032 | False |
| 55-255 | wild | t0 | 130.6 | 131.5 | 169.7 | 169.1 | 198.6 | 198.6 | 17.84 | 17.88 | 0.014 | False |
| 107-283 | pairs | t0 | -71.57 | -71.53 | -68.03 | -68.08 | -63.23 | -63.36 | 2.284 | 2.132 | 0.015 | False |
| 107-283 | pairs | use | 6.788 | 6.799 | 6.975 | 6.974 | 7.066 | 7.063 | 0.07 | 0.07 | 0.039 | False |
| 107-283 | wild | t0 | -71.35 | -71.32 | -68.05 | -67.98 | -64.62 | -64.63 | 1.887 | 1.943 | 0.011 | False |
| 107-283 | wild | use | 6.843 | 6.845 | 6.957 | 6.958 | 7.055 | 7.051 | 0.054 | 0.053 | 0.017 | False |
| 55-257 | pairs | t0 | 179.7 | 179.4 | 206.8 | 208.1 | 440.5 | 442.7 | 59.27 | 61.82 | 0.008 | False |
| 55-257 | pairs | use | 10.1 | 10.09 | 10.88 | 10.93 | 119.4 | 119.4 | 24.35 | 25.92 | 0 | False |
| 55-257 | wild | t0 | 176 | 174.6 | 204 | 203.5 | 234.6 | 233.2 | 15.53 | 15.36 | 0.024 | False |
| 55-257 | wild | use | 8.839 | 8.856 | 10.96 | 10.96 | 13.6 | 13.52 | 1.405 | 1.375 | 0.016 | False |

| method | target | curve_target_rows | median_share_of_width | max_share_of_width | max_abs_change_q025 | max_abs_change_q975 | max_abs_change_sd | reportable_status_changes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pairs | t0 | 16 | 0.0216 | 0.5122 | 21.66 | 2.602 | 3.861 | 0 |
| pairs | t41j | 8 | 0.0132 | 0.0588 | 0.5172 | 0.8262 | 1.657 | 0 |
| pairs | use | 16 | 0.0181 | 0.1163 | 0.7559 | 28.42 | 8.129 | 0 |
| wild | t0 | 16 | 0.0161 | 0.058 | 2.006 | 1.432 | 0.4691 | 0 |
| wild | t41j | 8 | 0.0161 | 0.0317 | 0.064 | 0.3122 | 0.1337 | 0 |
| wild | use | 16 | 0.0156 | 0.0331 | 1.509 | 3.478 | 0.7777 | 0 |

## 14. Empirical published-data residual scatter (not a pure material-scatter distribution)

| curve_set | geometry_category | region | quantity | residuals | curves | mean | sd | median | mad_scaled | q05 | q25 | q75 | q95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| usable WP3 fits (primary summary) | full-size | lower shelf (x <= -1.5) | residual / fitted USE | 154 | 70 | 0.0146 | 0.0354 | 0.0079 | 0.0226 | -0.0234 | -0.0071 | 0.0232 | 0.0821 |
| usable WP3 fits (primary summary) | full-size | lower shelf (x <= -1.5) | leverage-adjusted residual / fitted USE | 154 | 70 | 0.0149 | 0.0361 | 0.008 | 0.0225 | -0.0236 | -0.0071 | 0.0232 | 0.0827 |
| usable WP3 fits (primary summary) | full-size | lower transition (-1.5 < x <= -0.5) | residual / fitted USE | 339 | 102 | -0.0039 | 0.0669 | -0.0096 | 0.0493 | -0.1066 | -0.0409 | 0.0283 | 0.122 |
| usable WP3 fits (primary summary) | full-size | lower transition (-1.5 < x <= -0.5) | leverage-adjusted residual / fitted USE | 339 | 102 | -0.0047 | 0.0729 | -0.0107 | 0.0543 | -0.1191 | -0.0451 | 0.0316 | 0.1286 |
| usable WP3 fits (primary summary) | full-size | central transition (-0.5 < x < 0.5) | residual / fitted USE | 511 | 103 | -0.0014 | 0.096 | -0.0025 | 0.0851 | -0.1579 | -0.0586 | 0.0557 | 0.1448 |
| usable WP3 fits (primary summary) | full-size | central transition (-0.5 < x < 0.5) | leverage-adjusted residual / fitted USE | 511 | 103 | -0.0009 | 0.1052 | -0.0027 | 0.0986 | -0.1716 | -0.067 | 0.0647 | 0.1631 |
| usable WP3 fits (primary summary) | full-size | upper transition (0.5 <= x < 1.5) | residual / fitted USE | 286 | 101 | 0.0089 | 0.0911 | 0.0056 | 0.0764 | -0.1357 | -0.0457 | 0.057 | 0.1671 |
| usable WP3 fits (primary summary) | full-size | upper transition (0.5 <= x < 1.5) | leverage-adjusted residual / fitted USE | 286 | 101 | 0.0086 | 0.0998 | 0.0063 | 0.0852 | -0.1572 | -0.0514 | 0.0622 | 0.1787 |
| usable WP3 fits (primary summary) | full-size | upper shelf (x >= 1.5) | residual / fitted USE | 395 | 104 | -0.0029 | 0.0535 | -0.0026 | 0.0444 | -0.0878 | -0.0323 | 0.0274 | 0.0786 |
| usable WP3 fits (primary summary) | full-size | upper shelf (x >= 1.5) | leverage-adjusted residual / fitted USE | 395 | 104 | -0.0031 | 0.0616 | -0.0031 | 0.0513 | -0.1056 | -0.0377 | 0.0314 | 0.0948 |
| usable WP3 fits (primary summary) | miniature | lower shelf (x <= -1.5) | residual / fitted USE | 35 | 13 | -0.007 | 0.0588 | -0.0066 | 0.0391 | -0.0741 | -0.0311 | 0.0188 | 0.0925 |
| usable WP3 fits (primary summary) | miniature | lower shelf (x <= -1.5) | leverage-adjusted residual / fitted USE | 35 | 13 | -0.0103 | 0.07 | -0.0081 | 0.048 | -0.0942 | -0.0395 | 0.0232 | 0.104 |
| usable WP3 fits (primary summary) | miniature | lower transition (-1.5 < x <= -0.5) | residual / fitted USE | 23 | 13 | 0.01 | 0.1 | 0.0343 | 0.0723 | -0.1501 | -0.0525 | 0.0515 | 0.1846 |
| usable WP3 fits (primary summary) | miniature | lower transition (-1.5 < x <= -0.5) | leverage-adjusted residual / fitted USE | 23 | 13 | 0.0128 | 0.1156 | 0.0474 | 0.0953 | -0.1746 | -0.0588 | 0.0655 | 0.1994 |
| usable WP3 fits (primary summary) | miniature | central transition (-0.5 < x < 0.5) | residual / fitted USE | 42 | 13 | -0.0168 | 0.1428 | -0.0231 | 0.0997 | -0.2374 | -0.0765 | 0.0527 | 0.2221 |
| usable WP3 fits (primary summary) | miniature | central transition (-0.5 < x < 0.5) | leverage-adjusted residual / fitted USE | 42 | 13 | -0.0182 | 0.167 | -0.0287 | 0.1158 | -0.2729 | -0.0892 | 0.0629 | 0.2483 |
| usable WP3 fits (primary summary) | miniature | upper transition (0.5 <= x < 1.5) | residual / fitted USE | 33 | 13 | 0.0403 | 0.0973 | 0.0272 | 0.0886 | -0.0937 | -0.0192 | 0.0918 | 0.1987 |
| usable WP3 fits (primary summary) | miniature | upper transition (0.5 <= x < 1.5) | leverage-adjusted residual / fitted USE | 33 | 13 | 0.0454 | 0.1133 | 0.0308 | 0.1015 | -0.1273 | -0.0203 | 0.105 | 0.2239 |
| usable WP3 fits (primary summary) | miniature | upper shelf (x >= 1.5) | residual / fitted USE | 46 | 13 | -0.0132 | 0.0532 | -0.0043 | 0.0192 | -0.0993 | -0.0358 | 0.0027 | 0.0572 |
| usable WP3 fits (primary summary) | miniature | upper shelf (x >= 1.5) | leverage-adjusted residual / fitted USE | 46 | 13 | -0.0182 | 0.066 | -0.0047 | 0.023 | -0.1506 | -0.0465 | 0.003 | 0.0746 |
| all WP3 fits (sensitivity) | full-size | lower shelf (x <= -1.5) | residual / fitted USE | 186 | 85 | 0.0121 | 0.0336 | 0.0063 | 0.0205 | -0.0251 | -0.0074 | 0.0205 | 0.0764 |
| all WP3 fits (sensitivity) | full-size | lower shelf (x <= -1.5) | leverage-adjusted residual / fitted USE | 186 | 85 | 0.0122 | 0.0342 | 0.0064 | 0.0211 | -0.0259 | -0.0075 | 0.021 | 0.0779 |
| all WP3 fits (sensitivity) | full-size | lower transition (-1.5 < x <= -0.5) | residual / fitted USE | 431 | 131 | -0.003 | 0.0667 | -0.0083 | 0.051 | -0.108 | -0.0396 | 0.0298 | 0.1254 |
| all WP3 fits (sensitivity) | full-size | lower transition (-1.5 < x <= -0.5) | leverage-adjusted residual / fitted USE | 431 | 131 | -0.0037 | 0.0729 | -0.0091 | 0.0561 | -0.1211 | -0.0447 | 0.0324 | 0.1338 |
| all WP3 fits (sensitivity) | full-size | central transition (-0.5 < x < 0.5) | residual / fitted USE | 641 | 131 | -0.0009 | 0.0964 | -0.0025 | 0.0851 | -0.1536 | -0.0589 | 0.0554 | 0.1495 |
| all WP3 fits (sensitivity) | full-size | central transition (-0.5 < x < 0.5) | leverage-adjusted residual / fitted USE | 641 | 131 | -0.0005 | 0.1061 | -0.0027 | 0.0978 | -0.1658 | -0.0674 | 0.0642 | 0.1685 |
| all WP3 fits (sensitivity) | full-size | upper transition (0.5 <= x < 1.5) | residual / fitted USE | 379 | 130 | 0.0073 | 0.0881 | 0.0089 | 0.0721 | -0.1272 | -0.0449 | 0.0529 | 0.1563 |
| all WP3 fits (sensitivity) | full-size | upper transition (0.5 <= x < 1.5) | leverage-adjusted residual / fitted USE | 379 | 130 | 0.0071 | 0.0971 | 0.0097 | 0.0817 | -0.1461 | -0.0512 | 0.06 | 0.1632 |
| all WP3 fits (sensitivity) | full-size | upper shelf (x >= 1.5) | residual / fitted USE | 422 | 128 | -0.0032 | 0.0558 | -0.0039 | 0.0464 | -0.0907 | -0.0345 | 0.0275 | 0.0812 |
| all WP3 fits (sensitivity) | full-size | upper shelf (x >= 1.5) | leverage-adjusted residual / fitted USE | 422 | 128 | -0.004 | 0.0666 | -0.0044 | 0.0546 | -0.114 | -0.0424 | 0.0318 | 0.0967 |
| all WP3 fits (sensitivity) | miniature | lower shelf (x <= -1.5) | residual / fitted USE | 61 | 27 | 0.0002 | 0.0523 | 0.0011 | 0.0352 | -0.0603 | -0.021 | 0.0248 | 0.0915 |
| all WP3 fits (sensitivity) | miniature | lower shelf (x <= -1.5) | leverage-adjusted residual / fitted USE | 61 | 27 | 0.0032 | 0.0669 | 0.0013 | 0.0455 | -0.0739 | -0.0293 | 0.0308 | 0.1155 |
| all WP3 fits (sensitivity) | miniature | lower transition (-1.5 < x <= -0.5) | residual / fitted USE | 77 | 33 | -0.026 | 0.0803 | -0.0305 | 0.0781 | -0.1424 | -0.0762 | 0.0226 | 0.129 |
| all WP3 fits (sensitivity) | miniature | lower transition (-1.5 < x <= -0.5) | leverage-adjusted residual / fitted USE | 77 | 33 | -0.0303 | 0.0923 | -0.0358 | 0.1021 | -0.1648 | -0.0869 | 0.0338 | 0.1455 |
| all WP3 fits (sensitivity) | miniature | central transition (-0.5 < x < 0.5) | residual / fitted USE | 141 | 35 | 0.008 | 0.1693 | -0 | 0.1509 | -0.2564 | -0.0961 | 0.1018 | 0.2566 |
| all WP3 fits (sensitivity) | miniature | central transition (-0.5 < x < 0.5) | leverage-adjusted residual / fitted USE | 141 | 35 | 0.0096 | 0.187 | 0 | 0.1737 | -0.2759 | -0.1097 | 0.1196 | 0.2713 |
| all WP3 fits (sensitivity) | miniature | upper transition (0.5 <= x < 1.5) | residual / fitted USE | 107 | 34 | 0.0061 | 0.1129 | 0.005 | 0.0875 | -0.1509 | -0.0498 | 0.0662 | 0.17 |
| all WP3 fits (sensitivity) | miniature | upper transition (0.5 <= x < 1.5) | leverage-adjusted residual / fitted USE | 107 | 34 | 0.0069 | 0.127 | 0.0146 | 0.0992 | -0.1896 | -0.0619 | 0.0756 | 0.1924 |
| all WP3 fits (sensitivity) | miniature | upper shelf (x >= 1.5) | residual / fitted USE | 143 | 34 | -0.0018 | 0.0699 | 0.0003 | 0.0465 | -0.1273 | -0.0348 | 0.0265 | 0.1101 |
| all WP3 fits (sensitivity) | miniature | upper shelf (x >= 1.5) | leverage-adjusted residual / fitted USE | 143 | 34 | -0.0031 | 0.0787 | 0.0004 | 0.0518 | -0.1526 | -0.0404 | 0.0295 | 0.1192 |

Strata (full-size usable fits, leverage-adjusted residual / fitted USE):

| curve_set | dimension | value | zone | residuals | curves | interpretable | mean | sd | median | mad_scaled | q05 | q25 | q75 | q95 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| usable WP3 fits, full-size | product_form_group | HAZ (incl. simulated) | lower shelf (x <= -1.5) | 9 | 5 | False | 0.0148 | 0.013 | 0.0113 | 0.0143 | -0.0015 | 0.0074 | 0.0232 | 0.0325 |
| usable WP3 fits, full-size | product_form_group | HAZ (incl. simulated) | transition (-1.5 < x < 1.5) | 65 | 9 | False | -0.0012 | 0.108 | -0.0236 | 0.0644 | -0.1712 | -0.0531 | 0.053 | 0.1188 |
| usable WP3 fits, full-size | product_form_group | HAZ (incl. simulated) | upper shelf (x >= 1.5) | 21 | 9 | False | -0.0023 | 0.0552 | -0.0009 | 0.0423 | -0.0898 | -0.0225 | 0.0346 | 0.0796 |
| usable WP3 fits, full-size | product_form_group | forging | lower shelf (x <= -1.5) | 78 | 41 | True | 0.0105 | 0.0322 | 0.0034 | 0.0178 | -0.0217 | -0.0077 | 0.0162 | 0.0641 |
| usable WP3 fits, full-size | product_form_group | forging | transition (-1.5 < x < 1.5) | 483 | 54 | True | -0.0035 | 0.0838 | -0.007 | 0.0741 | -0.132 | -0.0527 | 0.0443 | 0.1435 |
| usable WP3 fits, full-size | product_form_group | forging | upper shelf (x >= 1.5) | 181 | 54 | True | 0.0029 | 0.0575 | -0.0025 | 0.0519 | -0.0845 | -0.0324 | 0.0364 | 0.0967 |
| usable WP3 fits, full-size | product_form_group | not determinable | lower shelf (x <= -1.5) | 20 | 5 | False | 0.0402 | 0.0555 | 0.0252 | 0.0528 | -0.0229 | 0.0024 | 0.0708 | 0.1293 |
| usable WP3 fits, full-size | product_form_group | not determinable | transition (-1.5 < x < 1.5) | 96 | 6 | False | 0.0072 | 0.1304 | 0.0045 | 0.0914 | -0.1806 | -0.0622 | 0.0609 | 0.2182 |
| usable WP3 fits, full-size | product_form_group | not determinable | upper shelf (x >= 1.5) | 35 | 6 | False | -0.0179 | 0.0565 | -0.0074 | 0.0467 | -0.1099 | -0.0405 | 0.0186 | 0.0408 |
| usable WP3 fits, full-size | product_form_group | plate | lower shelf (x <= -1.5) | 46 | 18 | True | 0.0114 | 0.0315 | 0.0075 | 0.0217 | -0.0281 | -0.0079 | 0.0194 | 0.0709 |
| usable WP3 fits, full-size | product_form_group | plate | transition (-1.5 < x < 1.5) | 479 | 34 | True | 0.0031 | 0.095 | -0.0027 | 0.09 | -0.1525 | -0.0556 | 0.0655 | 0.1545 |
| usable WP3 fits, full-size | product_form_group | plate | upper shelf (x >= 1.5) | 155 | 34 | True | -0.0069 | 0.0672 | -0.0079 | 0.058 | -0.1151 | -0.0484 | 0.0299 | 0.0872 |
| usable WP3 fits, full-size | product_form_group | weld metal | lower shelf (x <= -1.5) | 1 | 1 | False | 0.0101 |  | 0.0101 | 0 | 0.0101 | 0.0101 | 0.0101 | 0.0101 |
| usable WP3 fits, full-size | product_form_group | weld metal | transition (-1.5 < x < 1.5) | 13 | 1 | False | -0.0021 | 0.1383 | 0.011 | 0.1204 | -0.1784 | -0.0836 | 0.0725 | 0.1913 |
| usable WP3 fits, full-size | product_form_group | weld metal | upper shelf (x >= 1.5) | 3 | 1 | False | 0.0013 | 0.0935 | 0.0259 | 0.0804 | -0.0892 | -0.0381 | 0.053 | 0.0747 |
| usable WP3 fits, full-size | irradiated | False | lower shelf (x <= -1.5) | 148 | 66 | True | 0.0152 | 0.0366 | 0.0077 | 0.0227 | -0.0243 | -0.0071 | 0.0243 | 0.0844 |
| usable WP3 fits, full-size | irradiated | False | transition (-1.5 < x < 1.5) | 1008 | 90 | True | 0.0002 | 0.0959 | -0.0043 | 0.0822 | -0.1517 | -0.0555 | 0.0533 | 0.16 |
| usable WP3 fits, full-size | irradiated | False | upper shelf (x >= 1.5) | 359 | 90 | True | -0.003 | 0.06 | -0.003 | 0.0509 | -0.1023 | -0.0367 | 0.0313 | 0.0932 |
| usable WP3 fits, full-size | irradiated | True | lower shelf (x <= -1.5) | 6 | 4 | False | 0.0058 | 0.0167 | 0.0114 | 0.0142 | -0.0158 | -0.0078 | 0.0183 | 0.0214 |
| usable WP3 fits, full-size | irradiated | True | transition (-1.5 < x < 1.5) | 128 | 14 | True | 0.0013 | 0.0912 | -0.0076 | 0.0983 | -0.1485 | -0.0492 | 0.069 | 0.1461 |
| usable WP3 fits, full-size | irradiated | True | upper shelf (x >= 1.5) | 36 | 14 | True | -0.0033 | 0.0763 | -0.0063 | 0.0693 | -0.1107 | -0.0498 | 0.0398 | 0.1006 |

## 15. Figures

- `worked_example_t41j_bootstrap.png`: curve 3-17 (selection rule D-065; 19 eligible curves).
- `diagnostic_33-153_bootstrap.png`: the one full-size T41J not bracketed by measured energies.
- `t41j_uncertainty_vs_sampling.png`: pairs bootstrap SD of T41J against sampling properties, with Marini (2020) for reference.
- `published_residual_scatter.png`: residual scatter against the normalized temperature.
- `pairs_vs_fixed_design_sd.png`: the two methods compared.
