# WP3 summary: transition-curve fitting (q4x6v-dyt25)

Analysis of published Charpy V-notch test data (Materials Cloud 2025.30). Section 2 is SYNTHETIC fitter validation; every other section concerns the published measurements of the CP2-frozen cohorts. Decisions: DECISIONS.md D-040 to D-051.

## 1. Method

| item | setting | decision |
| --- | --- | --- |
| model | E(T) = LSE + (USE - LSE)/2 [1 + tanh((T - T0)/C)]; solver parameters (LSE, USE - LSE, T0, C) | D-040 |
| lower shelf | `fitted` (LSE a free parameter, >= 0 J) | D-042 |
| upper shelf | fitted asymptote LSE + (USE - LSE); supported if >= 2 specimens where the fit is >= 95.3 % of the rise (x >= 1.5); residual trend test (p < 0.05) reported as a model-adequacy flag outside the outcome | D-043 |
| index temperature, full-size 55x10x10 mm | T at 41 J, analytic; only if LSE < 41 J < USE and inside the tested range | D-044 |
| index temperature, miniature / E23 sub-size | not calculated (no defensible criterion) | D-045 |
| optimizer | scipy.optimize.least_squares, method trf, analytic Jacobian, scaled parameters, ftol = xtol = gtol = 1e-10, max_nfev = 2000 per start | D-041 |
| weighting | ordinary (unweighted) least squares on energy | D-041 |
| starts (6, deterministic) | LSE = lowest energy; USE = mean of 3 highest; T0 in {midpoint crossing, lower quartile, upper quartile of distinct temperatures}; C in {span/12, span/4} | D-041 |
| bounds | LSE [0, highest energy]; USE - LSE [0, 10 x highest energy]; T0 [max(-273.15, T_min - span), T_max + span]; C [1 °C, span]; on a bound = active or within 0.1 % of the interval | D-041 |
| weak transition | < 2 distinct temperatures with -1 < x < 1 | D-047 |
| weak shelves | < 2 specimens with x >= 1.5 (upper) or x <= -1.5 (lower, fitted LSE only) | D-047 |
| numerically singular | Jacobian rank < number of parameters (NumPy default tolerance) | D-047 |
| outcome precedence | optimizer failure > non-physical > boundary-limited > weakly identified > usable fit, index temperature unavailable > usable fit, index temperature calculated | D-046 |
| synthetic validation | seed 20260913; 200 replicates per scenario with scatter; scatter levels (sigma_T, cv): zero (0 °C, 0); low (2 °C, 0.03); moderate (5 °C, 0.06); high (10 °C, 0.12) | D-048 |
| reference scales (summaries only) | 10 °C for T41J and T0; 10 % for USE; 25 % for C | D-048 |

## 2. Fitter validation on SYNTHETIC curves (not published data)

All tables in this section come from synthetic curves with known truth (657 scenarios, 128216 fits, seed 20260913; `synthetic_*` files). Errors are fitted minus true. P90 |err| = the value 90 % of fits stay within. 'usable' = no optimizer failure, non-physical, boundary or weak-identification flag. T41J errors use the analytic crossing of every fit that returned estimates, including crossings outside the tested range that the method would not report. Reference scales (for reading, not acceptance): 10 °C for T41J and T0, 10 % for USE.

### 2.1 Lower shelf: fitted or fixed (Block L, D-042)

| lse_strategy | score_mean_p90_c | mean_missing_share | score_full-size_c | score_miniature_c | cohort_weighted_score_c_not_used_by_rule | cohort_weight_full_size | eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fitted | 12.62 | 0.02 | 11.94 | 12.96 | 12.16 | 0.79 | True |
| fixed_convention | 11.93 | 0 | 10.13 | 12.83 | 10.7 | 0.79 | True |
| fixed_zero | 14.6 | 0 | 9.8 | 17 | 11.32 | 0.79 | True |
| hybrid | 12.06 | 0.01 | 11.66 | 12.27 | 11.79 | 0.79 | True |

Pre-registered rule outcome: `fitted` (rule 3: no strategy at least 10 % better; 'fitted' within 10 % of the lowest score).

### 2.2 Specimen count and scatter (Block A: uniform over x = -3...3; truth LSE 5 J, USE 150 J, T0 0 °C, C 30 °C)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform x -3..3, n=6 | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| uniform x -3..3, n=6 | low | 200 | 4.7 | 5.4 | 5 % | 22 % | 82 % | 4.6 | 5 % |
| uniform x -3..3, n=6 | moderate | 200 | 10.2 | 11.2 | 9 % | 59 % | 40 % | 6.2 | 7 % |
| uniform x -3..3, n=6 | high | 200 | 33.1 | 21.6 | 21 % | 97 % | 13 % | 7.3 | 11 % |
| uniform x -3..3, n=8 | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| uniform x -3..3, n=8 | low | 200 | 4.6 | 4.7 | 4 % | 24 % | 100 % | 4.6 | 4 % |
| uniform x -3..3, n=8 | moderate | 200 | 9.7 | 10.9 | 8 % | 55 % | 74 % | 8.7 | 7 % |
| uniform x -3..3, n=8 | high | 200 | 26.5 | 17 | 20 % | 97 % | 28 % | 11.5 | 13 % |
| uniform x -3..3, n=12 | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| uniform x -3..3, n=12 | low | 200 | 3.3 | 3.5 | 4 % | 20 % | 100 % | 3.4 | 3 % |
| uniform x -3..3, n=12 | moderate | 200 | 9.1 | 7.9 | 8 % | 43 % | 90 % | 8.9 | 8 % |
| uniform x -3..3, n=12 | high | 200 | 20.5 | 18 | 14 % | 97 % | 57 % | 13.9 | 10 % |
| uniform x -3..3, n=18 | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| uniform x -3..3, n=18 | low | 200 | 2.9 | 3.1 | 3 % | 15 % | 100 % | 2.9 | 3 % |
| uniform x -3..3, n=18 | moderate | 200 | 7 | 6.9 | 6 % | 36 % | 95 % | 6.6 | 6 % |
| uniform x -3..3, n=18 | high | 200 | 17.9 | 14.4 | 14 % | 93 % | 67 % | 12.5 | 13 % |
| uniform x -3..3, n=30 | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| uniform x -3..3, n=30 | low | 200 | 2.1 | 2.2 | 3 % | 12 % | 100 % | 2.1 | 3 % |
| uniform x -3..3, n=30 | moderate | 200 | 5 | 5.5 | 5 % | 28 % | 99 % | 4.9 | 5 % |
| uniform x -3..3, n=30 | high | 200 | 11.1 | 10 | 11 % | 68 % | 82 % | 10 | 10 % |

