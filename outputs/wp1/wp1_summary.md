# WP1 summary (eny5v-www93)

Dataset: Materials Cloud record eny5v-www93 (DOI 10.24435/materialscloud:gh-za, issued 2024-12-19)

- Records in: 4775; retained: 3208; excluded: 1567.
- Retained references: 53; retained dataset curve IDs: 210.
- Text values changed (see value_changes_log.csv): 741 cell edits.

## Duplicate-curve detection

Parameters: |dT| <= 3.0 °C, |dE| <= 2% of the larger curve maximum, at least 3 one-to-one matched points and at least 70% of the smaller series matched.

- Candidate pairs with >= 3 matched points: 579; duplicates: 155; partial overlaps (flagged only): 22.
- Series removed: 66 (752 records) from references [8, 9, 10, 13, 14, 17, 19, 20, 22, 26, 27, 28, 33, 37, 38, 40, 44, 45, 46, 52, 53, 55].

Distribution of the matched fraction over candidate pairs (a gap separates chance overlaps from re-publications):

| fraction of smaller series matched | pairs |
| --- | --- |
| (0.0, 0.1] | 0 |
| (0.1, 0.2] | 48 |
| (0.2, 0.3] | 204 |
| (0.3, 0.4] | 121 |
| (0.4, 0.5] | 36 |
| (0.5, 0.6] | 15 |
| (0.6, 0.7] | 0 |
| (0.7, 0.8] | 2 |
| (0.8, 0.9] | 14 |
| (0.9, 0.9999] | 2 |
| (0.9999, 1.0001] | 137 |

Sensitivity of the removals to the three parameters:

| tol_T_C | tol_E_fraction_of_max | min_fraction_matched | duplicate_pairs | partial_overlap_pairs | units_removed | records_removed | references_losing_records | chosen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.01 | 0.6 | 153 | 1 | 64 | 734 | 22 | False |
| 2 | 0.01 | 0.7 | 152 | 2 | 63 | 723 | 22 | False |
| 2 | 0.01 | 0.8 | 148 | 6 | 62 | 710 | 22 | False |
| 2 | 0.01 | 0.9 | 138 | 16 | 58 | 676 | 21 | False |
| 2 | 0.02 | 0.6 | 155 | 20 | 66 | 752 | 22 | False |
| 2 | 0.02 | 0.7 | 155 | 20 | 66 | 752 | 22 | False |
| 2 | 0.02 | 0.8 | 152 | 23 | 66 | 752 | 22 | False |
| 2 | 0.02 | 0.9 | 140 | 35 | 60 | 697 | 22 | False |
| 2 | 0.03 | 0.6 | 159 | 90 | 70 | 794 | 24 | False |
| 2 | 0.03 | 0.7 | 156 | 93 | 67 | 764 | 22 | False |
| 2 | 0.03 | 0.8 | 152 | 97 | 66 | 752 | 22 | False |
| 2 | 0.03 | 0.9 | 140 | 109 | 60 | 697 | 22 | False |
| 3 | 0.01 | 0.6 | 153 | 3 | 64 | 734 | 22 | False |
| 3 | 0.01 | 0.7 | 152 | 4 | 63 | 723 | 22 | False |
| 3 | 0.01 | 0.8 | 149 | 7 | 62 | 710 | 22 | False |
| 3 | 0.01 | 0.9 | 140 | 16 | 59 | 685 | 22 | False |
| 3 | 0.02 | 0.6 | 155 | 22 | 66 | 752 | 22 | False |
| 3 | 0.02 | 0.7 | 155 | 22 | 66 | 752 | 22 | True |
| 3 | 0.02 | 0.8 | 153 | 24 | 66 | 752 | 22 | False |
| 3 | 0.02 | 0.9 | 143 | 34 | 62 | 714 | 22 | False |
| 3 | 0.03 | 0.6 | 159 | 95 | 70 | 794 | 24 | False |
| 3 | 0.03 | 0.7 | 156 | 98 | 67 | 764 | 22 | False |
| 3 | 0.03 | 0.8 | 154 | 100 | 67 | 764 | 22 | False |
| 3 | 0.03 | 0.9 | 144 | 110 | 63 | 726 | 22 | False |
| 5 | 0.01 | 0.6 | 155 | 4 | 66 | 839 | 23 | False |
| 5 | 0.01 | 0.7 | 154 | 5 | 65 | 828 | 23 | False |
| 5 | 0.01 | 0.8 | 152 | 7 | 65 | 828 | 23 | False |
| 5 | 0.01 | 0.9 | 142 | 17 | 61 | 790 | 23 | False |
| 5 | 0.02 | 0.6 | 159 | 27 | 69 | 867 | 23 | False |
| 5 | 0.02 | 0.7 | 157 | 29 | 68 | 857 | 23 | False |
| 5 | 0.02 | 0.8 | 155 | 31 | 68 | 857 | 23 | False |
| 5 | 0.02 | 0.9 | 146 | 40 | 65 | 832 | 23 | False |
| 5 | 0.03 | 0.6 | 166 | 108 | 73 | 909 | 25 | False |
| 5 | 0.03 | 0.7 | 158 | 116 | 69 | 869 | 23 | False |
| 5 | 0.03 | 0.8 | 156 | 118 | 69 | 869 | 23 | False |
| 5 | 0.03 | 0.9 | 147 | 127 | 66 | 844 | 23 | False |

Effect of the rule choosing which copy to keep (same duplicate pairs; 'uncorroborated' = point found in no other copy):

| keep_rule | records_removed | uncorroborated_points_kept | uncorroborated_points_removed |
| --- | --- | --- | --- |
| A (chosen): most records, then earliest publication | 752 | 40 | 3 |
| B: earliest publication, then most records | 783 | 11 | 32 |
| C: most corroborated records, then earliest publication | 770 | 22 | 21 |
