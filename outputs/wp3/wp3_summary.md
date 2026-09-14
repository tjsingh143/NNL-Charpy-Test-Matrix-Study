# WP3 summary: transition-curve fitting (q4x6v-dyt25)

Analysis of published Charpy V-notch test data (Materials Cloud 2025.30). Section 2 is SYNTHETIC fitter validation; every other section concerns the published measurements of the CP2-frozen cohorts. Decisions: DECISIONS.md D-040 to D-051.

**Method status: FINAL APPROVED at CP3 (author, 2026-09-14).** WP3 was approved in principle at the CP3 review with amendments; after reviewing the amended results the author gave final approval of D-040 to D-051, with one additional support diagnostic (D-044: empirical bracketing of 41 J by the measured energies, section 3.2). D-042 amended at CP3: the FINAL PRIMARY method fixes the lower shelf at 2.7 J for full-size specimens and fits it (>= 0 J) for miniature specimens. It replaces the pre-registered rule's outcome (LSE fitted for every geometry), which was presented at CP3 and is kept as an explicit sensitivity case (sections 2.10 and 6, `sensitivity_all_fitted_lse/`). D-046 amended: a fitted LSE at its 0 J bound is a boundary-limited fit, not a non-physical one. D-044: exact-notch-unreported full-size curves keep T41J with an explicit flag; two index-support diagnostics (index position on the fitted rise; empirical bracketing by the measured energies) and a notch-metadata sensitivity are reported; neither diagnostic is an outcome.

## 1. Method

| item | setting | decision |
| --- | --- | --- |
| model | E(T) = LSE + (USE - LSE)/2 [1 + tanh((T - T0)/C)]; solver parameters (LSE, USE - LSE, T0, C); a symmetric, empirical form that does not describe every measured transition | D-040 |
| lower shelf, FINAL PRIMARY | `geometry_specific`: full-size 55x10x10 mm LSE fixed at 2.7 J (Sokolov & Nanstad 1995 p. 7); miniature LSE fitted, >= 0 J (no fixed miniature value). CP3 amendment by the author, not the pre-registered rule's outcome | D-042 |
| lower shelf, sensitivity case | `fitted`: LSE fitted (>= 0 J) for every geometry; the pre-registered rule's outcome, presented at CP3 | D-042 |
| upper shelf | fitted asymptote LSE + (USE - LSE); supported if >= 2 specimens where the fit is >= 95.3 % of the rise (x >= 1.5); residual trend test (p < 0.05) reported as a model-adequacy flag outside the outcome | D-043 |
| index temperature, full-size 55x10x10 mm V-notch | T at 41 J, analytic; only if LSE < 41 J < USE and inside the tested range; also for full-size V-notch curves whose exact notch dimensions are unreported (flagged) | D-044 |
| index support: position on the fitted rise (not an outcome) | calculated T41J with 41 J outside the central 11.9-88.1 % of the fitted rise (x = -1...+1): flag_index_near_fitted_shelf; the value is kept | D-044 |
| index support: empirical bracketing (not an outcome; project diagnostic, not an ASTM requirement) | criterion_bracketed_by_measured_energy = min(measured energy) <= 41 J <= max(measured energy), with the measured energies below, at and above 41 J counted; a calculated T41J that is not bracketed carries flag_index_not_bracketed_by_measured_energy ("T41J calculated from fitted curve; 41 J not empirically bracketed by measured energies."); the value is kept; computed outside the outcome classification (final CP3 approval) | D-044 |
| index temperature, miniature / E23 sub-size | not calculated (no defensible criterion) | D-045 |
| optimizer | scipy.optimize.least_squares, method trf, analytic Jacobian, scaled parameters, ftol = xtol = gtol = 1e-10, max_nfev = 2000 per start | D-041 |
| weighting | ordinary (unweighted) least squares on energy | D-041 |
| starts (6, deterministic) | LSE = lowest energy (fitted LSE only); USE = mean of 3 highest; T0 in {midpoint crossing, lower quartile, upper quartile of distinct temperatures}; C in {span/12, span/4} | D-041 |
| bounds | LSE [0, highest energy] (fitted LSE only); USE - LSE [0, 10 x highest energy]; T0 [max(-273.15, T_min - span), T_max + span]; C [1 °C, span]; on a bound = active or within 0.1 % of the interval | D-041 |
| weak transition | < 2 distinct temperatures with -1 < x < 1 | D-047 |
| weak shelves | < 2 specimens with x >= 1.5 (upper) or x <= -1.5 (lower, fitted LSE only) | D-047 |
| numerically singular | Jacobian rank < number of parameters (NumPy default tolerance) | D-047 |
| outcome precedence | optimizer failure > non-physical (inadmissible) > boundary-limited > weakly identified > usable fit, index temperature unavailable > usable fit, index temperature calculated | D-046 |
| outcome groups (CP3 amendment) | non-physical (inadmissible) = no rise or T0 at absolute zero; boundary-limited = fitted LSE at its 0 J bound or a numerical-safety bound; weakly identified = weak transition, weak upper shelf, weak lower shelf (fitted LSE), rank-deficient Jacobian | D-046 |
| synthetic validation | seed 20260913; 200 replicates per scenario with scatter; scatter levels (sigma_T, cv): zero (0 °C, 0); low (2 °C, 0.03); moderate (5 °C, 0.06); high (10 °C, 0.12); Blocks A-E run with the final method and with the all-fitted sensitivity method | D-048 |
| reference scales (summaries only) | 10 °C for T41J and T0; 10 % for USE; 25 % for C | D-048 |

## 2. Fitter validation on SYNTHETIC curves (not published data)

All tables in this section come from synthetic curves with known truth (774 scenarios, 148432 fits, seed 20260913; `synthetic_*` files). Errors are fitted minus true. P90 |err| = the value 90 % of fits stay within. 'usable' = no optimizer failure, non-physical, boundary or weak-identification flag. T41J errors use the analytic crossing of every fit that returned estimates, including crossings outside the tested range that the method would not report. Reference scales (for reading, not acceptance): 10 °C for T41J and T0, 10 % for USE.

Sections 2.2-2.8 describe the FINAL PRIMARY method (117 scenarios of Blocks A-E). Every Block A-E truth is full-size (true LSE 5 J, or 2 and 10 J in Block C), so there the final method fixes LSE at 2.7 J, a deliberately imperfect value, as it would be for a real steel. The same Blocks A-E, on identical synthetic data, were also fitted with the pre-registered all-fitted method (sensitivity and history case, scenario IDs as before CP3; section 2.10 and `sensitivity_all_fitted_lse/`). The final method's miniature behaviour rests on Block L only (section 2.9). No scenario was added or changed at CP3.

### 2.1 Lower shelf (Block L): the pre-registered rule and the CP3 amendment (D-042)

| lse_strategy | score_mean_p90_c | mean_missing_share | score_full-size_c | score_miniature_c | cohort_weighted_score_c_not_used_by_rule | cohort_weight_full_size | eligible | role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fitted | 12.62 | 0.02 | 11.94 | 12.96 | 12.16 | 0.79 | True | pre-registered Block L candidate |
| fixed_convention | 11.93 | 0 | 10.13 | 12.83 | 10.7 | 0.79 | True | pre-registered Block L candidate |
| fixed_zero | 14.6 | 0 | 9.8 | 17 | 11.32 | 0.79 | True | pre-registered Block L candidate |
| hybrid | 12.06 | 0.01 | 11.66 | 12.27 | 11.79 | 0.79 | True | pre-registered Block L candidate |
| geometry_specific | 12.02 | 0 | 10.13 | 12.96 | 10.73 | 0.79 | not a rule candidate | final primary method (CP3 author decision); assembled from fixed_convention (full-size) and fitted (miniature); not a rule candidate |

Pre-registered rule outcome: `fitted` (rule 3: no strategy at least 10 % better; 'fitted' within 10 % of the lowest score).

The final method's row is assembled from the fits it reproduces exactly (full-size data sets: `fixed_convention`; miniature data sets: `fitted`); it is descriptive, not a candidate of the rule. Full-size data sets, key temperature T41J, mean P90 |error| (°C) by scatter level:

| noise | fitted | fixed_convention | fixed_zero | hybrid |
| --- | --- | --- | --- | --- |
| low | 4.67 | 3.64 | 3.77 | 3.96 |
| moderate | 10.17 | 8.25 | 7.99 | 9.82 |
| high | 20.99 | 18.5 | 17.63 | 21.21 |

The 2.7 J convention gave a lower T41J P90 than the fitted lower shelf in 42 of 45 full-size data sets (low: 14 of 15, moderate: 15 of 15, high: 13 of 15); where it did not: window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf), low scatter, true LSE 10 J (5.11 against 4.34 °C); x -0.5..3, n=12 (lower shelf missing), high scatter, true LSE 5 J (20.10 against 19.84 °C); x -0.5..3, n=12 (lower shelf missing), high scatter, true LSE 10 J (25.15 against 21.97 °C).

### 2.2 Specimen count and scatter (Block A, final method: uniform over x = -3...3; truth LSE 5 J, USE 150 J, T0 0 °C, C 30 °C)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform x -3..3, n=6 | zero | 1 | 0.4 | 0.7 | 0 % | 4 % | 100 % | 0.4 | 0 % |
| uniform x -3..3, n=6 | low | 200 | 4.5 | 5.3 | 5 % | 24 % | 82 % | 4.5 | 4 % |
| uniform x -3..3, n=6 | moderate | 200 | 9.8 | 11.4 | 9 % | 54 % | 48 % | 7.7 | 7 % |
| uniform x -3..3, n=6 | high | 200 | 22.7 | 21.8 | 21 % | 97 % | 20 % | 12.5 | 13 % |
| uniform x -3..3, n=8 | zero | 1 | 0.4 | 0.6 | 0 % | 4 % | 100 % | 0.4 | 0 % |
| uniform x -3..3, n=8 | low | 200 | 3.7 | 4.7 | 4 % | 21 % | 99 % | 3.7 | 4 % |
| uniform x -3..3, n=8 | moderate | 200 | 8.6 | 9.9 | 9 % | 48 % | 80 % | 8.1 | 7 % |
| uniform x -3..3, n=8 | high | 200 | 18 | 16.9 | 20 % | 97 % | 40 % | 12.8 | 14 % |
| uniform x -3..3, n=12 | zero | 1 | 0.4 | 0.6 | 0 % | 5 % | 100 % | 0.4 | 0 % |
| uniform x -3..3, n=12 | low | 200 | 3.1 | 3.5 | 4 % | 18 % | 100 % | 3.1 | 4 % |
| uniform x -3..3, n=12 | moderate | 200 | 8 | 7.4 | 8 % | 35 % | 97 % | 8 | 8 % |
| uniform x -3..3, n=12 | high | 200 | 16.3 | 16.3 | 15 % | 96 % | 71 % | 13.3 | 11 % |
| uniform x -3..3, n=18 | zero | 1 | 0.4 | 0.6 | 0 % | 5 % | 100 % | 0.4 | 0 % |
| uniform x -3..3, n=18 | low | 200 | 2.8 | 3.3 | 3 % | 16 % | 100 % | 2.8 | 3 % |
| uniform x -3..3, n=18 | moderate | 200 | 5.9 | 6.4 | 6 % | 32 % | 100 % | 5.9 | 6 % |
| uniform x -3..3, n=18 | high | 200 | 13 | 14.1 | 14 % | 77 % | 84 % | 12 | 12 % |
| uniform x -3..3, n=30 | zero | 1 | 0.4 | 0.5 | 0 % | 5 % | 100 % | 0.4 | 0 % |
| uniform x -3..3, n=30 | low | 200 | 2.1 | 2.4 | 3 % | 12 % | 100 % | 2.1 | 3 % |
| uniform x -3..3, n=30 | moderate | 200 | 4.3 | 5.3 | 5 % | 25 % | 100 % | 4.3 | 5 % |
| uniform x -3..3, n=30 | high | 200 | 8.4 | 9.7 | 10 % | 53 % | 96 % | 8.3 | 10 % |