### 2.3 Sampling patterns (Block B)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shelves only, 0 transition points (n=6) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | low | 200 | 89 | 73 | 5 % | 97 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | moderate | 200 | 89.8 | 73.7 | 10 % | 97 % | 0 % |  |  |
| shelves only, 0 transition points (n=6) | high | 200 | 90.1 | 74.3 | 22 % | 113 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | low | 200 | 16 | 5.7 | 4 % | 97 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | moderate | 200 | 16.2 | 13.9 | 10 % | 100 % | 0 % |  |  |
| shelves + 1 transition point (n=7) | high | 200 | 31.1 | 45.9 | 21 % | 117 % | 0 % |  |  |
| shelves + 2 transition points (n=8) | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| shelves + 2 transition points (n=8) | low | 200 | 4.5 | 4.4 | 3 % | 26 % | 100 % | 4.5 | 3 % |
| shelves + 2 transition points (n=8) | moderate | 200 | 11.8 | 10.7 | 8 % | 75 % | 72 % | 9.2 | 7 % |
| shelves + 2 transition points (n=8) | high | 200 | 27 | 24 | 17 % | 112 % | 30 % | 13.1 | 12 % |
| shelves + 3 transition points (n=9) | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| shelves + 3 transition points (n=9) | low | 200 | 4.5 | 3.8 | 3 % | 23 % | 100 % | 4.5 | 3 % |
| shelves + 3 transition points (n=9) | moderate | 200 | 10.3 | 9.2 | 7 % | 53 % | 84 % | 9.4 | 6 % |
| shelves + 3 transition points (n=9) | high | 200 | 22.4 | 20.5 | 17 % | 119 % | 44 % | 16.6 | 13 % |
| x -1.5..3, n=12 (lower shelf weak) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| x -1.5..3, n=12 (lower shelf weak) | low | 200 | 3.2 | 3.3 | 3 % | 21 % | 2 % | 4.4 | 2 % |
| x -1.5..3, n=12 (lower shelf weak) | moderate | 200 | 8.2 | 8.5 | 6 % | 48 % | 28 % | 13.4 | 5 % |
| x -1.5..3, n=12 (lower shelf weak) | high | 200 | 19.8 | 15.9 | 16 % | 97 % | 18 % | 17.5 | 14 % |
| x -0.5..3, n=12 (lower shelf missing) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| x -0.5..3, n=12 (lower shelf missing) | low | 200 | 8.4 | 9.1 | 3 % | 32 % | 0 % |  |  |
| x -0.5..3, n=12 (lower shelf missing) | moderate | 200 | 13.9 | 14.5 | 7 % | 89 % | 6 % |  | 4 % |
| x -0.5..3, n=12 (lower shelf missing) | high | 200 | 23.3 | 21.7 | 12 % | 97 % | 8 % | 24.3 | 11 % |
| x -3..1.5, n=12 (upper shelf weak) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| x -3..1.5, n=12 (upper shelf weak) | low | 200 | 3 | 5.3 | 9 % | 25 % | 7 % | 3 | 10 % |
| x -3..1.5, n=12 (upper shelf weak) | moderate | 200 | 7.4 | 11 | 18 % | 58 % | 26 % | 7.3 | 14 % |
| x -3..1.5, n=12 (upper shelf weak) | high | 200 | 16 | 35.1 | 85 % | 97 % | 23 % | 11.7 | 21 % |
| x -3..0.5, n=12 (upper shelf missing) | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| x -3..0.5, n=12 (upper shelf missing) | low | 200 | 2.6 | 19.1 | 70 % | 46 % | 0 % |  |  |
| x -3..0.5, n=12 (upper shelf missing) | moderate | 200 | 6.9 | 59.8 | 686 % | 80 % | 4 % | 6 | 51 % |
| x -3..0.5, n=12 (upper shelf missing) | high | 200 | 12.6 | 63 | 901 % | 97 % | 12 % | 12.3 | 58 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | low | 200 | 3.3 | 2.5 | 4 % | 22 % | 100 % | 3.3 | 4 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | moderate | 200 | 9.8 | 6.2 | 9 % | 65 % | 92 % | 7.8 | 8 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) | high | 200 | 18.5 | 15.7 | 22 % | 117 % | 72 % | 11.8 | 20 % |
| clustered cold side: x -3..-0.5, n=12 | zero | 1 | 0 | 0 | 0 % | 0 % | 0 % |  |  |
| clustered cold side: x -3..-0.5, n=12 | low | 200 | 4.6 | 30.3 | 238 % | 49 % | 0 % |  |  |
| clustered cold side: x -3..-0.5, n=12 | moderate | 200 | 8.7 | 37.3 | 288 % | 94 % | 6 % | 10.8 | 85 % |
| clustered cold side: x -3..-0.5, n=12 | high | 200 | 13.2 | 45.5 | 345 % | 97 % | 10 % | 15 | 88 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | zero | 1 | 0 | 0 | 0 % | 0 % | 100 % | 0 | 0 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | low | 200 | 2.8 | 2.8 | 3 % | 14 % | 66 % | 2.6 | 3 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | moderate | 200 | 6.7 | 7 | 7 % | 35 % | 60 % | 6.3 | 6 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) | high | 200 | 15.8 | 13.9 | 15 % | 92 % | 40 % | 11.4 | 16 % |

