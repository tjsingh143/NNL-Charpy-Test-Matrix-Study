# WP2 summary (eny5v-www93)

Dataset: Materials Cloud 2024.206, record eny5v-www93 (DOI 10.24435/materialscloud:gh-za, issued 2024-12-19)

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
| Start | Records retained by WP1 (canonical keep rule) | outputs/wp1*/reconciliation_table.md | 3050 | 223 | 54 |
| P1 | excluded: specimen type not supported as ordinary Charpy V-notch | CP1 decision 2; D-020 | 0 | 0 | 0 |
| P2 | excluded: condition label contradicted by the source | D-031 (approved at CP2) | 48 | 7 | 1 |
| P3 | excluded: irradiation status unresolved between releases | CP1 decision 1; D-021; D-035 (approved at CP2) | 138 | 11 | 4 |
| P4 | secondary: SA508 Gr.1A main-steam-line piping steel | CP1 decision 3; D-027 | 212 | 19 | 5 |
| P5 | secondary: additively manufactured SA508 Gr.3 (manufacturing route differs from conventional RPV material) | D-034 (approved at CP2) | 66 | 5 | 1 |
| End | primary RPV population |  | 2586 | 181 | 45 |

## 3. Curve inventory before inclusion filtering (primary population)

- Curves: 181; records: 2586; references: 45.
- Points per curve: median 12, 10th-90th percentile 7-23, range 1-95.
- Temperature span per curve: median 234 °C, 10th-90th percentile 140-354 °C.
- Distinct test temperatures in the transition band: median 5; curves with none: 4.
- Spearman rank correlation of energy with temperature below 0.7 (diagnostic only): 7 curves.

What the points cover (primary thresholds):

| sampling_class | curves | records |
| --- | --- | --- |
| brackets the transition in the screening bands (lower side, transition band and upper band sampled) | 162 | 2459 |
| fewer than 2 transition-band temperatures | 7 | 55 |
| lower shelf not approached | 8 | 61 |
| lower shelf not approached; fewer than 2 transition-band temperatures | 2 | 8 |
| too few points to describe | 2 | 3 |

Points per curve:

| points | curves |
| --- | --- |
| 1-4 | 6 |
| 5 | 1 |
| 6-7 | 12 |
| 8-9 | 23 |
| 10-11 | 44 |
| 12-14 | 39 |
| 15-19 | 26 |
| 20-29 | 22 |
| 30+ | 8 |

## 4. Pre-fit screening rules (D-038)

**What passing means.** A curve that passes a rule appears sufficiently sampled to *attempt* a transition-curve fit in WP3. Passing does not show that a tanh fit will converge, be well conditioned or give physically reasonable parameters, nor that the curve is scientifically valid; a curve whose WP3 fit fails is reported as a failure, never silently removed.

**Screening references and bands (D-037).** Lower reference = lowest measured energy; screening upper reference = mean of the 3 highest measured energies. The screening upper reference is not an upper-shelf energy (USE); USE is estimated in WP3. Transition band = 0.12-0.88 of the rise between the references: for the normalized tanh y = (1 + tanh x) / 2, y = 0.119 at x = -1 and 0.881 at x = +1, so the band is T0 - C to T0 + C. This is a project-defined, model-based convention, not an ASTM requirement. The stricter rule's specimen counts are historical ASTM E185-82 surveillance guidance, used as a deliberately conservative comparison.

| rule | min_points_unirradiated | min_points_irradiated | min_T_transition | min_T_upper | min_points_upper | min_T_lower | max_energy_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| looser | 5 | 5 | 1 | 1 | 1 | 1 | 0.3 |
| primary | 6 | 6 | 2 | 2 | 2 | 1 | 0.2 |
| stricter | 15 | 12 | 3 | 2 | 3 | 2 | 0.15 |

