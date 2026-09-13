# DECISIONS.md — judgement-call log

One entry per decision that could reasonably have gone another way (PROJECT_BRIEF.md §1.1 and §6.4).
Each entry states what was decided, the alternatives, why, and what would change under the alternative.
Where a number is quoted, the file that regenerates it is named.

**Status legend:** `DECIDED` = in force. `PROVISIONAL (CP1)` = in force for now, explicitly put to the author at
checkpoint CP1 for confirmation. `OPEN` = not yet decided.

**Sources cited below**
- [descriptor] Lee I., Merickel J.W., Sreenivasulu Y.K., Xu F., Tang Y., Rittenhouse J.E., Vakanski A., Song R. (2025).
  *Comprehensive Toughness Dataset of Nuclear Reactor Structural Materials using Charpy V-Notch Impact Testing.* Sci. Data 12:543.
  doi:10.1038/s41597-025-04823-1
- [record-A] Materials Cloud Archive record eny5v-www93, doi:10.24435/materialscloud:gh-za (issued 2024-12-19)
- [record-B] Materials Cloud Archive record q4x6v-dyt25, doi:10.24435/materialscloud:p6-5y (issued 2025-02-26)
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

---

## D-001 — Which release of the dataset is the project dataset
**Status:** PROVISIONAL (CP1)

**Context.** Two releases of the same dataset exist on Materials Cloud, under different parent records:
[record-A] (named in PROJECT_BRIEF.md; 4,775 records, 55 columns, 106 references) and [record-B] (4,961 records,
56 columns, 109 references, an extra `Specimen Type` column and a `Notes` curation sheet). The descriptor paper describes
and cites record-B, and the authors' GitHub repository holds a byte-identical copy of record-B's workbook (git blob SHA
533d056d…, checked at acquisition on 2026-09-12). The brief's own numbers mix the two (4,775 records from A; 109 publications from B).
Row-level comparison: `outputs/wp0/dataset_version_comparison.md`.

**Decision.** Use record-A, as the brief specifies. Vendor record-B beside it for comparison only, and run the WP1 pipeline
on both so the consequence of switching is known. Ask the author at CP1.

**Alternatives.** (1) Switch to record-B now (what the paper describes). (2) Hybrid: record-A plus corrections copied from B.

**Why.** The brief is the authoritative requirements document and names record-A; switching silently would change a requirement.
A hybrid would create a third, unpublished version. Evidence gathered for the CP1 discussion:
- For shared references, every measurement column (temperature, energy, dimensions, USE, curve ID) is identical in A and B.
  B changes only metadata (manufacturer, treatment, microstructure, orientation, irradiation fields) and 16 DBTT values.
- B adds references 107–109 (186 records), including a sub-size correlation study (107) relevant to WP5 and a WWER-440 steel (108) outside the brief's named family.
- Some of B's metadata corrections look wrong: four curves B relabels as irradiated (refs 8, 9, 9, 13; two with no fluence)
  match unirradiated curves from other publications point for point (`outputs/wp1*/duplicate_curve_removals.csv`; see D-021).

**If the alternative were chosen.** WP1 on record-B retains 3,409 records instead of 3,208 (`outputs/wp1_alt_q4x6v-dyt25/`),
adds KLST-type miniature specimens and 15Cr2MoV-A (pending scope), and imports B's irradiation relabels. Switching is one
setting (`PRIMARY_DATASET` in `src/common.py`).

---

## D-002 — Computational environment
**Status:** DECIDED

**Decision.** macOS system CPython 3.9.6 in a project-local virtual environment (`.venv/`), with pinned numpy 2.0.2,
pandas 2.2.3, openpyxl 3.1.5 (`requirements.txt`).
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

**Decision.** Store both workbooks, their `files_description.md` and archive record JSON snapshots in `data/raw/`, the CC BY 4.0
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
**Evidence.** No test temperature below −196.9 °C or above 377.6 °C for ferritic steels (no kelvin or °F pattern); irradiation temperatures
carry conversion fingerprints (149 °C = 300 °F, 288 °C = 550 °F, 269.85 °C = 543.00 K); every dataset curve's highest energy lies within
0.92–1.45× its USE (an unconverted ft·lbf curve would sit near 0.74× or 1.36×); all fluences 6.2×10¹⁷–1×10²⁰ (n/m² would be 10⁴× larger);
no inch-like dimensions; composition sums 100.000–100.019 wt.%.
**Alternatives.** Convert fluence to n/m²; re-derive units from each source paper.
**Why.** Verification found no inconsistency; converting what is already consistent adds a step without benefit.
**Limitation.** The energy check detects a unit error *within* a curve; a source whose energies and USE were both left in ft·lbf would pass. Only the source papers can rule that out.
**If the alternative were chosen.** n/m²: values ×10⁴, no analytical change.

## D-011 — Neutron energy threshold of the fluence values
**Status:** DECIDED (documented as unknown)