### 2.4 Parameter values (Block C, moderate scatter)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| USE 44 J (41 J near upper shelf); uniform x -3..3, n=12 | moderate | 200 | 23.5 | 11 | 10 % | 65 % | 83 % | 19.7 | 8 % |
| USE 44 J (41 J near upper shelf); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 17.2 | 8.3 | 8 % | 45 % | 60 % | 15.3 | 9 % |
| USE 70 J; uniform x -3..3, n=12 | moderate | 200 | 7.9 | 8.7 | 7 % | 56 % | 89 % | 7.8 | 7 % |
| USE 70 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 6.7 | 7.1 | 8 % | 32 % | 66 % | 7.4 | 8 % |
| USE 250 J; uniform x -3..3, n=12 | moderate | 200 | 11.8 | 8.6 | 8 % | 50 % | 81 % | 10.8 | 7 % |
| USE 250 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 7.4 | 6.4 | 6 % | 33 % | 52 % | 5.7 | 6 % |
| LSE 2 J; uniform x -3..3, n=12 | moderate | 200 | 7.1 | 7.4 | 7 % | 40 % | 72 % | 6.9 | 7 % |
| LSE 2 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 6.3 | 6.6 | 7 % | 32 % | 40 % | 6.4 | 6 % |
| LSE 10 J; uniform x -3..3, n=12 | moderate | 200 | 9.3 | 9.3 | 8 % | 53 % | 87 % | 7.9 | 7 % |
| LSE 10 J; 5 temperatures x 3 specimens (n=15) | moderate | 200 | 8.4 | 7.3 | 7 % | 37 % | 60 % | 6.4 | 7 % |
| C 12 °C (narrow); uniform x -3..3, n=12 | moderate | 200 | 8.5 | 6.6 | 10 % | 92 % | 57 % | 5.7 | 8 % |
| C 12 °C (narrow); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 5.6 | 5 | 8 % | 53 % | 53 % | 5.1 | 8 % |
| C 60 °C (broad); uniform x -3..3, n=12 | moderate | 200 | 11.5 | 12.5 | 7 % | 32 % | 98 % | 11.5 | 7 % |
| C 60 °C (broad); 5 temperatures x 3 specimens (n=15) | moderate | 200 | 8.7 | 10.3 | 7 % | 28 % | 64 % | 7.7 | 7 % |

### 2.5 Fixed test windows planned without knowing T0 (Block D, moderate scatter)

| design | scatter | fits | T41J P90 \|err\| °C | T0 P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| | usable | T41J P90 usable fits °C | USE P90 usable fits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 9.9 | 9.8 | 5 % | 92 % | 0 % |  |  |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 17.2 | 17.4 | 5 % | 94 % | 0 % |  |  |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 20.8 | 32.9 | 9 % | 81 % | 2 % |  | 6 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 8.2 | 9 | 6 % | 92 % | 14 % | 7.4 | 7 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 8.9 | 9.8 | 10 % | 51 % | 65 % | 6.6 | 9 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 11.1 | 22.1 | 24 % | 53 % | 8 % | 16.7 | 18 % |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 13.5 | 25.2 | 659 % | 92 % | 0 % |  |  |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 8.1 | 67.5 | 701 % | 66 % | 0 % |  |  |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 9.4 | 103.9 | 597 % | 64 % | 4 % | 6.5 | 56 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 9.5 | 9.5 | 4 % | 92 % | 4 % | 9.1 | 5 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 10 | 10.1 | 5 % | 47 % | 44 % | 9.7 | 5 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 10.8 | 12.4 | 6 % | 40 % | 6 % | 20.9 | 9 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 12.1 | 10.6 | 5 % | 92 % | 24 % | 6.3 | 5 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 9.2 | 9.6 | 6 % | 46 % | 92 % | 8.8 | 6 % |
| window 250 °C, n=12; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 9.4 | 11.3 | 9 % | 35 % | 70 % | 9 | 8 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 7.8 | 7.9 | 7 % | 92 % | 10 % | 6.6 | 6 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 10.6 | 10.6 | 12 % | 47 % | 44 % | 9.9 | 10 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 9.1 | 29.1 | 34 % | 49 % | 5 % | 7.2 | 25 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 12 °C | moderate | 200 | 10.5 | 7.9 | 3 % | 92 % | 44 % | 5.3 | 3 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 30 °C | moderate | 200 | 8.1 | 6.6 | 3 % | 45 % | 98 % | 8.1 | 3 % |
| window 360 °C, n=24; true T0 -60 °C from centre; true C 60 °C | moderate | 200 | 8.3 | 8.1 | 3 % | 27 % | 82 % | 8 | 3 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 12 °C | moderate | 200 | 8.5 | 7.4 | 4 % | 92 % | 40 % | 7.2 | 3 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 30 °C | moderate | 200 | 8.1 | 6.3 | 4 % | 36 % | 100 % | 8.1 | 4 % |
| window 360 °C, n=24; true T0 +0 °C from centre; true C 60 °C | moderate | 200 | 7.1 | 8.6 | 5 % | 24 % | 98 % | 6.7 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 12 °C | moderate | 200 | 8.7 | 7.6 | 5 % | 92 % | 40 % | 5.5 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 30 °C | moderate | 200 | 7.3 | 7.6 | 5 % | 39 % | 98 % | 7.3 | 5 % |
| window 360 °C, n=24; true T0 +60 °C from centre; true C 60 °C | moderate | 200 | 6.7 | 10.4 | 9 % | 25 % | 76 % | 7 | 7 % |

### 2.6 What the outcome categories and flags mean (Blocks A-D with scatter)

| outcome | fits | share | T0 P90 \|err\| °C | T41J P90 \|err\| °C | USE P90 \|err\| |
| --- | --- | --- | --- | --- | --- |
| optimizer failure | 0 | 0 % |  |  |  |
| non-physical | 1759 | 10 % | 22.1 | 13.9 | 24 % |
| boundary-limited | 1680 | 9 % | 73.1 | 56.6 | 513 % |
| weakly identified | 6021 | 34 % | 23.6 | 15 | 29 % |
| usable fit, index temperature unavailable | 80 | 0 % | 45.5 | 59.1 | 85 % |
| usable fit, index temperature calculated | 8260 | 46 % | 8.4 | 8.5 | 7 % |
| all usable outcomes | 8340 | 47 % | 8.6 | 8.5 | 7 % |
| all fits with estimates | 17800 | 100 % | 18 | 13.3 | 19 % |