| criterion | basis |
| --- | --- |
| points | 5 = fewest that leave one residual degree of freedom for a 4-parameter tanh; 6 = two; 15 unirradiated / 12 irradiated = historical ASTM E185-82 §6.3 surveillance-programme specimen minimums (baseline curve / irradiated capsule), used as a deliberately conservative comparison, not as a statistical law that fewer points make a curve unusable |
| transition temperatures | transition band = 0.12-0.88 of the rise between the screening references, i.e. T0 - C to T0 + C of a normalized tanh (project-defined, model-based, not an ASTM requirement); 1 temperature locates the transition; 2 fix location and width (T0 and C); 3 add one check on the shape |
| upper band | 1 = no requirement; 2 distinct temperatures show the rise has stopped; 3 specimens mirrors the normally three specimens ASTM E185-82 §4.18 averages for upper-shelf energy (a screening count only; USE is estimated in WP3) |
| energy ratio | lowest energy / screening upper reference: the coldest point lies at or below the lower band edge (T0 - C) whenever the true lower-to-upper shelf ratio is at most 0.20 (limit 0.30), 0.09 (limit 0.20), 0.03 (limit 0.15) |

## 5. What each rule keeps

| rule | curves | records | curves_lost | records_lost | median_points | median_T_span_c | median_transition_temperatures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| before inclusion filtering | 181 | 2586 | 0 | 0 | 12 | 234.4 | 5 |
| looser | 172 | 2544 | 9 | 42 | 12 | 239.5 | 5 |
| primary | 161 | 2454 | 20 | 132 | 12 | 249.6 | 5 |
| stricter | 54 | 1235 | 127 | 1351 | 19.5 | 218.9 | 6 |

Curves failing each criterion (a curve can fail several):

| rule | criterion | curves_failing | curves_failing_only_this |
| --- | --- | --- | --- |
| looser | points | 6 | 0 |
| looser | transition temperatures | 4 | 0 |
| looser | upper band | 1 | 0 |
| looser | lower band temperatures | 0 | 0 |
| looser | energy ratio | 7 | 3 |
| primary | points | 7 | 1 |
| primary | transition temperatures | 11 | 5 |
| primary | upper band | 2 | 0 |
| primary | lower band temperatures | 0 | 0 |
| primary | energy ratio | 12 | 8 |
| stricter | points | 114 | 61 |
| stricter | transition temperatures | 18 | 0 |
| stricter | upper band | 24 | 3 |
| stricter | lower band temperatures | 43 | 7 |
| stricter | energy ratio | 20 | 2 |

By material family, product form, irradiation status and geometry:

| dimension | group | curves_before | records_before | curves_looser | records_looser | curves_primary | records_primary | curves_stricter | records_stricter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| material_family | 20MnMoNi55 | 8 | 178 | 8 | 178 | 8 | 178 | 5 | 140 |
| material_family | A302B | 2 | 38 | 2 | 38 | 2 | 38 | 2 | 38 |
| material_family | A508 | 96 | 1189 | 90 | 1161 | 86 | 1126 | 18 | 358 |
| material_family | A533B | 71 | 1103 | 68 | 1089 | 61 | 1034 | 26 | 632 |
| material_family | A533B weld metal | 4 | 78 | 4 | 78 | 4 | 78 | 3 | 67 |
| product_form_group | HAZ (incl. simulated) | 26 | 280 | 23 | 261 | 19 | 228 | 3 | 65 |
| product_form_group | forging | 79 | 1048 | 77 | 1043 | 75 | 1023 | 18 | 358 |
| product_form_group | not determinable | 6 | 151 | 6 | 151 | 6 | 151 | 5 | 140 |
| product_form_group | plate | 65 | 1025 | 62 | 1011 | 57 | 974 | 25 | 605 |
| product_form_group | weld metal | 4 | 78 | 4 | 78 | 4 | 78 | 3 | 67 |
| product_form_group | weld region (zone not stated) | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| irradiation | irradiated | 34 | 379 | 32 | 372 | 28 | 343 | 12 | 167 |
| irradiation | unirradiated | 147 | 2207 | 140 | 2172 | 133 | 2111 | 42 | 1068 |
| geometry_class | full-size (55x10x10 mm) | 149 | 2139 | 142 | 2105 | 133 | 2033 | 38 | 947 |
| geometry_class | miniature (reduced length) | 30 | 439 | 30 | 439 | 28 | 421 | 16 | 288 |
| geometry_class | sub-size, standard length (55 mm, reduced thickness) | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 |

## 6. Cohorts carried forward (D-039)

Membership is frozen at CP2: explicit files `cohort_membership.csv` and `cohort_manifest.csv`, checked on every run against `data/FROZEN_COHORTS_CP2.csv`. Later work packages read these cohorts; they do not regenerate them with other thresholds.

