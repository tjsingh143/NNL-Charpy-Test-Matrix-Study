# WP2 summary (q4x6v-dyt25)

Dataset: Materials Cloud 2025.30, record q4x6v-dyt25 (DOI 10.24435/materialscloud:p6-5y, issued 2025-02-26)

Analysis of published Charpy V-notch test data. Nothing is fitted in WP2; the dataset's USE, DBTT and curve IDs are provenance only.

## 1. What one transition curve is (D-032, D-033)

Records form one curve only if they come from the same source publication and the same dataset series, and agree on every field below; a dataset series is split wherever any of these fields differs. Blank values count as their own value (never filled in).

| group | fields | reason |
| --- | --- | --- |
| source | ref_id, curve_id_dataset | different laboratories and figure series are never pooled into one curve |
| material and heat | material_std, composition_signature, product_form | specification/class, heat chemistry (heat proxy) and product form change toughness |
| specimen geometry | length_mm, width_mm, thickness_mm, notch_depth_mm, notch_angle_deg, notch_root_radius_mm, orientation | size, notch and orientation change absorbed energy and the transition |
| irradiation | irradiated_resolved, fluence_level, irradiation_temp_c, irradiation_time_h | neutron exposure and its temperature shift the transition |
| material / specimen condition | treatment, post_treatment_temp_c, post_treatment_time_h, cooling_method, cooling_rate_c_per_min, test_condition_statement | heat treatment, HAZ zone, reconstitution, welded area, loading rate |

## 2. Population accounting (records retained by WP1 -> primary RPV population)

Every record is counted once, at the first step that applies. Nothing is deleted: excluded and secondary records keep curve IDs.

| step | criterion | basis | records | curves | references |
| --- | --- | --- | --- | --- | --- |
| Start | Records retained by WP1 (canonical keep rule) | outputs/wp1*/reconciliation_table.md | 3198 | 233 | 56 |
| P1 | excluded: specimen type not supported as ordinary Charpy V-notch | CP1 decision 2; D-020 | 0 | 0 | 0 |
| P2 | excluded: condition label contradicted by the source | D-031 | 46 | 6 | 1 |
| P3 | excluded: irradiation status unresolved between releases | CP1 decision 1; D-021; D-035 | 138 | 11 | 4 |
| P4 | secondary: SA508 Gr.1A main-steam-line piping steel | CP1 decision 3; D-027 | 212 | 19 | 5 |
| P5 | secondary: additively manufactured SA508 Gr.3 (not an RPV product form) | D-034 (provisional, CP2) | 66 | 5 | 1 |
| End | primary RPV population |  | 2736 | 192 | 47 |

## 3. Curve inventory before inclusion filtering (primary population)

- Curves: 192; records: 2736; references: 47.
- Points per curve: median 12, 10th-90th percentile 7-23, range 1-95.
- Temperature span per curve: median 247 °C, 10th-90th percentile 140-363 °C.
- Distinct test temperatures in the transition band: median 5; curves with none: 5.
- Spearman rank correlation of energy with temperature below 0.7 (diagnostic only): 7 curves.

What the points cover (primary thresholds):

| sampling_class | curves | records |
| --- | --- | --- |
| brackets the transition (lower side, transition and upper shelf sampled) | 171 | 2593 |
| fewer than 2 transition temperatures | 7 | 55 |
| lower shelf not approached | 9 | 75 |
| lower shelf not approached; fewer than 2 transition temperatures | 2 | 8 |
| too few points to describe | 3 | 5 |

Points per curve:

| points | curves |
| --- | --- |
| 1-4 | 7 |
| 5 | 1 |
| 6-7 | 12 |
| 8-9 | 23 |
| 10-11 | 46 |
| 12-14 | 43 |
| 15-19 | 29 |
| 20-29 | 23 |
| 30+ | 8 |

## 4. Inclusion rules (D-038)

| rule | min_points_unirradiated | min_points_irradiated | min_T_transition | min_T_upper | min_points_upper | min_T_lower | max_energy_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| looser | 5 | 5 | 1 | 1 | 1 | 1 | 0.3 |
| primary | 6 | 6 | 2 | 2 | 2 | 1 | 0.2 |
| stricter | 15 | 12 | 3 | 2 | 3 | 2 | 0.15 |