### 2.3 Sampling patterns (Block B, final method)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shelves only, 0 transition points (n=6) | zero | 1 | 11.1 | 7.9 | 0 % | 26 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | low | 200 | 23.7 | 26.6 | 6 % | 67 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | moderate | 200 | 31.2 | 39.1 | 13 % | 97 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | high | 200 | 90.1 | 74.3 | 23 % | 112 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | zero | 1 | 5.2 | 0.3 | 1 % | 35 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | low | 200 | 13.8 | 6.8 | 4 % | 81 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | moderate | 200 | 16.2 | 16.1 | 9 % | 97 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | high | 200 | 29.1 | 48.9 | 20 % | 108 % | 0 % |  |  |
| shelves + 2 transition points (n=8) | zero | 1 | 0.2 | 0.6 | 0 % | 3 % | 100 % | 0.2 | 0 % |
| shelves + 2 transition points (n=8) | low | 200 | 4.6 | 4.7 | 3 % | 28 % | 100 % | 4.6 | 3 % |
| shelves + 2 transition points (n=8) | moderate | 200 | 11.2 | 10.9 | 8 % | 72 % | 80 % | 10.5 | 7 % |
| shelves + 2 transition points (n=8) | high | 200 | 22.4 | 22.9 | 17 % | 103 % | 37 % | 15.7 | 13 % |
| shelves + 3 transition points (n=9) | zero | 1 | 0.2 | 0.6 | 0 % | 3 % | 100 % | 0.2 | 0 % |
| shelves + 3 transition points (n=9) | low | 200 | 4.5 | 3.8 | 3 % | 23 % | 100 % | 4.5 | 3 % |
| shelves + 3 transition points (n=9) | moderate | 200 | 9.8 | 9.1 | 7 % | 48 % | 90 % | 9.5 | 7 % |
| shelves + 3 transition points (n=9) | high | 200 | 20 | 20.6 | 16 % | 107 % | 56 % | 17.5 | 13 % |
| x -1.5..3, n=12 (lower shelf weak) | zero | 1 | 0.2 | 0.6 | 0 % | 3 % | 100 % | 0.2 | 0 % |
| x -1.5..3, n=12 (lower shelf weak) | low | 200 | 2.7 | 2.8 | 3 % | 16 % | 100 % | 2.7 | 3 % |
| x -1.5..3, n=12 (lower shelf weak) | moderate | 200 | 6.7 | 7.1 | 6 % | 35 % | 100 % | 6.7 | 6 % |
| x -1.5..3, n=12 (lower shelf weak) | high | 200 | 14.2 | 14.5 | 16 % | 97 % | 75 % | 12 | 13 % |
| x -0.5..3, n=12 (lower shelf missing) | zero | 1 | 0.2 | 0.5 | 0 % | 2 % | 100 % |  | 0 % |
| x -0.5..3, n=12 (lower shelf missing) | low | 200 | 3.7 | 2.7 | 3 % | 16 % | 100 % | 4.3 | 3 % |
| x -0.5..3, n=12 (lower shelf missing) | moderate | 200 | 10.6 | 6.9 | 7 % | 46 % | 96 % | 8.4 | 6 % |
| x -0.5..3, n=12 (lower shelf missing) | high | 200 | 20.1 | 12.1 | 14 % | 97 % | 80 % | 15.1 | 11 % |
| x -3..1.5, n=12 (upper shelf weak) | zero | 1 | 0.5 | 0.1 | 1 % | 7 % | 0 % |  |  |
| x -3..1.5, n=12 (upper shelf weak) | low | 200 | 2.7 | 5.5 | 10 % | 24 % | 2 % | 3.3 | 9 % |
| x -3..1.5, n=12 (upper shelf weak) | moderate | 200 | 6.4 | 11.4 | 20 % | 44 % | 24 % | 7.9 | 12 % |
| x -3..1.5, n=12 (upper shelf weak) | high | 200 | 13.1 | 33.9 | 83 % | 97 % | 26 % | 11.7 | 20 % |
| x -3..0.5, n=12 (upper shelf missing) | zero | 1 | 0.4 | 3.3 | 11 % | 14 % | 0 % |  |  |
| x -3..0.5, n=12 (upper shelf missing) | low | 200 | 2.7 | 23.3 | 84 % | 41 % | 0 % |  |  |
| x -3..0.5, n=12 (upper shelf missing) | moderate | 200 | 6.3 | 63.7 | 686 % | 62 % | 2 % | 5.5 | 41 % |
| x -3..0.5, n=12 (upper shelf missing) | high | 200 | 11.9 | 64.6 | 902 % | 97 % | 10 % | 12.1 | 59 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | zero | 1 | 0.1 | 0.5 | 0 % | 2 % | 100 % | 0.1 | 0 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | low | 200 | 3.3 | 2.8 | 4 % | 23 % | 100 % | 3.3 | 4 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | moderate | 200 | 9.7 | 6.1 | 8 % | 58 % | 96 % | 8.8 | 8 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | high | 200 | 15.7 | 14.4 | 22 % | 108 % | 86 % | 14.6 | 17 % |
| clustered cold side: x -3..-0.5, n=12 | zero | 1 | 0.3 | 30.3 | 195 % | 32 % | 0 % |  |  |
| clustered cold side: x -3..-0.5, n=12 | low | 200 | 4.5 | 34.9 | 241 % | 46 % | 0 % |  |  |
| clustered cold side: x -3..-0.5, n=12 | moderate | 200 | 9.8 | 41.2 | 293 % | 62 % | 1 % |  | 79 % |
| clustered cold side: x -3..-0.5, n=12 | high | 200 | 16.1 | 49.1 | 397 % | 97 % | 8 % | 15.2 | 89 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | zero | 1 | 0.3 | 0.5 | 0 % | 4 % | 100 % | 0.3 | 0 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | low | 200 | 2.6 | 2.8 | 3 % | 13 % | 88 % | 2.6 | 3 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | moderate | 200 | 5.8 | 6.8 | 7 % | 29 % | 77 % | 5.8 | 7 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | high | 200 | 12 | 14 | 15 % | 57 % | 56 % | 10.7 | 14 % |

### 2.4 Parameter values (Block C, final method, moderate scatter)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| USE 44 J (41 J near upper shelf); uniform x -3..3, n=12 | moderate | 200 | 20.6 | 11 | 10 % | 60 % | 86 % | 19.3 | 8 % |
| USE 44 J (41 J near upper shelf); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 16.6 | 8.3 | 9 % | 43 % | 85 % | 15.8 | 8 % |
| USE 70 J; uniform x -3..3, n=12 | moderate | 200 | 7.7 | 8 | 8 % | 46 % | 92 % | 7.2 | 7 % |
| USE 70 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 6.6 | 7.3 | 8 % | 33 % | 82 % | 6.8 | 9 % |
| USE 250 J; uniform x -3..3, n=12 | moderate | 200 | 10.4 | 8.2 | 8 % | 39 % | 96 % | 9.9 | 8 % |
| USE 250 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 6.8 | 6.4 | 6 % | 27 % | 74 % | 6.4 | 6 % |
| LSE 2 J; uniform x -3..3, n=12 | moderate | 200 | 6.9 | 7.2 | 6 % | 33 % | 98 % | 6.9 | 6 % |
| LSE 2 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 5.8 | 6.3 | 7 % | 26 % | 62 % | 5.9 | 7 % |
| LSE 10 J; uniform x -3..3, n=12 | moderate | 200 | 8.3 | 9.3 | 8 % | 50 % | 93 % | 8.3 | 7 % |
| LSE 10 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 6.4 | 7.8 | 8 % | 37 % | 86 % | 5.8 | 8 % |
| C 12 °C (narrow); uniform x -3..3, n=12 | moderate | 200 | 7.3 | 6.4 | 10 % | 83 % | 74 % | 5.5 | 8 % |
| C 12 °C (narrow); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 4.6 | 5 | 8 % | 46 % | 66 % | 4.5 | 8 % |
| C 60 °C (broad); uniform x -3..3, n=12 | moderate | 200 | 10.6 | 11.8 | 7 % | 28 % | 99 % | 10.7 | 7 % |
| C 60 °C (broad); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 8 | 10.1 | 7 % | 24 % | 80 % | 7.1 | 7 % |