Fits carrying exactly one flag, against fits carrying none (flags overlap, so this is the clean comparison):

| fits carrying | fits | T0 P90 \|err\| °C | T41J P90 \|err\| °C | USE P90 \|err\| | C P90 \|err\| |
| --- | --- | --- | --- | --- | --- |
| no flag | 8060 | 8.6 | 8.5 | 8 % | 42 % |
| only optimizer_failure | 0 |  |  |  |  |
| only nonphysical_lse_at_zero | 335 | 8.7 | 11.6 | 9 % | 60 % |
| only nonphysical_no_rise | 0 |  |  |  |  |
| only nonphysical_t0_at_absolute_zero | 0 |  |  |  |  |
| only boundary_c_min | 0 |  |  |  |  |
| only boundary_c_max | 0 |  |  |  |  |
| only boundary_t0_limit | 0 |  |  |  |  |
| only boundary_rise_max | 0 |  |  |  |  |
| only boundary_lse_max | 0 |  |  |  |  |
| only weak_transition | 2614 | 17.8 | 19.4 | 8 % | 85 % |
| only weak_upper_shelf | 1881 | 28.1 | 8.3 | 62 % | 56 % |
| only nonflat_upper_shelf | 280 | 9.1 | 8.6 | 6 % | 46 % |
| only weak_lower_shelf | 850 | 15.4 | 10.9 | 6 % | 49 % |
| only numerically_singular | 0 |  |  |  |  |
| two or more flags | 3780 | 53.4 | 24.5 | 196 % | 97 % |

Audit diagnostics (recorded, not used to classify):

| audit diagnostic | fits | T0 P90 \|err\| °C | T41J P90 \|err\| °C |
| --- | --- | --- | --- |
| Jacobian condition number Q1 (lowest) | 4450 | 9.5 | 10.5 |
| Jacobian condition number Q2 | 4450 | 8.9 | 7.9 |
| Jacobian condition number Q3 | 4450 | 14.7 | 10.5 |
| Jacobian condition number Q4 (highest) | 4450 | 53.2 | 28.2 |
| starts within 1 % of best cost disagree on T0 by > 1 °C | 287 | 71.7 | 56.7 |
| starts within 1 % of best cost agree on T0 within 1 °C | 17513 | 17.6 | 12.6 |

### 2.7 Upper shelves that are not flat (Block E, added after Blocks A-D; D-047, D-051)

| design | noise | shelf_slope_fraction_of_use_per_100c | fits | share_trend_test_applicable | share_trend_flagged | share_trend_flagged_when_applicable | share_usable | use_error_rel_median | use_error_rel_p90_abs | t41_error_p90_abs_c | t0_error_p90_abs_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| upper shelf -20 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | -0.2 | 200 | 100 % | 86 % | 86 % | 78 % | -11 % | 13 % | 5 | 7 |
| upper shelf -20 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | -0.2 | 200 | 100 % | 36 % | 36 % | 70 % | -11 % | 14 % | 12 | 11.2 |
| upper shelf -20 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | -0.2 | 200 | 100 % | 88 % | 88 % | 34 % | -9 % | 11 % | 2.4 | 4.8 |
| upper shelf -20 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | -0.2 | 200 | 99 % | 44 % | 45 % | 40 % | -10 % | 13 % | 6.4 | 8.6 |
| upper shelf -10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | -0.1 | 200 | 100 % | 36 % | 36 % | 97 % | -6 % | 8 % | 4.3 | 5 |
| upper shelf -10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | -0.1 | 200 | 100 % | 11 % | 11 % | 79 % | -6 % | 9 % | 11.7 | 9 |
| upper shelf -10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | -0.1 | 200 | 100 % | 26 % | 26 % | 30 % | -5 % | 7 % | 2.7 | 3.8 |
| upper shelf -10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | -0.1 | 200 | 96 % | 12 % | 13 % | 42 % | -5 % | 8 % | 5.5 | 7 |
| upper shelf +10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | low | 0.1 | 200 | 100 % | 12 % | 12 % | 94 % | 7 % | 9 % | 4.2 | 5.6 |
| upper shelf +10 % of USE per 100 °C; uniform x -3..5, n=12 (upper shelf sampled to x = 5) | moderate | 0.1 | 200 | 100 % | 10 % | 10 % | 76 % | 6 % | 11 % | 10.3 | 10.2 |
| upper shelf +10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | low | 0.1 | 200 | 68 % | 10 % | 15 % | 78 % | 6 % | 8 % | 2.9 | 5.3 |
| upper shelf +10 % of USE per 100 °C; x = -2.5, -1, 0, 2, 4 x 3 specimens (n=15) | moderate | 0.1 | 200 | 60 % | 4 % | 8 % | 41 % | 7 % | 12 % | 5.5 | 10.9 |

### 2.8 Where the fitter stops being trustworthy

Of 89 scenarios with scatter in Blocks A-D: in 39, 90 % of all fits recover T41J, T0 and USE within the reference scales (10 °C, 10 °C, 10 %). In 10 more, only the fits that pass the flags do. In 14, fewer than 5 % of fits pass the flags: the method declines to report, which is the intended behaviour. In 26, 5 % or more of fits pass the flags yet the passing fits still miss at least one reference scale; these are where the fitter stops being trustworthy even with its diagnostics:

| scenario (block B/C/D designs, [scatter]) | usable | T41J P90 all / usable °C | T0 P90 all / usable °C | USE P90 all / usable |
| --- | --- | --- | --- | --- |
| uniform x -3..3, n=12 [high] | 57 % | 20.5 / 13.9 | 18.0 / 15.3 | 14 % / 10 % |
| uniform x -3..3, n=18 [high] | 67 % | 17.9 / 12.5 | 14.4 / 11.8 | 14 % / 13 % |
| uniform x -3..3, n=30 [high] | 82 % | 11.1 / 10.0 | 10.0 / 10.0 | 11 % / 10 % |
| uniform x -3..3, n=6 [high] | 13 % | 33.1 / 7.3 | 21.6 / 7.5 | 21 % / 11 % |
| uniform x -3..3, n=8 [high] | 28 % | 26.5 / 11.5 | 17.0 / 11.6 | 20 % / 13 % |
| 5 temperatures x 3 specimens, x = -2.5, -1, 0, 1, 2.5 (n=15) [high] | 40 % | 15.8 / 11.4 | 13.9 / 14.6 | 15 % / 16 % |
| clustered at centre: 2+2 shelf points, 8 in \|x\|<=0.5 (n=12) [high] | 72 % | 18.5 / 11.8 | 15.7 / 9.7 | 22 % / 20 % |
| clustered cold side: x -3..-0.5, n=12 [high] | 10 % | 13.2 / 15.0 | 45.5 / 54.8 | 345 % / 88 % |
| clustered cold side: x -3..-0.5, n=12 [moderate] | 6 % | 8.7 / 10.8 | 37.3 / 42.7 | 288 % / 85 % |
| shelves + 2 transition points (n=8) [high] | 30 % | 27.0 / 13.1 | 24.0 / 14.5 | 17 % / 12 % |
| shelves + 3 transition points (n=9) [high] | 44 % | 22.4 / 16.6 | 20.5 / 15.2 | 17 % / 13 % |
| x -0.5..3, n=12 (lower shelf missing) [high] | 8 % | 23.3 / 24.3 | 21.7 / 24.1 | 12 % / 11 % |
| x -0.5..3, n=12 (lower shelf missing) [moderate] | 6 % | 13.9 / – | 14.5 / 21.7 | 7 % / 4 % |
| x -1.5..3, n=12 (lower shelf weak) [high] | 18 % | 19.8 / 17.5 | 15.9 / 14.0 | 16 % / 14 % |
| x -3..0.5, n=12 (upper shelf missing) [high] | 12 % | 12.6 / 12.3 | 63.0 / 30.0 | 901 % / 58 % |
| x -3..1.5, n=12 (upper shelf weak) [high] | 23 % | 16.0 / 11.7 | 35.1 / 15.5 | 85 % / 21 % |
| x -3..1.5, n=12 (upper shelf weak) [moderate] | 26 % | 7.4 / 7.3 | 11.0 / 9.5 | 18 % / 14 % |
| C 60 °C (broad); 5 temperatures x 3 specimens (n=15) [moderate] | 64 % | 8.7 / 7.7 | 10.3 / 11.5 | 7 % / 7 % |
| C 60 °C (broad); uniform x -3..3, n=12 [moderate] | 98 % | 11.5 / 11.5 | 12.5 / 12.2 | 7 % / 7 % |
| USE 250 J; uniform x -3..3, n=12 [moderate] | 81 % | 11.8 / 10.8 | 8.6 / 8.2 | 8 % / 7 % |
| USE 44 J (41 J near upper shelf); 5 temperatures x 3 specimens (n=15) [moderate] | 60 % | 17.2 / 15.3 | 8.3 / 8.7 | 8 % / 9 % |
| USE 44 J (41 J near upper shelf); uniform x -3..3, n=12 [moderate] | 83 % | 23.5 / 19.7 | 11.0 / 10.0 | 10 % / 8 % |
| window 150 °C, n=9; true T0 +0 °C from centre; true C 60 °C [moderate] | 8 % | 11.1 / 16.7 | 22.1 / 7.9 | 24 % / 18 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 30 °C [moderate] | 44 % | 10.6 / 9.9 | 10.6 / 11.5 | 12 % / 10 % |
| window 250 °C, n=12; true T0 +60 °C from centre; true C 60 °C [moderate] | 5 % | 9.1 / 7.2 | 29.1 / 26.6 | 34 % / 25 % |
| window 250 °C, n=12; true T0 -60 °C from centre; true C 60 °C [moderate] | 6 % | 10.8 / 20.9 | 12.4 / 17.9 | 6 % / 9 % |

Scenarios in which the method declines (fewer than 5 % of fits pass):

| scenario (block B/C/D designs, [scatter]) | usable | T41J P90 all / usable °C | T0 P90 all / usable °C | USE P90 all / usable |
| --- | --- | --- | --- | --- |
| clustered cold side: x -3..-0.5, n=12 [low] | 0 % | 4.6 / – | 30.3 / – | 238 % / – |
| shelves + 1 transition point (n=7) [high] | 0 % | 31.1 / – | 45.9 / – | 21 % / – |
| shelves + 1 transition point (n=7) [low] | 0 % | 16.0 / – | 5.7 / – | 4 % / – |
| shelves + 1 transition point (n=7) [moderate] | 0 % | 16.2 / – | 13.9 / – | 10 % / – |
| shelves only, 0 transition points (n=6) [high] | 0 % | 90.1 / – | 74.3 / – | 22 % / – |
| shelves only, 0 transition points (n=6) [low] | 0 % | 89.0 / – | 73.0 / – | 5 % / – |
| shelves only, 0 transition points (n=6) [moderate] | 0 % | 89.8 / – | 73.7 / – | 10 % / – |
| x -3..0.5, n=12 (upper shelf missing) [low] | 0 % | 2.6 / – | 19.1 / – | 70 % / – |
| x -3..0.5, n=12 (upper shelf missing) [moderate] | 4 % | 6.9 / 6.0 | 59.8 / 21.0 | 686 % / 51 % |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 12 °C [moderate] | 0 % | 13.5 / – | 25.2 / – | 659 % / – |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 30 °C [moderate] | 0 % | 8.1 / – | 67.5 / – | 701 % / – |
| window 150 °C, n=9; true T0 +60 °C from centre; true C 60 °C [moderate] | 4 % | 9.4 / 6.5 | 103.9 / 42.7 | 597 % / 56 % |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 30 °C [moderate] | 0 % | 17.2 / – | 17.4 / – | 5 % / – |
| window 150 °C, n=9; true T0 -60 °C from centre; true C 60 °C [moderate] | 2 % | 20.8 / – | 32.9 / 49.5 | 9 % / 6 % |

