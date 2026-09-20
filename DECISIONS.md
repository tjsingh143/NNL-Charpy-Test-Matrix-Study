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
`outputs/wp3/` (the all-fitted sensitivity case into `outputs/wp3/sensitivity_all_fitted_lse/`). Both call the same fitter,
`src/wp3_fitter.py`. Synthetic results live only in files named `synthetic_*` and carry a `data_type` column saying SYNTHETIC.
**Status legend for this section:** `PRE-REGISTERED` = written and committed before the results it governs existed (the commit is named in
D-051). `PROPOSED (CP3)` = the status of every WP3 entry when CP3 was first presented (commit `20481dd`). `APPROVED IN PRINCIPLE (CP3)` =
approved by the author at the CP3 review (2026-09-14); final CP3 approval follows the author's review of the amended results.
`AMENDED (CP3)` = changed by the author's CP3 decision; the entry keeps its earlier text, rule and outcome as history.
`FINAL APPROVED (CP3)` = approved by the author at final CP3 approval (2026-09-14), after reviewing the amended results; the earlier statuses
follow it as history.

**CP3 review record (author, 2026-09-14).** WP3 is approved in principle; the final primary fitting method is amended before CP3 is
finally approved and `wp3` is merged. Each item is recorded in full in the entry named.
1. D-040 model form: approved; the symmetric tanh's limitation stays explicit.
2. D-041 optimizer: approved; starts and bounds are not tuned on individual published curves.
3. D-042 lower shelf: **amended.** Final primary method: full-size LSE fixed at 2.7 J; miniature LSE fitted, >= 0 J; no universal 0.1 J
   miniature shelf. The pre-registered all-fitted rule, its outcome, the weighting issue and the reason for the change are preserved; the
   all-fitted method stays as an explicit sensitivity case; the choice is not re-made on the new published-data counts.
4. D-046 zero-LSE classification: **amended.** A fitted LSE at its 0 J bound is a boundary-limited fit (`flag_lse_at_lower_bound`), not
   a non-physical one; "non-physical" is reserved for inadmissible parameter relationships.
5. D-043 upper shelf: approved; the trend flag stays a model-adequacy warning, with its classification history.
6. D-044 full-size T41J: approved with a metadata caveat (74 exact-notch-unreported curves keep T41J, flagged and described as
   "full-size V-notch, exact notch dimensions unreported"; notch-metadata sensitivity; separate index-support diagnostic, value never withheld).
7. D-045 miniature index: approved; no 41 J-equivalent, no volume-scaled 41 J, no universal miniature criterion.
8. D-047 identifiability flags: approved subject to item 4; no new condition-number cutoff; the documented weaknesses stay.
9. D-048 synthetic validation: approved; its history is preserved; outputs rerun for the final method without redesign or new scenarios;
   the all-fitted results stay recoverable.
10. D-049 dataset values: approved as a diagnostic only.
11. D-050 cohorts: approved; the CP2 memberships stay frozen.
12. D-051 method history: approved and extended with this amendment.
Not authorized by this review: WP4, merging `wp3` into `main`, bootstrap estimates of real-data uncertainty.

**CP3 final approval record (author, 2026-09-14).** The author reviewed the amended results and gave final CP3 approval; `wp3` is merged into
`main` once the one clarification below is implemented and verified. Each item is recorded in full in the entry named.
1. D-040 model: FINAL APPROVED; the symmetric tanh stays, with its empirical-model limitation explicit.
2. D-041 optimizer: FINAL APPROVED; deterministic bounded `least_squares`, analytic Jacobian, deterministic starts, wide safety bounds, audit
   information and the current weighting; not tuned per published curve.
3. D-042 lower shelf: FINAL APPROVED AS AMENDED AT CP3; full-size LSE fixed at 2.7 J, miniature LSE fitted with a 0 J lower bound; the
   all-fitted approach stays a named sensitivity and history case, and its chronology stays as recorded.
4. D-043 upper shelf: FINAL APPROVED; USE = fitted asymptote with support diagnostics; a non-flat shelf trend stays a model-adequacy warning.
5. D-044 full-size T41J: FINAL APPROVED WITH ONE ADDITIONAL SUPPORT DIAGNOSTIC, the empirical bracketing of 41 J by the measured energies
   (`criterion_bracketed_by_measured_energy`; warning "T41J calculated from fitted curve; 41 J not empirically bracketed by measured
   energies."). A project support diagnostic, not an ASTM requirement; values are kept; no frozen WP2 cohort or fit outcome changes. The
   index-position warning stays; the two are reported separately. Triggered by curve 33-153, which is not tuned.
6. D-045 miniature index: FINAL APPROVED; no invented criterion; any cross-size or index correlation is WP5 work.
7. D-046 outcomes: FINAL APPROVED AS AMENDED; zero-LSE miniature fits are boundary-limited, "non-physical" is reserved for inadmissible
   solutions, and the empirical-bracketing diagnostic is a support warning, never an outcome.
8. D-047 identifiability diagnostics: FINAL APPROVED subject to the D-046 terminology; the empirical-bracketing flag is an index-support
   diagnostic, not a fitter-identifiability outcome; no condition-number threshold.
9. D-048 synthetic validation: FINAL APPROVED; not redesigned; no scenario added for the diagnostic-only change; history intact.
10. D-049 dataset values: FINAL APPROVED as a diagnostic only; nothing is fitted toward the dataset's undocumented values.
11. D-050 cohorts: FINAL APPROVED; frozen memberships unchanged.
12. D-051 method history: FINAL APPROVED and extended with step 6 (this clarification).
WP4 (per-curve uncertainty) is the next permitted work package and has not started; this approval session did not include WP4 work,
bootstrap uncertainty, a scatter model or WP5.

**Sources cited in WP3** (what was actually read is stated; nothing below is cited from memory)
- [Marini2020] Marini B. (2020). *Empirical estimation of uncertainties of Charpy impact testing transition temperatures for an RPV steel.*
  EPJ Nuclear Sci. Technol. 6:57, doi:10.1051/epjn/2020019 (full text, open-access copy HAL hal-02999694): Eq. 1, §1, §3.1–3.2, Tables 2–7.
- [Switzner2023] Switzner N.T., Anderson J., Ahmed L.A., Rosenfeld M., Veloo P. (2023). *Algorithms to Estimate the Ductile to Brittle
  Transition Temperature, Upper Shelf Energy, and Their Uncertainties for Steel Using Charpy V-Notch Shear Area and Absorbed Energy Data.*
  Metals 13(5):877, doi:10.3390/met13050877 (full text): Eqs 1–3, 8–10, 22; §2.3–2.7; §4.1, §4.3.
- [WallinBaer2023] Wallin K., Baer W. (2023). *Evaluation of Charpy-V transition curve fitting based on distribution-free statistical
  assessment.* Int. J. Pres. Ves. Pip. 206:105079, doi:10.1016/j.ijpvp.2023.105079. **Abstract only** (BAM repository record, docId
  58635): the full text, including its fitting recommendations, could not be accessed from this environment.
  *Citation check (2026-09-14, when the author's CP3 decision cited this paper).* The abstract shown by that record was re-read. Its six
  sentences describe a non-parametric, distribution-free assessment of five large Charpy transition-curve data sets used to find optimum
  fitting equations for smaller data sets, an improvement of that assessment method, its unsuitability as a standard method, and state that
  "several recommendations for transition curve fitting can be made". It does not mention the lower shelf, a fixed shelf value, the tanh or
  asymmetric curves; the record marks the full text "Closed Access". So (i) the author's CP3 statement that Wallin & Baer explain why a
  realistic fixed lower shelf is appropriate when lower-shelf information is inadequate is recorded as the author's basis and could not be
  verified from what this repository can read (D-042), and (ii) the earlier statements in D-040 and D-042 attributing to *the abstract* a
  finding that asymmetric sigmoids fit large data sets better are not supported by the abstract text; they are left in place and marked.
- [Miura2025] Miura N., Shinko T., Nomoto A. (2025). *Variation of ductile-brittle transition temperature for Charpy curve provided by
  hyperbolic tangent function.* Int. J. Pres. Ves. Pip. (ScienceDirect S0308016125000651); preprint SSRN doi:10.2139/ssrn.4917170.
  **Abstract only** (Crossref record of the preprint). [WP4, 2026-09-14: the full text of the SSRN preprint was read; see WP4 sources.]
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
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); PRE-REGISTERED
**Final CP3 decision (author, 2026-09-14).** Approved: the symmetric hyperbolic-tangent model stays, and its empirical-model limitation stays explicit.
**CP3 decision (author, 2026-09-14).** Approved. The model form and the transparent parameter names LSE, USE, T0 and C are kept. The
symmetric tanh is an empirical model and does not describe every measured Charpy transition curve; that limitation stays explicit
(on the published curves it shows as alternating residual patterns, D-042, `residual_pattern_by_lower_shelf_outcome.csv`).
**Decision.** E(T) = LSE + (USE − LSE)/2 · [1 + tanh((T − T0)/C)]. LSE and USE are the lower- and upper-shelf absorbed energies (J), T0 the
mid-transition temperature (°C), C the half-width (°C): between T0 − C and T0 + C the curve climbs from 11.9 % to 88.1 % of (USE − LSE), the
interval D-037's screening band was modelled on. Equivalent to E = A + B·tanh((T − D)/C) with A = (USE + LSE)/2, B = (USE − LSE)/2, D = T0
([Switzner2023] Eqs 1–3; [SokolovNanstad1995] Eq. 1; [Kumar1994] Eq. 2 writes c = 1/C and d = T0; [Marini2020] Eq. 1 is the special case LSE = 0).
The solver works on (LSE, RISE = USE − LSE, T0, C), so that simple box bounds (RISE ≥ 0, C > 0) keep USE ≥ LSE and the curve rising.
**Alternatives.** Asymmetric sigmoids (Burr-type, exponential lower part), which [WallinBaer2023]'s abstract reports as better for large data
sets [citation check 2026-09-14: not found in the abstract text; see WP3 sources]; fitting temperature as a function of energy. **Why not.** The brief fixes the tanh family; the author must be able to explain the model;
the Wallin & Baer recommendations could not be read. **Consequence.** A symmetric tanh cannot represent an asymmetric transition or a falling
upper shelf; misfit of that kind is diagnosed (D-043, D-047), not removed.

## D-041 — Optimizer, starting values, bounds and weighting
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); PRE-REGISTERED
**Final CP3 decision (author, 2026-09-14).** Approved: deterministic bounded SciPy `least_squares`, analytic Jacobian, deterministic starts, wide
safety bounds, audit information and the current (unweighted) weighting. The optimizer is not tuned per published curve.
**CP3 decision (author, 2026-09-14).** Approved: the deterministic bounded `least_squares` implementation, analytic Jacobian, documented wide
safety bounds, deterministic starts and audit metadata stay. Starts and bounds are not tuned on individual published curves. Where LSE is
fixed (full-size curves under the D-042 amendment) the LSE start and the LSE bounds do not apply; nothing else changes.
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
**Status:** FINAL APPROVED AS AMENDED AT CP3 (author, 2026-09-14). Earlier: AMENDED (CP3) by the author, 2026-09-14 — the final primary method
is geometry-specific. This amendment was made at the CP3 review, after the synthetic and the published-data results existed; it is **not** pre-registered. The pre-registered rule (commit `11daf72`),
its outcome (`fitted` for every geometry, presented at CP3 in commit `20481dd`) and the reasoning presented then are kept below as history, and
the all-fitted method is kept as an explicit sensitivity case.

**Final CP3 decision (author, 2026-09-14).** Approved as amended: full-size LSE fixed at 2.7 J; miniature LSE fitted with a 0 J lower bound; the
original all-fitted approach stays a named sensitivity and history case. The chronology recorded here and in D-051 stands unchanged: the
all-fitted method was the pre-registered rule's outcome; the rule's synthetic weighting issue was found when the Block L results were inspected
and brought to the author at CP3; the author then approved the geometry-specific method on the literature, the full-size T41J estimand and the
synthetic evidence that already existed; it was not chosen by maximizing published-data fit counts.

**CP3 decision (author, 2026-09-14): final primary lower-shelf method.**
- *Full-size 55 × 10 × 10 mm CVN:* LSE fixed at **2.7 J**.
- *Miniature (MCVN):* LSE **fitted**, constrained to LSE >= 0 J. No 0.1 J (or other single) lower shelf is imposed across the nine miniature
  geometries.
- *Sensitivity:* LSE fitted for every geometry (the pre-registered rule's outcome), on synthetic Blocks A–E and on the published curves. The
  choice between the two is not re-made on the new published-data counts.

**The author's reasons (CP3).**
1. *Literature.* [SokolovNanstad1995] (ORNL RPV / subsize Charpy work) fixed the lower shelf at 2.7 J for full-size specimens (p. 7; full
   scanned text read). The author also cites [WallinBaer2023] as explaining that a realistic fixed lower shelf is appropriate when lower-shelf
   information is inadequate. Only that paper's abstract is accessible here and the abstract does not discuss the lower shelf (WP3 sources,
   citation check), so this part of the basis is the author's reading and is not verified in this repository.
2. *Synthetic validation made before the approval* (Block L, SYNTHETIC; `synthetic_lse_strategy_per_dataset.csv`, `wp3_summary.md` §2.1).
   Full-size T41J recovery was better with the 2.7 J convention at every tested scatter level: mean 90th-percentile |T41J error| low 3.64 against
   4.67 °C (fitted), moderate 8.25 against 10.17 °C, high 18.50 against 20.99 °C. Stated precisely: the convention gave the lower value in 13 of 15
   design × scatter cells (exceptions: the window whose cold end lies deep in the lower shelf at low scatter, and the missing lower shelf at high
   scatter) and in 42 of 45 individual full-size data sets.
3. *The pre-registered score's weighting.* The rule gave each synthetic data set equal weight, so its 6 miniature truths outweighed its 3
   full-size truths about 2 : 1, while the frozen primary cohort is 134 full-size : 36 miniature. Weighted by the cohort, the same pre-existing
   Block L results favour the fixed full-size convention (`fixed_convention` 10.70, `fixed_zero` 11.32, `hybrid` 11.79, `fitted` 12.16 °C). This was
   discovered at inspection before CP3 and presented at CP3; the rule itself was never changed.
4. *Estimand.* T41J is the principal full-size RPV index of interest (D-044); with 41 J far above the shelf, a slightly wrong fixed shelf moves
   T41J little, while a free shelf adds variance.
5. *Miniature.* No single defensible fixed lower-shelf value was established for the nine miniature geometries; their observed lower shelves
   vary materially (pre-fit evidence below: 4 curves with energies below 0.1 J, 23 with lowest energies above 0.3 J); imposing one full-size or
   subsize convention on them would add an unsupported assumption. Block L showed a wrong fixed value failing badly when many miniature specimens
   sit on the lower shelf (mean miniature T0 score for the window whose cold end lies deep in the lower shelf: fitted 14.35 °C, fixed 0.1 J 22.21 °C).
The decision rests on the literature, the intended estimand and the synthetic validation. It does not rest on maximizing published-data success
counts; the counts below were produced after the decision and were not used to make it.

**Implementation.** `src/wp3_fitter.py`: `PRIMARY_LSE_STRATEGY = "geometry_specific"`, `SENSITIVITY_LSE_STRATEGY = "fitted"`, and
`lse_setting()` returns 2.7 J for full-size and "fitted" for miniature curves. `src/wp3_validation.py`: the pre-registered rule still runs on Block
L on every run and must still select `fitted` (`PREREGISTERED_RULE_OUTCOME`, named `LOCKED_LSE_STRATEGY` before CP3); the run stops otherwise.
The final method is not a Block L candidate. On identical synthetic data it reproduces exactly the fits of `fixed_convention` for full-size truths
and of `fitted` for miniature truths, so its Block L scores are assembled from those and reported as a descriptive row (`role` column of
`synthetic_lse_strategy_comparison.csv`): pooled score 12.02 °C, full-size 10.13 °C, miniature 12.96 °C, cohort-weighted 10.73 °C, no missing key
temperatures. Blocks A–E are run with both methods on identical synthetic data (D-048). `src/wp3_fit_curves.py` fits the frozen cohorts with the
final method and the primary cohort again with the all-fitted method, which must reproduce the counts presented at CP3 under the pre-CP3
classification (0 / 71 / 3 / 47 / 13 / 36); the run stops otherwise.

**Result of the final method** (published primary cohort; outcomes as amended in D-046; `fit_outcomes.csv`). Optimizer failure 0; non-physical
(inadmissible) 0; boundary-limited 18; weakly identified 35; usable fit without index 13 (miniature); usable fit with T41J 104 (full-size). T41J is
calculated for all 134 full-size curves (132 before; `index_availability_by_geometry.csv`).

**Sensitivity: all fitted against final** (`lse_sensitivity_published.csv`, `lse_sensitivity_published_summary.csv`,
`lse_sensitivity_outcome_changes.csv`, `method_change_before_after.csv`). Miniature fits are identical under both. Full-size, all fitted minus final:
|T41J difference| median 0.29 °C, 90th percentile 1.89 °C, largest 15.4 °C (12-54, whose all-fitted LSE was 37 J; 132 curves with T41J under both);
|T0 difference| median 0.73 °C, 90th percentile 5.34 °C, largest 252.6 °C (49-206, whose upper shelf is never reached); |USE difference| median 0.24 %
(0.45 J), 90th percentile 2.4 % (4.6 J). Only two T41J values move by more than 5 °C (12-54, 49-206), and neither is a usable fit under the final
method. The outcome category differs for 89 of 134 full-size curves and 0 miniature curves (all fitted → final): 43 boundary-limited with LSE at
0 J → usable with T41J; 28 weakly identified by the weak lower shelf alone → usable with T41J; 14 boundary-limited (13 with LSE at 0 J, and 12-49
with C at 1 °C) → weakly identified (13 weak upper shelf, 1 weak transition); 3 usable → weakly identified (weak upper shelf: 11-45, 17-84, 28-133,
T41J moving by less than 1 °C); 1 weakly identified → boundary-limited (49-206). Index
availability differs for 2 curves, both gaining T41J (12-49, whose all-fitted LSE of 81 J lay above 41 J; 33-153, whose all-fitted crossing lay below
the lowest test temperature). These differences are reported, not used to choose.

**What the fixed full-size shelf cannot show, and what was found in the amended run (reported; nothing was tuned).**
- With LSE fixed, a full-size fit cannot trigger the lower-shelf diagnostics (LSE at bound, weak lower shelf). Part of the fall in flagged curves is
  therefore mechanical: in the primary cohort, curves with one WP2 lower-band temperature were 10 % usable under the all-fitted method (3 of 31) and are
  68 % usable under the final method (21 of 31; `fit_outcomes_by_group.csv`). Lower-shelf misfit of full-size curves is not flagged; its effect on T41J,
  T0 and USE is what the all-fitted comparison measures.
- SYNTHETIC: where the full-size lower shelf is not sampled, the diagnostics no longer decline. For the "lower shelf missing" design (Block B) usable fits
  rise from 0–8 % (all fitted) to 80–100 % (final); most of them report no T41J because the crossing lies below the tested range (D-044), and those that do
  report one had a 90th-percentile error of 4.3 / 8.4 / 15.1 °C at low / moderate / high scatter. In the 150 °C window with the true T0 60 °C below its
  centre, 99 % (C 30 °C) and 82 % (C 60 °C) of fits pass the flags; 80 and 2 of 200 report T41J, with 90th-percentile errors of 12.5 and 24.1 °C
  (`wp3_summary.md` §2.3, §2.5, §2.8). A mis-specified fixed shelf also biases noise-free fits slightly (Block A, true LSE 5 J, no scatter: T41J 0.4 °C,
  T0 0.5–0.7 °C, C 4–5 %; exact recovery under the all-fitted method).
- Published curve 33-153 receives a usable-fit T41J (−114.5 °C, 5.6 °C above its lowest test temperature) although none of its 7 measured energies is
  below 41 J (lowest 42.8 J): the crossing rests on the fixed 2.7 J shelf rather than on a measurement below 41 J. It is the only such curve; 11 more have
  exactly one measured energy below 41 J. The existing index-support diagnostic (D-044) does not flag it. Audit columns `n_points_below_criterion` and
  `n_points_above_criterion` were added to expose this; no rule is attached (on SYNTHETIC Blocks A–D, the 78 usable T41J fits without a specimen below
  41 J had a 90th-percentile error of 5.5 °C against 8.5 °C for the rest, with true lower shelves of 2–10 J). Whether this should become part of the
  index-support diagnostic is for the author. [Final CP3 approval, 2026-09-14: the author added a separate empirical-bracketing support diagnostic
  instead of extending the index-position warning; 33-153 now carries its warning; its fit, T41J and outcome are unchanged (D-044, D-051 step 6).]
- Published curve 49-206 (upper shelf never reached): with the lower shelf fixed, the fit moves to USE − LSE at 10 × the highest energy and T0 at its
  range limit (boundary-limited); its T41J is still calculated (index-support warning: 41 J at 3 % of the fitted rise).

**History — D-042 as presented at CP3 (status then: PROPOSED (CP3), decided by the pre-registered rule on synthetic Block L before any published
curve was fitted; "the rule's outcome is sensitive to how its score weights the two specimen scales; that sensitivity is put to the author at CP3").**

**Decision (as presented at CP3).** The lower-shelf energy is a fitted parameter (bounded below by 0 J) for every curve and every geometry.

**Block L result** (`outputs/wp3/synthetic_lse_strategy_comparison.csv`, `synthetic_lse_strategy_per_dataset.csv`; SYNTHETIC). Score = mean
over the 135 synthetic data sets of the 90th-percentile |key-temperature error| (°C): `fitted` 12.62, `fixed_convention` 11.93, `fixed_zero`
14.60, `hybrid` 12.06. Share of replicates without a key temperature: 1.8 %, 0, 0, 1.0 %. All four eligible; the lowest score (11.93) is not
10 % below `hybrid` (12.06); `fitted` is within 10 % of the lowest → rule 3 → `fitted`.

**What the pooled score hides (reported; not used to change the rule).**
- *Full-size T41J favours a fixed shelf in every design and at every scatter level.* [CP3 correction, 2026-09-14: true of the three scatter-level
  averages below; in 13 of 15 design × scatter cells and 42 of 45 data sets, not in every design; see the CP3 decision above.] Full-size scores: `fixed_zero` 9.80, `fixed_convention`
  10.13, `hybrid` 11.66, `fitted` 11.94 °C; by scatter level `fitted` vs `fixed_convention`: low 4.67 vs 3.64, moderate 10.17 vs 8.25, high
  20.99 vs 18.50 °C. With 41 J far above the shelf, a wrong fixed LSE shifts T41J little, while a free LSE adds variance.
- *Miniature-scale T0 favours fitting.* Miniature scores: `hybrid` 12.27, `fixed_convention` 12.83, `fitted` 12.96, `fixed_zero` 17.00 °C.
  A wrong fixed value fails badly when many specimens sit on the lower shelf: for the test window whose cold end lies deep in the lower
  shelf, the miniature score (all six miniature truths) was 14.35 °C `fitted` against 22.21 (`fixed_convention`) and 43.12 °C
  (`fixed_zero`); for LSE = 12 % of USE, USE 8 J and moderate scatter, 14.6 °C fitted against 52.8 °C (fixed 0.1 J) and 81.6 °C (fixed 0 J). The cohort's KLST-type curves (lowest energies
  0.5–1.2 J, 6–14 % of the screening upper reference) resemble this case.
- *Lower shelf missing* (coldest test at x = −0.5): a fitted LSE can land above 41 J, so T41J is undefined in up to 32 % (moderate) and 44 %
  (high scatter) of full-size replicates; this design accounts for 96 % of the fitted strategy's missing key temperatures. There the true
  T41J lies below the lowest test temperature, so no strategy's T41J would be reported as supported (D-044).
- *Weighting sensitivity of the rule itself.* The score gives equal weight to each synthetic data set: 6 miniature truths against 3 full-size
  truths, so miniature results carry two thirds of the weight, although 134 of the 170 primary curves are full-size. That weighting was not a
  deliberate choice. Weighting the two scale groups 134 : 36 instead gives `fixed_convention` 10.70, `fixed_zero` 11.32, `hybrid` 11.79,
  `fitted` 12.16 °C, and the same rule would then select `fixed_convention`. The pre-registered outcome is kept, because rewriting a
  pre-registered rule after seeing its result is exactly what pre-registration exists to prevent.

**Why `fitted` is acceptable, and what argues against it.** For: no externally imposed number; no sourced fixed value is consistent with
every geometry in the cohort (pre-fit evidence above); one method for all geometries keeps a method difference out of WP5's size
comparison; a poorly determined fitted shelf is visible (weak-lower-shelf and non-physical flags, undefined index) rather than a hidden bias.
Against: for full-size T41J — the project's index — the synthetic 90th-percentile error was about 15–20 % larger than with LSE fixed at 2.7 J.

**Declared before any published curve was fitted: sensitivity reported at CP3.** The primary cohort is also fitted with `fixed_convention`.
Only the differences in T41J, T0 and USE are reported (`outputs/wp3/lse_sensitivity_published.csv`) [since the CP3 amendment that file holds the
final-versus-all-fitted comparison; the version described here, including the 0.1 J miniature refit, is kept in commit `a2ce7f2`]. Outcome counts under the alternative
are not used to choose, because a fixed shelf mechanically cannot trigger the lower-shelf flags.

**Open for CP3.** Keep `fitted` for all geometries, or approve a geometry-specific choice (LSE fixed at 2.7 J for full-size, fitted for
miniatures); the latter would be recorded as a change made after the synthetic results and before approval.

**What the published curves then showed (method not changed; brought to CP3 as a methodological weakness).** With a fitted lower shelf,
71 of the 170 primary curves (56 full-size, 15 miniature) rest at the 0 J bound — "non-physical" under the pre-CP3 D-046 (boundary-limited since
the CP3 amendment) — against about 10 % of synthetic fits;
105 carry the weak-lower-shelf flag (`outputs/wp3/fit_flags.csv`). This is not a software fault: those curves leave an alternating residual
pattern (full-size: +0.1 % of USE on the fitted lower shelf, −2.8 % in the lower transition, +1.7 % in the middle, −1.5 % in the upper
transition) and a wider fitted transition (median C 51 °C against 41 °C), the signature of a measured transition that rises sharply from a
low shelf and approaches the upper shelf slowly, which a symmetric tanh can imitate only by widening C and lowering LSE
(`residual_pattern_by_lower_shelf_outcome.csv`; compare the abstract of [WallinBaer2023] [citation check 2026-09-14: the abstract does not discuss
  curve shape; see WP3 sources]; since CP3 in `sensitivity_all_fitted_lse/`). The pre-declared refit with LSE fixed at 2.7 J
(full-size) or 0.1 J (miniature) moved full-size T41J by a median 0.29 °C (90th percentile 1.89 °C, largest 15.4 °C) and T0 by a median
0.73 °C (90th percentile 5.3 °C; the largest, 253 °C, is curve 49-206, whose upper shelf is never reached)
(`lse_sensitivity_published_summary.csv`). So the lower-shelf choice barely moves the index temperature of the published curves but does
decide how many of them are classed non-physical. The choice is the author's at CP3; it must not be made on those counts.

**History — pre-registered text (unchanged below).**
**Evidence from the literature.** [Marini2020] fits LSE = 0 (three parameters) for a 16MND5 forging. [SokolovNanstad1995] (ORNL, NRC HSSI
programme) fixed the lower shelf at 2.7 J for every full-size fit and 0.1 J for every sub-size fit (p. 7). [Switzner2023] fits all four
parameters without constraints; its free shear-area curve went below 0 % shear, "physically impossible" (§3.1), and four-parameter fits can fail to converge (§4.1).
[PR-EDB] restrains both shelves with penalties to avoid unphysical fits. [Miura2025]'s abstract makes the scatter of T41J depend on LSE and on
the number of lower- and upper-shelf points. [WP4 citation check 2026-09-14: the abstract does not say this; the full preprint, read in WP4, reports
that the SD of T41J rises with LSE, that more lower-shelf specimens do not reduce it and that more than 2 upper-shelf specimens barely do, the
number of transition specimens dominating (WP4 sources).] No source gives a lower shelf for 1.5–5 mm miniature specimens of 20–27.5 mm length.
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
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); PRE-REGISTERED (the trend flag's
role changed after the synthetic validation and before any published curve was fitted, as recorded below and in D-051)
**Final CP3 decision (author, 2026-09-14).** Approved: USE remains the fitted asymptote; the upper-shelf support diagnostics stay; a non-flat
upper-shelf trend stays a model-adequacy warning, not an outcome failure.
**CP3 decision (author, 2026-09-14).** Approved: USE stays the fitted asymptote, with the upper-shelf support diagnostic; a significant
upper-shelf residual trend stays a model-adequacy warning, not by itself a fit-failure outcome. The history of that classification change is
kept. Under the final method the trend flag fires on 7 primary curves (5 full-size, 2 miniature; 8 under the all-fitted method; `fit_flags.csv`).
**Decision.** USE is the fitted upper asymptote of the tanh (LSE + RISE), as in [Switzner2023] Eq. 10 and [Kumar1994] (USE = a + b). It is
never the WP2 screening upper reference (D-037). Every fit reports whether the data support it, using the fitted curve (x = (T − T0)/C):
- `use_support` = *supported* if at least 2 specimens were tested at x ≥ 1.5 (where the fitted curve has reached ≥ 95.3 % of its rise),
  *single specimen* if 1, *extrapolated* if 0 — the energy is still rising at the highest test temperature and USE is an asymptote the data
  never reached. The 95 % level mirrors [E185-82] §4.17, which places the upper shelf above 95 % shear; shear data do not exist here.
- *Upper-shelf trend*: for ≥ 3 specimens at ≥ 2 temperatures with x ≥ 1.5, the slope of the residuals against temperature is tested
  (two-sided t-test, p < 0.05). A significant slope means the "shelf" is rising or falling (e.g. ref 104, where energy falls above ~250 °C),
  so a flat asymptote is a compromise. **Changed after the synthetic validation (D-051):** the pre-registered version counted this flag
  towards *weakly identified*; it is now a separate model-adequacy flag reported beside the outcome, because on correctly specified
  synthetic curves it fired only at its chance rate and flagged fits were no less accurate (D-047). Its power against genuinely non-flat
  shelves is measured in synthetic Block E.
- *Plateau mean*: mean energy of the specimens at x ≥ 1.5, the closest available analogue of [E185-82] §4.18's definition (average of the
  specimens above the transition). Diagnostic only.
Data are never removed to make a shelf flat.
**Alternatives.** USE = E185-style average of upper-shelf points as the estimate; fixing USE before fitting. **Why not.** Identifying which
points are "above the transition" needs shear data or a fit; averaging would also make USE depend on an extra threshold. Both remain visible
as diagnostics.

## D-044 — Index temperature for standard full-size specimens
**Status:** FINAL APPROVED WITH ONE ADDITIONAL SUPPORT DIAGNOSTIC (CP3, author 2026-09-14): the empirical bracketing of 41 J by the measured
energies. Earlier: APPROVED IN PRINCIPLE WITH A METADATA CAVEAT (CP3, author 2026-09-14); PRE-REGISTERED. Added at the author's CP3 instruction:
the explicit notch-metadata flag and description, the notch-metadata sensitivity summary, and the index-support diagnostic as a flag.

**Final CP3 decision (author, 2026-09-14).** T41J continues to be calculated for full-size V-notch curves from the analytic crossing of the fitted
curve when the existing mathematical requirements are met, including the 74 curves whose exact notch dimensions are unreported (metadata caveat and
notch-metadata sensitivity kept). Added: an independent **empirical-bracketing** diagnostic, defined from the actual measurements:
`criterion_bracketed_by_measured_energy` = min(measured energy) <= 41 J <= max(measured energy), recorded with the numbers of measured energies
below, exactly at and above 41 J. A T41J that is mathematically calculated while the measurements do not bracket 41 J is not deleted; it is
flagged `flag_index_not_bracketed_by_measured_energy`, with the text "T41J calculated from fitted curve; 41 J not empirically bracketed by measured
energies." The diagnostic lets a user tell (A) a fitted crossing supported by observations on both sides of 41 J from (B) a crossing supplied
mainly by the model because the observed energies lie on one side only. It is a **project support diagnostic, not an ASTM requirement**; it does
not change the frozen WP2 cohorts, does not make a fit failed and is not an outcome (D-046); it is an index-support diagnostic, not a
fitter-identifiability diagnostic (D-047). The index-position warning (`flag_index_near_fitted_shelf`) is kept, and the two are reported
separately because they answer different questions: the index position says where 41 J lies on the fitted S-curve; the empirical bracketing says
whether measured energies occur on both sides of 41 J. Curve 33-153 triggered the review; its fit was not tuned.
**Implementation.** `criterion_bracketing()` in `src/wp3_fitter.py`, a pure function of the measured energies, the criterion and the index status,
called in `src/wp3_fit_curves.py::fit_all` after `classify()`; `classify()` is unchanged and never sees the result. New columns in `fits_primary.csv`,
`fits_looser_cohort_curves.csv` and `sensitivity_all_fitted_lse/fits_primary.csv`: `measured_energy_min_j`, `measured_energy_max_j`,
`n_points_at_criterion`, `criterion_bracketed_by_measured_energy`, `flag_index_not_bracketed_by_measured_energy`, `index_empirical_bracketing`
(beside the existing audit columns `n_points_below_criterion` and `n_points_above_criterion`, which it now uses). Reporting:
`t41j_empirical_bracketing_by_curve.csv` (every full-size primary curve), `t41j_empirical_bracketing_summary.csv` (counts and overlaps), a row in
`fit_flags.csv`, `method_change_before_after.csv` and `method_configuration.md`, a column in `index_availability_by_geometry.csv`, and
`wp3_summary.md` §3.2. The synthetic validation is unchanged (D-048).
**Result** (primary cohort, final method; `t41j_empirical_bracketing_summary.csv`). Of the 134 full-size curves with a calculated T41J, 133 are
bracketed by their measured energies and 1 is not: 33-153, a usable fit. Overlaps: none of the 9 T41J values with the index-position warning and
none of the 74 from curves with exact notch dimensions unreported is unbracketed; by outcome, unbracketed / T41J values: boundary-limited 0 / 1,
weakly identified 0 / 29, usable 1 / 104. No calculated T41J lacks a measured energy above 41 J; 11 are bracketed by a single measured energy below
41 J; no measured energy is exactly 41 J. Under the all-fitted sensitivity case 0 of 132 T41J values are unbracketed (33-153 has no T41J there).
**Curve 33-153** (ref 33; A508 forging, unirradiated, full-size V-notch with notch dimensions reported; 7 points from −120.1 to 24.4 °C). T41J
−114.5 °C, 5.6 °C above the lowest test temperature, from a usable fit (LSE fixed at 2.7 J, USE 235.8 J, T0 −77.9 °C, C 44.9 °C). 41 J lies at
16.4 % of the fitted rise, inside 11.9–88.1 %, so the index-position warning does not fire. All 7 measured energies are above 41 J; the lowest,
42.8 J, was measured at the coldest test temperature, −120.1 °C, which is colder than the reported T41J, and the fitted curve gives 33.7 J there.
The crossing is therefore placed by the tanh shape and the fixed 2.7 J lower shelf, not by measurements on both sides of 41 J. With the lower shelf
fitted (sensitivity case) the same data give LSE 31.7 J and a crossing at −123.0 °C, below the lowest test temperature, so no T41J is reported.
The value is retained unchanged and warned.
**Synthetic context** (existing audit rows of `synthetic_flag_check.csv`, Blocks A–D with scatter, final method; no scenario added). Usable T41J
fits with no specimen energy below 41 J: 78 fits, T41J P90 |error| 5.5 °C; with at least one: 10,172 fits, 8.5 °C. Those truths are symmetric tanh
curves with lower shelves of 2–10 J; none has a lower transition that departs from the tanh shape, which is where a crossing without a measurement
below 41 J depends most on the model. The warning records missing empirical support, not a demonstrated loss of accuracy.
**Alternatives.** (1) Withhold an unbracketed T41J. (2) Fold the condition into the index-position warning. (3) Count it towards the fit outcome.
**Why not.** (1) deletes a mathematically defined value that a later analysis can still examine; (2) merges two different questions, which 33-153
shows can disagree; (3) would reclassify a fit because of a support property of its index, contrary to D-046. **If an alternative were chosen.**
(1) or (3): 103 instead of 104 usable-fit T41J values; (2): one merged warning on 10 curves instead of 9, with its two reasons indistinguishable.

**CP3 decision (author, 2026-09-14).** T41J continues to be calculated for full-size 55 × 10 × 10 mm V-notch curves when LSE < 41 J < USE, the
crossing is mathematically defined, and it lies inside the tested temperatures. For the 74 full-size curves whose exact notch dimensions are not
reported, T41J stays in the primary WP3 analysis with an explicit flag; they are described as "full-size V-notch, exact notch dimensions
unreported" and their notch geometry is not described as confirmed ASTM-standard merely because they are full-size V-notch records. The available
evidence supports treating them as full-size V-notch data, but the missing notch depth and radius remain a real provenance limitation. A simple
sensitivity summary shows what remains if these 74 are excluded; it does not redefine the primary cohort. The warning for T41J values lying very
near a fitted shelf is kept: a T41J can be mathematically calculated while still weakly supported, and a separate index-support diagnostic says so
instead of silently withholding the value.