### 2.5 Fixed test windows planned without knowing T0 (Block D, final method, moderate scatter)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 9.8 | 8.1 | 5 % | 92 % | 20 % | 6.7 | 4 % |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 13 | 8.5 | 5 % | 55 % | 99 % | 12.5 | 5 % |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 19.5 | 11.4 | 9 % | 48 % | 82 % | 24.1 | 7 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 8.5 | 9 | 6 % | 92 % | 16 % | 6.7 | 7 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 7.8 | 9.3 | 10 % | 39 % | 73 % | 7.6 | 9 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 7.9 | 21.9 | 23 % | 36 % | 6 % | 10.8 | 18 % |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 12.4 | 33.4 | 798 % | 92 % | 0 % |  |  |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 7.6 | 69.7 | 703 % | 69 % | 0 % |  |  |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 9.1 | 107.7 | 615 % | 45 % | 0 % | 8.4 | 56 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 9.6 | 9.8 | 4 % | 92 % | 7 % | 8 | 4 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 9.3 | 9.2 | 5 % | 36 % | 98 % | 8.9 | 5 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 8.6 | 10.8 | 6 % | 25 % | 100 % | 8.6 | 6 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 9.4 | 10.5 | 5 % | 92 % | 27 % | 6.2 | 5 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 8.9 | 9.1 | 6 % | 43 % | 96 % | 8.9 | 6 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 7.8 | 11.4 | 9 % | 27 % | 72 % | 7.3 | 8 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 8.1 | 7.9 | 7 % | 92 % | 10 % | 6.9 | 6 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 9.2 | 11.2 | 12 % | 45 % | 42 % | 7.5 | 10 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 7.8 | 27.4 | 34 % | 41 % | 4 % | 9 | 24 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 10.3 | 7.7 | 3 % | 91 % | 48 % | 5.5 | 3 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 7.1 | 6.6 | 3 % | 41 % | 100 % | 7.1 | 3 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 6.6 | 7.1 | 3 % | 19 % | 100 % | 6.6 | 3 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 7.8 | 7.4 | 4 % | 92 % | 45 % | 6.9 | 3 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 7.3 | 6.4 | 4 % | 31 % | 100 % | 7.3 | 4 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 6.7 | 8.3 | 5 % | 20 % | 100 % | 6.7 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 8.5 | 7.3 | 5 % | 92 % | 41 % | 5.9 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 7 | 7.2 | 5 % | 34 % | 100 % | 6.8 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 6.4 | 10.9 | 9 % | 25 % | 68 % | 6.6 | 6 % |

### 2.6 What the outcome categories and flags mean (Blocks A-D with scatter, final method)

| outcome | fits | share | T0 P90 \|err\| °C | T41J P90 \|err\| °C | USE P90 \|err\| |
| --- | --- | --- | --- | --- | --- |
| optimizer failure | 0 | 0 % |  |  |  |
| non-physical (inadmissible) | 0 | 0 % |  |  |  |
| boundary-limited | 1250 | 7 % | 73.5 | 23.8 | 697 % |
| weakly identified | 5682 | 32 % | 26.8 | 16.4 | 36 % |
| usable fit, index temperature unavailable | 618 | 3 % | 9.4 | 12.8 | 8 % |
| usable fit, index temperature calculated | 10250 | 58 % | 8.4 | 8.4 | 7 % |
| all usable outcomes | 10868 | 61 % | 8.5 | 8.7 | 7 % |
| all fits with estimates | 17800 | 100 % | 17.5 | 11.6 | 19 % |

Fits carrying exactly one fit flag, against fits carrying none (flags overlap, so this is the clean comparison). With LSE fixed, the lower-shelf diagnostics cannot fire here; section 2.10 shows them for the fitted lower shelf:

| fits carrying | fits | T0 P90 \|err\| °C | T41J P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| |
| --- | --- | --- | --- | --- | --- |
| no flag | 10516 | 8.4 | 8.7 | 7 % | 40 % |
| only optimizer_failure | 0 |  |  |  |  |
| only nonphysical_no_rise | 0 |  |  |  |  |
| only nonphysical_t0_at_absolute_zero | 0 |  |  |  |  |
| only lse_at_lower_bound | 0 |  |  |  |  |
| only boundary_c_min | 0 |  |  |  |  |
| only boundary_c_max | 0 |  |  |  |  |
| only boundary_t0_limit | 0 |  |  |  |  |
| only boundary_rise_max | 0 |  |  |  |  |
| only boundary_lse_max | 0 |  |  |  |  |
| only weak_transition | 2582 | 21.4 | 21.4 | 8 % | 76 % |
| only weak_upper_shelf | 2736 | 31.3 | 10.9 | 58 % | 86 % |
| only nonflat_upper_shelf | 352 | 9.4 | 8.5 | 7 % | 44 % |
| only weak_lower_shelf | 0 |  |  |  |  |
| only numerically_singular | 0 |  |  |  |  |
| two or more flags | 1614 | 71.3 | 20.6 | 638 % | 97 % |

Index-support diagnostic (D-044): usable fits with a calculated T41J, by where 41 J lies on the fitted rise:

| usable fits with a calculated T41J | fits | T41J median \|err\| °C | T41J P90 \|err\| °C | share beyond 10 °C |
| --- | --- | --- | --- | --- |
| usable fit with T41J: 41 J inside the central 11.9-88.1 % of the fitted rise | 10006 | 2.7 | 8.1 | 6 % |
| usable fit with T41J: 41 J outside it (flag_index_near_fitted_shelf) | 244 | 7.7 | 19.2 | 37 % |

Audit diagnostics (recorded, not used to classify):

| audit diagnostic | fits | T0 P90 \|err\| °C | T41J P90 \|err\| °C |
| --- | --- | --- | --- |
| Jacobian condition number Q1 (lowest) | 4450 | 8.8 | 9.1 |
| Jacobian condition number Q2 | 4450 | 8.4 | 7.7 |
| Jacobian condition number Q3 | 4450 | 11.3 | 10.2 |
| Jacobian condition number Q4 (highest) | 4450 | 42 | 21.4 |
| starts within 1 % of best cost disagree on T0 by > 1 °C | 112 | 32.6 | 33.5 |
| starts within 1 % of best cost agree on T0 within 1 °C | 17688 | 17.5 | 11.4 |
| usable fit with T41J: no specimen energy below 41 J | 78 | 5.3 | 5.5 |
| usable fit with T41J: at least one specimen energy below 41 J | 10172 | 8.4 | 8.5 |

### 2.7 Upper shelves that are not flat (Block E, final method; added after Blocks A-D, D-047, D-051)

| design | noise | shelf_slope_fraction_of_use_per_100c | fits | share_trend_test_applicable | share_trend_flagged | share_trend_flagged_when_applicable | share_usable | use_error_rel_median | use_error_rel_p90_abs | t41_error_p90_abs_c | t0_error_p90_abs_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| upper shelf -20 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | -0.2 | 200 | 100 % | 88 % | 88 % | 98 % | -11 % | 13 % | 3.9 | 8.1 |
| upper shelf -20 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | -0.2 | 200 | 100 % | 38 % | 38 % | 84 % | -11 % | 14 % | 9.7 | 11.9 |
| upper shelf -20 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | -0.2 | 200 | 100 % | 88 % | 88 % | 93 % | -9 % | 11 % | 2 | 5.7 |
| upper shelf -20 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | -0.2 | 200 | 98 % | 46 % | 47 % | 68 % | -9 % | 13 % | 5.5 | 9.5 |
| upper shelf -10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | -0.1 | 200 | 100 % | 38 % | 38 % | 100 % | -6 % | 7 % | 3.6 | 6 |
| upper shelf -10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | -0.1 | 200 | 100 % | 12 % | 12 % | 87 % | -6 % | 9 % | 9.5 | 9.3 |
| upper shelf -10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | -0.1 | 200 | 100 % | 31 % | 31 % | 83 % | -5 % | 7 % | 2.5 | 4.6 |
| upper shelf -10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | -0.1 | 200 | 94 % | 13 % | 14 % | 68 % | -5 % | 8 % | 5 | 6.9 |
| upper shelf +10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | 0.1 | 200 | 100 % | 11 % | 11 % | 100 % | 7 % | 9 % | 3.8 | 5.3 |
| upper shelf +10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | 0.1 | 200 | 100 % | 10 % | 10 % | 98 % | 6 % | 11 % | 9.3 | 9.7 |
| upper shelf +10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | 0.1 | 200 | 69 % | 11 % | 16 % | 95 % | 6 % | 8 % | 2.7 | 5.3 |
| upper shelf +10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | 0.1 | 200 | 62 % | 6 % | 9 % | 68 % | 7 % | 11 % | 5.2 | 10.8 |

### 2.8 Where the fitter stops being trustworthy (final method)

Of 89 scenarios with scatter in Blocks A-D: in 41, 90 % of all fits recover T41J, T0 and USE within the reference scales (10 °C, 10 °C, 10 %). In 9 more, only the fits that pass the flags do. In 14, fewer than 5 % of fits pass the flags: the method declines to report, which is the intended behaviour. In 25, 5 % or more of fits pass the flags yet the passing fits still miss at least one reference scale; these are where the fitter stops being trustworthy even with its diagnostics:

| scenario (design, [scatter]) | usable | T41J P90 all / usable °C | T0 P90 all / usable °C | USE P90 all / usable |
| --- | --- | --- | --- | --- |
| uniform x -3..3, n=12 [high] | 71 % | 16.3 / 13.3 | 16.3 / 13.4 | 15 % / 11 % |
| uniform x -3..3, n=18 [high] | 84 % | 13.0 / 12.0 | 14.1 / 11.6 | 14 % / 12 % |
| uniform x -3..3, n=6 [high] | 20 % | 22.7 / 12.5 | 21.8 / 9.7 | 21 % / 13 % |
| uniform x -3..3, n=8 [high] | 40 % | 18.0 / 12.8 | 16.9 / 13.0 | 20 % / 14 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) [high] | 56 % | 12.0 / 10.7 | 14.0 / 13.4 | 15 % / 14 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) [high] | 86 % | 15.7 / 14.6 | 14.4 / 11.4 | 22 % / 17 % |
| clustered cold side: x -3..-0.5, n=12 [high] | 8 % | 16.1 / 15.2 | 49.1 / 61.0 | 397 % / 89 % |
| shelves + 2 transition points (n=8) [high] | 37 % | 22.4 / 15.7 | 22.9 / 14.1 | 17 % / 13 % |
| shelves + 2 transition points (n=8) [moderate] | 80 % | 11.2 / 10.5 | 10.9 / 9.1 | 8 % / 7 % |
| shelves + 3 transition points (n=9) [high] | 56 % | 20.0 / 17.5 | 20.6 / 14.5 | 16 % / 13 % |
| x -0.5..3, n=12 (lower shelf missing) [high] | 80 % | 20.1 / 15.1 | 12.1 / 11.3 | 14 % / 11 % |
| x -1.5..3, n=12 (lower shelf weak) [high] | 75 % | 14.2 / 12.0 | 14.5 / 13.0 | 16 % / 13 % |
| x -3..0.5, n=12 (upper shelf missing) [high] | 10 % | 11.9 / 12.1 | 64.6 / 31.7 | 902 % / 59 % |
| x -3..1.5, n=12 (upper shelf weak) [high] | 26 % | 13.1 / 11.7 | 33.9 / 14.5 | 83 % / 20 % |
| x -3..1.5, n=12 (upper shelf weak) [moderate] | 24 % | 6.4 / 7.9 | 11.4 / 10.2 | 20 % / 12 % |
| C 60 °C (broad); 5 temperatures x 3 specimens (n=15) [moderate] | 80 % | 8.0 / 7.1 | 10.1 / 10.9 | 7 % / 7 % |
| C 60 °C (broad); uniform x -3..3, n=12 [moderate] | 99 % | 10.6 / 10.7 | 11.8 / 11.7 | 7 % / 7 % |
| USE 44 J (41 J near upper shelf); 5 temperatures x 3 specimens (n=15) [moderate] | 85 % | 16.6 / 15.8 | 8.3 / 8.1 | 9 % / 8 % |
| USE 44 J (41 J near upper shelf); uniform x -3..3, n=12 [moderate] | 86 % | 20.6 / 19.3 | 11.0 / 9.4 | 10 % / 8 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 60 °C [moderate] | 6 % | 7.9 / 10.8 | 21.9 / 20.7 | 23 % / 18 % |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 30 °C [moderate] | 99 % | 13.0 / 12.5 | 8.5 / 8.5 | 5 % / 5 % |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 60 °C [moderate] | 82 % | 19.5 / 24.1 | 11.4 / 10.7 | 9 % / 7 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 60 °C [moderate] | 72 % | 7.8 / 7.3 | 11.4 / 11.1 | 9 % / 8 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 30 °C [moderate] | 42 % | 9.2 / 7.5 | 11.2 / 12.2 | 12 % / 10 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 60 °C [moderate] | 100 % | 8.6 / 8.6 | 10.8 / 10.8 | 6 % / 6 % |

