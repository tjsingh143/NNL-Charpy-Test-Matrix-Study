# DECISIONS.md — judgement-call log

One entry per decision that could reasonably have gone another way (PROJECT_BRIEF.md §1.1 and §6.4).
Each entry states what was decided, the alternatives, why, and what would change under the alternative.
Where a number is quoted, the file that regenerates it is named.

**Status legend:** `DECIDED` = in force. `APPROVED (CP1)` / `APPROVED (CP2)` = decided or approved by the author at that checkpoint
(the entry keeps earlier reasoning as history). `APPROVED (CP2, with the WP2 state)` = in force as part of the completed WP2 state the
author approved at CP2, without an entry-specific instruction. `OPEN` = not yet decided. After CP2 no entry is provisional.

**CP2 approval record (author, 2026-09-13).** The author reviewed CP2 and approved WP2; each item is recorded in full in the entry named.
1. Additively manufactured SA508 is a secondary group outside the primary conventional-RPV population (D-034).
2. Records whose irradiation status cannot be resolved from adequate source evidence are excluded from the primary analysis; the state is never guessed (D-035).
3. Reconstituted specimens are kept as their own curves and not combined with conventional specimens without a later, approved analysis (D-033).
4. D-038 is the primary pre-fit screening rule: passing it means only that a curve appears sufficiently sampled to attempt a fit. The
   looser, primary and stricter cohorts are frozen (D-039). Clarifications: 4A the WP2 upper quantity is a screening upper reference, not
   the upper-shelf energy; 4B the 0.12–0.88 band is a project-defined, model-based convention; 4C the stricter rule's specimen counts are
   historical ASTM E185 surveillance guidance used as a conservative comparison (D-037, D-038).
5. WP1 corrections surfaced in WP2: ref 1 source-contradicted labels leave the primary analysis (D-031); ref 21's HSST Plate 02 series is a
   republication of ref 1, under safeguards for offset-based duplicates (D-019); ref 53 curve 237 is a mislabelled duplicate of curve 241 (D-019, D-029).
6. WP2 is merged into `main` after these are implemented and verified (D-030).

Put to the author while CP2 was being finalized, and decided: the two irradiated-labelled records of ref 1 series 6 (curve 1-6.3) carry
the same source-contradicted label and join the exclusion of item 5 (D-031); the approximately 0.10–0.85 band alternative is preserved
with its literature source still to be documented (D-037).

**Sources cited below**
- [descriptor] Lee I., Merickel J.W., Sreenivasulu Y.K., Xu F., Tang Y., Rittenhouse J.E., Vakanski A., Song R. (2025).
  *Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy V-Notch Impact Testing.* Sci. Data 12:543.
  doi:10.1038/s41597-025-04823-1
- [record-A] Materials Cloud Archive 2024.206, record eny5v-www93, doi:10.24435/materialscloud:gh-za (issued 2024-12-19); version-sensitivity dataset
- [record-B] Materials Cloud Archive 2025.30, record q4x6v-dyt25, doi:10.24435/materialscloud:p6-5y (issued 2025-02-26); primary dataset
- [E23-82] ASTM E23-82, *Standard Methods for Notched Bar Impact Testing of Metallic Materials* (public copy via law.resource.org)
- [ISO148-1] ISO 148-1:2016, *Metallic materials — Charpy pendulum impact test — Part 1: Test method* (§3.2 definitions, from the published sample pages)
- [E900] ASTM E900, *Standard Guide for Predicting Radiation-Induced Transition Temperature Shift in Reactor Vessel Materials* (fluence defined for E > 1 MeV)
- [A533] ASTM A533/A533M, *Pressure Vessel Plates, Alloy Steel, Quenched and Tempered, Manganese-Molybdenum and Manganese-Molybdenum-Nickel* (Types A–E; Classes 1–3 = strength levels)
- [A302] ASTM A302/A302M, *Pressure Vessel Plates, Alloy Steel, Manganese-Molybdenum and Manganese-Molybdenum-Nickel*
- [A508] ASTM A508/A508M, *Quenched and Tempered Vacuum-Treated Carbon and Alloy Steel Forgings for Pressure Vessels*
- [ASME-II] ASME BPVC Section II Part A: SA-specifications are adopted from, and identical with or similar to, the corresponding ASTM specifications
- [NP-1661] Server W.L. et al. (1981), EPRI NP-1661 abstract (OSTI 6609271): covers Charpy V-notch and precracked Charpy data, reconstituted specimens, shock-hardened surrogate
- [Lee2011] Lee K.-H. et al. (2011), Mater. Sci. Eng. A 529:156–163, abstract: Charpy impact tests to ASTM E23, fracture toughness to ASTM E1921
- [Drevon2017] Drevon D., Fursa S.R., Malcolm A.L. (2017). *Intercoder reliability and validity of WebPlotDigitizer in extracting graphed data.* Behav. Modif. 41(2):323–339
- [NP-1661] Server W.L., Wullaert R.A., Odette G.R., Oldfield W. (1981). *Analysis of Radiation Embrittlement Reference Toughness Curves*, EPRI NP-1661, full report (OSTI 6609271): Figs 2-5, 3-14, 3-15, 3-17; Table 3-1
- [BLG-1016] Lucon E. (2005). *The Use of Single-Specimen Techniques for Measuring Upper Shelf Toughness Properties under Impact Loading Rates*, SCK•CEN open report BLG-1016, Tables 1–4 (OSTI ETDEWeb 20902511)
- [Lee2014] Lee K.-H., Jhung M.J., Kim M.-C., Lee B.-S. (2014). Nucl. Eng. Technol. 46(3):413–422, full text, §2 (ref 13)
- [Kim2012] Kim B.J., Mitsui H., Kasada R., Kimura A. (2012). J. Nucl. Sci. Technol. 49(6):618–631, abstract (ref 53)
- [E185-82] ASTM E185-82, *Standard Practice for Conducting Surveillance Tests for Light-Water Cooled Nuclear Power Reactor Vessels*, copy incorporated by reference in 10 CFR 50 (Internet Archive item gov.law.astm.e185.1982): §4.16–4.18, §6.3, §9.2.2
- [Jendrich2003] Jendrich U., Tricot N. (2003). *Neutron fluence at the reactor pressure vessel wall – a comparison of French and German procedures and strategies in PWRs*, IRSN report DES/546 (EUROSAFE 2002), §1.3–1.4 (OSTI ETDEWeb 20375315)

---

## D-001 — Which release of the dataset is the project dataset
**Status:** APPROVED (CP1) — amends PROJECT_BRIEF.md §3 (amendment A1 recorded in the brief)

**CP1 decision (author, 2026-09-12).** The primary dataset is [record-B] (Materials Cloud 2025.30; 4,961 records, 56 columns,
109 publications), the release described and cited by the descriptor paper. [record-A] (Materials Cloud 2024.206; 4,775 records),
which the original brief named, is the version-sensitivity dataset: WP1 and later stages are run on it too, to test whether the
choice of release changes important conclusions. Corrections in record-B are not assumed correct because they are newer: its
irradiation relabels and other suspicious changes remain data-quality flags (D-020, D-021). Implemented by `PRIMARY_DATASET` and
`SENSITIVITY_DATASET` in `src/common.py`; the raw files moved to `data/raw/release_2025.30_q4x6v-dyt25/` and
`data/raw/release_2024.206_eny5v-www93/` (checksums unchanged).

**Effect of the switch (regenerated).** WP1 retains 3,198 records from record-B and 3,050 from record-A (`outputs/wp1*/reconciliation_table.md`).
The difference is exactly refs 107 and 109 (148 records); ref 108 (15Cr2MoV-A, 38 records) leaves at E2. Both releases now give the same
duplicate removals because unresolved labels no longer block duplicate matching (D-019, D-021). In WP2 the two releases yield the same curves
for refs 1–106; the primary cohorts differ only by the 9 passing curves of refs 107 and 109 (`outputs/wp2/version_sensitivity_comparison.md`).

**History — pre-CP1 provisional decision (superseded).** Use record-A, as the brief then specified, and run record-B for comparison.

**Context (pre-CP1).** Two releases of the same dataset exist on Materials Cloud, under different parent records:
[record-A] (named in PROJECT_BRIEF.md; 4,775 records, 55 columns, 106 references) and [record-B] (4,961 records,
56 columns, 109 references, an extra `Specimen Type` column and a `Notes` curation sheet). The descriptor paper describes
and cites record-B, and the authors' GitHub repository holds a byte-identical copy of record-B's workbook (git blob SHA
533d056d…, checked at acquisition on 2026-09-12). The brief's own numbers mix the two (4,775 records from A; 109 publications from B).
Row-level comparison: `outputs/wp0/dataset_version_comparison.md`.

**Pre-CP1 decision (superseded).** Use record-A, as the brief specifies. Vendor record-B beside it for comparison only, and run the WP1 pipeline
on both so the consequence of switching is known. Ask the author at CP1.

**Alternatives.** (1) Switch to record-B now (what the paper describes). (2) Hybrid: record-A plus corrections copied from B.

**Why.** The brief is the authoritative requirements document and names record-A; switching silently would change a requirement.
A hybrid would create a third, unpublished version. Evidence gathered for the CP1 discussion:
- For shared references, every measurement column (temperature, energy, dimensions, USE, curve ID) is identical in A and B.
  B changes only metadata (manufacturer, treatment, microstructure, orientation, irradiation fields) and 16 DBTT values.
- B adds references 107–109 (186 records), including a sub-size correlation study (107) relevant to WP5 and a WWER-440 steel (108) outside the brief's named family.
- Some of B's metadata corrections look wrong: four curves B relabels as irradiated (refs 8, 9, 9, 13; two with no fluence)
  match unirradiated curves from other publications point for point (`outputs/wp1*/duplicate_curve_removals.csv`; see D-021).

**Pre-CP1 estimate of the switch (under the CP1 duplicate rule).** WP1 on record-B retained 3,409 records instead of 3,208,
added KLST-type miniature specimens and 15Cr2MoV-A (then pending scope), and imported B's irradiation relabels. These figures are
superseded by the regenerated numbers above.

---

## D-002 — Computational environment
**Status:** DECIDED

**Decision.** macOS system CPython 3.9.6 in a project-local virtual environment (`.venv/`), with pinned numpy 2.0.2,
pandas 2.2.3, openpyxl 3.1.5, and (from WP2, for figures) matplotlib 3.9.4 (`requirements.txt`). Figures are written with the Agg
backend and without a software-version tag, so they regenerate byte-identically.
**Alternatives.** Install a newer Python with Homebrew; use conda.
**Why.** Uses what is already on the machine without modifying the system; pinned versions make results reproducible.
Python 3.9 is past end-of-life, which matters for security updates, not for these calculations.
**If the alternative were chosen.** No expected numerical difference; a newer interpreter would require re-pinning packages.

## D-003 — How the spreadsheet is read
**Status:** DECIDED

**Decision.** Read cells with openpyxl (`data_only=True`) and assign types explicitly (`src/common.py::load_charpy_data`).
Do not use `pandas.read_excel`.
**Alternatives.** `pandas.read_excel` (the usual choice).
**Why.** Demonstrated failure: pandas converts whole-number floats to Python integers; fluence values such as 3×10¹⁹ exceed
the 64-bit integer range, so the column stays generic and pandas leaves its 4,336 empty cells as the text `''` instead of
missing values (`outputs/wp0/workbook_structure.md`, "Reader cross-check"). The problem is silent. openpyxl normal and
read-only modes agree on every cell.
**If the alternative were chosen.** Fluence would be text for most rows; any numeric filter or binning in WP2 would silently fail or error.

## D-004 — Excel formula cells
**Status:** DECIDED

**Decision.** Use the values stored by Excel for the 439 formula cells (all in the fluence column), after verifying that every
formula is a constant of the form `=(a*10^b)` whose stored value equals its evaluation (0 mismatches; `workbook_structure.md`).
**Alternatives.** Re-evaluate formulas ourselves; treat formula cells as suspect and exclude.
**Why.** The formulas are a data-entry convenience for scientific notation, not calculations; verification shows the stored values are exact.
**If the alternative were chosen.** Identical values (re-evaluation); or loss of 439 irradiated records (exclusion), for no reason.

## D-005 — Vendoring and checksums
**Status:** DECIDED

**Decision.** Store both workbooks, their `files_description.md` and archive record JSON snapshots in `data/raw/` (one folder per release,
named by Materials Cloud ID and record since CP1: `release_2025.30_q4x6v-dyt25/`, `release_2024.206_eny5v-www93/`), the CC BY 4.0
legal text in `data/`, and SHA-256 values in `data/CHECKSUMS.sha256`. Every run verifies SHA-256, and verifies each workbook's
MD5 against the value published in its archive record (`outputs/wp0/checksum_verification.md`).
**Alternatives.** Download at run time; record MD5 only.
**Why.** Run-time downloads break reproducibility if the archive changes; SHA-256 is the stronger recorded fingerprint, while MD5 is
what the archive publishes, so both are checked. The JSON snapshots contain view/download counters that change online, so a fresh
download of the JSON would not match; the vendored snapshot is what is checksummed.
**If the alternative were chosen.** Results could change without notice if the archive record were edited.

