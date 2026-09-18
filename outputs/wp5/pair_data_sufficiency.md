# WP5 - specimen-size pair inventory and data sufficiency

Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort (170 curves). Every row here describes PUBLISHED MEASURED DATA and FITTED PARAMETERS from it; nothing is normalized or transformed in this file. Pair matching rules: DECISIONS.md D-068; match classes: D-069; families: D-070.

**This inventory was produced before any size-normalization result existed.** Match classes are decided from provenance metadata alone and are not revised after seeing how well a normalization works.

## 1. What had to agree

Two curves are treated as the same material and condition measured at two specimen geometries only if every field below agrees. A field blank on both sides counts as agreement (the publication reported it for neither curve); a field blank on one side only is a provenance gap; a recorded disagreement rejects the pair.

| field | meaning | required present for STRICT |
| --- | --- | --- |
| material_family | material family | yes |
| material_std | material designation (specification, type/grade, class, weld-metal label) | yes |
| product_form | product form | yes |
| composition_signature | heat chemistry (the heat/lot proxy; the dataset has no heat identifier) | yes |
| irradiated_resolved | irradiation status | yes |
| fluence_n_per_cm2 | fluence | yes |
| irradiation_temp_c | irradiation temperature | no |
| irradiation_time_h | irradiation time | no |
| treatment | heat treatment | no |
| post_treatment_temp_c | post-treatment temperature | no |
| post_treatment_time_h | post-treatment time | no |
| cooling_method | cooling method | no |
| cooling_rate_c_per_min | cooling rate | no |
| test_condition_statement | test-condition statement (HAZ location, reconstituted, welded area, striking velocity) | yes |
| tag_reconstituted_specimen | reconstituted-specimen status | yes |
| orientation | specimen orientation | no |

## 2. Candidate pairs and why they were rejected

All 4824 ordered (smaller-geometry curve, full-size curve) pairs of the frozen primary cohort were enumerated (36 smaller-specimen curves x 134 full-size curves).

| match_class | pairs |
| --- | --- |
| NOT MATCHED (a recorded field disagrees) | 4806 |
| STRICT (same study, no conflict, no one-sided gap) | 18 |

## 3. How much matched evidence there is

| subset | comparisons | families | studies | heats | geometry_combinations | both_wp3_usable | product_forms | irradiation_states |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STRICT matches | 18 | 10 | 5 | 6 | 8 | 6 | forging: 5; plate: 10; weld metal: 3 | unirradiated: 11; irradiated: 7 |
| PARTIAL matches | 0 | 0 | 0 | 0 | 0 | 0 |  |  |
| STRICT + PARTIAL | 18 | 10 | 5 | 6 | 8 | 6 | forging: 5; plate: 10; weld metal: 3 | unirradiated: 11; irradiated: 7 |
| STRICT and both WP3 fits usable (candidate PRIMARY analysis set) | 6 | 4 | 3 | 3 | 4 | 6 | forging: 1; plate: 5 | unirradiated: 1; irradiated: 5 |

## 4. Independence: comparisons are not independent material observations

One full-size curve paired with several smaller geometries gives several comparisons of ONE material in ONE condition. The family is the unit of independence.

| family_id | comparisons | smaller_geometries | study | material | product_form | irradiated | fluence_n_per_cm2 | full_size_curve | full_size_wp3_outcome | full_size_t41j_c | smaller_curves | comparisons_both_wp3_usable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R107-107-282-unirradiated | 1 | 27x3x4 a=1 | 107 | A508, grade/class not stated | forging | False |  | 107-282 | usable fit, index temperature calculated | -27.58 | 107-283 | 1 |
| R53-53-225-unirradiated | 3 | 20x1.5x1.5 a=0.33; 20x3.33x3.33 a=0.51; 20x5x5 a=0.76 | 53 | Weld metal from an A533B weldment | weld metal | False |  | 53-225 | usable fit, index temperature calculated | -54.41 | 53-229; 53-233; 53-241 | 0 |
| R55-55-254-unirradiated | 2 | 23.6x3.33x3.33 a=0.51; 23.6x5x5 a=0.76 | 55 | A533 Type B, class not stated | plate | False |  | 55-254 | weakly identified | 114.6 | 55-256; 55-258 | 0 |
| R55-55-255-1e+19 n/cm2 | 2 | 23.6x3.33x3.33 a=0.51; 23.6x5x5 a=0.76 | 55 | A533 Type B, class not stated | plate | True | 1e+19 | 55-255 | usable fit, index temperature calculated | 213.5 | 55-257; 55-259 | 2 |
| R59-59-266-unirradiated | 2 | 20x2.5x2.5 a=0.38; 23.6x3.33x3.33 a=0.51 | 59 | A533 Type B, class not stated | plate | False |  | 59-266 | usable fit, index temperature calculated | -47.13 | 59-269; 59-271.2 | 0 |
| R59-59-267-1.3e+18 n/cm2 | 2 | 20x2.5x2.5 a=0.38; 23.6x3.33x3.33 a=0.51 | 59 | A533 Type B, class not stated | plate | True | 1.3e+18 | 59-267 | usable fit, index temperature calculated | -20.27 | 59-270; 59-272 | 2 |
| R59-59-268-2.7e+19 n/cm2 | 1 | 23.6x3.33x3.33 a=0.51 | 59 | A533 Type B, class not stated | plate | True | 2.7e+19 | 59-268 | usable fit, index temperature calculated | -20.24 | 59-271.1 | 1 |
| R59-59-274-unirradiated | 2 | 20x2.5x2.5 a=0.38; 23.6x3.33x3.33 a=0.51 | 59 | A508, grade/class not stated | forging | False |  | 59-274 | usable fit, index temperature calculated | -63.49 | 59-276; 59-278 | 0 |
| R59-59-275-1.3e+18 n/cm2 | 2 | 20x2.5x2.5 a=0.38; 23.6x3.33x3.33 a=0.51 | 59 | A508, grade/class not stated | forging | True | 1.3e+18 | 59-275 | usable fit, index temperature calculated | -39.64 | 59-277; 59-279 | 0 |
| R60-60-280-unirradiated | 1 | 27.5x3.33x3.33 a=0.6 | 60 | A533 Type B, class not stated | plate | False |  | 60-280 | usable fit, index temperature calculated | -40.13 | 60-281 | 0 |