Scenarios in which the method declines (fewer than 5 % of fits pass):

| scenario (design, [scatter]) | usable | T41J P90 all / usable °C | T0 P90 all / usable °C | USE P90 all / usable |
| --- | --- | --- | --- | --- |
| clustered cold side: x -3..-0.5, n=12 [low] | 0 % | 4.5 / – | 34.9 / – | 241 % / – |
| clustered cold side: x -3..-0.5, n=12 [moderate] | 1 % | 9.8 / – | 41.2 / 40.9 | 293 % / 79 % |
| shelves + 1 transition point (n=7) [high] | 0 % | 29.1 / – | 48.9 / – | 20 % / – |
| shelves + 1 transition point (n=7) [low] | 0 % | 13.8 / – | 6.8 / – | 4 % / – |
| shelves + 1 transition point (n=7) [moderate] | 0 % | 16.2 / – | 16.1 / – | 9 % / – |
| shelves only, 0 transition points (n=6) [high] | 0 % | 90.1 / – | 74.3 / – | 23 % / – |
| shelves only, 0 transition points (n=6) [low] | 0 % | 23.7 / – | 26.6 / – | 6 % / – |
| shelves only, 0 transition points (n=6) [moderate] | 0 % | 31.2 / – | 39.1 / – | 13 % / – |
| x -3..0.5, n=12 (upper shelf missing) [low] | 0 % | 2.7 / – | 23.3 / – | 84 % / – |
| x -3..0.5, n=12 (upper shelf missing) [moderate] | 2 % | 6.3 / 5.5 | 63.7 / 19.7 | 686 % / 41 % |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 12 °C [moderate] | 0 % | 12.4 / – | 33.4 / – | 798 % / – |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 30 °C [moderate] | 0 % | 7.6 / – | 69.7 / – | 703 % / – |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 60 °C [moderate] | 0 % | 9.1 / 8.4 | 107.7 / 48.0 | 615 % / 56 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 60 °C [moderate] | 4 % | 7.8 / 9.0 | 27.4 / 27.9 | 34 % / 24 % |

### 2.9 Block L under the final method: the only miniature evidence (and full-size with LSE fixed)

Miniature truths (final method = fitted LSE): means over the truths of each design and scatter level. No index exists for these specimens (D-045), so T0 and USE are judged:

| design (miniature truths, USE 1 or 8 J; LSE 1, 6, 12 % of USE) | scatter | truths | usable | LSE at 0 J bound | weak lower shelf | T0 P90 all °C (mean / worst truth) | T0 P90 usable °C | USE P90 all / usable | truths whose usable fits meet the references |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform x -3..3, n=12 (lower shelf well sampled) | low | 6 | 95 % | 5 % | 0 % | 4.0 / 4.7 | 3.9 | 4 % / 4 % | 6 |
| uniform x -3..3, n=12 (lower shelf well sampled) | moderate | 6 | 80 % | 11 % | 2 % | 9.1 / 11.1 | 8.6 | 8 % / 8 % | 5 |
| uniform x -3..3, n=12 (lower shelf well sampled) | high | 6 | 44 % | 17 % | 9 % | 19.7 / 23.8 | 15.4 | 18 % / 14 % | 0 |
| x -1.5..3, n=12 (lower shelf weak) | low | 6 | 6 % | 18 % | 94 % | 4.3 / 5.5 | 5.4 | 4 % / 3 % | 6 |
| x -1.5..3, n=12 (lower shelf weak) | moderate | 6 | 27 % | 27 % | 69 % | 8.7 / 10.6 | 9.3 | 8 % / 7 % | 4 |
| x -1.5..3, n=12 (lower shelf weak) | high | 6 | 21 % | 29 % | 46 % | 18.2 / 21.6 | 18.5 | 16 % / 12 % | 0 |
| x -0.5..3, n=12 (lower shelf missing) | low | 6 | 0 % | 40 % | 99 % | 9.2 / 10.7 | 15.2 | 3 % / 3 % | 0 |
| x -0.5..3, n=12 (lower shelf missing) | moderate | 6 | 7 % | 37 % | 80 % | 15.9 / 18.5 | 23.5 | 7 % / 6 % | 0 |
| x -0.5..3, n=12 (lower shelf missing) | high | 6 | 8 % | 27 % | 51 % | 28.0 / 33.1 | 31.5 | 13 % / 10 % | 0 |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | low | 6 | 36 % | 0 % | 0 % | 5.2 / 6.1 | 5.1 | 6 % / 5 % | 6 |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | moderate | 6 | 36 % | 2 % | 0 % | 12.2 / 14.7 | 11.5 | 13 % / 10 % | 1 |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | high | 6 | 21 % | 5 % | 0 % | 25.6 / 31.5 | 17.0 | 30 % / 18 % | 0 |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | low | 6 | 37 % | 9 % | 61 % | 4.5 / 5.4 | 4.8 | 2 % / 2 % | 6 |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | moderate | 6 | 33 % | 17 % | 49 % | 9.9 / 12.5 | 10.9 | 5 % / 5 % | 3 |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | high | 6 | 22 % | 22 % | 37 % | 19.9 / 24.0 | 19.9 | 10 % / 10 % | 0 |

Full-size truths (final method = LSE fixed at 2.7 J; true LSE 2, 5 or 10 J):

| design (full-size truths, LSE 2, 5, 10 J; USE 150 J) | scatter | truths | usable | T41J P90 all / usable °C | T0 P90 all °C | USE P90 all |
| --- | --- | --- | --- | --- | --- | --- |
| uniform x -3..3, n=12 (lower shelf well sampled) | low | 3 | 100 % | 3.2 / 3.2 | 4.1 | 4 % |
| uniform x -3..3, n=12 (lower shelf well sampled) | moderate | 3 | 94 % | 7.3 / 7.1 | 8.0 | 8 % |
| uniform x -3..3, n=12 (lower shelf well sampled) | high | 3 | 67 % | 17.4 / 13.9 | 16.9 | 17 % |
| x -1.5..3, n=12 (lower shelf weak) | low | 3 | 100 % | 2.7 / 2.7 | 3.5 | 3 % |
| x -1.5..3, n=12 (lower shelf weak) | moderate | 3 | 99 % | 6.8 / 6.7 | 6.9 | 7 % |
| x -1.5..3, n=12 (lower shelf weak) | high | 3 | 78 % | 16.4 / 11.9 | 14.9 | 16 % |
| x -0.5..3, n=12 (lower shelf missing) | low | 3 | 100 % | 4.1 / 4.6 | 3.3 | 3 % |
| x -0.5..3, n=12 (lower shelf missing) | moderate | 3 | 99 % | 9.0 / 8.7 | 6.7 | 7 % |
| x -0.5..3, n=12 (lower shelf missing) | high | 3 | 76 % | 21.5 / 15.0 | 14.2 | 15 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | low | 3 | 28 % | 4.1 / 3.7 | 5.2 | 7 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | moderate | 3 | 31 % | 9.3 / 8.9 | 11.0 | 13 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf) | high | 3 | 25 % | 17.7 / 14.6 | 24.0 | 34 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | low | 3 | 100 % | 4.0 / 4.0 | 4.1 | 2 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | moderate | 3 | 94 % | 8.9 / 7.6 | 8.2 | 4 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition) | high | 3 | 73 % | 19.5 / 14.3 | 15.9 | 9 % |

Trust classes per Block L data set under the final method (T41J judged for full-size truths only):

| class | full-size data sets, final method (LSE 2.7 J) | full-size data sets, all fitted (sensitivity) | miniature data sets (LSE fitted under both) |
| --- | --- | --- | --- |
| within reference (all fits) | 26 | 19 | 41 |
| within reference only after the flags | 1 | 3 | 2 |
| method declines (< 5 % usable) | 0 | 3 | 3 |
| usable fits still miss a reference scale | 18 | 20 | 44 |

Miniature data sets whose usable fits still miss a reference scale (the diagnostics do not protect these):