| cohort | role | definition | curves | records |
| --- | --- | --- | --- | --- |
| primary | primary analysis | primary population, primary rule, canonical keep rule | 161 | 2454 |
| looser | inclusion-rule sensitivity | primary population, looser rule | 172 | 2544 |
| stricter | inclusion-rule sensitivity | primary population, stricter rule | 54 | 1235 |
| alt_keep_rule | duplicate keep-rule sensitivity | primary population, primary rule, alternative duplicate keep rule (most records first) | 161 | 2494 |
| plus_unresolved_irradiation | population sensitivity | primary population plus records with unresolved irradiation labels (this release's labels), primary rule | 170 | 2570 |
| plus_additively_manufactured | population sensitivity (secondary material) | primary population plus additively manufactured SA508 Gr.3, primary rule | 166 | 2520 |
| piping_secondary | secondary group | SA508 Gr.1A piping steel only, primary rule | 15 | 181 |

## 7. Accounting of special cases

- Duplicated (WP1 E8, D-019): 69 series, 910 records removed as republications. Curves that exist under only one of the two keep rules: 19; primary-cohort curves replaced when the alternative keep rule is used: ['1-6.1', '1-6.2', '14-62', '14-64', '17-84', '44-193', '44-194', '55-255', '55-259'] -> ['19-90.1', '21-99.1', '21-99.2', '26-117', '26-120', '43-191', '43-192', '52-217', '52-219'].
- Out of scope (WP1): E1 austenitic stainless 713 records; E2 15Cr2MoV-A 0 records.
- Ambiguous or contradicted labels (population steps above): specimen type not supported 0 records; condition label contradicted by source 48; irradiation status unresolved 138.
- Piping (secondary): 212 records; additively manufactured (secondary): 66 records.
- Curves excluded because the source contradicts their condition labels (P2, D-031). Measurements and labels are unchanged; the exact reason is kept per record and per curve:

| curve_id | n_points | irradiated | treatment | test_condition_statement | condition_label_contradicted_by_source |
| --- | --- | --- | --- | --- | --- |
| 1-3.1 | 14 | False | Shock Wave Hardening (Bottom-Surface) |  | Treatment label contradicted by [NP-1661] Table 3-1: tanh fits give USE about 136, 108 and 41 J and T0 about 13, 21 and 7 C for the non-shocked, bottom-layer and top-layer materials; dataset curves 3, 4 and 5 (labelled bottom-surface shock hardened, top-surface shock hardened, and untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 C, i.e. the labels are shifted by one series. |
| 1-3.2 | 1 | False | Shock Wave Hardening (Top-Surface) |  | Treatment label contradicted by [NP-1661] Table 3-1: tanh fits give USE about 136, 108 and 41 J and T0 about 13, 21 and 7 C for the non-shocked, bottom-layer and top-layer materials; dataset curves 3, 4 and 5 (labelled bottom-surface shock hardened, top-surface shock hardened, and untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 C, i.e. the labels are shifted by one series. |
| 1-4 | 10 | False | Shock Wave Hardening (Top-Surface) |  | Treatment label contradicted by [NP-1661] Table 3-1: tanh fits give USE about 136, 108 and 41 J and T0 about 13, 21 and 7 C for the non-shocked, bottom-layer and top-layer materials; dataset curves 3, 4 and 5 (labelled bottom-surface shock hardened, top-surface shock hardened, and untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 C, i.e. the labels are shifted by one series. |
| 1-5 | 10 | False |  |  | Treatment label contradicted by [NP-1661] Table 3-1: tanh fits give USE about 136, 108 and 41 J and T0 about 13, 21 and 7 C for the non-shocked, bottom-layer and top-layer materials; dataset curves 3, 4 and 5 (labelled bottom-surface shock hardened, top-surface shock hardened, and untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 C, i.e. the labels are shifted by one series. |
| 1-6.3 | 2 | True |  | Reconstituted specimen | Fluence contradicted by [NP-1661] Fig. 3-17: the irradiated HSST Plate 02 specimens received 2.5e18 n/cm2 (E > 1 MeV); the dataset gives 3e19 n/cm2. These two reconstituted records carry the series-7 label (irradiated, 3e19 n/cm2) inside unirradiated HSST Plate 02 series 6. Their energies do not fit an irradiated curve (series 7 has only 11 J at -7 C): 6.9 J at -74.8 C lies within the unirradiated data (7.4 J at -70.5 C) and 41.3 J at -59.8 C is above even the unirradiated original specimens at -60 C (8.9-22.3 J), so the irradiation label itself is also doubtful. |
| 1-7.1 | 8 | True |  |  | Fluence contradicted by [NP-1661] Fig. 3-17: the irradiated HSST Plate 02 specimens received 2.5e18 n/cm2 (E > 1 MeV); the dataset gives 3e19 n/cm2. |
| 1-7.2 | 3 | True |  | Reconstituted specimen | Fluence contradicted by [NP-1661] Fig. 3-17: the irradiated HSST Plate 02 specimens received 2.5e18 n/cm2 (E > 1 MeV); the dataset gives 3e19 n/cm2. |

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
| laboratory heats / model alloys (title) | 11 | 177 |
| product form uncertain (title reports weld/HAZ) | 11 | 171 |
| notch dimensions not reported | 74 | 993 |

Primary-population curves rejected by the primary rule:

| curve_id | material_family | product_form | geometry | irradiated | n_points | n_T_transition_band | n_T_upper_band | energy_ratio_min_to_screening_upper | fails_primary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11-47 | A508 | forging | 55x10x10 a=2 | False | 14 | 1 | 3 | 0.02 | transition-band temperatures 1 (needs >= 2) |
| 15-66.2 | A508 | simulated HAZ | 55x10x10 a=? | False | 10 | 5 | 4 | 0.31 | lowest energy / screening upper reference 0.31 (needs <= 0.20) |
| 15-68 | A508 | simulated HAZ | 55x10x10 a=? | False | 7 | 4 | 2 | 0.29 | lowest energy / screening upper reference 0.29 (needs <= 0.20) |
| 15-69 | A508 | simulated HAZ | 55x10x10 a=? | False | 7 | 4 | 2 | 0.36 | lowest energy / screening upper reference 0.36 (needs <= 0.20) |
| 15-76.1 | A508 | simulated HAZ | 55x10x10 a=? | False | 8 | 3 | 4 | 0.26 | lowest energy / screening upper reference 0.26 (needs <= 0.20) |
| 15-76.2 | A508 | simulated HAZ | 55x10x10 a=? | False | 2 | 0 | 1 | 0.73 | points 2 (needs >= 6); transition-band temperatures 0 (needs >= 2); upper band 1 points at 1 temperatures (needs >= 2 points at >= 2); lowest energy / screening upper reference 0.73 (needs <= 0.20) |
| 18-86.1 | A508 | forging | 55x10x6 a=2 | False | 4 | 1 | 2 | 0.73 | points 4 (needs >= 6); transition-band temperatures 1 (needs >= 2); lowest energy / screening upper reference 0.73 (needs <= 0.20) |
| 18-86.2 | A508 | weld region (zone not stated) | 55x10x6 a=2 | False | 4 | 1 | 2 | 0.81 | points 4 (needs >= 6); transition-band temperatures 1 (needs >= 2); lowest energy / screening upper reference 0.81 (needs <= 0.20) |
| 21-100.2 | A508 | forging | 55x10x10 a=2 | False | 6 | 3 | 2 | 0.21 | lowest energy / screening upper reference 0.21 (needs <= 0.20) |
| 39-182.1 | A508 | forging | 55x10x10 a=? | False | 1 | 0 | 0 | 1 | points 1 (needs >= 6); transition-band temperatures 0 (needs >= 2); upper band 0 points at 0 temperatures (needs >= 2 points at >= 2); lowest energy / screening upper reference 1.00 (needs <= 0.20) |
| 49-205 | A533B | plate | 55x10x10 a=? | False | 9 | 3 | 3 | 0.23 | lowest energy / screening upper reference 0.23 (needs <= 0.20) |
| 50-211 | A533B | plate | 55x10x10 a=? | True | 5 | 2 | 2 | 0.15 | points 5 (needs >= 6) |
| 50-212 | A533B | plate | 55x10x10 a=? | True | 10 | 1 | 4 | 0.09 | transition-band temperatures 1 (needs >= 2) |
| 53-236 | A533B | HAZ | 20x1.5x1.5 a=0.33 | False | 10 | 1 | 7 | 0.05 | transition-band temperatures 1 (needs >= 2) |
| 53-243 | A533B | HAZ | 20x1.5x1.5 a=0.33 | True | 8 | 1 | 4 | 0.13 | transition-band temperatures 1 (needs >= 2) |
| 56-261 | A533B | plate | 55x10x10 a=? | False | 7 | 3 | 3 | 0.29 | lowest energy / screening upper reference 0.29 (needs <= 0.20) |
| 56-262 | A533B | plate | 55x10x10 a=? | False | 7 | 3 | 2 | 0.31 | lowest energy / screening upper reference 0.31 (needs <= 0.20) |
| 104-none.2 | A533B | plate | 55x10x10 a=? | True | 6 | 1 | 4 | 0.06 | transition-band temperatures 1 (needs >= 2) |
| 104-none.4 | A533B | plate | 55x10x10 a=? | True | 3 | 0 | 2 | 0.11 | points 3 (needs >= 6); transition-band temperatures 0 (needs >= 2) |
| 104-none.5 | A533B | plate | 55x10x10 a=? | True | 4 | 0 | 2 | 0.05 | points 4 (needs >= 6); transition-band temperatures 0 (needs >= 2) |

## 8. Fluence treatment (D-036)

Irradiated records retained by WP1: 404; with a fluence value: 404; with an irradiation temperature: 269; fluence range 6.2e+17 to 1e+20 n/cm²; dataset series containing more than one fluence value: 0.

Fluence never varies within a dataset series and curves never cross series, so the fluence treatment can only matter where a source has no series IDs (ref 104, whose levels are at least 1.8x apart). The diagnostics show what would merge if the series boundary were ignored.

| fluence_treatment | curves | identical_to_primary | primary_curves_merged |
| --- | --- | --- | --- |
| exact reported value (primary) | 223 | True | none |
| within a factor of 1.2 (alternative) | 223 | True | none |
| diagnostic: exact value, dataset series ignored | 217 | False | 1-3.2 + 1-4 \| 1-5 + 1-6.1 \| 1-6.3 + 1-7.2 \| 15-76.2 + 15-77 \| 17-84 + 17-85 \| 41-187 + 41-188 |
| diagnostic: within a factor of 1.2, dataset series ignored | 216 | False | 1-3.2 + 1-4 \| 1-5 + 1-6.1 \| 1-6.3 + 1-7.2 \| 15-76.2 + 15-77 \| 16-80 + 16-81 \| 17-84 + 17-85 \| 41-187 + 41-188 |

Every reported irradiation condition (population column: primary or the excluding step):

| ref_id | irradiation_label_check | fluence_n_per_cm2 | irradiation_temp_c | irradiation_time_h | records | dataset_series | curves | populations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | releases agree | 3e+19 |  |  | 13 | 6, 7 | 1-6.3, 1-7.1, 1-7.2 | P2 |
| 2 | releases agree | 1.3e+19 | 288 |  | 23 | 8, 10 | 2-8, 2-10 | primary |
| 3 | releases agree | 1.6e+19 | 288 | 672 | 64 | 13, 15, 17, 19 | 3-13, 3-15, 3-17, 3-19 | primary |
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
| 53 | unresolved | 8e+19 | 290 |  | 12 | 242, 245 | 53-242, 53-245 | P3 |
| 55 | releases agree | 1e+19 | 150 |  | 35 | 255, 257, 259 | 55-255, 55-257, 55-259 | primary |
| 57 | releases agree | 3.4e+19 | 269.9 |  | 19 | 264 | 57-264 | primary |
| 59 | releases agree | 1.3e+18 |  |  | 75 | 267, 270, 272, 275, 277, 279 | 59-267, 59-270, 59-272, 59-275, 59-277, 59-279 | primary |
| 59 | releases agree | 2.7e+18 |  |  | 12 | 273 | 59-273 | primary |
| 59 | releases agree | 2.7e+19 |  |  | 20 | 268, 271 | 59-268, 59-271.1 | primary |
| 104 | releases agree | 6.2e+17 | 200 |  | 6 | none | 104-none.2 | primary |
| 104 | releases agree | 3.9e+18 | 200 |  | 6 | none | 104-none.3 | primary |
| 104 | releases agree | 1.3e+19 | 200 |  | 3 | none | 104-none.4 | primary |
| 104 | releases agree | 2.34e+19 | 200 |  | 4 | none | 104-none.5 | primary |
