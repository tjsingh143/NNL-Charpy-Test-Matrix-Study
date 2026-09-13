# WP2 version sensitivity: 2025.30 (primary) versus 2024.206

Curves are matched by their exact record sets. Measurements are identical in the two releases for refs 1-106 (WP0); differences come from refs 107-109 and from metadata the releases label differently.

## Cohort sizes

| cohort | curves_2025 | records_2025 | curves_2024 | records_2024 |
| --- | --- | --- | --- | --- |
| primary | 170 | 2588 | 161 | 2454 |
| looser | 182 | 2692 | 172 | 2544 |
| stricter | 60 | 1333 | 54 | 1235 |
| alt_keep_rule | 170 | 2628 | 161 | 2494 |
| plus_unresolved_irradiation | 179 | 2704 | 170 | 2570 |
| plus_additively_manufactured | 175 | 2654 | 166 | 2520 |
| piping_secondary | 15 | 181 | 15 | 181 |

## Curves that differ

| change | curves | records |
| --- | --- | --- |
| differs: irradiated | 3 | 56 |
| differs: irradiated, treatment | 4 | 36 |
| differs: irradiated, treatment, orientation | 4 | 46 |
| differs: treatment | 4 | 65 |
| differs: treatment, orientation | 15 | 245 |
| reference only in 2025.30 (refs 107-109) | 10 | 148 |

| ref_id | curve_2025 | curve_2024 | records | change | cohort_primary_2025 | cohort_primary_2024 |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 7-27 | 7-27 | 10 | differs: irradiated, treatment | False | False |
| 7 | 7-28 | 7-28 | 7 | differs: irradiated, treatment | False | False |
| 7 | 7-29 | 7-29 | 12 | differs: irradiated, treatment | False | False |
| 7 | 7-30 | 7-30 | 7 | differs: irradiated, treatment | False | False |
| 8 | 8-31 | 8-31 | 25 | differs: irradiated | False | False |
| 8 | 8-32 | 8-32 | 17 | differs: irradiated | False | False |
| 9 | 9-35 | 9-35 | 14 | differs: irradiated | False | False |
| 18 | 18-86.1 | 18-86.1 | 4 | differs: treatment | False | False |
| 18 | 18-86.2 | 18-86.2 | 4 | differs: treatment | False | False |
| 53 | 53-223 | 53-223 | 18 | differs: irradiated, treatment, orientation | False | False |
| 53 | 53-224 | 53-224 | 16 | differs: irradiated, treatment, orientation | False | False |
| 53 | 53-225 | 53-225 | 17 | differs: treatment, orientation | True | True |
| 53 | 53-226 | 53-226 | 23 | differs: treatment, orientation | True | True |
| 53 | 53-227 | 53-227 | 24 | differs: treatment, orientation | True | True |
| 53 | 53-228 | 53-228 | 19 | differs: treatment, orientation | True | True |
| 53 | 53-229 | 53-229 | 29 | differs: treatment, orientation | True | True |
| 53 | 53-230 | 53-230 | 20 | differs: treatment, orientation | True | True |
| 53 | 53-231 | 53-231 | 14 | differs: treatment, orientation | True | True |
| 53 | 53-232 | 53-232 | 22 | differs: treatment, orientation | True | True |
| 53 | 53-233 | 53-233 | 21 | differs: treatment, orientation | True | True |
| 53 | 53-234 | 53-234 | 8 | differs: treatment, orientation | True | True |
| 53 | 53-235 | 53-235 | 11 | differs: treatment, orientation | True | True |
| 53 | 53-236 | 53-236 | 10 | differs: treatment, orientation | False | False |
| 53 | 53-241 | 53-241 | 11 | differs: treatment, orientation | True | True |
| 53 | 53-242 | 53-242 | 6 | differs: irradiated, treatment, orientation | False | False |
| 53 | 53-243 | 53-243 | 8 | differs: treatment, orientation | False | False |
| 53 | 53-244 | 53-244 | 8 | differs: treatment, orientation | True | True |
| 53 | 53-245 | 53-245 | 6 | differs: irradiated, treatment, orientation | False | False |
| 60 | 60-280 | 60-280 | 30 | differs: treatment | True | True |
| 60 | 60-281 | 60-281 | 27 | differs: treatment | True | True |
| 107 | 107-282 |  | 26 | reference only in 2025.30 (refs 107-109) | True |  |
| 107 | 107-283 |  | 19 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-286 |  | 15 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-287 |  | 13 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-288 |  | 10 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-289 |  | 12 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-290 |  | 15 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-291 |  | 14 | reference only in 2025.30 (refs 107-109) | False |  |
| 109 | 109-292 |  | 11 | reference only in 2025.30 (refs 107-109) | True |  |
| 109 | 109-293 |  | 13 | reference only in 2025.30 (refs 107-109) | True |  |
