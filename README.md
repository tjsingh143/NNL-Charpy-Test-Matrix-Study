# Charpy Transition Temperature Uncertainty and Test Matrix Study

An analysis of published Charpy V-notch test data for reactor pressure vessel (RPV) steels. No Charpy tests were performed for
this project; all measurements come from the published dataset credited below.

## Research question

A reactor pressure vessel surveillance capsule holds a small, fixed volume of irradiated material. It can be spent on a few
full-size Charpy specimens or on many miniature ones. **Which choice gives a better-determined ductile-to-brittle transition
temperature once both curve-fitting uncertainty and sub-size-to-full-size correction uncertainty are counted?**
Full requirements: `PROJECT_BRIEF.md`.

This is a test-programme *design* question. It is not an attempt to predict full-size properties from sub-size specimens.

## Status

| Work package | State |
|---|---|
| WP0 Acquisition and data dictionary | done (CP1 approved; regenerated for the 2025.30 primary release) |
| WP1 Cleaning and normalization | done (CP1 approved; regenerated with the canonical duplicate hierarchy) |
| WP2 Curve grouping and inclusion criteria | in progress |
| WP3–WP7 | not started |

Progress and open issues: `PROGRESS.md`. Every judgement call: `DECISIONS.md`.

A plain-language summary of the findings will be added when the analysis is complete.

## Data attribution (required)

Lee, I., Merickel, J. W., Kasala Sreenivasulu, Y., Xu, F., Tang, Y., Rittenhouse, J. E., Vakanski, A., & Song, R.
*Dataset of Charpy V-notch impact test records of nuclear structural materials.* Materials Cloud Archive 2025.30, record q4x6v-dyt25,
DOI [10.24435/materialscloud:p6-5y](https://doi.org/10.24435/materialscloud:p6-5y) (2025). License: CC BY 4.0. **Primary dataset.**

The earlier release, Materials Cloud Archive 2024.206, record eny5v-www93, DOI
[10.24435/materialscloud:gh-za](https://doi.org/10.24435/materialscloud:gh-za) (2024), CC BY 4.0, is used as the version-sensitivity dataset.

Descriptor paper: Lee, I. et al. (2025). Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy
V-Notch Impact Testing. *Scientific Data* 12, 543. [doi:10.1038/s41597-025-04823-1](https://doi.org/10.1038/s41597-025-04823-1)

Which release is primary, and why, is decision D-001 (approved at CP1); see also `data/README.md`.

## Reproduce

```bash
./run_all.sh
```

Creates `.venv/` with the pinned packages if it does not exist, verifies the raw-data checksums, and regenerates everything in
`outputs/` and `data/processed/` from `data/raw/`.

## Repository layout

| Path | Contents |
|---|---|
| `PROJECT_BRIEF.md` | Requirements (with approved amendments listed at the top) |
| `DECISIONS.md` | Every judgement call, with alternatives and consequences |
| `PROGRESS.md` | Last checkpoint, decisions in force, next permitted work, open issues |
| `CLAUDE.md` | Persistent working rules for AI-assisted sessions on this repository |
| `data/` | Vendored raw data, license, checksums, processed data (see `data/README.md`) |
| `src/common.py` | Paths, checksum verification, spreadsheet loader |
| `src/curated_metadata.py` | All hand-curated inputs: column meanings, name maps, reference-level evidence |
| `src/wp0_data_dictionary.py` | WP0: checksums, workbook audit, data dictionary, version comparison |
| `src/wp1_clean.py` | WP1: cleaning, flags, exclusions, duplicate detection, reconciliation |
| `outputs/wp0/` | Data dictionary and WP0 reports |
| `outputs/wp1/` | Reconciliation table and WP1 reports (primary dataset, 2025.30) |
| `outputs/wp1_sensitivity_eny5v-www93/` | The same WP1 reports for the version-sensitivity dataset (2024.206) |