## 3. Published data: primary cohort outcomes

Primary cohort: 170 curves, 2588 records (134 full-size, 36 miniature). Every curve was fitted; none was removed.

Mutually exclusive outcomes (first applicable category, D-046):

| outcome | curves | fit_quality_group | share |
| --- | --- | --- | --- |
| optimizer failure | 0 | optimizer failure | 0 % |
| non-physical | 71 | non-physical | 42 % |
| boundary-limited | 3 | boundary-limited | 2 % |
| weakly identified | 47 | weakly identified | 28 % |
| usable fit, index temperature unavailable | 13 | usable fit | 8 % |
| usable fit, index temperature calculated | 36 | usable fit | 21 % |
| TOTAL | 170 |  | 100 % |

Diagnostic flags (a curve can carry several):

| flag | meaning | curves |
| --- | --- | --- |
| flag_optimizer_failure | optimizer failure (no start converged) | 0 |
| flag_nonphysical_lse_at_zero | non-physical: fitted LSE at 0 J | 71 |
| flag_nonphysical_no_rise | non-physical: no rise (USE = LSE) | 0 |
| flag_nonphysical_t0_at_absolute_zero | non-physical: T0 at absolute zero | 0 |
| flag_boundary_c_min | boundary: C at 1 °C (width unresolved) | 3 |
| flag_boundary_c_max | boundary: C at the tested span | 0 |
| flag_boundary_t0_limit | boundary: T0 at a range limit | 0 |
| flag_boundary_rise_max | boundary: USE - LSE at 10x highest energy | 0 |
| flag_boundary_lse_max | boundary: LSE at highest energy | 0 |
| flag_weak_transition | weak: < 2 test temperatures inside T0 ± C | 5 |
| flag_weak_upper_shelf | weak: upper shelf not supported (< 2 specimens at >= 95 % of rise) | 29 |
| flag_nonflat_upper_shelf | model adequacy (not an outcome): upper-shelf residual trend (p < 0.05) | 8 |
| flag_weak_lower_shelf | weak: lower shelf not supported (< 2 specimens at <= 5 % of rise; LSE fitted) | 105 |
| flag_numerically_singular | ill-conditioned: Jacobian rank-deficient | 1 |
| flag_index_unavailable | index temperature not calculated (any reason) | 38 |

Index temperature by geometry (D-044, D-045):

| geometry_group | curves | criterion | basis | index_calculated | index_calculated_and_fit_usable | not_calculated | not_calculated_reasons |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full-size 55x10x10 mm, notch not reported | 74 | 41 J | 10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044) | 74 | 20 | 0 |  |
| full-size 55x10x10 mm, notch reported | 60 | 41 J | 10 CFR 50 App. G §II.E; ASTM E185-82 §4.15, §10.2.1 (D-044) | 58 | 16 | 2 | undefined: 41 J at or below the fitted LSE (1); unsupported: crossing below the lowest test temperature (1) |
| miniature: 20x1.5x1.5 a=0.33 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 20x2.5x2.5 a=0.38 | 5 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 5 | not calculated: no defensible criterion for this geometry (5) |
| miniature: 20x3.33x3.33 a=0.51 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 20x5x5 a=0.76 | 4 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 4 | not calculated: no defensible criterion for this geometry (4) |
| miniature: 23.6x3.33x3.33 a=0.51 | 7 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 7 | not calculated: no defensible criterion for this geometry (7) |
| miniature: 23.6x5x5 a=0.76 | 2 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 2 | not calculated: no defensible criterion for this geometry (2) |
| miniature: 23.6x5x5 a=0.78 | 1 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 1 | not calculated: no defensible criterion for this geometry (1) |
| miniature: 27.5x3.33x3.33 a=0.6 | 1 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 1 | not calculated: no defensible criterion for this geometry (1) |
| miniature: 27x3x4 a=1 | 8 | none established | ASTM E2248-18 §1.3, §5.2; no applicable correlation (D-045) | 0 | 0 | 8 | not calculated: no defensible criterion for this geometry (8) |

Where 41 J lies on the fitted rise (full-size curves with a calculated index; audit only, D-047):

| 41 J position on the fitted rise | curves | non-physical | weakly identified | usable fit, index temperature calculated |
| --- | --- | --- | --- | --- |
| below 11.9 % (flat lower part of the fit) | 15 | 3 | 3 | 9 |
| 11.9-88.1 % (inside T0 ± C) | 117 | 53 | 37 | 27 |

## 4. Where fits fail or are weak, against the WP2 sampling descriptors