**Implementation.** Per curve (`fits_primary.csv`): `notch_reported` (unchanged), `flag_full_size_notch_dimensions_unreported` and
`geometry_description` ("full-size 55x10x10 mm V-notch, exact notch dimensions unreported" or "..., notch dimensions reported"). As reported in the
records, all 60 notch-reported full-size curves give a 2 mm deep, 45°, 0.25 mm root-radius V-notch, and all 74 others give the V shape with depth,
angle and radius blank (`wp3_summary.md` §3.1); nothing is filled in (D-009). Index-support diagnostic: `flag_index_near_fitted_shelf` = a
calculated T41J with 41 J outside the central 11.9–88.1 % of the fitted rise (x = −1…+1, the interval of D-037 and D-047; it formalizes the
pre-CP3 audit table `index_position_on_fitted_rise.csv` and introduces no new threshold), with `index_support` naming the position; it never
withholds the value and is not part of the outcome (D-046). Audit only, added after the amended fits existed (D-051, D-042): `n_points_below_criterion`
and `n_points_above_criterion`, the measured energies on each side of 41 J. Sensitivity: `t41j_notch_metadata_sensitivity.csv`.

**Result under the final method** (`index_availability_by_geometry.csv`, `index_position_on_fitted_rise.csv`, `t41j_notch_metadata_sensitivity.csv`).
T41J calculated for all 134 full-size primary curves (74 of 74 with exact notch dimensions unreported, 60 of 60 with them reported); 104 of the
134 come from usable fits, 30 from weakly identified (29) or boundary-limited (1) fits. The index-support warning applies to 9 (all with 41 J
below 11.9 % of the rise, mostly high-USE ref 12 A508 forgings: 4-20, 12-49, 12-50, 12-51, 12-53, 12-54, 12-55, 38-168, 49-206); 3 of the 9 are usable
fits. SYNTHETIC check (Blocks A–D, final method): usable fits with the warning had a 90th-percentile |T41J error| of 19.2 °C (37 % beyond 10 °C, 244
fits) against 8.1 °C (6 %, 10,006 fits) without it. One usable-fit T41J (33-153) has no measured energy below 41 J and carries no warning (D-042).
[Final CP3 approval, 2026-09-14: it now carries the separate empirical-bracketing warning; see the final decision above.]
*Notch-metadata sensitivity:* excluding the 74 exact-notch-unreported curves leaves 60 full-size curves (1,066 records), all with T41J; 46 with a
usable-fit T41J (104 with them), 43 of those without the index-support warning (101), 22 in the stricter cohort (33) and 10 irradiated (14). The
median usable-fit T41J is −27 °C for the 60 notch-reported curves and −69 °C for the 74 others (−53 °C together); the two groups differ in material
and source as well as in notch metadata, so the difference is not attributed to the notch.

**History — decision text as pre-registered and presented at CP3.**
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
**Result as presented at CP3** (all-fitted method; `outputs/wp3/index_availability_by_geometry.csv` then, regenerable from
`sensitivity_all_fitted_lse/fits_primary.csv`): T41J calculated for 132 of 134 full-size primary curves (74 of 74 without,
58 of 60 with a reported notch); not calculated for 2 (41 J at or below the fitted LSE, 1; crossing below the lowest test temperature, 1).
Of the 132, 36 come from fits with no flag. For 15 of the 132, 41 J lies on the flat lower part of the fitted curve (below 11.9 % of the
rise), 9 of them in fits with no flag (`index_position_on_fitted_rise.csv`); their T41J is poorly anchored even when every flag passes.

## D-045 — Index temperature for non-standard geometries
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); PRE-REGISTERED
**Final CP3 decision (author, 2026-09-14).** Approved: no invented miniature T41J-equivalent criterion; miniature curves receive LSE, USE, T0 and C
where defensible; any cross-size or index correlation remains WP5 work.
**CP3 decision (author, 2026-09-14).** Approved. No 41 J-equivalent criterion is invented for miniature specimens, 41 J is not
volume-scaled, and no universal miniature energy criterion is introduced. Miniature curves report LSE, USE, T0 and C where defensible and no
geometry-normalized index temperature, unless a later WP5 correlation establishes one. [E2248-18]'s warning that miniature transition data are
not directly comparable with full-size CVN data remains a core limitation. **Result under the final method** (miniature LSE is fitted, so the
miniature fits are identical to those presented at CP3): 13 of 36 miniature curves are usable fits (T0, C, LSE and USE reported); 17 are
boundary-limited (15 with the fitted LSE at its 0 J bound, 2 with C at 1 °C; the 15 were classed non-physical before the D-046 amendment);
6 are weakly identified; no index temperature for any of the 36 (`fit_outcomes.csv`, `index_availability_by_geometry.csv`).
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
temperature; comparing them with full-size index temperatures is WP5's job, with its uncertainty. **Result:** index temperature not
calculated for all 36 miniature curves (9 geometries); 13 of them are fits with no flag.

## D-046 — Failure categories and the mutually exclusive outcome
**Status:** FINAL APPROVED AS AMENDED (CP3, author 2026-09-14). Earlier: AMENDED (CP3) by the author, 2026-09-14 — zero-LSE classification and
terminology. The pre-registered version (below) is kept as history; it produced the counts presented at CP3.

**Final CP3 decision (author, 2026-09-14).** Approved as amended: zero-LSE miniature fits stay boundary-limited (support-limited) rather than
automatically non-physical; "non-physical" stays reserved for truly inadmissible solutions. The empirical-bracketing diagnostic of D-044 is a
support warning reported beside the outcome, like the index-position warning, and never a mutually exclusive outcome: it is computed after
`classify()`, which is unchanged. Checked when it was added: the outcome of every curve in the primary cohort, the looser cohort and the all-fitted
sensitivity case is identical before and after; primary counts 0 / 0 / 18 / 35 / 13 / 104 (170).

**CP3 decision (author, 2026-09-14).** A fitted LSE landing at its 0 J lower bound does not by itself make a curve's outcome "non-physical".
It keeps an explicit diagnostic, `flag_lse_at_lower_bound`, and the fit is classed *boundary-limited* (lower-shelf-bound-limited) when that is
the controlling issue; weak-lower-shelf and model-adequacy diagnostics are kept separately where they apply. Interpretation: *the constrained
fit wants the lower asymptote at its allowed lower boundary, indicating that the lower shelf is not independently supported or that the
symmetric tanh is compensating for curve-shape mismatch.* That is different from saying the measured curve is physically impossible: the
measured energies are physical, and a 0 J lower shelf is itself an admissible value ([Marini2020] fixes it). "Non-physical" is reserved for
genuinely inadmissible parameter relationships, or failures that remain physically impossible after the constraints. No measured value is changed.

**Decision as amended (`classify` and `OUTCOME_FLAG_GROUPS` in `src/wp3_fitter.py`).** Flags may overlap; each curve gets exactly one outcome,
the first that applies:
1. *Optimizer failure* — no start returned a converged, finite solution.
2. *Non-physical (inadmissible)* — even the constrained best fit has no admissible transition: USE − LSE at 0 (the data want a flat or
   falling curve, so there is no ductile-to-brittle transition and T0 and C lose their meaning), or T0 at absolute zero. Both flags were kept
   in this group without change; the author's amendment concerned the lower shelf only.
3. *Boundary-limited* — the fit rests on a bound: the fitted LSE at its 0 J bound (`flag_lse_at_lower_bound`; the author's amendment), or a
   numerical-safety bound (C at 1 °C, C at the tested span, T0 at a range limit, USE − LSE at 10 × the highest energy, fitted LSE at the
   highest energy). `fit_outcome_reasons.csv` and the `outcome_detail` column say which bound controls.
4. *Weakly identified* — converged, inside its bounds, but the sampling does not constrain a parameter (D-047): weak transition, weak
   upper shelf, weak lower shelf (fitted LSE only), or a rank-deficient Jacobian.
5. *Usable fit, index temperature unavailable* — reason recorded (D-044, D-045).
6. *Usable fit, index temperature calculated.*
Reported beside the outcome and never part of it: the upper-shelf trend flag (model adequacy, D-043), the index-support diagnostic and the
notch-metadata flag (D-044). Nothing is dropped: every curve has a row with its outcome, flags, bounds, starts and solver messages.

**Result, final primary method** (`fit_outcomes.csv`, `fit_outcome_reasons.csv`; primary cohort, 170 curves): optimizer failure 0;
non-physical (inadmissible) 0; boundary-limited 18 (fitted LSE at its 0 J bound 15, all miniature; C at 1 °C 2, miniature; T0 at a range
limit together with USE − LSE at 10 × the highest energy 1, full-size curve 49-206); weakly identified 35; usable fit without index 13;
usable fit with T41J 104. **Effect of the terminology change alone** (the all-fitted fits of the CP3 presentation, reclassified,
`sensitivity_all_fitted_lse/fit_outcomes.csv`): 0 / 0 / 74 / 47 / 13 / 36 instead of 0 / 71 / 3 / 47 / 13 / 36 — the 71 curves then counted
non-physical all had exactly that one non-physical reason (LSE at 0 J) and become boundary-limited; no other count moves. The step from there to
the final counts is the lower-shelf amendment of D-042 (`method_change_before_after.csv`).

**History — the pre-registered decision (status then: PROPOSED (CP3); PRE-REGISTERED).**
**Decision (`classify` in `src/wp3_fitter.py`).** Flags may overlap; each curve also gets exactly one outcome, the first that applies:
1. *Optimizer failure* — no start returned a converged, finite solution.
2. *Non-physical* — the best tanh would need a physically impossible parameter, so the solution rests on a physical bound: fitted LSE at
   0 J (a negative lower shelf wanted), USE − LSE at 0 (no rise or a falling curve wanted), or T0 at absolute zero.
3. *Boundary-limited* — a numerical-safety bound is active: C at 1 °C (the rise happens between two test temperatures, width unresolved),
   C at the tested span, T0 at a range limit, USE − LSE at 10 × the highest energy, or fitted LSE at the highest energy.
4. *Weakly identified* — converged, inside its bounds, but the sampling does not constrain a parameter (D-047): weak transition, weak
   upper shelf, weak lower shelf (fitted LSE), or a rank-deficient Jacobian. (The upper-shelf trend flag belonged here at pre-registration
   and was moved out after the synthetic validation, D-051.)
5. *Usable fit, index temperature unavailable* — reason recorded: no defensible criterion (D-045), criterion not crossed, or crossing
   outside the tested range (D-044).
6. *Usable fit, index temperature calculated.*
Nothing is dropped: every curve has a row with its outcome, flags, bounds, starts and solver messages. Unlike [PR-EDB] §A.4.3.5, whose Monte
Carlo "eliminated" nonphysical results, failures are counted.

## D-047 — Identifiability diagnostics
**Status:** FINAL APPROVED (CP3, author 2026-09-14), subject to the D-046 terminology already implemented. Earlier: APPROVED IN PRINCIPLE (CP3,
author 2026-09-14), subject to the D-046 amendment; PRE-REGISTERED (their usefulness is tested in the synthetic validation, not assumed)
**Final CP3 decision (author, 2026-09-14).** Approved: the validated support, bound, transition and Jacobian diagnostics stay as they are. The
D-044 empirical-bracketing flag (`flag_index_not_bracketed_by_measured_energy`) is added as an index-support diagnostic, not as a
fitter-identifiability diagnostic or outcome: it is not in `FIT_FLAGS`, not in the "only this flag" comparison and not in `classify()`. No
condition-number threshold is introduced.
**CP3 decision (author, 2026-09-14).** Approved, with the zero-LSE classification amended (D-046). Kept: weak transition sampling, weak upper-shelf
support, weak lower-shelf support where LSE is fitted, rank/Jacobian diagnostics, bound diagnostics, and audit-only condition-number and start-spread
information. No condition-number cutoff is introduced. The documented weaknesses stay stated: false confidence can remain in some cold-side-only
designs; flags can be conservative near sharp thresholds; high scatter can defeat the method even with many specimens.
**Changes at the CP3 amendment.** `flag_nonphysical_lse_at_zero` is renamed `flag_lse_at_lower_bound` and counts towards *boundary-limited*
(D-046). Under the final method the lower-shelf diagnostics (LSE at bound, weak lower shelf) apply to miniature curves only, because full-size LSE is
fixed (D-042). The index-support diagnostic `flag_index_near_fitted_shelf` (D-044) is reported beside the fit diagnostics and kept out of the "only this
flag" comparison, which concerns fit diagnostics.
**Synthetic results for the final method** (`synthetic_flag_check.csv`, Blocks A–D with scatter, 17,800 fits, every truth full-size, LSE fixed at
2.7 J). Fits with no fit flag (10,516): 90th-percentile |error| T0 8.4 °C, T41J 8.7 °C, USE 7 %. Only a weak transition (2,582): T0 21.4 °C, T41J
21.4 °C. Only a weak upper shelf (2,736): T0 31.3 °C, USE 58 %. Only the upper-shelf trend flag (352): T0 9.4 °C, T41J 8.5 °C, no loss of accuracy.
Two or more flags (1,614): T0 71 °C, USE 638 %. Highest condition-number quartile: T0 42 °C, T41J 21 °C; disagreeing starts (112 fits): T0 33 °C,
T41J 34 °C (audit only). Outcome shares: usable 61 % (47 % under the all-fitted method), boundary-limited 7 %, weakly identified 32 %. **For the
fitted lower shelf** (the miniature case; all-fitted run, `sensitivity_all_fitted_lse/synthetic_flag_check.csv`, identical to the pre-CP3 numbers):
only LSE at its 0 J bound (335 fits): T41J 11.6 °C, C 60 % against 8.5 °C and 42 % with no flag; only a weak lower shelf (850): T0 15.4 °C against 8.6 °C.
**The documented weaknesses, re-checked for the final method** (`wp3_summary.md` §2.3, §2.8, §2.9).
- *Cold-side-only designs still fool the flags:* with every specimen below the true mid-transition (x −3…−0.5), 1 % (moderate) and 8 % (high scatter)
  of fits pass, with USE off by 79 % and 89 % (90th percentile of the passing fits); all fitted: 6 % and 10 %, 85 % and 88 %.
- *Conservative near thresholds:* e.g. five temperatures × three specimens at low scatter, where 90 % of all fits are within 2.6 °C of the true T41J,
  but only 88 % pass; on the published curves 11-45, 17-84 and 28-133 move from usable to weak upper shelf when the lower shelf is fixed, while their
  T41J changes by less than 1 °C. Passing fits can also be a biased subset (upper shelf weak, low scatter: T41J P90 3.3 °C for passing fits against 2.7 °C for all).
- *High scatter defeats the method even with many specimens:* with 18 specimens spread uniformly, 84 % of fits pass but their T41J P90 is 12.0 °C;
  only at 30 specimens (96 % pass, 8.3 °C) do passing fits meet the 10 °C reference.
- *New with the fixed full-size shelf:* an unsampled lower shelf is no longer flagged. The tested-range rule of D-044 still withholds most such T41J
  values, but the ones reported can miss the reference (150 °C window, true T0 60 °C below centre, C 30 °C: 80 of 200 fits report T41J, P90 12.5 °C).
- *Miniature truths (Block L, fitted LSE):* in 44 of 90 data sets, 5 % or more of fits pass the flags and the passing fits still miss T0 10 °C or USE
  10 %, mainly at high scatter, in the 250 °C windows and with the lower shelf weak or missing (lower shelf missing: 6–10 % pass with T0 errors of
  21–35 °C); this summary of Block L was first produced at the CP3 amendment.
**History — text as pre-registered and presented at CP3 (all-fitted method).**
**Decision.** Defined on the fitted curve, with x = (T − T0)/C and distinct temperatures as in D-037:
- *weak transition*: fewer than 2 distinct test temperatures with −1 < x < 1 (inside the 11.9–88.1 % part of the rise). With one or none,
  location and width cannot both be measured — the brief's ill-conditioning case.
- *weak upper shelf*: `use_support` is not *supported* (D-043). (Pre-registered: "or the upper-shelf residual trend is significant";
  moved to a separate model-adequacy flag after the synthetic validation, D-051.)
- *weak lower shelf* (only when LSE is fitted): fewer than 2 specimens at x ≤ −1.5.
- *numerically singular*: the Jacobian at the solution has rank below the number of parameters (NumPy's default rank tolerance).
The x-limits come from the tanh shape (±1: characteristic interval; ±1.5: within 4.7 % of a shelf); the counts of 2 are the smallest that
measure a level or a width twice. No condition-number threshold is imposed. The condition number of the scaled Jacobian and the spread of T0
among starts within 1 % of the best cost are recorded for audit; the synthetic validation reports how they relate to the true error.
**What the synthetic validation showed** (`outputs/wp3/synthetic_flag_check.csv`, Blocks A–D with scatter, 17,800 fits; the clean comparison
is fits carrying exactly one flag against fits carrying none). Weak transition, weak upper shelf and weak lower shelf each mark clearly
worse recovery (T0 90th-percentile error about 1.8–3.3 times, USE or LSE errors far larger); C at its lower bound, USE − LSE at its upper bound
and a rank-deficient Jacobian never occur alone and mark the worst fits; LSE at 0 J alone mildly worsens T41J and C. The upper-shelf trend flag
alone marks no loss of accuracy and fires at its chance rate (4.7 % of applicable fits), so it was moved out of the outcome (D-051). The audit
diagnostics also separate good from bad fits (highest condition-number quartile, disagreeing starts), but no threshold was set on them.
**Known weaknesses of these diagnostics, to be stated at CP3.** They are computed on the fitted curve, so (i) a wrong fit can look supported —
when every specimen lies below the true transition, 6–10 % of fits pass with USE off by about 85 %; (ii) passing can select a biased subset —
with the lower shelf just at the support limit, the fits that pass had a larger T41J error than all fits together; (iii) they are conservative
where a design sits exactly on a threshold. Where 41 J lies near the upper shelf (USE 44 J), T41J stays imprecise even in passing fits; the
position of 41 J on the fitted rise is recorded (`index_fraction_of_rise`) without a flag.

## D-048 — Synthetic validation design
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); PRE-REGISTERED (Blocks L and A–D);
Block E added after Blocks A–D had been run
**Final CP3 decision (author, 2026-09-14).** Approved; not redesigned. No scenario was added for the D-044 empirical-bracketing diagnostic, a
diagnostic-only change, and `src/wp3_validation.py` is unchanged: every synthetic output regenerated byte-identically when the diagnostic was
added. Its only synthetic evidence is the existing audit row of `synthetic_flag_check.csv` (usable T41J fits with no specimen energy below 41 J;
D-044). The validation history stays intact.
**CP3 decision (author, 2026-09-14).** Approved. The history is preserved: Blocks L and A–D were pre-registered; Block E was added later,
specifically to test non-flat upper shelves; the seed (20260913) and the deterministic behaviour stay documented. The synthetic outputs needed for
the final geometry-specific method are rerun; the validation matrix is not redesigned and no scenario is added to improve the final method's
appearance; the original all-fitted validation results stay recoverable.
**How that was done.** Blocks A–E run twice on identical synthetic data (`data_key()` excludes the strategy): with the all-fitted method as before
(scenario IDs S541–S657, unchanged from before CP3) and with the final method (S658–S774). Block L is unchanged (S001–S540): it is the pre-registered
comparison and already contains the final method's fits (D-042). 774 scenarios, 148,432 fits (657 and 128,216 before). Checked when the amendment was
run (scratch script, not a pipeline step): the Block L per-data-set table is byte-identical to commit `a2ce7f2`, and the regenerated all-fitted Blocks
A–E reproduce that commit's design, replicates, metrics, flag check, trust limits and Block E tables exactly, apart from the renamed LSE-at-bound
flag, the amended outcome labels and, for the 27 fits with the LSE at 0 J together with another bound, a reason string that now lists both bounds.
Per-replicate rows of both methods are stored (`synthetic_validation_replicates_blocks_A-E.csv.gz`). Summaries added from existing runs, not new
scenarios: trust classes per Block L data set under the final method (`synthetic_final_method_block_l.csv`), the final method's assembled Block L
scores, an index-support comparison and a criterion-bracketing audit (`synthetic_flag_check.csv`). Every Block A–E truth is full-size, so the final
method's miniature behaviour rests on Block L alone.
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
**Added after Blocks A–D had been run (D-051):** Block E, upper shelves that are not flat (the true energy changes by −20, −10 or +10 % of USE
per 100 °C above x = 1.5), two designs, low and moderate scatter, to measure what the upper-shelf trend flag detects. Block L replicates are
summarized per synthetic data set (`synthetic_lse_strategy_per_dataset.csv`); per-replicate rows are stored for Blocks A–E.
**Reference scales (summaries only, not acceptance criteria).** 10 °C for T41J and T0 — about the 17 °F (9.4 °C) limit on the scatter of
ΔRT_NDT for base metal in [10CFR50] §50.61(c)(2)(i)(C); 10 % for USE; 25 % for C.

## D-049 — Dataset-provided USE and DBTT: a diagnostic comparison only
**Status:** FINAL APPROVED (CP3, author 2026-09-14) as a diagnostic only. Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14) as a diagnostic
only; declared before any published curve was fitted
**Final CP3 decision (author, 2026-09-14).** Approved as a diagnostic only; nothing is fitted toward the dataset's undocumented USE or DBTT values.
**CP3 decision (author, 2026-09-14).** Approved as diagnostic only. The method is not tuned to reproduce the dataset's undocumented DBTT or USE.
**Result under the final method** (`dataset_value_comparison_summary.csv`). The dataset DBTT still behaves much more like T0 than like T41J: for 129
of the 134 full-size curves it lies closer to our T0 (101 of 104 usable fits, 28 of 30 others); the median |T0 − DBTT| is 3.2 °C (usable fits) and
3.4 °C (others), while our T41J is a median 29 °C and 35 °C colder than the dataset DBTT. The dataset USE lies within 10 % of our USE for 98 % of the
usable full-size fits and 87 % of the others; for 35 of the 36 miniature curves the dataset USE is below 41 J. Observed, not used: before the
amendment our all-fitted USE matched the dataset USE almost exactly for usable full-size fits (10th–90th percentile ratio 0.99999–1.00000); with the
lower shelf fixed the ratio spreads to 0.98–1.02. That is consistent with the dataset values coming from a tanh fit with a free lower shelf, but the
dataset authors' procedure remains undocumented (D-022). The pre-CP3 result below used the all-fitted method.
**Decision.** The dataset's `use_j_dataset` and `dbtt_c_dataset` (definition undocumented; the descriptor calls them "estimated values",
D-022) play no part in fitting, initialization, bounds, flags or method choice. After all fits are made, `src/wp3_fit_curves.py` compares them
per primary curve with our fitted USE, T41J (full-size) and T0, reports how often the dataset DBTT is closer to our T41J or to our T0, and
counts dataset USE values below 41 J (where a 41 J DBTT cannot exist). Disagreements are reported and, where a source defines its DBTT (e.g.
[Kumar1994]: the tanh midpoint), the definitional difference is named. The method is not adjusted to reproduce the dataset values.
**Result** (`outputs/wp3/dataset_value_comparison_summary.csv`). The dataset's DBTT is not a 41 J temperature: for 128 of the 132 full-size
curves with both values it lies closer to our T0 than to our T41J; the median |T0 − DBTT| is 2.9–3.3 °C, while our T41J is a median 26–31 °C
colder than the dataset DBTT. For 35 of the 36 miniature curves the dataset USE itself is below 41 J. The dataset USE agrees with our fitted
USE within 10 % for 94 % (flagged fits) to 97 % (unflagged fits) of full-size curves. Consistent with a mid-transition (tanh midpoint)
definition such as [Kumar1994]'s; the dataset authors' actual procedure remains undocumented (D-022).

## D-050 — Looser and stricter cohorts
**Status:** FINAL APPROVED (CP3, author 2026-09-14). Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14); declared before any published curve
was fitted
**Final CP3 decision (author, 2026-09-14).** Approved; the frozen CP2 memberships are not changed.
**CP3 decision (author, 2026-09-14).** Approved. The CP2 looser, primary and stricter memberships stay frozen and are not changed because of
WP3 fit quality. **Result under the final method** (`cohort_sensitivity_outcomes.csv`; optimizer failure / non-physical (inadmissible) /
boundary-limited / weakly identified / usable without index / usable with index): looser 0 / 0 / 19 / 42 / 14 / 107 (182); primary
0 / 0 / 18 / 35 / 13 / 104 (170); stricter 0 / 0 / 12 / 6 / 9 / 33 (60). Boundary-limited curves in the stricter cohort are 11 miniature and
1 full-size. The pre-CP3 result below used the all-fitted method and the pre-amendment classification.
**Decision.** The CP2-frozen looser cohort (182 curves) contains the primary (170) and stricter (60) cohorts, so every looser-cohort curve
is fitted once with the locked method, and outcome counts are tabulated for all three (`cohort_sensitivity_outcomes.csv`). This is a
diagnostic: the cohorts did not inform the fitter, and no WP4–WP6 conclusion is drawn from them in WP3. The membership check against
`data/FROZEN_COHORTS_CP2.csv` runs before any fit. Other frozen cohorts (alternative keep rule, unresolved irradiation, additively
manufactured, piping) and the 2024.206 release are not fitted in WP3.
**Result** (`cohort_sensitivity_outcomes.csv`; optimizer failure / non-physical / boundary-limited / weakly identified / usable without index
/ usable with index): looser 0 / 71 / 4 / 57 / 13 / 37 (182); primary 0 / 71 / 3 / 47 / 13 / 36 (170); stricter 0 / 23 / 1 / 8 / 9 / 19 (60).
The stricter screen removes most weakly identified curves but not the lower shelf at 0 J (38 % of stricter curves against 42 % of
primary), consistent with a model-shape cause rather than a sampling cause.

## D-051 — How the WP3 method evolved (chronological, including changes after results existed)
**Status:** record. FINAL APPROVED (CP3, author 2026-09-14) and extended with step 6. Earlier: APPROVED IN PRINCIPLE (CP3, author 2026-09-14)
and extended with step 5; no earlier step is rewritten, and no earlier commit is removed (`11daf72`, `0d5e548`, `20481dd`, `a2ce7f2` remain on
branch `wp3`; so do `5bd4c2c` and `76b9f87`, the amended state reviewed at final approval).
1. *Pre-registration* (commit `11daf72`): fitter, validation design, four lower-shelf candidates and the decision rule, committed before any
   synthetic or published-data fit.
2. *Block L run* (synthetic only): rule 3 selected `fitted`; `LOCKED_LSE_STRATEGY` set accordingly. Inspection showed the full-size advantage
   of a fixed shelf and the unintended 2 : 1 weighting of miniature data sets (D-042). The rule was **not** changed; a column reporting the
   cohort-weighted score was added to the output, marked as not used by the rule.
3. *Blocks A–D run* (synthetic only). Changes made as a result, all before any published curve was fitted:
   a. Methodological: the upper-shelf trend flag no longer makes a fit *weakly identified*; it is a separate model-adequacy flag (D-043,
      D-046, D-047). Before the change the same fits were counted weakly identified; error statistics are unchanged, and per scenario up to
      8.5 % of fits moved from *weakly identified* to *usable* (verified by rerunning: every error statistic identical, only outcome shares moved).
   b. Validation design: Block E added to measure that flag's power (D-048).
   c. Reporting: the "only this flag" comparison added to `synthetic_flag_check.csv`; the audit column `index_fraction_of_rise` added
      (no rule attached); per-replicate storage limited to Blocks A–E.
   d. Teaching figure: the "poor sampling" example first showed one replicate, which happened to be more accurate than the "good sampling"
      replicate and so misrepresented unreliability; it now overlays 40 replicate fits and states the 90th-percentile errors.
   e. Software bugs fixed (no reported number affected): a column-name collision in `scenario_metrics` stopped the figure step; the
      example figure first regenerated synthetic data from rounded temperatures.
4. *Published data*: first fitted after commit `0d5e548`, which locked the method. Nothing that determines a fit, flag or outcome changed
   afterwards; every run reproduced the same outcome counts (0 / 71 / 3 / 47 / 13 / 36). Changes made after the published fits existed:
   a. Software bug (reporting): the audit column `index_fraction_of_rise`, promised by D-047, had been added to the synthetic output only;
      it was added to the published-data output.
   b. Reporting: medians of empty groups (miniature curves have no T41J) raised warnings; guarded, values unchanged.
   c. Added to characterize an observed weakness, not to change the method: `residual_pattern_by_lower_shelf_outcome.csv` and
      `index_position_on_fitted_rise.csv` (D-042, D-044).
   d. Teaching figure: a boundary-limited panel was added to `fits_published_examples.png` beside the pre-declared non-physical one, and the
      captions were reformatted (LSE at its bound printed as 0 J).
   e. Methodological weakness found and **not** tuned around: the lower shelf rests at 0 J for 71 curves (D-042); left for the author at CP3.
