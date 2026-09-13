# WP1 summary (q4x6v-dyt25)

Dataset: Materials Cloud 2025.30, record q4x6v-dyt25 (DOI 10.24435/materialscloud:p6-5y, issued 2025-02-26)

- Records in: 4961; retained: 3325; excluded: 1636.
- Retained references: 56; retained dataset curve IDs: 220.
- Text values changed (see value_changes_log.csv): 973 cell edits.

## Duplicate-curve detection

Parameters: |dT| <= 3.0 °C, |dE| <= 2% of the larger curve maximum, at least 3 one-to-one matched points and at least 70% of the smaller series matched.

- Candidate pairs with >= 3 matched points: 580; duplicates: 155; partial overlaps (flagged only): 22.
- Series removed: 66 (783 records) from references [8, 9, 10, 13, 14, 19, 20, 22, 26, 27, 28, 33, 37, 38, 40, 43, 45, 46, 52, 53].
- Which criterion of the canonical hierarchy decided each removal: (b) earlier publication (original source): 61; (c) fewer unresolved labeling problems: 1; (d) tie-breaker: earlier spreadsheet row: 3; (d) tie-breaker: lower reference ID: 1.
- Removed copies whose irradiation label differs from the kept copy: 4.
- Records retained under the alternative keep rule (most records first): 3356 (chosen rule: 3325).

Distribution of the matched fraction over candidate pairs (a gap separates chance overlaps from re-publications):

| fraction of smaller series matched | pairs |
| --- | --- |
| (0.0, 0.1] | 0 |
| (0.1, 0.2] | 48 |
| (0.2, 0.3] | 205 |
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
| 2 | 0.01 | 0.6 | 153 | 1 | 64 | 764 | 20 | False |
| 2 | 0.01 | 0.7 | 152 | 2 | 63 | 753 | 20 | False |
| 2 | 0.01 | 0.8 | 148 | 6 | 62 | 728 | 20 | False |
| 2 | 0.01 | 0.9 | 138 | 16 | 58 | 694 | 20 | False |
| 2 | 0.02 | 0.6 | 155 | 20 | 66 | 783 | 20 | False |
| 2 | 0.02 | 0.7 | 155 | 20 | 66 | 783 | 20 | False |
| 2 | 0.02 | 0.8 | 152 | 23 | 66 | 783 | 20 | False |
| 2 | 0.02 | 0.9 | 140 | 35 | 60 | 716 | 20 | False |
| 2 | 0.03 | 0.6 | 159 | 90 | 70 | 828 | 22 | False |
| 2 | 0.03 | 0.7 | 156 | 93 | 67 | 795 | 20 | False |
| 2 | 0.03 | 0.8 | 152 | 97 | 66 | 783 | 20 | False |
| 2 | 0.03 | 0.9 | 140 | 109 | 60 | 716 | 20 | False |
| 3 | 0.01 | 0.6 | 153 | 3 | 64 | 764 | 20 | False |
| 3 | 0.01 | 0.7 | 152 | 4 | 63 | 753 | 20 | False |
| 3 | 0.01 | 0.8 | 149 | 7 | 62 | 728 | 20 | False |
| 3 | 0.01 | 0.9 | 140 | 16 | 59 | 703 | 20 | False |
| 3 | 0.02 | 0.6 | 155 | 22 | 66 | 783 | 20 | False |
| 3 | 0.02 | 0.7 | 155 | 22 | 66 | 783 | 20 | True |
| 3 | 0.02 | 0.8 | 153 | 24 | 66 | 783 | 20 | False |
| 3 | 0.02 | 0.9 | 143 | 34 | 62 | 733 | 20 | False |
| 3 | 0.03 | 0.6 | 159 | 95 | 70 | 828 | 22 | False |
| 3 | 0.03 | 0.7 | 156 | 98 | 67 | 795 | 20 | False |
| 3 | 0.03 | 0.8 | 154 | 100 | 67 | 795 | 20 | False |
| 3 | 0.03 | 0.9 | 144 | 110 | 63 | 745 | 20 | False |
| 5 | 0.01 | 0.6 | 155 | 4 | 66 | 880 | 21 | False |
| 5 | 0.01 | 0.7 | 154 | 5 | 65 | 869 | 21 | False |
| 5 | 0.01 | 0.8 | 152 | 7 | 65 | 869 | 21 | False |
| 5 | 0.01 | 0.9 | 142 | 17 | 61 | 819 | 21 | False |
| 5 | 0.02 | 0.6 | 159 | 27 | 69 | 909 | 21 | False |
| 5 | 0.02 | 0.7 | 157 | 29 | 68 | 899 | 21 | False |
| 5 | 0.02 | 0.8 | 155 | 31 | 68 | 899 | 21 | False |
| 5 | 0.02 | 0.9 | 146 | 40 | 65 | 874 | 21 | False |
| 5 | 0.03 | 0.6 | 166 | 108 | 74 | 975 | 24 | False |
| 5 | 0.03 | 0.7 | 158 | 116 | 69 | 911 | 21 | False |
| 5 | 0.03 | 0.8 | 156 | 118 | 69 | 911 | 21 | False |
| 5 | 0.03 | 0.9 | 147 | 127 | 66 | 886 | 21 | False |

Effect of the rule choosing which copy to keep (same duplicate pairs; 'uncorroborated' = point found in no other copy):

| keep_rule | series_removed | records_removed | uncorroborated_points_kept | uncorroborated_points_removed | series_kept_with_unresolved_label_problems | series_removed_here_but_kept_by_chosen_rule | series_kept_here_but_removed_by_chosen_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| canonical hierarchy (chosen) | 66 | 783 | 11 | 32 | 0 | 0 | 0 |
| most records, then fewer labeling problems (sensitivity alternative) | 66 | 752 | 40 | 3 | 0 | 7 | 7 |
| most records, then earliest publication (CP1 rule) | 66 | 752 | 40 | 3 | 1 | 8 | 8 |
| earliest publication, then most records | 66 | 783 | 11 | 32 | 1 | 1 | 1 |
| most corroborated records, then earliest publication | 66 | 770 | 22 | 21 | 1 | 3 | 3 |