| scenario (design, [scatter]) | usable | T0 P90 all / usable °C | USE P90 all / usable |
| --- | --- | --- | --- |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 1 J, LSE 1 % of USE [high] | 40 % | 14.1 / 13.9 | 15 % / 12 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 1 J, LSE 12 % of USE [high] | 40 % | 21.9 / 16.1 | 21 % / 15 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 1 J, LSE 6 % of USE [high] | 53 % | 23.8 / 17.9 | 18 % / 14 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 8 J, LSE 1 % of USE [high] | 48 % | 14.3 / 13.8 | 12 % / 12 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 8 J, LSE 12 % of USE [high] | 40 % | 22.0 / 17.0 | 22 % / 15 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 8 J, LSE 12 % of USE [moderate] | 86 % | 11.1 / 10.7 | 10 % / 9 % |
| uniform x -3..3, n=12 (lower shelf well sampled); USE 8 J, LSE 6 % of USE [high] | 46 % | 21.8 / 13.8 | 19 % / 14 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 1 J, LSE 1 % of USE [high] | 28 % | 20.7 / 15.6 | 23 % / 18 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 1 J, LSE 12 % of USE [high] | 18 % | 31.5 / 22.0 | 36 % / 21 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 1 J, LSE 12 % of USE [moderate] | 31 % | 14.7 / 12.5 | 16 % / 13 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 1 J, LSE 6 % of USE [high] | 19 % | 25.8 / 17.0 | 36 % / 13 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 1 J, LSE 6 % of USE [moderate] | 30 % | 11.8 / 11.8 | 13 % / 10 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 1 % of USE [high] | 23 % | 24.6 / 12.9 | 25 % / 15 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 1 % of USE [moderate] | 37 % | 9.6 / 10.7 | 11 % / 9 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 12 % of USE [high] | 14 % | 25.7 / 18.5 | 31 % / 24 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 12 % of USE [moderate] | 34 % | 14.6 / 12.4 | 16 % / 11 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 6 % of USE [high] | 23 % | 25.4 / 16.2 | 30 % / 19 % |
| window 250 °C, n=12, T0 60 °C above centre (cold end deep in lower shelf); USE 8 J, LSE 6 % of USE [moderate] | 40 % | 12.2 / 11.6 | 12 % / 10 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 1 J, LSE 1 % of USE [high] | 28 % | 17.9 / 17.4 | 9 % / 8 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 1 J, LSE 12 % of USE [high] | 20 % | 24.0 / 24.7 | 11 % / 11 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 1 J, LSE 12 % of USE [moderate] | 25 % | 11.2 / 12.7 | 6 % / 6 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 1 J, LSE 6 % of USE [high] | 23 % | 19.3 / 19.6 | 10 % / 8 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 8 J, LSE 1 % of USE [high] | 25 % | 17.2 / 17.2 | 8 % / 9 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 8 J, LSE 12 % of USE [high] | 22 % | 21.8 / 22.5 | 14 % / 14 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 8 J, LSE 12 % of USE [moderate] | 28 % | 12.5 / 13.6 | 6 % / 6 % |
| window 250 °C, n=12, T0 60 °C below centre (cold end near transition); USE 8 J, LSE 6 % of USE [high] | 17 % | 19.3 / 17.7 | 9 % / 8 % |
| x -0.5..3, n=12 (lower shelf missing); USE 1 J, LSE 1 % of USE [high] | 10 % | 27.9 / 32.6 | 12 % / 11 % |
| x -0.5..3, n=12 (lower shelf missing); USE 1 J, LSE 12 % of USE [high] | 6 % | 33.1 / 28.1 | 14 % / 7 % |
| x -0.5..3, n=12 (lower shelf missing); USE 1 J, LSE 12 % of USE [moderate] | 6 % | 18.5 / 22.5 | 7 % / 6 % |
| x -0.5..3, n=12 (lower shelf missing); USE 1 J, LSE 6 % of USE [high] | 10 % | 28.8 / 35.0 | 12 % / 8 % |
| x -0.5..3, n=12 (lower shelf missing); USE 1 J, LSE 6 % of USE [moderate] | 6 % | 15.5 / 24.4 | 7 % / 6 % |
| x -0.5..3, n=12 (lower shelf missing); USE 8 J, LSE 1 % of USE [high] | 8 % | 21.4 / 29.4 | 11 % / 7 % |
| x -0.5..3, n=12 (lower shelf missing); USE 8 J, LSE 1 % of USE [moderate] | 9 % | 15.1 / 21.3 | 6 % / 6 % |
| x -0.5..3, n=12 (lower shelf missing); USE 8 J, LSE 12 % of USE [moderate] | 6 % | 16.1 / 27.1 | 8 % / 5 % |
| x -0.5..3, n=12 (lower shelf missing); USE 8 J, LSE 6 % of USE [high] | 8 % | 27.0 / 31.1 | 12 % / 12 % |
| x -0.5..3, n=12 (lower shelf missing); USE 8 J, LSE 6 % of USE [moderate] | 10 % | 16.1 / 23.4 | 7 % / 5 % |
| x -1.5..3, n=12 (lower shelf weak); USE 1 J, LSE 1 % of USE [high] | 24 % | 16.2 / 16.8 | 12 % / 11 % |
| x -1.5..3, n=12 (lower shelf weak); USE 1 J, LSE 12 % of USE [high] | 16 % | 21.6 / 22.0 | 19 % / 14 % |
| x -1.5..3, n=12 (lower shelf weak); USE 1 J, LSE 12 % of USE [moderate] | 32 % | 10.5 / 10.6 | 9 % / 7 % |
| x -1.5..3, n=12 (lower shelf weak); USE 1 J, LSE 6 % of USE [high] | 20 % | 16.3 / 15.9 | 14 % / 12 % |
| x -1.5..3, n=12 (lower shelf weak); USE 8 J, LSE 1 % of USE [high] | 23 % | 17.0 / 17.2 | 15 % / 9 % |
| x -1.5..3, n=12 (lower shelf weak); USE 8 J, LSE 12 % of USE [high] | 20 % | 21.4 / 22.6 | 20 % / 12 % |
| x -1.5..3, n=12 (lower shelf weak); USE 8 J, LSE 12 % of USE [moderate] | 30 % | 10.6 / 10.6 | 9 % / 8 % |
| x -1.5..3, n=12 (lower shelf weak); USE 8 J, LSE 6 % of USE [high] | 25 % | 16.4 / 16.3 | 16 % / 13 % |

### 2.10 All-fitted sensitivity case (pre-registered method) on the same Blocks A-D

| class (Blocks A-D with scatter) | final method | all fitted (sensitivity) |
| --- | --- | --- |
| within reference (all fits) | 41 | 39 |
| within reference only after the flags | 9 | 10 |
| method declines (< 5 % usable) | 14 | 14 |
| usable fits still miss a reference scale | 25 | 26 |

Across the 89 scenarios, final minus all-fitted T41J P90 |error|: median -0.77 °C (range -65.3 to 2.8 °C); T0 P90 |error|: median -0.06 °C (range -46.4 to 8.1 °C). Scenarios whose trust class differs between the two methods:

| block | design | noise | trust_class_final | trust_class_all_fitted |
| --- | --- | --- | --- | --- |
| A | uniform x -3..3, n=8 | moderate | within reference (all fits) | within reference only after the flags |
| B | shelves + 3 transition points (n=9) | moderate | within reference (all fits) | within reference only after the flags |
| D | window 250 °C, n=12; true T0 -60 °C from centre; true C 30 °C | moderate | within reference (all fits) | within reference only after the flags |
| A | uniform x -3..3, n=30 | high | within reference only after the flags | usable fits still miss a reference scale |
| B | x -0.5..3, n=12 (lower shelf missing) | moderate | within reference only after the flags | usable fits still miss a reference scale |
| C | USE 250 J; uniform x -3..3, n=12 | moderate | within reference only after the flags | usable fits still miss a reference scale |
| C | C 12 °C (narrow); uniform x -3..3, n=12 | moderate | within reference only after the flags | within reference (all fits) |
| B | clustered cold side: x -3..-0.5, n=12 | moderate | method declines (< 5 % usable) | usable fits still miss a reference scale |
| D | window 250 °C, n=12; true T0 +60 °C from centre; true C 60 °C | moderate | method declines (< 5 % usable) | usable fits still miss a reference scale |
| B | shelves + 2 transition points (n=8) | moderate | usable fits still miss a reference scale | within reference only after the flags |
| D | window 150 °C, n=9; true T0 -60 °C from centre; true C 30 °C | moderate | usable fits still miss a reference scale | method declines (< 5 % usable) |
| D | window 150 °C, n=9; true T0 -60 °C from centre; true C 60 °C | moderate | usable fits still miss a reference scale | method declines (< 5 % usable) |
| D | window 250 °C, n=12; true T0 +0 °C from centre; true C 60 °C | moderate | usable fits still miss a reference scale | within reference only after the flags |

What the lower-shelf diagnostics mean when LSE is fitted (all-fitted case; this is the method applied to miniature curves):

| fits carrying | fits | T0 P90 \|err\| °C | T41J P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| |
| --- | --- | --- | --- | --- | --- |
| no flag | 8060 | 8.6 | 8.5 | 8 % | 42 % |
| only lse_at_lower_bound | 335 | 8.7 | 11.6 | 9 % | 60 % |
| only weak_lower_shelf | 850 | 15.4 | 10.9 | 6 % | 49 % |

## 3. Published data: primary cohort outcomes (final primary method)

Primary cohort: 170 curves, 2588 records (134 full-size, 36 miniature). Every curve was fitted; none was removed.

Mutually exclusive outcomes (first applicable category, D-046 as amended at CP3):

| outcome | curves | fit_quality_group | full-size_curves | miniature_curves | share |
| --- | --- | --- | --- | --- | --- |
| optimizer failure | 0 | optimizer failure | 0 | 0 | 0 % |
| non-physical (inadmissible) | 0 | non-physical (inadmissible) | 0 | 0 | 0 % |
| boundary-limited | 18 | boundary-limited | 1 | 17 | 11 % |
| weakly identified | 35 | weakly identified | 29 | 6 | 21 % |
| usable fit, index temperature unavailable | 13 | usable fit | 0 | 13 | 8 % |
| usable fit, index temperature calculated | 104 | usable fit | 104 | 0 | 61 % |
| TOTAL | 170 |  | 134 | 36 | 100 % |

The same outcomes split by the recorded reason (also mutually exclusive):

| outcome | outcome_detail | outcome_reason | curves | full_size_curves | miniature_curves |
| --- | --- | --- | --- | --- | --- |
| boundary-limited | fitted LSE at its 0 J bound (lower-shelf-bound-limited) | lse_at_lower_bound | 15 | 0 | 15 |
| boundary-limited | numerical-safety bound | boundary_c_min | 2 | 0 | 2 |
| boundary-limited | numerical-safety bound | boundary_t0_limit, boundary_rise_max | 1 | 1 | 0 |
| weakly identified |  | weak_upper_shelf | 29 | 28 | 1 |
| weakly identified |  | weak_lower_shelf | 3 | 0 | 3 |
| weakly identified |  | weak_transition | 1 | 1 | 0 |
| weakly identified |  | weak_transition, weak_lower_shelf | 1 | 0 | 1 |
| weakly identified |  | weak_upper_shelf, weak_lower_shelf | 1 | 0 | 1 |
| usable fit, index temperature unavailable |  | not calculated: no defensible criterion for this geometry | 13 | 0 | 13 |
| usable fit, index temperature calculated |  |  | 104 | 104 | 0 |

Diagnostic flags (overlapping; a curve can carry several):

