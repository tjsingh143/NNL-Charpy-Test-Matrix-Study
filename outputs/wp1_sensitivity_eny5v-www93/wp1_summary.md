# WP1 summary (eny5v-www93)

Dataset: Materials Cloud 2024.206, record eny5v-www93 (DOI 10.24435/materialscloud:gh-za, issued 2024-12-19)

- Records in: 4775; retained: 3050; excluded: 1725.
- Retained references: 54; retained dataset curve IDs: 208.
- Text values changed (see value_changes_log.csv): 741 cell edits.

## Duplicate-curve detection

Parameters: |dT| <= 3.0 °C, |dE| <= 2% of the larger curve maximum, at least 3 one-to-one matched points and at least 70% of the smaller series matched.

- Candidate pairs with >= 3 matched points: 581; duplicates by plain point matching: 156; duplicates by constant-axis-offset matching: 2; partial overlaps (flagged only): 20.
- Constant-offset test: one copy shifted by a constant -6 to 6 °C and scaled by 0.98-1.02 in energy, then matched within 1 °C and 1%; duplicate if >= 5 points and >= 70% of the smaller copy match. Pairs found: ref 1 curve 6 (95) with ref 21 curve 99 (104): 73 matched at offset -3 °C, scale 1; ref 1 curve 6 (10) with ref 21 curve 99 (12): 8 matched at offset -3 °C, scale 1.01.
- Series removed: 69 (910 records) from references [8, 9, 10, 13, 14, 19, 20, 21, 22, 26, 27, 28, 33, 37, 38, 40, 43, 45, 46, 52, 53].
- Which criterion of the canonical hierarchy decided each removal: (b) earlier publication (original source): 63; (c) fewer unresolved labeling problems: 2; (d) tie-breaker: earlier spreadsheet row: 3; (d) tie-breaker: lower reference ID: 1.
- Removed copies whose irradiation label differs from the kept copy: 0.
- Records retained under the alternative keep rule (most records first): 3092 (chosen rule: 3050).

Distribution of the matched fraction over candidate pairs (a gap separates chance overlaps from re-publications):

| fraction of smaller series matched | pairs |
| --- | --- |
| (0.0, 0.1] | 0 |
| (0.1, 0.2] | 48 |
| (0.2, 0.3] | 205 |
| (0.3, 0.4] | 121 |
| (0.4, 0.5] | 35 |
| (0.5, 0.6] | 14 |
| (0.6, 0.7] | 0 |
| (0.7, 0.8] | 4 |
| (0.8, 0.9] | 14 |
| (0.9, 0.9999] | 2 |
| (0.9999, 1.0001] | 138 |

Sensitivity of the removals to the three parameters:

| tol_T_C | tol_E_fraction_of_max | min_fraction_matched | duplicate_pairs | partial_overlap_pairs | units_removed | records_removed | references_losing_records | chosen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 0.01 | 0.6 | 156 | 1 | 67 | 891 | 21 | False |
| 2 | 0.01 | 0.7 | 155 | 2 | 66 | 880 | 21 | False |
| 2 | 0.01 | 0.8 | 151 | 6 | 65 | 855 | 21 | False |
| 2 | 0.01 | 0.9 | 141 | 16 | 61 | 821 | 21 | False |
| 2 | 0.02 | 0.6 | 158 | 20 | 69 | 910 | 21 | False |
| 2 | 0.02 | 0.7 | 158 | 20 | 69 | 910 | 21 | False |
| 2 | 0.02 | 0.8 | 155 | 23 | 69 | 910 | 21 | False |
| 2 | 0.02 | 0.9 | 143 | 35 | 63 | 843 | 21 | False |
| 2 | 0.03 | 0.6 | 162 | 90 | 73 | 955 | 23 | False |
| 2 | 0.03 | 0.7 | 159 | 93 | 70 | 922 | 21 | False |
| 2 | 0.03 | 0.8 | 155 | 97 | 69 | 910 | 21 | False |
| 2 | 0.03 | 0.9 | 143 | 109 | 63 | 843 | 21 | False |
| 3 | 0.01 | 0.6 | 156 | 1 | 67 | 891 | 21 | False |
| 3 | 0.01 | 0.7 | 155 | 2 | 66 | 880 | 21 | False |
| 3 | 0.01 | 0.8 | 152 | 5 | 65 | 855 | 21 | False |
| 3 | 0.01 | 0.9 | 143 | 14 | 62 | 830 | 21 | False |
| 3 | 0.02 | 0.6 | 158 | 20 | 69 | 910 | 21 | False |
| 3 | 0.02 | 0.7 | 158 | 20 | 69 | 910 | 21 | True |
| 3 | 0.02 | 0.8 | 156 | 22 | 69 | 910 | 21 | False |
| 3 | 0.02 | 0.9 | 146 | 32 | 65 | 860 | 21 | False |
| 3 | 0.03 | 0.6 | 162 | 93 | 73 | 955 | 23 | False |
| 3 | 0.03 | 0.7 | 159 | 96 | 70 | 922 | 21 | False |
| 3 | 0.03 | 0.8 | 157 | 98 | 70 | 922 | 21 | False |
| 3 | 0.03 | 0.9 | 147 | 108 | 66 | 872 | 21 | False |
| 5 | 0.01 | 0.6 | 156 | 4 | 67 | 891 | 21 | False |
| 5 | 0.01 | 0.7 | 155 | 5 | 66 | 880 | 21 | False |
| 5 | 0.01 | 0.8 | 153 | 7 | 66 | 880 | 21 | False |
| 5 | 0.01 | 0.9 | 143 | 17 | 62 | 830 | 21 | False |
| 5 | 0.02 | 0.6 | 160 | 27 | 70 | 920 | 21 | False |
| 5 | 0.02 | 0.7 | 158 | 29 | 69 | 910 | 21 | False |
| 5 | 0.02 | 0.8 | 156 | 31 | 69 | 910 | 21 | False |
| 5 | 0.02 | 0.9 | 147 | 40 | 66 | 885 | 21 | False |
| 5 | 0.03 | 0.6 | 167 | 108 | 75 | 986 | 24 | False |
| 5 | 0.03 | 0.7 | 159 | 116 | 70 | 922 | 21 | False |
| 5 | 0.03 | 0.8 | 157 | 118 | 70 | 922 | 21 | False |
| 5 | 0.03 | 0.9 | 148 | 127 | 67 | 897 | 21 | False |

Effect of the rule choosing which copy to keep (same duplicate pairs; 'uncorroborated' = point found in no other copy):

| keep_rule | series_removed | records_removed | uncorroborated_points_kept | uncorroborated_points_removed | series_kept_with_unresolved_label_problems | series_removed_here_but_kept_by_chosen_rule | series_kept_here_but_removed_by_chosen_rule |
| --- | --- | --- | --- | --- | --- | --- | --- |
| canonical hierarchy (chosen) | 69 | 910 | 35 | 65 | 2 | 0 | 0 |
| most records, then fewer labeling problems (sensitivity alternative) | 69 | 868 | 73 | 27 | 2 | 9 | 9 |
| most records, then earliest publication (CP1 rule) | 69 | 868 | 73 | 27 | 4 | 11 | 11 |
| earliest publication, then most records | 69 | 910 | 35 | 65 | 4 | 2 | 2 |
| most corroborated records, then earliest publication | 69 | 888 | 53 | 47 | 4 | 5 | 5 |