| criterion | basis |
| --- | --- |
| points | 5 = fewest that leave one residual degree of freedom for a 4-parameter tanh; 6 = two; 15 unirradiated / 12 irradiated = ASTM E185-82 §6.3 minimum Charpy specimens for a baseline curve / per irradiated capsule |
| transition temperatures | 1 locates the transition; 2 fix location and width (T0 and C); 3 add one check on the shape |
| upper band | 1 = no requirement; 2 distinct temperatures show the rise has stopped; 3 specimens = ASTM E185-82 §4.18 upper-shelf energy is the average of normally three specimens |
| energy ratio | lowest energy / upper reference: the coldest point lies at or below the lower band edge (T0 - C) whenever the true lower-to-upper shelf ratio is at most 0.20 (limit 0.30), 0.09 (limit 0.20), 0.03 (limit 0.15) |

## 5. What each rule keeps

| rule | curves | records | curves_lost | records_lost | median_points | median_T_span_c | median_transition_temperatures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| before inclusion filtering | 192 | 2736 | 0 | 0 | 12 | 247.2 | 5 |
| looser | 182 | 2692 | 10 | 44 | 12 | 249.7 | 5 |
| primary | 170 | 2588 | 22 | 148 | 12 | 249.9 | 5 |
| stricter | 60 | 1333 | 132 | 1403 | 19 | 223.9 | 6 |

Curves failing each criterion (a curve can fail several):

| rule | criterion | curves_failing | curves_failing_only_this |
| --- | --- | --- | --- |
| looser | points | 7 | 0 |
| looser | transition temperatures | 5 | 0 |
| looser | upper band | 1 | 0 |
| looser | lower band temperatures | 0 | 0 |
| looser | energy ratio | 7 | 3 |
| primary | points | 8 | 1 |
| primary | transition temperatures | 12 | 5 |
| primary | upper band | 3 | 0 |
| primary | lower band temperatures | 0 | 0 |
| primary | energy ratio | 14 | 9 |
| stricter | points | 117 | 62 |
| stricter | transition temperatures | 19 | 0 |
| stricter | upper band | 25 | 3 |
| stricter | lower band temperatures | 47 | 8 |
| stricter | energy ratio | 22 | 2 |

By material family, product form, irradiation status and geometry:

| dimension | group | curves_before | records_before | curves_looser | records_looser | curves_primary | records_primary | curves_stricter | records_stricter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| material_family | 20MnMoNi55 | 8 | 178 | 8 | 178 | 8 | 178 | 5 | 140 |
| material_family | A302B | 2 | 38 | 2 | 38 | 2 | 38 | 2 | 38 |
| material_family | A508 | 106 | 1337 | 100 | 1309 | 95 | 1260 | 24 | 456 |
| material_family | A533B | 72 | 1105 | 68 | 1089 | 61 | 1034 | 26 | 632 |
| material_family | A533B weld metal | 4 | 78 | 4 | 78 | 4 | 78 | 3 | 67 |
| product_form_group | HAZ (incl. simulated) | 26 | 280 | 23 | 261 | 19 | 228 | 3 | 65 |
| product_form_group | forging | 89 | 1196 | 87 | 1191 | 84 | 1157 | 24 | 456 |
| product_form_group | not determinable | 6 | 151 | 6 | 151 | 6 | 151 | 5 | 140 |
| product_form_group | plate | 66 | 1027 | 62 | 1011 | 57 | 974 | 25 | 605 |
| product_form_group | weld metal | 4 | 78 | 4 | 78 | 4 | 78 | 3 | 67 |
| product_form_group | weld region (zone not stated) | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| irradiation | irradiated | 39 | 433 | 36 | 424 | 31 | 381 | 15 | 205 |
| irradiation | unirradiated | 153 | 2303 | 146 | 2268 | 139 | 2207 | 45 | 1128 |
| geometry_class | full-size (55x10x10 mm) | 151 | 2167 | 143 | 2131 | 134 | 2059 | 39 | 973 |
| geometry_class | miniature (reduced length) | 39 | 561 | 39 | 561 | 36 | 529 | 21 | 360 |
| geometry_class | sub-size, standard length (55 mm, reduced thickness) | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |

## 6. Cohorts carried forward (D-039)

