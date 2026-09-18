# WP5 - specimen-size normalization: the method exactly as applied

Pre-registered in DECISIONS.md D-072 to D-086 and committed before any residual existed. Implemented in `src/wp5_normalization.py`; the refits use the unchanged approved WP3 fitter `src/wp3_fitter.py`.

## 1. Symbols

| symbol | meaning | units |
| --- | --- | --- |
| W | specimen width: the dimension the notch is cut into and the crack grows through | mm |
| B | specimen thickness: the dimension parallel to the notch root | mm |
| a | notch depth | mm |
| b = W - a | remaining ligament below the notch | mm |
| B b | fracture area | mm^2 |
| B b^2 | nominal fracture (ligament) volume | mm^3 |
| E | absorbed energy | J |
| T | test temperature | deg C |
| NF_E | energy normalization factor, a ratio of like geometric quantities | dimensionless |
| M | temperature correction added to the smaller specimen's test temperatures | deg C |

Full-size reference (ASTM E23 standard Charpy V-notch): B = 10 mm, W = 10 mm, a = 2 mm, so b = 8 mm, B b = 80 mm^2 and B b^2 = 640 mm^3.

## 2. Primary method (D-073, D-074)

**Energy.**  E_full-size-equivalent = NF_E x E_measured,  with  NF_E = (B b^2)_full-size / (B b^2)_smaller = 640 / (B_s b_s^2).
Source: Lucas et al. (1986), the nominal-fracture-volume normalization; quoted as B b^2 by NUREG/CR-6379 p.14, as NF3 by Lucon/NIST Eq. 10, as B(W-A)^2 by this dataset's own descriptor (Table 2), and in the 2026 ML paper's Table 1. PROJECT_BRIEF.md §5 and §6.4 name the ligament-volume convention, and this is it.

**Temperature.**  T_full-size-equivalent = T_measured + M,  with  M = 98 - 15.1 x ln(B b^2)  [deg C, B b^2 in mm^3].
Source: Sokolov & Alexander, NUREG/CR-6379 (ORNL-6888, 1997) Eq. (22) and Fig. 27, applied as their Eq. (17). Fitted through their four subsize specimen types and forced to give exactly zero for the full-size specimen. Developed on RPV steels (A533B plate, A508 class 2, 15Kh2MFA forging, HSSI weld 72W).

**Both are functions of the smaller specimen's own published dimensions and fixed published constants only.** Nothing about the paired full-size curve enters either one, which is what makes the residual an out-of-sample test rather than a restatement of the pairing.

**Refit.** The transformed points are refitted with the approved WP3 fitter under the FULL-SIZE convention (lower shelf fixed at 2.7 J; USE, T0 and C fitted), and T41J is taken from the analytic crossing under the unchanged D-044 rules, including the tested-range rule applied to the transformed temperatures (D-077).

## 3. What is deliberately not run, and why (D-076)

| method | why it cannot be run here |
| --- | --- |
| Sokolov & Alexander Eq. (11), their own proposed procedure: E = E_s [NF_brittle (100-SHEAR)/100 + NF_ductile SHEAR/100] | the dataset has **no shear-fracture-appearance column at all** (56 columns, none is shear area, fracture appearance or lateral expansion). Shear is absent for all 2,588 primary records, not partly missing. It is not imputed, not derived from temperature and not assumed to be 0 % or 100 %. Their Eq. (12) route from instrumented traces needs F_iu, F_a, F_gy and F_m, which the dataset also lacks. |
| Louden B b^2/(L K_t); Kayano B b^2/K_t' | need an elastic stress-concentration factor K_t, tabulated in the sources for a handful of geometries only (five in the 2026 ML paper's Table 3, against nine miniature geometries here). Louden's DBTT form additionally needs the instrumented maximum force P_m. |
| Kumar dUSE + USE_p | needs precracked-specimen energies; every retained curve here is ordinary Charpy V-notch (D-020). |
| Uehira m(Bb)^n; Wallin (b_f/b_s)^m USE power law | their exponents must be calibrated against the full-size USE of the same material, which is in-sample calibration against the quantity the correction is then scored on. |

## 4. Geometry and the normalization factors it gives