| flag | meaning | curves | full_size_curves | miniature_curves |
| --- | --- | --- | --- | --- |
| flag_optimizer_failure | optimizer failure (no start converged) | 0 | 0 | 0 |
| flag_nonphysical_no_rise | non-physical (inadmissible): no rise (USE = LSE) | 0 | 0 | 0 |
| flag_nonphysical_t0_at_absolute_zero | non-physical (inadmissible): T0 at absolute zero | 0 | 0 | 0 |
| flag_lse_at_lower_bound | boundary: fitted LSE at its 0 J lower bound (lower shelf not independently supported, or the symmetric tanh compensating for a curve-shape mismatch; LSE fitted only) | 15 | 0 | 15 |
| flag_boundary_c_min | boundary: C at 1 °C (width unresolved) | 2 | 0 | 2 |
| flag_boundary_c_max | boundary: C at the tested span | 0 | 0 | 0 |
| flag_boundary_t0_limit | boundary: T0 at a range limit | 1 | 1 | 0 |
| flag_boundary_rise_max | boundary: USE - LSE at 10x highest energy | 1 | 1 | 0 |
| flag_boundary_lse_max | boundary: LSE at highest energy | 0 | 0 | 0 |
| flag_weak_transition | weak: < 2 test temperatures inside T0 ± C | 5 | 2 | 3 |
| flag_weak_upper_shelf | weak: upper shelf not supported (< 2 specimens at >= 95 % of rise) | 35 | 29 | 6 |
| flag_weak_lower_shelf | weak: lower shelf not supported (< 2 specimens at <= 5 % of rise; LSE fitted only) | 18 | 0 | 18 |
| flag_numerically_singular | ill-conditioned: Jacobian rank-deficient | 1 | 0 | 1 |
| flag_nonflat_upper_shelf | model adequacy (not an outcome): upper-shelf residual trend (p < 0.05) | 7 | 5 | 2 |
| flag_index_unavailable | index temperature not calculated (any reason) | 36 | 0 | 36 |
| flag_index_near_fitted_shelf | index support (not an outcome): T41J calculated, but 41 J outside the central 11.9-88.1 % of the fitted rise | 9 | 9 | 0 |
| flag_index_not_bracketed_by_measured_energy | index support (not an outcome; project diagnostic, not an ASTM requirement): T41J calculated from fitted curve; 41 J not empirically bracketed by measured energies (all measured energies on one side of 41 J) | 1 | 1 | 0 |
| flag_full_size_notch_dimensions_unreported | metadata (not a fit diagnostic): full-size V-notch, exact notch dimensions unreported; T41J still calculated (D-044) | 74 | 74 | 0 |

Index temperature by geometry (D-044, D-045):

| geometry_group | curves | criterion | basis | index_calculated | index_calculated_and_fit_usable | index_calculated_with_index_support_warning | index_calculated_not_bracketed_by_measured_energy | not_calculated | not_calculated_reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size 55x10x10 mm V-notch, exact notch dimensions unreported | 74 | 41 J | 10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044) | 74 | 58 | 2 | 0 | 0 |  |
| full-size 55x10x10 mm V-notch, notch dimensions reported | 60 | 41 J | 10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044) | 60 | 46 | 7 | 1 | 0 |  |
| miniature: 20x1.5x1.5 a=0.33 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 20x2.5x2.5 a=0.38 | 5 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 5 | not calculated: no defensible criterion for this geometry (5) |
| miniature: 20x3.33x3.33 a=0.51 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 20x5x5 a=0.76 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 23.6x3.33x3.33 a=0.51 | 7 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 7 | not calculated: no defensible criterion for this geometry (7) |
| miniature: 23.6x5x5 a=0.76 | 2 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 2 | not calculated: no defensible criterion for this geometry (2) |
| miniature: 23.6x5x5 a=0.78 | 1 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 1 | not calculated: no defensible criterion for this geometry (1) |
| miniature: 27.5x3.33x3.33 a=0.6 | 1 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 1 | not calculated: no defensible criterion for this geometry (1) |
| miniature: 27x3x4 a=1 | 8 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 0 | 0 | 8 | not calculated: no defensible criterion for this geometry (8) |

Where 41 J lies on the fitted rise (full-size curves with a calculated index; index-support diagnostic, D-044):

| 41 J position on the fitted rise | curves | notch dimensions unreported | boundary-limited | weakly identified | usable fit, index temperature calculated |
| --- | --- | --- | --- | --- | --- |
| below 11.9 % (flat lower part of the fit) | 9 | 2 | 1 | 5 | 3 |
| 11.9-88.1 % (inside T0 ± C) | 125 | 72 | 0 | 24 | 101 |
| above 88.1 % (flat upper part) | 0 | 0 | 0 | 0 | 0 |

Summary: T41J calculated for 134 of 134 full-size curves; not calculated for 0 (none). 74 of the calculated values come from full-size V-notch curves with exact notch dimensions unreported; 9 carry the index-support warning for the index position (41 J outside 11.9-88.1 % of the fitted rise) and 1 the empirical-bracketing warning (no measured energy on one side of 41 J; section 3.2). Miniature curves with a usable fit (T0, C, LSE and USE reported, no index temperature): 13 of 36.

### 3.1 Notch-metadata sensitivity (D-044; a diagnostic, the primary cohort is unchanged)

| case | full-size curves | records | T41J calculated | T41J with a usable fit | T41J with a usable fit and no index-support warning | T41J with an index-support warning | T41J in a weakly identified or boundary-limited fit | stricter-cohort curves with a usable-fit T41J | irradiated curves with a usable-fit T41J | median T41J, usable fits (°C) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary: all full-size curves | 134 | 2059 | 134 | 104 | 101 | 9 | 30 | 33 | 14 | -52.86 |
| sensitivity: excluding curves with exact notch dimensions unreported | 60 | 1066 | 60 | 46 | 43 | 7 | 14 | 22 | 10 | -27.07 |
| the excluded curves: full-size V-notch, exact notch dimensions unreported | 74 | 993 | 74 | 58 | 58 | 2 | 16 | 11 | 4 | -68.86 |

Notch fields of the full-size records, as reported (nothing filled in):

| curve_notch_reported | notch_shape | notch_depth_mm | notch_angle_deg | notch_root_radius_mm | records | curves |
| --- | --- | --- | --- | --- | --- | --- |
| False | V |  |  |  | 993 | 74 |
| True | V | 2 | 45 | 0.25 | 1066 | 60 |

### 3.2 Empirical bracketing of 41 J by the measured energies (D-044 support diagnostic, added at final CP3 approval; not an outcome)

Two separate index-support diagnostics are reported beside every calculated T41J. The index-position warning (`flag_index_near_fitted_shelf`, section 3) asks where 41 J lies on the fitted S-curve. The empirical-bracketing diagnostic asks whether the published measured energies themselves lie on both sides of 41 J: `criterion_bracketed_by_measured_energy` = min(measured energy) <= 41 J <= max(measured energy), with the measured energies below, exactly at and above 41 J counted. A calculated T41J that is not bracketed is kept unchanged and flagged `flag_index_not_bracketed_by_measured_energy`: "T41J calculated from fitted curve; 41 J not empirically bracketed by measured energies." It separates a fitted crossing supported by observations on both sides of 41 J from one supplied mainly by the model because every observation lies on one side. This is a project support diagnostic, not an ASTM requirement. It is computed from the measurements after the outcome classification, so it changes no fit, T41J value, outcome or frozen WP2 cohort.

Answers (primary cohort, final method). (1) Of the 134 full-size curves with a calculated T41J, 133 are empirically bracketed by their measured energies. (2) 1 is not. (3) Among the 104 usable-fit T41J values, 1 is not bracketed. (4) Not bracketed: 33-153. (5) Overlap: of the 9 T41J values with the index-position warning, 0 are not bracketed, so 0 curves carry both warnings; of the 74 from curves with exact notch dimensions unreported, 0 are not bracketed; by fit outcome, not bracketed / T41J values: boundary-limited 0 / 1; weakly identified 0 / 29; usable fit, index temperature calculated 1 / 104. Context: 0 calculated T41J values lack a measured energy above 41 J; 11 are bracketed by a single measured energy below 41 J; 0 curves have a measured energy of exactly 41 J. Under the all-fitted sensitivity case, 0 of its 132 calculated T41J values are not bracketed.

| dimension | group | t41j_curves | bracketed | not_bracketed | not_bracketed_curve_ids |
| --- | --- | --- | --- | --- | --- |
| all | full-size curves with a calculated T41J (final method) | 134 | 133 | 1 | 33-153 |
| fit outcome | boundary-limited | 1 | 1 | 0 |  |
| fit outcome | weakly identified | 29 | 29 | 0 |  |
| fit outcome | usable fit, index temperature calculated | 104 | 103 | 1 | 33-153 |
| index-position warning | warning: 41 J outside the central 11.9-88.1 % of the fitted rise | 9 | 9 | 0 |  |
| index-position warning | no warning: 41 J inside the central 11.9-88.1 % of the fitted rise | 125 | 124 | 1 | 33-153 |
| notch metadata | full-size V-notch, exact notch dimensions unreported | 74 | 74 | 0 |  |
| notch metadata | notch dimensions reported | 60 | 59 | 1 | 33-153 |
| measured energies below 41 J | 0 | 1 | 0 | 1 | 33-153 |
| measured energies below 41 J | 1 | 11 | 11 | 0 |  |
| measured energies below 41 J | 2 | 30 | 30 | 0 |  |
| measured energies below 41 J | 3 or more | 92 | 92 | 0 |  |
| measured energies above 41 J | 0 | 0 | 0 | 0 |  |
| measured energies above 41 J | 1 | 0 | 0 | 0 |  |
| measured energies above 41 J | 2 | 0 | 0 | 0 |  |
| measured energies above 41 J | 3 or more | 134 | 133 | 1 | 33-153 |
| measured energies exactly at 41 J | 0 | 134 | 133 | 1 | 33-153 |
| measured energies exactly at 41 J | 1 or more | 0 | 0 | 0 |  |
| lower-shelf sensitivity case | full-size curves with a calculated T41J (all-fitted method) | 132 | 132 | 0 |  |

**Curve 33-153** (ref 33; A508 forging, unirradiated, full-size 55x10x10 mm V-notch, notch dimensions reported; 7 points from -120.1 to 24.4 °C). Final method: LSE fixed at 2.7 J, USE 235.8 J, T0 -77.9 °C, C 44.9 °C; outcome 'usable fit, index temperature calculated'; T41J -114.5 °C, 5.6 °C above the lowest test temperature. 41 J lies at 16.4 % of the fitted rise ('41 J inside the central 11.9-88.1 % of the fitted rise'), so the index-position warning does not fire. But all 7 measured energies are above 41 J (lowest 42.8 J, at -120.1 °C, where the fitted curve gives 33.7 J): the crossing is placed by the fitted curve, its tanh shape and the fixed 2.7 J lower shelf, not by measurements on both sides of 41 J. Under the all-fitted sensitivity case the same measurements give LSE 31.7 J (fitted) and a 41 J crossing of the fitted curve at -123.0 °C; that method's index status is 'unsupported: crossing below the lowest test temperature'. The T41J value, fit and outcome are kept; the curve carries the empirical-bracketing warning. This is the curve whose review exposed the missing diagnostic at CP3 (D-051); nothing about its fit was changed because of it.

