# WP4 method configuration (generated from src/wp4_bootstrap.py, src/wp4_validation.py, src/wp4_uncertainty.py)

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