| geometry | geometry_category | curves | studies | klst_geometry_reading | length_mm | W_mm | B_mm | notch_depth_mm | notch_angle_deg | notch_root_radius_mm | ligament_b_mm | notch_depth_over_width | fracture_area_Bb_mm2 | ligament_volume_Bb2_mm3 | notch_depth_over_root_radius | sokolov_specimen_type | sokolov_per_type_shift_c | sokolov_per_type_two_sigma_c | normalization_applicable | NF_E [ligament volume B b^2 (Lucas et al.)] | NF_E [fracture volume (B b)^3/2 (Corwin et al.)] | NF_E [fracture area B b (Corwin first factor; Sokolov NF_brittle)] | M_degC [M = 98 - 15.1 ln(B b^2) (Sokolov & Alexander, NUREG/CR-6379 Eq. 22)] | M_degC [M = 92.7 - 14.34 ln(B b^2) (Lucon et al.)] | M_degC [M = 0.7 (10 - B)^2 (Towers)] | M_degC [M = -51.4 ln(2 (B/10)^0.25 - 1) (Wallin)] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 55x10x10 a=2 | full-size | 60 | 20 | standard KLST (D-072 primary) | 55 | 10 | 10 | 2 | 45 | 0.25 | 8 | 0.2 | 80 | 640 | 8 | none |  |  | True | 1 | 1 | 1 | 0.4318 | 0.04255 | 0 | -0 |
| 55x10x10 a=? | full-size | 74 | 24 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | False |  |  |  |  |  |  |  |
| 20x5x5 a=0.76 | miniature | 4 | 1 | standard KLST (D-072 primary) | 20 | 5 | 5 | 0.76 | 30 | 0.08 | 4.24 | 0.152 | 21.2 | 89.89 | 9.5 | type 1 | 30 | 28 | True | 7.12 | 7.33 | 3.774 | 30.07 | 28.19 | 17.5 | 19.69 |
| 23.6x5x5 a=0.76 | miniature | 2 | 1 | standard KLST (D-072 primary) | 23.6 | 5 | 5 | 0.76 | 30 | 0.08 | 4.24 | 0.152 | 21.2 | 89.89 | 9.5 | type 1 | 30 | 28 | True | 7.12 | 7.33 | 3.774 | 30.07 | 28.19 | 17.5 | 19.69 |
| 23.6x5x5 a=0.78 | miniature | 1 | 1 | standard KLST (D-072 primary) | 23.6 | 5 | 5 | 0.78 | 30 | 0.08 | 4.22 | 0.156 | 21.1 | 89.04 | 9.75 | type 1 | 30 | 28 | True | 7.188 | 7.383 | 3.791 | 30.21 | 28.33 | 17.5 | 19.69 |
| 27x3x4 a=1 | miniature | 8 | 2 | standard KLST (D-072 primary) | 27 | 4 | 3 | 1 | 60 | 0.1 | 3 | 0.25 | 9 | 27 | 10 | type 4 | 38 | 30 | True | 23.7 | 26.5 | 8.889 | 48.23 | 45.44 | 34.3 | 37.71 |
| 20x3.33x3.33 a=0.51 | miniature | 4 | 1 | standard KLST (D-072 primary) | 20 | 3.33 | 3.33 | 0.51 | 30 | 0.08 | 2.82 | 0.1532 | 9.391 | 26.48 | 6.375 | type 2 | 53 | 24 | True | 24.17 | 24.87 | 8.519 | 48.53 | 45.72 | 31.14 | 33.68 |
| 23.6x3.33x3.33 a=0.51 | miniature | 7 | 2 | standard KLST (D-072 primary) | 23.6 | 3.33 | 3.33 | 0.51 | 30 | 0.08 | 2.82 | 0.1532 | 9.391 | 26.48 | 6.375 | type 2 | 53 | 24 | True | 24.17 | 24.87 | 8.519 | 48.53 | 45.72 | 31.14 | 33.68 |
| 27.5x3.33x3.33 a=0.6 | miniature | 1 | 1 | standard KLST (D-072 primary) | 27.5 | 3.33 | 3.33 | 0.6 | 30 | 0.08 | 2.73 | 0.1802 | 9.091 | 24.82 | 7.5 | none |  |  | True | 25.79 | 26.11 | 8.8 | 49.51 | 46.65 | 31.14 | 33.68 |
| 27x3x4 a=1 | miniature | 8 | 2 | dataset literal (D-075 S6) | 27 | 3 | 4 | 1 | 60 | 0.1 | 2 | 0.3333 | 8 | 16 | 10 | none |  |  | True | 40 | 31.62 | 10 | 56.13 | 52.94 | 25.2 | 27.07 |
| 20x2.5x2.5 a=0.38 | miniature | 5 | 1 | standard KLST (D-072 primary) | 20 | 2.5 | 2.5 | 0.38 | 30 | 0.08 | 2.12 | 0.152 | 5.3 | 11.24 | 4.75 | none |  |  | True | 56.96 | 58.64 | 15.09 | 61.47 | 58.01 | 39.38 | 45.3 |
| 20x1.5x1.5 a=0.33 | miniature | 4 | 1 | standard KLST (D-072 primary) | 20 | 1.5 | 1.5 | 0.33 | 30 | 0.08 | 1.17 | 0.22 | 1.755 | 2.053 | 4.125 | none |  |  | True | 311.7 | 307.8 | 45.58 | 87.14 | 82.38 | 50.57 | 72.36 |

## 5. Checks that must pass before any number is used (D-086)