## D-006 — Record identity
**Status:** DECIDED

**Decision.** Each record is identified by its spreadsheet row (`source_row`, e.g. 3) and `record_id` (`R0003`). All outputs carry these.
**Alternatives.** A new sequential index; a hash of record contents.
**Why.** Anyone can open the workbook at that row and see the original record.
**If the alternative were chosen.** Traceability back to the spreadsheet would need an extra lookup table.

## D-007 — Column names in the processed data
**Status:** DECIDED

**Decision.** snake_case names with units (`test_temp_c`, `energy_j`, `fluence_n_per_cm2`, `width_mm`); the verbatim original header is
kept in the data dictionary. "Irradiation Dose (n/cm^2)" is renamed `fluence_n_per_cm2`. The dataset's own USE, DBTT and curve
columns get a `_dataset` suffix (`use_j_dataset`, `dbtt_c_dataset`, `curve_id_dataset`). Mapping: `src/curated_metadata.py::COLUMNS`.
**Alternatives.** Keep original headers (with their trailing spaces and typos); name the fluence column "dose".
**Why.** Units in names prevent unit mistakes downstream. n/cm² is a fluence unit; in radiation-damage usage "dose" usually means
displacements per atom or absorbed energy, so keeping "dose" invites confusion. The `_dataset` suffix keeps the dataset's fitted values
visibly separate from the values this project will compute in WP3.
**If the alternative were chosen.** No numerical change; higher risk of confusing dataset-provided and project-computed quantities.

## D-008 — Meaning of `Width` and `Thickness`
**Status:** DECIDED

**Decision.** `width_mm` (W) = distance between the notched face and the opposite face (the direction the notch is cut and the crack grows);
`thickness_mm` (B) = dimension parallel to the notch. Ligament = W − notch depth.
**Alternatives.** The opposite assignment, which is what ISO 148 editions before 2016 and much older literature used ("height" and "width").
**Why.** This matches ISO 148-1:2016 §3.2.1–3.2.2 and the descriptor's normalization notation B(W−A)² [descriptor, ISO148-1]; the data agree:
every 2 mm notch is paired with W = 10 mm, and sub-size reductions (5, 6, 3.33 mm) appear in B at 55 mm length.
**If the alternative were chosen.** Ligament areas and the WP5 volume normalization would be computed on the wrong dimension for every
sub-size specimen with W ≠ B.

## D-009 — Missing values
**Status:** DECIDED

**Decision.** A blank cell means "not reported". Nothing is imputed or filled in from a standard (e.g. notch depth 2 mm is not assumed for full-size
specimens that omit it). Leading/trailing whitespace is trimmed from text (logged in `value_changes_log.csv`); the verbatim material label is kept.
**Alternatives.** Fill standard notch dimensions for 55×10×10 mm specimens; treat blank composition as zero.
**Why.** Brief §7 forbids imputed measurement data. A blank composition entry means not measured or not reported, not absent.
**If the alternative were chosen.** More records would look complete, but the completeness would be invented.

## D-010 — Unit harmonization
**Status:** DECIDED

**Decision.** No conversion applied. The descriptor states all values were already converted to one unit per column; WP1 verifies this
(`outputs/wp1/unit_checks.md`). Fluence stays in n/cm² (the unit of the dataset and of most RPV surveillance literature; ASTM E900 uses n/m²).
**Evidence (regenerated for the 2025.30 primary release).** No test temperature below −200 °C or above 377.6 °C for in-scope ferritic steels (no kelvin or °F pattern;
the −200 °C values are whole-number temperatures in the newly added refs 107 and 109); irradiation temperatures
carry conversion fingerprints (149 °C = 300 °F, 288 °C = 550 °F, 269.85 °C = 543.00 K); every retained dataset curve's highest energy lies within
0.92–1.45× its USE (an unconverted ft·lbf curve would sit near 0.74× or 1.36×); all fluences 6.2×10¹⁷–1.11×10²⁰ (n/m² would be 10⁴× larger);
no inch-like dimensions; composition sums 99.994–100.019 wt.%.
**Alternatives.** Convert fluence to n/m²; re-derive units from each source paper.
**Why.** Verification found no inconsistency; converting what is already consistent adds a step without benefit.
**Limitation.** The energy check detects a unit error *within* a curve; a source whose energies and USE were both left in ft·lbf would pass. Only the source papers can rule that out.
**If the alternative were chosen.** n/m²: values ×10⁴, no analytical change.

## D-011 — Neutron energy threshold of the fluence values
**Status:** DECIDED (documented as unknown)

**Decision.** Record that the energy threshold (E > 1 MeV, E > 0.1 MeV, …) is not stated anywhere in the dataset. Do not assume E > 1 MeV.
**Alternatives.** Assume E > 1 MeV, the ASTM E900 convention.
**Why.** Different thresholds can differ by a factor of about two for the same irradiation; assuming would be a silent judgement.
**If the alternative were chosen.** Fluence would look comparable across sources when it may not be. Consequence for WP2: fluence is compared only within one source (D-032, D-036), where the threshold is at least consistent.

## D-012 — Material name harmonization: what was merged and what was kept separate
**Status:** DECIDED; 15Cr2MoV-A scope APPROVED (CP1): out of scope

Mapping: `src/curated_metadata.py::MATERIAL_MAP`; applied counts: `outputs/wp1/value_changes_log.csv`. The verbatim label is kept in `material_raw`.

| Raw labels | Treated as | Confidence and basis |
|---|---|---|
| `A533B`, `A533B ` (trailing space), `SA533B` | A533 Type B, class not stated | Whitespace: certain. SA vs A: same specification [ASME-II]. |
| `A533B-1`, `SA533B-1` | A533 Type B Class 1 | Same as above. |
| class-not-stated vs Class 1 | **same family (A533B), class kept in `material_class_stated`** | Not merged at class level: Classes 1–3 are different strength levels [A533]. |
| `A533B - WM` | **separate family:** weld metal from an A533B weldment | A weld deposit is not A533B plate. |
| `A508`, `SA508` | A508, grade/class not stated | SA vs A: same specification. Grade (1A, 3, 4N…) is absent from the label; titles give it at reference level only (`ref_grade_title`). |
| `A302B` | A302 Grade B | Own family; A302B and A533B are different specifications. |
| `20MnMoNi55` | own family | German grade (DIN 1.6310); not merged with A508 or A533B even though related. |
| `15Cr2MoV-A` (record-B only) | own family, **out of scope (CP1 decision 4)** | Ferritic WWER-440 vessel steel, not in the brief's named family; excluded at step E2 (38 records, ref 108), preserved in `charpy_records_with_status.csv`. The 2025.30 release puts it in Material Group 'Nuclear Structural Material' with SS316. |
| `SS316`, `SS316L`, `SS316LN`, `SS316H` | one family for scope exclusion; variants kept in `material_std` | All austenitic (D-014). |

**Alternatives.** Merge A533B classes; merge SA508 grades into one material; merge 20MnMoNi55 with A508 Grade 3.
**Why.** Brief §5 WP1: merge only what is certainly the same. Specification prefixes and whitespace are certain; classes and grades are not.
**If the alternative were chosen.** Materials with different strength, chemistry and toughness would be pooled, adding real material differences to what WP2–WP4 would read as scatter.

## D-013 — Product form (plate, forging, weld) is derived, not recorded
**Status:** DECIDED

**Context.** The dataset has no product-form column. Brief WP2/WP5/Q3 need one.
**Decision.** `product_form` with `product_form_basis`, using the first available evidence in this order (`src/wp1_clean.py::derive_product_form`):
1. record-level labels: weld metal (material label), simulated HAZ (treatment code), HAZ (condition statement, except "Bulk Metal" base-metal records), weld region, additive manufacturing (manufacturer);
2. explicit product form in the citation title (ref 47 "20MnMoNi55 forging"; ref 31 additive manufacturing, covering its records that lack the label);
3. nominal form from the specification's scope: A533 and A302 are plate specifications [A533, A302]; A508 is a forging specification [A508] — basis recorded as "specification scope (nominal)";
4. otherwise "not determinable" (20MnMoNi55, a grade used for both plates and forgings).

Records whose citation title reports weld or HAZ material that the records do not identify (refs 5, 7, 18, 25, 34, 50, 60) carry
`flag_title_reports_weld_or_haz_not_identified_in_records`. Model alloys and lab melts (refs 3, 10, 16) and Grade 1A piping steel keep the nominal form, with the reason visible in `ref_material_note`.
**Alternatives.** Nominal form from the specification only; classify every reference manually from the full papers; leave product form blank.
**Why.** Record-level evidence is the most direct; the specification scope is a documented fact about what the specification covers; papers were not all available to read in full.
**Known weakness.** "Nominal" is not verified: e.g. ref 34's curves are labelled SA508 but the title says weld and HAZ, and lab-melted "SA508 Gr.4N" model alloys were not forged.
**If the alternative were chosen.** Specification-only: HAZ, weld and additively manufactured material would be labelled base plate/forging. Manual classification: more accurate, much slower, and still limited by what papers state.

## D-014 — Exclusion E1: austenitic stainless steels
**Status:** DECIDED
**Decision.** Exclude all SS316-family records (713). **Basis.** Brief §4 (out of scope). Physical reason, for the report: austenitic (face-centred cubic) steels
do not show the ferritic ductile-to-brittle transition that the transition-curve model describes.
**Alternatives.** None within the brief. **Effect.** Also removes every below-absolute-zero temperature, all missing temperatures and all exact duplicates in the raw file (see `exclusion_reasons_all_applicable.csv`).

## D-015 — Exclusion E3: tests at non-standard striking velocity
**Status:** DECIDED
**Decision.** Exclude records whose condition statement gives a striking velocity outside 3–6 m/s: ref 51 tests at 0.5 m/s (27) and 0.001 m/s (20). The 5 m/s series (48) is kept.
**Basis.** [E23-82] §4.1.6: the impact velocity "shall not be less than 3 nor more than 6 m/s". Loading rate shifts the transition (E23-82 Appendix X1.6), so slower tests are a different test.
**Alternatives.** Keep and tag them; let WP2 decide.
**Why.** A 0.001 m/s test is effectively a slow bend test; pooling it with impact tests is not defensible for any analysis in this project.
**If the alternative were chosen.** 47 more records, forming two extra curves that are not Charpy impact curves.

## D-016 — Exclusions E4/E5: missing essential measurements; what is not excluded
**Status:** DECIDED
**Decision.** Exclude records missing test temperature or absorbed energy (E4; none remain after E1) or any of length, width, thickness (E5; 55 records, refs 25 and 36).
Keep records with missing notch depth, angle or radius (flagged `flag_notch_dimensions_not_reported`).
**Why.** Every analysis in WP2–WP6 needs temperature, energy and specimen geometry. Notch details are not needed to identify a
55×10×10 mm specimen, so excluding them now would pre-empt WP2 and WP5 (where ligament-based normalization needs notch depth and the rule can be stated there).
**Alternatives.** Assume full-size for refs 25/36 (they are probably full-size, but that is an assumption); exclude records lacking notch depth now.
**If the alternative were chosen.** Assuming geometry: +55 records built on a guess. Excluding missing notch depth: 1,243 more retained records lost before any need is shown.

