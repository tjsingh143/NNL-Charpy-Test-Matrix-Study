# WP5 - specimen size effect: results

Analysis of published Charpy V-notch test data (Materials Cloud 2025.30), CP2-frozen primary cohort, CP3-approved WP3 fits. Every mapped value is a TRANSFORMED ESTIMATE derived from published smaller-specimen measurements, never a new measurement. Method and every judgement call: DECISIONS.md D-068 to D-086, pre-registered and committed before any residual existed. **Status: WP5 complete - CP4 AWAITING AUTHOR APPROVAL.**

## 1. Headline

The classical normalization **helps a great deal but does not collapse the curves**. Across the 10 matched geometry comparisons of the primary analysis set, drawn from **7 independent material-condition families in 5 publications**, the residual index-temperature disagreement after normalization has a family-weighted mean of **-3.5 °C** and a family-weighted standard deviation of **11.4 °C**, with individual comparisons spanning -33.8 to +18.3 °C.

**No single smaller-specimen geometry reaches the pre-registered evidence threshold** of 3 independent matched families from 2 publications (D-079): 0 of 9 geometry classes are DIRECTLY SUPPORTED. The dataset is therefore **not sufficient to establish a geometry-resolved size-correction uncertainty**, and the only scale it can offer WP6 is a pooled one across all miniature geometries, carried as WEAKLY SUPPORTED with that limitation attached.

## 2. How much genuinely matched evidence exists

- **18** STRICT matched geometry comparisons, from **10** independent material-condition families in **5** publications (refs 53, 55, 59, 60 and 107), out of 4,824 enumerated candidate pairs (`pair_data_sufficiency.md`).
- **10** reach the pre-registered PRIMARY analysis set, from **7** families in **5** publications; **8** are held as sensitivity.
- **0 PARTIAL and 0 cross-study comparisons.** Without a heat identifier the reported composition is the only heat proxy, and it never matches exactly across publications, so every cross-publication pair is rejected on a recorded composition difference.
- **No ASTM E23-type sub-size curve exists in any cohort.** The only two such curves (ref 18, 55 x 10 x 6 mm) have 4 points each and fail every WP2 screening rule. All the evidence here is miniaturized (MCVN) evidence (D-071).

## 3. Residual size-correction disagreement

DT_size = T41J(normalized smaller specimen) - T41J(measured full-size curve). **Positive** means the correction places the transition WARMER than the measured full-size curve, the conservative direction for a vessel integrity argument.