## 5. Smaller-specimen geometries: how many reach a matched full-size partner

| geometry | curves | studies | strict_comparisons | families |
| --- | --- | --- | --- | --- |
| 20x1.5x1.5 a=0.33 | 4 | 1 | 1 | 1 |
| 20x2.5x2.5 a=0.38 | 5 | 1 | 4 | 4 |
| 20x3.33x3.33 a=0.51 | 4 | 1 | 1 | 1 |
| 20x5x5 a=0.76 | 4 | 1 | 1 | 1 |
| 23.6x3.33x3.33 a=0.51 | 7 | 2 | 7 | 7 |
| 23.6x5x5 a=0.76 | 2 | 1 | 2 | 2 |
| 23.6x5x5 a=0.78 | 1 | 1 | 0 | 0 |
| 27.5x3.33x3.33 a=0.6 | 1 | 1 | 1 | 1 |
| 27x3x4 a=1 | 8 | 2 | 1 | 1 |

## 5b. Smaller-specimen curves with no STRICT full-size partner

| curve_id | ref_id | geometry | material_std | product_form | irradiated | n_points | wp3_outcome | same_study_full_size_candidates | reason_no_strict_partner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 109-286 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | False | 15 | usable fit, index temperature unavailable | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-287 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | True | 13 | usable fit, index temperature unavailable | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-288 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | False | 10 | weakly identified | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-289 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | True | 12 | boundary-limited | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-290 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | False | 15 | usable fit, index temperature unavailable | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-292 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | False | 11 | boundary-limited | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 109-293 | 109 | 27x3x4 a=1 | A508, grade/class not stated | forging | True | 13 | weakly identified | 0 | the publication contributes no full-size curve to the frozen primary cohort |
| 52-221 | 52 | 23.6x5x5 a=0.78 | A533 Type B, class not stated | plate | True | 12 | usable fit, index temperature unavailable | 0 | the publication contributes no full-size curve to the frozen primary cohort (its full-size curves left at WP1 step E8 as republications of ref 55's tests, D-019) |
| 53-226 | 53 | 20x5x5 a=0.76 | A533 Type B, class not stated | plate | False | 23 | boundary-limited | 1 | recorded disagreement in material family |
| 53-227 | 53 | 20x5x5 a=0.76 | A533 Type B, class not stated | HAZ | False | 24 | boundary-limited | 1 | recorded disagreement in material family |
| 53-228 | 53 | 20x5x5 a=0.76 | A533 Type B, class not stated | HAZ | False | 19 | usable fit, index temperature unavailable | 1 | recorded disagreement in material family |
| 53-230 | 53 | 20x3.33x3.33 a=0.51 | A533 Type B, class not stated | plate | False | 20 | boundary-limited | 1 | recorded disagreement in material family |
| 53-231 | 53 | 20x3.33x3.33 a=0.51 | A533 Type B, class not stated | HAZ | False | 14 | weakly identified | 1 | recorded disagreement in material family |
| 53-232 | 53 | 20x3.33x3.33 a=0.51 | A533 Type B, class not stated | HAZ | False | 22 | boundary-limited | 1 | recorded disagreement in material family |
| 53-234 | 53 | 20x1.5x1.5 a=0.33 | A533 Type B, class not stated | plate | False | 8 | weakly identified | 1 | recorded disagreement in material family |
| 53-235 | 53 | 20x1.5x1.5 a=0.33 | A533 Type B, class not stated | HAZ | False | 11 | boundary-limited | 1 | recorded disagreement in material family |
| 53-244 | 53 | 20x1.5x1.5 a=0.33 | A533 Type B, class not stated | HAZ | True | 8 | boundary-limited | 1 | recorded disagreement in material family |
| 59-273 | 59 | 20x2.5x2.5 a=0.38 | A533 Type B, class not stated | plate | True | 12 | usable fit, index temperature unavailable | 5 | recorded disagreement in fluence; recorded disagreement in irradiation status; recorded disagreement in material family |

## 6. Sufficiency verdict

- STRICT matched geometry comparisons: **18**, from **10** independent material-condition families in **5** publications.
- Of those, **6** comparisons (4 families) have a usable WP3 fit on BOTH curves.
- Smaller-specimen geometries represented among STRICT comparisons: **8** of 9 in the cohort.
- Product forms among STRICT families: forging (3); plate (6); weld metal (1).
- Irradiation states among STRICT families: unirradiated (6); irradiated (4).

The size-correction analysis proceeds on this evidence, and every summary it produces is reported with these counts beside it. Whether the counts support a general size-correction uncertainty is answered in `wp5_summary.md` against the pre-registered evidence thresholds of DECISIONS.md D-079.