| record_id | test temperature (°C) | measured energy (J) | side of 41 J | fitted energy, final method (J) | measured - fitted (J) |
| --- | --- | --- | --- | --- | --- |
| R2030 | -120.1 | 42.8 | above | 33.7 | 9.1 |
| R2029 | -90 | 81.3 | above | 88.8 | -7.5 |
| R2028 | -60.4 | 163.7 | above | 162.5 | 1.3 |
| R2027 | -45.7 | 189.7 | above | 191 | -1.3 |
| R2026 | -29.7 | 220.2 | above | 211.4 | 8.8 |
| R2025 | -0.2 | 222.3 | above | 228.7 | -6.4 |
| R2024 | 24.4 | 233.5 | above | 233.4 | 0.1 |

SYNTHETIC context (the existing audit rows of `synthetic_flag_check.csv`, Blocks A-D with scatter, final method; no scenario was added for this diagnostic): usable fit with T41J: no specimen energy below 41 J: 78 fits, T41J P90 |error| 5.5 °C; usable fit with T41J: at least one specimen energy below 41 J: 10172 fits, T41J P90 |error| 8.5 °C. Those synthetic truths are symmetric tanh curves with true lower shelves of 2-10 J (the final method fixes 2.7 J); none has a lower transition that departs from the tanh shape, which is where a crossing without a measurement below 41 J depends most on the model. The warning therefore records missing empirical support; it is not a demonstrated loss of accuracy, and the synthetic audit does not show one.

## 4. Where fits fail or are weak, against the WP2 sampling descriptors (final method)

| dimension | group | curves | optimizer failure | non-physical (inadmissible) | boundary-limited | weakly identified | usable fit, index temperature unavailable | usable fit, index temperature calculated | share_not_usable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| material_family | 20MnMoNi55 | 8 | 0 | 0 | 0 | 0 | 0 | 8 | 0 |
| material_family | A302B | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| material_family | A508 | 95 | 0 | 0 | 6 | 24 | 4 | 61 | 0.316 |
| material_family | A533B | 61 | 0 | 0 | 9 | 11 | 9 | 32 | 0.328 |
| material_family | A533B weld metal | 4 | 0 | 0 | 3 | 0 | 0 | 1 | 0.75 |
| product_form_group | HAZ (incl. simulated) | 19 | 0 | 0 | 4 | 5 | 1 | 9 | 0.474 |
| product_form_group | forging | 84 | 0 | 0 | 6 | 20 | 4 | 54 | 0.31 |
| product_form_group | not determinable | 6 | 0 | 0 | 0 | 0 | 0 | 6 | 0 |
| product_form_group | plate | 57 | 0 | 0 | 5 | 10 | 8 | 34 | 0.263 |
| product_form_group | weld metal | 4 | 0 | 0 | 3 | 0 | 0 | 1 | 0.75 |
| irradiation | irradiated | 31 | 0 | 0 | 4 | 5 | 8 | 14 | 0.29 |
| irradiation | unirradiated | 139 | 0 | 0 | 14 | 30 | 5 | 90 | 0.317 |
| geometry_class | full-size (55x10x10 mm) | 134 | 0 | 0 | 1 | 29 | 0 | 104 | 0.224 |
| geometry_class | miniature (reduced length) | 36 | 0 | 0 | 17 | 6 | 13 | 0 | 0.639 |
| n_points_bin | 6-8 | 13 | 0 | 0 | 1 | 7 | 1 | 4 | 0.615 |
| n_points_bin | 9-11 | 56 | 0 | 0 | 5 | 13 | 0 | 38 | 0.321 |
| n_points_bin | 12-14 | 41 | 0 | 0 | 3 | 9 | 7 | 22 | 0.293 |
| n_points_bin | 15-19 | 29 | 0 | 0 | 1 | 4 | 5 | 19 | 0.172 |
| n_points_bin | 20+ | 31 | 0 | 0 | 8 | 2 | 0 | 21 | 0.323 |
| wp2_transition_temperatures | 2 | 6 | 0 | 0 | 2 | 1 | 0 | 3 | 0.5 |
| wp2_transition_temperatures | 3 | 24 | 0 | 0 | 2 | 10 | 2 | 10 | 0.5 |
| wp2_transition_temperatures | 4-5 | 78 | 0 | 0 | 8 | 11 | 6 | 53 | 0.244 |
| wp2_transition_temperatures | 6+ | 62 | 0 | 0 | 6 | 13 | 5 | 38 | 0.306 |
| wp2_lower_band_temperatures | 1 | 31 | 0 | 0 | 1 | 9 | 2 | 19 | 0.323 |
| wp2_lower_band_temperatures | 2 | 64 | 0 | 0 | 10 | 16 | 4 | 34 | 0.406 |
| wp2_lower_band_temperatures | 3+ | 75 | 0 | 0 | 7 | 10 | 7 | 51 | 0.227 |
| wp2_upper_band_temperatures | 2 | 25 | 0 | 0 | 3 | 11 | 1 | 10 | 0.56 |
| wp2_upper_band_temperatures | 3 | 62 | 0 | 0 | 4 | 16 | 2 | 40 | 0.323 |
| wp2_upper_band_temperatures | 4+ | 83 | 0 | 0 | 11 | 8 | 10 | 54 | 0.229 |
| temperature_span | <=150 °C | 23 | 0 | 0 | 5 | 8 | 3 | 7 | 0.565 |
| temperature_span | 150-250 °C | 64 | 0 | 0 | 12 | 15 | 2 | 35 | 0.422 |
| temperature_span | 250-350 °C | 58 | 0 | 0 | 0 | 11 | 3 | 44 | 0.19 |
| temperature_span | >350 °C | 25 | 0 | 0 | 1 | 1 | 5 | 18 | 0.08 |

Residual pattern by lower-shelf treatment (measured minus fitted, % of fitted USE), final method:

| geometry_category | lower_shelf_treatment | curves | mean residual, x <= -1.5 (fitted lower shelf), % of USE | curves with points, x <= -1.5 (fitted lower shelf) | mean residual, -1.5 < x <= -0.5 (lower transition), % of USE | curves with points, -1.5 < x <= -0.5 (lower transition) | mean residual, -0.5 < x < 0.5 (middle), % of USE | curves with points, -0.5 < x < 0.5 (middle) | mean residual, 0.5 <= x < 1.5 (upper transition), % of USE | curves with points, 0.5 <= x < 1.5 (upper transition) | median C (°C) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | LSE fixed at 2.7 J | 134 | 0.7 | 85 | -0.59 | 131 | 0.39 | 131 | 0.3 | 130 | 47.48 |
| miniature | LSE fitted, above 0 J | 21 | -0.44 | 19 | 0.04 | 18 | -0.42 | 20 | 2.76 | 19 | 29.15 |
| miniature | LSE fitted, at its 0 J bound | 15 | 1.14 | 8 | -5.96 | 15 | 2.86 | 15 | -1.43 | 15 | 34.75 |

The same for the all-fitted sensitivity case (the table that explained the fitted LSE at 0 J before CP3, D-042):

| geometry_category | lower_shelf_treatment | curves | mean residual, x <= -1.5 (fitted lower shelf), % of USE | curves with points, x <= -1.5 (fitted lower shelf) | mean residual, -1.5 < x <= -0.5 (lower transition), % of USE | curves with points, -1.5 < x <= -0.5 (lower transition) | mean residual, -0.5 < x < 0.5 (middle), % of USE | curves with points, -0.5 < x < 0.5 (middle) | mean residual, 0.5 <= x < 1.5 (upper transition), % of USE | curves with points, 0.5 <= x < 1.5 (upper transition) | median C (°C) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | LSE fitted, above 0 J | 78 | -0.44 | 62 | 0.48 | 76 | -0.41 | 76 | 1.24 | 74 | 40.94 |
| full-size | LSE fitted, at its 0 J bound | 56 | 0.12 | 30 | -2.81 | 55 | 1.67 | 55 | -1.54 | 54 | 50.83 |
| miniature | LSE fitted, above 0 J | 21 | -0.44 | 19 | 0.04 | 18 | -0.42 | 20 | 2.76 | 19 | 29.15 |
| miniature | LSE fitted, at its 0 J bound | 15 | 1.14 | 8 | -5.96 | 15 | 2.86 | 15 | -1.43 | 15 | 34.75 |

## 5. Fitted parameters (usable fits, final method)

| geometry_category | parameter | curves | minimum | p10 | median | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | USE (J) | 104 | 51.24 | 100.2 | 201.4 | 272.9 | 395.7 |
| full-size | T0 (°C) | 104 | -118.4 | -88.95 | -19.97 | 44.08 | 199.9 |
| full-size | C (°C) | 104 | 20.21 | 28.21 | 46.45 | 60.66 | 74.05 |
| full-size | T41J (°C) | 104 | -164.7 | -124.6 | -52.86 | 29.79 | 213.5 |
| miniature | LSE (J), fitted values only | 13 | 0.299 | 0.336 | 1.012 | 1.576 | 2.177 |
| miniature | USE (J) | 13 | 3.32 | 3.698 | 7.929 | 12.82 | 29.08 |
| miniature | T0 (°C) | 13 | -157.5 | -138.3 | -50.1 | 195.1 | 202.3 |
| miniature | C (°C) | 13 | 17.41 | 18.95 | 29.16 | 61.11 | 78.43 |

Extremes (all primary fits):

| parameter | which | curve_id | value | outcome | outcome_reason | material_family | product_form | irradiated | geometry | n_points | T_min_c | T_max_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| use_j | minimum | 53-241 | 0.979 | boundary-limited | lse_at_lower_bound | A533B weld metal | weld metal | False | 20x1.5x1.5 a=0.33 | 11 | -159.9 | 39.73 |
| use_j | maximum | 49-206 | 1197 | boundary-limited | boundary_t0_limit, boundary_rise_max | A533B | plate | False | 55x10x10 a=? | 20 | -23.2 | 199.3 |
| t0_c | minimum | 109-287 | -157.5 | usable fit, index temperature unavailable | not calculated: no defensible criterion for this geometry | A508 | forging | True | 27x3x4 a=1 | 13 | -200 | 200 |
| t0_c | maximum | 49-206 | 421.9 | boundary-limited | boundary_t0_limit, boundary_rise_max | A533B | plate | False | 55x10x10 a=? | 20 | -23.2 | 199.3 |
| c_c | minimum | 53-230 | 1 | boundary-limited | boundary_c_min | A533B | plate | False | 20x3.33x3.33 a=0.51 | 20 | -196 | 19.93 |
| c_c | maximum | 109-293 | 196.8 | weakly identified | weak_upper_shelf, weak_lower_shelf | A508 | forging | True | 27x3x4 a=1 | 13 | -160 | 350 |
| index_temperature_c | minimum | 17-83 | -164.7 | usable fit, index temperature calculated |  | A508 | forging | False | 55x10x10 a=? | 10 | -196.3 | 99.66 |
| index_temperature_c | maximum | 55-255 | 213.5 | usable fit, index temperature calculated |  | A533B | plate | True | 55x10x10 a=2 | 10 | 23.75 | 343.1 |
| lse_j (fitted values only) | minimum | 53-241 | 0 | boundary-limited | lse_at_lower_bound | A533B weld metal | weld metal | False | 20x1.5x1.5 a=0.33 | 11 | -159.9 | 39.73 |
| lse_j (fitted values only) | maximum | 59-270 | 2.177 | usable fit, index temperature unavailable | not calculated: no defensible criterion for this geometry | A533B | plate | True | 23.6x3.33x3.33 a=0.51 | 17 | -163.9 | 16.64 |

