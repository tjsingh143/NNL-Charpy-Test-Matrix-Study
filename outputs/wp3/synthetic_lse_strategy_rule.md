# SYNTHETIC: lower-shelf strategy comparison (Block L, D-042)

Data type: SYNTHETIC (fitter validation; not published measurements).

Key temperature: T41J from the analytic crossing (full-size truths) or T0 (miniature-scale truths). Score = mean over synthetic data sets of the 90th percentile of |error| (°C). Missing = share of replicates without a key temperature.

| lse_strategy | score_mean_p90_c | mean_missing_share | score_full-size_c | score_miniature_c | cohort_weighted_score_c_not_used_by_rule | cohort_weight_full_size | eligible | role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fitted | 12.62 | 0.018 | 11.95 | 12.96 | 12.16 | 0.788 | True | pre-registered Block L candidate |
| fixed_convention | 11.93 | 0 | 10.13 | 12.83 | 10.7 | 0.788 | True | pre-registered Block L candidate |
| fixed_zero | 14.6 | 0 | 9.797 | 17 | 11.32 | 0.788 | True | pre-registered Block L candidate |
| hybrid | 12.06 | 0.01 | 11.66 | 12.27 | 11.79 | 0.788 | True | pre-registered Block L candidate |
| geometry_specific | 12.02 | 0 | 10.13 | 12.96 | 10.73 | 0.788 | not a rule candidate | final primary method (CP3 author decision); assembled from fixed_convention (full-size) and fitted (miniature); not a rule candidate |

**Rule outcome: `fitted`** (rule 3: no strategy at least 10 % better; 'fitted' within 10 % of the lowest score).

**CP3 amendment (author, 2026-09-14; D-042).** The pre-registered rule's outcome above is kept as history and is reproduced on every run. The final primary method is `geometry_specific` (geometry-specific: LSE fixed at 2.7 J (full-size), fitted >= 0 J (miniature)), chosen by the author on the literature, the intended estimand (full-size T41J) and the full-size synthetic results, after the rule's equal weighting of synthetic data sets was found to weight miniature truths about 2 : 1 against full-size truths. Its row is assembled from the candidates whose fits it reproduces exactly and is descriptive: it is not a candidate of the rule and selected nothing. The all-fitted method (`fitted`) is kept as an explicit sensitivity case.