## D-017 — Exclusion E6: physically impossible values; review flags for implausible ones
**Status:** DECIDED
**Decision.** Exclude only values that are impossible: absorbed energy < 0 J; temperature below absolute zero (−273.15 °C); length, width or thickness ≤ 0;
notch depth ≥ width (no ligament); negative fluence. Flag, but keep, values that are merely implausible:
energy exactly 0 J; energy > 1.5 × the curve's dataset USE; energy per ligament area > 1000 J/cm²; test temperature outside −200 to 400 °C.
**Result.** After E1–E5 no record is impossible. Flags on retained records (2025.30 primary): one zero-energy record (ref 32; the ref 43 zero left at E8 with its series); nothing else (`flags_summary.md`).
Refs 107 and 109 (2025.30 only) report tests at exactly −200 °C, on the boundary of the review window and therefore not flagged; they are
whole-number (tabulated or rounded) temperatures 4 °C below the liquid-nitrogen boiling point, each with 1.0 J absorbed energy (0.6 % of its curve's dataset USE for the full-size curve of ref 107; 11–13 % for two KLST curves of ref 109).
**Why these lines.** Impossible values need no threshold choice. For "energy far above any plausible upper shelf" (brief WP1) there is no universal
maximum, because capacity depends on the machine and upper-shelf energy on the material and specimen size; so the two screens compare energy with the
record's own curve (1.5× USE) and with a size-normalized bound roughly twice the highest value among retained records (537 J/cm², a full-size SA508 specimen).
The −200 °C floor sits just below liquid-nitrogen tests (−196 °C); 400 °C is above the upper shelf of the most embrittled curves in the data.
Zero energy is kept because a lower-shelf point digitized on a graph's axis reads 0 J within digitization error.
**Alternatives.** Exclude zero-energy points; use a fixed energy cap (e.g. 300 J machine capacity); percentile-based outlier removal.
**If the alternative were chosen.** Excluding zeros: −2 records. A 300 J cap would wrongly remove genuine 300–430 J upper-shelf results of tough SA508 steels. Percentile trimming would remove real extreme curves.

## D-018 — Exclusion E7: exact duplicate records
**Status:** DECIDED
**Decision.** Among records still retained, exclude a record identical in every original field to an earlier row; keep the first.
**Result.** 0 in-scope; all 13 exact duplicates in the raw file are SS316 and leave at E1 (`exclusion_reasons_all_applicable.csv`).
**Alternatives.** Treat exact duplicates as genuine replicate specimens.
**Why.** For digitized values carrying 12+ decimals, identical rows are copy errors, not replicates. For whole-number tabular values, replicates are possible; none occur in scope, so the question does not arise.

## D-019 — Exclusion E8: the same tests reported more than once
**Status:** APPROVED (CP1) — deduplication and the hierarchy's criteria. APPROVED (CP2) — their operationalization, the matching change for
unresolved labels and the two detection additions made after CP1 (ref 53 curve 237 = curve 241; ref 21's HSST Plate 02 copy of ref 1), with
the safeguards for offset-based duplicates below

**CP1 decision (author).** Deduplicate republished tests for the primary analysis, because counting a republication as a new
experiment would overstate confidence. "Keep the copy with most points" is not acceptable as the sole rule (extra points can be
contamination, e.g. ref 19 curve 90 below). Establish a transparent hierarchy before any fitting; never average separate digitizations;
keep an audit mapping every removed copy to its kept copy; carry at least one reasonable alternative rule forward as a sensitivity case;
do not tune the rule on downstream results.

**CP2 decision (author, 2026-09-13).** Approved: (i) ref 53 curve 237 is a mislabelled duplicate of weld-metal curve 241, on the
point-for-point evidence (11 of 11 points identical), and leaves the primary independent-data population; the raw curve, its original label,
the canonical relationship (kept copy: curve 241) and the reason stay in the audit trail (D-029). (ii) Ref 21's HSST Plate 02 series is a
republication/redigitization of ref 1, and ref 1, the original source, is the canonical copy. (iii) Safeguards: the constant-offset detector
must not become a generic method that shifts arbitrary curves until unrelated curves happen to match. An offset-based duplicate
classification requires all of: 1. compatible source, material and condition provenance; 2. evidence that the publications represent the
same underlying experiment or specimen population; 3. strong point-pattern overlap under ONE approximately constant axis offset; 4. a
predeclared quantitative overlap criterion; 5. an auditable retained-copy / excluded-copy mapping. An offset is never selected on downstream
fit quality; two digitizations are never averaged into a smoother curve; the alternative duplicate-selection cohort is preserved.

**Canonical-source hierarchy (implemented in `src/wp1_clean.py::KEEP_RULES`, chosen before any fitting).** Among copies linked as
duplicates, the copy kept is the first by:
- (a) *directly tabulated values over graph digitizations.* A copy counts as tabulated when ≥ 90 % of its records have temperature and
  energy at table resolution (≤ 1 decimal place in °C and J, or a whole number of °F / ft·lbf before conversion). **No copy in any duplicate
  group qualifies** (every copy is a digitization; shares in `duplicate_curve_removals.csv`), so (a) never decides here.
- (b) *original experimental source over a later republication,* operationalized as the earlier publication year (the first report of the tests).
- (c) *clearer provenance, fewer unresolved labeling problems:* the number of distinct unresolved problems on the copy (irradiation status
  unresolved between releases; specimen type unresolved; title reports weld/HAZ not identified in records; material label contradicts
  composition; dataset curve ID mixes conditions; condition label contradicted by the source). Problems resolved by a source check do not count.
- (d) *deterministic tie-breaker independent of the data values:* lower reference ID, then earlier spreadsheet row.

**Duplicate matching when irradiation labels are disputed (bug exposed by the switch to record-B).** Candidates were required to share
irradiation status and fluence. Record-B relabels four republished unirradiated series as irradiated, which hid them from matching
and would have counted the same tests twice (once as irradiated). A label that is unresolved between the releases (D-021) can no longer rule a
match out; settled labels (both releases agree, or source-checked) are still compared. The four cross-label duplicates (ref 8 curve 33,
ref 9 curves 34 and 36, ref 13 curve 59; 53 records) are removed in favour of their unirradiated copies; the audit records both labels.

**Two further detection gaps closed after CP1 (found while accounting for duplicates in WP2; both change which records are retained).**
- *Contradicted material labels.* Candidates had to share a material family, so ref 53 curve 237 (labelled base metal, weld-metal
  composition, D-029) was never compared with weld-metal curve 241, although all 11 points are identical. A material label contradicted
  by the record's own composition can no longer rule a match out (same principle as unresolved irradiation labels).
- *Constant axis offset between digitizations.* Ref 1 curve 6 (95 original + 10 reconstituted HSST Plate 02 specimens) and ref 21 curve 99
  (104 + 12) matched only about half their points within 3 °C / 2 %, below the 70 % rule. Independent tests cannot line up point for point
  under one constant shift; two digitizations of the same plotted data with differently calibrated axes do. How the CP2 safeguards are met
  (`src/wp1_clean.py::offset_aligned_pairs`; audit `outputs/wp1/duplicate_offset_evidence.csv`):
  1. *Compatible provenance:* the two copies must agree on material family (a stated class may not contradict the other copy), specimen
     dimensions and notch depth, settled irradiation status and fluence, treatment, and test-condition statement. Unlike the plain test, no
     disputed label is waived. Original specimens are compared only with original ones, reconstituted only with reconstituted.
  2. *Same experiment:* the test runs only on dataset-series pairs listed in `src/curated_metadata.py::OFFSET_DUPLICATE_PROVENANCE`, each
     with its evidence and what was not verified. Refs 1 and 21: W. L. Server co-authored both reports (1981, 1982); ref 1 series 6 is HSST
     Plate 02, original plus reconstituted specimens [NP-1661]; ref 21 is a report on preparing reconstituted Charpy V-notch specimens whose
     SA533B series has the same structure (95 + 10 against 104 + 12 specimens, same geometry, unirradiated). Not verified: ref 21's full text
     was not read; that its series is HSST Plate 02 is inferred from this evidence and from the point pattern.
  3. *One constant offset:* a single transform (temperature shift −6 to +6 °C in 0.5 °C steps, energy scale 0.98–1.02) is shared by every
     compatible series pair of the two publications. It is chosen by the largest total number of one-to-one matched points (ties: smallest
     shift, then scale nearest 1), never by any fit. Result: −3.0 °C and ×1.00 for both the original and the reconstituted series. (At the
     CP2 presentation each pair was searched on its own; the reconstituted pair then reported ×1.01 purely through a tie-break, with the same 8 matches.)
  4. *Predeclared criterion:* after the transform, points match within 1 °C and 1 % of the larger maximum energy; duplicate if ≥ 5 points
     and ≥ 70 % of the smaller copy match. Result: 73 of 95 original and 8 of 10 reconstituted points; without the shift, 8 and 1 at the
     same tolerance (51 and 5 at the plain 3 °C / 2 %); chance baseline (the same copy shifted by ±20 and ±30 °C, plain tolerance) 5–15 and 0.
     History, stated plainly: the 70 % fraction is the plain test's CP1 value, but the 1 °C / 1 % tolerances, the ±6 °C and 0.98–1.02
     search ranges and the 5-point minimum were introduced in WP2 (commit `10d4e89`), when the ref 1 / ref 21 pair had already been noticed
     and before any fit existed. They are frozen from CP2 and apply unchanged to any future candidate.
  5. *Audit:* `duplicate_curve_removals.csv` maps each removed copy to its kept copy (`linked_by` = constant axis offset; 29 of 104 and 4 of
     12 points of the removed copies have no counterpart in ref 1); `duplicate_offset_evidence.csv` records the provenance evidence,
     label compatibility, the shared transform, matches with and without it, and the chance baseline.
  A review-only screen runs the same search on every other candidate pair so that a future pair meeting the criterion without documented
  provenance is listed for a person to examine, never removed. It finds none.

**Result (regenerated; identical for both releases).** 69 series, 910 records removed at E8: 67 series (794 records) by plain point matching,
2 (116 records, ref 21 curve 99) by the constant-offset test. Deciding criterion: (b) 63 series (852 records); (c) 2 series (26 records:
ref 9 curve 34 vs ref 37 curve 161 of the same year; ref 53 curve 237 vs 241); (d) 4 series (32 records: three figure copies within ref 53,
refs 42/45 of the same year). Audit: `outputs/wp1/duplicate_curve_removals.csv` (kept copy, how the copies were linked, matched points,
points in the removed copy with no match in the kept copy, deciding criterion, labeling problems and irradiation labels of both copies).
Consequences worth knowing: ref 19 curve 90 (whose two extra points belong to another alloy's upper shelf) is replaced by the 2007
original (ref 17); ref 43 (2021) curves 191 and 192 are replaced by the 2008 originals in ref 44, losing 11 and 14 points of ref 43 that
appear in no other copy (possibly additional tests, possibly contamination: curve 191's extra points lie above the 181 J upper shelf
[BLG-1016] reports for that steel); ref 21's HSST Plate 02 copy (1982) gives way to ref 1's (1981), losing 29 of its 104 original points
that have no counterpart. Parameter sensitivity of the plain test (36 settings): 821–986 records removed, median 904 (`duplicate_sensitivity.csv`).

**Alternative rule carried forward (sensitivity).** "Most records, then fewer labeling problems, then earliest publication, lower
reference ID, earlier row" — the CP1 completeness rule, made label-aware so it never keeps a disputed copy over an identical clean one.
It keeps 9 different series (refs 19, 21 ×2, 26 ×2, 43 ×2, 52 ×2 instead of 17, 1 ×2, 14 ×2, 44 ×2, 55 ×2), removes 868 records and retains
3,240 (chosen: 3,198). Record-level column `status_under_alt_keep_rule`; audit `duplicate_curve_removals_alt_keep_rule.csv`;
all rules compared in `duplicate_keep_rule_comparison.csv`; WP2 cohort `alt_keep_rule` (D-039).

**History — pre-CP1 method and evidence (detection unchanged; keep rule superseded).**

**Context.**

**Context.** Several research groups republished the same Charpy curves in conference and journal papers (e.g. the KAERI SA508 Gr.4N series,
refs 10, 13, 14, 17, 19, 20, 26, 27, 28, 33, 37, 38; refs 52 and 55; 42 and 45; 43 and 44; 46 and 48; 22, 23 and 40), and the dataset digitized each figure separately.
None of the 752 removed points is bit-identical to its kept counterpart: matched points differ by a median of 0.26 °C and 0.4 % in energy (95th percentiles 1.15 °C and 9 %; the large relative differences are small lower-shelf energies), consistent with separate digitizations of the same data points. Counting them twice would double-count tests and understate scatter.

**Decision (method, `src/wp1_clean.py::find_duplicates`).**
- *Unit compared:* a dataset curve, split by reference, material, geometry, irradiation, fluence, treatment and condition statement.
- *Candidates:* two units with the same material family, same length/width/thickness, same irradiation status and fluence.
- *Point match:* one-to-one pairing with |ΔT| ≤ 3 °C and |ΔE| ≤ 2 % of the larger unit's maximum energy (a fraction of the plot's energy axis, because digitization error scales with the axis, not with the value; a fixed 1 J tolerance falsely matched sub-1 J miniature curves).
- *Duplicate:* ≥ 3 matched points and ≥ 70 % of the smaller unit matched. 50–70 % is flagged as partial overlap, not removed.
- *Which copy is kept (pre-CP1, superseded):* the unit with most records, then earliest publication, then lowest reference ID. Every removed unit matches its kept unit directly.

**Evidence the threshold is not arbitrary.** The distribution of matched fractions has an empty 0.6–0.7 bin separating chance overlaps (0.1–0.6) from re-publications (0.7–1.0)
(`outputs/wp1/wp1_summary.md`). Across 36 parameter combinations (ΔT 2/3/5 °C × ΔE 1/2/3 % × fraction 0.6/0.7/0.8/0.9) removals range from 694 to 975
records (median 783; regenerated after CP1): every setting with ΔT ≤ 3 °C removes 694–828, while ΔT = 5 °C removes 819–975 because the looser window admits more chance matches (`duplicate_sensitivity.csv`). All 66 removals were audited against metadata: composition differences are nominal-vs-measured
values of the same alloys; USE/DBTT of copies differ by a median of 0.5 J and 2 °C.

**Keep-rule comparison at CP1** (`duplicate_keep_rule_comparison.csv`, now regenerated with the hierarchy): most-records-first removes 752 records and keeps 40 points found in no other copy; earliest-publication-first
removes 783 and discards 32 such points; most-corroborated-first removes 770. "Uncorroborated" points are either extra real data or errors, and cannot be told apart
without the papers. Example of an error: in dataset curve 90 (ref 19, kept) two points at 25 °C/210.85 J and 100.3 °C/233.6 J belong to a different alloy's
upper shelf on the same figure. Chosen rule removes only records that are demonstrably copies; every uncorroborated kept point carries
`flag_point_not_corroborated_by_duplicate_copies`; composition disagreements between copies carry `flag_duplicate_copies_disagree_on_composition`.

**Known limitations (CP1; the first is now resolved, see above).** A duplicate whose labels disagree was not compared (ref 53 curve 237 labelled base metal vs weld-metal curve 241). The ref 52/55 irradiated 5 mm pair at 50 % match remains a partial overlap (no constant offset aligns it). Units with fewer than 3 points are never removed.

**Alternatives.** Keep all copies (double counting); remove only matched points rather than whole units (leaves fragments of 1–3 points); manual curation from the papers.
**If the alternative were chosen.** Keeping copies: +752 records, the SA508 Gr.4N alloys counted up to seven times, scatter understated. Point-level removal: similar totals, plus orphan fragments for WP2 to handle.

## D-020 — "Pre-Cracked" label in record-B
**Status:** APPROVED (CP1) — rule set by the author; source checks completed

**CP1 decision (author).** Do not exclude whole publications because of a dataset-level "Pre-Cracked" note. In the primary analysis keep
records that can be supported as ordinary Charpy V-notch impact measurements; exclude records that can be supported as precracked
fracture-toughness measurements; if a record or series is still genuinely ambiguous after checking the source, flag it and exclude it from
the primary analysis rather than guessing, preserving it for sensitivity analysis.

**Source checks (evidence per reference in `src/curated_metadata.py::SPECIMEN_TYPE_CHECKS`; record field `specimen_type_check`).**
- Ref 1: [NP-1661] full report — every absorbed-energy (J) versus temperature figure for SA533B-1 is a Charpy V-notch figure (Figs 2-5, 3-14,
  3-15, 3-17); precracked Charpy results appear only as fracture toughness or normalized energy. Ordinary CVN.
- Ref 13: [Lee2014] full text — Charpy tests on standard V-notch specimens to ASTM E23-07a; precracked specimens were tested in quasi-static
  bending for the master-curve T0 (ASTM E1921-09c). Ordinary CVN.
- Refs 19, 20: [Lee2011] abstract (CVN to ASTM E23, fracture toughness to ASTM E1921); every curve is identical to curves of refs 17, 27, 28,
  which record-B's own curation notes call "No Pre-cracked Specimen". Ordinary CVN.
- Refs 43, 44: [BLG-1016] Tables 1–4 — the compositions are identical to SCK•CEN's 20MnMoNi55 and JSPS steels, whose Charpy V-notch
  properties (USE 181 J, T41J −76 °C; USE 72 J, T41J 34 °C) match these curves; ref 44's precracked specimens were for its crack-resistance tests. Ordinary CVN.
- Refs 8, 9: records cite ASTM E23 and parts of both are point-for-point identical to V-notch curves elsewhere; full texts not accessible.
  Supported as ordinary CVN (both are excluded from the primary population anyway, for unresolved irradiation labels, D-021).
- Ref 23: records cite ASTM E23; not source-checked because SA508 Gr.1A piping is outside the primary population (D-027).

**Outcome.** No record is supported as a precracked fracture-toughness measurement and no record remains ambiguous on specimen type,
so this rule removes nothing (the WP2 population accounting shows the zero explicitly). If a later check finds a precracked series,
setting its resolution to `pre-cracked` or `unresolved` in `SPECIMEN_TYPE_CHECKS` routes it out of the primary population.

**History — pre-CP1 provisional decision.** Do not exclude. Flag records that record-B labels "Pre-Cracked" (`flag_precracked_label_in_later_release`) and, separately, references whose own text reports precracked specimens (`flag_source_reports_precracked_specimens`: ref 1; ref 44, whose records all left at E8).
**Evidence.** B labels every record of refs 1, 8, 9, 13, 19, 20, 23. These records are 55×10×10 mm V-notch specimens with ASTM E23 cited where a standard is given, lower shelves of 2–4 J and upper shelves of 180–360 J, typical of standard Charpy tests. [Lee2011] states Charpy tests to ASTM E23 and fracture toughness to ASTM E1921 — the precracked specimens were for the separate toughness tests. Precracked fracture-toughness tests do not normally produce absorbed-energy transition curves. Ref 44's title says "precracked Charpy specimens", yet all its curves duplicate curves of ref 43 (an instrumented Charpy V-notch study). But [NP-1661] (ref 1) does cover both Charpy V-notch and precracked Charpy data, so ref 1 remains genuinely uncertain.
**Alternatives (pre-CP1).** Exclude all labelled records (−366 retained records at CP1); exclude ref 1 only.
**If the alternative were chosen.** Loss of hundreds of ordinary Charpy V-notch records, including ref 1's irradiated and reconstituted SA533B-1 data, on the strength of a paper-level note.

## D-021 — Irradiation status that differs between releases
**Status:** CP1 decision 1 applied (disagreements remain flags; newer is not assumed correct). Treatment of unresolved labels APPROVED (CP2,
D-035); ref 13's source-check resolution APPROVED (CP2, with the WP2 state)

**Decision (after CP1).** Keep record-B's label in the data, flag every disagreement, and check the source. The field
`irradiated_resolved` holds the label both releases agree on, or the source-supported value where a check resolves the disagreement,
otherwise record-B's label; `irradiation_label_check` says which (`src/curated_metadata.py::IRRADIATION_LABEL_CHECKS`).
- Ref 13 — **resolved: not irradiated.** [Lee2014] full text is a tempering/PWHT study of an unirradiated model alloy; "irradiation" occurs only in a
  cited title. Record-A is right and record-B wrong for all 57 records (47 retained after E8).
- Refs 7, 8, 9, 53 — **unresolved** (full texts not accessible). Record-B's curation notes say irradiation conditions were added after
  "checking references", the same route that produced the demonstrably wrong ref 13 label; ref 8 curve 33 and ref 9 curves 34 and 36 are
  point-for-point identical to unirradiated curves in other papers; for ref 53, [Kim2012]'s abstract reports irradiated base-metal
  specimens, which record-A has (curve 242) and record-B does not. These point towards record-A but do not settle every series.
- Unresolved labels cannot rule out a duplicate match (D-019); the four republished series are removed at E8.
- After E8, 138 retained records carry an unresolved label (refs 7, 8, 9, 53; 11 dataset series). They are excluded from the primary
  analysis and preserved (D-035, approved at CP2).

**History — pre-CP1 provisional decision (superseded).** Use record-A's irradiation status; flag the 200 retained records where record-B differs (`flag_irradiation_status_differs_between_releases`; refs 7, 8, 9, 13, 53).
**Evidence.** B changes 226 records from "No" to "Yes" and 12 from "Yes" to "No"; 78 of the new "Yes" records gain a fluence and the rest have none (`dataset_version_comparison.md`). Four curves B marks irradiated (refs 8, 9, 9, 13) match unirradiated curves in other publications point for point (10/10, 13/13, 15/15, 15/15) within digitization error. Neutron irradiation hardens these steels and shifts the transition curve, so an irradiated curve should not reproduce an unirradiated one point for point: those relabels are very likely wrong. The ref 53 changes could not be checked this way.
**Alternatives.** Adopt B's values without checking; adopt A's values everywhere; exclude all disputed records.
**If the alternative were chosen.** Adopting B unchecked would have kept four republished unirradiated series (53 records) as extra "irradiated" curves and mislabelled ref 13; adopting A everywhere would override the primary release without evidence for refs 7, 8, 9, 53; excluding all disputed records would also discard ref 13's 47 verified records.

## D-022 — The dataset's USE, DBTT and curve-ID columns
**Status:** APPROVED (CP1 decision 7)

**CP1 decision (author).** `curve_id_dataset` is provenance, not scientific ground truth. Where one ID mixes geometries, irradiation
conditions, material conditions, heats or anything else that should not be fitted together, split it by the WP2 grouping definition (D-033).
**Decision.** Keep as reference-only fields (`_dataset` suffix). They are not used as ground truth; WP3 fits its own curves. The curve ID may be used as a starting point for WP2 grouping, subject to the WP2 rules.
**Why.** The method and DBTT criterion are undocumented; DBTT cannot be a 41 J temperature for miniature specimens whose USE is below 41 J; copies of identical data carry different values (up to 32 J and 14 °C apart), which suggests per-copy fitting by the dataset authors; ten curve IDs mix geometry, irradiation, treatment, condition or orientation (D-028).
**Alternatives.** Use them as published transition temperatures for comparison in WP4.
**If the alternative were chosen.** The WP4 cross-check would compare against numbers of unknown definition.

## D-023 — Special material and specimen conditions are tagged, not excluded
**Status:** DECIDED; WP2 outcome APPROVED (CP2): each condition forms its own curves in the primary population (D-033; reconstituted specimens are never combined with conventional ones without a later, approved analysis), except additively manufactured material (secondary, D-034) and ref 1's series whose labels the source contradicts (D-031)
**Decision.** Keep and tag: reconstituted specimens, shock-wave-hardened surrogate (ref 1), pre-strained (ref 41), simulated HAZ (ref 15), HAZ, weld region, step cooled, PWHT, standard reference material (ref 2), orientation semantics differ (ref 31), additively manufactured (ref 31).
**Why.** None is invalid as a Charpy test; each defines a different material condition. Whether a condition forms its own curve or is excluded is a curve-definition question (WP2) whose influence must be tested there.
**Alternatives.** Exclude all non-standard conditions now.
**If the alternative were chosen.** Several hundred records removed before the inclusion rule is stated and sensitivity-tested.

## D-024 — Text harmonization of other columns
**Status:** DECIDED
**Decision.** Change only case, spelling, spacing, one duplicated label ("Reconstituted" → "Reconstituted specimen") and one spreadsheet auto-fill artefact ("EN 10045-1:1990" … ":1997", where the year increments row by row, → "EN 10045-1"). Orientation codes are not changed. Every change is in `value_changes_log.csv`; maps in `curated_metadata.py::TEXT_VALUE_MAPS`.
**Why.** Removes spurious distinctions that would otherwise split groups in WP2, without merging different meanings (e.g. "T" is not merged with "T-L").
**Alternatives.** Leave all text verbatim; normalize orientation codes.
**If the alternative were chosen.** Verbatim: WP2 grouping would treat "Step cooling" and "Step Cooling" as different treatments. Normalized orientation: would require guessing what single-letter codes meant.

## D-025 — Order of exclusion steps and how records are counted
**Status:** DECIDED
**Decision.** Steps run in the order E1 scope → E2 pending scope → E3 test type → E4/E5 missing essentials → E6 impossible → E7 exact duplicates → E8 duplicate curves. Each record is counted once, at the first step that applies. `exclusion_reasons_all_applicable.csv` counts every criterion for every record regardless of order.
**Why.** Scope first avoids spending judgement on data that leave anyway; duplicates last, so a valid copy is never removed in favour of a copy that is itself invalid.
**If the alternative were chosen.** Same final set for E1–E7 (their criteria are independent); per-step counts would differ; E8 could keep a copy that a later step would have removed.

## D-026 — Fill-rate bands in the data dictionary
**Status:** DECIDED
**Decision.** Descriptive bands on ferritic records: ≥95 % complete or nearly complete; 50–95 % partially populated; 10–50 % sparse; <10 % very sparse (unusable for dataset-wide analysis).
**Why.** The brief asks which fields are too sparse to use; usability depends on the question, so bands describe coverage and do not decide use. Conditional completeness (e.g. fluence for irradiated records) is reported separately in `notable_facts.md`.

## D-027 — SA508 Grade 1A piping steel
**Status:** APPROVED (CP1 decision 3)

**CP1 decision (author).** SA508 Grade 1A main-steam-line piping data are not part of the main RPV population. Keep them, flagged, but
exclude them from the primary RPV analysis; they may be used later as a secondary or sensitivity group. Implemented as a WP2 population
step (D-034): refs 22, 23, 30, 32, 40, identified by grade in the citation title.

**History — pre-CP1 provisional decision (superseded).**
**Decision.** Keep refs 22, 23, 30, 32, 40 (SA508 Grade 1A, carbon steel for main-steam-line piping; 212 retained records) in scope as members of the SA508 specification family, identified through `ref_grade_title`.
**Why.** They meet the brief's literal family definition and are ferritic with a transition, but they are not vessel steels. Deciding scope by grade is the author's call.
**If the alternative were chosen.** −212 retained records, all full-size unirradiated curves.

## D-028 — Dataset curve IDs with internal inconsistencies
**Status:** DECIDED (WP1 flags); split in WP2 per CP1 decision 7 (D-033)
**Decision.** Flag, do not correct (`flag_dataset_curve_id_mixes`); WP2 splits mixed IDs by its own grouping variables. Examples: curve 271 combines 20×2.5×2.5 mm unirradiated and 23.6×3.33×3.33 mm irradiated specimens (it also causes the only energy/USE ratio above 1.25); curve 6 includes 2 irradiated and 12 reconstituted records among 107; curves 66 and 76 pool two simulated-HAZ sub-zones each.
**Why.** Correcting requires deciding what the curve should be, which is WP2's curve definition.

## D-029 — Material label that contradicts composition
**Status:** DECIDED (flag); duplicate resolution in E8 APPROVED (CP2)
**Decision.** Flag, do not relabel, the 11 records of ref 53 curve 237: labelled A533B base metal but carrying the weld-metal composition (C 0.08, Ni 0.83, Mn 1.33) of the same paper, in a sequence (base, HAZ 1 mm, HAZ 4 mm, weld) that repeats for another figure.
**Why.** The evidence strongly suggests weld metal, but relabelling is an inference.
**Resolution (WP2 inspection).** Its 11 points are identical to weld-metal curve 241 of the same paper, so it is the weld-metal series shown a
second time under a wrong label. Because a contradicted material label can no longer rule out a duplicate match (D-019), E8 now removes it in favour of curve 241 (criterion (c)).
**Approved at CP2 (author).** Curve 237 is excluded from the primary independent-data population and nothing about it is lost: its 11 raw
records stay in `charpy_records_with_status.csv` with the verbatim label (`material_raw` 'A533B' / 'A533B '), the flag
`flag_label_says_base_metal_but_weld_metal_composition`, `exclusion_step` E8 and an `exclusion_reason` naming the kept copy (curve 241, 11 of
11 points matched, criterion (c)); the pair is in `duplicate_curve_pairs.csv` and `duplicate_curve_removals.csv`.

## D-030 — Git repository
**Status:** APPROVED (CP1 decision 6); branch-per-unapproved-work-package convention APPROVED (CP2)
**CP2 decision (author, 2026-09-13).** Merge the completed `wp2` branch into `main` only after the CP2 decisions are implemented and the full
pipeline is verified from raw data; use an explicit non-fast-forward merge so the checkpoint stays visible in history; keep the `wp2`
branch; no remote, no push.
**Decision.** Git initialized after CP1. Commit `9bc28fc` on `main` is the CP1 state exactly as presented (verified to regenerate
byte-identically before committing). Later work is committed at meaningful boundaries on a branch named for the work package
(`wp2`), so `main` holds only checkpoint-approved states; merge after approval. No remote, no push, unless the author asks.
Repository-local author identity (`git config user.name/user.email`); global settings untouched.
**Alternatives.** Commit directly to `main`; no version control.
**Why.** A branch per unapproved work package keeps the approved state recoverable and makes each checkpoint's changes reviewable as one diff.

## D-031 — Condition labels that the source contradicts
**Status:** APPROVED (CP2); extended to the two irradiated-labelled records of series 6 (curve 1-6.3) by the author while CP2 was finalized

**CP2 decision (author, 2026-09-13).** Exclude from the primary analysis the records whose condition labels the source evidence
contradicts. Raw measurements are not altered; uncertain labels are not replaced with invented corrected values; the records, the source
evidence and the exact reason each affected series is excluded are preserved (record field `flag_condition_label_contradicted_by_source`,
curve field `condition_label_contradicted_by_source` in `curve_inventory.csv`, table in `wp2_summary.md` §7), and the records stay outside
the primary population (population step P2, curve IDs kept) for audit or sensitivity use.
**Extension (author decision when CP2 was finalized).** Ref 1 series 6 is unirradiated HSST Plate 02, but two of its reconstituted records
(R0172, R0173; curve 1-6.3) carry exactly the series-7 label "irradiated, 3×10¹⁹ n/cm²" that NP-1661 Fig. 3-17 contradicts. Their
energies do not fit an irradiated curve either: the irradiated series 7 has only 11 J at −7 °C, while these give 6.9 J at −74.8 °C (within
the unirradiated data, e.g. 7.4 J at −70.5 °C) and 41.3 J at −59.8 °C (above even the unirradiated original specimens at −60 °C, 8.9–22.3 J).
(When the question was put to the author, both energies were described as inside the unirradiated scatter; that holds for the first
point only. The decision rests on the identical contradicted label.) The original entry missed them because the contradiction map was
keyed by dataset series. Put to the author because it changed an approved count: P2 grows from 46 records / 6 curves
to 48 / 7, and the primary population before screening from 192 curves / 2,736 records to 191 / 2,734. No cohort changes (1-6.3 has 2
points and fails every rule). The map now names the records it covers (`SOURCE_CONTRADICTED_LABELS`, `records` = "all" or "irradiated").
**Context.** Checking ref 1 for D-020 showed two labeling errors present in both releases (`SOURCE_CONTRADICTED_LABELS`):
- *Shock-hardening treatment labels shifted by one series.* [NP-1661] Table 3-1 gives tanh fits for heat IbH: non-shocked USE ≈ 136 J,
  T0 ≈ 13 °C; bottom layer USE ≈ 108 J, T0 ≈ 21 °C; top layer USE ≈ 41 J, T0 ≈ 7 °C. Dataset curves 3, 4, 5 (labelled bottom-surface
  hardened, top-surface hardened, untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 °C: curve 3 is the non-shocked material,
  curve 4 the bottom layer, curve 5 the most-hardened top layer.
- *Fluence.* Curve 7 (irradiated HSST Plate 02, original and reconstituted specimens) has 3×10¹⁹ n/cm² in the dataset; NP-1661 Fig. 3-17
  gives 2.5×10¹⁸ n/cm² (E > 1 MeV).
NP-1661 also covers several heats (D, IbH, HSST Plate 02 = IbA) while every ref 1 record carries one composition, so for this reference
composition cannot identify the heat.
**Decision.** Flag (`flag_condition_label_contradicted_by_source`, 48 retained records: dataset series 3, 4, 5 and 7, and the two
irradiated-labelled records of series 6; WP2 curves 1-3.1, 1-3.2, 1-4, 1-5, 1-6.3, 1-7.1, 1-7.2); do not relabel. Relabeling would create
values that neither release publishes. These records are outside the primary population (D-034); they count as an unresolved labeling
problem in the duplicate hierarchy.
**Alternatives.** Relabel from the source; keep the dataset labels.
**If the alternative were chosen.** Relabeling: 4 more curves in the primary population (one unirradiated, two shock-hardened, one
irradiated), at the cost of project-made labels (1-6.3 could not be relabelled at all: its true condition is unknown). Keeping dataset
labels: an "untreated" SA533B-1 curve that is really the most-hardened surrogate would enter the primary analysis, and a 12× fluence error
would enter the inventory.

---

# WP2 — Curve grouping and inclusion criteria

All numbers below are for the 2025.30 primary release and regenerate with `src/wp2_curves.py` into `outputs/wp2/` (the 2024.206
release: `outputs/wp2_sensitivity_eny5v-www93/`). Nothing in WP2 is fitted; the dataset's USE, DBTT and curve IDs are provenance only (D-022).

## D-032 — A curve never spans two publications or two dataset series
**Status:** APPROVED (CP2, with the WP2 state)
**Decision.** Records from different source publications are never one curve. Within a publication, the dataset series (`curve_id_dataset`;
records without an ID form their own set) is a boundary a curve never crosses; the grouping variables of D-033 split series, never merge them.
**Evidence.** Seven pairs of different series agree on every recorded grouping variable yet are different materials or conditions
(`outputs/wp2/fluence_treatments.csv`, diagnostic rows): ref 17 series 84 and 85 are two Ni/Cr model alloys with the same recorded
composition (dataset USE 180 vs 218 J, DBTT −42 vs −107 °C); ref 1 series 5 and 6 are the most-hardened shock surrogate and HSST Plate 02
(D-031); ref 41 series 187 and 188 (dataset DBTT −104 vs −82 °C); ref 53 series 241 and 245 (unirradiated weld metal vs a series whose
irradiation label the releases dispute); ref 1 series 3/4 and 6/7 (mislabelled records); ref 15 series 76/77 (two ICIC records inside
an FGFG series). Ref 1's records carry one composition for several heats (D-031). The recorded columns therefore do not always identify
heat or condition, while the series is the source figure's own plotted grouping. Across publications, laboratory, machine and
calibration differences would enter one curve's scatter (brief §3); republications of the same tests are handled by E8 (D-019).
**Alternatives.** Merge series that agree on all recorded variables; pool the same heat across publications (e.g. HSST Plate 02).
**If the alternative were chosen.** Seven merges (226 instead of 233 curves before inclusion), five of which demonstrably mix different
materials or labels; pooling across publications would mix between-laboratory differences into single-curve scatter.
**Limitation.** A curve that the dataset authors split across two series stays split. The only candidate seen is ref 15's two ICIC records
in series 76, left as a 2-point fragment that fails every rule.

## D-033 — The definition of one transition curve (grouping variables)
**Status:** APPROVED (CP2), with the author's interpretation for reconstituted specimens

**CP2 decision (author, 2026-09-13): reconstituted specimens.** Reconstituted specimens are legitimate published Charpy measurements and
are not discarded because they are reconstituted. Reconstitution is, however, a materially different specimen history. Therefore they are
kept as transition curves separate from otherwise comparable original specimens (the test-condition statement is a grouping variable);
the tag travels through every later work package (record field `tag_reconstituted_specimen`, curve field `reconstituted`, both carried in
`cohort_membership.csv`); and reconstituted and conventional specimens are not combined unless a later, explicitly justified analysis is
approved by the author.
**Decision.** Within one publication and one dataset series, records are one transition curve only if they agree on all of:
- *material identity:* `material_std` (specification, type/grade, class where stated, weld-metal label) and the heat chemistry
  (`composition_signature`, all reported elements; the heat proxy, as the dataset has no heat or lot identifier); product form (D-013);
- *specimen geometry:* length, width, thickness, notch depth, notch angle, notch root radius, and orientation;
- *irradiation condition:* irradiation status as resolved in D-021, fluence level (D-036), irradiation temperature and time;
- *material condition:* treatment, post-treatment temperature and time, cooling method and rate;
- *specimen/test condition statement:* HAZ location, reconstituted specimen, welded area, standard reference material, striking velocity.
A blank value is its own value; nothing is filled in. Curve IDs read `<ref>-<series>` with `.k` for pieces of a split series.
**Why each matters physically.** Different specifications, classes and heats have different strength and toughness; product forms differ in
microstructure, segregation and cleanliness; absorbed energy and the transition temperature depend strongly on specimen size, notch acuity
and crack orientation relative to rolling; neutron fluence and irradiation temperature raise the transition temperature and lower the upper
shelf; tempering, PWHT, step cooling, HAZ thermal cycles and pre-strain change the microstructure; reconstituted specimens are prepared
differently; loading rate shifts the transition (ASTM E23-82 X1.6).
**Not used.** Manufacturer, microstructure, morphology and grain size (descriptive; never vary within a series; the releases relabel some of
them); test standard (edition differences do not define a material); dataset USE, DBTT and curve IDs (fitted outputs and provenance, D-022).
**Result.** 243 curves from the 3,446 records retained under either duplicate keep rule (233 under the canonical rule). Nine dataset series
are split (246 records; `dataset_series_splits.csv`): simulated-HAZ sub-zones (ref 15 series 66, 76), reconstituted versus original
specimens (refs 1, 21), weld region versus unidentified base (ref 18), two geometries and irradiation states (ref 59 series 271), irradiated
records inside an unirradiated series (ref 1 series 6), a treatment-label mix (ref 1 series 3), one record at a different PWHT temperature
(ref 39 series 182). Under the alternative keep rule the heat-chemistry field also separates the two contaminating points of ref 19
series 90 (D-019): they carry Cr 2.47 wt.% instead of 1.04, the composition of the other alloy on that figure. Special conditions stay as their own curves in the primary population (reconstituted, simulated HAZ, PWHT, step
cooled, pre-strained, standard reference material, the deliberately embrittled JSPS plate; counts in `wp2_summary.md` §7).
**Alternatives.** Coarser grouping (family, geometry and irradiation status only); pool reconstituted with original specimens.
**If the alternative were chosen.** Coarser grouping would pool, for example, ref 15's FGCG and ICCG simulated-HAZ zones (lowest energies
8 J vs 29 J) into one curve, turning a material difference into apparent scatter. Pooling reconstituted specimens would enlarge 1-6.1
(95 → 105 points) and 21-100.1 (14 → 20). NP-1661 reports that reconstitution did not change properties, but that is not enough to pool by
default: pooling may be examined later only as an explicitly justified analysis that the author approves (CP2 decision above).

## D-034 — Primary RPV population and secondary groups
**Status:** P1–P4 implement CP1 decisions 1–3 (P2 and P3 as approved at CP2 in D-031 and D-035); P5 APPROVED (CP2)

**CP2 decision (author, 2026-09-13): additively manufactured SA508.** Approved as a SECONDARY group, not part of the primary
conventional-RPV population: the manufacturing route can materially affect microstructure and toughness, so this material must not be
pooled with conventional or forged SA508 as though the route were irrelevant. All 66 records are preserved. The identifying tag travels
with every record and curve through later work packages (`product_form` = "additively manufactured" and `population_step` = P5, in
`charpy_records_with_curves.csv`, `curve_inventory.csv` and `cohort_membership.csv`). Permitted later uses: a clearly labelled secondary or
sensitivity population (cohort `plus_additively_manufactured`), and secondary evidence in the WP5 specimen-size analysis if scientifically
useful. It must not affect the primary headline conclusion unless a later, explicitly approved sensitivity analysis evaluates that effect.

**Decision.** Starting from the 3,198 records WP1 retains, each record is assigned to the first step that applies
(`population_accounting.csv`; nothing is deleted, every record keeps its curve ID):

| step | criterion | records | curves |
|---|---|---|---|
| P1 | specimen type not supported as ordinary Charpy V-notch (D-020) | 0 | 0 |
| P2 | condition label contradicted by the source (D-031) | 48 | 7 |
| P3 | irradiation status unresolved between releases (D-035) | 138 | 11 |
| P4 | secondary: SA508 Gr.1A main-steam-line piping steel (CP1 decision 3) | 212 | 19 |
| P5 | secondary: additively manufactured SA508 Gr.3 (ref 31) | 66 | 5 |
| | **primary RPV population** | **2,734** | **191** |

At the CP2 presentation P2 was 46 records / 6 curves and the primary population 2,736 / 192; the difference is curve 1-6.3 (D-031).

**Why P5.** The brief's scope is RPV steels and their welds. Ref 31's material is laser powder directed-energy-deposited SA508 Gr.3
chemistry, not a plate, forging or weld made by an RPV fabrication route: its layer-wise solidification microstructure and anisotropy
(its own records note that orientation means something different) are not those of vessel material, and it matches none of the product
forms WP5 must compare. Same reasoning as the piping decision: in the specification family, outside the vessel population.
Laboratory heats and model alloys stay in: they are melted, hot worked and heat treated like the product they model.
**Alternatives.** Keep additively manufactured material in the primary population as its own product form.
**If the alternative were chosen.** +5 curves before inclusion, +5 curves and +66 records in the primary cohort (cohort `plus_additively_manufactured`, D-039).

## D-035 — Unresolved irradiation labels are outside the primary population
**Status:** APPROVED (CP2)

**CP2 decision (author, 2026-09-13).** Where irradiation status cannot be resolved from adequate source evidence: exclude those records from
the primary analysis; preserve the records and their uncertainty flags (record fields `irradiation_label_check`, `irradiated`,
`irradiated_in_other_release`, `flag_irradiation_status_differs_between_releases`; curve fields `irradiation_label_check` and
`irradiated_in_other_release`); keep them available for an explicit later sensitivity analysis where useful; never guess the irradiation
state; never treat a conflicting dataset label as ground truth merely because it appears in the spreadsheet. The cohort
`plus_unresolved_irradiation` is such a sensitivity case: it is run once per release, with each release's own labels, as an explicit
"if these labels were right" comparison, not as a finding about which label is true.
**Decision.** Records whose irradiation status the two releases disagree on and the source check could not resolve (refs 7, 8, 9, 53;
D-021) are excluded from the primary population and preserved. Cohort `plus_unresolved_irradiation` carries them with each release's
own labels.
**Why.** Irradiation condition is a grouping variable and later stages analyse irradiated and unirradiated curves differently; a curve
whose status is unknown cannot be placed in either set without guessing. This applies CP1 decision 2's rule for ambiguity (flag,
exclude from the primary analysis, preserve for sensitivity) to the other disputed label, and follows CP1 decision 1 (newer is not assumed correct).
**Alternatives.** Use the 2025.30 labels; use the 2024.206 labels.
**If the alternative were chosen.** +9 curves passing the primary rule and +116 records in either release, but labelled irradiated
(2025.30) or unirradiated (2024.206) (`outputs/wp2*/wp2_summary.md` §6).

## D-036 — How fluence is treated in curve grouping
**Status:** APPROVED (CP2, with the WP2 state)
**Inspection** (`fluence_by_source.csv`). 570 irradiated records retained by WP1; 492 carry a fluence (6.2×10¹⁷ to 1.11×10²⁰ n/cm²) and
343 an irradiation temperature. No dataset series contains more than one fluence value. Within sources the reported levels are distinct
exposures: ref 59 1.3×10¹⁸, 2.7×10¹⁸, 2.7×10¹⁹; ref 104 (no series IDs) 6.2×10¹⁷, 3.9×10¹⁸, 1.3×10¹⁹, 2.34×10¹⁹; ref 16 1.48, 1.75 and
2.52×10¹⁹ in three series; ref 50 2.7, 2.8 (two irradiation temperatures) and 3.1×10¹⁹ in four series of two plates.
**Decision.** Fluence enters the curve key as the exact reported value, compared only within one publication and dataset series.
**Alternative carried forward.** Levels within a factor of 1.2 of each other (single linkage, same publication and series) are one level.
Basis: the uncertainty of an absolute fluence value is about 20 % when a single measurement is compared with a calculation
[Jendrich2003]. No bins are used: pooling different exposures into one curve mixes different transition temperatures, because the
irradiation shift grows with fluence [E900]; relative fluences within one irradiation programme are much better determined than absolute
values [Jendrich2003], so reported levels within a source are real distinctions; and the neutron-energy threshold is unknown (D-011),
so fluence values from different sources are not comparable anyway.
**Result.** Exact values and the factor-1.2 tolerance give identical curves (233 under the canonical keep rule). The treatment cannot matter
here: fluence never varies within a series, and the only source without series IDs has levels at least 1.8× apart.
**Diagnostic.** If the series boundary were ignored, the tolerance would merge ref 16's series 80 and 81 (1.48 vs 1.75×10¹⁹): different
model alloys whose dataset DBTTs are −14 and −75 °C (`fluence_treatments.csv`). This supports D-032 rather than the tolerance.
**If the alternative were chosen.** No change to any curve or cohort.

## D-037 — Describing how a curve samples its shelves and transition, without fitting
**Status:** APPROVED (CP2), with the author's clarifications 4A (terminology) and 4B (basis of the transition band)
**Decision** (`curve_inventory.csv`).
- *Distinct test temperatures:* temperatures closer than 2 °C are one (about twice the 95th percentile of the digitization difference
  between copies of the same point, D-019).
- *Screening references (terminology fixed at CP2, clarification 4A):* lower = the lowest measured energy (`E_min_j`); **screening upper
  reference** (acceptable alternative name: "upper-shelf reference") = the mean of the three highest measured energies
  (`E_screening_upper_reference_j`). It is a pre-fit screening quantity. It must not be called the measured or ASTM upper-shelf energy
  (USE) merely because it averages three high observations: nothing in WP2 shows that those points lie on a flat upper shelf (54-247's top
  end, for example, is still rising). Three points are averaged so that no single high point sets the scale, as [E185-82] §4.18 averages
  normally three upper-shelf specimens; that is the reason for "three", not a claim that the quantity is the E185 USE. USE estimation
  belongs to WP3 and must follow the method separately justified and approved there.
- *Energy bands:* each point's position between the two references, 0 (lower) to 1 (upper). Lower band ≤ 0.12; transition band 0.12–0.88;
  upper band ≥ 0.88. **Basis (clarification 4B).** For the normalized hyperbolic tangent y = (1 + tanh x)/2 with x = (T − T0)/C,
  y = 0.119 at x = −1 and y = 0.881 at x = +1. The 0.12–0.88 interval is therefore approximately the central characteristic transition
  interval T0 − C to T0 + C (the middle 76 % of the rise). This is a project-defined, model-based screening convention. It is not an ASTM
  requirement, and it is not uniquely correct.
- *Alternative preserved (clarification 4B).* An approximately 0.10–0.85 transition-region convention is kept as a later sensitivity or
  diagnostic option. No source for it is documented in this repository (every tracked file was searched when CP2 was finalized), so its
  literature basis must be found and cited before it is used (brief §7). It changes no cohort now; cohort membership is never changed to
  obtain a nicer curve count.
- *Energy ratio:* lowest energy / screening upper reference (how far the coldest test fell towards the lower shelf).
- *Diagnostic only:* Spearman rank correlation of energy with temperature.
**Change made during WP2, logged under brief §7.** The first version used the single highest energy as the screening upper reference. Inspecting the curves that failed only the
upper-band criterion showed flat, scattered upper shelves failing because one high point set the band (e.g. 57-264, whose points
at 95–180 °C lie between 75 and 119 J; 56-262, levelling at 43–51 J). That definition would preferentially reject high-scatter curves and so
bias the WP6 scatter model low. It was replaced by the E185-style average of three. The change was made because of what the descriptor measured;
no fit or uncertainty result exists yet. Effect (`screening_upper_reference_diagnostic.csv`): primary rule 157 → 170 curves (2,410 → 2,588 records);
stricter 48 → 60; looser 183 → 182.
**Known limitations.** Upper-shelf scatter larger than 12 % of the rise is counted as transition; a still-rising top end can pass as upper
band when its three highest points are close (e.g. 54-247). Rank correlation is not a criterion: its low values here come from upper-shelf-
dominated miniature curves (ref 53) and from energy falling above about 250 °C (ref 104), not from mixed data.
**Alternatives.** Fit a model to classify shelves (that is WP3); fixed absolute energy thresholds (not transferable across specimen sizes).

## D-038 — Inclusion rules: primary, looser, stricter
**Status:** APPROVED (CP2) as the PRIMARY PRE-FIT SCREENING RULE, with the author's clarifications 4A–4C

**CP2 decision (author, 2026-09-13).** The primary rule is approved as a pre-fit screening rule, and this distinction is mandatory. Passing
D-038 means only: *this data group appears sufficiently sampled to ATTEMPT transition-curve fitting in WP3.* It does NOT establish that the
tanh model will fit successfully, that the fit will be well conditioned, that the extracted parameters will be physically reasonable, or
that the curve is scientifically valid because it passed the screen; and a curve whose WP3 fit fails may not be silently removed. WP3
fitter validation and explicit fit-failure accounting remain mandatory. The looser, primary and stricter cohorts are frozen and preserved
for downstream sensitivity analysis rather than regenerated later with changed thresholds (D-039). Clarifications: 4A the upper quantity is
the *screening upper reference*, not a measured or ASTM upper-shelf energy (D-037); 4B the 0.12–0.88 band stays for the primary rule, as a
project-defined, model-based convention with a preserved 0.10–0.85 alternative (D-037); 4C the 15 unirradiated / 12 irradiated specimen
counts stay as the STRICTER comparison cohort, described as historical ASTM E185 surveillance-programme guidance/requirements used here as
a deliberately conservative comparison, not as a universal statistical law that a curve with fewer points is unusable.

**Decision** (`RULES` in `src/wp2_curves.py`; failing criteria per curve in `curve_inventory.csv`):

| criterion | looser | primary | stricter | basis |
|---|---|---|---|---|
| points | ≥ 5 | ≥ 6 | ≥ 15 unirradiated, ≥ 12 irradiated | 5 leaves one residual degree of freedom for a 4-parameter tanh, 6 leaves two; stricter = the historical [E185-82] §6.3.1–6.3.2 surveillance-programme specimen minimums, a deliberately conservative comparison, not a statistical law |
| distinct temperatures in transition band (0.12–0.88, D-037) | ≥ 1 | ≥ 2 | ≥ 3 | 1 locates the transition; 2 fix location and width (T0 and C); 3 add a check on the shape |
| upper band | no requirement | ≥ 2 points at ≥ 2 temperatures | ≥ 3 points at ≥ 2 temperatures | two temperatures show the rise has stopped; three points mirror the normally three specimens [E185-82] §4.18 averages (a screening count, not a USE determination) |
| lower band | — | — | ≥ 2 distinct temperatures | lower-shelf plateau shown |
| lowest energy / screening upper reference | ≤ 0.30 | ≤ 0.20 | ≤ 0.15 | coldest point at or below the lower band edge when the true lower/upper shelf ratio is ≤ 0.20 / 0.09 / 0.03 (full-size RPV steels are typically a few %) |

**Outcome** (`rule_outcomes.csv`, `rule_outcomes_by_group.csv`). Primary population before screening: 191 curves, 2,734 records.
Looser keeps 182 curves (2,692 records); primary 170 (2,588; loses 21 curves and 146 records); stricter 60 (1,333; median 19 points).
Primary losses: 9 curves never approach the lower shelf (4 simulated HAZ, 3 plate, 1 reconstituted forging, 1 irradiated KLST), 5 jump across the
transition with one intermediate temperature (e.g. 11-47), the other 7 are fragments of 1–5 points; two narrow misses have ratios of 0.21 (21-100.2, 109-291).
The stricter rule removes most curves for point count (the E185 counts) and keeps 15 of 38 irradiated and 21 of 39 miniature curves.
At the CP2 presentation the population was 192 / 2,736 and the primary rule lost 22 curves / 148 records (15 of 39 irradiated); the
difference is the 2-point curve 1-6.3, which failed every rule and now leaves earlier, at P2 (D-031). No cohort changed.
**Why the primary rule is not the stricter one.** The project must characterise how index-temperature uncertainty grows as sampling
becomes sparse (brief WP3 note). A rule admitting only surveillance-standard sampling would remove the sparse curves whose ill-conditioning is
under study, and most irradiated and miniature curves with them. The primary rule asks only for what makes the tanh parameters
identifiable in principle, with minimal redundancy. The stricter rule is the "surveillance-quality" contrast; that E185 asked for more
specimens does not prove a curve with fewer is unusable, which is why it is the comparison cohort and not the primary rule.
**Sensitivity.** Not yet quantified for the headline result, which does not exist until WP6. The looser, primary and stricter cohorts are
frozen (D-039) and must be propagated.
**If an alternative were chosen.** Looser: +12 curves, mostly weakly sampled, which WP3 would have to fit and report as failures if they
fail. Stricter: −110 curves; the median curve has 19 instead of 12 points.

## D-039 — Cohorts carried forward to WP3–WP6
**Status:** APPROVED (CP2) — membership frozen

**CP2 decision (author, 2026-09-13).** Freeze and preserve the looser, primary and stricter cohorts for downstream sensitivity analysis
instead of regenerating them later with changed thresholds; persist the duplicate-selection sensitivity cohort (`alt_keep_rule`) the same way.
**Implementation (when CP2 was finalized).** Explicit files per release, `outputs/wp2/` and `outputs/wp2_sensitivity_eny5v-www93/`:
`cohort_membership.csv` (one row per cohort and curve, with its record IDs and the tags later stages must carry: population step, product
form, reconstituted, irradiated and its label check, geometry class) and `cohort_manifest.csv` (role, definition, counts, and a SHA-256
fingerprint of the cohort's curve IDs with their sorted record IDs). All seven cohorts of both releases are fingerprinted in
`data/FROZEN_COHORTS_CP2.csv`. Every run of `src/wp2_curves.py` ends by comparing the regenerated membership with that file and stops on
any difference (tested: raising the primary ratio limit from 0.20 to 0.21 stops the run, naming four changed cohorts). A frozen cohort
changes only through an approved decision logged here, with the file edited in the same commit.
**Alternative (freeze).** Keep membership only as inventory columns and rely on byte-identical regeneration. **Why not.** Later work
packages need files they can read directly, and a check in the pipeline enforces "do not regenerate with other thresholds" instead of
leaving it as a convention.

**Decision.** Each cohort differs from the primary cohort in one respect, so later stages can attribute any change in results to one
judgement. Membership is stored per curve (`curve_inventory.csv`, columns `cohort_*`), per record (`data/processed/*/charpy_records_with_curves.csv`)
and in the explicit cohort files above.

| cohort | what changes | 2025.30 curves / records | 2024.206 curves / records |
|---|---|---|---|
| primary | — | 170 / 2,588 | 161 / 2,454 |
| looser | inclusion rule | 182 / 2,692 | 172 / 2,544 |
| stricter | inclusion rule | 60 / 1,333 | 54 / 1,235 |
| alt_keep_rule | duplicate keep rule (D-019) | 170 / 2,628 | 161 / 2,494 |
| plus_unresolved_irradiation | population (D-035) | 179 / 2,704 | 170 / 2,570 |
| plus_additively_manufactured | population (D-034) | 175 / 2,654 | 166 / 2,520 |
| piping_secondary | SA508 Gr.1A only (secondary group) | 15 / 181 | 15 / 181 |

The 2024.206 column is the version-sensitivity case. For refs 1–106 both releases give the same curves; only descriptive labels
(treatment, orientation, irradiation of excluded series) differ (`outputs/wp2/version_sensitivity_comparison.md`).
**Alternatives.** Carry only the primary cohort; combine several changes per cohort.
**Why.** The brief requires quantifying how the inclusion rule changes the headline result. One change per cohort keeps each effect
attributable.

---

# WP3 — Transition curve fitting

All numbers regenerate with `src/wp3_validation.py` (synthetic curves only) and `src/wp3_fit_curves.py` (published data) into
`outputs/wp3/`. Both call the same fitter, `src/wp3_fitter.py`. Synthetic results live only in files named `synthetic_*` and carry a
`data_type` column saying SYNTHETIC. **Status legend for this section:** `PROPOSED (CP3)` = decided in WP3, awaiting the author at CP3.
`PRE-REGISTERED` = written and committed before the results it governs existed (the commit is named in D-051).

**Sources cited in WP3** (what was actually read is stated; nothing below is cited from memory)
- [Marini2020] Marini B. (2020). *Empirical estimation of uncertainties of Charpy impact testing transition temperatures for an RPV steel.*
  EPJ Nuclear Sci. Technol. 6:57, doi:10.1051/epjn/2020019 (full text, open-access copy HAL hal-02999694): Eq. 1, §1, §3.1–3.2, Tables 2–7.
- [Switzner2023] Switzner N.T., Anderson J., Ahmed L.A., Rosenfeld M., Veloo P. (2023). *Algorithms to Estimate the Ductile to Brittle
  Transition Temperature, Upper Shelf Energy, and Their Uncertainties for Steel Using Charpy V-Notch Shear Area and Absorbed Energy Data.*
  Metals 13(5):877, doi:10.3390/met13050877 (full text): Eqs 1–3, 8–10, 22; §2.3–2.7; §4.1, §4.3.
- [WallinBaer2023] Wallin K., Baer W. (2023). *Evaluation of Charpy-V transition curve fitting based on distribution-free statistical
  assessment.* Int. J. Pres. Ves. Pip. 206:105079, doi:10.1016/j.ijpvp.2023.105079. **Abstract only** (BAM repository record, docId
  58635): the full text, including its fitting recommendations, could not be accessed from this environment.
- [Miura2025] Miura N., Shinko T., Nomoto A. (2025). *Variation of ductile-brittle transition temperature for Charpy curve provided by
  hyperbolic tangent function.* Int. J. Pres. Ves. Pip. (ScienceDirect S0308016125000651); preprint SSRN doi:10.2139/ssrn.4917170.
  **Abstract only** (Crossref record of the preprint).
- [SokolovNanstad1995] Sokolov M.A., Nanstad R.K. (1995). *On Impact Testing of Subsize Charpy V-Notch Type Specimens.* ASTM STP 1270
  (ORNL paper CONF-940657-12, OSTI 207586, full scanned text): Eq. 1 and p. 7 (fixed lower shelves), Fig. 1 (specimen types 1–5), Eqs 11, 16–21.
- [NUREG/CR-6379] Sokolov M.A., Alexander D.J. (1997). *An Improved Correlation Procedure for Subsize and Full-Size Charpy Impact Specimen
  Data.* NUREG/CR-6379, ORNL-6888 (OSTI 463630): abstract (same procedure as [SokolovNanstad1995]).
- [Kumar1994] Kumar A.S., Schubert L.E., Cannon N.S., Hamilton M.L. *Effect of neutron irradiation on the impact properties of A533B
  steel* (dataset ref 55; conference report version, OSTI 10191340, full scanned text): Eq. 2, Fig. 1, pp. 2–4.
- [PR-EDB] Wang J.A., Subramani R. (2007). *PR-EDB: Power Reactor Embrittlement Database Version 3.* ORNL/TM-2006/605 (OSTI 932609): §A.4.3.5.
- [10CFR50] 10 CFR Part 50 (eCFR, title 10 issue of 2026-09-09): Appendix G §II.D–E and §IV.A.1.a; §50.61(c)(2)(i)(B)–(C); §50.61a(a).
- [E185-82] (listed above for WP2): §4.15, §4.17, §4.18, §9.2.2.2, §9.2.3, §10.2.1–10.2.4.
- [E2248-18] ASTM E2248-18, *Standard Test Method for Impact Testing of Miniaturized Charpy V-Notch Specimens* (ASTM product page): §1.2, §1.3, §1.5, §5.2.
- [SciPy] SciPy 1.13.1 reference documentation: `scipy.optimize.least_squares` (methods, bounds, `status`, `active_mask`) and
  `scipy.optimize.curve_fit` (`pcov` with a rank-deficient Jacobian).
- Not verified and not used: that US surveillance reports fitted with the CVGRAPH program fix the lower shelf at a stated value. Search
  results point to NRC-hosted Westinghouse reports, but every copy tried refused automated download.

**How the literature maps onto this dataset.** Marini 2020 and Switzner et al. 2023 each fit one well-characterized steel with a designed
test matrix; this cohort is 170 curves digitized from 47 publications, with shelves sampled unevenly, several specimen geometries, no
shear-fracture or lateral-expansion data (WP0 data dictionary) and no replicate structure. So (i) Switzner's two- and one-parameter
algorithms, which borrow T0 and C from a shear-area fit, cannot be used; (ii) a fixed lower shelf taken from one steel or one specimen
family cannot be assumed to transfer; (iii) a fit that converges is not evidence that the curve's sampling identifies its parameters, which
is the WP3 question itself (brief §5 note).

## D-040 — Model and parameterization
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision.** E(T) = LSE + (USE − LSE)/2 · [1 + tanh((T − T0)/C)]. LSE and USE are the lower- and upper-shelf absorbed energies (J), T0 the
mid-transition temperature (°C), C the half-width (°C): between T0 − C and T0 + C the curve climbs from 11.9 % to 88.1 % of (USE − LSE), the
interval D-037's screening band was modelled on. Equivalent to E = A + B·tanh((T − D)/C) with A = (USE + LSE)/2, B = (USE − LSE)/2, D = T0
([Switzner2023] Eqs 1–3; [SokolovNanstad1995] Eq. 1; [Kumar1994] Eq. 2 writes c = 1/C and d = T0; [Marini2020] Eq. 1 is the special case LSE = 0).
The solver works on (LSE, RISE = USE − LSE, T0, C), so that simple box bounds (RISE ≥ 0, C > 0) keep USE ≥ LSE and the curve rising.
**Alternatives.** Asymmetric sigmoids (Burr-type, exponential lower part), which [WallinBaer2023]'s abstract reports as better for large data
sets; fitting temperature as a function of energy. **Why not.** The brief fixes the tanh family; the author must be able to explain the model;
the Wallin & Baer recommendations could not be read. **Consequence.** A symmetric tanh cannot represent an asymmetric transition or a falling
upper shelf; misfit of that kind is diagnosed (D-043, D-047), not removed.

## D-041 — Optimizer, starting values, bounds and weighting
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision.**
- *Method.* `scipy.optimize.least_squares`, method `trf` (trust-region reflective: SciPy's method for box bounds [SciPy]), analytic Jacobian,
  energies scaled by the curve's highest energy and temperatures by half its tested span, tolerances ftol = xtol = gtol = 1e-10,
  at most 2,000 function evaluations per start. Not `curve_fit`: it wraps the same solver but hides the status and bound-activity
  information, and with bounds it silently returns a pseudo-inverse covariance when the Jacobian is rank-deficient [SciPy]. Levenberg-
  Marquardt (`nlsLM` in [Switzner2023], IMSL ZSSQ in [PR-EDB]) does not handle bounds.
- *Weighting.* Ordinary, unweighted least squares on absorbed energy, as in [Marini2020], [Switzner2023], [SokolovNanstad1995], [Kumar1994].
  Charpy scatter is not constant along the curve ([Marini2020] §3.1), but a weighting scheme needs a scatter model, which belongs to WP4.
- *Starts.* Six, fixed in advance: LSE = lowest measured energy (or the fixed value); USE = mean of the three highest energies (D-037's
  screening upper reference, used only as a starting value, never as the estimate); T0 ∈ {temperature at which the per-temperature mean energy
  first crosses the midpoint of those two, lower quartile, upper quartile of the distinct test temperatures}; C ∈ {span/12, span/4}. The
  solution is the lowest residual sum of squares among starts that report convergence (status > 0) with finite values (ties: earliest start).
  Every start is recorded. Six starts separate a solver failure from an unlucky start; they are not a search for a convenient answer.
- *Bounds* (physical unless stated): LSE ≥ 0 J; USE − LSE ≥ 0; T0 ≥ −273.15 °C. Numerical safety, deliberately wide so that resting on one
  means the data did not constrain the parameter: C ≥ 1 °C (below the 2 °C test-temperature resolution of D-037); C ≤ tested span; T0 within
  one span of the tested temperatures; USE − LSE ≤ 10 × highest measured energy; LSE ≤ highest measured energy. "On a bound" = SciPy reports
  the bound active, or the scaled parameter is within 0.1 % of the bound interval.
- *Environment.* SciPy 1.13.1 added to `requirements.txt` (the last SciPy release that supports the project's Python 3.9; built for NumPy 2).
**Alternatives.** Unbounded fitting with post-hoc checks; soft penalties that pull shelves towards initial estimates ([PR-EDB] §A.4.3.5 does
this "to avoid unphysical fits"); many random starts. **Why not.** Unbounded fits can swap the two shelves (a negative C describes the same
curve), penalties quietly replace data with starting guesses, and random multistart is neither transparent nor needed for four parameters.

## D-042 — Lower shelf: fixed or fitted
**Status:** OPEN at pre-registration: the candidates, evidence and decision rule below were committed before any synthetic result existed.
**Evidence from the literature.** [Marini2020] fits LSE = 0 (three parameters) for a 16MND5 forging. [SokolovNanstad1995] (ORNL, NRC HSSI
programme) fixed the lower shelf at 2.7 J for every full-size fit and 0.1 J for every sub-size fit (p. 7). [Switzner2023] fits all four
parameters without constraints; its free shear-area curve went below 0 % shear, "physically impossible" (§3.1), and four-parameter fits can fail to converge (§4.1).
[PR-EDB] restrains both shelves with penalties to avoid unphysical fits. [Miura2025]'s abstract makes the scatter of T41J depend on LSE and on
the number of lower- and upper-shelf points. No source gives a lower shelf for 1.5–5 mm miniature specimens of 20–27.5 mm length.
**Pre-fit evidence from this cohort (WP2 descriptors only; no fit).** Full-size curves whose coldest test is at or below −150 °C have a median
lowest energy of 5.2 J (quartiles 3.7–7.8 J; 41 curves), above 2.7 J; 17 of 134 full-size curves have measured energies below 2.7 J. Among the
36 miniature curves, 4 have energies below 0.1 J (20 × 1.5 × 1.5 mm, 27.5 × 3.33 × 3.33 mm) and 23 have lowest energies above 0.3 J (KLST-type
27 × 3 × 4 mm curves reach 0.5–1.2 J). No single sourced fixed value is consistent with all geometries in the cohort.
**Candidates.** (1) `fitted`: LSE is a free parameter, bounded below by 0 J. (2) `fixed_convention`: 2.7 J full-size, 0.1 J miniature
[SokolovNanstad1995]. (3) `fixed_zero`: LSE = 0 [Marini2020]. (4) `hybrid`: fitted when the curve has at least two distinct temperatures in
D-037's lower screening band (a pre-fit count), otherwise the convention of (2).
**Decision rule (pre-registered; `choose_lse_strategy` in `src/wp3_validation.py`).** Synthetic Block L: 3 full-size truths (LSE 2, 5, 10 J;
USE 150 J; C 30 °C) and 6 miniature-scale truths (USE 1 or 8 J; LSE 1 %, 6 %, 12 % of USE) × 5 designs (lower shelf well sampled, weak,
missing, and a 250 °C / 12-specimen window with T0 60 °C above or below its centre) × low, moderate, high scatter × 200 replicates, each
strategy fitted to identical synthetic data. Key temperature: T41J from the analytic crossing (full-size) or T0 (miniature). Score = mean over
data sets of the 90th percentile of |error|. (1) Eligible: mean share of replicates without a key temperature (solver failure or criterion not
crossed) within 5 percentage points of the lowest. (2) The lowest score wins if at least 10 % below every other eligible score. (3) Otherwise
`fitted` if within 10 % of the lowest score, else the lowest score. Rule 3 prefers not imposing a value because of the pre-fit evidence above.
Real-data fit counts play no part.

## D-043 — Upper-shelf energy
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision.** USE is the fitted upper asymptote of the tanh (LSE + RISE), as in [Switzner2023] Eq. 10 and [Kumar1994] (USE = a + b). It is
never the WP2 screening upper reference (D-037). Every fit reports whether the data support it, using the fitted curve (x = (T − T0)/C):
- `use_support` = *supported* if at least 2 specimens were tested at x ≥ 1.5 (where the fitted curve has reached ≥ 95.3 % of its rise),
  *single specimen* if 1, *extrapolated* if 0 — the energy is still rising at the highest test temperature and USE is an asymptote the data
  never reached. The 95 % level mirrors [E185-82] §4.17, which places the upper shelf above 95 % shear; shear data do not exist here.
- *Upper-shelf trend*: for ≥ 3 specimens at ≥ 2 temperatures with x ≥ 1.5, the slope of the residuals against temperature is tested
  (two-sided t-test, p < 0.05). A significant slope means the "shelf" is rising or falling (e.g. ref 104, where energy falls above ~250 °C),
  so a flat asymptote is a compromise.
- *Plateau mean*: mean energy of the specimens at x ≥ 1.5, the closest available analogue of [E185-82] §4.18's definition (average of the
  specimens above the transition). Diagnostic only.
Data are never removed to make a shelf flat.
**Alternatives.** USE = E185-style average of upper-shelf points as the estimate; fixing USE before fitting. **Why not.** Identifying which
points are "above the transition" needs shear data or a fit; averaging would also make USE depend on an extra threshold. Both remain visible
as diagnostics.

## D-044 — Index temperature for standard full-size specimens
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision.** For 55 × 10 × 10 mm Charpy V-notch specimens the index temperature is T41J, the temperature where the fitted curve equals 41 J,
solved analytically: T41J = T0 + C·artanh(2(41 − LSE)/(USE − LSE) − 1).
**Basis.** [10CFR50] Appendix G §II.E: ΔRT_NDT "is evaluated as the difference in the 30 ft-lb (41 J) index temperatures from the average
Charpy curves measured before and after irradiation"; §50.61(c)(2)(i)(B) requires Charpy scatter small enough "to permit the determination of
the 30-foot-pound temperature unambiguously"; [E185-82] §4.15, §9.2.3 and §10.2.1 define the shift at 41 J and require the index temperatures
"from the average curves". [Marini2020] §1 lists 28, 41 and 68 J as the conventional nuclear levels. The 41 J level is a regulatory
correlation index for full-size specimens, not a material constant.
**Not calculated (value left blank, reason recorded)** when 41 J ≤ fitted LSE, 41 J ≥ fitted USE, the fit failed, or the crossing lies outside
the tested temperatures (an extrapolated index is unsupported by data).
**Full-size curves whose notch dimensions are not reported** (74 curves, 993 records): every record is labelled V-notch and 180 cite ASTM E23;
WP1/WP2 classify them as full-size (D-016, D-037). They receive T41J and keep `notch_reported = False`; the CP3 tables count them separately.
**Alternative.** Withhold T41J for them (−74 curves with an index). **Consequence if their notch were non-standard:** a biased T41J for those curves.

## D-045 — Index temperature for non-standard geometries
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Geometries in the frozen primary cohort** (pre-fit, `curve_inventory.csv`): full-size 55 × 10 × 10 mm (134 curves); no E23-type sub-size
specimens (55 mm long, reduced section); 36 reduced-length curves in nine geometries: 20 mm long with 1.5, 2.5, 3.33, 5 mm sections (refs 53,
59), 23.6 mm with 3.33 and 5 mm (refs 52, 55, 59), 27.5 × 3.33 × 3.33 mm (ref 60), and 27 × 3 × 4 mm with a 1 mm, 60°, 0.1 mm-radius notch
(KLST type; refs 107, 109). All reduced-length specimens reduce every dimension, the defining feature of miniaturized (MCVN) specimens in
[E2248-18] §1.2, which §1.5 separates from E23 sub-size specimens.
**Decision.** No index temperature is calculated for miniature (or E23 sub-size) curves; `index_status` records "no defensible criterion
for this geometry". Their T0, C, LSE and USE are still estimated and diagnosed.
**Why.** [E2248-18] §5.2: MCVN transition-region data "are not directly comparable to those obtained from full-size standard Charpy V-notch
specimens and suitable correlation procedures have to be employed"; §1.3 leaves comparison with CVN data to the user. The published
procedures do not give a criterion energy that can be applied here: [SokolovNanstad1995] obtain a subsize T41J only after converting
subsize energies with brittle and ductile normalization factors weighted by *percent shear* (Eq. 11; factors fitted for their four specimen
types), then shift temperatures by 30–53 °C with ±2σ bands of 20–30 °C (Eqs 17–20); this dataset has no shear data and different
lengths and notches. [Kumar1994] define DBTT as the tanh midpoint and review constant-offset correlations whose scatter bands were 25–65 °C.
The correlations listed in the dataset's descriptor (Table 3) correlate transition temperatures between sizes with material- and
condition-specific constants; they are WP5 size corrections, not index criteria. Multiplying 41 J by a volume or ligament ratio is not
supported by any of these sources.
**Alternatives.** 41 J × a normalization factor; a relative criterion such as 50 % of USE ([E185-82] §10.2.4 lists it as an optional
full-size index). **Consequence.** 36 miniature curves have T0 (a model parameter with the same definition at every size) but no index
temperature; comparing them with full-size index temperatures is WP5's job, with its uncertainty.

## D-046 — Failure categories and the mutually exclusive outcome
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision (`classify` in `src/wp3_fitter.py`).** Flags may overlap; each curve also gets exactly one outcome, the first that applies:
1. *Optimizer failure* — no start returned a converged, finite solution.
2. *Non-physical* — the best tanh would need a physically impossible parameter, so the solution rests on a physical bound: fitted LSE at
   0 J (a negative lower shelf wanted), USE − LSE at 0 (no rise or a falling curve wanted), or T0 at absolute zero.
3. *Boundary-limited* — a numerical-safety bound is active: C at 1 °C (the rise happens between two test temperatures, width unresolved),
   C at the tested span, T0 at a range limit, USE − LSE at 10 × the highest energy, or fitted LSE at the highest energy.
4. *Weakly identified* — converged, inside its bounds, but the sampling does not constrain a parameter (D-047).
5. *Usable fit, index temperature unavailable* — reason recorded: no defensible criterion (D-045), criterion not crossed, or crossing
   outside the tested range (D-044).
6. *Usable fit, index temperature calculated.*
Nothing is dropped: every curve has a row with its outcome, flags, bounds, starts and solver messages. Unlike [PR-EDB] §A.4.3.5, whose Monte
Carlo "eliminated" nonphysical results, failures are counted.

## D-047 — Identifiability diagnostics
**Status:** PROPOSED (CP3); PRE-REGISTERED (their usefulness is tested in the synthetic validation, not assumed)
**Decision.** Defined on the fitted curve, with x = (T − T0)/C and distinct temperatures as in D-037:
- *weak transition*: fewer than 2 distinct test temperatures with −1 < x < 1 (inside the 11.9–88.1 % part of the rise). With one or none,
  location and width cannot both be measured — the brief's ill-conditioning case.
- *weak upper shelf*: `use_support` is not *supported*, or the upper-shelf residual trend is significant (D-043).
- *weak lower shelf* (only when LSE is fitted): fewer than 2 specimens at x ≤ −1.5.
- *numerically singular*: the Jacobian at the solution has rank below the number of parameters (NumPy's default rank tolerance).
The x-limits come from the tanh shape (±1: characteristic interval; ±1.5: within 4.7 % of a shelf); the counts of 2 are the smallest that
measure a level or a width twice. No condition-number threshold is imposed. The condition number of the scaled Jacobian and the spread of T0
among starts within 1 % of the best cost are recorded for audit; the synthetic validation reports how they relate to the true error.

## D-048 — Synthetic validation design
**Status:** PROPOSED (CP3); PRE-REGISTERED
**Decision (`src/wp3_validation.py`).** Synthetic curves from known tanh parameters; fixed seed 20260913, one seed per synthetic data set
(so results do not depend on run order or worker count; lower-shelf strategies see identical data). Controlled, uncalibrated scatter —
not the WP4 scatter model: Gaussian with standard deviation sd(T) = σ_T·|dE/dT| + cv·E(T) + 3·cv·LSE, levels zero (0, 0), low (2 °C, 0.03),
moderate (5 °C, 0.06), high (10 °C, 0.12). The first term peaks at mid-transition, where [Marini2020] §3.1 reports the largest scatter; the
last term stops lower-shelf energies being implausibly precise. Draws below 0 J are set to 0 J and counted.
Blocks: L (lower-shelf strategies, D-042); A (sampling density: n = 6, 8, 12, 18, 30 uniformly over x = −3…3); B (patterns: shelves with 0–3
transition points; lower or upper shelf weak or missing; clustered at the centre; clustered on the cold side; five temperatures × three
specimens); C (USE 44, 70, 250 J; LSE 2, 10 J; C 12, 60 °C); D (fixed windows of 9/150 °C, 12/250 °C, 24/360 °C — the 10th percentile,
median and 90th percentile of points and span of the full-size primary-cohort curves — with the true T0 at −60, 0, +60 °C from the window centre and C 12,
30, 60 °C). 200 replicates per noisy scenario, 1 at zero noise. Designs expected to fail are included on purpose.
**Reference scales (summaries only, not acceptance criteria).** 10 °C for T41J and T0 — about the 17 °F (9.4 °C) limit on the scatter of
ΔRT_NDT for base metal in [10CFR50] §50.61(c)(2)(i)(C); 10 % for USE; 25 % for C.