| dimension | group | curves | optimizer failure | non-physical | boundary-limited | weakly identified | usable fit, index temperature unavailable | usable fit, index temperature calculated | share_not_usable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| material_family | 20MnMoNi55 | 8 | 0 | 1 | 0 | 2 | 0 | 5 | 0.375 |
| material_family | A302B | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| material_family | A508 | 95 | 0 | 47 | 1 | 24 | 4 | 19 | 0.758 |
| material_family | A533B | 61 | 0 | 19 | 2 | 19 | 9 | 12 | 0.656 |
| material_family | A533B weld metal | 4 | 0 | 3 | 0 | 1 | 0 | 0 | 1 |
| product_form_group | HAZ (incl. simulated) | 19 | 0 | 8 | 1 | 6 | 1 | 3 | 0.789 |
| product_form_group | forging | 84 | 0 | 43 | 1 | 20 | 4 | 16 | 0.762 |
| product_form_group | not determinable | 6 | 0 | 0 | 0 | 1 | 0 | 5 | 0.167 |
| product_form_group | plate | 57 | 0 | 17 | 1 | 19 | 8 | 12 | 0.649 |
| product_form_group | weld metal | 4 | 0 | 3 | 0 | 1 | 0 | 0 | 1 |
| irradiation | irradiated | 31 | 0 | 12 | 1 | 7 | 8 | 3 | 0.645 |
| irradiation | unirradiated | 139 | 0 | 59 | 2 | 40 | 5 | 33 | 0.727 |
| geometry_class | full-size (55x10x10 mm) | 134 | 0 | 56 | 1 | 41 | 0 | 36 | 0.731 |
| geometry_class | miniature (reduced length) | 36 | 0 | 15 | 2 | 6 | 13 | 0 | 0.639 |
| n_points_bin | 6-8 | 13 | 0 | 3 | 1 | 8 | 1 | 0 | 0.923 |
| n_points_bin | 9-11 | 56 | 0 | 30 | 0 | 15 | 0 | 11 | 0.804 |
| n_points_bin | 12-14 | 41 | 0 | 16 | 1 | 11 | 7 | 6 | 0.683 |
| n_points_bin | 15-19 | 29 | 0 | 8 | 0 | 9 | 5 | 7 | 0.586 |
| n_points_bin | 20+ | 31 | 0 | 14 | 1 | 4 | 0 | 12 | 0.613 |
| wp2_transition_temperatures | 2 | 6 | 0 | 2 | 1 | 3 | 0 | 0 | 1 |
| wp2_transition_temperatures | 3 | 24 | 0 | 10 | 0 | 7 | 2 | 5 | 0.708 |
| wp2_transition_temperatures | 4-5 | 78 | 0 | 36 | 1 | 20 | 6 | 15 | 0.731 |
| wp2_transition_temperatures | 6+ | 62 | 0 | 23 | 1 | 17 | 5 | 16 | 0.661 |
| wp2_lower_band_temperatures | 1 | 31 | 0 | 8 | 0 | 20 | 2 | 1 | 0.903 |
| wp2_lower_band_temperatures | 2 | 64 | 0 | 35 | 1 | 17 | 4 | 7 | 0.828 |
| wp2_lower_band_temperatures | 3+ | 75 | 0 | 28 | 2 | 10 | 7 | 28 | 0.533 |
| wp2_upper_band_temperatures | 2 | 25 | 0 | 12 | 1 | 8 | 1 | 3 | 0.84 |
| wp2_upper_band_temperatures | 3 | 62 | 0 | 27 | 1 | 15 | 2 | 17 | 0.694 |
| wp2_upper_band_temperatures | 4+ | 83 | 0 | 32 | 1 | 24 | 10 | 16 | 0.687 |
| temperature_span | <=150 °C | 23 | 0 | 14 | 0 | 6 | 3 | 0 | 0.87 |
| temperature_span | 150-250 °C | 64 | 0 | 25 | 3 | 15 | 2 | 19 | 0.672 |
| temperature_span | 250-350 °C | 58 | 0 | 21 | 0 | 22 | 3 | 12 | 0.741 |
| temperature_span | >350 °C | 25 | 0 | 11 | 0 | 4 | 5 | 5 | 0.6 |

Residual pattern behind the lower shelf at 0 J (measured minus fitted, % of fitted USE; added after the fits existed, D-051):

| geometry_category | lse_at_zero | curves | mean residual, x <= -1.5 (fitted lower shelf), % of USE | curves with points, x <= -1.5 (fitted lower shelf) | mean residual, -1.5 < x <= -0.5 (lower transition), % of USE | curves with points, -1.5 < x <= -0.5 (lower transition) | mean residual, -0.5 < x < 0.5 (middle), % of USE | curves with points, -0.5 < x < 0.5 (middle) | mean residual, 0.5 <= x < 1.5 (upper transition), % of USE | curves with points, 0.5 <= x < 1.5 (upper transition) | median C (°C) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | False | 78 | -0.44 | 62 | 0.48 | 76 | -0.41 | 76 | 1.24 | 74 | 40.94 |
| full-size | True | 56 | 0.12 | 30 | -2.81 | 55 | 1.67 | 55 | -1.54 | 54 | 50.83 |
| miniature | False | 21 | -0.44 | 19 | 0.04 | 18 | -0.42 | 20 | 2.76 | 19 | 29.15 |
| miniature | True | 15 | 1.14 | 8 | -5.96 | 15 | 2.86 | 15 | -1.43 | 15 | 34.75 |

## 5. Fitted parameters (usable fits)

| geometry_category | parameter | curves | minimum | p10 | median | p90 | maximum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | LSE (J) | 36 | 0.398 | 1.001 | 8.25 | 27.66 | 32.58 |
| full-size | USE (J) | 36 | 71.29 | 127.9 | 205.8 | 263.8 | 393.6 |
| full-size | T0 (°C) | 36 | -87.88 | -74.75 | -17.04 | 32.73 | 100.2 |
| full-size | C (°C) | 36 | 15.1 | 24.07 | 34.11 | 47.46 | 58.2 |
| full-size | T41J (°C) | 36 | -132.2 | -101.5 | -50.04 | 27.24 | 78.4 |
| miniature | LSE (J) | 13 | 0.299 | 0.336 | 1.012 | 1.576 | 2.177 |
| miniature | USE (J) | 13 | 3.32 | 3.698 | 7.929 | 12.82 | 29.08 |
| miniature | T0 (°C) | 13 | -157.5 | -138.3 | -50.1 | 195.1 | 202.3 |
| miniature | C (°C) | 13 | 17.41 | 18.95 | 29.16 | 61.11 | 78.43 |

Extremes (all primary fits):

