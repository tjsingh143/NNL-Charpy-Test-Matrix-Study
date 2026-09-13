# Data directory: provenance, attribution and license

This project is an analysis of published test data. No Charpy tests were performed for it.

## Attribution (required by the CC BY 4.0 license)

**Dataset.** Lee, I., Merickel, J. W., Kasala Sreenivasulu, Y., Xu, F., Tang, Y., Rittenhouse, J. E., Vakanski, A., & Song, R.
*Dataset of Charpy V-notch impact test records of nuclear structural materials.* Materials Cloud Archive.
- **Primary dataset:** record q4x6v-dyt25, Materials Cloud ID 2025.30,
  DOI [10.24435/materialscloud:p6-5y](https://doi.org/10.24435/materialscloud:p6-5y), issued 2025-02-26.
  This is the release described and cited by the descriptor paper.
- **Version-sensitivity dataset:** record eny5v-www93, Materials Cloud ID 2024.206,
  DOI [10.24435/materialscloud:gh-za](https://doi.org/10.24435/materialscloud:gh-za), issued 2024-12-19 (the release named in the
  original PROJECT_BRIEF.md). The choice was approved at checkpoint CP1: decision D-001 in `DECISIONS.md`.

**Descriptor paper.** Lee, I., Merickel, J. W., Sreenivasulu, Y. K., Xu, F., Tang, Y., Rittenhouse, J. E., Vakanski, A., & Song, R. (2025).
Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy V-Notch Impact Testing.
*Scientific Data*, 12, 543. [doi:10.1038/s41597-025-04823-1](https://doi.org/10.1038/s41597-025-04823-1)

The dataset compiles results digitized or transcribed from 106 (first release) or 109 (later release) earlier publications, listed in the
`References` sheet of each workbook. Those original authors produced the measurements.

## License

Both dataset releases are licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0), which permits
redistribution and adaptation with attribution. The full legal text is in `LICENSE-CC-BY-4.0.txt`
(from https://creativecommons.org/licenses/by/4.0/legalcode.txt).

Notes: the descriptor *article* is published under CC BY-NC-ND 4.0 and is not redistributed here. The authors' GitHub copy of the
workbook is under an MIT license; this project uses the Materials Cloud copies instead.

**Changes.** The files in `raw/` are unmodified (moved into one folder per release after CP1; checksums unchanged). Files in
`processed/` are derived by `src/wp1_clean.py`: text labels are harmonized, descriptive fields and flags are added, and records are
marked retained or excluded with a reason. No measurement value is altered. Every change is logged in
`outputs/wp1*/value_changes_log.csv` and justified in `DECISIONS.md`.

## Files

| Path | What it is |
|---|---|
| `raw/release_2025.30_q4x6v-dyt25/Charpy_Impact_Test_Dataset.xlsx` | Primary dataset workbook |
| `raw/release_2025.30_q4x6v-dyt25/files_description.md` | File description published with that record |
| `raw/release_2025.30_q4x6v-dyt25/materialscloud_record_q4x6v-dyt25.json` | Snapshot of the archive record metadata (its view/download counters change online) |
| `raw/release_2024.206_eny5v-www93/` | The same three files for the version-sensitivity dataset |
| `LICENSE-CC-BY-4.0.txt` | License text |
| `CHECKSUMS.sha256` | SHA-256 of every file above |
| `FROZEN_COHORTS_CP2.csv` | Curve and record counts and a SHA-256 membership fingerprint for each WP2 cohort of both releases, frozen at checkpoint CP2; `src/wp2_curves.py` stops if regenerated cohorts differ (DECISIONS.md D-039). Not data; not generated |
| `processed/primary/` | WP1 output (`charpy_records_with_status.csv`, `charpy_clean.csv`) and WP2 output (`charpy_records_with_curves.csv`: curve, population and cohort of every record) for the primary dataset (generated) |
| `processed/sensitivity_eny5v-www93/` | The same files for the version-sensitivity dataset (generated) |

## Acquisition

Downloaded on 2026-09-12 (UTC) from `https://archive.materialscloud.org/records/<record>/files/<file>` and the archive API.
Each workbook's MD5 matched the value published in its record (eny5v-www93: a7e2f05e92baa298c8043569d8ab8b26;
q4x6v-dyt25: d4002dd0bfc7d029d254851b985bd05b). Every pipeline run re-verifies SHA-256 and MD5
(`outputs/wp0/checksum_verification.md`). To check by hand from this directory: `shasum -a 256 -c CHECKSUMS.sha256`.