5. *CP3 review and author-approved amendment* (author, 2026-09-14; this is not pre-registered, and every result it could have been influenced by
   already existed: the Block L comparison, Blocks A–E, and the published fits presented at CP3).
   a. What was pre-registered and what it gave: the all-fitted lower shelf was the primary method, selected by the pre-registered rule (step 2)
      and presented at CP3 with 71 of 170 curves at the 0 J bound, classed non-physical.
   b. What the synthetic validation had exposed: a specimen-scale weighting sensitivity of the rule's score (miniature truths weighted about 2 : 1
      against a cohort of 134 full-size : 36 miniature curves) and a full-size T41J advantage of the fixed 2.7 J convention at every scatter level
      (step 2, D-042).
   c. What the author decided: final primary lower shelf fixed at 2.7 J for full-size and fitted (>= 0 J) for miniature specimens (D-042); a fitted LSE
      at its 0 J bound is boundary-limited rather than non-physical (D-046); the metadata caveat, notch-metadata sensitivity and index-support diagnostic
      for T41J (D-044); approval in principle of D-040, D-041, D-043, D-045, D-047 to D-050.
   d. Why: literature ([SokolovNanstad1995]; the author's reading of [WallinBaer2023], unverified here, see WP3 sources), full-size T41J synthetic
      performance, and the actual project population and estimand. Not because of published-data success counts.
   e. The old all-fitted result remains as a sensitivity analysis: regenerated on every run, required to reproduce the CP3 counts
      (0 / 71 / 3 / 47 / 13 / 36) under the pre-CP3 classification, and compared curve by curve with the final method.
   Implementation changes: `PRIMARY_LSE_STRATEGY`, `SENSITIVITY_LSE_STRATEGY` and `lse_setting("geometry_specific")` in `src/wp3_fitter.py`;
   `LOCKED_LSE_STRATEGY` renamed `PREREGISTERED_RULE_OUTCOME` (it still guards the rule's outcome); `flag_nonphysical_lse_at_zero` renamed
   `flag_lse_at_lower_bound` and moved to the boundary-limited group; outcome label "non-physical" renamed "non-physical (inadmissible)";
   `flag_index_near_fitted_shelf` (the pre-CP3 audit position, now a flag outside the outcome); `pre_cp3_outcome()` to reproduce the old counts;
   Blocks A–E run with both methods; synthetic figures and published example figures regenerated with the final method and labelled with it.
   Reporting added: `fit_outcome_reasons.csv`, `t41j_notch_metadata_sensitivity.csv`, `lse_sensitivity_outcome_changes.csv`,
   `method_change_before_after.csv`, `synthetic_final_method_block_l.csv`, the `sensitivity_all_fitted_lse/` folder, and new columns
   (`geometry_description`, `index_support`, `outcome_detail`, `flag_full_size_notch_dimensions_unreported`). `lse_sensitivity_published*.csv` now
   compare final and all fitted; their pre-CP3 contents (all fitted against a 2.7 J / 0.1 J refit) remain in commit `a2ce7f2`.
   f. Teaching figure: the example panels after "successful" and "weakly identified" were re-specified before the amended fits were run: optimizer
      failure, non-physical (inadmissible), boundary-limited with the LSE at its bound, and boundary-limited by another bound, each if any, most points.
   g. Found after the amended fits existed, reported and **not** tuned around: published curve 33-153 receives a usable-fit T41J with no measured
      energy below 41 J; the audit columns `n_points_below_criterion` and `n_points_above_criterion` and a matching synthetic audit row were added,
      with no rule attached (D-042, D-044). Curve 49-206 becomes boundary-limited with the fixed shelf. With the full-size lower shelf fixed, the
      diagnostics no longer decline full-size designs whose lower shelf is unsampled (D-047). The first Block L trust-class summary shows 44 of 90
      miniature data sets where passing fits still miss a reference scale (D-047).
   h. Citation check: the accessible abstract of [WallinBaer2023] does not contain the statements attributed to it in D-040 and D-042 before CP3, nor
      the author's CP3 reading; the statements are marked, not deleted (WP3 sources). The pre-CP3 D-042 phrase "in every design" is corrected in a
      bracket (13 of 15 design × scatter cells).
   i. Software: the `wp3_fit_curves.py` docstring listed a file that never existed (`fit_outcomes_by_wp2_sampling.csv`); corrected. Cohort record IDs
      are now carried with the fits (`record_ids`, not written to the fit tables) instead of being merged back in; no value changes.
6. *Final CP3 approval and one support-diagnostic clarification* (author, 2026-09-14; every result it could concern already existed: the amended
   fits and synthetic outputs of step 5, commits `5bd4c2c` and `76b9f87`).
   a. Trigger: during the CP3 review, published curve 33-153 (step 5g) exposed a missing diagnostic: nothing said when a calculated T41J has
      measured energies on one side of 41 J only. The index-position warning cannot show it (41 J lies at 16.4 % of that curve's fitted rise).
   b. Added, and only this: the empirical-bracketing support diagnostic of D-044 (`criterion_bracketing()` in `src/wp3_fitter.py`, called after
      `classify()`), its per-curve columns, `t41j_empirical_bracketing_by_curve.csv`, `t41j_empirical_bracketing_summary.csv`, `wp3_summary.md`
      §3.2, a row in `fit_flags.csv`, `method_change_before_after.csv` and `method_configuration.md`, and a column in
      `index_availability_by_geometry.csv`. The audit columns of step 5g now feed it.
   c. Not changed because of it: no fit parameter, T41J value, fit outcome, fitting method, bound, start, weighting, cohort membership or
      synthetic scenario; `classify()` and `src/wp3_validation.py` are unchanged. Checked on the full regeneration (`./run_all.sh`): every
      pre-existing column of `fits_primary.csv`, `fits_looser_cohort_curves.csv` and `sensitivity_all_fitted_lse/fits_primary.csv` is identical
      to commit `76b9f87`; apart from the additions listed in b, every output of WP0–WP3, synthetic outputs and figures included, is
      byte-identical; the frozen-cohort check passed in WP2 and WP3; primary outcome counts 0 / 0 / 18 / 35 / 13 / 104 (170).
   d. The author gave final approval of D-040 to D-051 (CP3 final approval record above); `wp3` is merged into `main` with an explicit merge
      commit and kept.


---

# WP4 — Per-curve uncertainty

All numbers regenerate with `src/wp4_validation.py` (SYNTHETIC checks of the bootstrap) and `src/wp4_uncertainty.py` (published curves)
into `outputs/wp4/`. Both call `src/wp4_bootstrap.py`, which refits every replicate with the approved WP3 functions of `src/wp3_fitter.py`,
unchanged. Synthetic results live only in files named `synthetic_*` with a `data_type` column saying SYNTHETIC. WP4 does not normalize
specimen size, does not compare fixed material volumes and does not simulate test matrices (WP5, WP6).
**Status legend for this section:** `PRE-REGISTERED (WP4)` = written and committed before the published-data bootstrap results it governs
existed (commits named in D-067). Every WP4 entry is **provisional until the author's internal WP4 review** (an internal stop the author
set before WP5; the official CP4 follows WP5). `PROPOSED (WP4 review)` = written after results, for the author to decide.
`FINAL APPROVED (WP4 internal review)` = approved by the author at the internal WP4 review (2026-09-15), after reviewing the completed WP4
results; the earlier statuses follow it as history, and the pre-registered text below each final decision is kept unchanged as the record.
`APPROVED AS CANDIDATE SET ONLY (WP4 internal review)` = approved as candidates to carry into a later decision; nothing is chosen (D-066).

**WP4 internal-review approval record (author, 2026-09-15).** The author reviewed the completed WP4 state (branch `wp4`, commit `a806d93`) and
approved WP4 subject to the clarifications below; `wp4` is merged into `main` once they are recorded and verified. This review is the internal
stop the author set before WP5; the official checkpoint CP4 still follows WP5. Each item is recorded in full in the entry named.
1. D-052 pairs (case) bootstrap: FINAL APPROVED as the PRIMARY WP4 uncertainty method; not replaced after seeing the results.
2. D-053 fixed-design wild bootstrap: FINAL APPROVED AS SENSITIVITY ONLY; never promoted to primary; never a silent replacement because it is
   narrower.
3. D-054 approved WP3 fitter inside every replicate: FINAL APPROVED; the 2.7 J full-size shelf is not varied inside the bootstrap; model-choice
   uncertainty and sampling uncertainty stay separate.
4. D-055 replicates, seeds, stability subset and memory-safe execution: FINAL APPROVED; the change from 8 to 3 worker processes is an execution
   (systems) change only.
5. D-056 targets and percentile interval: FINAL APPROVED WITH A TERMINOLOGY CLARIFICATION (below); the endpoints are neither relabelled nor
   recomputed.
6. D-057 95 % finite-target reporting rule: FINAL APPROVED EXACTLY AS PRE-REGISTERED; not lowered; the 54 unavailable full-size T41J intervals
   stay the primary result (below).
7. D-058 primary / diagnostic / unavailable labels: FINAL APPROVED; a narrow diagnostic interval never upgrades a weak WP3 fit.
8. D-059 T41J support diagnostics: FINAL APPROVED; curve 33-153 stays retained and explicitly warned; the warning is not an exclusion rule.
9. D-060 SYNTHETIC bootstrap validation: FINAL APPROVED with its complete history; no new bootstrap method is selected; the coverage
   limitations are part of the result.
10. D-061 residual scatter: FINAL APPROVED AS CHARACTERIZATION ONLY; empirical published-data residual scatter, never pure material scatter.
11. D-062 uncertainty against sampling properties: FINAL APPROVED; descriptive associations, not causal claims.
12. D-063 published cross-check: FINAL APPROVED; bootstrap SD against Marini's (2020) SD, never a 95 % width against a one-sigma value; the
    conclusion stays nuanced.
13. D-064 pairs against fixed design: FINAL APPROVED as diagnostic evidence; the method giving the smaller interval is never chosen for that reason.
14. D-065 worked-example and diagnostic figures: FINAL APPROVED; mean-curve confidence band, T41J interval and new-specimen prediction
    uncertainty stay distinct.
15. D-066 WP6 scatter-model candidates C1-C3: APPROVED AS CANDIDATE SET ONLY; the final WP6 scatter model is NOT chosen.
16. D-067 method and system history: FINAL APPROVED AS A CHRONOLOGICAL RECORD; step 9 records this approval session.

**Final author decision: the 54 unavailable full-size T41J intervals stay the primary result (2026-09-15).** Under the primary pairs bootstrap,
54 of the 134 full-size T41J intervals are unavailable under the pre-registered 95 % finite-target rule (38 from usable WP3 fits, 16 from weakly
identified fits; `interval_curve_accounting.csv`). They are KEPT AS THE PRIMARY RESULT under the original rule. No alternative reporting
threshold is added, and their conditional finite-target quantiles are not promoted: those stay in the tables for audit only, under the label
"interval unavailable: bootstrap-unstable", and are never presented as equivalent to a primary CI. Interpretation: *the pairs bootstrap revealed
that, for these curves, enough resampled test matrices lose support for an in-range 41 J crossing that a nominal 95 % interval cannot honestly be
reported under the pre-registered rule.* (In each of the 54 curves, every replicate without a T41J is one whose 41 J crossing lies below that
replicate's own lowest test temperature; `t41j_support_bootstrap.csv`, D-067 step 7.) The fixed-design wild result is preserved as a separate sensitivity:
keeping the test temperatures fixed leaves only 8 full-size T41J intervals unavailable (97 primary + 29 diagnostic + 8), and that difference is
scientifically informative. Changing the rule after observing the count would be post-hoc tuning; the number of unavailable intervals is itself
a result about test-matrix fragility.

**Interval terminology and calibration caveat (D-056; applies to every WP4 interval).** Every WP4 interval is a *nominal 95 % percentile
bootstrap interval* (the 2.5th to 97.5th percentile of the finite replicate values; where space is limited, *95 % percentile bootstrap CI*). It
was not empirically calibrated to exactly 95 % frequentist coverage, and nothing may imply that it was. **SYNTHETIC coverage of the primary pairs
intervals was not exactly 95 %:** about 89.5 % for well-sampled full-size T41J, about 93 % for high-scatter full-size T41J, about 97 % for the
weakly sampled full-size design and about 96.5 % for miniature T0 (200 synthetic data sets per scenario, Monte Carlo SE about 1.5 percentage
points; `synthetic_bootstrap_coverage_summary.csv`, D-060): below nominal in some well-sampled or high-scatter designs, above nominal in some
weak designs. This is a reporting calibration caveat only: the estimator, the interval endpoints and the validation numbers are unchanged and
not reinterpreted.

**Use of WP4 in later work packages (author, 2026-09-15).**
- *WP5* may consume the approved WP3 fits and the WP4 uncertainty labels where relevant. It must not treat a bootstrap interval width as
  specimen-size correction uncertainty, and it must determine the size effect independently, from genuinely comparable specimen-size pairs.
- *WP6* (later): primary uncertainty and scatter basis = the pairs-bootstrap results where appropriate, with the empirical published-data residual
  profile as calibration evidence; sensitivities = the fixed-design bootstrap and the C1, C2 and C3 scatter-model alternatives (D-066).
- Never treated as pure material scatter without qualification: between-curve spread, bootstrap interval widths, conditional ranges, SYNTHETIC
  validation outputs, the published residual scatter.
Not authorized by this approval: WP5 work, specimen-size normalization, WP6 work, calibrating or recalibrating any scatter model, and any change
to WP4 code, data or generated outputs.

**Sources cited in WP4** (what was actually read is stated; nothing below is cited from memory)
- [Marini2020] (listed under WP3). WP4 read the full text again, from the Internet Archive copy of the publisher's open-access PDF (CC BY;
  the publisher site and HAL refused automated access on 2026-09-14): §2, §3.1–3.5, §4.1–4.3, §5, Tables 2–14, Eqs 1–6. Facts used: one
  16MND5 forging, 142 tests from −196 to +300 °C; tanh with LSE = 0 (Eq. 1); scatter represented per test temperature by a mixture of two
  Weibull distributions (Eq. 2); 10,000 simulated data sets per test matrix; *precision* σ = standard deviation of the transition temperature
  over those data sets, *accuracy* ε = mean minus the reference value, *uncertainty* u = (σ² + ε²)^½ (Eq. 3); "RCC-M" matrix of 18 tests,
  3 at each of −60, −40, −20, 0, +20 °C and 3 at +100 °C (Table 6): T41 σ 3.52 °C, ε −0.13 °C, u 3.52 °C, USE σ 4.44 J (Table 7); reference
  case of 600 specimens: T41 σ 0.72 °C (Table 5); u = a·N^−β with β 0.51 (B matrices, Table 10) and 0.53 (C matrices, Table 12), "almost
  inversely proportional to the squared root of the number of specimens"; Eq. 6, u = (a S² + b S + c)/√N with the test-matrix shift S of
  Eq. 4, for T41 a 3.1, b 1.2, c 12.5 (best estimate) and 16.0 (upper bound) (Table 13), shifts of the A matrices −0.23 to 1.33 (§4.1,
  Table 8), RCC-M shift 0.67 with best estimate 3.46 °C and upper bound 4.28 °C (Table 14); position of the matrix matters (§4.1, Fig. 7).
- [Switzner2023] (listed under WP3). WP4 re-read the full text (Internet Archive copy of the MDPI PDF): §1.5, §2.7, §3.1–3.2, §4.2–4.4.
  Facts used: 12 Charpy tests of one API-5L X52 pipe with 4.5 mm bars; uncertainty by Monte Carlo of an assumed measurement error (absorbed
  energy SD = 0.6 J + 0.026 × measured value, attributed there to ASTM E23), 1,000 data sets, "95 % quantile"; USE (EUS) 46 ± 8 J
  (four-parameter), 46 ± 5 J (two-parameter); T85 is an 85 % shear-appearance temperature.
- [Miura2024preprint] Miura N., Shinko T., Nomoto A. *Variation of ductile-brittle transition temperature for Charpy curve provided by
  hyperbolic tangent function.* SSRN preprint 4917170, posted 2024-08-06, doi:10.2139/ssrn.4917170, **not peer reviewed** (full text, 11 pp.,
  opened through SSRN's public "Open PDF in Browser" link): §2 Eqs 1–14, §3 (Monte Carlo check, 1,000 samples, interquartile-range outlier
  exclusion), §4 (parameter survey; standard parameters LSE 3 J, USE 200 J, C 50 °C, N_LSE 2, N_USE 4, N_TT 6, CV_LSE 0.1, CV_USE 0.1,
  CV_CVE 0.49), §5. The model propagates the uncertainty of LSE, USE and the energy at T41J into T41J with the curve's C and D treated as known
  (§2, §5: "this model assumes that the parameters are known"). Findings: σT41J approximately ∝ 1/√N_TT; more lower-shelf specimens do not
  reduce it; more than 2 upper-shelf specimens barely do; the scatter at 41 J dominates. The published version [Miura2025] (IJPVP 216:105495)
  was not accessible; differences between the two versions are unknown.
- [NIST-TN2158] Lucon E., Splett J., Koepke A., Newton D. (2021). *NIST Software Package for Obtaining Charpy Transition Curves.* NIST
  Technical Note 2158, doi:10.6028/NIST.TN.2158 (full text): §4.2, Appendix A.1, A.3–A.6, A.9. Facts used: fixed-temperature parametric
  bootstrap with normal errors of SD = RMSE of the original fit, truncated at 0 (A.4); 1,000 iterations "based on the results of numerical
  simulations investigating the number of iterations needed for the bootstrap interval estimates to stabilize" (A.4); fixed shelves are
  also varied, default u(LS) = 0.3 J for absorbed energy and u(US) = 5 % of US, "based on engineering judgement" (A.5); confidence intervals
  from the 2.5 % and 97.5 % percentiles, chosen because the percentile bootstrap is robust "when the fitted parameters lie near their
  boundary" (A.6); temperatures assumed known without error (A.3); only random effects covered (A.4).
- [EfronTibshirani1986] Efron B., Tibshirani R. (1986). *Bootstrap Methods for Standard Errors, Confidence Intervals, and Other Measures of
  Statistical Accuracy.* Statistical Science 1(1):54–77, doi:10.1214/ss/1177013815 (scanned full text; pages 54–55, 62–64, 68 and 72 read):
  §5, regression y_i = g(β, t_i) + ε_i with covariates "considered fixed at their observed values" and residuals resampled (Eqs 5.3–5.10);
  "another, simpler way": resampling each covariate-response pair; the two "are asymptotically equivalent, but can perform quite differently
  in small sample situations", and the pairs method "gives a trustworthy estimate of β̂'s variability even if the regression model ... is not
  correct"; §7, percentile method (interval between the 100·α and 100·(1 − α) percentiles, transformation-invariant; Table 6 lists standard,
  percentile, BC, BCa); §9, "B = 1000 is a rough minimum" for BC or BCa intervals, "Somewhat smaller values, say B = 250, can give a useful
  percentile interval"; standard errors improve little past B = 100.
- [MacKinnon2012] MacKinnon J.G. *Thirty Years of Heteroskedasticity-Robust Inference* (published 2012 as a book chapter,
  doi:10.1007/978-1-4614-1653-1_17, not read); read as Queen's Economics Department Working Paper No. 1268 (May 2011): §2 (HC1: residuals
  × √(n/(n − k)); HC2: û²/(1 − h); HC3: û/(1 − h)), §3 (pairs bootstrap of Freedman 1981 resamples rows of the data matrix, "does not make sense
  if the regressors are thought of as fixed in repeated samples", "does not condition on X"; wild bootstrap y* = Xβ̂ + f(û)v*, Eq. 8, with
  f = û/(1 − h)^½ "a natural choice", Eq. 9; two-point distributions F1 (Mammen) and F2 (Rademacher, ±1 with probability ½); "a great deal of
  evidence that the wild bootstrap outperforms the pairs bootstrap" for heteroskedasticity-robust tests and intervals), §5 (simulations: F2
  and leverage-adjusted residuals favoured), §6.
- [DavidsonFlachaire2001] Davidson R., Flachaire E. (2001). *The Wild Bootstrap, Tamed at Last.* Queen's Economics Department Working Paper
  No. 1000 (full text; published 2008 in the Journal of Econometrics, doi:10.1016/j.jeconom.2008.08.003, not read): Abstract (the Rademacher
  distribution "usually gives smaller ERPs, in small samples" than Mammen's distribution; a particular version is recommended), §2 (wild
  bootstrap DGP, auxiliary variable with E(ε) = 0 and E(ε²) = 1, residual transformations as in HC0–HC3, Liu (1988) mentions Rademacher
  variables; for a nonlinear regression a consistent estimate of the parameters should be used in the bootstrap DGP).
- Cited only through [MacKinnon2012] and [DavidsonFlachaire2001], not read: Freedman (1981), Wu (1986), Liu (1988), Mammen (1993), MacKinnon &
  White (1985), Flachaire (2005).
- Citation check (2026-09-14): a statement attributed in the pre-registered D-042 text to the abstract of [Miura2025] is not in the
  abstract; the finding it paraphrases is in the preprint's full text, with a different emphasis. Marked in place (D-042), not deleted.

## D-052 — Primary resampling method: nonparametric pairs (case) bootstrap
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: the nonparametric pairs (case) bootstrap remains the PRIMARY WP4
uncertainty method, because it was pre-registered before any published-data result existed, keeps temperature and energy paired, honestly
exposes the fragility of an estimate to which specimens and test temperatures happen to be present, and in the SYNTHETIC validation covered the
truth substantially better than the fixed-design wild method (D-060). It is not replaced after seeing the results.
**Decision.** For a curve with N measured specimens, one bootstrap replicate draws N complete specimen records (test temperature and absorbed
energy together) with replacement, each record with probability 1/N, and refits them with the approved WP3 method (D-054). The drawn records
are kept in spreadsheet order. `src/wp4_bootstrap.py::run_replicates` (method `pairs`).
**What it represents.** The variability of the WP3 estimate if the curve's specimens are regarded as a random sample of (temperature, energy)
outcomes of that test programme: specimen-to-specimen scatter *and* which test temperatures happen to be present. It does **not** condition on
the tested temperatures: a replicate can lose a temperature, a shelf or the only transition specimens. That is information about the fragility of
the sampling plan, not a defect; but it means the spread includes finite-sample design fragility in addition to outcome scatter, and for curves
with few distinct temperatures it is expected to exceed a fixed-design analysis.
**Why primary (argued before results).** (i) No scatter model and no assumption that the symmetric tanh is the true curve, which WP3 showed it
is not for every curve (D-040, D-042 residual patterns); the pairs method "gives a trustworthy estimate of β̂'s variability even if the
regression model ... is not correct" [EfronTibshirani1986] §5. (ii) Non-constant Charpy scatter ([Marini2020] §3.1, D-041) is carried
automatically by the resampled pairs. (iii) It exposes how fragile a sparse sampling plan is, which is WP4's question (brief Q1, Q2).
(iv) It is simple to explain. [MacKinnon2012] §3 describes the method and its main limitation (no conditioning on the design).
**Evidence against, weighed before results.** [MacKinnon2012] reports much evidence that the wild bootstrap outperforms the pairs bootstrap for
heteroskedasticity-robust tests and intervals, and Charpy test temperatures are chosen, not random. Not decisive here: that evidence concerns
studentized inference on linear-regression coefficients, whereas WP4 needs percentile intervals of a nonlinear index from a model that is
misspecified for some curves; and a residual-based fixed-design method cannot perturb specimens the fit interpolates (leverage near 1), which
are exactly the fragile designs WP4 must expose. The fixed-design method is therefore run on every curve as the sensitivity (D-053) so the
consequence of the choice is measured.
**Alternatives.** Fixed-design residual or wild bootstrap as primary; parametric bootstrap with one normal scatter [NIST-TN2158] A.4; delta
method from the fit's Jacobian; jackknife. **Why not.** Conditional on the design and on the fitted model (residual methods); constant scatter
imposed (parametric); linearization fails where the fit is weakly identified or rank-deficient (delta method); the jackknife is unreliable for
non-smooth estimators such as a crossing that can disappear. **If the alternative were chosen.** Intervals conditional on the tested
temperatures, typically narrower for sparse designs, possibly too narrow where the fit passes through isolated transition points.

