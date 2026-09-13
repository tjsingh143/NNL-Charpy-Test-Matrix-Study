# WP1 unit checks

The dataset authors state that they converted all values to one unit per column [descriptor]. WP1 therefore verifies rather than converts. No conversion was applied to any value. Checks use in-scope ferritic records unless stated otherwise.

## Temperature (°C)

- Test temperature range: -196.90 to 377.55 °C. Below absolute zero: 0. Outside the review window (-200.0, 400.0): 0.
- A column left in kelvin would have no values below 0 and cluster near 77-600; a column left in °F would put liquid-nitrogen tests near -321. Neither pattern is present: the coldest tests sit at the liquid-nitrogen point (-196 °C).
- Irradiation temperatures and what they equal in other units (a whole number suggests the original unit):

| value_C | in_K | in_F | records |
| --- | --- | --- | --- |
| 149.00 | 422.15 | 300.20 | 21 |
| 150.00 | 423.15 | 302.00 | 72 |
| 200.00 | 473.15 | 392.00 | 19 |
| 269.85 | 543.00 | 517.73 | 19 |
| 288.00 | 561.15 | 550.40 | 102 |
| 290.00 | 563.15 | 554.00 | 61 |

## Absorbed energy (J)

If a curve's energies had been left in ft-lbf while its dataset USE was in joules, the curve's highest energy would sit near 0.74 x USE (1 ft-lbf = 1.3558 J); the reverse error would give about 1.36 x USE.

- Retained dataset curves checked: 210. Ratio max(energy)/USE: median 1.026, 5th-95th percentile 0.974-1.133, min 0.922, max 1.448.
- Curves with ratio below 0.85 or above 1.25: 1 (271: 1.45).
- Limitation: this detects inconsistency within a curve. A source whose energies and USE were both left unconverted would pass; that can only be ruled out against the source papers.

## Fluence (n/cm²)

- Range 6.2e+17 to 1e+20. Values in n/m² would be 10^4 times larger (typically 1e21-1e24); values in dpa would be below about 1. All values are consistent with n/cm².
- The neutron-energy threshold is not stated anywhere in the dataset (D-011).

## Specimen dimensions (mm)

Inch values would appear as 2.165 (55 mm), 0.394 (10 mm), 0.079 (2 mm) or 0.010 (0.25 mm). None are present.

| column | distinct values |
| --- | --- |
| length_mm | 20, 23.6, 24.1, 27.5, 55 |
| width_mm | 1.5, 2.5, 3.33, 4.8, 5, 10 |
| thickness_mm | 1.5, 2.5, 3.33, 4.8, 5, 6, 10 |
| notch_depth_mm | 0.33, 0.38, 0.51, 0.6, 0.76, 0.78, 0.97, 2 |
| notch_angle_deg | 30, 45 |
| notch_root_radius_mm | 0.08, 0.25 |

## Composition (wt.%)

- Records with Fe reported: 3908. Sum of all reported elements: 100.000 to 100.019 wt.%; outside 99-101: 0. Sums close to 100 are expected because Fe was often computed as the balance, so this check mainly catches ppm-for-wt.% entry errors (none seen).