**Decision.** Record that the energy threshold (E > 1 MeV, E > 0.1 MeV, …) is not stated anywhere in the dataset. Do not assume E > 1 MeV.
**Alternatives.** Assume E > 1 MeV, the ASTM E900 convention.
**Why.** Different thresholds can differ by a factor of about two for the same irradiation; assuming would be a silent judgement.
**If the alternative were chosen.** Fluence would look comparable across sources when it may not be. Consequence for WP2: fluence binning must be coarse or per-source, and this uncertainty stated.

## D-012 — Material name harmonization: what was merged and what was kept separate
**Status:** DECIDED (15Cr2MoV-A scope is PROVISIONAL (CP1), record-B only)

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
| `15Cr2MoV-A` (record-B only) | own family, **scope pending** | Ferritic WWER-440 vessel steel, but not in the brief's named family; excluded provisionally in the record-B run (step E2). |
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
**Result.** After E1–E5 no record is impossible. Flags on retained records: two zero-energy records (refs 32, 43); nothing else (`flags_summary.md`).
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
**Status:** DECIDED (method); results for author review at CP1

**Context.** Several research groups republished the same Charpy curves in conference and journal papers (e.g. the KAERI SA508 Gr.4N series,
refs 10, 13, 14, 17, 19, 20, 26, 27, 28, 33, 37, 38; refs 52 and 55; 42 and 45; 43 and 44; 46 and 48; 22, 23 and 40), and the dataset digitized each figure separately.
None of the 752 removed points is bit-identical to its kept counterpart: matched points differ by a median of 0.26 °C and 0.4 % in energy (95th percentiles 1.15 °C and 9 %; the large relative differences are small lower-shelf energies), consistent with separate digitizations of the same data points. Counting them twice would double-count tests and understate scatter.

**Decision (method, `src/wp1_clean.py::find_duplicates`).**
- *Unit compared:* a dataset curve, split by reference, material, geometry, irradiation, fluence, treatment and condition statement.
- *Candidates:* two units with the same material family, same length/width/thickness, same irradiation status and fluence.
- *Point match:* one-to-one pairing with |ΔT| ≤ 3 °C and |ΔE| ≤ 2 % of the larger unit's maximum energy (a fraction of the plot's energy axis, because digitization error scales with the axis, not with the value; a fixed 1 J tolerance falsely matched sub-1 J miniature curves).
- *Duplicate:* ≥ 3 matched points and ≥ 70 % of the smaller unit matched. 50–70 % is flagged as partial overlap, not removed.
- *Which copy is kept:* the unit with most records, then earliest publication, then lowest reference ID. Every removed unit matches its kept unit directly.

**Evidence the threshold is not arbitrary.** The distribution of matched fractions has an empty 0.6–0.7 bin separating chance overlaps (0.1–0.6) from re-publications (0.7–1.0)
(`outputs/wp1/wp1_summary.md`). Across 36 parameter combinations (ΔT 2/3/5 °C × ΔE 1/2/3 % × fraction 0.6/0.7/0.8/0.9) removals range from 676 to 909
records (median 752): every setting with ΔT ≤ 3 °C removes 676–794, while ΔT = 5 °C removes 790–909 because the looser window admits more chance matches (`duplicate_sensitivity.csv`). All 66 removals were audited against metadata: composition differences are nominal-vs-measured
values of the same alloys; USE/DBTT of copies differ by a median of 0.5 J and 2 °C.

**Keep-rule comparison** (`duplicate_keep_rule_comparison.csv`): most-records-first removes 752 records and keeps 40 points found in no other copy; earliest-publication-first
removes 783 and discards 32 such points; most-corroborated-first removes 770. "Uncorroborated" points are either extra real data or errors, and cannot be told apart
without the papers. Example of an error: in dataset curve 90 (ref 19, kept) two points at 25 °C/210.85 J and 100.3 °C/233.6 J belong to a different alloy's
upper shelf on the same figure. Chosen rule removes only records that are demonstrably copies; every uncorroborated kept point carries
`flag_point_not_corroborated_by_duplicate_copies`; composition disagreements between copies carry `flag_duplicate_copies_disagree_on_composition`.

**Known limitations.** A duplicate whose labels disagree is not compared (ref 53 curve 237 labelled base metal vs weld-metal curve 241; the ref 52/55 irradiated 5 mm pair at 50 % match, flagged as partial overlap). Units with fewer than 3 points are never removed.

**Alternatives.** Keep all copies (double counting); remove only matched points rather than whole units (leaves fragments of 1–3 points); manual curation from the papers.
**If the alternative were chosen.** Keeping copies: +752 records, the SA508 Gr.4N alloys counted up to seven times, scatter understated. Point-level removal: similar totals, plus orphan fragments for WP2 to handle.

## D-020 — "Pre-Cracked" label in record-B
**Status:** PROVISIONAL (CP1)