## D-053 — Fixed-design sensitivity: wild bootstrap, Rademacher signs, HC2 leverage-adjusted residuals
**Status:** FINAL APPROVED AS SENSITIVITY ONLY (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the
author's internal WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved as a sensitivity only; it is NOT promoted to primary. The SYNTHETIC
validation showed material under-coverage, worst for weak sampling (T41J 80 % well sampled, 75 % high scatter, 38.5 % weakly sampled; miniature
T0 75.5 %; D-060). Its purpose is diagnostic: *what happens if the original test temperatures are kept fixed and only the residual scatter is
perturbed?* It may be carried into later stages as a sensitivity comparison, but it must never silently replace the pairs result because it
gives narrower intervals.
**Decision.** The tested temperatures are kept. Replicate energy E*_i = Ê(T_i) + ũ_i·v_i, where Ê is the approved WP3 fit of the curve,
r_i = E_i − Ê(T_i) its residual, ũ_i = r_i / (1 − h_i)^½, h_i the leverage (diagonal of the linearized hat matrix J(JᵀJ)⁺Jᵀ, J = Jacobian of
the fitted curve with respect to the parameters that are free at the WP3 solution, in WP3's scaled parameterization; a fixed LSE and
parameters at a bound, by WP3's definition, have no column; rank tolerance as WP3's numerically-singular flag), and v_i independent
Rademacher signs (+1 or −1, each with probability ½). Energies below 0 J are set to 0 J and counted, as in the WP3 synthetic generator (D-048).
Where 1 − h_i ≤ 1e-8 the fit passes through the point (its residual is 0 at a least-squares solution); ũ_i is set to 0 and counted.
`src/wp4_bootstrap.py::leverage_adjusted_residuals`, `run_replicates` (method `wild`).
**Why a wild bootstrap, not resampling residuals as one pool.** Scatter is not constant along the curve ([Marini2020] §3.1; D-041). Pooling
would move lower-shelf residuals of a few joules into the transition and transition residuals of tens of joules onto the shelves. The wild
bootstrap keeps each residual at its own temperature ([DavidsonFlachaire2001] §2; [MacKinnon2012] §3, Eq. 8).
**Why HC2 residuals.** Least-squares residuals are on average too small, most at influential points; with 6–10 specimens and 3–4 parameters the
average leverage p/N is large. r/(1 − h)^½ has constant variance under homoskedastic errors ([MacKinnon2012] Eq. 9, "a natural choice";
[DavidsonFlachaire2001] §2). HC3 over-compensates ([MacKinnon2012] §2, §5); a single factor √(N/(N − p)) (HC1) ignores leverage, which differs
greatly between shelf and transition points of a tanh fit.
**Why Rademacher signs.** Recommended by [DavidsonFlachaire2001] (Abstract) and [MacKinnon2012] §3, §5 over Mammen's two-point distribution in
small samples. Explainable: each replicate energy is either the observed energy or its mirror image about the fitted curve (after the leverage
adjustment).
**Why not the NIST parametric bootstrap.** [NIST-TN2158] A.4 draws normal errors with one SD, the RMSE, at every temperature (constant scatter)
and varies fixed shelves (A.5; see D-054).
**What it represents.** Scatter-driven uncertainty for the actual test matrix, conditional on the fitted curve being the mean curve and on each
curve's own residuals representing the scatter at its temperatures.
**Limitations stated before results.** It relies on the fitted model (systematic misfit is treated as scatter about a mean curve that every
replicate shares); it cannot perturb interpolated points, so it can understate uncertainty where designs are most fragile; with few residual
degrees of freedom the residuals estimate the scatter poorly; mirroring a residual can place a synthetic energy on the other side of 41 J
that was never measured (relevant to 33-153). **Role:** sensitivity only; it is never preferred for giving narrower or wider intervals.

## D-054 — The approved WP3 method inside every replicate; the 2.7 J full-size lower shelf held fixed
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: every bootstrap replicate continues to use the final approved WP3 fitter:
full-size LSE fixed at 2.7 J; miniature LSE fitted >= 0 J; the USE, T0 and C treatment unchanged. The 2.7 J shelf is not varied inside the
bootstrap. Model-choice uncertainty (the all-fitted sensitivity case of D-042) and sampling uncertainty (WP4) remain separate.
**Decision.** Every replicate is refitted with the exact approved functions, in the order of `wp3_fit_curves.fit_all`: `lse_setting`
(geometry-specific), `fit_curve` (its bounds and starts derived from the replicate's own data, as the method defines them), `index_temperature`
(the tested-range rule applied to the replicate's own lowest and highest temperature), `index_fraction_of_rise`, `classify`, and
`criterion_bracketing` (on the replicate's energies). `src/wp3_fitter.py` is unchanged. Full-size LSE stays fixed at 2.7 J in every replicate;
miniature LSE stays fitted with a 0 J lower bound. Before any bootstrap, `src/wp4_uncertainty.py` refits every original curve and stops unless
it reproduces `outputs/wp3/fits_primary.csv` (LSE, USE, T0, C, SSE and T41J within 1e-9; identical outcome, index status and support flags).
A replicate whose evaluation raises an unexpected exception is counted as a replicate evaluation error (none expected), never skipped.
**Why the 2.7 J shelf is not varied.** WP4 estimates sampling uncertainty conditional on the approved model. Uncertainty about the lower-shelf
convention is model uncertainty, already quantified by the approved all-fitted sensitivity case (D-042: full-size |ΔT41J| median 0.29 °C,
90th percentile 1.89 °C). Mixing the two would make neither attributable. [NIST-TN2158] A.5 varies fixed shelves (default u(LS) = 0.3 J for
absorbed energy, by engineering judgement): a defensible alternative not adopted, whose effect on T41J would be small because 41 J lies far
above the shelf.
**Why the tested-range rule is re-applied per replicate.** The bootstrap must replicate the whole estimation procedure, including when it
declines to report: a replicate whose crossing lies outside its own tested temperatures has no T41J, and that is counted (D-057).
**Alternatives.** A simplified or "bootstrap-friendly" fitter; varying LSE; using the original curve's tested range. **If chosen.** A different
estimator from the one reported; sampling and model uncertainty mixed; extrapolated crossings counted as values.

## D-055 — Replicates, seeds, determinism and Monte Carlo stability
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: B = 2,000 per curve per method; the deterministic per-replicate seed
construction; the B = 4,000 Monte Carlo stability subset; the memory-safe worker and checkpoint implementation. The change from 8 to 3 worker
processes is purely an execution (systems) change and stays documented as such (D-067 steps 3-5); results do not depend on the worker count
(D-060 determinism check).
**Decision.** B = 2,000 replicates per curve, both methods, all 170 primary curves, fixed before any interval existed. Basis:
[EfronTibshirani1986] §9 (B = 1,000 a rough minimum for BC/BCa intervals, about 250 useful for a percentile interval); [NIST-TN2158] A.4 uses
1,000; 2,000 leaves about 50 replicates beyond each 2.5 % tail. Benchmarked before the choice (timings only): about 6 ms per refit on one core,
1.85 ms of wall time with 8 worker processes on the project machine, so both methods take about 21 min; no reduction was needed, and no curve
receives fewer replicates. [After the low-memory stop (D-067 steps 3-4) runs use 3 worker processes by default; B is unchanged and results do not
depend on the worker count.]
**Seeds.** `numpy.random.SeedSequence([20260914, h(curve ID), h(method name), replicate index])`, h = the integer of the first 15 hex digits of
SHA-256 (WP3's construction). One independent stream per replicate: results do not depend on the number of worker processes, the chunking or
the execution order (checked, D-060, and on two published curves). Pairs: `rng.integers(0, N, N)`, sorted; wild signs: `rng.integers(0, 2, N)`.
**Monte Carlo stability.** Predeclared subset: (a) in each stratum geometry (full-size, miniature) × original WP3 quality (usable; weakly
identified or boundary-limited), the curves with the fewest, the median (lower median) and the most specimens (ties by curve ID); (b) after
the B = 2,000 run, the full-size curves with the narrowest and the broadest reportable pairs T41J interval and the miniature curves with the
narrowest and the broadest reportable pairs T0 interval; duplicates merged (at most 16 curves). Both methods rerun with B = 4,000 on an
independent seed stream (method name + "|stability-4000"); compared at the 2.5th, 50th and 97.5th percentiles, SD, finite fraction and
reportability, and the largest change expressed as a share of the B = 2,000 width. B is never tuned curve by curve.
**Alternatives.** B = 1,000; a nested 4,000 that reuses the first 2,000 (it would understate the Monte Carlo change).

## D-056 — Targets and interval definition
**Status:** FINAL APPROVED WITH A TERMINOLOGY CLARIFICATION (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional
pending the author's internal WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: the targets and the percentile method stay, 2.5th percentile to 97.5th
percentile of the finite target values; the numerical endpoints are neither relabelled nor recomputed. Terminology: in documentation and figures
the precise phrase is *nominal 95 % percentile bootstrap interval*, or, where space is limited, *95 % percentile bootstrap CI*. Nothing may imply
that these intervals were empirically calibrated to exactly 95 % frequentist coverage. The SYNTHETIC validation stays visible wherever they are
reported: the primary pairs intervals covered the truth below nominal in some well-sampled or high-scatter scenarios and over-covered some weak
designs (about 89.5 %, 93 %, 97 % and 96.5 %; the interval terminology and calibration caveat in the WP4 internal-review approval record). They
are therefore nominal 95 % percentile bootstrap intervals with known calibration limitations. Generated table and figure labels written before
this decision are unchanged (D-067 step 9).
**Decision.** Full-size: T41J (primary target), USE, T0; C diagnostic. Miniature: T0 (primary target), USE; LSE and C diagnostic. No index
temperature, geometry-scaled or volume-scaled 41 J or other criterion for miniature curves (D-045). **Interval:** 95 % percentile bootstrap
interval, lower = 2.5th and upper = 97.5th percentile of the finite target values ([EfronTibshirani1986] §7; [NIST-TN2158] A.6), NumPy's default
linear interpolation. Also reported: median, mean, SD (ddof 1), width, bias = bootstrap mean − original estimate, 16th and 84th percentiles and
(q84 − q16)/2 as a robust spread that exposes SDs dominated by a few extreme replicates, finite count and fraction; USE also relative to the
original USE. **Band in figures:** pointwise 2.5th–97.5th percentiles of the replicate fitted mean curves over the admissible replicates: a
confidence band for the mean curve, not a prediction interval for a new specimen.
**BCa not used.** It needs an acceleration estimate and more replicates ([EfronTibshirani1986] §9), is harder to explain, and its advantages
presuppose a smooth, well-identified estimator, which weak and boundary-limited fits are not. The percentile interval is transformation-invariant
([EfronTibshirani1986] §7) and robust near bounds ([NIST-TN2158] A.6). BCa is not called better and is not run as a sensitivity.
**Alternatives.** Normal interval ± 1.96 SD (ignores skew); bootstrap-t (needs a per-replicate variance estimate, unreliable for weak fits).

## D-057 — Failed and target-unavailable replicates; the 95 % finite-target reporting rule
**Status:** FINAL APPROVED EXACTLY AS PRE-REGISTERED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending
the author's internal WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved exactly as pre-registered: a formal reportable interval requires at least
95 % of all requested replicates to produce a finite target value; failed and unavailable replicates remain in the denominator; the threshold is
not lowered. For curves below the threshold the conditional finite-replicate quantiles are kept for audit only, the formal interval is labelled
unavailable / bootstrap-unstable, and the conditional range is never presented as equivalent to a primary CI. No new primary interval is created
merely to recover the 54 unavailable full-size T41J intervals: they stay the primary result (author decision recorded in the WP4 internal-review
approval record). Reason: the large number of unavailable intervals is itself a scientific result about test-matrix fragility, and changing the
rule after observing that count would be post-hoc tuning.
**Decision.** Every requested replicate stays in the denominator. Per curve and method the replicate outcomes are counted in the WP3 categories
(optimizer failure; non-physical (inadmissible); boundary-limited; weakly identified; usable fit without index; usable fit with index) plus
evaluation errors, and must sum to the replicates requested (the run stops otherwise). **Target available:** T41J when that replicate's index
status is "calculated" (otherwise optimizer failure, 41 J outside the fitted shelves, or crossing below or above the replicate's tested range) —
T41J from weakly identified or boundary-limited replicate fits therefore counts, as it does for the original curves (D-044), with those outcome
counts reported beside it; T0, C, USE and LSE when the fit converged and is not non-physical, because such a fit has no admissible transition
(D-046). **Reporting rule:** conditional quantiles of the finite values are always stored for audit; a formal "reportable 95 % bootstrap interval"
requires finite values in at least 95 % of the replicates requested; otherwise `interval_reportable = False`, the target is described as
bootstrap-unstable / interval unavailable, and its finite fraction is reported.
**Why 95 %.** If more than 5 % of the bootstrap probability mass has no defined estimate, a nominal central 95 % interval built from the surviving
estimates can hide a material failure probability: the missing mass would equal both excluded tails together. **This is a project reporting
rule, not an ASTM requirement.** It is fixed before any result and will not be changed after seeing results.
**Alternatives.** Intervals from successful replicates only, labelled as if unconditional; unavailable T41J treated as ±∞; a lower threshold.

## D-058 — Which original fit outcomes receive primary or diagnostic intervals
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: an original WP3 usable fit receives a primary bootstrap interval if the
finite-target rule passes; an original WP3 weakly identified or boundary-limited fit receives a diagnostic bootstrap interval only; a target
finite in fewer than 95 % of the replicates requested has its interval unavailable. A narrow diagnostic interval is never used to upgrade a weak
or boundary-limited WP3 fit.
**Decision.** All 170 primary curves are bootstrapped, not only the 117 usable fits. Reportable interval and original WP3 outcome usable (either
usable category) → **primary bootstrap CI**; reportable and original outcome boundary-limited or weakly identified → **diagnostic bootstrap
interval**, not equivalent in evidentiary strength; not reportable → **interval unavailable: bootstrap-unstable**. A narrow interval never
overrules a WP3 warning, and bootstrap success never upgrades a WP3 outcome. The index-position and empirical-bracketing warnings and the
notch-metadata flag are reported beside the label, never folded into it. `src/wp4_bootstrap.py::interval_label`.
**Why.** WP4 must show how uncertainty behaves for weakly identified and boundary-limited curves; replicates of a boundary-limited fit can pile
up on the same bound and give a misleadingly narrow conditional distribution.

## D-059 — T41J support diagnostics carried into the bootstrap
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved; carried forward: the empirical bracketing of 41 J, the fitted-rise
(index) position, the bootstrap share of replicates that bracket 41 J, and the target-unavailable reason. Curve 33-153 remains retained but
explicitly warned: it is not deleted, and the warning is not turned into an exclusion rule.
**Decision.** For every full-size curve and method: the share of replicates whose (resampled or synthetic) energies bracket 41 J; among replicates
with a finite T41J, the share not bracketed and the share with the index-position warning (41 J outside 11.9–88.1 % of that replicate's fitted
rise); T41J unavailability by reason; beside the original curve's two diagnostics (`t41j_support_bootstrap.csv`). Curve 33-153 keeps its T41J
and its warning and gets a diagnostic figure. Support diagnostics are neither fit failures nor interval rules. The handoff keeps apart
mathematical bootstrap variability (SD, interval), empirical support for the index (bracketing, index position) and original WP3 fit quality.

## D-060 — SYNTHETIC validation of the bootstrap implementation
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review. The coverage replicate count was set after a runtime benchmark and before any coverage result (below).
**Final WP4 internal-review decision (author, 2026-09-15).** Approved, with the complete validation history preserved: the first low-memory
run, the systems-only memory fix, the successful rerun, the zero-scatter check, the deterministic worker-count checks, the failure accounting and
the coverage results (D-067 steps 3-5). No new bootstrap method is selected at the WP4 review; the coverage limitations are part of the result.
**Decision** (`src/wp4_validation.py`; synthetic data regenerated exactly from the approved WP3 validation: scenario definitions, scatter model
and seed 20260913; WP3's validation is not redesigned and no scenario is added to it).
1. *Zero scatter.* Data exactly on the model, WP3 design uniform over x = −3…3 with 12 specimens: full-size truth LSE 2.7 J (representable with
   the fixed shelf), USE 150 J, T0 0 °C, C 30 °C; miniature truth LSE 0.48 J, USE 8 J, T0 0 °C, C 30 °C (fitted LSE); B = 2,000 per method.
   Pass: wild, every replicate admissible and within 0.001 °C (key target: T41J or T0) and 1e-5 (USE ratio) of the original; pairs, at least 95 %
   of replicates within those tolerances (a replicate that loses every transition temperature cannot pin T0 and C even on exact data).
2. *Determinism.* WP3 Block A uniform n = 12, moderate scatter, replicate 0: two single-process runs and one run with 8 worker processes and
   chunks of 97 must give identical per-replicate arrays and summaries. [Changed with the memory fix, D-067 step 4: the multi-process runs use
   3 workers with chunks of 97 and 2 workers with chunks of 333; the 8-worker run of the stopped first run also passed.]
3. *Failure accounting.* WP3 Block B "x -0.5..3, n=12 (lower shelf missing)", "shelves + 1 transition point (n=7)" and "clustered cold side:
   x -3..-0.5, n=12", moderate scatter, replicate 0, both methods, B = 2,000: outcome counts, T41J status counts and finite + unavailable must
   each equal the replicates requested; the finite fraction must use all requested replicates; the reportable flag and the label must follow
   D-057 and D-058; at least one data set must switch the interval off, otherwise the check fails.
4. *Coverage.* WP3 scenarios, final method: Block A uniform n = 18, moderate ("well sampled"); Block B shelves + 2 transition points (n = 8),
   moderate ("weakly sampled"); Block A uniform n = 18, high ("high scatter"); Block L uniform n = 12 (lower shelf well sampled), miniature
   truth USE 8 J with LSE 6 % of USE, moderate ("miniature, fitted lower shelf"). Their first 200 data sets (WP3 replicates 0–199), 500 bootstrap
   replicates per data set and method. Reported: share of reportable intervals; coverage of the truth by reportable intervals, with its Monte
   Carlo SE; truth below and above; median width; median bootstrap SD against the empirical SD of the original estimates over the 200 data sets
   (the true sampling SD of that fixed design); bias and RMSE of the original estimates. No acceptance threshold, and the bootstrap is not tuned
   on coverage. Full-size truths have LSE 5 J while the method fixes 2.7 J, so coverage is measured against the truth including WP3's small bias
   (D-042).
**Coverage replicates (benchmark before any coverage result).** 1.85 ms of wall time per refit with 8 worker processes: 1,000 replicates per data
set would take about 49 min, 500 about 25 min; 500 chosen. The Monte Carlo noise of a 2.5 % endpoint from 500 replicates is about ±0.7
percentage points of tail probability, small beside the coverage Monte Carlo SE of about 1.5 points at 200 data sets; [EfronTibshirani1986] §9
finds about 250 useful for percentile intervals. The published curves keep B = 2,000 (D-055). [With 3 worker processes after the memory fix the
coverage study takes longer (about 32 min measured from its first block); the replicate count was not changed.]

## D-061 — Empirical published-data residual scatter (characterization only)
**Status:** FINAL APPROVED AS CHARACTERIZATION ONLY (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4) for the definitions;
provisional pending the author's internal WP4 review. WP6 candidates: D-066.
**Final WP4 internal-review decision (author, 2026-09-15).** Approved as characterization only. It keeps the name *empirical published-data
residual scatter* (or equivalent) and is never called pure material scatter: it mixes specimen-to-specimen material variation, laboratory and
machine differences, calibration and reporting differences, digitization error and tanh model-shape mismatch, and its leverage correction is
approximate. These limitations are carried prominently into WP6.
**Decision.** A dataset of all 2,588 primary records with the approved WP3 point fit (`published_residual_scatter_dataset.csv`): record ID,
spreadsheet row, curve, reference, geometry, material, product form, irradiation, WP3 outcome and reason, temperature, measured and fitted
energy, residual (J), residual / fitted USE, leverage, leverage-adjusted (HC2) residual in J and / fitted USE, x = (T − T0)/C, fraction of the
fitted rise, region, fitted slope. Regions: lower shelf x ≤ −1.5; lower transition −1.5 < x ≤ −0.5; central transition −0.5 < x < 0.5; upper
transition 0.5 ≤ x < 1.5; upper shelf x ≥ 1.5 (WP3's four regions, D-042, plus the upper shelf). Summaries by geometry and region: count,
curves, mean, SD, median, 1.4826 × MAD, 5th/25th/75th/95th percentiles; primary summary on usable WP3 fits (the T0, C and USE of a weakly
identified or boundary-limited fit make x and the normalization unreliable), all fits as sensitivity. Strata, full-size usable fits only:
product form group and irradiation × three zones (lower shelf, transition |x| < 1.5, upper shelf); strata with fewer than 10 curves or 30
residuals are shown and marked "too few to interpret". Normalization by the fitted USE, as WP3's residual-pattern table; raw joules kept.
**Name.** *Empirical published-data residual scatter*, never "material scatter": it mixes specimen-to-specimen material scatter, between-study
machine, calibration and reporting differences (109 source publications, brief §3), digitization error, and model-shape error (symmetric tanh,
fixed 2.7 J shelf). Residuals also shrink by the degrees of freedom the fit uses, hence the leverage-adjusted version.
**Alternatives.** Normalization by USE − LSE; per-curve standardization (would erase the between-curve differences WP6 needs to see).

## D-062 — Uncertainty against pre-existing sampling properties
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: the descriptive Spearman and grouped analyses are kept and are not
converted into causal claims. The observed relationship between T41J interval availability and the number of measured energies below 41 J
(Spearman 0.89 with the finite-T41J fraction; `uncertainty_vs_sampling_spearman.csv`, `uncertainty_vs_sampling_binned.csv`) is preserved as a
useful empirical design result.
**Decision.** One row per curve (`uncertainty_vs_sampling_by_curve.csv`). Uncertainty: key target (full-size T41J, miniature T0) pairs bootstrap
SD and 95 % width over reportable intervals, finite fraction over all curves; USE relative width. Properties, all existing before the bootstrap:
N, distinct temperatures, tested span, distinct temperatures and specimens inside T0 ± C of the WP3 fit, specimens on the fitted lower
(x ≤ −1.5) and upper (x ≥ 1.5) shelves, WP2 lower-, transition- and upper-band temperatures, span / C, stricter-cohort membership, WP3
outcome; fitted C shown as a curve-shape covariate, not a sampling property. The WP2 sampling class is identical for all 170 primary curves
("brackets the transition in the screening bands"), so it cannot explain differences and is only listed. Methods: Spearman rank correlations
with curve counts (p-values descriptive only), binned medians with counts; a one-variable Theil–Sen slope of log SD against log N only for the
published comparison (D-063). No multivariable or machine-learning model. Association, not causation: the properties are correlated with one
another and with material and source.

## D-063 — Published uncertainty cross-check: quantities compared
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: [Marini2020] stays the principal like-for-like RPV sanity check. This
project's bootstrap SD is compared primarily with Marini's SD (precision-like) quantity; a full 95 % interval width is never compared with a
one-sigma literature value. The conclusion stays nuanced: the typical full-size uncertainty here is somewhat larger than, but of the same
engineering order as, the published RPV result (pairs SD median 4.87 °C at median N 14 against Marini's σ(T41) 3.52 °C at N = 18;
`published_uncertainty_crosscheck.csv`), which is reasonable given heterogeneous multi-study data and test layouts. Agreement is not claimed more
strongly than the evidence supports.
**Decision.** Principal comparison [Marini2020]: the *precision* σ of T41 is the SD of T41 over repeated simulated data sets for one fixed matrix,
a one-standard-deviation quantity for a single determination; it is compared with this project's **bootstrap SD**, never with a 95 % width.
RCC-M matrix, N = 18: σ(T41) 3.52 °C. Normalized comparison: SD × √N against Marini's Eq. 6 amplitude for T41 over the shifts he studied:
12.38–19.58 °C (best estimate, c = 12.5), at most 23.08 °C (upper bound, c = 16.0) — computed from Table 13 and checked against his Table 14
(3.46 and 4.28 °C at S = 0.67, N = 18). Specimen-count trend: Theil–Sen slope of log SD against log N, against Marini's exponents 0.51 and
0.53. Subsets: C1, usable full-size fits with a primary pairs T41J CI; C2, C1 with 15–25 specimens (Marini's 15–25-specimen A matrices and the
18-specimen RCC-M matrix); C3, C1 in the stricter cohort; both methods shown, pairs primary. Statistics: median and quartiles of SD and of
SD × √N; shares of C1 amplitudes below, within and above Marini's ranges. The verdict (broadly comparable / systematically larger /
systematically smaller / too heterogeneous) is argued from these statistics, not forced to a match.
**Secondary.** [Miura2024preprint] Eq. 13 at its standard parameters gives σT41J ≈ 6.9 °C (this project's evaluation of their equation;
6 transition specimens at T41J, CV 0.49 at 41 J, C 50 °C, curve parameters known): order of magnitude and 1/√N_TT scaling only.
[Switzner2023]: T85 is a shear-area index, and its USE ± 8 J comes from an assumed-measurement-error Monte Carlo on 12 sub-size pipe specimens:
not commensurate with T41J; USE mentioned loosely only. [NIST-TN2158]: method reference only.
**Differences to discuss, not to correct for.** Many materials and studies pooled; heterogeneous temperature layouts; the pairs bootstrap
resamples the design while Marini simulates a fixed matrix; LSE fixed at 2.7 J here, 0 in Marini; between-study variability; irradiated and
unirradiated curves; digitized data. Much smaller uncertainties than the literature would be a warning to investigate; much larger ones call for
checking sampling quality, heterogeneity and the bootstrap's interpretation.

## D-064 — Pairs against fixed-design comparison
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved; the comparison is preserved as diagnostic evidence, and the method giving
the smaller interval is never chosen for that reason. When the comparison is cited later it states that the pairs bootstrap includes
test-matrix composition fragility, that the fixed-design bootstrap conditions on the original test temperatures, and that the fixed-design wild
intervals were anti-conservative in the SYNTHETIC validation (D-060).
**Decision.** For each target, curves where both methods give reportable intervals (and, separately, those with a usable original WP3 fit):
ratios of pairs to wild SD and 95 % width; median, 10th and 90th percentiles, minimum and maximum with curve IDs, share with pairs wider; the
three lowest and three highest SD ratios for full-size T41J and miniature T0 examined against N, distinct temperatures, transition specimens,
maximum leverage and interpolated points. **Interpretation fixed in advance.** Pairs wider: the composition of the test matrix and the placement
of its temperatures contribute materially. Wild wider: the residual perturbation generates more variability than case resampling (for example
large residuals at influential temperatures). Neither is "better"; the pairs bootstrap remains the primary measure (D-052).

## D-065 — Worked-example figure and diagnostic figure
**Status:** FINAL APPROVED (WP4 internal review, author 2026-09-15). Earlier: PRE-REGISTERED (WP4); provisional pending the author's internal
WP4 review
**Final WP4 internal-review decision (author, 2026-09-15).** Approved: the worked-example figure (curve 3-17) and the diagnostic figure (curve
33-153) are kept. The distinction stays explicit between the confidence band for the fitted mean curve, the uncertainty interval on T41J, and
prediction uncertainty for a new specimen, which is NOT what the band represents. Preferred interval wording: D-056; the text drawn in the
generated figures is unchanged (D-067 step 9).
**Decision.** *Worked example* (`worked_example_t41j_bootstrap.png`): among usable full-size fits with a calculated T41J whose notch dimensions are
reported, that are empirically bracketed, carry no index-position warning, have 10–20 specimens and a primary pairs T41J CI, the curve whose
pairs bootstrap SD is closest to the median SD of that pool (ties: fewer specimens, then curve ID): representative, not the best-behaved. It shows
the published test data (so labelled), the approved WP3 fit, the pointwise 95 % pairs-bootstrap band of the fitted mean curve (not a prediction
interval), T41J with its 95 % bootstrap CI, the empirical-bracketing status and the method, and the replicate T41J distribution. *Diagnostic
figure:* curve 33-153 with both methods. Grayscale-legible: dark points, black fit line, grey band, orange-and-black diamond, black error bar,
solid hairline grid; a non-reportable interval is drawn grey and named a conditional range.

## D-066 — Candidate scatter models for WP6, from the WP4 residual characterization
**Status:** CENTRAL MODEL CHOSEN IN WP6 PLANNING: **C1** (D-095, approved by the author in WP6 Plan Mode, 2026-09-18, before
any WP6 result), which changes the planning preference recorded below (C2 central) on calibration evidence; C2 and C3
(amended to centred resampling, D-094) remain mandatory sensitivities. Earlier: APPROVED AS CANDIDATE SET ONLY (WP4 internal
review, author 2026-09-15); FINAL WP6 SCATTER MODEL NOT YET CHOSEN. Earlier: PROPOSED
(WP4 review), written after the WP4 results existed. Not chosen, not calibrated, not run: the WP6 scatter model is decided in
WP6, with the sensitivity analysis the brief requires (brief §5 WP6, "the scatter model is the weak link").
**WP4 internal-review decision (author, 2026-09-15).** Approved as a candidate set only; no scatter model is marked final. All three candidates
are carried into the future WP6 review:
- *C1:* region-wise normal scatter scaled by USE.
- *C2:* the smooth WP3-style form sd(T) = σ_T·|dE/dT| + cv·E(T) + 3·cv·LSE, calibrated later to reproduce the empirical profile.
- *C3:* empirical region-wise residual resampling.
Current planning preference only: C2 may be treated as the CENTRAL candidate, because it is smooth and physically interpretable; C1 with the
robust scale should provide a lower-scatter sensitivity; C3 should preserve the empirical heavy tails and heterogeneity as a contrasting
sensitivity. This is NOT the final WP6 scatter-model decision: WP6 must calibrate and test the candidates and report explicitly whether the
headline full-size-versus-miniature conclusion changes across them. The central model is not stratified by product form or irradiation unless
later evidence supports adequate sample counts. Miniature scatter stays separately identified as more weakly supported.
**Evidence** (`published_residual_scatter_summary.csv`, `published_residual_scatter_strata.csv`; usable WP3 fits; leverage-adjusted residual /
fitted USE, SD with the robust scale 1.4826 × MAD in brackets). *Full-size* (1,685 residuals, 104 curves, 42 references): lower shelf 0.036
(0.023); lower transition 0.073 (0.054); central transition 0.105 (0.099); upper transition 0.100 (0.085); upper shelf 0.062 (0.051); in joules
(raw residuals) 6.9, 14.3, 20.2, 18.1 and 10.9 J. The scatter is not constant: largest through the transition, about three times the lower
shelf and 1.7 times the upper shelf; on the shelves the SD exceeds the robust scale (heavier tails). The lower-shelf mean residual is +0.015 USE
(+2.8 J): many measured lower shelves lie above the fixed 2.7 J convention, a model-convention error rather than scatter. *Miniature* (179
residuals, 13 curves, 6 references): larger relative scatter (central transition 0.167 (0.116)) from few curves. *Strata* (full-size): forging and
plate transition 0.084 and 0.095 (robust 0.074 and 0.090); unirradiated and irradiated 0.096 and 0.091 (14 irradiated curves); HAZ, weld metal and
"not determinable" have fewer than 10 curves, so no product-form-specific scatter is supported. The pool mixes specimen-to-specimen material
scatter, between-study machine, calibration and reporting differences, digitization error and model-shape error; the leverage adjustment
corrects the shrinkage of fitted residuals only approximately. It is an *empirical published-data residual scatter*, not a material-scatter
distribution.
**Candidates.**
- *C1, region-wise normal scatter scaled by USE:* sd = USE × s(region) with the five full-size values above; a lower variant from the robust
  scale; a separate, weakly supported miniature table. Simplest and directly traceable; steps at region edges.
- *C2, the WP3 synthetic generator's form* sd(T) = σ_T·|dE/dT| + cv·E(T) + 3·cv·LSE (D-048), with σ_T and cv calibrated in WP6 so that it
  reproduces the C1 profile. Smooth and physically readable (transition scatter as specimen-to-specimen shifts of the local transition
  temperature, plus a proportional part); already implemented; its calibration is WP6 work.
- *C3, empirical resampling of the leverage-adjusted residuals by region* (nonparametric), keeping skew and heavy tails and, with them, the
  between-study heterogeneity of the pool (an upper-bracket flavour).
**Proposal for the WP6 review.** C2 as the central model calibrated to the C1 profile, bracketed by the C1 robust variant (lower scatter) and C3
(empirical tails); no stratification by product form or irradiation; miniature scatter handled separately with its larger uncertainty stated.
The author decides at WP6; nothing in WP4 depends on the choice.

## D-067 — How the WP4 method evolved (chronological, including changes after results existed)
**Status:** record. FINAL APPROVED AS A CHRONOLOGICAL RECORD (WP4 internal review, author 2026-09-15) and extended with step 9. Earlier: record;
provisional pending the author's internal WP4 review. No step is rewritten later; later steps are appended.
**Final WP4 internal-review decision (author, 2026-09-15).** Approved as a chronological record. Kept: the memory crash, what caused it, the
streaming and checkpoint fix, the proof that statistical outputs did not change, which changes occurred before and which after results existed,
and the reproducibility tests. The chronology is not rewritten to make the development look cleaner than it was; step 9 is appended.
1. *Before any WP4 code.* Literature read (WP4 sources). Runtime benchmark of the approved fitter on pairs resamples of 8 published primary
   curves (60 replicates each): only milliseconds per refit were computed or viewed, no bootstrap statistic. A scratch smoke test of the new
   code on one SYNTHETIC WP3 data set (100 replicates per method) confirmed that chunked multi-process runs equal single-process runs. A parallel
   benchmark on SYNTHETIC coverage data sets (timings only) set the coverage replicate count (D-060).
2. *Pre-registration commit.* D-052 to D-065, D-067, the WP4 sources, the citation check on [Miura2025] in D-042, and `src/wp4_bootstrap.py`,
   `src/wp4_validation.py`, `src/wp4_uncertainty.py`, committed before either script had been run (no synthetic coverage result and no
   published-data bootstrap result existed).
3. *First synthetic validation run, stopped for low memory (2026-09-14; code of the pre-registration commit).* With 8 worker processes it
   completed and wrote the zero-scatter, determinism and failure-accounting checks (all passed) and was stopped by the operating
   environment, which reported the system running low on memory, during the coverage study; no coverage result existed. Its three
   completed outputs were kept aside for comparison; they are not final results. Diagnosis (measured): on the 8 GB project machine about
   2.2 GB was wired by a virtual machine and simulator runtimes; every spawned worker imports numpy, scipy and pandas (about 110 MB); the
   coverage stage submitted all 1,600 bootstrap runs at once and the parent kept every replicate array (about 100 MB), so 9 Python processes
   of roughly 1.2-1.4 GB competed with the rest of the system.
4. *Systems fix, no statistical change (before any coverage or published-data result).* `wp4_bootstrap.stream_map` (a spawn-context worker
   pool, 3 workers by default for this machine, `WP4_WORKERS` to override, workers recycled after 200 tasks, tasks fed lazily, results
   consumed one at a time); coverage runs summarised inside the workers, so replicate arrays never reach the parent; `src/wp4_checkpoint.py`
   with fingerprinted, atomically written checkpoints (validation steps, coverage blocks of 25 data sets, and one file per published-data run)
   in the git-ignored `cache/wp4/`, reused only when code, package versions, parameters and input data are identical; the determinism check
   now compares single-process runs with 3-worker and 2-worker runs (8 workers before); run-dependent timings removed from
   `synthetic_bootstrap_validation.md` so that it regenerates byte-identically. Unchanged: B, seeds and seed streams, scenarios, data sets,
   targets, rules and checks. Smoke test before the rerun (scratch script; SYNTHETIC): streamed coverage rows identical to the first
   implementation's for the same seeds; the failure-accounting table identical to the pre-crash output (24 rows, 32 columns); a checkpointed
   run interrupted by deleting one block recomputed only that block and gave identical rows; peak memory of the Python process tree 414 MB.
   Also before any published-data result: three robustness fixes in `src/wp4_uncertainty.py` from a static review (an order-dependent maximum
   over missing values, an empty-pool guard in the stability subset, a pandas group-apply deprecation) and the published-data runs moved to the
   same streamed, checkpointed execution.
5. *Synthetic validation rerun with the memory-safe code (completed; SYNTHETIC only; no published-data bootstrap result existed).* 46.8 min
   with 3 worker processes; peak memory of the Python process tree 316 MB (sampled every 2 s; main process 116 MB, largest worker 114 MB),
   against about 1.2-1.4 GB estimated for the stopped run. Nothing statistical changed: the zero-scatter and failure-accounting outputs are
   byte-identical to the stopped run's; the determinism check gives identical replicates and summaries for single-process runs and for 3- and
   2-worker runs, and the same T41J SD and interval endpoints as the stopped run's 8-worker run. All checks passed; the failure-accounting check
   switched the interval off in 4 rows (T41J finite in 0-36 % of replicates) with every replicate still in the denominator; all 4,400 coverage
   rows account for their 500 replicates. **What coverage showed (reported; no method, rule or B changed because of it).** Pairs percentile
   intervals covered the truth in 89.5 % (T41J), 89.5 % (T0), 90.5 % (USE) of 200 data sets for the well-sampled design (Monte Carlo SE about
   1.5 points), 93 % / 93 % / 90 % at high scatter, 97 % / 96 % / 86 % for the weakly sampled 8-specimen design and 96.5 % (T0) / 91.5 % (USE)
   for the miniature case; the median pairs SD was 0.91 (T41J) to 1.1 (T0) of the actual spread of the estimate in well-sampled and high-scatter
   designs, 2-3 times it for T41J and T0 in the weak design (design fragility counted), and dominated by extreme replicates for USE there (19
   times; percentile coverage 86 %), which is why the robust spread (q84 - q16)/2 is reported beside the SD. Fixed-design wild intervals
   under-covered everywhere: T41J 80 % (well sampled), 75 % (high scatter), 38.5 % (weak design); miniature T0 75.5 %; median SD 0.67-0.87 of the
   actual spread in well-sampled designs and 0.31 in the weak design — the anti-conservative behaviour D-053 anticipated. The pairs bootstrap
   stays the primary method as pre-registered (D-052); in the method comparison (D-064), "pairs wider" must be read with this demonstrated
   under-coverage of the fixed-design method in mind.
6. *Software dry run of the published-data script, then layout fixes (before the real run).* After the synthetic validation was committed,
   `src/wp4_uncertainty.py` ran once with B = 40 (stability rerun B = 80), writing its outputs and checkpoints to a scratch directory outside the
   repository, to exercise every code path before the long run; it finished in 1 min with a 327 MB peak. Its numbers were not used and are not
   in the repository. What it made visible, recorded because results were then partly visible: with only 40 replicates many full-size T41J
   intervals fell below the 95 % finite-target rule, mostly because pairs replicates that lose a curve's coldest temperatures place the 41 J
   crossing below their own tested range, where the approved estimator declines to report T41J (D-054). This is a consequence of the
   pre-registered rules, reported by reason in `t41j_support_bootstrap.csv` (D-059); no rule was changed. Changes made after the dry run,
   presentation only: figure layout (panel titles and legends that overlapped data, replicate counts read from the run instead of typed,
   line styles that stay distinguishable in grayscale, a plural label). No estimator, rule, B, seed or selection rule changed.
7. *Published-data run with the pre-registered rules (results now exist).* 40.5 min with 3 worker processes (the 340 bootstrap runs 33.1 min, the
   B = 4,000 stability rerun 7.1 min); peak memory of the Python process tree 300 MB. The WP4 refits reproduced `outputs/wp3/fits_primary.csv` for
   all 170 curves; the published-data determinism spot check (replicates 0-249 of two curves, single process against the pooled run) was
   identical. Changes after the results were visible, recorded as such: (i) figure layout only (legends of the two curve figures moved above
   the panels, comparison-figure legends moved off the points); (ii) one descriptive addition to explain the unavailable full-size T41J
   intervals (all 54 arise from replicates whose 41 J crossing falls below their own tested range): the WP3 audit count of measured energies below
   41 J (D-044, pre-existing) added to the sampling correlations and bins (Spearman ρ 0.89 with the finite-T41J fraction; reportable pairs
   intervals 0 of 1 curve with no measured energy below 41 J, 0 of 11 with one, 3 of 30 with two, 47 of 61 with three or four, 30 of 31 with
   five or more). No estimator, rule, B, seed, subset rule or label changed. Regenerated from the verified checkpoints in 17 s: all other outputs
   byte-identical to the first run (33 of 36 files; the three that changed are the two extended tables and the summary).
   **Observations for the author's review, no action taken:** the 95 % rule together with the tested-range rule leaves 54 of 134 full-size
   T41J intervals unavailable under the primary method (8 under the fixed-design method); the pairs percentile intervals covered about 90 % of
   synthetic truths in well-sampled designs (slightly below nominal) and the fixed-design intervals clearly under-covered; T41J endpoints were
   stable between B = 2,000 and 4,000 (largest change 5.9 % of the interval width), whereas the SD of heavy-tailed USE distributions and one
   multimodal T0 distribution (curve 104-none.3, 51 % of its width) were not, so percentiles, not SDs, are the reportable quantities there.
8. *Reproducibility runs of the committed state (no code, rule, seed or result changed).* `./run_all.sh` in the repository with the checkpoint
   cache moved aside, so that every bootstrap was recomputed from the raw data: exit 0 in 3 h 01 min while other applications loaded the 8 GB
   machine heavily (WP4 synthetic validation 59.6 min, published data 75.5 min; peak memory of the Python processes 813 MB); all 151 tracked
   output and processed-data files rewritten, 0 changed. The runtime notes in `run_all.sh` and `README.md` ("about 30 min" per WP4 script)
   were corrected to the measured times (commit `ea1ec97`, comments and README only). A fresh clone of `ea1ec97` with a newly created `.venv`
   regenerated all 151 files with 0 tracked files changed and 0 untracked files. The environment stopped that clone's run once for low memory
   during the synthetic coverage study, with other applications holding most of the memory (26 of 32 coverage blocks written, each
   byte-identical to the repository run's checkpoint); the two remaining WP4 scripts were then run in the same clone, resuming from its own
   fingerprint-verified checkpoints (6 blocks computed, 26 reused; the published-data stage computed all 340 runs).
9. *WP4 internal-review approval (author, 2026-09-15; every result it concerns already existed, in the committed state `a806d93`).*
   a. Decided: D-052 to D-065 and D-067 FINAL APPROVED; D-066 APPROVED AS CANDIDATE SET ONLY, the WP6 scatter model not chosen; the 54 unavailable
      pairs full-size T41J intervals kept as the primary result under the unchanged 95 % rule, with no alternative threshold and no promoted
      conditional quantiles; the interval wording *nominal 95 % percentile bootstrap interval* with the synthetic calibration caveat (D-056); the
      use of WP4 in WP5 and WP6 (WP4 internal-review approval record).
   b. Changed: documentation and status wording only, in `DECISIONS.md` (the approval record, the final decisions and statuses of D-052 to D-067,
      this step), `PROGRESS.md` and `README.md`. The pre-registered text of every entry is unchanged.
   c. Not changed: any code, data, cohort, estimator, rule, B, seed, label, number, generated table or generated figure. Generated text therefore
      keeps its generated wording: labels such as "primary bootstrap CI", the "95 % percentile intervals" of the coverage tables and "95 % CI" in
      the caption of `worked_example_t41j_bootstrap.png` denote the nominal 95 % percentile bootstrap interval of D-056, and the status line of
      `outputs/wp4/wp4_summary.md` still reads "internal review awaiting the author". That text is written by `src/wp4_uncertainty.py` and
      `src/wp4_validation.py`; changing it requires a code change and a regeneration, which this approval session did not make. `PROGRESS.md` is
      the authoritative status.
   d. Checks (lightweight; no bootstrap and no pipeline step was rerun, because no executable code changed): only `DECISIONS.md`, `PROGRESS.md`
      and `README.md` differ from `a806d93`; the SHA-256 of each of the other 178 tracked files is identical to its value before the edits,
      including all 41 `outputs/wp4/` files and the four WP4 source files; `data/` and every WP0-WP3 output and source file are identical to
      `main` (`b47d08e`); the raw-data SHA-256 checksums verify (7 of 7); the CP2 membership fingerprints recomputed from
      `outputs/wp2*/cohort_membership.csv` match `data/FROZEN_COHORTS_CP2.csv` for all 14 cohorts (primary 170 curves / 2,588 records). An
      independent recomputation from the per-curve WP4 tables (a scratch script outside the repository that imports no project code) reproduced
      the interval accounting (pairs full-size T41J 66 / 14 / 54, fixed-design 97 / 29 / 8; USE 104 / 30 / 0 full-size and 13 / 23 / 0 miniature;
      miniature T0 13 / 23 / 0), confirmed that every stored label follows the pre-registered rule and that each of the 340 bootstrap runs accounts
      for its 2,000 replicates, and confirmed that in each of the 54 curves every replicate without a T41J is one whose crossing lies below its own
      lowest test temperature.
   e. `wp4` is merged into `main` with an explicit merge commit and kept; no remote, no push. WP5 has not started.

---

# WP5 — Specimen size effect

All numbers regenerate with `src/wp5_pairs.py` (pair inventory, no normalization) and `src/wp5_size_effect.py` (normalization,
mapping, residuals) into `outputs/wp5/`; both use `src/wp5_normalization.py`, which holds the literature equations and their
self-checks, and the unchanged approved WP3 fitter `src/wp3_fitter.py`. WP5 contains **no synthetic data**: every row is either a
published measurement, a parameter fitted to published measurements, or a transformed estimate derived from published
measurements, and every output table says which.

**Status legend for this section:** `PRE-REGISTERED (WP5)` = written and committed before the normalization result it governs
existed (commits named in D-085). `PROPOSED (CP4)` = written after results, for the author to decide at CP4.
`FINAL APPROVED (CP4)` = approved by the author at the official checkpoint CP4 (2026-09-17), after reviewing the completed WP5
results; the earlier statuses follow it as history and the pre-registered text of every entry is kept unchanged as the record.

**CP4 approval record (author, 2026-09-17).** The author reviewed CP4 and approved WP5 subject to the decisions below; `wp5` is
merged into `main` once they are recorded and verified. Each item is recorded in full in the entry named. **These approvals are
documentation and status only: no code, estimator, normalization, threshold, match class, sign convention, inclusion rule,
cohort, number, generated table or generated figure changed, and no WP5 number moved** (verified by SHA-256 over all 206 tracked
files in `data/`, `outputs/`, `src/` and `run_all.sh` before and after the approval edits; D-088).

1. **D-073, D-074 FINAL APPROVED** — the primary normalization stands as pre-registered: energy by the ligament (nominal
   fracture) volume ratio (B b²)_full / (B b²)_small with b = W − a, temperature by M = 98 − 15.1 ln(B b²) °C with B b² in mm³,
   as in the published Sokolov & Alexander correlation. The documented caveats are kept verbatim: the energy normalization is a
   classical geometry-based approximation; the temperature equation was developed from specific RPV steels and specimen
   geometries; **neither equation is exact physics**; geometry, notch and constraint effects remain; and applicability outside
   the originally studied geometries is weaker. **The primary method is not changed because a post-hoc sensitivity had a
   different residual.**
2. **D-075 FINAL APPROVED AS SENSITIVITY SET** — the seven pre-declared alternatives stay sensitivities and are regenerated on
   every run.
3. **D-072 FINAL APPROVED** — the KLST specimens of refs 107 and 109 are read with the 3 mm ligament direction (W = 4 mm,
   B = 3 mm) as primary, with the dataset-literal reading kept as sensitivity S6. **The raw dataset is not rewritten**: the
   recorded dimensions, the interpreted geometry, the source basis and the S6 alternative all stay auditable in
   `geometry_normalization_factors.csv` and in this entry.
4. **D-068, D-069 FINAL APPROVED** — primary WP5 evidence stays same-study matched material-condition comparisons. **The rule is
   not loosened to increase N.** The empty cross-study primary class is an honest result. STRICT, PARTIAL, NOT MATCHED and the
   explicit per-pair rejection reasons are preserved in `candidate_pair_inventory.csv` and `unmatched_reason_summary.csv`.
5. **D-070 FINAL APPROVED** — several geometries from one material-condition family are not independent material observations.
   Family-weighted summaries are essential and are **preferred for the WP6 penalty handoff**.
6. **D-079, D-080 FINAL APPROVED AS PRE-REGISTERED** — the direct-support threshold stays at **at least 3 independent families
   from at least 2 publications**, and is **not lowered after seeing that no individual geometry satisfies it**. Therefore no
   individual miniature geometry is DIRECTLY SUPPORTED; seven are WEAKLY SUPPORTED; two are UNSUPPORTED BY THIS DATASET. **This
   negative evidence is part of the result.**
7. **WP6 central size-correction scenario APPROVED, AS WEAKLY SUPPORTED ONLY** (D-083): the pooled family-weighted bias
   **−3.5 °C** and pooled family-weighted SD **11.4 °C**, from **7 independent families in 5 studies**, status **WEAKLY
   SUPPORTED**. The sign convention stays exactly as D-078 defines it, ΔT_size = T41J(normalized smaller-specimen estimate) −
   T41J(matched full-size curve); **WP6 must not silently reverse it**. This pooled distribution is **not** a geometry-specific
   law, **not** pure material scatter, **not** an ASTM uncertainty and **not** directly supported for every miniature geometry.
   It is the best empirical pooled penalty this dataset provides after the pre-registered primary filters.
8. **WP6 conservative sensitivity REQUIRED** (D-083): the all-STRICT matched result, family-weighted mean about −10.8 °C and SD
   about 21.1 °C from **10 independent families**, is a required WP6 sensitivity. WP6 must read the exact regenerated values,
   not these rounded figures, and must **report whether the headline full-size-versus-miniature conclusion changes** when the
   primary pooled penalty is replaced by it. **Neither is chosen because it produces a preferred answer.**
9. **Normalization-method bias sensitivity REQUIRED FOR WP6 PLANNING** (D-087, D-089): WP5 found the residual spread relatively
   stable across several defensible temperature-correction formulas while the central bias moved materially with the chosen
   published normalization. That is preserved as a **methodological uncertainty**. WP6 planning must consider how to represent
   the size-correction bias sensitivity across the pre-declared methods **without double-counting the residual SD**. **That
   modelling choice is not resolved at CP4; it is a WP6 planning decision.**
10. **Product-form evidence APPROVED** (D-081): plate has enough matched evidence for its own descriptive result; forging and
    weld metal do not. **No standalone forging or weld correction distribution is created.** The plate-only result may be
    carried into WP6 as a sensitivity or diagnostic if useful, but **must not replace the pooled central result without
    explicit justification**.
11. **Irradiation APPROVED** (D-081): the dataset does **not** support a reliable separate irradiated size correction. **No
    separate irradiated penalty is estimated from two families**, and it is **not assumed** that irradiation and geometry do not
    interact. Irradiation stays an explicit limitation and sensitivity concern.
12. **Unsupported geometries** (D-083): `20x5x5 a=0.76` and `23.6x5x5 a=0.78` must **not** be used in the central WP6 comparison
    as though WP5 measured their correction uncertainty. WP6 may (A) omit them from the central analysis and, if scientifically
    useful, (B) include them only in a clearly labelled EXTERNAL/LITERATURE SCENARIO after verifying the external numerical
    assumption and its applicability. **No external correction number is approved yet**; WP6 Plan Mode decides whether such a
    scenario is useful at all.
13. **D-085 FINAL APPROVED AS CHRONOLOGY** — approved precisely because it is transparent. The normalized upper-shelf ratios were
    seen during the feasibility and literature-review stage before D-073 and D-074 were pre-registered. **History is not
    rewritten.** The safeguard is preserved: the primary formulas came from the project brief, the literature and applicability
    reasoning; the alternatives were fixed before any residual comparison; and the primary method was not selected by minimizing
    the final residual.
14. **The remaining WP5 entries** (D-071, D-076, D-077, D-078, D-082, D-084, D-086) contain no contradiction with the above and
    are **FINAL APPROVED**. **D-087** is FINAL APPROVED as the record of results.
Not authorized by this approval: WP6 work of any kind, the Monte Carlo simulator, the fixed-material-volume comparison,
calibrating or choosing a WP6 scatter model, adopting any external size-correction number, and any change to WP0–WP5 code, data
or generated outputs.

**Sources cited in WP5** (what was actually read is stated; nothing below is cited from memory)
- [NUREG/CR-6379] Sokolov M.A., Alexander D.J. (1997). *An Improved Correlation Procedure for Subsize and Full-Size Charpy Impact
  Specimen Data.* NUREG/CR-6379, ORNL-6888, Oak Ridge National Laboratory (HSSI Report 14), doi:10.2172/463630. **Full report read**
  (311-page scanned PDF from OSTI, rendered page by page; the abstract alone was cited in WP3). Used: Introduction and Materials
  (p. 1), Fig. 1 specimen types 1–5 (p. 4), Eq. (2) (p. 12), Eq. (3) and the review of Corwin, Lucas, Louden and Kumar (p. 14),
  Fig. 12 dimension definitions and Table 2 normalization-factor ratios (p. 15), Eq. (7) Kayano's Q, the 200 J upper-shelf limit
  and Eq. (8) (p. 16), Table 3 measured USEs (p. 17), Eqs (9)–(12) and the percent-shear procedure (p. 22), Table 4 shear
  sensitivity and Eqs (13)–(16) (p. 24), Fig. 22, Eq. (17), Eqs (18)–(19) (p. 25), Eqs (20)–(22) and Fig. 27 (p. 28),
  Figs 28–29 (p. 30), Figs 36–37 (p. 34), Summary and Conclusions (pp. 29, 35).
- [LuconNIST] Lucon E., McCowan C.N., Santoyo R.L. *Overview of NIST Activities on Sub-size and Miniaturized Charpy Specimens:
  Correlations with Full-Size Specimens and Verification Specimens for Small-Scale Pendulum Machines.* Journal of Pressure Vessel
  Technology; NIST open copy, publication id 918008 (tsapps.nist.gov). **Full text read.** Used: the CVN / SCVN / MCVN definitions
  and the KLST and RHS dimensions (p. 3), footnote 3 on B being the dimension parallel to the notch, Eqs (2)–(5) temperature
  shifts (pp. 9–11), Eqs (6)–(9) energy densities (pp. 11–12), Eq. (10) and NF1–NF7 (p. 13), Eqs (11)–(12) (p. 14), Conclusions
  1–7 (pp. 16–17), and the primary-source reference list (pp. 18–19).
- [STP1380] Lucon E., Chaouadi R., Fabry A., Puzzolante J.-L., van Walle E. (2000). *Characterizing Material Properties by the Use
  of Full-Size and Subsize Charpy Tests: An Overview of Different Correlation Procedures.* ASTM STP 1380:146–163.
  **Not read** (paywalled). Its two results used here are taken from sources that tabulate them: the KLST upper-shelf relation
  USE_CVN = 29.454·exp(0.2378·USE_KLST) ([LuconNIST] Eq. 12) and the temperature shift M = 92.7 − 14.34·ln(B b²)
  (dataset descriptor Table 3; [ML2026] Table 2). Cited as second-hand and labelled as such wherever it is used.
- [ML2026] Kasala Sreenivasulu Y., Lee I., Merickel J.W., Xu F., Tang Y., Rittenhouse J.E., Vakanski A., Song R. (2026).
  *Machine Learning-based Correlation of Charpy Impact Properties Between Sub-sized and Standard-sized Specimens for Nuclear
  Structural Materials.* Scientific Reports 16:16202; arXiv 2607.10412. **Full text read** (arXiv PDF). By the authors of this
  project's dataset and its descriptor. Used: §1 limitations of analytical methods, §2.2 the Louden and Wallin physical pictures,
  §2.3 Tables 1 and 2 of analytical USE and DBTT correlations, §3.1 dataset and matching definition and Table 3 geometries,
  §3.2 Eqs (4)–(7) their transformation, §4.1 Tables 4 and 5 analytical performance, §4.2 Tables 6–8 machine-learning performance.
- [descriptor] (listed at the head of this file). WP5 read its specimen-size-effect section in full: "Specimen size effect",
  "Correlation of Upper Shelf Energy" and Table 2, "Correlation of Ductile-to-Brittle Transition Temperature" and Table 3.
- [E2248-18] (listed under WP3 sources). WP5 re-read §1.1, §1.2, §1.3, §1.5 and §5.2 from the publisher's scope and abstract pages.
- Cited only through [NUREG/CR-6379], [LuconNIST], [descriptor] and [ML2026], and **not read**: Lucas et al. (1986, ASTM STP 888
  and Fusion Technology 10), Corwin et al. (1984 J. Nucl. Mater. 122–123 and 1986 ASTM STP 888), Louden et al. (1988 J. Nucl.
  Mater. 155–157), Kayano et al. (1991 J. Nucl. Mater. 179–181), Kurishita et al., Towers (1983 TWI RR 219/1983; 1986 Metal
  Construction), Wallin (1994 Jernkontorets Forskning 4013/89), Curll (1959), Uehira et al., Rosinski et al., Schubert et al.
  Every equation taken from them is quoted from a source that was read, and the second-hand route is stated at the equation.
- [ref107] Schill R.H., Forget P., Catherine C.S. (2013). *Correlation between Charpy-V and sub-size Charpy tests results for an
  un-irradiated low alloy RPV ferritic steel* (dataset ref 107). Read only through a search-result summary of its specimen
  description: "27 mm × 3 mm × 4 mm KLST specimens with a 60° notch angle, 1 mm depth, notch radius R = 0.1 mm, and distance
  between anvils of 22 mm". The full text was not accessible; this is used only as corroboration in D-072.

## D-068 — What must agree before two curves are one material and condition at two specimen sizes
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision** (`MATCH_FIELDS` in `src/wp5_pairs.py`). A smaller-specimen curve and a full-size curve are treated as the same
material in the same condition, measured at two specimen geometries, only if **every** field below agrees:
material family; material designation `material_std` (specification, type/grade, class where stated, weld-metal label); product
form; heat chemistry `composition_signature` (all reported elements — the heat/lot proxy, because the dataset has no heat or lot
identifier, D-033); irradiation status as resolved in D-021; fluence (the exact reported value, D-036); irradiation temperature;
irradiation time; treatment; post-treatment temperature and time; cooling method and rate; test-condition statement (HAZ location,
reconstituted specimen, welded area, striking velocity); reconstituted-specimen tag (D-033); specimen orientation.
A field blank on **both** sides counts as agreement — within one publication it means the publication reported it for neither
curve, which is consistent, not contradictory. A field blank on **one** side is a provenance gap. A recorded **disagreement** in
any field rejects the pair, and the first disagreeing field in the order above is recorded as the reason.

**Why.** These are the WP2 grouping variables of D-033 minus specimen geometry, which is the intended substantive difference.
Sharing a material name is not enough: "SA533B" spans different heats, product forms, heat treatments, irradiation histories,
laboratories and publications, and a pair matched on the name alone would confound all of those with the specimen-size effect.
[ML2026] §3.1 matched on the same principle, selecting "only the sub-sized specimen data for which corresponding experimental
results from full-sized specimens are available in the original publications", the full-size set being one "produced under the
same manufacturing and heat treatment conditions and tested using the same test protocol".
**Alternatives.** (1) Match on material family and irradiation status only. (2) Match on the dataset's own curve ID.
**If an alternative were chosen.** (1) would admit hundreds of cross-heat, cross-laboratory pairs whose transition-temperature
differences are mostly material and study differences, and would make the residual an estimate of between-study variation rather
than of a specimen-size effect. (2) would inherit the curve IDs that mix geometries and conditions (D-022, D-028).

## D-069 — Match-quality classes, fixed before any normalization result existed
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** Four classes, decided from provenance metadata alone:
- **STRICT** — same publication, no recorded disagreement, and no one-sided gap in the identity-critical fields (material family,
  material designation, product form, heat chemistry, irradiation status, fluence, test-condition statement, reconstituted tag).
- **PARTIAL** — same publication, no recorded disagreement, but at least one identity-critical field is reported for only one of
  the two curves.
- **CROSS-STUDY** — no recorded disagreement, but the two curves come from different publications.
- **NOT MATCHED** — at least one recorded field disagrees.
Only STRICT pairs enter the primary analysis. PARTIAL pairs would be reported as a clearly labelled secondary set; CROSS-STUDY
pairs are never primary. **A class is never upgraded after seeing that a pair's curves happen to normalize onto one another.**

**Why same-study is required for the primary analysis.** D-032 already established that this dataset's recorded columns do not
always identify heat or condition, and that between-laboratory, machine and calibration differences are real and unmeasurable
here (brief §3). A cross-publication pair therefore mixes those differences into what would be reported as a specimen-size
residual. The same reasoning that keeps a curve inside one publication keeps a primary size comparison inside one publication.
**Consequence, and it is a real cost.** The dataset has no heat identifier, so the only heat proxy is the reported composition,
and compositions are almost never reported identically by two publications. In practice this makes the CROSS-STUDY class empty
(0 of 4,824 candidate pairs) rather than merely secondary: every cross-publication pair is rejected on a recorded composition
difference. Genuinely matched cross-study pairs may exist in the literature and are invisible to this dataset.

## D-070 — The unit of independence is the material-condition family, not the pair
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** A **matched material-condition family** is one publication, one material designation, one product form, one heat
chemistry, one irradiation condition and one test-condition statement — that is, one full-size curve and every smaller-geometry
curve matched to it. Family ID `R<ref>-<full-size curve>-<irradiation condition>`. Several smaller geometries matched to one
full-size curve give several **geometry comparisons** of **one** material observation. Every summary statistic is therefore
reported twice: **comparison-weighted** (each comparison counts once) and **family-weighted** (each family contributes the mean
of its comparisons, then each family counts once). Counts of both are printed beside every number.
**Why.** Treating four geometries of one plate as four independent observations would understate the spread of the size
correction across materials, which is exactly the quantity WP6 needs. **Alternative.** Report comparison-weighted statistics
only. **If chosen.** One material with many geometries would dominate the headline uncertainty invisibly.

## D-071 — Which published curves the size analysis may use
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** The CP2-frozen **primary** cohort only (170 curves; `outputs/wp2/cohort_membership.csv`, verified against
`data/FROZEN_COHORTS_CP2.csv` before anything is read, D-039). No cohort is regenerated, loosened or tightened for WP5. The
secondary populations stay out of the primary size analysis: SA508 Gr.1A piping (D-027), additively manufactured SA508 (D-034,
whose permitted use as "secondary evidence in the WP5 specimen-size analysis if scientifically useful" is **not** taken up — its
only geometry, 24.1 × 4.8 × 4.8 mm RHS, has no full-size partner in its own publication, so it would add no comparison),
source-contradicted labels (D-031) and unresolved irradiation labels (D-035).
**Consequence.** The two 55 × 10 × 6 mm curves of ref 18 — the only ASTM E23-type sub-size specimens (reduced thickness, standard
length) anywhere in the data — have 4 points each and fail every WP2 rule, so they are not in any cohort. **This dataset
therefore contains no usable E23-type sub-size curve at all**, and WP5's smaller-specimen evidence is entirely miniaturized
(MCVN) evidence. [E2248-18] §1.5 and [LuconNIST] both insist the two classes are not interchangeable; nothing here is presented
as evidence about E23-type sub-size specimens.

## D-072 — Which recorded dimension is the notched one for the KLST specimens of refs 107 and 109
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Context.** D-008 fixed the convention: `width_mm` (W) is the dimension the notch is cut into and the crack grows through;
`thickness_mm` (B) is the dimension parallel to the notch; ligament b = W − a. The dataset records the KLST-type specimens of
refs 107 and 109 as length 27 mm, **width 3 mm, thickness 4 mm**, notch depth 1.0 mm, notch angle 60°, root radius 0.1 mm. Read
literally under D-008 this gives a ligament of 2 mm and a notch depth to width ratio a/W = 0.33.

**Decision.** For these records the notched dimension is the 4 mm one: **W = 4 mm, B = 3 mm, ligament b = 3 mm, a/W = 0.25**.
No raw value is altered and no measurement is changed; this is a decision about which of two recorded dimensions is which, made
because three independent authorities define the specimen and all three agree:
1. [LuconNIST] p. 3: "The most popular MCVN specimen type is designated KLST (from the German Kleinstprobe), and has thickness
   B = 3 mm, width W = 4 mm, notch depth N = 1 mm and length L = 27 mm", with B defined in that paper as the dimension parallel
   to the notch — this project's `thickness_mm`.
2. [NUREG/CR-6379] Fig. 1 type 4: 26 mm long, cross-section drawn as 4.0 mm in the notched direction and 3.0 mm across, notch
   depth 1.0 mm, 60°, span 22 mm; p. 29 states "a/W = 0.25" for type 4 and "the specimen thickness is only 3 mm as compared to
   5 mm for type 3". Its Table 2 ratio for type 4, Bb² = 23.7, is reproducible only with B = 3 and b = 3 (10 × 8² / (3 × 3²) =
   23.7); with B = 4 and b = 2 it would be 40.0. `src/wp5_normalization.py::self_checks` reproduces all of Table 2 to 0.3 %.
3. [ref107] describes its specimens as "27 mm × 3 mm × 4 mm KLST specimens with a 60° notch angle, 1 mm depth, notch radius
   R = 0.1 mm, and distance between anvils of 22 mm" — a KLST by name, with the same 22 mm span as NUREG's type 4. The paper's
   "3 mm × 4 mm" states the cross-section without saying which dimension is notched, which is exactly the ambiguity the dataset
   resolved one way and the standard resolves the other.
Implemented as `SWAPPED_WIDTH_THICKNESS` in `src/wp5_normalization.py`, applied only to the exact dimension tuple
(27.0, 3.0, 4.0, 1.0) and recorded per curve in the outputs.

**Why this is not a free choice.** A 1 mm notch leaving a 2 mm ligament is not a KLST and matches no specimen in [E2248-18],
ISO 14556 or DIN 50115. The alternative would apply a published correlation to a specimen the publication did not test.
**Alternatives.** (1) Use the dataset's assignment literally. (2) Exclude refs 107 and 109 from WP5.
**Effect of the alternative, quantified and carried as a pre-declared sensitivity (S6, D-075).** Literal reading gives
B b² = 4 × 2² = 16 mm³ against 3 × 3² = 27 mm³, so the energy factor changes from 23.70 to 40.00 (×1.69) and the Sokolov shift
from 48.2 °C to 40.3 °C (−7.9 °C). Excluding refs 107 and 109 would remove the only KLST comparison in the study.
**Chronology, stated plainly.** This decision was made during the WP5 literature review, before `src/wp5_size_effect.py` existed
and before any residual was computed, on the three sources above. A scoping feasibility calculation made at the same time
(D-085 step 1) showed that the corrected reading also happens to place the normalized KLST upper shelf close to its paired
full-size upper shelf; **that observation played no part in the decision**, and the literal reading is regenerated on every run
as S6 so the reader can see both.

## D-073 — Primary energy normalization: the ligament (nominal fracture) volume B b²
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** Absorbed energy is mapped into the full-size-equivalent domain by the scalar ratio of nominal fracture volumes:

&nbsp;&nbsp;&nbsp;&nbsp;**E_fse = NF_E × E_measured,&nbsp;&nbsp; NF_E = (B b²)_full-size / (B b²)_smaller = 640 mm³ / (B_s b_s²)**

where B is the specimen thickness (mm, the dimension parallel to the notch), b = W − a the remaining ligament (mm), W the
specimen width (mm) and a the notch depth (mm); B b² is the nominal fracture volume (mm³); the full-size reference is
B_f = 10 mm, b_f = 10 − 2 = 8 mm, B_f b_f² = 640 mm³. NF_E is dimensionless and equals exactly 1 for a full-size specimen.
**This is an empirical geometry scaling with a volume interpretation, not a physical law**, and it is not called "volume
scaling" loosely: B b² is the *nominal* fracture volume of Lucas et al., distinct from the *fracture area* B b and from the
(B b)^{3/2} volume measure of Corwin et al., which are carried separately as S1 and S2.

**Source.** Lucas, Odette, Sheckherd, McConnell & Perrin (1986), ASTM STP 888:304–324, and Lucas, Odette, Sheckherd &
Krishnadev (1986), Fusion Technology 10:728–733 — not read directly; quoted identically by four sources that were read:
[NUREG/CR-6379] p. 14 ("Lucas et al. also used an NF equal to the ratio of the FV of full-size to subsize specimens, but
expressed the nominal FV as Bb²"); [LuconNIST] Eq. (10) NF₃; [descriptor] Table 2, which writes it **B(W − A)²** — the notation
the brief's own data description uses; [ML2026] Table 1 (`USE_s · (B_f b_f²)/(B_s b_s²)`).
**Geometry applicability.** Developed for sub-sized bend and Charpy specimens for irradiated-materials testing; it is a
geometry ratio defined for any B and b, and both [LuconNIST] (conclusion 4: "A strong exponential correlation with cross
sectional area was found, in close agreement with the normalization factor based on the ratio of nominal fracture volumes B d²")
and [NUREG/CR-6379] p. 16 ("an NF based on the FV of specimens, namely (Bb²)_full size/(Bb²)_subsize, gives the closest
estimation for each geometry") report it as the best of the purely geometric factors across several geometries.
**Physical idea, plainly.** On the upper shelf the specimen fractures in a ductile way, and most of the energy goes into plastic
work in the material around the growing crack. That deforming region scales with the ligament in all three directions, so the
energy is taken to scale with a volume-like measure B b² rather than with the fracture area alone.

**Why this is the primary method, argued before any residual was computed.**
1. PROJECT_BRIEF.md §5 WP5 requires "absorbed energy is scaled by a measure of the specimen ligament volume", and §6.4 requires
   "the ligament-volume normalization convention adopted, and from which reference". B(W − A)² is the ligament-volume
   convention, and the descriptor of this project's own dataset writes it in exactly that notation. The brief's wording ties
   unambiguously to this one convention; the others are area scaling or a different volume measure, so they are sensitivities.
2. It needs nothing the dataset does not have: only published specimen dimensions.
3. It is independent of the paired full-size curve, so no full-size answer can enter its own correction.
**Alternatives and why not primary.** (B b)^{3/2} (Corwin) and B b (area) are S1 and S2. Louden's B b²/(L K_t) and Kayano's
B b²/K_t′ need an elastic stress-concentration factor and Kayano's plastic factor Q = 1 + (π − θ)/2; published K_t values exist
for a handful of geometries only (five in [ML2026] Table 3, against nine miniature geometries in this cohort), so running them
would mean inventing K_t for most curves — see D-076. Sokolov's own Eq. (11) needs percent shear, which this dataset does not
have at all — D-076. Uehira's and Wallin's USE power laws need exponents calibrated against the full-size USE of the same
material, which is the circularity the brief forbids — D-076.
**If an alternative were chosen.** S1 and S2 quantify exactly that, and the comparison is reported in
`normalization_sensitivity_comparison.csv`.

## D-074 — Primary temperature correction: Sokolov & Alexander Eq. (22)
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** Test temperatures are mapped into the full-size-equivalent domain by adding a shift that depends only on the
smaller specimen's own geometry:

&nbsp;&nbsp;&nbsp;&nbsp;**T_fse = T_measured + M,&nbsp;&nbsp; M = 98 − 15.1 × ln(B b²)&nbsp;&nbsp;[M in °C; B b² in mm³]**

**Source.** [NUREG/CR-6379] Eq. (22) and Fig. 27, applied in the form of their Eq. (17), DBTT_full-size = DBTT_subsize + M.
**Geometry applicability.** Fitted through the four specimen types that report built (types 1–4 of its Fig. 1) plus a point
forced at the full-size specimen: "the equation was forced to give a correction factor of 0 for the full-size specimen". The
report offers it beyond those four types — "the form of the dependence may be used as guidance to estimate size corrections for
subsize specimens" — while stating the limitation in the same sentence: "Deviations from this dependence reflect the constraint
effects of different notch dimensions". Materials: A533B plate, A508 class 2, 15Kh2MFA ring forging and HSSI weld 72W, USE
73–330 J, transition temperatures −46 to +58 °C, yield strengths 410–940 MPa.
**Physical idea, plainly.** A bigger specimen contains more material near the notch, so it is more likely to contain the one
weak spot that starts a cleavage crack, and it is also held more rigidly in the through-thickness direction. Both push a bigger
specimen towards brittle behaviour at a given temperature, so its transition sits at a higher temperature. Sokolov & Alexander
derive the log form from that picture: a yield stress that rises as temperature falls (their Eq. 13) meeting a cleavage strength
that falls with stressed volume as V^(−1/m) (Weibull weakest link, their Eq. 14) gives DBTT = 1/(R − S ln V) (their Eq. 16), and
Eq. (22) is the empirical fit of that form to their measured shifts.

**Why this is the primary correction, argued before any residual was computed.**
1. It is the RPV-specific classical convention, from the ORNL/NRC HSSI report that PROJECT_BRIEF.md §11 points to, developed on
   this project's own material family.
2. Its argument is **the same B b² ligament volume as the primary energy normalization**, so one geometric measure drives both
   halves of the mapping instead of two unrelated ones.
3. It is defined for any B b² and carries an identity at full size, unlike the per-type constants of Eqs (18)–(21), which exist
   only for the four specimen types that report built.
4. It is **independent of the paired full-size curve**: M depends only on the smaller specimen's published dimensions and two
   fixed published constants. This is what keeps the residual an out-of-sample test (D-078, D-086 check 7).
5. It comes with a published uncertainty scale for comparison: the ±2σ intervals of Eqs (18)–(21), 20–30 °C.
**Alternatives, all pre-declared as sensitivities (D-075).** Lucon's refit of the same form (S3), Towers's thickness-only
quadratic (S4), Wallin's thickness-only logarithm (S5), and Sokolov's own per-type constants where the geometry is one of his
four types (S7).
**Explicitly NOT used as an input.** A pair-specific shift measured as T0(full-size) − T0(smaller) is *calculated and reported*
as an outcome of the size effect, and is never used to correct the curve it was measured from. Doing so would align each
smaller curve to its own partner and then report the resulting agreement as evidence that the correction works, which is
circular; it is also, in a different form, what [ML2026] Eq. (5) does to build its training targets, which is legitimate for
supervised learning and illegitimate as an uncertainty estimate.
**If an alternative were chosen.** At the cohort's smallest geometry (B b² = 2.05 mm³) the four shifts differ by tens of
degrees; `normalization_sensitivity_comparison.csv` reports the spread of the residual across all of them.

## D-075 — Pre-declared sensitivity normalizations
**Status:** FINAL APPROVED AS SENSITIVITY SET (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional
pending CP4

**Decision.** Exactly these seven alternatives are run, chosen now from published methods and their stated applicability, before
any of their residuals is seen. No further method is added later, and the primary method is not replaced by one that performs
better on these data.

| id | what changes | equation | source (read?) |
|---|---|---|---|
| S1 | energy | NF_E = (B_f b_f)^{3/2} / (B_s b_s)^{3/2} | Corwin et al. 1984, 1986 — via [NUREG/CR-6379] p. 14, [LuconNIST] NF₂ (not read directly) |
| S2 | energy | NF_E = (B_f b_f) / (B_s b_s) — fracture area; = Sokolov's NF_brittle, Eq. (10) | [NUREG/CR-6379] Eqs (8)–(10) (read) |
| S3 | temperature | M = 92.7 − 14.34 ln(B b²) | Lucon et al. 2000 [STP1380] — via [descriptor] Table 3 and [ML2026] Table 2 (not read directly) |
| S4 | temperature | M = 0.7 (10 − B)² | Towers 1983, 1986 — via [LuconNIST] Eq. (2), [ML2026] Table 2 (not read directly) |
| S5 | temperature | M = −51.4 ln[2 (B/10)^0.25 − 1] | Wallin 1994 — via [LuconNIST] Eq. (3), [ML2026] Table 2 (not read directly) |
| S6 | geometry | the dataset's literal width/thickness for the KLST records (D-072) | — |
| S7 | temperature | Sokolov's per-type shifts, Eqs (18)–(21): +30 (±28), +53 (±24), +34 (±20), +38 (±30) °C | [NUREG/CR-6379] Eqs (18)–(21) (read) |

S4 and S5 depend on thickness alone and were developed for **sub-size specimens of reduced thickness (SCVN)**; [LuconNIST]
reports that KLST and RHS miniaturized specimens nevertheless "seem to follow the same trend as SCVN specimens", which is why
they are admissible sensitivities and not the primary method. S7 is applied **only** where the geometry matches one of the four
types that report built, on cross-section, notch depth and notch root radius; it is never extrapolated to a geometry the report
did not build (`sokolov_type` in `src/wp5_normalization.py`), and where it does not apply the row says
**"normalization not defensibly established for this geometry"** rather than carrying an invented shift.

## D-076 — Published methods that cannot be run on this dataset, and why
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** Each of the following is named, with its reason, and **not run**. None of its missing inputs is imputed.

1. **Sokolov & Alexander's own proposed procedure, Eq. (11)** —
   E = E_subsize × [NF_brittle·(100 − SHEAR)/100 + NF_ductile·SHEAR/100], with NF_brittle the fracture-area ratio (Eq. 10) and
   NF_ductile the empirical upper-shelf ratio (5.1, 18.3, 6.3, 21.3 for their types 1–4), SHEAR the percent shear fracture on
   each specimen's fracture surface. **The dataset has no shear-fracture-appearance column at all** — 56 columns, none of which
   is shear area, fracture appearance or lateral expansion (`outputs/wp0/data_dictionary.csv`). Shear is not partly missing
   here; it is absent for all 2,588 primary records. It is therefore **not imputed, not derived from test temperature, not
   assumed to be 0 % or 100 %**, and Eq. (11) cannot be run, as primary or as sensitivity. Their Eq. (12), which recovers shear
   from instrumented force–displacement traces, needs F_iu, F_a, F_gy and F_m, which the dataset also does not have.
   **Consequence, stated rather than hidden.** The primary method applies **one** factor to a whole curve, while Sokolov's
   evidence is that the brittle and ductile factors differ by roughly 1.3–2.4× for his four types (NF_brittle 3.77 / 8.52 /
   4.00 / 8.90 against NF_ductile 5.1 / 18.3 / 6.3 / 21.3). A single factor is therefore expected to misfit the lower and upper
   parts of the curve in opposite directions — the failure mode [descriptor] describes ("sub-sized specimens tend to produce
   higher impact energies in the lower shelf region and proportionally lower energies in the upper shelf region") and [ML2026]
   §1 repeats. WP5 measures that misfit (S2 is the pure-area factor, so S2 against the primary brackets it) instead of denying it.
2. **Louden's NF (B b²/L K_t) and DBTT normalization, and Kayano's NF (B b²/K_t′)** — need the elastic stress-concentration
   factor K_t, a function of ligament size and notch root radius whose values the sources tabulate for particular geometries
   only ([ML2026] Table 3 gives K_t, K_t′ and K_t″ for five geometries; this cohort has nine miniature geometries). Running
   them would mean inventing K_t for the rest. Louden's DBTT normalization additionally needs the maximum force P_m from an
   instrumented test, which this dataset does not record. Not run.
3. **Kumar's ΔUSE + USE_p** — needs energies from precracked specimens as well as notched ones. D-020 established that every
   retained curve here is an ordinary Charpy V-notch measurement and that no precracked series survives; there are no USE_p
   values. Not run.
4. **Uehira's m(B b)^n and Wallin's USE power law (b_f/b_s)^m** — their exponents must be calibrated against full-size USE
   values of the same material. That is in-sample calibration against the quantity a size correction is then evaluated on, which
   PROJECT_BRIEF.md §7 forbids. [ML2026] §4.1 illustrates the effect: its best analytical USE variants (R² 0.824 and 0.859) were
   obtained by fitting m and n per publication or per thickness to the same full-size data used to score them, against R² 0.488
   for one uncalibrated fit. Not run, as primary or as sensitivity.
5. **[STP1380]'s KLST upper-shelf relation USE_CVN = 29.454·exp(0.2378·USE_KLST)** ([LuconNIST] Eq. 12) — a material-specific
   dimensional relation for one geometry, not a geometry normalization, and read only second-hand. Reported as an external
   comparison for the single KLST family, never applied as the correction.
6. **Kurishita's a/ρ ≈ 15 rule** — reported as a diagnostic for every geometry, never used as a correction. The cohort's ratios
   are 4.1–10 (miniature) and 8.0 (full-size), so no geometry meets the condition under which that rule says no shift is needed.

## D-077 — The full-size-equivalent fitting rule
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** The transformed points (T_fse, E_fse) of a smaller-specimen curve are fitted with the **unchanged approved WP3
functions** (`src/wp3_fitter.py`: `fit_curve`, `index_temperature`, `index_fraction_of_rise`, `classify`,
`criterion_bracketing`), using the **full-size convention of D-042: LSE fixed at 2.7 J**, with USE, T0 and C fitted, and with
bounds and starting values derived from the transformed data exactly as D-041 defines them. T41J is then taken from the analytic
crossing under the unchanged D-044 rules, including the tested-range rule applied to the **transformed** tested temperatures, and
carries the same two support diagnostics (index position on the fitted rise; empirical bracketing of 41 J by the transformed
energies). The resulting row is labelled **"transformed estimate of full-size-equivalent behaviour derived from published
smaller-specimen measurements"** and is never called a measurement.
**Why the full-size shelf convention.** After mapping, the points are estimates of full-size-equivalent behaviour, so the
convention that D-042 approved for full-size curves is the consistent one; keeping the miniature convention (fitted LSE) would
leave a fitting-method difference inside the size comparison and confound it with the size effect. It also matters mechanically:
15 of the cohort's 36 miniature curves are classed boundary-limited only because their fitted lower shelf rests on its 0 J bound
(D-046), which is an artefact of the miniature convention and cannot occur once the shelf is fixed.
**Note on what this changes.** The energy normalization multiplies every energy by one constant, but the 2.7 J lower shelf is
**not** scaled with it: 2.7 J is the full-size shelf convention and the transformed curve lives in the full-size domain. The
transformed lower shelf is therefore not a scaled version of the miniature one, and the difference is visible in the fits.
**Alternatives.** (1) Fit the transformed points with the miniature convention. (2) Scale the raw miniature fit's parameters
analytically instead of refitting. **If chosen.** (1) mixes a method difference into the residual; (2) would not reapply the
tested-range and support rules, and would hide that the transformed curve can fail them.

## D-078 — The residual size-effect quantity and its sign
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** For every matched geometry comparison the primary residual is

&nbsp;&nbsp;&nbsp;&nbsp;**ΔT_size = T41J(normalized smaller specimen, full-size-equivalent) − T41J(measured full-size curve)&nbsp;&nbsp;[°C]**

Both terms come from the same WP3 fitter and the same 41 J criterion. **Sign, locked here before any residual exists:** a
**positive** ΔT_size means the classical correction places the full-size-equivalent transition **warmer** than the measured
full-size curve — the correction over-predicts the transition temperature, which is the conservative direction for a vessel
integrity argument. A negative ΔT_size means it under-predicts, the non-conservative direction.
Secondary residual, available for comparisons where a T41J cannot be formed: **ΔT0 = T0(normalized) − T0(measured full-size)**,
with T0 the tanh mid-transition temperature, which is defined at every specimen size.
Reported as an outcome and never used as an input (D-074): the **observed** pair shift T0(full-size) − T0(smaller specimen, raw),
against the published shift M. This is the cleanest single statement of the measured size effect in this dataset.
**Per comparison the outputs store:** family ID; study; material; heat proxy; product form; irradiation condition and fluence;
smaller geometry and full-size geometry; match-quality class; NF_E and M with the geometry quantities behind them; normalized
predicted T41J; measured full-size T41J; ΔT_size; the WP3 outcome, index-support and bracketing flags of both original curves and
of the transformed refit; the WP4 interval label and width of the full-size curve where one exists; and every applicability flag.
**A perfect scalar normalization would make ΔT_size near zero. It is not forced towards zero, and negative results stay visible.**

## D-079 — Which comparisons enter the primary analysis, and the evidence thresholds
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision, fixed before any residual exists.**
- **PRIMARY analysis set:** match class STRICT, **and** the full-size curve has a WP3 *usable fit* with a calculated T41J,
  **and** the transformed refit is a *usable fit* with a calculated T41J under the same D-046 and D-044 rules.
- **SENSITIVITY sets, reported separately and never merged into the headline:** comparisons whose full-size fit is weakly
  identified or boundary-limited; comparisons whose transformed refit is weakly identified or boundary-limited; comparisons
  whose transformed refit yields no T41J; and any PARTIAL-class comparison.
- The **original** smaller-specimen WP3 outcome is carried on every row but is **not** an inclusion criterion, because it is
  measured under the miniature lower-shelf convention that D-077 replaces (see D-077).
- **Evidence thresholds for reporting a stratum-specific correction** (product form, geometry class, irradiation state):
  a central bias and a scale are reported only with **at least 3 independent matched families from at least 2 publications**.
  Below that the row reads "insufficient matched evidence for a standalone estimate" and the individual comparisons are shown
  instead of a summary statistic. **No SD is printed from two observations.**
- **Evidence status handed to WP6** (D-083): DIRECTLY SUPPORTED = ≥ 3 families from ≥ 2 publications; WEAKLY SUPPORTED = 1–2
  families, or ≥ 3 families from a single publication; UNSUPPORTED BY THIS DATASET = no STRICT matched comparison.

## D-080 — Summary statistics for the residual
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** Every residual summary reports, side by side and each with its counts: N comparisons; N independent families;
N studies; mean signed residual; median signed residual; mean absolute error; root-mean-square error; ordinary standard
deviation (ddof 1); robust scale 1.4826 × median absolute deviation; the 10th, 25th, 75th and 90th percentiles; and the minimum
and maximum with their pair IDs. Each set is given **comparison-weighted** and **family-weighted** (D-070). With fewer than
4 observations the SD and the percentiles are suppressed and the individual values are printed instead. No distribution is
smoothed or fitted; with samples this small the individual points are the honest presentation.

## D-081 — Product-form and irradiation reporting
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** The residual is broken out by the approved harmonized product forms (plate, forging, weld metal; D-013) and by
irradiation state, using the D-079 thresholds. Overall and stratum-specific evidence are always shown side by side, and product
forms are **not** pooled merely to raise N: the pooled row is reported as the pooled row, and the per-form rows are reported with
their own counts, including the rows that say the evidence is insufficient. The primary size normalization does **not** assume
that irradiation and geometry do not interact; whether the matched evidence can resolve an interaction is answered from the
counts, and if it cannot, that is reported as a limitation rather than estimated.

## D-082 — Three uncertainties that must not be confused
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** WP5 keeps these separate and says so wherever a number is reported.
1. **Per-curve fit and sampling uncertainty** (WP4): how well one curve's own index temperature is determined by its own
   specimens. A bootstrap interval width.
2. **Size-correction residual disagreement** (WP5): the spread of ΔT_size across matched comparisons after the classical
   correction has been applied. **This is what WP6 needs.**
3. **Between-material and between-study variation**: differences among matched families, which include real material differences
   and the between-laboratory differences of a 109-publication compilation (brief §3).
**A WP4 interval width is never used as a WP5 size-correction penalty** (PROGRESS.md, author's WP4 decision). Quantity 2 is
**not** claimed to be pure physical specimen-size variance: it contains contributions from 1 and 3, because each ΔT_size is a
difference of two independently fitted curves from heterogeneous published data. **No variance deconvolution is attempted**:
subtracting WP4 variances from the observed residual variance would need the two to be independent and the WP4 intervals to be
calibrated, and D-056 records that the WP4 intervals are nominal, not calibrated. A conservative residual-disagreement estimate
that still contains fit noise is preferred to a falsely precise deconvolution.

## D-083 — What WP5 hands to WP6
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** `wp6_size_correction_handoff.csv`, one row per smaller-geometry class, carrying: the geometry and its B, b, B b²
and NF_E; the central size-correction bias (the family-weighted mean ΔT_size) where the D-079 threshold is met; the residual
size-correction scale, **defined explicitly** as the family-weighted standard deviation of ΔT_size about that bias, in °C, with
the robust 1.4826 × MAD scale beside it; the number of independent matched families and publications supporting it; the product
forms and irradiation states represented; the applicability limits (the 200 J full-size upper-shelf limit of
[NUREG/CR-6379] p. 16 and p. 29; whether the geometry is one of the four types that report built); and the evidence status of
D-079. **Geometry classes are not collapsed into one correction unless the evidence supports it**, and a class marked
UNSUPPORTED BY THIS DATASET is handed to WP6 with that label, so that WP6 must either not simulate it or use a clearly labelled
external literature scenario for it. WP5 does not run WP6, does not compare fixed material volumes and does not choose a
scatter model.

**CP4 decision (author, 2026-09-17): exactly what WP6 carries, and from which regenerated file.** WP6 reads the values from the
outputs, never from rounded prose in this file or in any summary.

| what | value at CP4 | where WP6 reads it |
|---|---|---|
| **CENTRAL scenario, status WEAKLY SUPPORTED** — pooled family-weighted bias | −3.4941546891181936 °C | `wp6_size_correction_handoff.csv`, row `POOLED: all miniature geometries together`, column `central_bias_c` |
| **CENTRAL scenario** — pooled family-weighted residual SD | 11.433714718421587 °C | same row, column `residual_scale_sd_c` (robust 1.4826 × MAD beside it in `residual_scale_robust_c`, 11.337678974122086 °C) |
| **CENTRAL scenario** — supporting evidence | 7 independent families, 5 studies, 10 comparisons | same row, columns `n_families`, `n_studies`, `n_primary_comparisons`, `evidence_status` |
| **CONSERVATIVE sensitivity, REQUIRED** — all-STRICT family-weighted mean | −10.804718715572376 °C | `size_correction_summary_overall.csv`, row `subset` = "all STRICT comparisons with a residual (primary + held as sensitivity)" and `weighting` = "family-weighted (each family's mean counts once)", column `mean_c` |
| **CONSERVATIVE sensitivity** — all-STRICT family-weighted SD | 21.08698664047987 °C | same row, column `sd_c` (robust scale 19.903817963325263 °C in `robust_scale_1p4826_mad_c`) |
| **CONSERVATIVE sensitivity** — supporting evidence | 10 independent families, 5 studies, 17 comparisons | same row, columns `n_families`, `n_studies`, `n` |

**Rules attached to the handoff.**
- The **sign convention is D-078's and is not reversed**: ΔT_size = T41J(normalized smaller-specimen estimate) −
  T41J(matched full-size curve). Positive means the correction places the transition warmer than the measured full-size curve.
- The pooled central scenario is **WEAKLY SUPPORTED, not DIRECTLY SUPPORTED**. It is **not** a geometry-specific law, **not**
  pure material scatter, **not** an ASTM uncertainty, and **not** directly supported for every miniature geometry. Every WP6
  table and figure that uses it states that.
- **No individual miniature geometry is DIRECTLY SUPPORTED** (0 of 9), so WP6 may not apply a geometry-specific correction
  uncertainty from this dataset. The per-geometry biases in the handoff are descriptive only.
- WP6 **must** run the conservative sensitivity and **must report whether the headline full-size-versus-miniature conclusion
  changes** when the central penalty is replaced by it. Neither is selected because it gives a preferred answer.
- The two geometries marked UNSUPPORTED BY THIS DATASET (`20x5x5 a=0.76`, `23.6x5x5 a=0.78`) are **excluded from the central
  WP6 comparison**. WP6 may (A) omit them entirely or (B) include them only in a clearly labelled EXTERNAL/LITERATURE SCENARIO,
  after verifying the external number and its applicability. **No external correction number is approved at CP4**; whether such
  a scenario is useful at all is a WP6 Plan Mode decision.
- The plate-only result (4 families, 3 publications) may be carried as a sensitivity or diagnostic; it **must not replace the
  pooled central result without explicit justification**. No standalone forging or weld-metal correction distribution exists.
- No separate irradiated penalty is handed over, and WP6 must not assume irradiation and geometry do not interact (D-081).

## D-084 — Does the normalization actually help? The before/after test
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** For every matched comparison and for the set as a whole, three metrics are reported **before** and **after**
normalization, with the count that improved and the count that worsened:
1. **Transition temperature:** |T0(smaller, raw WP3 fit) − T0(full-size)| before, against |T0(normalized refit) − T0(full-size)|
   after. T0 is used because it is defined at every specimen size, whereas a raw miniature curve has no 41 J index (D-045).
   Where both T41J values exist, the same comparison is also given on T41J.
2. **Upper-shelf energy:** (USE_smaller − USE_full)/USE_full before, against (USE_normalized − USE_full)/USE_full after.
3. **Curve-level energy:** the root-mean-square difference between the smaller curve's fitted energy and the full-size curve's
   fitted energy, expressed as a fraction of the full-size fitted USE, evaluated **only over the temperature interval where both
   curves have measured support** — the overlap of the full-size tested range with the smaller curve's tested range (raw for
   "before", transformed for "after"). Where the overlap is empty the row says so and no number is produced; the normalized curve
   is never evaluated where one member of the pair has no data.
**Negative results stay visible.** If the normalization leaves agreement unchanged or makes some pairs worse, that is the
finding and it is reported as such, per comparison and in the summary.

## D-085 — How the WP5 method was arrived at (chronological, including anything learned before pre-registration)
**Status:** record. FINAL APPROVED AS CHRONOLOGY (CP4, author 2026-09-17). Earlier: record; PRE-REGISTERED (WP5) for
steps 1–2; extended as work proceeds. No step is rewritten later.

1. *State reconstruction and literature review, before any WP5 code existed.* The approved state was verified (raw-data
   checksums, the 14 CP2 cohort fingerprints, the 170/2,588 primary cohort, the WP3 outcome counts 0/0/18/35/13/104 and the WP4
   interval accounting). The sources listed at the head of this section were then read, the full NUREG/CR-6379 report first.
   **Two things were computed during that review, before any decision below was written, and both are recorded here because they
   could in principle have influenced a choice:**
   a. *Feasibility check required by the brief's own structure:* whether a normalized miniature curve can support a 41 J index
      at all. Multiplying each matched miniature curve's WP3 upper shelf by its B b² factor gives full-size-equivalent upper
      shelves of roughly 79–305 J, all above 41 J, so the index is computable in principle and WP5 is not futile. This is a
      feasibility fact about the method, not a residual.
   b. *Observed while doing (a):* the ratio of those normalized upper shelves to the paired full-size upper shelves, which is a
      result and not merely a feasibility fact. It is recorded here that this was seen before D-073 and D-074 were written.
      **Neither choice rests on it.** D-073 follows PROJECT_BRIEF.md §5 and §6.4, which name the ligament-volume convention, and
      the four read sources that write it B b² or B(W − A)²; D-074 follows the RPV-specific report the brief's §11 points to and
      the requirement that the correction be independent of the paired full-size curve. The alternatives are all carried as
      pre-declared sensitivities (D-075), so a reader can see what any other choice would have given.
2. *Pair inventory, committed before any normalization existed* (commit `6d2aba0`): `src/wp5_pairs.py` and its outputs. Match
   classes (D-068, D-069) were defined and applied before `src/wp5_size_effect.py` was written.
3. *Pre-registration commit* (`e160fe3`): D-068 to D-086 and `src/wp5_normalization.py` (the literature equations and their
   self-checks), committed before any normalization residual, refit or before/after metric existed.
4. *Implementation and results* (`src/wp5_size_effect.py`, `src/wp5_tests.py`). Everything that determines a residual — the two
   primary equations, the seven sensitivities, the full-size-equivalent fitting rule, the match classes, the primary analysis
   set, the evidence thresholds, the sign convention and the summary statistics — was already fixed in step 3 and none of it
   changed. Changes made after the results existed, recorded as such:
   a. *Reporting only:* the stratified summaries now emit both weightings per stratum instead of one merged row; the WP6 handoff
      gained a POOLED row and suppresses a standard deviation below 4 families, which applies D-080's existing rule that the
      pre-registered text already stated; the WP4 interval label of the full-size curve is carried on every comparison for
      reporting (it is never used as a size penalty, D-082).
   b. *Figures only:* geometries ordered by ligament volume, rotated axis labels, and one panel added to the performance figure
      showing the published shift against the observed pair shift (a quantity D-078 had already declared as an outcome).
   c. *Corrected in the generated text:* the count of miniature geometries matching a NUREG/CR-6379 specimen type was written
      from a wrong expression and printed 5, then 1 in a limitation; recomputed from the geometry table it is 6 of 9. No number
      used in an estimate was affected.
   No estimator, normalization, threshold, match class, sign convention, inclusion rule or cohort changed.

## D-086 — Software and sanity checks that must pass before any WP5 number is trusted
**Status:** FINAL APPROVED (CP4, author 2026-09-17). Earlier: PRE-REGISTERED (WP5); provisional pending CP4

**Decision.** These run on every execution (`src/wp5_normalization.py::self_checks` and `src/wp5_size_effect.py`), and a failure
raises and stops the pipeline rather than producing numbers.
1. **Dimensions.** B b has units mm², B b² mm³; every NF_E is a ratio of like quantities and so dimensionless; every shift is in
   °C; ln(B b²) takes mm³, the unit the published constants were fitted in.
2. **Identity.** Feeding the full-size geometry into every energy normalization must give NF_E = 1 exactly. Towers's and
   Wallin's shifts must give exactly 0 at B = 10 mm; Sokolov's and Lucon's, whose published coefficients are rounded, must give
   |M| ≤ 0.5 °C (they give +0.43 and +0.04 °C), and the source states the fit was forced through zero there.
3. **Hand calculation.** One geometry is worked by hand in the generated documentation so a reader can repeat it with a
   calculator.
4. **Round trip.** Dividing back by NF_E and subtracting M returns the measured values to machine precision.
5. **No-op shift.** A geometry whose published shift is zero leaves the temperatures unchanged.
6. **Reproduces the published source.** Recomputing NUREG/CR-6379's Table 2 ratios (B b, B b², (B b)^{3/2} for its types 1–4)
   from the type dimensions must match the printed values; this checks the equations *and* the convention for which dimension is
   notched. Achieved to 0.3 %.
7. **Pairing audit.** Every primary matched comparison must be reconstructable from the source metadata: the inventory carries
   the field-by-field comparison for all 4,824 candidate pairs.
8. **Leakage check.** The correction applied to a smaller curve must be a function of that curve's own published dimensions and
   fixed published constants only. Verified numerically on every run by recomputing NF_E and M from the geometry alone and
   requiring an exact match with the values used, and structurally by `normalize()` taking no full-size-curve argument.
9. **Raw data immutability.** `data/raw/` checksums are verified by WP0 on every pipeline run; WP5 writes nothing outside
   `outputs/wp5/`.
10. **Frozen cohorts.** The CP2 membership check runs before WP5 reads anything.

## D-087 — What the analysis found (results; the method above was fixed before any of this existed)
**Status:** record of results. FINAL APPROVED (CP4, author 2026-09-17). Earlier: PROPOSED (CP4) — the author decides at
CP4 what WP6 may carry forward; decided as recorded in the CP4 approval record above.

**Matched evidence** (`pair_data_sufficiency.md`, `wp5_summary.md` §2). Of 4,824 enumerated candidate pairs, **18** are STRICT
matched geometry comparisons, from **10** independent material-condition families in **5** publications (refs 53, 55, 59, 60,
107). **0** PARTIAL and **0** cross-study. **10** comparisons from **7** families in **5** publications reach the pre-registered
primary analysis set; 8 are held as sensitivity. 8 of the 9 miniature geometries reach at least one STRICT comparison.

**Primary residual** (`size_correction_summary_overall.csv`). ΔT_size, primary analysis set: comparison-weighted mean −3.5 °C,
median −3.7, MAE 13.9, RMSE 16.2, SD 16.7, robust scale 19.5, range −33.8 to +18.3 °C (10 comparisons); family-weighted mean
−3.5 °C, median −5.0, MAE 9.5, RMSE 11.1, **SD 11.4 °C**, robust scale 11.3 (7 families). Over all 17 STRICT comparisons with a
residual: family-weighted mean −10.8 °C, SD 21.1 °C (10 families).

**No geometry class reaches the D-079 threshold** (`size_correction_summary_by_geometry.csv`, `wp6_size_correction_handoff.csv`):
0 of 9 are DIRECTLY SUPPORTED, 7 are WEAKLY SUPPORTED (1–3 families each, and where there are 3 they come from one publication),
2 are UNSUPPORTED BY THIS DATASET. Product form: plate is the only stratum meeting the threshold (4 families, 3 publications;
family-weighted mean −2.2 °C, SD 14.6); forging (2 families) and weld metal (1 family) do not. Irradiation: unirradiated meets it
(5 families, 4 publications; mean −1.7 °C, SD 12.8); irradiated (2 families) does not, so **no separate irradiated correction is
estimated and no interaction between irradiation and geometry is claimed either way**.

**The normalization does help** (`before_after_normalization_metrics.csv`). Median |T0 difference| 66.9 → 16.2 °C; median
|relative USE difference| 0.96 → 0.24; median curve-level RMS energy difference over the shared supported range 0.46 → 0.26 of
the full-size USE. 8 of 10 comparisons improved on T0, 9 of 10 on USE, 8 of 10 on the curve-level metric.

**The two failures are both ref 55**, the same severely embrittled low-toughness A533B plate (full-size USE 51–63 J, T41J +115
and +214 °C). For those pairs the measured shift runs the wrong way — T0(full-size) − T0(smaller) = −35.5 and −2.2 °C, i.e. the
miniature specimens transitioned at or above the full-size temperature — so adding a positive published shift makes the
agreement worse. Reported, not removed. For the other 8 comparisons the published shift lands within 30 °C of the shift the
matched pair actually shows, over observed shifts of 35–90 °C.

**Sensitivity** (`normalization_sensitivity_comparison.csv`). The central bias moves a great deal with the convention and the
scatter barely moves: family-weighted mean −3.5 (primary), −4.5 (Corwin (Bb)^{3/2}), −6.6 (Lucon), −18.0 (Wallin), −23.2 °C
(Towers), with family-weighted SD 11.1–11.9 °C throughout; the two volume-type energy normalizations are nearly
indistinguishable. Pure fracture-area energy scaling (S2) gives mean +42.9 °C and SD 42.1 °C, the expected result of applying
Sokolov's *brittle* factor to a whole transition curve. The KLST geometry reading (S6) moves the pooled mean by 0.5 °C.

**Systematic over-prediction of the upper shelf.** The normalized USE exceeds the matched full-size USE in 16 of 18 comparisons,
by a median factor of about 1.19 (range 0.98–1.93). This reproduces NUREG/CR-6379's own observation (p. 16) that the B b²
factor gives estimates "slightly higher than empirical ratios for each specimen geometry".

**Against published values** (`wp5_summary.md` §10). NUREG/CR-6379's own ±2σ intervals on its per-type shifts are 20–30 °C
(σ 10–15 °C); [ML2026] Table 5 reports RMSE 45.8 °C for Sokolov's correction and 35.5 °C for the best classical method it
benchmarked, on 27 SA533B sub-size sets, against 24.9–27.2 °C for its trained models. This project's family-weighted SD of
11.4 °C (primary set, 7 families) to 21.1 °C (all STRICT, 10 families) sits inside that range.

**Checks** (`wp5_check_results.csv`, `normalization_self_checks.csv`). All 9 independent checks and all 12 normalization
self-checks pass, including the reproduction of NUREG/CR-6379's Table 2 ratios for its four specimen types to 0.3 %.

**Nothing was tuned on these results.** The method, the match classes, the primary analysis set, the evidence thresholds, the
sign convention and the seven sensitivities were all committed in `e160fe3` before `src/wp5_size_effect.py` was written.
Changes made after the results existed, recorded as such (D-085 step 4): the counts of miniature geometries matching a
NUREG/CR-6379 specimen type were corrected in the generated summary text from a wrong expression to the table's own value (6 of
9); figure ordering, label rotation and one added figure panel (the published shift against the observed pair shift); the
stratified summaries were changed to emit both weightings per stratum instead of one; the WP6 handoff gained a pooled row and
suppressed standard deviations below 4 families, applying D-080's existing rule that the method text already stated. No
estimator, normalization, threshold, match class, sign convention or inclusion rule changed.

## D-088 — The CP4 approval session changed documentation only (verification record)
**Status:** record. FINAL APPROVED (CP4, author 2026-09-17)

**What was done.** The author's CP4 decisions were recorded: the CP4 approval record at the head of this section, the status
line of every WP5 entry (D-068 to D-087), the D-075 heading wording, the D-083 handoff table and its attached rules, and this
entry and D-089. `PROGRESS.md` and `README.md` were updated to the approved status. **No executable code was changed**, so no
analysis was rerun beyond the lightweight WP5 checks; the full `./run_all.sh` reproducibility run of the CP4 state (exit 0 in
10 min 18 s, 0 tracked output files changed) stands (author's CP4 verification instruction 7).

**Verification performed before the merge.**
1. *Branch base.* `git merge-base wp5 main` equals `main` (`0b5dad6`, the approved WP4 state): `wp5` is a clean descendant with
   no divergence.
2. *Primary analysis set unchanged:* 10 comparisons, 7 independent families, 5 studies.
3. *Direct-support threshold:* 0 of 9 geometry classes DIRECTLY SUPPORTED; 7 WEAKLY SUPPORTED; 2 UNSUPPORTED BY THIS DATASET
   (`20x5x5 a=0.76`, `23.6x5x5 a=0.78`).
4. *Exact regenerated values, read from the outputs at full precision:* primary family-weighted mean −3.4941546891181936 °C and
   SD 11.433714718421587 °C (7 families, 5 studies); all-STRICT family-weighted mean −10.804718715572376 °C and SD
   21.08698664047987 °C (10 families, 5 studies). These are the values D-083 hands to WP6; the rounded −3.5 / 11.4 and
   −10.8 / 21.1 used in prose are those numbers to one decimal.
5. *No number moved.* SHA-256 was taken over all 206 tracked files in `data/`, `outputs/`, `src/` and `run_all.sh` before the
   approval edits and again afterwards: **0 differ**. The only files this session changed are `DECISIONS.md`, `PROGRESS.md` and
   `README.md`.
6. *Checks rerun:* `src/wp5_tests.py`, 9 of 9 pass (pairing audit, leakage, sign convention, full-size side untouched, round
   trip, raw-data immutability, evidence thresholds, primary-set membership). The 12 normalization self-checks are unchanged and
   run inside `src/wp5_size_effect.py`.
7. *Raw data and cohorts:* raw-file SHA-256 verified (7 of 7); the 14 CP2 cohort fingerprints recomputed and matching
   (primary 170 curves / 2,588 records); WP3 outcome counts 0 / 0 / 18 / 35 / 13 / 104.
8. *AGENTS.md* was not modified, not deleted, not committed and not added to `.gitignore`; it remains the only untracked file.

**Nothing in the approvals required an executable change.** Had one been needed, the session was to stop and say why before
merging (author's CP4 verification instruction 8); it was not.

## D-089 — The normalization-method bias sensitivity is a WP6 planning decision, not a CP4 one
**Status:** RESOLVED IN WP6 PLANNING by D-100 (approved by the author in WP6 Plan Mode, 2026-09-18, before any WP6 result):
each published normalization is a complete scenario with its own bias and residual SD, nothing is added in quadrature,
and which method is "true" is never randomly sampled. Earlier: OPEN — deliberately not resolved at CP4; carried into WP6
planning (author, 2026-09-17)

**Finding to preserve** (D-087, `normalization_sensitivity_comparison.csv`). Across the pre-declared normalization methods the
**residual spread is relatively stable** — family-weighted SD 11.1 to 11.9 °C for every volume-type energy convention paired
with any of the four published temperature corrections — while the **central bias moves materially**: family-weighted mean
−3.5 °C (primary, Sokolov Eq. 22), −4.5 °C (Corwin (B b)^{3/2} energy), −6.6 °C (Lucon shift), −18.0 °C (Wallin shift),
−23.2 °C (Towers shift). Pure fracture-area energy scaling is far worse on both counts (mean +42.9 °C, SD 42.1 °C) and is not a
candidate for a central scenario.

**What this means.** The choice of which published correlation to cite is itself a source of uncertainty in the *location* of
the size correction, largely separate from the scatter of the residual about it.

**What WP6 must do, and what it must not do.** WP6 planning must consider how to represent this bias sensitivity across the
pre-declared methods **without double-counting the residual SD** — the SD already describes scatter about a chosen bias, so
adding a bias spread drawn from the same comparisons on top of it would count the same disagreement twice. **This modelling
choice is not made here.** No combination rule, no widened distribution and no bias prior is approved at CP4. It is a WP6
planning decision, to be taken in WP6 Plan Mode with the alternatives visible.

---

# WP6 — Monte Carlo test-matrix study

All numbers regenerate with `src/wp6_validation.py` (simulator validation) and `src/wp6_experiment.py` (the frozen
experiment), with `src/wp6_tests.py` as the independent check module, into `outputs/wp6/`. The simulator calls the
**unchanged approved** `src/wp3_fitter.py` and `src/wp5_normalization.py`; WP6 changes no WP0–WP5 source file, output,
cohort or decision.

**WP6 contains only SYNTHETIC data.** Every WP6 table and figure carries
`data_type = "SYNTHETIC (Monte Carlo test-matrix study; not published measurements)"`. No simulated measurement is ever
mixed with a published measurement. The only published quantities that enter are *calibrated parameters* — WP3 curve
parameters, the WP4 residual-scatter profile, and the WP5 correction bias, SD and family-level residuals — each read from
its regenerated file at full precision at run time, never typed from prose.

**Status legend for this section:** `PRE-REGISTERED (WP6)` = written and committed before any headline WP6 cell was run
(the commit is named in D-112). `APPROVED (WP6 plan)` = approved by the author in WP6 Plan Mode, before any WP6 result
existed, over three review rounds (2026-09-17/18); every entry below was approved before implementation began.
`FINAL APPROVED (CP5)` = approved by the author at the official checkpoint CP5 (2026-09-19) after reviewing the completed
WP6 results; the earlier statuses follow it as history and no pre-registered text is rewritten.

**WP6 plan-approval record (author, 2026-09-18).** The author reviewed a written WP6 implementation plan in three rounds
and approved it. Round 1 produced the plan; round 2 issued 14 amendments; round 3 issued a temperature-frame correction
and three implementation clarifications; a final round corrected one remaining coordinate-frame ambiguity. Each amendment
is recorded in the entry it changed and in the chronology D-112. **Nothing in this section was decided after seeing a WP6
simulation result**; the only WP6 numbers that existed at approval were planning-stage calibration diagnostics and
feasibility checks, all listed in D-112.

**CP5 approval record (author, 2026-09-19).** The author reviewed the completed WP6 state and **approved WP6**;
`wp6` is merged into `main` with an explicit merge commit once these decisions are recorded and verified. **These
approvals are documentation and status only: no code, estimator, grid cell, scatter model, correction value, seed,
threshold, number, generated table or generated figure changed, and no WP6 computation was rerun** (author's CP5
instruction 7). Each item is recorded in full in the entry named.

1. **Adaptive step pattern (D-101, D-112 step 10): KEEP the pre-registered EXTENDING interpretation as implemented.**
   The wrapping interpretation is **not** added as a WP6 sensitivity. Reasons, as the author gave them: the extending
   implementation was frozen before headline results existed; the ambiguity was found afterwards and is transparently
   recorded; no full-size result depends on the ambiguous portion; the measured effect on miniature T1 RMSE is small;
   and tier T7 already provides a genuinely different adaptive/staircase sensitivity, so the project already
   demonstrates that adaptive-design conclusions can depend on the algorithm. **The wording ambiguity is preserved as
   an explicit limitation, and the original wording is not rewritten to look unambiguous.**
2. **Coldest test temperature (D-101, D-112 step 5c): CONFIRMED at −195 °C.** The approved simulation requires both a
   raw specimen temperature of at least −196 °C and a temperature on the 5 °C grid; −196 °C is not on that grid, so
   −195 °C is the coldest point satisfying both. The consequence is kept: **22 rather than 21** of the 104 usable
   full-size truths are unreachable for the `20x1.5x1.5` geometry. Recorded as an **implementation clarification, not a
   post-result tuning decision**.
3. **D-090 to D-112 FINAL APPROVED** as the final WP6 record, **including the whole D-112 chronology**. Nothing is
   deleted or sanitised: the implementation defects found after the first run and the fact that they were corrected TO
   the pre-registered plan; the determinism test that originally passed without genuinely testing worker-count
   independence; the reporting fixes; the adaptive wording ambiguity; the ~21 h cold reproducibility run stretched by
   the machine sleeping on battery; and the two awake cold-run runtimes of about 381–390 min. **The transparent
   chronology is part of the project's reproducibility evidence.**
4. **The WP6 headline is approved in CONDITIONAL form.** The final report **must not** claim that full-size specimens
   are universally better than miniature specimens. The approved statement is: under the CENTRAL scenario the WP5
   programme-level size-correction bias is about −3.49 °C with a residual SD of about 11.43 °C, which produces an
   approximately **12 °C full-size-equivalent RMSE floor for miniature programmes that does not average away as the
   specimen count rises**; and under the idealized finished-specimen material-volume accounting, at k = 4 miniature
   wins for uniform, anchored and model-based adaptive placement while clustered placement gives it no general win;
   around k = 6 the answer is placement-dependent and often tied; from k = 8 miniature wins no CENTRAL T1 comparison;
   and from k = 18 full-size wins every CENTRAL T1 comparison. **The generated tables remain authoritative over prose.**
   Also preserved: that **correction uncertainty, not the WP4 scatter model, is the dominant assumption**; that the
   correction SD would have to be roughly 5.3–9.7 °C at k = 8 for the median archetype (1.3–12.3 °C over all three
   archetypes) to reach the full-size RMSE, against the measured central 11.43 °C; that the conservative / all-STRICT
   and several published-normalization sensitivities favour full-size more strongly; that **no individual miniature
   geometry had a DIRECTLY SUPPORTED WP5 correction distribution** and the central correction is pooled and **WEAKLY
   SUPPORTED**; that the material-volume comparison is **idealized finished-specimen accounting, not a
   surveillance-capsule machining-yield model**; that the smaller specimens studied are **miniature/MCVN-type, not
   conventional ASTM E23 sub-size evidence**; and that **irradiation × geometry interaction remains unresolved**.
5. **The T6 interval finding is approved, with its interpretation preserved prominently** (D-109): a WP4-style
   bootstrap on a miniature-derived programme can cover that programme's **own corrected estimand** well while severely
   under-covering the **true full-size T41J**, because the programme-level size-correction error lies outside an
   ordinary specimen-resampling bootstrap. **This is not described as a failure of the WP4 bootstrap**; it is a
   mismatch between sampling/fitting uncertainty and full-size-equivalent uncertainty after an uncertain specimen-size
   correction. The generated coverage results for N = 126 / 252 / 504 stand exactly as produced.
6. **Physical reachability is approved as a first-class WP6 result** (D-092, D-093): the raw floor of −195 °C on the
   declared grid; the geometry-dependent full-size-equivalent floor of −195 + M; that some cold transitions therefore
   cannot be adequately sampled by particular miniature geometries; that V16 at T41J = −150 °C makes **every** tested
   miniature comparison ineligible; and that the 104-real-curve breadth check shows cold-transition cases becoming
   unreliable **before** the hard mathematical reachability boundary. **Feasibility failures are not collapsed into
   ordinary RMSE comparisons.**
7. **No further expensive WP6 runs.** The project has already completed two full cold WP6 runs on an awake machine, a
   corrected rerun after the implementation deviations were fixed, the final full `./run_all.sh` from raw data with the
   WP6 cache moved aside, raw checksum verification, upstream WP0–WP5 regeneration, 19 simulator tests (20 validation
   rows), 11 independent checks and byte-identical regenerated outputs. This session therefore made documentation and
   status changes only. Had any executable WP6 source file required modification, the session was to stop and explain
   before merging; none did.
8. **Status and merge.** WP0–WP6 are complete and approved (CP1, CP1, CP2, CP3, internal review, CP4, CP5); **WP7 is
   the next permitted work package and has NOT started.** `wp6` is merged into `main` with an explicit merge commit,
   the branch is kept, nothing is pushed to any remote, and `AGENTS.md` stays untouched and untracked.

**Generated text keeps its generated wording** (the D-067 step 9c and D-088 precedent): `method_configuration.md` still
says the −195 °C clarification is recorded "for the author to confirm or reverse", and `wp6_summary.md` still lists the
adaptive delta reading as open for the author. Changing that text would require editing executable code and rerunning the
analysis, which this approval session did not do. **This file and `PROGRESS.md` are the authoritative record of the CP5
decisions.**

Not authorized by this approval: WP7 work of any kind, report drafting, any change to WP0–WP6 code, data, cohorts or
generated outputs, and any new simulation.

**Sources cited in WP6** (all previously read and cited in WP3–WP5; no new source is introduced)
- [Marini2020], [Switzner2023], [NIST-TN2158], [EfronTibshirani1986] — listed under WP3/WP4.
- [NUREG/CR-6379], [LuconNIST], [ML2026], [E2248-18], [descriptor] — listed under WP5.
- [10CFR50] §50.61(c)(2)(i)(C) and [E185-82] §6.3 — listed under WP2/WP3.
No number in WP6 comes from a source that this repository has not already read and recorded.

## D-090 — What WP6 simulates, and what it must never do
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** WP6 answers PROJECT_BRIEF.md §2 by Monte Carlo simulation of complete test programmes against a **known**
true full-size transition curve. One replicate = one simulated test programme: choose a true curve, a specimen geometry and
a material budget; derive the specimen count; place test temperatures by a declared strategy using only declared prior
information; generate specimen energies from a declared scatter model; for a smaller geometry apply the approved WP5
classical correction back into the full-size domain; fit with the approved WP3 method; take T41J by the approved rule; and
record `error = T41J_hat − T41J_true`.

**Never.** WP6 does not fit, tune or calibrate anything on published measurements beyond reading the already-approved WP3,
WP4 and WP5 parameters; does not mix simulated and published measurements in any table; does not train a model to predict
full-size properties (brief §2.1 and §8); does not alter any WP0–WP5 output; and does not change a scientific decision
after seeing a WP6 result. Every WP6 file states that it is synthetic.

**Alternatives.** An analytic error-propagation study (no simulation). **Why not.** It cannot represent the estimator's
refusals (the tested-range rule), the failure modes, the adaptive designs, or the interaction between a mis-centred design
and the size correction — all of which are the substance of the question. **If chosen.** A smooth but unfaithful answer.

## D-091 — The fixed-material-volume accounting
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 2); PRE-REGISTERED (WP6)

**Decision.** The material budget is spent in **gross rectangular finished-specimen volume** L × W × B. The number of
specimens is `N = floor(V_budget / V_specimen)`: **integer floor, unused remainder discarded**, no partial specimens, no
reconstitution and no material recovered from broken halves. The notch-removed volume is **not** recovered (it is about
20 mm³ of a 5,500 mm³ full-size specimen, 0.36 %). Budgets are exact multiples of one full-size specimen,
k ∈ {4, 6, 8, 12, 18, 24}, so N_full = k and V = 22,000 / 33,000 / 44,000 / 66,000 / 99,000 / 132,000 mm³. k = 12 is close
to the [E185-82] §6.3 surveillance specimen counts already adopted as this project's stricter cohort (D-038).

**This is an idealized finished-specimen material-only accounting** (author's amendment, review round 2). It is **not** a
prediction of how many specimens physically fit in, or can be machined from, a real surveillance capsule. Capsule layout,
holder geometry, orientation constraints, archive requirements, broken-half reconstitution and machining yield are **not**
modelled. That sentence appears on every generated table and figure that carries a specimen count.

**No fabrication-yield model is invented and no specimen-count cap is imposed.** Instead, a declared **material-utilization
sensitivity** applies a uniform linear allowance c per face, V = (L+2c)(W+2c)(B+2c), c ∈ {0.5, 1.0} mm, to **every**
geometry including full-size (T4 variants V18, V19). It is an illustration of direction and magnitude, not a fabrication
model, and it is labelled as such. It matters: specimens per full-size equivalent fall from 122.2 to 51.6 to 30.5 for
20×1.5×1.5, from 44.0 to 26.3 to 18.4 for 20×2.5×2.5 and from 17.0 to 12.1 to 9.4 for the KLST geometry at
c = 0 / 0.5 / 1.0 mm.

**Alternatives.** (1) Subtract the notch volume. (2) Model a machining yield. (3) Cap the specimen count at a practical
number. **Why not.** (1) would understate consumption, because the specimen is machined from a prism at least as large;
(2) has no defensible basis in this repository or in the sources read, and inventing fabrication losses is forbidden
(brief §7); (3) would silently bias the comparison against the geometry that fits most specimens. **If chosen.** (3) in
particular would decide the headline by assumption rather than by evidence.

## D-092 — Which specimen geometries WP6 simulates, and how geometry enters
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2 and 3); PRE-REGISTERED (WP6)

**Decision.** WP6 simulates the full-size geometry G0 (55 × 10 × 10 mm, a = 2 mm, B b² = 640 mm³, NF_E = 1, M = 0) and
**all seven miniature geometry classes that D-083 hands over as WEAKLY SUPPORTED**:

| code | WP5 geometry id | B b² (mm³) | NF_E | M (°C) | gross V (mm³) | families / studies |
|---|---|---|---|---|---|---|
| G1 | `20x1.5x1.5 a=0.33` | 2.0533 | 311.686 | 87.136 | 45.000 | 1 / 1 |
| G2 | `20x2.5x2.5 a=0.38` | 11.2360 | 56.960 | 61.471 | 125.000 | 3 / 1 |
| G3 | `20x3.33x3.33 a=0.51` | 26.4815 | 24.168 | 48.526 | 221.778 | 1 / 1 |
| G5 | `23.6x3.33x3.33 a=0.51` | 26.4815 | 24.168 | 48.526 | 261.698 | 2 / 2 |
| G4 | `27.5x3.33x3.33 a=0.6` | 24.8182 | 25.788 | 49.505 | 304.945 | 1 / 1 |
| G6 | `27x3x4 a=1` (KLST) | 27.0000 | 23.704 | 48.233 | 324.000 | 1 / 1 |
| G7 | `23.6x5x5 a=0.76` | 89.8880 | 7.120 | 30.072 | 590.000 | 1 / 1 |

Every NF_E and M is recomputed at run time by the unchanged `src/wp5_normalization.py` from the geometry alone.
**No geometry is collapsed with another.** G3 and G5 share a ligament volume but differ in length, hence in gross volume
and specimen count, and are simulated separately.

**The two geometries D-083 marks UNSUPPORTED BY THIS DATASET — `20x5x5 a=0.76` and `23.6x5x5 a=0.78` — are omitted,
because the dataset does not support a correction for them.** They are **not** claimed to be physically redundant with any
simulated geometry: similar gross or ligament volume does not demonstrate equivalent notch, constraint or size-correction
behaviour. No external correction number is adopted and no external-literature scenario is built (CP4 item 12). A required
output `wp5_geometry_reconciliation.csv` accounts for all nine handoff rows: 7 simulated, 2 omitted, 0 collapsed.

**No geometry-specific performance claim is made.** D-083 forbids a geometry-specific correction and 0 of 9 geometries is
DIRECTLY SUPPORTED, so every geometry result is described as *a conditional fixed-volume scenario using the pooled,
WEAKLY SUPPORTED correction distribution*. That wording is enforced in every generated table, figure caption and summary
sentence.

**How geometry enters (restricted claim; author's amendment, review round 3).** The earlier planning statement that
"geometry enters only through specimen count" is **withdrawn**. The approved statement is: *away from physical
temperature-envelope clipping, geometry enters primarily through specimen count, because NF_E cancels in relative-scatter
terms and M displaces truth and design identically; near the raw physical temperature bounds, M also matters through
geometry-dependent temperature clipping* (D-101). The coldest full-size-equivalent temperature a geometry can physically
reach is `−196 + M`: −108.9 °C (G1), −134.5 (G2), −147.5 (G3, G5), −146.5 (G4), −147.8 (G6), −165.9 (G7), −196.0 (G0).
Equivalence is therefore **tested, not assumed** (validation test 12A interior, 12B boundary), and a deterministic output
`geometry_reachability.csv` reports reachability for every geometry against every archetype and all 104 real fitted curves.

**Alternatives.** Simulate only the best-supported geometries; collapse geometries with equal B b². **Why not.** The first
would leave the handoff unreconciled; the second would assume an equivalence the physical envelope breaks.

## D-093 — The true transition curves
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 3); PRE-REGISTERED (WP6)

**Decision.** Central: a 3 × 3 factorial of the marginal quantiles of the **104 usable full-size WP3 fits with a calculated
T41J** — USE ∈ {100, 200, 270} J (p10, median, p90) × C ∈ {28, 46, 60} °C (p10, median, p90), with LSE = 2.7 J (the
approved full-size convention, D-042) and T0 set so that T41J = −53 °C (the cohort median) in every archetype. Archetypes
are labelled A1…A9; the **declared reduced set used by every reduced tier is {A1, A5, A9}** — the median plus the two
corners that bracket both where 41 J sits on the fitted rise (0.394 at USE 100 against 0.143 at USE 270) and the transition
width (28 against 60 °C).

**Occupancy is reported, not assumed.** The number of the 104 real fits within ±25 % of both USE and C is printed for every
archetype (1, 5, 10 / 9, 44, 28 / 11, 31, 23). Every cell is occupied; the sparsest (A1) is reported as such. USE and C are
correlated in the cohort (Pearson −0.41), so the corners are deliberately stressed.

**Temperature-location invariance is conditional, not global** (author's amendment, review round 3). The problem is
translation-invariant in temperature **only when (i) no raw specimen temperature reaches the physical envelope and (ii) the
5 °C raw grid does not produce a materially different snapping pattern**. Because M changes a miniature geometry's
proximity to the raw bounds, **absolute location is not globally irrelevant** and is never described as such. The
invariance justifies one central archetype location and nothing more; validation test 10 checks it only in a declared
clip-free, snap-matched configuration and **records** where it breaks.

**Required envelope sensitivity, evaluated geometry-specifically:** T41J_true ∈ {−150, +100} °C on G0, G1, G5 and G7
(T4 variants V16, V17), chosen so that the largest M, an intermediate M, the smallest M and full-size are all covered.

**Required breadth check:** each of the 104 usable full-size fits is used in turn as a synthetic truth (tier T5), and the
distribution of the per-curve winner is reported in the summary, not in an appendix. This is what stops a few archetypes
carrying the headline.

**Declared model sensitivity on the lower shelf:** true LSE = 6 J analysed with the fixed 2.7 J convention (T4 variant
V15). Legitimate because WP4 measured an empirical lower-shelf mean residual of +0.0149 × USE (+3.0 J at USE = 200), i.e.
measured lower shelves commonly sit above the convention (D-066).

**Alternatives.** One convenient tanh curve; only real fitted curves as truths. **Why not.** The first would let a single
shape carry the headline; the second alone gives no factorial attribution to USE or C — so both are used, the factorial
centrally and the real curves as the breadth check.

## D-094 — The three scatter-model candidates and how each is calibrated
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2 and 3); PRE-REGISTERED (WP6)

**Decision.** The five regions are WP4's (D-061), evaluated on the **true** curve: lower shelf x ≤ −1.5; lower transition
−1.5 < x ≤ −0.5; central −0.5 < x < 0.5; upper transition 0.5 ≤ x < 1.5; upper shelf x ≥ 1.5, with x = (T − T0_true)/C_true.

- **C1 — region-wise normal scatter scaled by USE.** `sd = USE_true × s(region)`, zero mean, s read at full precision from
  `outputs/wp4/published_residual_scatter_summary.csv` (full-size, usable WP3 fits, leverage-adjusted residual / fitted
  USE, SD column): 0.036079, 0.072945, 0.105201, 0.099833, 0.061581. **Calibration = reading the table; nothing is fitted.**
  **C1-robust** uses the `mad_scaled` column (0.0225, 0.0543, 0.0986, 0.0852, 0.0513) as the low-scatter sensitivity.
- **C2 — the smooth WP3 generator form** `sd(T) = σ_T·|dE/dT| + cv·E(T) + 3·cv·LSE` (D-048). Calibration, declared before
  it was run: (σ_T, cv) by bounded least squares minimising Σ_r w_r·(profile_C2(r) − s_empirical(r))², where profile_C2(r)
  is the mean of sd(T)/USE over a 201-point uniform x-grid inside region r (shelf regions truncated at |x| = 3), averaged
  with equal weight over the nine archetypes, and w_r = √(n_r/Σn) with the WP4 residual counts n = (154, 339, 511, 286, 395).
- **C3 — region-wise empirical resampling of the leverage-adjusted residual / USE observations, CENTRED** (author's
  amendment, review round 2). From `outputs/wp4/published_residual_scatter_dataset.csv` (full-size, usable WP3 fits), split
  by region, **subtract that region's empirical mean** (+0.014854, −0.004736, −0.000900, +0.008567, −0.003058) and resample
  the **centred** values with replacement within region, multiplied by USE_true. This makes C3 a zero-mean stochastic
  scatter model directly comparable with C1 and C2, while keeping the empirical skew, heavy tails and heterogeneity about
  the mean. **The lower-shelf +0.0149 × USE offset is a model-convention / model-shape bias and is never injected as if it
  were random specimen scatter.**
- **C3-uncentered** is retained as a separate, clearly labelled case — *"empirical residual + model-shape /
  systematic-region-bias sensitivity"* — and is **not** the main C3 scatter sensitivity.

**Pre-declared selection criterion** (fixed before any headline cell, evaluated on calibration diagnostics only): the
central model must lie within ±25 % of the WP4 empirical SD/USE in **all five** regions and within ±15 % at the 41 J
crossing of the median archetype; ties are broken toward the candidate needing no fitted parameter; if none qualifies, C1
is central by default.

**Alternatives.** Fit a new scatter form to the residuals; stratify by product form or irradiation. **Why not.** A new form
would be a model invented after the WP4 results; D-066 found no product-form stratification supported (fewer than 10 curves
in most strata). **If chosen.** An unfalsifiable scatter model, or strata too thin to interpret.

## D-095 — The CENTRAL scatter model is C1, changing the D-066 planning preference
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6). **This supersedes the planning preference
recorded in D-066** (C2 central), and the change was made **before any headline WP6 result existed**.

**Decision.** The **CENTRAL** WP6 scatter model is **C1 with the ordinary SD scale**. C2 and C3-centred are **mandatory**
sensitivities; C1-robust is the low-scatter sensitivity; C3-uncentered is the labelled model-shape case; the
miniature-inflated profile is a required sensitivity (D-096). All are run on the frozen T4 grid and the headline is
reported under each, with an explicit statement of whether the full-size-versus-miniature conclusion changes across them
(required by D-066).

**Why C1 and not C2** (calibration evidence, produced during planning and regenerated by `src/wp6_scatter.py`). Calibrating
C2 by the D-094 procedure gives σ_T ≈ 7.38 °C and cv ≈ 0.057, and the resulting region profile is
0.0101 / 0.0510 / 0.1146 / 0.0921 / 0.0643 against the empirical 0.0361 / 0.0729 / 0.1052 / 0.0998 / 0.0616 — ratios
0.28 / 0.70 / 1.09 / 0.92 / 1.04. **C2 under-represents the lower shelf by a factor of about 3.6 and the lower transition
by about 30 %**, and it fails the D-094 criterion in two regions. For a 200 J RPV curve 41 J sits at x ≈ −0.71, i.e.
**inside the lower-transition region that C2 under-represents**, which is the single most important place on the curve for
the T41J estimand. C1 reproduces every region of the measured profile by construction and needs no fitted parameter; its
only defect, a step in sd at a region edge, does not bias T41J.

**Directional asymmetry, recorded so that the choice cannot later be mistaken for tuning.** Because
RMSE_mini ≈ √(V_sampling(N_mini) + bias² + SD_correction²) has a floor that the full-size sampling variance does not,
**understating the scatter favours full-size and overstating it favours miniature**. The choice was made on a calibration
diagnostic, before any headline simulation result existed, and all three candidates are run regardless.

**Alternatives.** Keep C2 central as D-066 preferred, reporting its lower-region deficit as a caveat. **Why not.** It would
build a known ≈ 30 % understatement into the headline, in the direction that favours full-size, at exactly the place on the
curve the estimand depends on. **If chosen.** A smoother scatter model, a lower full-size sampling error, and a headline
biased toward full-size by an amount the sensitivity analysis would then have to undo.

## D-096 — Miniature scatter: magnitude, coordinate and the un-modelled resolution floor
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 3); PRE-REGISTERED (WP6)

**Decision — magnitude.** Centrally, the **same relative scatter profile applies at both specimen sizes**, so that the
energy normalization is exactly variance-preserving in relative terms and the comparison isolates the test-programme design
question. A **required sensitivity** uses the WP4 **miniature** profile instead (central transition 0.1670 against
0.105201, a factor 1.59), from 13 curves and 6 references, and is stated to be weakly supported wherever it appears.

**Decision — coordinate (author's amendment, review round 3).** For a miniature programme with programme-level discrepancy
Δ, a specimen tested at raw temperature `T_raw` truly sits at
`T_equiv_true = T_raw + M − Δ`, `x_true = (T_equiv_true − T0_true)/C_true`.
**Region selection for C1 and C3, and evaluation of the C2 function, use `x_true`** — never the raw temperature alone, and
never the nominal position `T_raw + M`, which is where the analyst *thinks* the specimen sits. The magnitude is computed in
the full-size-equivalent frame and converted to raw energy units by dividing by NF_E before being added to the raw
specimen energy:
`sd_raw = sd_fse / NF_E`, with sd_fse from C1, C1-robust, C2, C3-centred, C3-uncentered or the miniature-inflated profile.
C2 is exactly scale-covariant in energy, so dividing by NF_E is identical to evaluating C2 in raw units with
USE_raw = USE/NF_E and LSE_raw = 2.7/NF_E at the same σ_T and cv. Energies drawn below 0 J are set to 0 J **in raw units**
and counted, as in D-048 and D-053. Multiplying by NF_E during normalization must therefore recover the intended
full-size-equivalent scatter distribution; validation test 17 proves it.

**Independence caveat, carried into every report of a large-N miniature gain.** All C1/C2/C3 specimen draws are
**independent conditional on the programme-level Δ**. WP6 does **not** model a within-programme correlated laboratory or
instrument systematic error — one machine, one operator, one calibration applied to every specimen of one programme. The
WP4 pool itself contains between-laboratory and model-shape heterogeneity (D-061), part of which would in reality act as a
*shared* within-programme offset. An independent error averages away as 1/√N; a correlated one does not. **Every
very-large-N miniature gain is therefore reported as conditional on this independence assumption and as potentially
optimistic.** No extra variance component is invented to cover it.

**Named, quantified, and deliberately not modelled: the absolute energy-resolution floor.** It is not scale-invariant and
would count against miniature specimens. Mapping a 200 J full-size material back through NF_E gives raw miniature curves
spanning 0.642 J (G1), 3.511 (G2), 8.275 (G5), 8.438 (G6) and 28.090 J (G7), with the 41 J criterion at 0.132 J raw for G1.
The 13 usable miniature WP3 fits have fitted USE between 3.32 and 29.08 J, so **G1's implied raw curve is smaller than
anything in the dataset's own miniature fits**. No citable resolution value was found in the sources read, so the effect is
named with its direction and magnitude rather than invented, and the G1 results carry that caveat.

**Alternatives.** Invent a resolution floor; assume miniature scatter equals the WP4 miniature profile centrally. **Why
not.** The first fabricates a number; the second would make a 13-curve, 6-reference estimate the central assumption.

## D-097 — How the size correction is injected into the simulated truth
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** The size-correction discrepancy enters as a **temperature-domain displacement of the simulated truth**. With
Δ the programme's discrepancy, the true miniature response is
`E_mini_true(T_raw) = E_full_true(T_raw + M − Δ) / NF_E`.
Applying the approved forward normalization (T + M, E × NF_E) then returns an estimate whose 41 J crossing lies at
`T41J_true + Δ`, which **reproduces D-078's definition and sign exactly**: ΔT_size = T41J(normalized smaller-specimen
estimate) − T41J(matched full-size curve), positive meaning the correction places the transition warmer. Verified end to
end during planning: injecting −25 / −3.5 / 0 / +15 °C returned mean recovered errors of −25.32 / −3.82 / +0.22 / +14.97 °C.
The sign convention is never silently reversed (CP4 item 7).

**A consequence that is kept, not removed:** the displacement also **mis-centres the miniature test temperatures**, because
the designer places specimens where the *published* correction says the transition is. That is physically real and is the
mechanism by which an adaptive design can partly rescue a badly corrected miniature programme; a post-hoc additive shift
applied to the recovered T41J would miss it.

**Alternatives.** (1) Add Δ to the recovered T41J after the fit. (2) Inject the discrepancy as an energy-scale error
(WP5 found normalized USE over-predicts by a median factor 1.19), at the same calibrated magnitude — retained as an
optional labelled sensitivity (T4 variant V20), not as the central form. **Why not (1).** It would remove the design
mis-centring and make the correction error purely additive, which is not what a wrong correlation does to a test programme.

## D-098 — The correction residual is ONE programme-level draw
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** Δ is drawn **once per simulated test programme** and shared by every specimen in that programme. It is **not**
redrawn per specimen in any central or headline analysis.

**Why.** (i) WP5's estimand is defined per matched geometry comparison — one whole smaller-specimen curve against one whole
full-size curve (D-078) — and D-082 describes it as "the spread of ΔT_size across matched comparisons". (ii) D-070 makes
the material-condition family the unit of independence, which is a programme-level unit, not a specimen. (iii) Decisive:
specimen-level noise would average away as 1/√N, so a programme with 500 miniature specimens would recover an *exact*
correction — the physically absurd conclusion that testing enough small specimens removes a systematic correlation error.
(iv) The observed structure supports it: ΔT_size varies between *geometries within one material* by tens of degrees
(R59-266: −33.8 and +11.5 °C), i.e. at the curve-mapping level.

**Kept as an explicitly labelled illustrative sensitivity only:** specimen-level redrawing (T4 variant V14). It makes the
correction penalty vanish at large N, and showing that is the point — it demonstrates how much the answer depends on this
one modelling choice. It is never the headline and never presented as an alternative central case.

**Alternatives.** Specimen-level draws as central; a hierarchical split of the residual into programme and specimen parts.
**Why not.** The first is refuted above; the second would need a variance decomposition that D-082 explicitly forbids
attempting from these data.

## D-099 — The distribution of the correction residual, and the two approved WP5 scenarios
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2 and 3); PRE-REGISTERED (WP6)

**Decision — scenarios and their exact values,** read at run time from the regenerated WP5 outputs at full precision,
never typed from prose (D-083):

| scenario | bias (°C) | SD (°C) | source file and row |
|---|---|---|---|
| **CENTRAL** (primary pooled, WEAKLY SUPPORTED) | −3.4941546891181936 | 11.433714718421587 | `wp6_size_correction_handoff.csv`, POOLED row |
| **CONSERVATIVE** (required, D-083) | −10.804718715572376 | 21.08698664047987 | `size_correction_summary_overall.csv`, all-STRICT family-weighted |
| robust-scale brackets | as above | 11.337678974122086 / 19.903817963325263 | same files |
| ZERO-PENALTY | 0 | 0 | validation only |

WP6 **must** report whether the headline conclusion changes when CENTRAL is replaced by CONSERVATIVE. Neither is chosen
because it gives a preferred answer.

**Decision — parametric form.** Centrally `Δ ~ Normal(bias, SD)`. **There is no truncation.** A ±4 SD numerical guard was
proposed during planning and **removed by the author**: it has no physical basis, and it is unnecessary, because the draw
displaces the *truth* relative to the design and can never generate an out-of-envelope test temperature. The only
consequence of an extreme draw is a programme that misses the transition, which is counted honestly as
estimator-unavailable and enters the availability gate and the failure accounting like any other refusal. **If some
numerical bound ever turns out to be genuinely necessary, the run stops and the author is asked before one is introduced.**

**Decision — required nonparametric sensitivity.** Δ is resampled with replacement directly from the **family-level**
ΔT_size values behind the approved summaries, reconstructed inside the pipeline from
`outputs/wp5/size_correction_residuals.csv` and checked against the approved mean and SD to 1e-9 before use (the run stops
on any mismatch):
- PRIMARY pool, 7 families: −13.3260, +2.6865, −2.0097, −11.1610, −14.0078, −4.9607, +18.3196 °C
  (reproducing −3.4941546891182 / 11.4337147184216).
- ALL-STRICT pool, 10 families: −13.3260, +7.1936, +9.8117, −2.0097, −11.1610, −48.9415, −38.8450, −9.4327, −19.6563,
  +18.3196 °C (reproducing −10.8047187155724 / 21.0869866404799).

**No bias is ever added to an empirical draw** (author's amendment, review round 3). The two forms are exactly
`Δ = bias + SD·z` (parametric) and `Δ = sample_with_replacement(family values)` (empirical, **directly**). The family
values already contain their own empirical mean, so `bias + sampled_value` would count the bias twice. This is enforced
structurally: an empirical scenario carries `bias_already_included = True` and the sampler refuses a separate bias
argument; validation test 18 checks it numerically on 10⁷ draws.

**Seven observations are not evidence that the residual is normal.** The normal model stays central only because it
supplies a smooth SD axis for the correction-threshold experiment (D-106); the empirical-family resampling is what tests
whether the parametric assumption changes the conclusion.

**Caveat carried wherever the SD appears.** The pooled SD is a family-weighted **between-material** spread that still
contains WP4 fit noise and between-study variation; no deconvolution is attempted (D-082), so it is if anything
conservative. It is not a geometry-specific law, not pure material scatter and not an ASTM uncertainty (CP4 item 7).

## D-100 — The normalization-method bias sensitivity (resolves the open D-089)
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6). **This resolves D-089**, which CP4 deliberately
left open as a WP6 planning decision.

**Decision.** Each pre-declared published normalization is treated as a **complete, self-consistent scenario carrying its
own (bias, SD) pair measured on the same matched comparisons**. Nothing is added in quadrature, no extra generic
"method-uncertainty SD" is introduced, and which literature method is "true" is **never** randomly sampled.

| scenario | family-weighted bias (°C) | family-weighted SD (°C) |
|---|---|---|
| **CENTRAL — Sokolov Eq. 22 with the B b² energy factor** | −3.494 | 11.434 |
| S1 Corwin (B b)^{3/2} energy | −4.485 | 11.887 |
| S3 Lucon shift | −6.614 | 11.499 |
| S6 KLST dataset-literal geometry | −3.975 | 11.975 |
| S5 Wallin shift | −18.010 | 11.056 |
| S4 Towers shift | −23.234 | 11.784 |

Values are read from `outputs/wp5/normalization_sensitivity_comparison.csv` at run time. S2 (pure fracture area,
+42.942 / 42.087) is **not** a scenario — D-089 rules it out as a central candidate — and is shown once as an illustration
of what an inappropriate convention costs.

**Why this does not double-count.** Each SD is the scatter of the residual **about that method's own bias**, measured on
that method's own residuals. The bias moves between rows; no SD is widened to cover the movement. This is exactly what
D-089 required: represent the bias sensitivity without double-counting the residual SD.

**Alternatives.** (1) Draw the bias from a distribution over the six methods and keep the pooled SD. (2) Add a fixed extra
method-uncertainty SD in quadrature. **Why not.** (1) adds a spread the same comparisons already generated and treats the
choice of which published paper to cite as a random variable with a frequency interpretation nobody can justify from four
published formulas; (2) is precisely what D-089 warns against. **What could be sensitive to it.** The miniature error floor
is √(3.494² + 11.434²) = 11.9 °C under Sokolov and √(23.234² + 11.784²) = 26.0 °C under Towers, so the choice of published
correlation may matter more than the scatter model. That is reported explicitly rather than assumed either way.

## D-101 — Test-temperature placement: the physical frame, the grid, and the five strategies
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2, 3 and 4); PRE-REGISTERED (WP6)

**Decision — the physical frame (author's amendment, review round 3).** The **−196 °C to +300 °C envelope is a physical
raw-specimen test-temperature envelope** (−196 °C is the liquid-nitrogen floor; the range also covers the −196…+300 °C span
of [Marini2020]'s RPV matrix and this cohort's own tested range), and the **5 °C grid is a physical raw test-temperature
grid**. Every placement therefore follows this order, without exception, for U, C, A, S, SS and **every adaptive update**:

1. the strategy proposes a desired **full-size-equivalent** temperature `T_fse_desired`;
2. convert to raw: `T_raw_desired = T_fse_desired − M` (M = 0 for full-size);
3. round the **raw** temperature to the 5 °C grid;
4. clip the **raw** temperature to [−196, +300] °C;
5. the specimen is tested at that snapped, clipped `T_raw_actual`;
6. for analysis the actual raw temperature is normalized back: `T_fse_actual = T_raw_actual + M`.

**Clipping and snapping never occur in full-size-equivalent space.** Clipping in the equivalent frame and then subtracting
M would request physically impossible raw temperatures — for G1 (M = 87.1 °C) a wide-span design would ask for specimens at
−265 °C.

**M is subtracted exactly once (author's amendment, review round 4).** The prior `T_assumed_fse = T41J_true + e_prior` and
every quantity a strategy reasons with are **full-size-equivalent, identically for full-size and miniature programmes**;
the one and only subtraction of M is step 2. No strategy is ever handed a pre-shifted prior, and this is enforced
structurally: the strategy functions take no geometry argument and only `place()` knows M. Validation test 19 proves the
single subtraction numerically. **SS is the one deliberate exception**: it operates directly in raw space, starting at
`T_raw_start = T_assumed_fse − M` (still a single subtraction) and stepping in raw temperature thereafter.

Specimens whose desired raw temperature is colder than −196 °C **pile up at −196 °C** — the engineer has run out of cooling.
This is the declared central behaviour; it is counted by the per-cell `temperature_clip_fraction` and
`n_distinct_raw_temperatures` and is never hidden. A "feasible-span" variant that re-spreads a design inside the reachable
raw window is a *different* design definition and is not substituted for any frozen arm.

**Decision — prior information available to every strategy.** `T_assumed_fse = T41J_true + e_prior` and a fixed declared
nominal width `C_assumed = 40 °C` (close to the cohort median 46 °C). **The true C is never visible to design code.**

**Decision — the strategies.** `place(·)` below means "apply steps 2–5".
- **U, UNIFORM / WIDE SPAN.** `T_i = place(T_assumed_fse + W_wide·(i/(N−1) − ½))`, i = 0…N−1, `W_wide = 250 °C`
  (the cohort median tested span is 268 °C; p10 175, p90 365). N = 1 places one specimen at the centre.
- **C, CLUSTERED.** The same rule with `W_clust = 3·C_assumed = 120 °C`.
- **A, CLUSTERED WITH SHELF ANCHORS.** `n_anchor = max(1, round(0.10·N))` specimens at
  `place(T_assumed_fse + 3·C_assumed)` and the same number at `place(T_assumed_fse − 3·C_assumed)`; the remaining
  N − 2·n_anchor by rule C. Modelled on [Marini2020]'s RCC-M matrix (15 tests from −60 to +20 °C plus 3 at +100 °C).
- **S, ADAPTIVE (model-based, batched).** Seed block `n0 = max(4, round(N/3))` placed by rule A from the prior alone; block
  size `k_blk = max(1, round(N/6))`; then repeat until N specimens are used: fit everything so far with the approved fitter
  in the full-size-equivalent frame using `T_fse_actual`; if the fit converged and 41 J lies strictly between the fitted
  shelves, place the next block at `place(T̂ + δ_j·Ĉ)` with δ cycling 0, −0.5, +0.5, −1.0, +1.0, −1.5, +1.5, …; otherwise,
  if every measured energy so far is ≥ 41 J place at `place(min(T_fse_actual) − 0.75·C_assumed)`, if every one is < 41 J at
  `place(max(T_fse_actual) + 0.75·C_assumed)`, and if the fit failed outright at `place(T_assumed_fse)`. **An out-of-range
  crossing may be used for design**: D-044's tested-range rule governs *reporting*, not the choice of the next test
  temperature. The budget fixes N exactly; there is no early stop and no extra specimen.
- **SS, SIMPLE UP/DOWN STAIRCASE** (required reduced-grid sensitivity, tier T7), frozen before any result and run entirely
  in raw space: start at `T_raw_start = T_assumed_fse − M` snapped and clipped; one specimen at a time; step
  `Δ_step = 0.5·C_assumed = 20 °C`; after each specimen, if **E_fse < 41 J** the next raw temperature is +Δ_step (warmer)
  and if **E_fse ≥ 41 J** (including exact equality, so the rule is total) it is −Δ_step (colder); each next raw
  temperature is snapped and clipped, repeats allowed and counted; no early stop, no re-centring, no fitting during design.

**Adaptation-update accounting (author's amendment, review round 2).** The number of genuine adaptation updates is reported
per arm in `adaptive_update_counts.csv`. It is **0 at N = 4**, 2 at N = 6 and 4 for N ≥ 8. **At the smallest full-size
budget (k = 4) the seed block consumes the whole programme and S is exactly strategy A**; every result, caption and
conclusion touching that cell says so, and no "adaptive" claim is made from a cell in which no adaptation occurred.

**No truth leakage is structurally possible.** `wp6_design.place_temperatures(strategy, t_assumed_fse, c_assumed, n,
history, ...)` has no truth parameter, and the simulator never passes one (validation test 7, structural and behavioural).

**Alternatives.** Place temperatures in the equivalent frame and clip there; let the adaptive rule see the true T0.
**Why not.** The first requests physically impossible tests; the second is information leakage and would invalidate the
whole comparison.

## D-102 — The prior-knowledge axis
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** `e_prior = T_assumed_fse − T41J_true`, symmetric and declared in advance, nine levels:
**{0, ±10, ±20, ±40, ±80} °C**. Basis: 80 °C is about 1.7 × the median fitted C (46 °C) and about twice a typical
irradiation shift; 10 °C is within the 9.4 °C base-metal scatter allowance of [10CFR50] §50.61(c)(2)(i)(C) already adopted
as this project's reference scale (D-048). A planning check confirmed the ladder brackets the collapse: a clustered design
at ±80 °C produced a reportable T41J in only 3–18 % of replicates, against ≥ 99 % at ±40 °C. **The levels were fixed before
any result and are not adjusted afterwards.**

**Why this axis matters.** PROJECT_BRIEF.md §5 expects the answer to depend on how well the transition is known before
testing, but says to determine rather than assume it. The sweep (tier T2) is what determines it.

## D-103 — The estimator is the approved WP3 and WP5 analysis, unchanged
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** Every simulated programme is analysed exactly as the corresponding real programme would be:
`wp3_fitter.fit_curve(t, e, lse_fixed=2.7)` (the approved full-size convention of D-042, which D-077 also approved for
normalized smaller-specimen points), then `index_temperature` with the tested-range rule applied to the **analysed**
temperatures, `index_fraction_of_rise`, `classify` and `criterion_bracketing` — the approved functions, imported unchanged
from `src/wp3_fitter.py`. For a miniature programme the transformation into the analysis frame is the approved
`wp5_normalization.normalize` (D-073, D-074) applied to the **actual raw** temperature and energy.

**The estimator's refusals are part of the estimator.** A replicate whose 41 J crossing lies outside its own tested range
has **no** T41J and is counted as unavailable (D-044); it is never replaced by an extrapolated value. Validation test 14
proves the WP6 analysis path reproduces `wp3_fitter` on stored published curves, so what is validated is what is applied
(the D-054 pattern).

**Alternatives.** A simplified or "simulation-friendly" fitter; allowing extrapolated crossings. **Why not.** Either would
measure a different estimator from the one this project reports.

## D-104 — The primary performance metric and the availability gate
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** The **primary metric is the RMSE of (T̂41J − T41J_true) in °C**, computed over the replicates in which the
approved estimator produced a value. The **eligibility gate is availability ≥ 95 % of the replicates requested** — the same
threshold and the same logic as the WP4 reporting rule D-057, reused rather than invented. Failed and unavailable
replicates always stay in the denominator. A cell below the gate is labelled **"estimator unavailable too often"** and can
never be declared a winner, however small its conditional RMSE.

**Also reported for every cell:** signed bias, SD, MAE, median |error|, P90 |error|, P95 |error|, availability fraction,
the WP3 outcome-category counts of the final fit, the index-unavailable reasons, `temperature_clip_fraction`,
`n_distinct_raw_temperatures`, and for strategy S the adaptation-update count.

**Why RMSE decides.** It combines the systematic correction penalty with the sampling variance in the units of the
regulatory index. SD alone would hide the correction bias; MAE would under-weight the tail that matters for a vessel
integrity argument. **Secondary decision metric: P90 |error|**, reported beside it, with any disagreement between the two
flagged explicitly rather than resolved silently.

**Why the gate is necessary.** A planning check found clustered designs at ±80 °C prior error available in only 3–18 % of
replicates with a conditional RMSE of 14–25 °C — which without the gate would look merely mediocre instead of unusable.

## D-105 — Win, practical tie, flip, and the label-threshold robustness matrix
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 2); PRE-REGISTERED (WP6)

**Decision.** With ΔRMSE = RMSE(full-size) − RMSE(miniature) for one budget, strategy, archetype and scenario:
- **τ = max(2.0 °C, 5 % of the smaller RMSE)**. Basis: 2 °C is this project's own distinct-test-temperature convention
  (D-037) — a difference below the resolution at which test temperatures are set and reported cannot drive a
  test-programme decision — and it is about 21 % of the 9.4 °C base-metal scatter allowance of [10CFR50]
  §50.61(c)(2)(i)(C) already adopted as a reference scale in D-048.
- **MINIATURE WINS** iff ΔRMSE > τ **and** ΔRMSE > 3·SE_paired(ΔRMSE) **and** both cells pass the D-104 gate.
- **FULL-SIZE WINS** iff −ΔRMSE > τ and −ΔRMSE > 3·SE_paired(ΔRMSE) and both cells pass the gate.
- **PRACTICALLY TIED** otherwise; **INELIGIBLE** if either cell fails the gate.
**No winner is ever declared from a fraction of a degree of Monte Carlo difference.**

**Flip point** = the value of a swept variable at which the declared winner changes, reported as a bracketing interval
between adjacent grid values and separating the **numerical crossing** (ΔRMSE changes sign; linear interpolation) from the
**practically meaningful crossing** (the whole tie band is crossed). Both are printed; the second is what conclusions quote.

**Label-threshold robustness matrix (author's amendment, review round 2), at zero additional simulation.** Recomputed post
hoc from the stored per-replicate errors and availability masks: availability gate ∈ {90 %, **95 % primary**, 99 %} ×
τ ∈ {0 °C, 2 °C fixed, 5 °C fixed, **max(2 °C, 5 %) primary**}, twelve label variants, written to
`label_threshold_robustness.csv` with an explicit statement of whether the headline winner and the flip depend materially
on these project-defined thresholds. **The threshold that gives a cleaner answer is never selected**; the primary rule is
fixed here and does not change.

**Alternatives.** A pure significance test with no practical tolerance; a fixed 5 °C tolerance. **Why not.** The first
would manufacture winners from Monte Carlo noise at large replicate counts; the second is one of the reported variants
rather than the rule, because it is not tied to any project convention.

## D-106 — The correction-uncertainty threshold SD*
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** The headline threshold quantity is **SD\*** = the correction residual SD at which
RMSE(miniature at N_mini) = RMSE(full-size at N_full), at the declared bias, for a given budget, strategy and archetype.
It is obtained two ways, both reported:
1. **Simulated (primary):** a declared sweep SD ∈ {0, 5, 10, 15, 20, 25, 30, 40} °C (tier T3), with SD\* by linear
   interpolation between the bracketing grid points and the tie band shown. The measured 11.4337 and 21.0870 °C are drawn
   as annotated verticals; their cells already exist in T1 and T4.
2. **Semi-analytic cross-check:** SD\* = √(RMSE_full² − V_sampling,mini − bias²) from the simulated sampling-only variances.

**Agreement is a validation check; disagreement is informative** — it measures the second-order effect that a large Δ also
mis-centres the miniature test temperatures (D-097), which the algebra cannot capture. This answers the brief's question
"how uncertain can the size correction be before the benefit of extra miniature specimens disappears?", per budget and per
strategy rather than as one global number.

## D-107 — Replicates, seeds, common random numbers, the paired Monte Carlo SE, and stability
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2 and 3); PRE-REGISTERED (WP6)

**Decision — replicates.** R = 1,000 in tiers T1, T2, T3 and T7; R = 500 in T4; R = 400 in T5; R = 200 programmes in T6.
Fixed before any result. **R is never chosen by which value makes a curve smoother**, and no cell receives a different R
because of its result.

**Decision — seeds.** `numpy.random.SeedSequence([20260918, h(cell_stream), h(component), replicate])`, with h the integer
of the first 15 hex digits of SHA-256 — the WP3 and WP4 construction (D-055). One independent stream per replicate per
component, so results do not depend on the worker count, the chunking or the execution order.

**Decision — common random numbers, declared in advance.** The standardized correction draw z and the specimen-noise stream
are keyed on (archetype, prior error, replicate index) and are therefore **shared across strategies, geometries and
correction-SD levels** within a replicate. This pairs exactly the comparisons the win and flip rules operate on. It is
declared here, before results, not adopted after seeing noisy curves.

**Decision — the availability gate and the Monte Carlo SE are separate quantities** (author's amendment, review round 3).
*Eligibility* is decided **once per cell on the complete R replicates** (availability ≥ 95 %, D-104); that is the sole use
of the gate. *The Monte Carlo SE* estimates the sampling error of ΔRMSE, where each cell's RMSE is its **conditional RMSE
over its available replicates**; the estimand is fixed first and the estimator mirrors it.

**Primary SE estimator: paired batch means over exactly 20 batches.** The R shared replicate indices are partitioned into
20 contiguous batches — **the same index batches in both cells** (R = 1000 → 50 each, R = 500 → 25, R = 400 → 20). Within
batch b each cell's conditional RMSE is computed from the available values in that batch, giving ΔRMSE_b; then
SE_paired = s({ΔRMSE_b}, ddof 1)/√20. This preserves the covariance created by the shared streams. **The 95 % gate is not
re-applied inside a batch**, because a noisy 50-replicate availability fraction would discard batches for no statistical
reason. The only batch-level rule: a batch with **zero** available values in either cell is dropped and counted, and if
more than **2 of 20** are unusable the comparison is labelled "paired SE unreliable — availability too low" and no winner
is declared. **The revision-1 proposal to combine two independent RMSE/√(2R) terms in quadrature is removed**: it is wrong
for cells that deliberately share random numbers.

**Declared cross-check, same estimand, no refits:** a **paired replicate-index bootstrap** — resample the R replicate
indices with replacement, apply the identical index set to both cells, compute each cell's conditional RMSE from its
available values, take ΔRMSE, repeat 2,000 times, and use the SD of the bootstrap ΔRMSE. It likewise does not re-apply the
gate inside a resample. It is reported beside the batch-means SE at every declared flip and for the stability subset;
disagreement by more than a factor 1.5 is reported, not silently resolved.

**Decision — Monte Carlo stability.** A predeclared subset — for each strategy, the cells at k = 4 and k = 24 and the cell
nearest the flip for archetype A5, at most 16 cells — is rerun at **R = 4,000** on an independent stream. **Criterion:**
every winner label unchanged, and the interpolated flip budget and SD\* each move by less than the grid spacing (or less
than τ in RMSE terms). Reported whether or not it passes.

## D-108 — The frozen experiment grid
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review rounds 2 and 3); PRE-REGISTERED (WP6)

**Decision.** Every cell of every tier is enumerated **before** implementation, so that no "representative" arm can be
chosen after results are visible. Archetypes A1–A9; reduced set {A1, A5, A9}; geometries G0–G7; budgets
k ∈ {4, 6, 8, 12, 18, 24}; strategies U, C, A, S (and SS in T7).

- **T1 headline.** A1–A9 (9) × 48 arms × 4 strategies; e_prior = 0; scatter C1; correction CENTRAL normal; normalization
  Sokolov. Arms: G0 × 6 budgets, and each of G1, G2, G3, G5, G4, G6, G7 × 6 budgets. **1,728 cells, R = 1,000.**
- **T2 prior sweep.** 9 prior levels × {A1, A5, A9} × 4 strategies × **8 frozen arms** (G0, G2, G5, G6 at k = 6 and 12).
  **864 cells, R = 1,000.**
- **T3 threshold sweep.** 8 correction-SD levels × {A1, A5, A9} × 4 strategies × **6 frozen miniature arms**
  (G2, G5, G6 at k = 4 and 8), bias fixed at −3.4941546891181936, e_prior = 0, scatter C1. Full-size comparators G0 at
  k = 4 and 8 are reused from T1. **576 cells, R = 1,000.**
- **T4 sensitivities.** 22 variants V1–V22 on {A1, A5, A9} × 4 strategies, using the frozen 6-arm set S6A
  (G0, G5, G6 at k = 6 and 12), the miniature-only 4-arm set S4M (G5, G6 at k = 6 and 12), or, for V16 and V17, the
  geometry-specific set (G0, G1, G5, G7 at k = 12). **1,296 cells, R = 500.** The variants are C1-robust, C2, C3-centred,
  C3-uncentered, miniature-inflated, CONSERVATIVE correction, the two empirical-family pools, five normalization scenarios,
  specimen-level draws, true LSE 6 J, the two envelope locations, the two machining allowances, the energy-scale injection,
  and the looser and stricter WP2 cohorts.
- **T5 breadth check.** Each of the 104 usable full-size WP3 fits as a truth × 4 strategies × **4 frozen arms**
  (G0 and G5 at k = 6 and 12). **1,664 cells, R = 400.**
- **T6 interval coverage.** **6 frozen cells** (G0 and G5 at k = 6, 12, 24), archetype A5, strategy U, e_prior = 0,
  scatter C1, correction CENTRAL. **R = 200 programmes, B = 500 bootstrap replicates each.**
- **T7 staircase.** Strategy SS × {A1, A5, A9} × e_prior ∈ {0, −40, +40} × S6A. **54 cells, R = 1,000.** Comparators
  already exist in T1 and T2.

**Total 6,188 cells, about 4.54 M simulated programmes, about 10.2 M fits.** The grid is not reduced for runtime; see
D-111.

## D-109 — The bounded interval-coverage sub-study
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 3); PRE-REGISTERED (WP6)

**Decision.** Tier T6 measures how a bootstrap interval behaves on a *simulated* programme, using the **approved WP4 pairs
bootstrap, unchanged** (D-052 to D-057). Two coverage quantities are reported **separately and never merged**:
- **Coverage A** — of the programme's own corrected estimand **conditional on its realised size correction**, i.e. of
  `T41J_true + Δ`. This isolates what the bootstrap actually samples.
- **Coverage B** — of the **true full-size T41J**, after programme-level size-correction uncertainty exists.
For full-size cells the two coincide because Δ ≡ 0. For miniature cells they must not: the bootstrap cannot see Δ, so
coverage B is expected to collapse while coverage A stays near the WP4 synthetic values. **That contrast is the result**,
and it is a practical warning about quoting a bootstrap CI on a sub-size-derived T41J. Median interval widths are reported
beside both.

**B = 500 is a bounded WP6 Monte Carlo coverage experiment only.** It neither replaces nor modifies WP4's approved
production procedure, which remains B = 2,000 per curve per method (D-055). No WP4 output, interval, rule or number is
affected, and nothing in WP6 may be described as a change to the WP4 bootstrap. **The bootstrap is never modified to
improve coverage.**

## D-110 — WP2 cohort propagation
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18); PRE-REGISTERED (WP6)

**Decision.** PROJECT_BRIEF.md §5 requires the headline to be tested against looser and stricter inclusion rules. WP6
propagates the CP2-frozen cohorts on the frozen T4 grid (variants V21, V22) through the two inputs it can legitimately
recompute:
- **true-curve archetypes** — USE and C quantiles re-derived from `outputs/wp3/fits_looser_cohort_curves.csv` (looser) and
  from the `in_stricter` subset of `outputs/wp3/fits_primary.csv` (stricter);
- **scatter profile** — re-aggregated with the unchanged D-061 definitions from the WP3 fits of that cohort; for the
  stricter cohort this is a filter of `outputs/wp4/published_residual_scatter_dataset.csv`, so **no WP4 run is repeated**.

**The WP5 size correction stays at the primary-cohort value in every cohort variant**, because D-071 fixes WP5 to the
CP2-frozen primary cohort and D-039 forbids regenerating cohorts. **That limitation is stated in the generated output**,
not worked around. No frozen cohort is touched, and the CP2 membership check runs before WP6 reads anything.

**Alternatives.** Rerun WP5 per cohort. **Why not.** It would require changing a frozen cohort, which needs its own
approved decision (D-039), and CP4 did not approve one.

## D-111 — Computational architecture, memory, determinism and the runtime stop rule
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: APPROVED (WP6 plan, author 2026-09-18, amended at review round 3); PRE-REGISTERED (WP6)

**Decision.** WP6 is built for the 8 GB project machine from the start, applying the WP4 lesson (D-067 steps 3–5):
- execution through the existing `wp4_bootstrap.stream_map` — spawn context, **3 worker processes by default**
  (`WP6_WORKERS` to override), workers recycled after 200 tasks, tasks fed lazily from a generator, results consumed one
  at a time;
- **workers return per-cell summaries and a compact float32 error array, never specimen-level data**; across all 6,188
  cells the stored per-replicate errors total about 25 MB, so exact quantiles need no streaming approximation;
- no simulated data set is written to disk except the single worked-example programme used for figure 9;
- **checkpoint and resume** through `src/wp6_checkpoint.py`, which has its own `SOURCES` list and reuses
  `src/wp4_checkpoint.py`'s atomic-write and fingerprint helpers **without editing any WP4 file**, so the WP4 cache is not
  invalidated. One fingerprinted `.npz` per cell block in the git-ignored `cache/wp6/`, reused only when code, package
  versions, parameters and inputs are identical; a stopped run recomputes only the missing blocks;
- **determinism**: per-replicate seeds make every result independent of worker count, chunking and order (validation
  test 6).

**Runtime stop rule (author's instruction).** The order of work is: implement → run the validation suite → **benchmark
actual runtime and peak memory on a declared subset** → if the projected full-run wall time is **≤ about 10 hours** and
memory is safe, run the complete frozen grid; **if it materially exceeds that, or memory safety is questionable, STOP and
report the benchmark to the author before any reduction is proposed.** Runtime alone is not a reason to reduce scientific
coverage. The **measured** runtime, not an estimate, is what goes into `README.md` and `run_all.sh` (the D-067 step 8
precedent).

**Hard constraint.** WP6 changes no WP0–WP5 source file, output, cohort or decision. The only pre-existing files it touches
are `run_all.sh`, `DECISIONS.md`, `PROGRESS.md` and `README.md`.

## D-112 — How the WP6 method was arrived at (chronological, including everything computed before pre-registration)
**Status:** FINAL APPROVED (CP5, author 2026-09-19). Earlier: record. PRE-REGISTERED (WP6) for steps 1–4; extended as work proceeds. No step is rewritten later.

1. *State reconstruction and planning, before any WP6 code existed (2026-09-17/18).* The approved state was verified
   read-only: branch, CP4 merge, 213 tracked files, the exact CP4 handoff numbers, the WP4 residual profile and the WP3
   parameter quantiles. `PROJECT_BRIEF.md` §5, §6.2 and §9, `PROGRESS.md` and the WP3, WP4 and WP5 sections of this file
   were read in full.
2. *Calculations performed during planning, before any decision above was fixed.* All ran outside the repository and none
   is a WP6 result; each is regenerated by the implementation under the pre-registered procedure. They are recorded here
   because they could in principle have influenced a choice.
   a. *Fitter benchmark (timings only):* 6.1–15.4 ms per full evaluation at N = 6…3,000, used to size the experiment.
   b. *C2 calibration arithmetic* against the WP4 profile: σ_T ≈ 7.38 °C, cv ≈ 0.057, region ratios
      0.28 / 0.70 / 1.09 / 0.92 / 1.04. **This is the evidence behind D-095 and it is a calibration diagnostic, not a
      simulation outcome.**
   c. *Feasibility pilot:* full-size T41J RMSE against N (17.8 °C at N = 4 down to 1.67 °C at N = 240), the clustered and
      prior-error variants, and the availability collapse to 3–18 % at e_prior = ±80 °C. Used to confirm that the budget
      ladder brackets the flip and that the availability gate does real work. The grid was chosen to **bracket** the flip,
      which is the brief's stated objective; no estimator, rule, metric or tolerance was chosen to produce a preferred
      winner.
   d. *Sign-convention check* of the correction injection: injected −25 / −3.5 / 0 / +15 °C returned −25.32 / −3.82 /
      +0.22 / +14.97 °C.
   e. *WP5 residual structure* read from the approved outputs: between-family SD 11.43 °C, within-family spread 23.2 °C on
      3 df. Used only to argue the D-098 programme-level draw.
   f. *Family-pool reconstruction:* the 7 primary and 10 all-STRICT family-level residuals rebuilt from
      `outputs/wp5/size_correction_residuals.csv`, reproducing the approved family-weighted means and SDs to 13
      significant figures.
   g. *Raw-envelope consequence calculation:* the coldest reachable full-size-equivalent temperature `−196 + M` per
      geometry, the clipped share of a 250 °C uniform span, and the number of the 104 usable full-size fits lying below
      each geometry's floor (21 of 104 for G1, 7 for G2). This motivated withdrawing the geometry-collapse claim (D-092)
      and widening the envelope sensitivity (D-093).
   h. *Raw miniature energy scale* implied by NF_E (0.64 J for a 200 J material at G1), used only to quantify the
      already-declared un-modelled resolution floor (D-096).
3. *Three author review rounds of the written plan (2026-09-17/18), all before implementation.*
   a. Round 1: the plan was written and presented with every decision listed for approval.
   b. Round 2: 14 amendments. C1 approved as the central scatter model against the D-066 preference (D-095); C3 amended to
      centred resampling (D-094); the programme-level correction draw approved (D-098); the ±4 SD truncation removed and
      the empirical-family sensitivity made required (D-099); all seven WEAKLY SUPPORTED geometries simulated and the
      nine-row reconciliation required (D-092); the budget accounting declared idealized (D-091); the paired batch-means
      SE replacing an incorrect quadrature (D-107); the label-threshold robustness matrix added (D-105); the staircase
      promoted to a required sensitivity and adaptation counts required (D-101); every reduced cell frozen (D-108); T6
      approved (D-109); D-100 approved unchanged; the grid not reduced for runtime (D-111).
   c. Round 3: the physical test-temperature envelope corrected to the **raw specimen** frame, with the placement order
      fixed (D-101); the global geometry-collapse claim withdrawn and restricted, and validation test 12 split into
      interior and boundary parts (D-092); raw-feasibility validation and the clip diagnostics added; translation
      invariance restricted and the envelope sensitivity made geometry-specific (D-093); the miniature scatter coordinate
      made explicit (D-096); the empirical-draw double-counting rule made explicit (D-099); the availability gate and the
      Monte Carlo SE separated (D-107).
   d. Round 4: one remaining coordinate-frame ambiguity corrected — the prior is stored and passed in the
      full-size-equivalent frame for U, C, A and S, and **M is subtracted exactly once**, inside `place()`; SS is the
      deliberate raw-space exception; validation test 19 added (D-101). Two reporting clarifications added: the
      conditional-independence caveat on large-N miniature gains (D-096) and the statement that T6's B = 500 does not
      modify WP4's approved B = 2,000 (D-109).
4. *Pre-registration commit.* D-090 to D-112 and the WP6 source modules — `wp6_design.py`, `wp6_scatter.py`,
   `wp6_correction.py`, `wp6_simulator.py`, `wp6_checkpoint.py`, `wp6_validation.py`, `wp6_experiment.py`,
   `wp6_tests.py` — together with the frozen grid definition and the calibration diagnostics, committed **before any
   headline WP6 cell was run**.
5. *Implementation checks and validation, after the pre-registration commit and before any headline cell.*
   a. *Two validation tests found real defects; both were fixed in the simulator, not in the test.* (i) Test 2: the
      miniature analysis branch recomputed M from the rounded Sokolov Eq. 22 instead of using the geometry's approved
      M, so the full-size case (Eq. 22 gives +0.432 deg C there, the published rounding residue recorded by WP5
      self-check 2) was not an exact identity. There is now one analysis path, asserted equal to
      `wp5_normalization.normalize()` for all seven miniature geometries. (ii) Test 17: the snapping sub-check
      conflated snapping with clipping, and applied a half-grid bound to the difference of two independently snapped
      designs; it now asserts each design's own residue within half a grid step and their difference within one.
   b. *Test 18, made precise.* Resampling a finite pool reproduces its population SD (the sample SD x sqrt((n-1)/n),
      10.586 deg C for the 7-family pool), not its ddof-1 SD; the test asserts the mean against the approved value
      and the SD against the population SD, with the relation printed. Its purpose - that no bias is added - is
      tested by the mean and is unchanged.
   c. *Implementation clarification, fixed before any result.* The physical floor of -196 deg C is not a multiple of
      the 5 deg C grid, so a temperature cannot be both inside the envelope and on the grid at -196 deg C. Clipped
      specimens are placed at -195 deg C, the coldest point satisfying both approved requirements of validation test
      16; no specimen is ever tested below the physical floor. Consequence: the coldest reachable full-size-equivalent
      temperature is -195 + M, and 22 (not the 21 quoted in planning) of the 104 usable full-size fits are
      unreachable for `20x1.5x1.5`. Recorded in `method_configuration.md` for the author to confirm or reverse.
   d. *Benchmark (D-111).* 62 cells (every 100th of the frozen grid), 0.51 % of the fit-weighted work: 148.3 s with
      3 workers, projected full run 8.13 h, peak 258 MB, both within the approved thresholds. A later re-invocation
      was served entirely from the warm checkpoint cache and overwrote the record with a meaningless 0.01 h; the
      cold-run measurement was restored before commit, and `benchmark()` now refuses to report a cache-served timing.
   e. *Smoke test.* The whole pipeline ran once at 2 % of the replicates in a scratch checkpoint directory outside
      the repository, to exercise every reporting path and the independent check module (`src/wp6_tests.py`, 11
      checks). Its outputs were overwritten by the real run and never committed.
6. *First full run with the frozen grid (results now exist).* 389.5 min with 3 worker processes, peak 313 MB; all 11
   independent checks passed. The T1 headline, the SD* table, the sensitivity summary, the interval coverage and the
   breadth check were then inspected.
7. *Two deviations from the approved plan, found AFTER results existed, both corrected TO the plan as approved - not
   to a new rule.*
   a. *V5, miniature-inflated scatter.* The D-108 grid and D-096 specify it for the **miniature arms only**, with the
      full-size arms of that variant kept on C1 as the reference; the first implementation applied the WP4 miniature
      profile to the full-size arms as well. It was noticed because the V5 result pointed the implausible way (a
      +5.05 deg C median shift toward miniature, since inflating the scatter of a small-N full-size programme costs
      it far more than a large-N miniature one). Corrected: a -0.51 deg C shift toward full-size and no miniature win.
   b. *V21 and V22, WP2 cohort propagation.* D-110 requires both the archetypes and the scatter profile to be
      re-derived for each cohort; the first implementation re-derived only the archetypes. Found by auditing the code
      against D-110 after results existed. Corrected with the unchanged D-061 definitions (`profile_from_curves`);
      validation test 13 now also asserts that the re-aggregation reproduces the approved WP4 profile exactly for the
      primary cohort. The stricter cohort's central-transition scatter is 0.1183 against 0.1052 (primary).
   c. *Reporting changes made after results existed, recorded as such.* (i) Each paired comparison is now computed on
      the replicate indices both cells share: D-107 defines the paired estimand on shared replicates, and the first run
      had combined a 1,000-replicate full-size RMSE with a 500-replicate miniature RMSE wherever the two tiers differ in
      R. That affects 480 comparisons (T4 variants against their T1 full-size comparators) and moved **14 of their
      480 labels**; no T1, T2, T3 or T7 label is affected. (ii) The paired replicate-index bootstrap SE, declared in
      D-107 as the cross-check but not computed in the first run, is now reported for T1 and T3: it agrees with the
      batch-means SE within a factor 1.5 in 97 % of T1 comparisons. (iii) A canonical `winner_class` for grouping,
      because the INELIGIBLE label embeds the availability percentages. (iv) Adaptive update counts grouped by the
      specimen count as well, because the machining-allowance variants had been averaged into the same (geometry,
      budget) row.
   d. *Because 7a and 7b changed fingerprinted sources, the whole checkpoint cache was invalidated and the complete
      frozen grid recomputed from cold:* validation re-passed (20 rows), the benchmark re-projected 4.89 h, and the
      second full run took 381.4 min with a 321 MB peak.
   e. *Determinism across two complete cold runs:* every T1 value of the second run reproduces the first exactly (the
      corrections did not touch T1).
8. *After the second run.*
   a. *Checkpoint-path collision.* The R = 4,000 stability rerun wrote to the same cache path as its R = 1,000 main
      cell. Fingerprints ensured no wrong value was ever used, but those 11 cells would have been recomputed on every
      run; the stability subset now has its own cache folder.
   b. *The stability deltas all point the same way* (median -0.25 deg C). By the declared common-random-number design,
      every R = 1,000 miniature cell uses the same 1,000 correction draws, so the eleven deltas are one sampling
      difference repeated, not eleven independent ones; the correction-RMS difference between the two samples alone is
      -0.22 deg C, within one Monte Carlo SE (0.27 deg C). Every label is unchanged and every delta is below tau, so the
      pre-registered stability criterion passes.
   c. The summary writer was rewritten so that every number quoted in `wp6_summary.md` is computed from the tables.
   d. **No estimator, decision rule, threshold, tolerance, grid cell, archetype, scatter model, correction value, prior
      level, replicate count or seed was changed because of any result.**
9. *Findings the approved plan anticipated differently, reported rather than hidden.*
   a. The machining allowance was expected to disadvantage the smaller specimens (D-091), which is true of the
      specimen counts; in RMSE terms it **favours** miniature, because the full-size count at k = 6 falls to 4 or 3,
      where the full-size RMSE is steep in N, while the miniature RMSE already sits at its correction floor. The
      idealized accounting is therefore, if anything, favourable to full-size.
   b. The simple staircase SS is far better than the batched model-based adaptive design S for full-size programmes;
      the adaptive conclusion depends on the algorithm, which is exactly the question tier T7 was required to answer.
10. *An ambiguity in the approved adaptive algorithm, found AFTER results existed, left as pre-registered and put
    to the author at CP5.* D-101 places each adaptive block at `T_hat + delta * C_hat` with "delta cycling 0, -0.5,
    +0.5, -1.0, +1.0, -1.5, +1.5, ...". The pre-registered code (commit `3714fe7`, `wp6_design._delta_cycle`) reads the
    ellipsis as EXTENDING the pattern (-2.0, +2.0, ...); the word "cycling" also admits a WRAPPING reading that repeats
    the listed values and keeps every specimen within +/- 1.5 C_hat of the estimated crossing. It was noticed in the
    worked-example figure, where a 21-specimen miniature block is spread to +/- 5 C_hat and many specimens are clipped
    at the envelope. Scope, measured: the listed values cover blocks of up to 7 specimens, and **every full-size S
    cell (block size at most 4) uses only the listed values, so no full-size result depends on the reading**. It
    matters for 1,138 miniature S cells, whose later blocks reach up to 122 C_hat and are largely clipped (mean clip
    fraction 36 % against 14 % for U); their RMSE barely moves (RMSE(S) - RMSE(U) median +0.04 deg C, range -0.62 to
    +0.43 deg C in T1) because the correction floor dominates, and no miniature S cell fails the availability gate.
    **The pre-registered reading is kept and nothing was rerun; changing an algorithm after its results are visible is
    exactly what the pre-registration forbids.** Whether to add the wrapping reading as a labelled sensitivity is the
    author's decision at CP5.
11. *A validation test that had passed without testing its property, found after results existed and corrected.*
    Validation test 6 (determinism) ran the same cells with 1, 2 and 3 worker processes through the checkpointed
    runner; the first configuration saved its results and the later ones read them back, so the test compared one
    computation with itself and **did not establish worker-count independence**, although the validation commit
    (`b24e7f6`) described it as doing so. The runner now has `use_cache=False`, which tests 6 and 9 use: rerun with every
    configuration computed afresh, test 6 passes - identical per-cell errors and outcome counts for 1, 2 and 3 workers
    and a reversed task order. Separately, the two complete cold runs reproduced every T1 value exactly (run-to-run
    determinism). Tests 6 and 9 had also overwritten 14 main-grid checkpoints with their small-R results (fingerprints
    ensured no wrong value was ever used; those cells were simply recomputed); they no longer touch the cache. The
    committed benchmark record is no longer overwritten by later measurements, which go to the git-ignored cache,
    because a wall-clock time is not a regenerable number (the D-067 precedent). No result changed.
12. *The CP5 reproducibility check (no code, rule, seed or result changed).* `./run_all.sh` from the repository with
    `cache/wp6/` moved aside, so every WP6 cell was recomputed from the raw data: **exit 0**; WP0-WP5 regenerated; the 19
    validation tests passed on the cold cache (test 6 computing every worker configuration afresh); the 11 independent
    checks passed; and **0 tracked files under `data/`, `outputs/` and `src/` or `run_all.sh` changed** - every WP0-WP6
    output regenerated byte-identically from raw data. The cold benchmark projected 5.58 h (peak 464 MB). The WP6 step
    took 1,258.7 min of wall-clock time (the whole script 76,078 s), peak 320 MB, because the machine entered idle sleep
    on battery during the run (125 sleep entries in the system power log) and the computation advanced only during brief
    dark wakes; the processing rate was the benchmark's until then. The two complete cold runs on an awake machine, 389.5
    and 381.4 min, are the runtime figures recorded in `run_all.sh` and `README.md`.
13. *CP5 approval session (author, 2026-09-19; every result it concerns already existed, in the committed state
    `26c8a84`).*
    a. *Decided:* D-090 to D-112 FINAL APPROVED, including the whole chronology; the pre-registered EXTENDING reading of
       the adaptive delta sequence kept, with the wrapping reading **not** added as a sensitivity and the wording
       ambiguity preserved as a limitation; −195 °C confirmed as the coldest raw test temperature, with the 22-of-104
       consequence kept and recorded as an implementation clarification; the headline approved in CONDITIONAL form with
       the "not universally better" constraint; the T6 interval finding approved as a mismatch of two uncertainties
       rather than a failure of the WP4 bootstrap; physical reachability approved as a first-class result, with
       feasibility failures kept separate from RMSE comparisons; no further expensive WP6 runs (CP5 approval record).
    b. *Changed:* documentation and status wording only, in `DECISIONS.md` (the CP5 approval record, the status line of
       every WP6 entry, this step), `PROGRESS.md` and `README.md`. The pre-registered text of every entry is unchanged.
    c. *Not changed:* any code, data, cohort, estimator, rule, threshold, seed, grid cell, scatter model, correction
       value, label, number, generated table or generated figure. No WP6 computation was rerun, so generated text keeps
       its generated wording (D-067 step 9c precedent): `method_configuration.md` still records the −195 °C
       clarification as awaiting the author's confirmation, and `wp6_summary.md` still lists the adaptive delta reading
       as open. This file and `PROGRESS.md` are authoritative for the CP5 decisions.
    d. *Checks (lightweight; no cold recomputation, author's CP5 instruction 7):* `git diff` showed **0 changed files**
       under `data/`, `outputs/`, `src/` and `run_all.sh` against the approved results commit `26c8a84`; the 11
       independent checks of `src/wp6_tests.py` passed, including that WP0–WP5 outputs and sources are byte-identical to
       `main` and that the 11 raw-data checksums verify; the frozen grid still holds 6,188 cells with the tier counts
       1,728 / 864 / 576 / 1,296 / 1,664 / 6 / 54.
    e. `wp6` is merged into `main` with an explicit merge commit and kept; no remote, no push; `AGENTS.md` untouched and
       untracked. **WP7 has not started.**

---

# WP7 — Report, repository and delivery

WP7 writes the deliverable and finishes the repository. It performs **no new analysis**: every number it
reports already exists in a table regenerated by WP0–WP6, and all four figures PROJECT_BRIEF.md §6.2 requires
already exist. The report, its filled source and its claim-to-source map regenerate with
`src/wp7_report.py`, and `src/wp7_tests.py` checks them independently, into `report/`.

**WP7 changes no WP0–WP6 code, output, cohort or decision.** The only pre-existing files it touches are
`run_all.sh`, `README.md`, `PROGRESS.md`, `AGENTS.md` and this file. This is not merely a convention: the WP6
independent check `src/wp6_tests.py::c10_wp0_wp5_untouched` compares `data/`, `outputs/wp0`–`outputs/wp5` and
every WP0–WP5 source file against `main` with `git diff` and **raises**, so any WP7 edit to an approved output
or source would stop the pipeline on this branch until the merge (D-118).

**Status legend for this section:** `PRE-REGISTERED (WP7)` = written and committed before the report text and
the report build it governs existed (the commit is named in D-124). `APPROVED (WP7 plan)` = approved by the
author in WP7 Plan Mode, before any report text existed. `FINAL APPROVED (WP7)` = approved by the author at
the final review; the earlier statuses follow it as history and no pre-registered text is rewritten.

**There is no CP6.** PROJECT_BRIEF.md §9 stops at CP5, so the gate before `wp7` is merged into `main` is a
**final author review**, not a numbered checkpoint. CLAUDE.md's rule is unchanged: merge only after the
author approves.

**Sources cited in WP7.** No new source is introduced. Every citation in the report is one this repository
has already read and recorded in the WP2–WP6 source lists above, carrying the same honesty marker it carries
there (*full text read*, *abstract only*, or *cited second-hand through …*). The matplotlib PDF backend's
documented behaviour for suppressing `Creator`, `Producer` and `CreationDate` is a property of the pinned
environment (D-002), verified in `matplotlib/backends/backend_pdf.py`, not a literature citation.

## D-113 — Report format and the PDF toolchain
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Context.** PROJECT_BRIEF.md §6.1 requires a PDF of roughly 10–15 pages and §6.3 requires that **one
command** regenerate every figure and every number in it. The development machine has no `pandoc`, no TeX
distribution, no `wkhtmltopdf` and no `weasyprint`, and `run_all.sh` refuses to run unless the pinned package
versions of `requirements.txt` are present (D-002).

**Decision.** The report is typeset into a multi-page PDF by `src/wp7_report.py` using **matplotlib's
`PdfPages`**, already pinned at 3.9.4, with `metadata={"Creator": None, "Producer": None,
"CreationDate": None}`. The approved PNG figures are embedded from `outputs/` as they are; the report never
re-plots them, so it cannot drift from the figures the checkpoints approved. Source of truth for the prose is
`report/report.md`; the build also writes `report/report_filled.md` (the same text with every number
substituted) so a reviewer can diff prose changes without opening a PDF.

**Why.** (i) It adds no dependency, so the environment in which every WP0–WP6 result was verified is
unchanged. (ii) The PDF regenerates **byte-identically**, the same property every figure in this repository
already has (`metadata={"Software": None}`), which makes "one command regenerates the report" checkable
rather than asserted. (iii) It keeps the deliverable inside `./run_all.sh` with no manual step.

**Alternatives.** (1) Pin `reportlab` and typeset with Platypus flowables. (2) Generate Markdown only and
produce the PDF by hand outside the pipeline. (3) Install a TeX distribution.

**If an alternative were chosen.** (1) would give better typography — a real paragraph, table and
page-number engine — at the cost of amending D-002, a network install, and `rl_config.invariant` plus fixed
document dates to recover byte-identical output; the pinned environment would no longer be the one WP0–WP6
were verified in. (2) would leave the PDF outside the pipeline and fail the §10 checkbox outright. (3) is a
large unpinned system dependency for one document.

**Known cost, stated plainly.** A matplotlib-typeset report has plainer typography than a LaTeX or Word
document: no hyphenation, no float placement, and tables drawn as text grids. That is accepted in exchange
for reproducibility, and is the same trade this project has made throughout (brief §1.1: prefer a transparent
method the author can defend).

## D-114 — Every number in the report is substituted from a generated table at build time
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** `report/report.md` is written by hand and contains **no literal result numbers**. Each numeric
claim is a typed placeholder resolved at build time by a registry in `src/wp7_report.py` that names, per
placeholder, the generated file, the row selector, the column and the print format. The build:
- fails with a non-zero exit if any placeholder is unresolved, if a named file is missing, if a row selector
  matches zero or more than one row, or if a registry entry is never used;
- emits `report/claim_source_map.csv`, one row per numeric claim, carrying the placeholder, the rendered
  value, the file, the row selector, the column and, for a derived value, its inputs and the expression;
- fails if a digit appears in the report prose outside a placeholder, a protected span (dates, section
  numbers, equation constants, citation years, specimen dimensions quoted from a standard) or a table
  rendered from a generated file.

**Why.** PROJECT_BRIEF.md §6.1 requires every numeric claim to be traceable to code and §10 requires that no
number appear that the repository cannot regenerate. A hand-maintained table of numbers goes stale silently
the first time an upstream value moves; a build that refuses to produce a PDF cannot. This also makes
Appendix A a by-product rather than a document to keep in step by hand.

**Alternatives.** (1) Write the numbers into the prose and check them by hand against the tables.
(2) Maintain the claim map as a separate hand-written file.
**If an alternative were chosen.** Both would satisfy the brief on the day they were written and would rot
afterwards, and neither would detect an upstream change.

**Limitation.** The lint cannot tell a *correct* claim from a *well-sourced* one: a placeholder pointed at the
wrong row renders a real number from a real file. That is what the independent checks of `src/wp7_tests.py`
and the hand spot-check in the verification record are for.

## D-115 — Which figures and tables the report carries
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** Seven figures (eight images) and eight tables in the body, every one an existing generated
file. **WP7 creates no new figure and no new table.** The brief's four required figures map as follows:

| brief §6.2 | report figure | file |
|---|---|---|
| 1 worked example | Figure 1 | `outputs/wp4/worked_example_t41j_bootstrap.png` |
| 2 uncertainty vs specimen count, series per placement strategy | Figure 2 | `outputs/wp6/rmse_vs_specimen_count.png` |
| 3 size normalization before/after, faceted by product form, residual quantified | Figures 3a and 3b | `outputs/wp5/before_after_normalization.png`, `outputs/wp5/size_correction_residuals.png` |
| 4 fixed-volume comparison with the crossover | Figure 4 | `outputs/wp6/fixed_volume_comparison.png` |

Plus Figure 5 `correction_uncertainty_flip.png` (SD\*), Figure 6 `prior_error_vs_performance.png` (prior
knowledge and the availability gate) and Figure 7 `synthetic_error_vs_specimens.png` (SYNTHETIC fitter
validation). Tables 1–8 are rendered from `wp1/reconciliation_table.csv`, `wp2/population_accounting.csv`
with `wp2/cohort_manifest.csv`, `wp3/fit_outcomes.csv` with `wp3/index_availability_by_geometry.csv`,
`wp4/interval_curve_accounting.csv` with `wp4/published_uncertainty_crosscheck.csv`,
`wp5/size_correction_summary_overall.csv` with its product-form and irradiation companions,
`wp6/fixed_volume_comparison.csv`, `wp6/correction_threshold.csv` and `wp6/sensitivity_summary.csv`.

**The brief asks for one faceted figure 3 and this repository answers with two.** The curve-level before and
after comparison and the residual faceted by product form are separate approved figures. The report says so
in the caption rather than implying a single figure was produced. Drawing a combined figure would mean new
plotting code writing into `outputs/wp5/`, which D-118 forbids and `src/wp6_tests.py::c10` would stop.

**Why this set.** It is the smallest set that answers the research question and Q1–Q4 without leaving a
claim unsupported: one figure per stage of the uncertainty stack, plus the two that carry the conditions
(SD\* and prior knowledge) and one that shows the estimator was validated before it was trusted.
**Alternatives.** Print only the four required figures; print all twenty-nine.
**If an alternative were chosen.** Four would leave Q4's conditions and the fitter validation unillustrated;
twenty-nine would bury the four that carry the argument and break the page budget.

## D-116 — The headline is reported in the CP5-approved conditional form, and generated tables outrank prose
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** The report states the WP6 result only in the conditional form the author approved at CP5
(CP5 approval record item 4), quoted verbatim in §8 and paraphrased nowhere that drops a condition. The
report **must not** claim that full-size specimens are universally better. Enforced, not merely intended:
`src/wp7_report.py` carries a forbidden-phrase lint that fails the build on unqualified superiority claims
("proves", "demonstrates that miniature specimens are worse", "full-size is better" without its conditions),
on "confidence interval" used without the word *nominal* for a WP4 interval, on "material scatter" without
its qualifier, and on "measured" applied to a transformed estimate; and it requires that any paragraph
carrying a win-or-loss claim about a miniature programme also carry the phrase *conditional fixed-volume
scenario using the pooled, WEAKLY SUPPORTED correction*.

Conditions that travel with the headline everywhere it appears: the ≈12 °C floor is
`sqrt(bias^2 + SD^2)` under the CENTRAL scenario with the CONSERVATIVE value beside it; the correction
assumption dominates the scatter model; no individual miniature geometry has a DIRECTLY SUPPORTED correction
distribution and the pooled one is WEAKLY SUPPORTED; the volume accounting is idealized finished-specimen
accounting, not a capsule machining-yield model; the smaller specimens are miniature/MCVN, not conventional
ASTM E23 sub-size; and irradiation × geometry is unresolved.

**Why.** CP5 approved the headline in this form and in no other, and the generated tables remain
authoritative over prose. A report is where a conditioned result is most likely to lose its conditions, so
the conditions are enforced at build time rather than left to a careful writer.
**Alternatives.** Rely on careful writing and review.
**If the alternative were chosen.** One unqualified sentence in a fifteen-page document would misstate the
project's central finding to exactly the reader the brief is written for.

## D-117 — Four evidence classes, labelled on every figure and table
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** The report defines four classes once, in the front matter, and carries one of them as a label
on **every** figure caption and table header. `src/wp7_report.py` fails the build if any is untagged.

| label | meaning | where it comes from |
|---|---|---|
| **MEASURED (published)** | A value published by one of the 109 source studies and compiled in the dataset | `data/raw/`, WP1, WP2 |
| **FITTED (derived from published data)** | A parameter or interval estimated from those measurements | WP3 parameters and T41J; WP4 intervals and residual scatter |
| **TRANSFORMED ESTIMATE (derived from published smaller-specimen measurements)** | A published smaller-specimen measurement mapped into the full-size-equivalent domain by a classical correction. **Never called a measurement** | WP5 normalized points, refits and ΔT_size |
| **SYNTHETIC** | Generated by this project from known truth; not a measurement of anything | WP3 validation, WP4 bootstrap validation, all of WP6 |

**Why.** PROJECT_BRIEF.md §7 forbids any implication that measurements were produced here and requires
synthetic data to be labelled synthetic everywhere it appears. The middle two classes are the ones a reader
can most easily conflate, and WP5's own outputs already insist on the distinction (D-077).
**Alternatives.** Label only the synthetic material, as the brief's literal minimum requires.
**If the alternative were chosen.** A transformed full-size-equivalent estimate could be read as a full-size
measurement, which is the single most misleading mistake this report could make.

## D-118 — Generated WP0–WP6 text is left exactly as generated
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Context.** Three generated summaries still carry the status they had when they were written:
`outputs/wp4/wp4_summary.md` says the internal review is awaiting the author and WP5 has not started;
`outputs/wp5/wp5_summary.md` says CP4 is awaiting author approval; `outputs/wp6/wp6_summary.md` §10 lists the
adaptive delta reading as open for the author. All three statements were true when generated and all three
have since been decided.

**Decision.** WP7 does **not** edit them, and does not edit any other WP0–WP6 output or source.
`DECISIONS.md` and `PROGRESS.md` are authoritative for approval status; a generated summary carries its
generation-time status line. The convention is stated explicitly in `README.md`, in the report's
reproducibility appendix, and here, and the three affected lines are named, so a reader meets the convention
before meeting the discrepancy.

**Why.** (i) It is the precedent this project has already set three times, for exactly this reason: D-067
step 9c, D-088 and D-112 step 13c each recorded that changing generated text requires a code change and a
regeneration. (ii) Changing it now would edit `src/wp4_uncertainty.py` and `src/wp5_size_effect.py`, which
makes `src/wp6_tests.py::c10_wp0_wp5_untouched` raise and **stop `./run_all.sh`** on this branch until the
merge, because that check compares those paths against `main` with `git diff`. (iii) It would break the
standing reproducibility result that a full run changes **0 tracked files** under `data/`, `outputs/` and
`src/` — a result worth more than three cosmetic lines.

**Alternatives.** (1) Fix all three, and amend `c10` to compare against the merge-base rather than `main` so
the pipeline still passes on the branch. (2) Fix only the WP6 line, which `c10` does not police.
**If an alternative were chosen.** (1) is defensible and costs little compute — neither
`src/wp4_uncertainty.py` nor `src/wp6_experiment.py` is in a checkpoint `SOURCES` list, so no bootstrap or
Monte Carlo cell would be recomputed — but it edits approved outputs and weakens an independent check to
accommodate the edit. (2) would leave the repository internally inconsistent in precisely the way a reviewer
would notice.

## D-119 — The comparison with the 2026 machine-learning paper
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** PROJECT_BRIEF.md §2.1 requires the relationship to [ML2026] to be stated explicitly. The report
carries a one-paragraph statement in §1.3 and the full factual comparison as §7.8, a named subsection of the
limitations section, because it is an honesty statement about what this work does and does not add. It
reports, as a table: the question each asks, the problem class, the data, the matching rule, the method, the
headline and the index used; then the overlap, the difference that matters, and what this work contributes.

**What is asserted, and on what basis.** [ML2026]'s full text was read from the arXiv PDF during WP5 and its
use is recorded in the WP5 source list. The comparison quotes their §3.1 matching definition, their Eqs (4)–(7)
transformation, and their Tables 5 and 7 performance figures. Their benchmark of classical methods is
described as larger and more systematic than anything here.

**The difference that matters, stated without insinuation.** Their transformation builds each training target
from the paired full-size curve. That is legitimate and necessary for supervised learning, their
cross-validation correctly holds out whole specimen sets, and their R² is an honest measure of *prediction*
accuracy. It is not, and **is not claimed by them to be**, an independent estimate of how much uncertainty a
classical correction adds. This project needs that second quantity, so its correction never sees the paired
full-size curve — a property checked numerically on every run (D-086 check 8).

**No novelty is claimed beyond this**: a strictly matched and fully audited pairing with every rejection
reason preserved; an out-of-sample correction; a residual-uncertainty estimate carrying an evidence status;
a statement of where the dataset is too thin to support one; and the propagation of that uncertainty into a
test-matrix design answer. This project trains no model and attempts no prediction (brief §2.1, §8).

**Alternatives.** Omit the comparison; or compare performance numbers head to head.
**If an alternative were chosen.** Omitting it fails a §10 checkbox. Comparing 11.4 °C against their
24.9–27.2 °C as though the two measured the same thing would be the exact error §7.8 exists to prevent: they
are different quantities on different samples with different indices.

## D-120 — The plain-language deliverable
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Decision.** Plain-language explanation lives in three places, each with a different job:
1. `report/PLAIN_LANGUAGE.md`, about two pages, covering the background PROJECT_BRIEF.md §11 says the author
   must hold in order to defend the work: why body-centred-cubic ferritic steels show a ductile-to-brittle
   transition and austenitic steels largely do not; what the Charpy V-notch test physically measures and why
   absorbed energy is an index rather than a transferable material property; why 41 J is the conventional
   criterion and what RT_NDT is used for; why surveillance capsules exist and why irradiated test material is
   scarce; what an ill-conditioned fit is; what a bootstrap does; what the size correction does and why a
   scalar volume ratio cannot capture constraint; and what a 12 °C error floor means in practice.
2. Three short *In plain terms* boxes in the report, at §1.2, §4.6 and the head of §6.4.
3. The plain-language summary of the finding in `README.md`, which PROJECT_BRIEF.md §6.3 requires.

**Why.** CLAUDE.md requires the engineering and statistics to be explainable to a first-year engineering
student, and brief §1.1 forbids black boxes. A professor, a technical interviewer and a first-year student
need the same content at different depths; separating the background primer from the report keeps the report
an engineering analysis document while giving the other two readers somewhere to start.
**Alternatives.** Put everything in the report; or rely on the README alone.
**If an alternative were chosen.** The first would push a 15-page report past its budget and change its
register; the second would leave brief §11's background list with no home.

## D-121 — AGENTS.md
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Context.** `AGENTS.md` has been the only untracked file in the tree since before WP5. It is a copy of
`CLAUDE.md` differing only in its title line. CP4 (D-088 check 8) and CP5 both deliberately left it alone
because those sessions were documentation-only.

**Decision.** Its duplicated body is replaced by a two-line pointer to `CLAUDE.md`, and the file is
committed. The delivered tree then has exactly one copy of the working rules and no untracked file.
**Alternatives.** Add it to `.gitignore`; delete it; leave it untracked and unmodified.
**Why.** Two copies of a rules file is a maintenance trap: the next session to edit one would silently
diverge from the other. A pointer keeps any other agent harness working while leaving `CLAUDE.md` the single
source.
**If an alternative were chosen.** Ignoring or deleting it would also give one source of truth, at the cost
of breaking a harness that looks for the filename; leaving it as it is would deliver a repository with an
untracked duplicate of its own rules.

## D-122 — Version sensitivity beyond WP2 is not run
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**The gap, stated rather than buried.** Brief amendment A1 and D-001 say the later stages "must test whether
the choice of release changes important conclusions". WP1 and WP2 are run on both releases and compared
(`outputs/wp1_sensitivity_eny5v-www93/`, `outputs/wp2_sensitivity_eny5v-www93/`,
`outputs/wp2/version_sensitivity_comparison.md`). **WP3 to WP6 are run on the 2025.30 primary release only.**
The two releases differ, in scope, by exactly refs 107 and 109 (148 records; 9 curves passing the primary
rule). Ref 107 supplies the only KLST matched comparison in WP5 and therefore one of the 7 independent
families behind the CENTRAL correction, so under 2024.206 the primary analysis set would fall to 6 families
and the pooled bias and SD would move by an amount this repository has not computed.

**Decision.** WP7 does not run it. The report states the gap, its exact scope and its direction in §7, and
names it among the things the analysis could not determine.

**Why not, with the cost.** (i) It is structurally blocked: D-039 freezes the CP2 cohorts and D-071 fixes WP5
to the CP2-frozen **primary** cohort, so propagating the sensitivity release downstream needs its own
approved decision against both. (ii) The cost is a WP3 + WP4 + WP5 + WP6 re-run, of order eight to nine hours
cold, and CP5 item 7 closed further expensive WP6 runs. (iii) The evidence already in hand indicates it does
not threaten the headline: the conclusion is set by the ≈12 °C correction floor, and the frozen sensitivities
already move that floor from about 11.1 °C (C1-robust) to about 26 °C (Towers) without reversing it, every
such move favouring full-size; the empirical 7-family resampling variant (V7) shows the answer is insensitive
to how those seven family values are used.

**This is not a claim that the release does not matter.** It is a statement that it was not tested downstream
and why, with the direction of the available evidence given. **Alternatives.** Run the full downstream
re-run; or recompute only the WP5 pool with the ref-107 family dropped.
**If an alternative were chosen.** The first answers the amendment directly at the cost above. The second is
seconds of compute but writes into `outputs/wp5/`, which D-118 forbids and `c10` would stop.

## D-123 — The plate-only correction floor is reported as arithmetic, never as a simulation result
**Status:** APPROVED (WP7 plan, author 2026-09-19); PRE-REGISTERED (WP7)

**Context.** D-083 and CP4 item 10 permitted the plate-only size correction (4 independent families from 3
publications; family-weighted mean −2.215 °C, SD 14.62 °C) to be carried into WP6 as a sensitivity or
diagnostic. The frozen T4 grid (D-108, variants V1–V22) contains no such variant, so **product form was never
tested in the simulation**. Adding a cell to a frozen grid after its results exist is what the
pre-registration forbids.

**Decision.** WP6 is not re-run. The report states the plate-only error floor as `sqrt(bias^2 + SD^2)` —
about 14.8 °C, against 11.96 °C for the pooled CENTRAL scenario and 23.69 °C for the CONSERVATIVE one —
**explicitly labelled as arithmetic on approved WP5 values, not as a simulated result**. The formula is the
one `src/wp6_experiment.py` already computes and prints for the CENTRAL and CONSERVATIVE scenarios; the
inputs, the expression and the source rows are recorded in `report/claim_source_map.csv` (D-114).

**Why.** The number is transparent, it is one line of arithmetic on two approved published-data values, and
it points **against** the reader's likely suspicion rather than for it: a plate-only scenario would raise the
miniature floor and favour full-size more strongly than the pooled one does. Suppressing it would leave a
permitted and unflattering-to-nobody sensitivity invisible; simulating it would break the frozen grid.
**Alternatives.** (1) Omit the number and state only that product form was never simulated. (2) Run a
plate-only T4 variant.
**If an alternative were chosen.** (1) leaves the reader to do the arithmetic from Table 5 unaided.
(2) costs minutes on a warm cache but adds a grid cell after results exist, which would require its own
approved decision and would cost the frozen-grid property CP5 approved.

**What this number is not.** It is not a simulated RMSE, not a measured quantity, and not evidence that
product form matters: it is what the floor arithmetic gives if the plate stratum's own residual scale is
substituted for the pooled one. The plate stratum is the only product form meeting the D-079 threshold;
forging (2 families) and weld metal (1 family) have no standalone estimate at all.

## D-124 — How WP7 was carried out (chronological, including anything found after the report existed)
**Status:** record. PRE-REGISTERED (WP7) for steps 1–2; extended as work proceeds. No step is rewritten later.

1. *State reconstruction, before any WP7 file existed (2026-09-19).* `PROJECT_BRIEF.md`, `CLAUDE.md`,
   `PROGRESS.md`, `README.md` and the whole of this file (D-001 to D-112) were read, with the WP0–WP6
   summaries, method configurations, figure-generating code, check modules, `run_all.sh` and the git history.
   Three facts found by reading the code rather than the documentation shaped the plan and are recorded
   because they constrain it:
   a. `src/wp6_tests.py::c10_wp0_wp5_untouched` compares `data/`, `outputs/wp0`–`outputs/wp5` and the WP0–WP5
      sources against `main` with `git diff` and **raises**, so any WP7 edit to an approved output or source
      would stop `./run_all.sh` on this branch until the merge (D-118).
   b. Neither `src/wp4_uncertainty.py` nor `src/wp6_experiment.py` appears in the `SOURCES` list of
      `src/wp4_checkpoint.py` or `src/wp6_checkpoint.py`, so **no WP7 change can invalidate a checkpoint**
      and no expensive recomputation is implied by anything in WP7.
   c. The machine has no `pandoc`, TeX, `wkhtmltopdf` or `weasyprint`; matplotlib's PDF backend documents
      removing `Creator`, `Producer` and `CreationDate`, which is what makes a byte-identical PDF possible in
      the pinned environment (D-113).
2. *WP7 plan approved by the author in Plan Mode (2026-09-19), before any report text existed.* Seven
   decisions were put to the author and answered: PDF via matplotlib `PdfPages` with no new dependency
   (D-113); generated WP0–WP6 text left exactly as generated (D-118); plain language as a standalone file
   plus report boxes plus the README summary (D-120); `AGENTS.md` committed as a pointer (D-121); the
   plate-only floor stated as labelled arithmetic (D-123); version sensitivity beyond WP2 recorded as a
   limitation only (D-122); and a named byline on the title page. The appendix policy, the final-review merge
   gate, committing the PDF and making the lint a hard build failure were taken as recommended.
   D-113 to D-124 and the report outline were then committed **before any report prose, any report build or
   any PDF existed**.
