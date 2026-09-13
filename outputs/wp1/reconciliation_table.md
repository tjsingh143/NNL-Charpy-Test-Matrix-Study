# WP1 reconciliation table

Dataset: Materials Cloud 2025.30, record q4x6v-dyt25 (DOI 10.24435/materialscloud:p6-5y, issued 2025-02-26).

Each record is counted once, at the first step that applies (steps run in the order shown). `exclusion_reasons_all_applicable.csv` counts every criterion that applies to each record, regardless of order.

| step | criterion | basis | records_removed | records_remaining |
| --- | --- | --- | --- | --- |
| Start | Records in the 'Charpy Data' sheet |  |  | 4961 |
| E1 | Out of scope: austenitic stainless steel (SS316 family) | brief section 4; D-014 | 713 | 4248 |
| E2 | Out of scope: ferritic steel outside the brief's named RPV-steel family (15Cr2MoV-A) | brief section 4; CP1 decision 4; D-012 | 38 | 4210 |
| E3 | Not a standard Charpy impact test: striking velocity outside ASTM E23 range (3-6 m/s) | ASTM E23-82 §4.1.6; D-015 | 47 | 4163 |
| E4 | Missing essential measurement: test temperature or absorbed energy | D-016 | 0 | 4163 |
| E5 | Missing essential measurement: specimen dimensions (length, width or thickness) | D-016 | 55 | 4108 |
| E6 | Physically impossible value | D-017 | 0 | 4108 |
| E7 | Exact duplicate of an earlier record (all original fields identical) | D-018 | 0 | 4108 |
| E8 | Duplicate curve: same tests already present from another figure or publication | D-019 | 910 | 3198 |
| End | Records retained after WP1 |  | 1763 | 3198 |

## Records by step and material family

| exclusion_step | 15Cr2MoV-A | 20MnMoNi55 | A302B | A508 | A533B | A533B weld metal | SS316 (austenitic stainless) | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 0 | 0 | 0 | 0 | 0 | 0 | 713 | 713 |
| E2 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | 38 |
| E3 | 0 | 0 | 0 | 47 | 0 | 0 | 0 | 47 |
| E5 | 0 | 0 | 0 | 55 | 0 | 0 | 0 | 55 |
| E8 | 0 | 93 | 0 | 542 | 275 | 0 | 0 | 910 |
| retained | 0 | 178 | 38 | 1707 | 1191 | 84 | 0 | 3198 |
| total | 38 | 271 | 38 | 2351 | 1466 | 84 | 713 | 4961 |