| parameter | which | curve_id | value | outcome | outcome_reason | material_family | product_form | irradiated | geometry | n_points | T_min_c | T_max_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| use_j | minimum | 53-241 | 0.979 | non-physical | nonphysical_lse_at_zero | A533B weld metal | weld metal | False | 20x1.5x1.5 a=0.33 | 11 | -159.9 | 39.73 |
| use_j | maximum | 12-54 | 426.3 | weakly identified | weak_upper_shelf | A508 | forging | False | 55x10x10 a=2 | 13 | -69.93 | 79.76 |
| t0_c | minimum | 109-287 | -157.5 | usable fit, index temperature unavailable | not calculated: no defensible criterion for this geometry | A508 | forging | True | 27x3x4 a=1 | 13 | -200 | 200 |
| t0_c | maximum | 55-257 | 202.3 | usable fit, index temperature unavailable | not calculated: no defensible criterion for this geometry | A533B | plate | True | 23.6x5x5 a=0.76 | 12 | -49.8 | 377.6 |
| c_c | minimum | 53-230 | 1 | boundary-limited | boundary_c_min | A533B | plate | False | 20x3.33x3.33 a=0.51 | 20 | -196 | 19.93 |
| c_c | maximum | 109-293 | 196.8 | weakly identified | weak_upper_shelf, weak_lower_shelf | A508 | forging | True | 27x3x4 a=1 | 13 | -160 | 350 |
| index_temperature_c | minimum | 17-83 | -165 | weakly identified | weak_lower_shelf | A508 | forging | False | 55x10x10 a=? | 10 | -196.3 | 99.66 |
| index_temperature_c | maximum | 55-255 | 213.6 | weakly identified | weak_lower_shelf | A533B | plate | True | 55x10x10 a=2 | 10 | 23.75 | 343.1 |
| lse_j | minimum | 53-241 | 0 | non-physical | nonphysical_lse_at_zero | A533B weld metal | weld metal | False | 20x1.5x1.5 a=0.33 | 11 | -159.9 | 39.73 |
| lse_j | maximum | 12-49 | 81.31 | boundary-limited | boundary_c_min | A508 | forging | False | 55x10x10 a=2 | 14 | -79.06 | 79.16 |

## 6. Lower-shelf sensitivity on the published curves (declared in D-042 before fitting)

Refit with LSE fixed at 2.7 J (full-size) or 0.1 J (miniature); differences only, outcome counts are not compared.

| geometry_category | quantity | curves_compared | median | median_abs | p90_abs | max_abs |
| --- | --- | --- | --- | --- | --- | --- |
| full-size | T41J (fixed - fitted), °C | 132 | -0.15 | 0.287 | 1.894 | 15.36 |
| full-size | T0 (fixed - fitted), °C | 134 | 0.195 | 0.73 | 5.341 | 252.6 |
| full-size | USE (fixed / fitted - 1) | 134 | -0.001 | 0.002 | 0.024 | 7.303 |
| miniature | T0 (fixed - fitted), °C | 36 | -0.073 | 1.156 | 7.346 | 12.47 |
| miniature | USE (fixed / fitted - 1) | 36 | -0 | 0.003 | 0.025 | 0.235 |

## 7. Dataset-provided USE and DBTT (diagnostic only, D-049)

| geometry_category | fit_usable | curves | with_dataset_use | with_dataset_dbtt | use_ratio_median | use_ratio_p10 | use_ratio_p90 | share_use_within_10pct | t41_minus_dbtt_median_c | t41_minus_dbtt_median_abs_c | share_t41_within_10c | t0_minus_dbtt_median_c | t0_minus_dbtt_median_abs_c | share_t0_within_10c | dbtt_closer_to_t41j | dbtt_closer_to_t0 | dataset_use_below_41j |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-size | False | 98 | 97 | 98 | 0.999 | 0.971 | 1 | 0.939 | -31.3 | 31.88 | 0.104 | -0.044 | 2.912 | 0.867 | 3 | 93 | 0 |
| full-size | True | 36 | 35 | 36 | 1 | 1 | 1 | 0.972 | -26.15 | 26.15 | 0.028 | 0.904 | 3.27 | 0.833 | 1 | 35 | 0 |
| miniature | False | 23 | 23 | 23 | 0.994 | 0.949 | 1 | 0.87 |  |  |  | -6.521 | 9.04 | 0.565 | 0 | 0 | 22 |
| miniature | True | 13 | 13 | 13 | 1 | 1 | 1.007 | 0.923 |  |  |  | 3.955 | 6.683 | 0.692 | 0 | 0 | 13 |

## 8. Looser and stricter cohorts (diagnostic, D-050)

| outcome | curves | fit_quality_group | share | cohort |
| --- | --- | --- | --- | --- |
| optimizer failure | 0 | optimizer failure | 0 % | looser |
| non-physical | 71 | non-physical | 39 % | looser |
| boundary-limited | 4 | boundary-limited | 2 % | looser |
| weakly identified | 57 | weakly identified | 31 % | looser |
| usable fit, index temperature unavailable | 13 | usable fit | 7 % | looser |
| usable fit, index temperature calculated | 37 | usable fit | 20 % | looser |
| TOTAL | 182 |  | 100 % | looser |
| optimizer failure | 0 | optimizer failure | 0 % | primary |
| non-physical | 71 | non-physical | 42 % | primary |
| boundary-limited | 3 | boundary-limited | 2 % | primary |
| weakly identified | 47 | weakly identified | 28 % | primary |
| usable fit, index temperature unavailable | 13 | usable fit | 8 % | primary |
| usable fit, index temperature calculated | 36 | usable fit | 21 % | primary |
| TOTAL | 170 |  | 100 % | primary |
| optimizer failure | 0 | optimizer failure | 0 % | stricter |
| non-physical | 23 | non-physical | 38 % | stricter |
| boundary-limited | 1 | boundary-limited | 2 % | stricter |
| weakly identified | 8 | weakly identified | 13 % | stricter |
| usable fit, index temperature unavailable | 9 | usable fit | 15 % | stricter |
| usable fit, index temperature calculated | 19 | usable fit | 32 % | stricter |
| TOTAL | 60 |  | 100 % | stricter |

## 9. Example figures

- `synthetic_examples.png`: SYNTHETIC good versus poor sampling (spread of 40 replicate fits).
- `synthetic_error_vs_specimens.png`, `synthetic_sampling_patterns.png`: SYNTHETIC validation summaries.
- `fits_published_examples.png`: published curves: clearly successful fit (2-9); converged but weakly identified (53-234); non-physical (54-246); boundary-limited (53-230).
- `fits_outcome_by_sampling.png`: outcome shares against WP2 sampling descriptors.
