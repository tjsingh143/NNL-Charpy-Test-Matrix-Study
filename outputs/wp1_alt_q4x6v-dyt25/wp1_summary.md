# WP1 summary (q4x6v-dyt25)

Dataset: Materials Cloud record q4x6v-dyt25 (DOI 10.24435/materialscloud:p6-5y, issued 2025-02-26)

- Records in: 4961; retained: 3409; excluded: 1552.
- Retained references: 55; retained dataset curve IDs: 224.
- Text values changed (see value_changes_log.csv): 973 cell edits.

## Duplicate-curve detection

Parameters: |dT| <= 3.0 °C, |dE| <= 2% of the larger curve maximum, at least 3 one-to-one matched points and at least 70% of the smaller series matched.

- Candidate pairs with >= 3 matched points: 507; duplicates: 143; partial overlaps (flagged only): 22.
- Series removed: 62 (699 records) from references [10, 14, 17, 19, 20, 22, 26, 27, 28, 33, 37, 38, 40, 44, 45, 46, 52, 53, 55].

Distribution of the matched fraction over candidate pairs (a gap separates chance overlaps from re-publications):

| fraction of smaller series matched | pairs |
| --- | --- |
| (0.0, 0.1] | 0 |
| (0.1, 0.2] | 44 |
| (0.2, 0.3] | 178 |
| (0.3, 0.4] | 98 |
| (0.4, 0.5] | 29 |
| (0.5, 0.6] | 15 |
| (0.6, 0.7] | 0 |
| (0.7, 0.8] | 2 |
| (0.8, 0.9] | 14 |
| (0.9, 0.9999] | 2 |
| (0.9999, 1.0001] | 125 |

Sensitivity of the removals to the three parameters:

| tol_T_C | tol_E_fraction_of_max | min_fraction_matched | duplicate_pairs | partial_overlap_pairs | units_removed | records_removed | references_losing_records | chosen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.01 | 0.6 | 141 | 1 | 60 | 681 | 19 | False |
| 2 | 0.01 | 0.7 | 140 | 2 | 59 | 670 | 19 | False |
| 2 | 0.01 | 0.8 | 137 | 5 | 58 | 657 | 19 | False |
| 2 | 0.01 | 0.9 | 127 | 15 | 54 | 623 | 18 | False |
| 2 | 0.02 | 0.6 | 143 | 20 | 62 | 699 | 19 | False |
| 2 | 0.02 | 0.7 | 143 | 20 | 62 | 699 | 19 | False |
| 2 | 0.02 | 0.8 | 141 | 22 | 62 | 699 | 19 | False |
| 2 | 0.02 | 0.9 | 129 | 34 | 56 | 644 | 19 | False |
| 2 | 0.03 | 0.6 | 146 | 73 | 65 | 732 | 21 | False |
| 2 | 0.03 | 0.7 | 144 | 75 | 63 | 711 | 19 | False |
| 2 | 0.03 | 0.8 | 141 | 78 | 62 | 699 | 19 | False |
| 2 | 0.03 | 0.9 | 129 | 90 | 56 | 644 | 19 | False |
| 3 | 0.01 | 0.6 | 141 | 3 | 60 | 681 | 19 | False |
| 3 | 0.01 | 0.7 | 140 | 4 | 59 | 670 | 19 | False |
| 3 | 0.01 | 0.8 | 137 | 7 | 58 | 657 | 19 | False |
| 3 | 0.01 | 0.9 | 128 | 16 | 55 | 632 | 19 | False |
| 3 | 0.02 | 0.6 | 143 | 22 | 62 | 699 | 19 | False |
| 3 | 0.02 | 0.7 | 143 | 22 | 62 | 699 | 19 | True |
| 3 | 0.02 | 0.8 | 141 | 24 | 62 | 699 | 19 | False |
| 3 | 0.02 | 0.9 | 131 | 34 | 58 | 661 | 19 | False |
| 3 | 0.03 | 0.6 | 146 | 78 | 65 | 732 | 21 | False |
| 3 | 0.03 | 0.7 | 144 | 80 | 63 | 711 | 19 | False |
| 3 | 0.03 | 0.8 | 142 | 82 | 63 | 711 | 19 | False |
| 3 | 0.03 | 0.9 | 132 | 92 | 59 | 673 | 19 | False |
| 5 | 0.01 | 0.6 | 143 | 4 | 62 | 786 | 20 | False |
| 5 | 0.01 | 0.7 | 142 | 5 | 61 | 775 | 20 | False |
| 5 | 0.01 | 0.8 | 140 | 7 | 61 | 775 | 20 | False |
| 5 | 0.01 | 0.9 | 130 | 17 | 57 | 737 | 20 | False |
| 5 | 0.02 | 0.6 | 147 | 27 | 65 | 814 | 20 | False |
| 5 | 0.02 | 0.7 | 145 | 29 | 64 | 804 | 20 | False |
| 5 | 0.02 | 0.8 | 143 | 31 | 64 | 804 | 20 | False |
| 5 | 0.02 | 0.9 | 134 | 40 | 61 | 779 | 20 | False |
| 5 | 0.03 | 0.6 | 153 | 89 | 68 | 847 | 22 | False |
| 5 | 0.03 | 0.7 | 146 | 96 | 65 | 816 | 20 | False |
| 5 | 0.03 | 0.8 | 144 | 98 | 65 | 816 | 20 | False |
| 5 | 0.03 | 0.9 | 135 | 107 | 62 | 791 | 20 | False |

Effect of the rule choosing which copy to keep (same duplicate pairs; 'uncorroborated' = point found in no other copy):

| keep_rule | records_removed | uncorroborated_points_kept | uncorroborated_points_removed |
| --- | --- | --- | --- |
| A (chosen): most records, then earliest publication | 699 | 40 | 3 |
| B: earliest publication, then most records | 730 | 11 | 32 |
| C: most corroborated records, then earliest publication | 717 | 22 | 21 |