| subset | weighting | n | n_families | n_studies | mean_c | median_c | mae_c | rmse_c | min_c | max_c | sd_c | robust_scale_1p4826_mad_c | p10_c | p25_c | p75_c | p90_c | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRIMARY analysis set | comparison-weighted | 10 | 7 | 5 | -3.494 | -3.745 | 13.9 | 16.19 | -33.82 | 18.32 | 16.66 | 19.46 | -19.9 | -13.84 | 10.6 | 14.73 |  |
| PRIMARY analysis set | family-weighted (each family's mean counts once) | 7 | 7 | 5 | -3.494 | -4.961 | 9.496 | 11.15 | -14.01 | 18.32 | 11.43 | 11.34 | -13.6 | -12.24 | 0.3384 | 8.94 |  |
| all STRICT comparisons with a residual (primary + held as sensitivity) | comparison-weighted | 17 | 10 | 5 | -9.141 | -4.961 | 19.48 | 26.88 | -83.88 | 18.32 | 26.05 | 21.79 | -35.83 | -18.36 | 11.49 | 16.15 |  |
| all STRICT comparisons with a residual (primary + held as sensitivity) | family-weighted (each family's mean counts once) | 10 | 10 | 5 | -10.8 | -10.3 | 17.87 | 22.74 | -48.94 | 18.32 | 21.09 | 19.9 | -39.85 | -18.07 | 4.893 | 10.66 |  |

## 4. By product form

| stratum | weighting | evidence | n_comparisons | n_families | n_studies | n_summarized | pair_ids | values_c | mean_c | median_c | mae_c | rmse_c | min_c | max_c | sd_c | robust_scale_1p4826_mad_c | p10_c | p25_c | p75_c | p90_c | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| product form: forging | not summarized | insufficient matched evidence for a standalone estimate (2 independent families from 2 publications; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 2 | 2 | 2 | 0 | 107-283\|107-282; 59-278\|59-274 | -13.3; -5.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| product form: plate | comparison-weighted | sufficient (>= 3 families from >= 2 publications) | 6 | 4 | 3 | 6 | 55-257\|55-255; 55-259\|55-255; 59-269\|59-266; 59-271.2\|59-266; 59-272\|59-267; 60-281\|60-280 | -33.8; -18.4; -14.0; +11.5; +14.3; +18.3 | -3.672 | -1.257 | 18.39 | 19.79 | -33.82 | 18.32 | 21.3 | 24.23 | -26.09 | -17.27 | 13.63 | 16.33 |  |
| product form: plate | family-weighted | sufficient (>= 3 families from >= 2 publications) | 6 | 4 | 3 | 4 | 55-257\|55-255; 55-259\|55-255; 59-269\|59-266; 59-271.2\|59-266; 59-272\|59-267; 60-281\|60-280 | -33.8; -18.4; -14.0; +11.5; +14.3; +18.3 | -2.215 | -6.585 | 11.37 | 12.85 | -14.01 | 18.32 | 14.62 | 8.894 | -13.15 | -11.87 | 3.073 | 12.22 |  |
| product form: weld metal | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 2 | 1 | 1 | 0 | 53-233\|53-225; 53-241\|53-225 | -2.5; +7.9 |  |  |  |  |  |  |  |  |  |  |  |  |  |

## 5. By smaller-specimen geometry

| stratum | weighting | evidence | n_comparisons | n_families | n_studies | n_summarized | pair_ids | values_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| geometry: 20x1.5x1.5 a=0.33 | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 1 | 1 | 1 | 0 | 53-241\|53-225 | -2.5 |
| geometry: 20x2.5x2.5 a=0.38 | not summarized | insufficient matched evidence for a standalone estimate (3 independent families from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 3 | 3 | 1 | 0 | 59-271.2\|59-266; 59-272\|59-267; 59-278\|59-274 | -14.0; -5.0; +11.5 |
| geometry: 20x3.33x3.33 a=0.51 | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 1 | 1 | 1 | 0 | 53-233\|53-225 | +7.9 |
| geometry: 23.6x3.33x3.33 a=0.51 | not summarized | insufficient matched evidence for a standalone estimate (2 independent families from 2 publications; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 2 | 2 | 2 | 0 | 55-259\|55-255; 59-269\|59-266 | -33.8; -18.4 |
| geometry: 23.6x5x5 a=0.76 | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 1 | 1 | 1 | 0 | 55-257\|55-255 | +14.3 |
| geometry: 27.5x3.33x3.33 a=0.6 | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 1 | 1 | 1 | 0 | 60-281\|60-280 | +18.3 |
| geometry: 27x3x4 a=1 | not summarized | insufficient matched evidence for a standalone estimate (1 independent family from 1 publication; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 1 | 1 | 1 | 0 | 107-283\|107-282 | -13.3 |

## 6. By irradiation state

| stratum | weighting | evidence | n_comparisons | n_families | n_studies | n_summarized | pair_ids | values_c | mean_c | median_c | mae_c | rmse_c | min_c | max_c | sd_c | robust_scale_1p4826_mad_c | p10_c | p25_c | p75_c | p90_c | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| irradiation state: irradiated | not summarized | insufficient matched evidence for a standalone estimate (2 independent families from 2 publications; D-079 requires >= 3 from >= 2). The individual comparisons are listed instead of a summary statistic. | 3 | 2 | 2 | 0 | 55-257\|55-255; 55-259\|55-255; 59-272\|59-267 | -18.4; -14.0; +14.3 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| irradiation state: unirradiated | comparison-weighted | sufficient (>= 3 families from >= 2 publications) | 7 | 5 | 4 | 7 | 107-283\|107-282; 53-233\|53-225; 53-241\|53-225; 59-269\|59-266; 59-271.2\|59-266; 59-278\|59-274; 60-281\|60-280 | -33.8; -13.3; -5.0; -2.5; +7.9; +11.5; +18.3 | -2.417 | -2.529 | 13.19 | 16.4 | -33.82 | 18.32 | 17.52 | 16.01 | -21.52 | -9.143 | 9.697 | 14.22 |  |
| irradiation state: unirradiated | family-weighted | sufficient (>= 3 families from >= 2 publications) | 7 | 5 | 4 | 5 | 107-283\|107-282; 53-233\|53-225; 53-241\|53-225; 59-269\|59-266; 59-271.2\|59-266; 59-278\|59-274; 60-281\|60-280 | -33.8; -13.3; -5.0; -2.5; +7.9; +11.5; +18.3 | -1.688 | -4.961 | 10.09 | 11.57 | -13.33 | 18.32 | 12.8 | 11.34 | -12.46 | -11.16 | 2.686 | 12.07 |  |

## 7. Does the normalization help? Before against after

Of the 10 primary comparisons: the mid-transition temperature agreed better after normalization in **8** and worse in **2**; the upper-shelf energy in **9** and worse in **1**; the curve-level energy over the shared supported temperature range in **8** and worse in **2**.

| quantity | median before | median after |
| --- | --- | --- |
| \|T0 difference\| (°C) | 66.9 | 16.2 |
| \|relative USE difference\| | 0.959 | 0.244 |
| curve RMS energy difference / full-size USE | 0.461 | 0.259 |

**The two failures are both from ref 55**, the same severely embrittled low-toughness A533B plate (full-size USE 51-63 J). For those two pairs the measured shift runs the WRONG WAY: the miniature specimens showed a transition temperature at or ABOVE the full-size one (observed T0(full-size) - T0(smaller) = -35.5 and -2.2 °C), so adding a positive published shift of +30 to +49 °C makes the agreement worse. This is a genuine negative result and it is reported, not removed.

| pair_id | smaller_geometry | t0_abs_difference_before_c | t0_abs_difference_after_c | t0_improved | relative_use_difference_before | relative_use_difference_after | use_improved | curve_rms_difference_over_shared_range_before | curve_rms_difference_over_shared_range_after | observed_pair_shift_t0_c | published_shift_c | published_minus_observed_shift_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 107-283\|107-282 | 27x3x4 a=1 | 73.82 | 27.49 | True | -0.9581 | 0.0007555 | True | 0.4729 | 0.1544 | 73.82 | 48.23 | -25.58 |
| 53-233\|53-225 | 20x3.33x3.33 a=0.51 | 35.23 | 13.75 | True | -0.9593 | -0.01689 | True | 0.3886 | 0.1198 | 35.23 | 48.53 | 13.3 |
| 53-241\|53-225 | 20x1.5x1.5 a=0.33 | 89.83 | 2.494 | True | -0.9957 | 0.3393 | True | 0.4589 | 0.2701 | 89.83 | 87.14 | -2.692 |
| 55-257\|55-255 | 23.6x5x5 a=0.76 | 35.53 | 61.16 | False | -0.7838 | 0.5484 | True | 0.5458 | 0.247 | -35.53 | 30.07 | 65.6 |
| 55-259\|55-255 | 23.6x3.33x3.33 a=0.51 | 2.213 | 47.56 | False | -0.9218 | 0.9328 | False | 0.5966 | 0.3834 | -2.213 | 48.53 | 50.74 |
| 59-269\|59-266 | 23.6x3.33x3.33 a=0.51 | 78.37 | 29.73 | True | -0.9525 | 0.1477 | True | 0.4695 | 0.2929 | 78.37 | 48.53 | -29.84 |
| 59-271.2\|59-266 | 20x2.5x2.5 a=0.38 | 60.03 | 1.786 | True | -0.9725 | 0.5639 | True | 0.4623 | 0.5173 | 60.03 | 61.47 | 1.437 |
| 59-272\|59-267 | 20x2.5x2.5 a=0.38 | 76.69 | 18.11 | True | -0.9742 | 0.4734 | True | 0.3713 | 0.5343 | 76.69 | 61.47 | -15.22 |
| 59-278\|59-274 | 20x2.5x2.5 a=0.38 | 76.26 | 14.37 | True | -0.9803 | 0.1213 | True | 0.4395 | 0.1989 | 76.26 | 61.47 | -14.79 |
| 60-281\|60-280 | 27.5x3.33x3.33 a=0.6 | 43.03 | 6.688 | True | -0.9563 | 0.1262 | True | 0.3493 | 0.148 | 43.03 | 49.51 | 6.475 |

## 8. The published temperature correction against the shift these pairs actually show

Excluding the two ref 55 pairs, the published shift M = 98 - 15.1 ln(B b^2) lands within 30 °C of the shift the matched pair actually shows, over observed shifts of 35 to 90 °C. Including them, the largest miss is 66 °C. This comparison is an OUTCOME: the observed pair shift is never used to correct the curve it was measured from (D-074, D-078).

## 9. How much the answer depends on the normalization convention

| case | label | n_comparisons | n_families | mean_c | median_c | mae_c | rmse_c | family_weighted_mean_c | family_weighted_sd_c | min_c | max_c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| primary | PRIMARY: energy by ligament volume B b^2 (Lucas), temperature by M = 98 - 15.1 ln(B b^2) (Sokolov Eq. 22) | 10 | 7 | -3.494 | -3.745 | 13.9 | 16.19 | -3.494 | 11.43 | -33.82 | 18.32 |
| S1 energy (Bb)^3/2 | S1: energy by the (B b)^3/2 fracture volume of Corwin et al. | 10 | 7 | -4.507 | -3.983 | 14.26 | 16.73 | -4.485 | 11.89 | -34.85 | 18.2 |
| S2 energy Bb (area) | S2: energy by fracture area B b, which is Sokolov's brittle (lower-shelf) factor | 9 | 7 | 40.75 | 33.17 | 40.75 | 53.79 | 42.94 | 42.09 | 16.15 | 136.4 |
| S3 temperature Lucon | S3: temperature by Lucon et al.'s refit of the same log form | 10 | 7 | -6.605 | -7.852 | 14.81 | 17.21 | -6.614 | 11.5 | -36.63 | 15.46 |
| S4 temperature Towers | S4: temperature by Towers's thickness-only quadratic | 10 | 7 | -23.48 | -27.16 | 23.83 | 29 | -23.23 | 11.78 | -51.2 | 1.765 |
| S5 temperature Wallin | S5: temperature by Wallin's thickness-only logarithm | 10 | 7 | -17.95 | -19.21 | 19.24 | 24.06 | -18.01 | 11.06 | -48.66 | 3.952 |
| S6 KLST as recorded | S6: the dataset's literal width/thickness for the KLST records (D-072 alternative) | 10 | 7 | -3.831 | -3.745 | 14.24 | 16.5 | -3.975 | 11.97 | -33.82 | 18.32 |

**The central bias moves a lot; the scatter barely moves.** Across the four published temperature corrections the family-weighted mean residual runs from -3.5 to -23.2 °C, while the family-weighted standard deviation stays between 11.1 and 11.9 °C. The two volume-type energy normalizations (B b^2 and (B b)^{3/2}) are almost indistinguishable. Pure fracture-area scaling (S2) is far worse, mean +42.9 °C with a standard deviation of 42.1 °C, which is the expected consequence of applying Sokolov's BRITTLE (lower-shelf) factor to a whole transition curve, and is exactly why his own procedure weights two factors by percent shear - a procedure this dataset cannot support (D-076).

Sokolov & Alexander's per-specimen-type shifts (S7) are applied only where the geometry is one of the four types that report built, and are not extrapolated elsewhere:

| pair_id | smaller_geometry | sokolov_specimen_type | applicable | shift_c | two_sigma_c | delta_t_size_c | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 107-283\|107-282 | 27x3x4 a=1 | type 4 | True | 38 | 30 | -23.56 | Sokolov & Alexander Eq. for type 4: +38 (+/- 30) deg C |
| 53-233\|53-225 | 20x3.33x3.33 a=0.51 | type 2 | True | 53 | 24 | 12.38 | Sokolov & Alexander Eq. for type 2: +53 (+/- 24) deg C |
| 53-241\|53-225 | 20x1.5x1.5 a=0.33 | none | False |  |  |  | normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four specimen types NUREG/CR-6379 built, and are not extrapolated |
| 55-257\|55-255 | 23.6x5x5 a=0.76 | type 1 | True | 30 | 28 | 14.26 | Sokolov & Alexander Eq. for type 1: +30 (+/- 28) deg C |
| 55-259\|55-255 | 23.6x3.33x3.33 a=0.51 | type 2 | True | 53 | 24 | -13.88 | Sokolov & Alexander Eq. for type 2: +53 (+/- 24) deg C |
| 59-269\|59-266 | 23.6x3.33x3.33 a=0.51 | type 2 | True | 53 | 24 | -29.34 | Sokolov & Alexander Eq. for type 2: +53 (+/- 24) deg C |
| 59-271.2\|59-266 | 20x2.5x2.5 a=0.38 | none | False |  |  |  | normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four specimen types NUREG/CR-6379 built, and are not extrapolated |
| 59-272\|59-267 | 20x2.5x2.5 a=0.38 | none | False |  |  |  | normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four specimen types NUREG/CR-6379 built, and are not extrapolated |
| 59-278\|59-274 | 20x2.5x2.5 a=0.38 | none | False |  |  |  | normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four specimen types NUREG/CR-6379 built, and are not extrapolated |
| 60-281\|60-280 | 27.5x3.33x3.33 a=0.6 | none | False |  |  |  | normalization not defensibly established for this geometry: Eqs (18)-(21) exist only for the four specimen types NUREG/CR-6379 built, and are not extrapolated |

## 10. How this compares with published estimates

| source | quantity | value |
| --- | --- | --- |
| NUREG/CR-6379 Eqs (18)-(21) | +/- 2 sigma on its own per-type DBTT shifts | 20-30 °C, i.e. sigma 10-15 °C |
| 2026 ML paper, Table 5 (27 SA533B sub-size sets, DBTT) | RMSE of Sokolov's correction | 45.8 °C |
| 2026 ML paper, Table 5 | RMSE of the best analytical correction (Towers) | 35.5 °C |
| 2026 ML paper, Table 7 | RMSE of its best trained ML model | 24.9-27.2 °C |
| **this work**, primary analysis set | family-weighted SD of DT_size | **11.4 °C** (7 families) |
| **this work**, all STRICT comparisons | family-weighted SD of DT_size | **21.1 °C** (10 families) |

The scale found here sits between Sokolov's own quoted sigma and the RMSE the 2026 paper reports for classical methods, which is the expected place for it: fewer but more strictly matched comparisons than the ML paper used, and a different index (T41J here, the tanh midpoint there).

## 11. Why a scalar volume factor cannot remove the specimen-size effect

1. **Less material means less energy.** A miniature specimen breaks a smaller piece of steel, so less plastic work is done and less energy is absorbed. That is the part a geometric factor can capture, and it is why the ligament volume B b^2 works as well as it does.
2. **But thickness also changes the constraint at the notch.** In a thick specimen the material beside the notch root is held by the material around it and cannot contract sideways, so it sits close to plane strain: the stress becomes strongly three-dimensional (high triaxiality), which favours cleavage and pushes the transition to a higher temperature. A thin specimen has more of its cross-section near plane stress, can deform out of plane, and behaves more ductilely at the same temperature. Its transition therefore sits LOWER, and no energy scale factor can express that: it is a temperature effect, not an energy effect, which is why a second, separate temperature correction is needed at all.
3. **The weakest-link effect points the same way.** Cleavage starts at the worst microstructural defect in the stressed volume. A bigger specimen samples more volume, so it is more likely to contain a bad one and fails in a brittle way sooner. This is the Weibull argument Sokolov & Alexander build their log form on.
4. **The parts of the absorbed energy do not scale together.** Crack initiation energy, crack propagation energy and the energy that forms the shear lips at the specimen sides each depend differently on thickness, ligament, notch depth and notch root radius. As a specimen gets thinner the shear lips take up a larger share of the fracture surface, which raises the measured energy on the lower shelf and lowers it on the upper shelf relative to a single scale factor.
5. **Notch geometry is not scaled with the specimen here.** The cohort's miniature specimens have 30° notches with a 0.08 mm root radius (refs 52, 53, 55, 59, 60) or 60° with 0.1 mm (KLST, refs 107, 109), against the full-size 45° and 0.25 mm; and their notch depth to width ratios are 0.15-0.33 against the standard 0.20. They are not photographic reductions of a full-size specimen. NUREG/CR-6379's own conclusion 2 reports that a sharper notch root lowers USE and RAISES the transition temperature, an effect no B b^2 ratio contains.

**Therefore: smaller specimen is not full-size specimen times one volume factor.** No scalar geometry correction is exact physics, and this one is not described as such anywhere in this work.

## 12. What the standards do and do not support

ASTM E2248-18 §5.2 states that transition-region data from miniaturized Charpy specimens "are not directly comparable to those obtained from full-size standard Charpy V-notch specimens and suitable correlation procedures have to be employed", and that "in all instances, correlations will have to be developed to relate upper shelf energy (USE) data from MCVN test to CVN comparable energy levels". §1.3 leaves the comparison with CVN data to the user. **ASTM provides no universal transformation from any miniature geometry to a full-size T41J**, and nothing here should be read as one. §5.2 also warns that MCVN data should not be used directly to set a lowest allowable operating temperature. Where a geometry falls outside a correlation's validated domain it is flagged rather than corrected (`geometry_normalization_factors.csv`): **6 of the 9 miniature geometries in this cohort ARE one of the four specimen types NUREG/CR-6379 built**, on cross-section, notch depth and notch root radius - the 5 x 5 mm geometries are its type 1, the 3.33 x 3.33 mm geometries its type 2, and the KLST its type 4. The remaining 3 (27.5 x 3.33 x 3.33 mm a = 0.6 mm, 20 x 2.5 x 2.5 mm and 20 x 1.5 x 1.5 mm) are not, and for those the primary correction rests on Eq. (22)'s own statement that its form may be used as guidance beyond its four types.

## 13. Relationship to the 2026 machine-learning paper

Kasala Sreenivasulu et al. (2026), *Scientific Reports* 16:16202 - by the authors of this project's own dataset.

| | their work | this work |
| --- | --- | --- |
| question | PREDICT full-size USE and DBTT from sub-size data | DESIGN a test matrix: is the size-correction penalty small enough that more small specimens beat fewer large ones? |
| data | 389 records, 27 sub-size sets, SA533B only, from 4 publications of the same dataset | 18 matched comparisons, 10 families, A533B plate and weld and A508 forging, from 5 publications of the same dataset |
| matching | sub-size sets whose publications also report full-size results under the same processing and test protocol | the same principle, applied field by field and audited for all 4,824 candidate pairs |
| method | temperature shift plus scaled residual projection, targets built from the matched full-size curve, then gradient-boosted trees over 37 input variables | one published geometry normalization and one published temperature correction, both functions of the smaller specimen's own dimensions only |
| headline | R^2 0.942 (USE) and 0.892 (DBTT); better than the analytical methods they benchmarked | a residual size-correction scale of 11.4 °C from 7 families, and the finding that no single geometry has enough matched evidence to support its own correction |

**Overlap:** the same published dataset, the same size-effect problem, the same tanh curve description, and largely the same matched sub-population (their refs 5, 40-42 are this dataset's refs 52, 53, 55, 59).

**Difference that matters for the uncertainty.** Their transformation builds each training target from the paired full-size curve (their Eqs 5-7: shift by DBTT_f - DBTT_s, scale residuals by USE_f/USE_s). That is legitimate and necessary for supervised learning, and their cross-validation correctly holds out whole specimen sets, so their R^2 is an honest measure of PREDICTION accuracy. It is not, and is not claimed by them to be, an independent estimate of how much uncertainty a classical correction adds. This project needs that second quantity, so its correction is not allowed to see the paired full-size curve at all.

**No novelty is claimed beyond this.** Their analytical benchmarks are a larger and more systematic comparison of classical methods than anything here. What this work adds is a strictly matched, fully audited pairing, an out-of-sample correction, an explicit residual-uncertainty estimate with its evidence status, and a statement of where the dataset is too thin to support one. This project trains no model and does not attempt prediction.

## 14. Three uncertainties that are not the same thing (D-082)

1. **Per-curve fit uncertainty (WP4).** How well one curve's own T41J is pinned down by its own specimens: median pairs-bootstrap SD 4.9 °C over the 66 full-size curves with a primary interval.
2. **Size-correction residual disagreement (WP5).** The spread of DT_size across matched comparisons after the classical correction: family-weighted SD 11.4 °C. **This is what WP6 needs, and it is about 2.3 times the per-curve fit uncertainty.**
3. **Between-material and between-study variation.** Differences among matched families, which here cannot be separated from (2): each DT_size is a difference of two independently fitted curves, and a 109-publication compilation carries laboratory, machine, calibration and digitization differences (brief §3).

No WP4 interval width is used as a size penalty, and no variance deconvolution is attempted: the WP4 intervals are nominal rather than calibrated (D-056), so subtracting their variance from the residual variance would be a false precision (D-082).

## 15. What WP6 is handed

| smaller_geometry | B_mm | ligament_b_mm | ligament_volume_Bb2_mm3 | NF_energy_primary | temperature_shift_primary_c | sokolov_specimen_type | n_strict_comparisons | n_primary_comparisons | n_families | n_studies | product_forms | irradiation_states | applicability_notes | central_bias_c | family_delta_t_size_values_c | residual_scale_sd_c | residual_scale_robust_c | evidence_status | evidence_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20x1.5x1.5 a=0.33 | 1.5 | 1.17 | 2.053 | 311.7 | 87.14 | none | 1 | 1 | 1 | 1 | weld metal | unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 1 of 1 primary comparisons; not one of the four specimen types NUREG/CR-6379 built; its Eqs (18)-(21) do not apply | -2.529 | -2.5 |  |  | WEAKLY SUPPORTED | 1 independent family from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 20x2.5x2.5 a=0.38 | 2.5 | 2.12 | 11.24 | 56.96 | 61.47 | none | 4 | 3 | 3 | 1 | forging; plate | irradiated; unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 1 of 3 primary comparisons; not one of the four specimen types NUREG/CR-6379 built; its Eqs (18)-(21) do not apply | -2.492 | -14.0; -5.0; +11.5 |  |  | WEAKLY SUPPORTED | 3 independent families from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 20x3.33x3.33 a=0.51 | 3.33 | 2.82 | 26.48 | 24.17 | 48.53 | type 2 | 1 | 1 | 1 | 1 | weld metal | unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 1 of 1 primary comparisons | 7.902 | +7.9 |  |  | WEAKLY SUPPORTED | 1 independent family from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 20x5x5 a=0.76 | 5 | 4.24 | 89.89 | 7.12 | 30.07 | type 1 | 1 | 0 | 0 | 0 | none | none |  |  |  |  |  | UNSUPPORTED BY THIS DATASET | no matched comparison reaches the primary analysis set; WP6 may not treat this dataset as having measured a correction for this geometry and must use a clearly labelled external literature scenario if it is to be simulated at all |
| 23.6x3.33x3.33 a=0.51 | 3.33 | 2.82 | 26.48 | 24.17 | 48.53 | type 2 | 7 | 2 | 2 | 2 | plate | irradiated; unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 0 of 2 primary comparisons | -26.09 | -33.8; -18.4 |  |  | WEAKLY SUPPORTED | 2 independent families from 2 publications: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 23.6x5x5 a=0.76 | 5 | 4.24 | 89.89 | 7.12 | 30.07 | type 1 | 2 | 1 | 1 | 1 | plate | irradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 0 of 1 primary comparisons | 14.34 | +14.3 |  |  | WEAKLY SUPPORTED | 1 independent family from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 23.6x5x5 a=0.78 | 5 | 4.22 | 89.04 | 7.188 | 30.21 | type 1 | 0 | 0 | 0 | 0 | none | none |  |  |  |  |  | UNSUPPORTED BY THIS DATASET | no matched comparison reaches the primary analysis set; WP6 may not treat this dataset as having measured a correction for this geometry and must use a clearly labelled external literature scenario if it is to be simulated at all |
| 27.5x3.33x3.33 a=0.6 | 3.33 | 2.73 | 24.82 | 25.79 | 49.51 | none | 1 | 1 | 1 | 1 | plate | unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 0 of 1 primary comparisons; not one of the four specimen types NUREG/CR-6379 built; its Eqs (18)-(21) do not apply | 18.32 | +18.3 |  |  | WEAKLY SUPPORTED | 1 independent family from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| 27x3x4 a=1 | 3 | 3 | 27 | 23.7 | 48.23 | type 4 | 1 | 1 | 1 | 1 | forging | unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 0 of 1 primary comparisons | -13.33 | -13.3 |  |  | WEAKLY SUPPORTED | 1 independent family from 1 publication: usable only as a sensitivity, with this limitation stated wherever it is used. Fewer than 4 families, so no standard deviation is reported for this geometry (D-080); the family values are listed. |
| POOLED: all miniature geometries together |  |  |  |  |  | mixed | 18 | 10 | 7 | 5 | forging; plate; weld metal | irradiated; unirradiated | full-size USE above the 200 J limit of NUREG/CR-6379 p.16 in 3 of 10 primary comparisons | -3.494 | -14.0; -13.3; -11.2; -5.0; -2.0; +2.7; +18.3 | 11.43 | 11.34 | WEAKLY SUPPORTED | 7 independent matched families from 5 publications, but only 1-3 families per geometry, so pooling assumes one correction across geometries that differ in ligament volume by a factor of 44. The data neither establish nor refute that assumption: the spread between geometries is the same size as the spread between families within a geometry. Usable as a WP6 sensitivity with that stated; not a geometry-resolved correction. |

Scale definition: family-weighted standard deviation of DT_size about the family-weighted mean, in deg C (DT_size = T41J from the normalized smaller specimen minus the measured full-size T41J)

## 16. Limitations

1. **Very few independent matched families.** 7 in the primary set, 10 in total. Every summary statistic here rests on single digits.
2. **Comparisons within a family are not independent.** Ref 59 alone contributes 5 of the 10 matched families and 9 of the 18 STRICT comparisons; every summary is therefore given family-weighted as well as comparison-weighted.
3. **No heat or lot identifier anywhere in the dataset.** The reported composition is the only heat proxy, which is what empties the cross-study class and confines the analysis to five publications.
4. **Cross-study heterogeneity.** 109 source publications, different machines, calibrations and reporting conventions; most of these curves are digitized from published figures (WebPlotDigitizer, per the descriptor).
5. **No shear-fracture data at all**, so the fracture-mode-dependent procedure that NUREG/CR-6379 actually recommends cannot be run, and a single scalar factor must serve a curve that spans brittle and ductile fracture.
6. **Geometry applicability.** 6 of the 9 miniature geometries are one of the four specimen types NUREG/CR-6379 built; the other 3 rely on Eq. (22)'s own statement that its form may be used as guidance beyond those four types, with its caveat that deviations reflect notch-constraint effects the formula does not contain.
7. **The 200 J upper-shelf limit is exceeded.** 3 of 10 primary comparisons have a full-size USE above the 200 J limit NUREG/CR-6379 sets on its upper-shelf analysis; they are flagged, not dropped.
8. **WP3 fit quality.** 8 of 18 STRICT comparisons are held out of the primary set because either the full-size fit or the transformed refit is weakly identified or boundary-limited; the held set is more scattered than the primary set, which is itself a warning that the primary set is the better-behaved subset rather than a random one.
9. **WP4 interval limitations.** The full-size T41J intervals carried here are nominal 95 % percentile bootstrap intervals with known calibration limits (D-056), and 54 of 134 full-size curves have no reportable interval at all.
10. **Product-form and irradiation imbalance.** Weld metal is one family from one publication; forging is two families; irradiated is two families. None supports a standalone estimate.
11. **Scalar normalization cannot capture constraint.** Section 11 above.