| cohort | definition | curves | records |
| --- | --- | --- | --- |
| primary | primary population, primary rule, canonical keep rule | 170 | 2588 |
| looser | primary population, looser rule | 182 | 2692 |
| stricter | primary population, stricter rule | 60 | 1333 |
| alt_keep_rule | primary population, primary rule, alternative duplicate keep rule (most records first) | 170 | 2628 |
| plus_unresolved_irradiation | primary population plus records with unresolved irradiation labels (this release's labels), primary rule | 179 | 2704 |
| plus_additively_manufactured | primary population plus additively manufactured SA508 Gr.3, primary rule | 175 | 2654 |
| piping_secondary | SA508 Gr.1A piping steel only, primary rule | 15 | 181 |

## 7. Accounting of special cases

- Duplicated (WP1 E8, D-019): 69 series, 910 records removed as republications. Curves that exist under only one of the two keep rules: 19; primary-cohort curves replaced when the alternative keep rule is used: ['1-6.1', '1-6.2', '14-62', '14-64', '17-84', '44-193', '44-194', '55-255', '55-259'] -> ['19-90.1', '21-99.1', '21-99.2', '26-117', '26-120', '43-191', '43-192', '52-217', '52-219'].
- Out of scope (WP1): E1 austenitic stainless 713 records; E2 15Cr2MoV-A 38 records.
- Ambiguous or contradicted labels (population steps above): specimen type not supported 0 records; condition label contradicted by source 46; irradiation status unresolved 138.
- Piping (secondary): 212 records; additively manufactured (secondary): 66 records.
- Mixed dataset series split into more than one curve: 9 series (246 records):

| ref_id | dataset_series | records | curves | split_by | pieces |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 15 | 2 | treatment | 1-3.1 (14); 1-3.2 (1) |
| 1 | 6 | 107 | 3 | irradiated_resolved, fluence_level, test_condition_statement | 1-6.1 (95); 1-6.2 (10); 1-6.3 (2) |
| 1 | 7 | 11 | 2 | test_condition_statement | 1-7.1 (8); 1-7.2 (3) |
| 15 | 66 | 20 | 2 | treatment | 15-66.1 (10); 15-66.2 (10) |
| 15 | 76 | 10 | 2 | treatment | 15-76.1 (8); 15-76.2 (2) |
| 18 | 86 | 8 | 2 | product_form, test_condition_statement | 18-86.1 (4); 18-86.2 (4) |
| 21 | 100 | 20 | 2 | test_condition_statement | 21-100.1 (14); 21-100.2 (6) |
| 39 | 182 | 33 | 2 | post_treatment_temp_c | 39-182.1 (1); 39-182.2 (32) |
| 59 | 271 | 22 | 2 | length_mm, width_mm, thickness_mm, notch_depth_mm, irradiated_resolved, fluence_level | 59-271.1 (12); 59-271.2 (10) |

Special conditions inside the primary cohort (each forms its own curves; none is excluded for being special):

| condition | curves | records |
| --- | --- | --- |
| reconstituted specimens | 1 | 10 |
| simulated HAZ | 10 | 91 |
| HAZ (test condition statement) | 19 | 228 |
| post-weld heat treatment | 11 | 125 |
| step cooled | 5 | 67 |
| pre-strained | 2 | 45 |
| standard reference material | 2 | 20 |
| deliberately embrittled JSPS steel (refs 43, 44) | 1 | 13 |
| laboratory heats / model alloys (title) | 18 | 266 |
| product form uncertain (title reports weld/HAZ) | 11 | 171 |
| notch dimensions not reported | 74 | 993 |

Primary-population curves rejected by the primary rule:

| curve_id | material_family | product_form | geometry | irradiated | n_points | n_T_transition_band | n_T_upper_band | energy_ratio_min_to_upper | fails_primary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1-6.3 | A533B | plate | 55x10x10 a=2 | True | 2 | 0 | 1 | 0.29 | points 2 (needs >= 6); transition-band temperatures 0 (needs >= 2); upper band 1 points at 1 temperatures (needs >= 2 points at >= 2); lowest energy / upper reference 0.29 (needs <= 0.20) |
| 11-47 | A508 | forging | 55x10x10 a=2 | False | 14 | 1 | 3 | 0.02 | transition-band temperatures 1 (needs >= 2) |
| 15-66.2 | A508 | simulated HAZ | 55x10x10 a=? | False | 10 | 5 | 4 | 0.31 | lowest energy / upper reference 0.31 (needs <= 0.20) |
| 15-68 | A508 | simulated HAZ | 55x10x10 a=? | False | 7 | 4 | 2 | 0.29 | lowest energy / upper reference 0.29 (needs <= 0.20) |
| 15-69 | A508 | simulated HAZ | 55x10x10 a=? | False | 7 | 4 | 2 | 0.36 | lowest energy / upper reference 0.36 (needs <= 0.20) |
| 15-76.1 | A508 | simulated HAZ | 55x10x10 a=? | False | 8 | 3 | 4 | 0.26 | lowest energy / upper reference 0.26 (needs <= 0.20) |
| 15-76.2 | A508 | simulated HAZ | 55x10x10 a=? | False | 2 | 0 | 1 | 0.73 | points 2 (needs >= 6); transition-band temperatures 0 (needs >= 2); upper band 1 points at 1 temperatures (needs >= 2 points at >= 2); lowest energy / upper reference 0.73 (needs <= 0.20) |
| 18-86.1 | A508 | forging | 55x10x6 a=2 | False | 4 | 1 | 2 | 0.73 | points 4 (needs >= 6); transition-band temperatures 1 (needs >= 2); lowest energy / upper reference 0.73 (needs <= 0.20) |
| 18-86.2 | A508 | weld region (zone not stated) | 55x10x6 a=2 | False | 4 | 1 | 2 | 0.81 | points 4 (needs >= 6); transition-band temperatures 1 (needs >= 2); lowest energy / upper reference 0.81 (needs <= 0.20) |
| 21-100.2 | A508 | forging | 55x10x10 a=2 | False | 6 | 3 | 2 | 0.21 | lowest energy / upper reference 0.21 (needs <= 0.20) |
| 39-182.1 | A508 | forging | 55x10x10 a=? | False | 1 | 0 | 0 | 1 | points 1 (needs >= 6); transition-band temperatures 0 (needs >= 2); upper band 0 points at 0 temperatures (needs >= 2 points at >= 2); lowest energy / upper reference 1.00 (needs <= 0.20) |
| 49-205 | A533B | plate | 55x10x10 a=? | False | 9 | 3 | 3 | 0.23 | lowest energy / upper reference 0.23 (needs <= 0.20) |
| 50-211 | A533B | plate | 55x10x10 a=? | True | 5 | 2 | 2 | 0.15 | points 5 (needs >= 6) |
| 50-212 | A533B | plate | 55x10x10 a=? | True | 10 | 1 | 4 | 0.09 | transition-band temperatures 1 (needs >= 2) |
| 53-236 | A533B | HAZ | 20x1.5x1.5 a=0.33 | False | 10 | 1 | 7 | 0.05 | transition-band temperatures 1 (needs >= 2) |
| 53-243 | A533B | HAZ | 20x1.5x1.5 a=0.33 | True | 8 | 1 | 4 | 0.13 | transition-band temperatures 1 (needs >= 2) |
| 56-261 | A533B | plate | 55x10x10 a=? | False | 7 | 3 | 3 | 0.29 | lowest energy / upper reference 0.29 (needs <= 0.20) |
| 56-262 | A533B | plate | 55x10x10 a=? | False | 7 | 3 | 2 | 0.31 | lowest energy / upper reference 0.31 (needs <= 0.20) |
| 104-none.2 | A533B | plate | 55x10x10 a=? | True | 6 | 1 | 4 | 0.06 | transition-band temperatures 1 (needs >= 2) |
| 104-none.4 | A533B | plate | 55x10x10 a=? | True | 3 | 0 | 2 | 0.11 | points 3 (needs >= 6); transition-band temperatures 0 (needs >= 2) |
| 104-none.5 | A533B | plate | 55x10x10 a=? | True | 4 | 0 | 2 | 0.05 | points 4 (needs >= 6); transition-band temperatures 0 (needs >= 2) |
| 109-291 | A508 | forging | 27x3x4 a=1 | True | 14 | 8 | 5 | 0.21 | lowest energy / upper reference 0.21 (needs <= 0.20) |

## 8. Fluence treatment (D-036)

Irradiated records retained by WP1: 570; with a fluence value: 492; with an irradiation temperature: 343; fluence range 6.2e+17 to 1.11e+20 n/cm²; dataset series containing more than one fluence value: 0.

Fluence never varies within a dataset series and curves never cross series, so the fluence treatment can only matter where a source has no series IDs (ref 104, whose levels are at least 1.8x apart). The diagnostics show what would merge if the series boundary were ignored.

| fluence_treatment | curves | identical_to_primary | primary_curves_merged |
| --- | --- | --- | --- |
| exact reported value (primary) | 233 | True | none |
| within a factor of 1.2 (alternative) | 233 | True | none |
| diagnostic: exact value, dataset series ignored | 226 | False | 1-3.2 + 1-4 \| 1-5 + 1-6.1 \| 1-6.3 + 1-7.2 \| 15-76.2 + 15-77 \| 17-84 + 17-85 \| 41-187 + 41-188 \| 53-241 + 53-245 |
| diagnostic: within a factor of 1.2, dataset series ignored | 225 | False | 1-3.2 + 1-4 \| 1-5 + 1-6.1 \| 1-6.3 + 1-7.2 \| 15-76.2 + 15-77 \| 16-80 + 16-81 \| 17-84 + 17-85 \| 41-187 + 41-188 \| 53-241 + 53-245 |

Every reported irradiation condition (population column: primary or the excluding step):

| ref_id | irradiation_label_check | fluence_n_per_cm2 | irradiation_temp_c | irradiation_time_h | records | dataset_series | curves | populations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | releases agree | 3e+19 |  |  | 13 | 6, 7 | 1-6.3, 1-7.1, 1-7.2 | P2, primary |
| 2 | releases agree | 1.3e+19 | 288 |  | 23 | 8, 10 | 2-8, 2-10 | primary |
| 3 | releases agree | 1.6e+19 | 288 | 672 | 64 | 13, 15, 17, 19 | 3-13, 3-15, 3-17, 3-19 | primary |
| 7 | unresolved |  |  |  | 36 | 27, 28, 29, 30 | 7-27, 7-28, 7-29, 7-30 | P3 |
| 8 | unresolved |  |  |  | 42 | 31, 32 | 8-31, 8-32 | P3 |
| 9 | unresolved | 6e+19 |  |  | 14 | 35 | 9-35 | P3 |
| 16 | releases agree | 1.48e+19 | 290 |  | 13 | 80 | 16-80 | primary |
| 16 | releases agree | 1.75e+19 | 290 |  | 11 | 81 | 16-81 | primary |
| 16 | releases agree | 2.52e+19 | 290 |  | 9 | 79 | 16-79 | primary |
| 35 | releases agree | 1e+20 |  |  | 15 | 159 | 35-159 | primary |
| 50 | releases agree | 2.7e+19 | 149 |  | 6 | 208 | 50-208 | primary |
| 50 | releases agree | 2.8e+19 | 149 |  | 5 | 211 | 50-211 | primary |
| 50 | releases agree | 2.8e+19 | 288 |  | 15 | 209 | 50-209 | primary |
| 50 | releases agree | 3.1e+19 | 149 |  | 10 | 212 | 50-212 | primary |
| 52 | releases agree | 1e+19 | 150 |  | 12 | 221 | 52-221 | primary |
| 53 | releases agree | 8e+19 | 290 |  | 16 | 243, 244 | 53-243, 53-244 | primary |
| 53 | unresolved | 8e+19 | 290 |  | 34 | 223, 224 | 53-223, 53-224 | P3 |
| 55 | releases agree | 1e+19 | 150 |  | 35 | 255, 257, 259 | 55-255, 55-257, 55-259 | primary |
| 57 | releases agree | 3.4e+19 | 269.9 |  | 19 | 264 | 57-264 | primary |
| 59 | releases agree | 1.3e+18 |  |  | 75 | 267, 270, 272, 275, 277, 279 | 59-267, 59-270, 59-272, 59-275, 59-277, 59-279 | primary |
| 59 | releases agree | 2.7e+18 |  |  | 12 | 273 | 59-273 | primary |
| 59 | releases agree | 2.7e+19 |  |  | 20 | 268, 271 | 59-268, 59-271.1 | primary |
| 104 | releases agree | 6.2e+17 | 200 |  | 6 | none | 104-none.2 | primary |
| 104 | releases agree | 3.9e+18 | 200 |  | 6 | none | 104-none.3 | primary |
| 104 | releases agree | 1.3e+19 | 200 |  | 3 | none | 104-none.4 | primary |
| 104 | releases agree | 2.34e+19 | 200 |  | 4 | none | 104-none.5 | primary |
| 109 | releases agree | 1.11e+20 | 286 |  | 52 | 287, 289, 291, 293 | 109-287, 109-289, 109-291, 109-293 | primary |
