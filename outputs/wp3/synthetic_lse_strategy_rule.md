# SYNTHETIC: lower-shelf strategy comparison (Block L, D-042)

Data type: SYNTHETIC (fitter validation; not published measurements).

Key temperature: T41J from the analytic crossing (full-size truths) or T0 (miniature-scale truths). Score = mean over synthetic data sets of the 90th percentile of |error| (°C). Missing = share of replicates without a key temperature.

| lse_strategy | score_mean_p90_c | mean_missing_share | score_full-size_c | score_miniature_c | cohort_weighted_score_c_not_used_by_rule | cohort_weight_full_size | eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fitted | 12.62 | 0.018 | 11.95 | 12.96 | 12.16 | 0.788 | True |
| fixed_convention | 11.93 | 0 | 10.13 | 12.83 | 10.7 | 0.788 | True |
| fixed_zero | 14.6 | 0 | 9.797 | 17 | 11.32 | 0.788 | True |
| hybrid | 12.06 | 0.01 | 11.66 | 12.27 | 11.79 | 0.788 | True |

**Rule outcome: `fitted`** (rule 3: no strategy at least 10 % better; 'fitted' within 10 % of the lowest score).