| check | detail | result |
| --- | --- | --- |
| dimensional consistency | B b has units mm^2 and B b^2 mm^3; full-size 10 mm x 8 mm = 80 mm^2 and 10 mm x (8 mm)^2 = 640 mm^3; every NF is a ratio of like quantities (dimensionless); every shift is in deg C; ln(B b^2) takes mm^3, which is the unit the published constants were fitted in | pass |
| identity: energy NF at full size | ligament volume B b^2 (Lucas et al.): NF = 1 | pass (exactly 1) |
| identity: energy NF at full size | fracture volume (B b)^3/2 (Corwin et al.): NF = 1 | pass (exactly 1) |
| identity: energy NF at full size | fracture area B b (Corwin first factor; Sokolov NF_brittle): NF = 1 | pass (exactly 1) |
| identity: temperature shift at full size | M = 98 - 15.1 ln(B b^2) (Sokolov & Alexander, NUREG/CR-6379 Eq. 22): M = +0.4318 deg C | pass (\|M\| = 0.43 deg C, the rounding of the published coefficients; the source states the fit was forced through zero at the full-size specimen) |
| identity: temperature shift at full size | M = 92.7 - 14.34 ln(B b^2) (Lucon et al.): M = +0.0425 deg C | pass (\|M\| = 0.04 deg C, the rounding of the published coefficients; the source states the fit was forced through zero at the full-size specimen) |
| identity: temperature shift at full size | M = 0.7 (10 - B)^2 (Towers): M = +0.0000 deg C | pass (exactly 0) |
| identity: temperature shift at full size | M = -51.4 ln(2 (B/10)^0.25 - 1) (Wallin): M = -0.0000 deg C | pass (exactly 0) |
| hand-calculated example (23.6 x 5 x 5 mm, a = 0.76 mm) | b = W - a = 5.00 - 0.76 = 4.24 mm; B b^2 = 5.00 x 4.24^2 = 5.00 x 17.9776 = 89.8880 mm^3; NF_E = 640 / 89.8880 = 7.1200; M = 98 - 15.1 x ln(89.8880) = 98 - 15.1 x 4.4986 = 30.07 deg C | pass (code gives NF_E = 7.1200, M = 30.07 deg C) |
| round trip | T_fse - M and E_fse / NF_E return the measured temperatures and energies | pass (max \|dT\| = 0.00e+00 deg C, max relative \|dE\| = 1.48e-16) |
| no-op shift | the full-size geometry gives NF_E = 1 and M = +0.4318 deg C, so the transformed temperatures move by +0.4318 deg C and the energies not at all | pass |
| monotonicity | over the 5.0, 3.33, 2.5 and 1.5 mm cross-sections the energy factor rises 7.1 -> 311.7 and the shift rises 30.1 -> 87.1 deg C as the ligament volume falls | pass |
| reproduces NUREG/CR-6379 for its type 1 | Table 2 ratios published Bb 3.77, Bb^2 7.12, (Bb)^3/2 7.33; recomputed 3.78, 7.13, 7.34. Eq. (22) gives M = 30.1 deg C against the type-specific Eq. shift +30 (+/- 28) deg C | pass (largest Table 2 difference 0.1 %) |
| reproduces NUREG/CR-6379 for its type 2 | Table 2 ratios published Bb 8.52, Bb^2 24.2, (Bb)^3/2 24.8; recomputed 8.51, 24.13, 24.84. Eq. (22) gives M = 48.5 deg C against the type-specific Eq. shift +53 (+/- 24) deg C | pass (largest Table 2 difference 0.3 %) |
| reproduces NUREG/CR-6379 for its type 3 | Table 2 ratios published Bb 4.0, Bb^2 8.0, (Bb)^3/2 8.0; recomputed 4.00, 8.00, 8.00. Eq. (22) gives M = 31.8 deg C against the type-specific Eq. shift +34 (+/- 20) deg C | pass (largest Table 2 difference 0.0 %) |
| reproduces NUREG/CR-6379 for its type 4 | Table 2 ratios published Bb 8.9, Bb^2 23.7, (Bb)^3/2 26.5; recomputed 8.89, 23.70, 26.50. Eq. (22) gives M = 48.2 deg C against the type-specific Eq. shift +38 (+/- 30) deg C | pass (largest Table 2 difference 0.1 %) |

A hand calculation for the 23.6 x 5 x 5 mm geometry, so it can be repeated with a calculator: the ligament is b = W - a = 5.00 - 0.76 = 4.24 mm; the nominal fracture volume is B b^2 = 5.00 x 4.24^2 = 89.888 mm^3; the energy factor is NF_E = 640 / 89.888 = 7.120; the temperature correction is M = 98 - 15.1 x ln(89.888) = 98 - 15.1 x 4.4986 = 30.07 deg C. NUREG/CR-6379's own Table 2 gives 7.12 for the same ratio and its Eq. (18) gives +30 deg C for the same specimen, which is an end-to-end check of both the equations and the convention for which dimension is notched.
