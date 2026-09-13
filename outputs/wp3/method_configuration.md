# WP3 method configuration (generated from src/wp3_fitter.py and src/wp3_validation.py)

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
