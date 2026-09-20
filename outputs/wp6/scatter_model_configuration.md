# WP6 scatter models - calibration and the central choice

SYNTHETIC (Monte Carlo test-matrix study; not published measurements)

The pool is empirical published-data residual scatter (D-061): specimen-to-specimen variation plus between-laboratory, machine, calibration and reporting differences, digitization error and tanh model-shape error. NOT material scatter.

## Pre-declared selection criterion (D-094)
The central model must lie within +/- 25 % of the WP4 empirical SD/USE in **all five** regions and within
+/- 15 % at the 41 J crossing of the median archetype A5; ties broken toward the candidate needing no fitted
parameter; if none qualifies, C1 by default. Evaluated on these calibration diagnostics only, which contain no
headline simulation result.

## C1 (CENTRAL, D-095)
sd = USE_true x s(region), with s read at full precision from outputs/wp4/published_residual_scatter_summary.csv
(full-size, usable WP3 fits, leverage-adjusted residual / fitted USE, SD column). Nothing is fitted, so C1 reproduces every region
of the measured profile by construction and passes the criterion trivially.

## C2 (mandatory sensitivity)
sd(T) = sigma_T |dE/dT| + cv E(T) + 3 cv LSE, calibrated by the declared D-094 procedure:
**sigma_T = 7.3816 deg C, cv = 0.056948**.

| region | empirical SD/USE | C2 SD/USE | ratio |
| --- | --- | --- | --- |
| lower shelf (x <= -1.5) | 0.03608 | 0.01009 | 0.28 |
| lower transition (-1.5 < x <= -0.5) | 0.07294 | 0.05099 | 0.699 |
| central transition (-0.5 < x < 0.5) | 0.1052 | 0.1146 | 1.09 |
| upper transition (0.5 <= x < 1.5) | 0.09983 | 0.09214 | 0.923 |
| upper shelf (x >= 1.5) | 0.06158 | 0.06435 | 1.045 |

C2 is within +/- 25 % in all five regions: **False**. The 41 J crossing of A5 lies at
x = -0.712, i.e. in the **lower transition (-1.5 < x <= -0.5)** region.

## C3 (mandatory sensitivity), centred
Region-wise resampling of the WP4 leverage-adjusted residual / USE observations with that region's empirical
mean subtracted, so the model is zero-mean and directly comparable with C1 and C2. The lower-shelf
+0.014854 x USE offset is a model-convention / model-shape bias and is **never** injected as if it
were random specimen scatter. **C3-uncentered** keeps the region means and is reported separately as an
"empirical residual + model-shape / systematic-region-bias" sensitivity, not as the main C3 case.

## Miniature scatter
Central: the same relative profile at both specimen sizes. Required sensitivity: the WP4 miniature profile
(central transition 0.1670 against 0.1052, a factor
1.59), from 13 curves - explicitly weakly supported.

## Directional asymmetry, recorded so the choice cannot be mistaken for tuning (D-095)
RMSE_mini is approximately sqrt(V_sampling(N_mini) + bias^2 + SD_correction^2), which has a floor that the
full-size sampling variance does not. **Understating the scatter favours full-size; overstating it favours
miniature.** The central model was chosen on the calibration diagnostic above, before any headline cell was run,
and all candidates are run regardless.