## 6. Lower-shelf sensitivity on the published curves: FINAL PRIMARY against ALL FITTED (CP3 amendment of D-042)

A sensitivity comparison, not a second method selection. Miniature curves are fitted identically by both (LSE fitted), so every difference comes from the full-size lower shelf. Part of any outcome change is mechanical: a fixed lower shelf cannot trigger the lower-shelf diagnostics.

| geometry_category | quantity | curves_compared | median | median_abs | p90_abs | max_abs | curve_with_max_abs | all_fitted_lse_of_that_curve_j |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | T41J (all fitted - final), °C | 132 | 0.15 | 0.287 | 1.894 | 15.36 | 12-54 | 37.04 |
| full-size | T0 (all fitted - final), °C | 134 | -0.195 | 0.73 | 5.341 | 252.6 | 49-206 | 22.86 |
| full-size | USE (all fitted - final), J | 134 | 0.104 | 0.448 | 4.608 | 1053 | 49-206 | 22.86 |
| full-size | USE (all fitted / final - 1) | 134 | 0.001 | 0.002 | 0.024 | 0.88 | 49-206 | 22.86 |
| full-size | C (all fitted / final - 1) | 134 | 0.013 | 0.029 | 0.259 | 0.967 | 12-49 | 81.31 |
| miniature | T0 (all fitted - final), °C | 36 | 0 | 0 | 0 | 0 |  |  |
| miniature | USE (all fitted - final), J | 36 | 0 | 0 | 0 | 0 |  |  |
| miniature | USE (all fitted / final - 1) | 36 | 0 | 0 | 0 | 0 |  |  |
| miniature | C (all fitted / final - 1) | 36 | 0 | 0 | 0 | 0 |  |  |

Full-size headline: |T41J difference| median 0.29 °C, 90th percentile 1.89 °C (132 curves with T41J under both); |T0 difference| median 0.73 °C, 90th percentile 5.34 °C; |USE difference| median 0.24 % (0.45 J), 90th percentile 2.36 %. Outcome category differs for 89 of 134 full-size curves and 0 miniature curves; index availability differs for 2 full-size curves.

Outcome and index-availability changes (curves):

| geometry_category | change | curves |
| --- | --- | --- |
| full-size | curves compared | 134 |
| full-size | outcome category differs | 89 |
| full-size | outcome: final 'boundary-limited' / all fitted 'weakly identified' | 1 |
| full-size | outcome: final 'usable fit, index temperature calculated' / all fitted 'boundary-limited' | 43 |
| full-size | outcome: final 'usable fit, index temperature calculated' / all fitted 'weakly identified' | 28 |
| full-size | outcome: final 'weakly identified' / all fitted 'boundary-limited' | 14 |
| full-size | outcome: final 'weakly identified' / all fitted 'usable fit, index temperature calculated' | 3 |
| full-size | index availability differs | 2 |
| full-size | index: final 'calculated' / all fitted 'undefined: 41 J at or below the fitted LSE' | 1 |
| full-size | index: final 'calculated' / all fitted 'unsupported: crossing below the lowest test temperature' | 1 |
| full-size | index-support warning differs (both calculated) | 11 |
| miniature | curves compared | 36 |
| miniature | outcome category differs | 0 |
| miniature | index availability differs | 0 |
| miniature | index-support warning differs (both calculated) | 0 |

Before and after (the previous CP3 presentation is reproduced exactly from the all-fitted run):

| quantity | previous CP3 presentation (all fitted; pre-CP3 classification) | all fitted; amended classification (terminology change only) | FINAL PRIMARY (geometry-specific lower shelf; amended classification) |
| --- | --- | --- | --- |
| lower-shelf strategy | all fitted: LSE fitted >= 0 J for every geometry (pre-registered rule outcome) | all fitted: LSE fitted >= 0 J for every geometry (pre-registered rule outcome) | geometry-specific: LSE fixed at 2.7 J (full-size), fitted >= 0 J (miniature) |
| optimizer failure | 0 | 0 | 0 |
| non-physical | 71 | 0 | 0 |
| boundary-limited | 3 | 74 | 18 |
|   boundary-limited: fitted LSE at its 0 J bound (alone or with another bound) | counted as non-physical | 71 | 15 |
|   boundary-limited: numerical-safety bound only | 3 | 3 | 3 |
| weakly identified | 47 | 47 | 35 |
| usable fit, index temperature unavailable | 13 | 13 | 13 |
| usable fit, index temperature calculated | 36 | 36 | 104 |
| usable fits (both usable categories) | 49 | 49 | 117 |
| TOTAL curves | 170 | 170 | 170 |
| full-size curves with T41J calculated (of 134) | 132 | 132 | 134 |
| full-size T41J with a usable fit | 36 | 36 | 104 |
| T41J with the index-support warning (41 J outside 11.9-88.1 % of the fitted rise) | 15 | 15 | 9 |
| T41J not empirically bracketed by measured energies (D-044 support diagnostic, added at final CP3 approval; not an outcome) | 0 | 0 | 1 |
| flag: fitted LSE at its 0 J bound (overlapping) | 71 | 71 | 15 |
| flag: weak lower shelf (overlapping) | 105 | 105 | 18 |
| miniature curves with a usable fit (of 36) | 13 | 13 | 13 |

Check: the all-fitted run under the pre-CP3 classification reproduces the counts presented at CP3:

| outcome | curves | fit_quality_group | full-size_curves | miniature_curves | share |
| --- | --- | --- | --- | --- | --- |
| optimizer failure | 0 | optimizer failure | 0 | 0 | 0 % |
| non-physical | 71 | non-physical | 56 | 15 | 42 % |
| boundary-limited | 3 | boundary-limited | 1 | 2 | 2 % |
| weakly identified | 47 | weakly identified | 41 | 6 | 28 % |
| usable fit, index temperature unavailable | 13 | usable fit | 0 | 13 | 8 % |
| usable fit, index temperature calculated | 36 | usable fit | 36 | 0 | 21 % |
| TOTAL | 170 |  | 134 | 36 | 100 % |

## 7. Dataset-provided USE and DBTT (diagnostic only, D-049; final method)

| geometry_category | fit_usable | curves | with_dataset_use | with_dataset_dbtt | use_ratio_median | use_ratio_p10 | use_ratio_p90 | share_use_within_10pct | t41_minus_dbtt_median_c | t41_minus_dbtt_median_abs_c | share_t41_within_10c | t0_minus_dbtt_median_c | t0_minus_dbtt_median_abs_c | share_t0_within_10c | dbtt_closer_to_t41j | dbtt_closer_to_t0 | dataset_use_below_41j |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | False | 30 | 29 | 30 | 1.001 | 0.959 | 1.056 | 0.867 | -34.64 | 34.9 | 0.067 | 1.925 | 3.409 | 0.767 | 2 | 28 | 0 |
| full-size | True | 104 | 103 | 104 | 0.999 | 0.984 | 1.019 | 0.981 | -28.79 | 29.11 | 0.077 | -0.562 | 3.156 | 0.933 | 3 | 101 | 0 |
| miniature | False | 23 | 23 | 23 | 0.994 | 0.949 | 1 | 0.87 |  |  |  | -6.521 | 9.04 | 0.565 | 0 | 0 | 22 |
| miniature | True | 13 | 13 | 13 | 1 | 1 | 1.007 | 0.923 |  |  |  | 3.955 | 6.683 | 0.692 | 0 | 0 | 13 |

## 8. Looser and stricter cohorts (diagnostic, D-050; final method)

| outcome | curves | fit_quality_group | full-size_curves | miniature_curves | share | cohort |
| --- | --- | --- | --- | --- | --- | --- |
| optimizer failure | 0 | optimizer failure | 0 | 0 | 0 % | looser |
| non-physical (inadmissible) | 0 | non-physical (inadmissible) | 0 | 0 | 0 % | looser |
| boundary-limited | 19 | boundary-limited | 1 | 18 | 10 % | looser |
| weakly identified | 42 | weakly identified | 34 | 8 | 23 % | looser |
| usable fit, index temperature unavailable | 14 | usable fit | 1 | 13 | 8 % | looser |
| usable fit, index temperature calculated | 107 | usable fit | 107 | 0 | 59 % | looser |
| TOTAL | 182 |  | 143 | 39 | 100 % | looser |
| optimizer failure | 0 | optimizer failure | 0 | 0 | 0 % | primary |
| non-physical (inadmissible) | 0 | non-physical (inadmissible) | 0 | 0 | 0 % | primary |
| boundary-limited | 18 | boundary-limited | 1 | 17 | 11 % | primary |
| weakly identified | 35 | weakly identified | 29 | 6 | 21 % | primary |
| usable fit, index temperature unavailable | 13 | usable fit | 0 | 13 | 8 % | primary |
| usable fit, index temperature calculated | 104 | usable fit | 104 | 0 | 61 % | primary |
| TOTAL | 170 |  | 134 | 36 | 100 % | primary |
| optimizer failure | 0 | optimizer failure | 0 | 0 | 0 % | stricter |
| non-physical (inadmissible) | 0 | non-physical (inadmissible) | 0 | 0 | 0 % | stricter |
| boundary-limited | 12 | boundary-limited | 1 | 11 | 20 % | stricter |
| weakly identified | 6 | weakly identified | 5 | 1 | 10 % | stricter |
| usable fit, index temperature unavailable | 9 | usable fit | 0 | 9 | 15 % | stricter |
| usable fit, index temperature calculated | 33 | usable fit | 33 | 0 | 55 % | stricter |
| TOTAL | 60 |  | 39 | 21 | 100 % | stricter |

## 9. Example figures

- `synthetic_examples.png`: SYNTHETIC good versus poor sampling (spread of 40 replicate fits), final method.
- `synthetic_error_vs_specimens.png`, `synthetic_sampling_patterns.png`: SYNTHETIC validation summaries, final method.
- `fits_published_examples.png`: published curves, final method: clearly successful fit (2-9); converged but weakly identified (53-234); boundary-limited: fitted LSE at its 0 J bound (53-229); boundary-limited: numerical-safety bound (49-206).
- `fits_outcome_by_sampling.png`: outcome shares against WP2 sampling descriptors, final method.