**Decision.** Do not exclude. Flag records that record-B labels "Pre-Cracked" (`flag_precracked_label_in_later_release`) and, separately, references whose own text reports precracked specimens (`flag_source_reports_precracked_specimens`: ref 1; ref 44, whose records all left at E8).
**Evidence.** B labels every record of refs 1, 8, 9, 13, 19, 20, 23. These records are 55×10×10 mm V-notch specimens with ASTM E23 cited where a standard is given, lower shelves of 2–4 J and upper shelves of 180–360 J, typical of standard Charpy tests. [Lee2011] states Charpy tests to ASTM E23 and fracture toughness to ASTM E1921 — the precracked specimens were for the separate toughness tests. Precracked fracture-toughness tests do not normally produce absorbed-energy transition curves. Ref 44's title says "precracked Charpy specimens", yet all its curves duplicate curves of ref 43 (an instrumented Charpy V-notch study). But [NP-1661] (ref 1) does cover both Charpy V-notch and precracked Charpy data, so ref 1 remains genuinely uncertain.
**Alternatives.** Exclude all labelled records (−366 retained records); exclude ref 1 only.
**If the alternative were chosen.** Loss of up to 366 retained records including ref 1's irradiated and reconstituted SA533B-1 data; this should be a WP2 sensitivity case rather than a WP1 deletion.

## D-021 — Irradiation status that differs between releases
**Status:** PROVISIONAL (CP1)

**Decision.** Use record-A's irradiation status; flag the 200 retained records where record-B differs (`flag_irradiation_status_differs_between_releases`; refs 7, 8, 9, 13, 53).
**Evidence.** B changes 226 records from "No" to "Yes" and 12 from "Yes" to "No"; 78 of the new "Yes" records gain a fluence and the rest have none (`dataset_version_comparison.md`). Four curves B marks irradiated (refs 8, 9, 9, 13) match unirradiated curves in other publications point for point (10/10, 13/13, 15/15, 15/15) within digitization error. Neutron irradiation hardens these steels and shifts the transition curve, so an irradiated curve should not reproduce an unirradiated one point for point: those relabels are very likely wrong. The ref 53 changes could not be checked this way.
**Alternatives.** Adopt B's values; exclude all disputed records.
**If the alternative were chosen.** Adopting B would split duplicate pairs (699 instead of 752 removals) and put unirradiated data into irradiated curves; excluding disputed records would remove 200 retained records.

## D-022 — The dataset's USE, DBTT and curve-ID columns
**Status:** DECIDED
**Decision.** Keep as reference-only fields (`_dataset` suffix). They are not used as ground truth; WP3 fits its own curves. The curve ID may be used as a starting point for WP2 grouping, subject to the WP2 rules.
**Why.** The method and DBTT criterion are undocumented; DBTT cannot be a 41 J temperature for miniature specimens whose USE is below 41 J; copies of identical data carry different values (up to 32 J and 14 °C apart), which suggests per-copy fitting by the dataset authors; ten curve IDs mix geometry, irradiation, treatment, condition or orientation (D-028).
**Alternatives.** Use them as published transition temperatures for comparison in WP4.
**If the alternative were chosen.** The WP4 cross-check would compare against numbers of unknown definition.

## D-023 — Special material and specimen conditions are tagged, not excluded
**Status:** DECIDED (inclusion deferred to WP2)
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
**Status:** PROVISIONAL (CP1)
**Decision.** Keep refs 22, 23, 30, 32, 40 (SA508 Grade 1A, carbon steel for main-steam-line piping; 212 retained records) in scope as members of the SA508 specification family, identified through `ref_grade_title`.
**Why.** They meet the brief's literal family definition and are ferritic with a transition, but they are not vessel steels. Deciding scope by grade is the author's call.
**If the alternative were chosen.** −212 retained records, all full-size unirradiated curves.

## D-028 — Dataset curve IDs with internal inconsistencies
**Status:** DECIDED
**Decision.** Flag, do not correct (`flag_dataset_curve_id_mixes`). Examples: curve 271 combines 20×2.5×2.5 mm unirradiated and 23.6×3.33×3.33 mm irradiated specimens (it also causes the only energy/USE ratio above 1.25); curve 6 includes 2 irradiated and 12 reconstituted records among 107; curves 66 and 76 pool two simulated-HAZ sub-zones each.
**Why.** Correcting requires deciding what the curve should be, which is WP2's curve definition.

## D-029 — Material label that contradicts composition
**Status:** DECIDED
**Decision.** Flag, do not relabel, the 11 records of ref 53 curve 237: labelled A533B base metal but carrying the weld-metal composition (C 0.08, Ni 0.83, Mn 1.33) of the same paper, in a sequence (base, HAZ 1 mm, HAZ 4 mm, weld) that repeats for another figure.
**Why.** The evidence strongly suggests weld metal, but relabelling is an inference; WP2 can decide with the flag visible.

## D-030 — Git repository
**Status:** OPEN
The project folder is not a git repository. Version control was not initialized without the author's approval; asked at CP1.
