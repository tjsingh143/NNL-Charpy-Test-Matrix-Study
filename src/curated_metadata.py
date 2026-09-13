"""Hand-curated metadata: every human judgement the WP0/WP1 pipeline relies on.

Nothing in this file is computed from the data. It records (a) what each column
means, (b) which text variants are treated as the same value, and (c) per-reference
evidence taken from the citation titles in the workbook's References sheet.
Each block cites the DECISIONS.md entry that justifies it, so the judgement calls
can be reviewed and challenged in one place.

Source abbreviations used in the notes:
  [descriptor]  Lee et al. (2025), Sci. Data 12:543, doi:10.1038/s41597-025-04823-1
  [coldesc]     'Column Descriptions' sheet inside the workbook
  [E23-82]      ASTM E23-82, Standard Methods for Notched Bar Impact Testing of Metallic Materials
  [ISO148-1]    ISO 148-1:2016, Metallic materials - Charpy pendulum impact test - Part 1
  [E900]        ASTM E900, Standard Guide for Predicting Radiation-Induced Transition Temperature Shift
"""

# ---------------------------------------------------------------------------
# (a) Columns: raw header (verbatim, trailing spaces included) -> clean name,
#     name used in the workbook's Column Descriptions sheet, unit, meaning, notes.
#     Renaming convention: DECISIONS.md D-007.
# ---------------------------------------------------------------------------
_ELEMENT_NOTE = ("Heat (melt) chemistry repeated on every specimen record of that heat. "
                 "A blank means 'not reported', not zero.")


def _element(raw, symbol, coldesc_name, extra=""):
    return dict(raw=raw, clean=f"{symbol.lower()}_wt_pct", coldesc=coldesc_name, unit="wt.%",
                meaning=f"Mass fraction of {symbol} in the material, in weight percent, as reported by the source publication.",
                notes=(_ELEMENT_NOTE + (" " + extra if extra else "")))


COLUMNS = [
    dict(raw="Reference", clean="ref_id", coldesc="Reference", unit="",
         meaning="Integer identifier of the source publication. Joins to the References sheet (citation and link).",
         notes="The 2025.30 release (primary) lists 109 publications and the 2024.206 release 106; counts are computed in WP0."),
    dict(raw="Material ", clean="material_raw", coldesc="Material", unit="",
         meaning="Material designation as written by the dataset authors: a steel specification or grade shorthand "
                 "(e.g. SA508, A533B-1, 20MnMoNi55); 'A533B - WM' denotes weld metal.",
         notes="Header has a trailing space. Grade/class is often missing (SA508 Grade 1A, 3 and 4N are all written 'SA508'). "
               "There is no product-form column (plate/forging/weld); see D-013."),
    dict(raw="Material Group", clean="material_group", coldesc="Material Group", unit="",
         meaning="Dataset authors' two-way grouping: 'Reactor pressure vessel steel' or 'Nuclear Structural Material'.",
         notes="'Nuclear Structural Material' holds the SS316 family and, in the 2025.30 release only, the ferritic WWER-440 steel 15Cr2MoV-A "
               "(WP0 notable facts), so the group label is not a ferritic/austenitic indicator. "
               "The group label 'Reactor pressure vessel steel' also covers SA508 Grade 1A piping steel (refs 22, 23, 30, 32, 40)."),
    _element("C, wt.%", "C", "C (wt.%)"),
    _element("Si, wt.%", "Si", "Si (wt.%)"),
    _element("Mn, wt.%", "Mn", "Mn (wt.%)"),
    _element("P, wt.%", "P", "P (wt.%)", "Some ferritic-steel records report P far above typical vessel-steel levels (see WP0 notable facts); not verified against the sources."),
    _element("S, wt.%", "S", "S (wt.%)"),
    _element("Ni, wt.%", "Ni", "Ni (wt.%)"),
    _element("Cr, wt.%", "Cr", "Cr (wt.%)"),
    _element("Mo, wt.%", "Mo", "Mo (wt.%)"),
    _element("Al, wt.%", "Al", "Al (wt.%)"),
    _element("N, wt.%", "N", "N (wt.%)"),
    _element("Ti, wt.%", "Ti", "Ti (wt.%)"),
    _element("Fe, wt.%", "Fe", "Fe (wt.%)",
             "Derived, not measured, in many records: the descriptor states that when sources reported iron as "
             "'balance' the authors computed it by subtracting all other reported elements [descriptor]."),
    _element("Nb, wt.%", "Nb", "Nb (wt.%)"),
    _element("B, wt.%", "B", "B (wt.%)"),
    _element("Cu, wt.%", "Cu", "Cu (wt.%)"),
    _element("V, wt.%", "V", "V (wt.%)"),
    _element("Zr, wt.%", "Zr", "Zr (wt.%)"),
    _element("W, wt.%", "W", "W (wt.%)"),
    _element("Sn, wt.%", "Sn", "Sn (wt.%)"),
    _element("Co, wt.%", "Co", "Co (wt.%)"),
    _element("O, wt,%", "O", "O (wt.%)", "Header typo in the workbook: 'wt,%' (comma)."),
    _element("Ta, wt.%", "Ta", "Ta (wt.%)"),
    _element("As, wt%", "As", "As (wt.%)", "Header typo in the workbook: 'wt%'."),
    _element("Sb, wt.%", "Sb", "Sb (wt.%)"),
    dict(raw="Manufacturer", clean="manufacturer", coldesc="Manufacturer", unit="",
         meaning="Producer of the material, or in some rows a production route.",
         notes="Mixed meanings: companies (e.g. HANJUNG, Industeel), research programmes (EPRI, HSST) and processes "
               "('Mandrel Forging Process', additive manufacturing by laser powder directed energy deposition)."),
    dict(raw="Treatment", clean="treatment", coldesc="Treatment", unit="",
         meaning="Free-text description of processing or conditioning applied to the material: heat treatments, "
                 "intercritical heat treatment, post-weld heat treatment (PWHT), step cooling, pre-strain, "
                 "shock-wave hardening, or simulated weld heat-affected-zone (HAZ) thermal cycles.",
         notes="Codes CGCG, FGCG, ICCG, SCCG, FGFG, ICIC, SCSC (ref 15) are read as simulated two-pass HAZ sub-zones "
               "(CG coarse-grained, FG fine-grained, IC intercritical, SC subcritical). This reading is ours; the dataset does not define them."),
    dict(raw="Post Treatment Temperature (ºC)", clean="post_treatment_temp_c", coldesc="Post Treatment Temperature (C)", unit="°C",
         meaning="Temperature of a heat-treatment step associated with the Treatment entry.",
         notes="Ambiguous: the authors describe it only as 'Temperature applied after the treatment'. Whether it is a tempering, "
               "PWHT, ageing or austenitizing temperature varies by source and is not recorded. Header uses 'º' (U+00BA), not '°'."),
    dict(raw="Post Treatment Time (h)", clean="post_treatment_time_h", coldesc="Post Treatment Time (h)", unit="h",
         meaning="Duration of that heat-treatment step, in hours.",
         notes="Same ambiguity as the post-treatment temperature. The longest times belong to thermal ageing of stainless steel."),
    dict(raw="Cooling", clean="cooling_method", coldesc="Cooling", unit="",
         meaning="Cooling method used after heat treatment when the material was produced (e.g. air cooled, water quenched, furnace cooled).",
         notes="Refers to material processing, not to how specimens were brought to test temperature. In the Column Descriptions sheet "
               "this entry is listed out of order (row 49)."),
    dict(raw="Cooling Rate (ºC/min)", clean="cooling_rate_c_per_min", coldesc="Cooling Rate (K/min)", unit="°C/min",
         meaning="Rate of temperature decrease during that cooling step.",
         notes="The header says °C/min and the Column Descriptions sheet says K/min. For a rate the two are numerically identical "
               "(a change of 1 °C equals a change of 1 K), so no conversion is needed."),
    dict(raw="Miocrostructure", clean="microstructure", coldesc="Microstructure", unit="",
         meaning="Microstructure reported by the source (e.g. tempered bainite, tempered martensite).",
         notes="Header misspelled in the workbook."),
    dict(raw="Morphology", clean="morphology", coldesc="Morphology ", unit="",
         meaning="Morphology of the microstructure (e.g. equiaxed, elongated, columnar).", notes=""),
    dict(raw="Grain size (um)", clean="grain_size_um", coldesc="Grain size (um)", unit="µm",
         meaning="Grain size in micrometres.",
         notes="Which grain (prior-austenite or ferrite) and which measurement method are not recorded."),
    dict(raw="Irradiated Specimen", clean="irradiated", coldesc="Irradiated Specimen", unit="",
         meaning="Whether the material had been neutron-irradiated before the Charpy test ('Yes'/'No').",
         notes="The 2025.30 release changes this field for refs 7, 8, 9, 13 and 53 relative to 2024.206, mostly without adding fluence "
               "(counts in the dataset version comparison). Source checks resolve ref 13 only; the others remain unresolved (D-021)."),
    dict(raw="Irradiation Dose (n/cm^2)", clean="fluence_n_per_cm2", coldesc="Irradiation Dose (n/cm^2)", unit="n/cm²",
         meaning="Neutron fluence: the number of neutrons that passed through each square centimetre of material during irradiation.",
         notes="Called 'dose' in the workbook, but n/cm² is the unit of fluence. The neutron-energy threshold (ASTM E900 uses E > 1 MeV) "
               "is not stated, nor are flux, spectrum or irradiation facility (D-011). Some cells are Excel formulas such as =(3*10^19); "
               "their stored results were verified in WP0 (D-004)."),
    dict(raw="Irradiation Temperature (ºC)", clean="irradiation_temp_c", coldesc="Irradiation Temperature (C)", unit="°C",
         meaning="Temperature of the material during irradiation.", notes="Missing for part of the irradiated records (count in WP0 notable facts)."),
    dict(raw="Irradiation Time (hours)", clean="irradiation_time_h", coldesc="Irradiation Time (hours)", unit="h",
         meaning="Duration of irradiation.", notes="Very sparsely reported (see fill rate and distinct values)."),
    dict(raw="Length (mm)", clean="length_mm", coldesc="Length (mm)", unit="mm",
         meaning="Overall specimen length L (55 mm for the standard Charpy specimen).",
         notes="The Column Descriptions sheet calls this 'gauge length', a tensile-test term; for a Charpy bar it is the overall length."),
    dict(raw="Width (mm)", clean="width_mm", coldesc="Width (mm)", unit="mm",
         meaning="Width W: distance between the notched face and the opposite face, i.e. the dimension in which the notch is cut "
                 "and the crack grows. The ligament (material left below the notch) is W minus the notch depth.",
         notes="Matches ISO 148-1:2016 §3.2.1 and the descriptor's notation B(W-A)^2. ISO 148 editions before 2016 called this "
               "dimension 'height', so older source papers may use the opposite name. Data are consistent with the 2016 meaning: every "
               "2 mm notch is paired with W = 10 mm (D-008)."),
    dict(raw="Thickness (mm)", clean="thickness_mm", coldesc="Thickness (mm)", unit="mm",
         meaning="Thickness B: dimension parallel to the notch, perpendicular to W. This is the dimension reduced in standard "
                 "sub-size specimens (e.g. 55 x 10 x 5 mm).",
         notes="Matches ISO 148-1:2016 §3.2.2. ISO 148 editions before 2016 called this dimension 'width' (D-008)."),
    dict(raw="Notch Depth (mm)", clean="notch_depth_mm", coldesc="Notch Depth (mm)", unit="mm",
         meaning="Depth of the notch measured from the notched face (2 mm for the standard V-notch specimen).",
         notes="Missing for many full-size records (count in WP0 notable facts); never filled in from the standard (D-016)."),
    dict(raw="Notch Angle (deg)", clean="notch_angle_deg", coldesc="Notch Angle (deg)", unit="degrees",
         meaning="Included angle of the V-notch (45° standard; 30° for several miniature designs).", notes=""),
    dict(raw="Notch Root Radius (mm)", clean="notch_root_radius_mm", coldesc="Notch Root Radius (mm)", unit="mm",
         meaning="Radius at the bottom of the notch (0.25 mm standard; 0.08 mm for several miniature designs).", notes=""),
    dict(raw="Notch Shape", clean="notch_shape", coldesc="Notch Shape", unit="",
         meaning="Notch type. 'V' for every record that has a value.", notes="Blank records are listed in WP0 notable facts."),
    dict(raw="Test Standard", clean="test_standard", coldesc="Test standard", unit="",
         meaning="Test standard cited by the source (ASTM E23 editions, JIS, GB/T 229, EN 10045-1, ASTM A370).",
         notes="Often blank. 'EN 10045-1:1990' to ':1997' is a spreadsheet auto-fill artefact: "
               "the year increments row by row (D-024)."),
    dict(raw="Test Temperature (C) ", clean="test_temp_c", coldesc="Test Temperature (C)", unit="°C",
         meaning="Temperature of the specimen at the moment of impact.",
         notes="Header has a trailing space. Values with many decimals (e.g. -77.0871985 °C) come from digitizing published graphs "
               "with WebPlotDigitizer [descriptor], so they carry digitization error."),
    dict(raw="Orientation", clean="orientation", coldesc="Orientation", unit="",
         meaning="Orientation of the specimen relative to the rolling or forging direction of the product (two-letter codes such as "
                 "L-T, T-L: first letter = direction normal to the crack plane, second = expected crack growth direction).",
         notes="Mixed conventions: single letters (L, T) are ambiguous; weld and additive-manufacturing codes (V, H, BD, WD, RW, WR, P, D) "
               "also appear; ref 31 records say 'Direction means different here'. No merging was done."),
    dict(raw="Test Condition Statement ", clean="test_condition_statement", coldesc="Test Condition Statement ", unit="",
         meaning="Free-text notes about the specimen or test: HAZ location, striking velocity, reconstituted specimen, "
                 "standard reference material, hydrogen charging, welded area.",
         notes="Header has a trailing space. Contains information that changes what a record is (e.g. striking velocity 0.001 m/s, "
               "reconstituted specimens), so it is parsed into tags in WP1."),
    dict(raw="Impact energy (J)", clean="energy_j", coldesc="Impact energy (J)", unit="J",
         meaning="Absorbed energy of one specimen: the energy the pendulum lost in breaking it, in joules.",
         notes="Mostly digitized from graphs [descriptor]. Units were converted to joules by the dataset authors; see the WP1 unit checks."),
    dict(raw="USE (J)", clean="use_j_dataset", coldesc="USE (J)", unit="J",
         meaning="Upper-shelf energy assigned by the dataset to the curve the record belongs to (same value on every record of that curve).",
         notes="Described only as an 'estimated value' [descriptor]; the estimation method is not documented. Slightly different values "
               "on duplicated copies of the same data suggest the dataset authors fitted it themselves. Kept for reference only (D-022)."),
    dict(raw="DBTT (ºC)", clean="dbtt_c_dataset", coldesc="DBTT (C)", unit="°C",
         meaning="Ductile-to-brittle transition temperature assigned by the dataset to the record's curve.",
         notes="The defining criterion (41 J, 50% of upper shelf, tanh mid-point, ...) is not documented. It cannot be a 41 J "
               "temperature for miniature specimens whose upper shelf is below 41 J. Kept for reference only (D-022)."),
    dict(raw="DBTT Fitted Curve", clean="curve_id_dataset", coldesc="DBTT Fitted Curve", unit="",
         meaning="Dataset-wide identifier of the group of records the dataset authors treated as one fitted transition curve.",
         notes="Undocumented beyond 'Number of the fitted curve'. Each ID is one contiguous block within one reference and material, "
               "but some IDs mix geometries, irradiation states or treatments (flagged in WP1, D-028)."),
    # Present only in the 2025.30 release (q4x6v-dyt25):
    dict(raw="Specimen Type", clean="specimen_type_dataset", coldesc=None, unit="",
         meaning="2025.30 release only: 'Pre-Cracked' for every record of refs 1, 8, 9, 13, 19, 20, 23; otherwise blank.",
         notes="Not described in the Column Descriptions sheet. A paper-level note: source checks show these energy curves are ordinary "
               "Charpy V-notch tests and the precracked specimens belonged to separate fracture-toughness tests (D-020)."),
]

COLUMN_BY_RAW = {c["raw"]: c for c in COLUMNS}

# Clean names of fields that are original measurements or metadata (used for exact-duplicate detection).
ORIGINAL_FIELDS = [c["clean"] for c in COLUMNS if c["raw"] != "Specimen Type"]

# ---------------------------------------------------------------------------
# (b1) Material names (DECISIONS.md D-012). Keys are the raw strings after
#      removing leading/trailing whitespace ('A533B ' -> 'A533B').
#   family       : level at which records are treated as the same material type
#   class_stated : A533 class as written in the label (None = not stated)
#   prefix       : 'SA' = ASME designation, 'A' = ASTM designation (same specification)
#   scope        : 'in' (brief section 4 family), 'out' (SS316), or 'pending'
# ---------------------------------------------------------------------------
MATERIAL_MAP = {
    "A533B":      dict(material_std="A533 Type B, class not stated", family="A533B", class_stated=None, prefix="A", weld_metal_label=False, scope="in"),
    "SA533B":     dict(material_std="A533 Type B, class not stated", family="A533B", class_stated=None, prefix="SA", weld_metal_label=False, scope="in"),
    "A533B-1":    dict(material_std="A533 Type B Class 1", family="A533B", class_stated="1", prefix="A", weld_metal_label=False, scope="in"),
    "SA533B-1":   dict(material_std="A533 Type B Class 1", family="A533B", class_stated="1", prefix="SA", weld_metal_label=False, scope="in"),
    "A533B - WM": dict(material_std="Weld metal from an A533B weldment", family="A533B weld metal", class_stated=None, prefix="A", weld_metal_label=True, scope="in"),
    "A508":       dict(material_std="A508, grade/class not stated", family="A508", class_stated=None, prefix="A", weld_metal_label=False, scope="in"),
    "SA508":      dict(material_std="A508, grade/class not stated", family="A508", class_stated=None, prefix="SA", weld_metal_label=False, scope="in"),
    "A302B":      dict(material_std="A302 Grade B", family="A302B", class_stated=None, prefix="A", weld_metal_label=False, scope="in"),
    "20MnMoNi55": dict(material_std="20MnMoNi55 (DIN 1.6310)", family="20MnMoNi55", class_stated=None, prefix="", weld_metal_label=False, scope="in"),
    # 2025.30 release only. Ferritic WWER-440 vessel steel outside the brief's named family: out of scope (CP1 decision 4, D-012).
    "15Cr2MoV-A": dict(material_std="15Cr2MoV-A (WWER-440 vessel steel)", family="15Cr2MoV-A", class_stated=None, prefix="", weld_metal_label=False, scope="out_ferritic"),
    # Austenitic stainless steels: out of scope (brief section 4, D-014). Variants kept distinct in material_std.
    "SS316":      dict(material_std="SS316", family="SS316 (austenitic stainless)", class_stated=None, prefix="", weld_metal_label=False, scope="out"),
    "SS316L":     dict(material_std="SS316L", family="SS316 (austenitic stainless)", class_stated=None, prefix="", weld_metal_label=False, scope="out"),
    "SS316LN":    dict(material_std="SS316LN", family="SS316 (austenitic stainless)", class_stated=None, prefix="", weld_metal_label=False, scope="out"),
    "SS316H":     dict(material_std="SS316H", family="SS316 (austenitic stainless)", class_stated=None, prefix="", weld_metal_label=False, scope="out"),
}

# Nominal product form implied by the specification's scope (D-013):
#   ASTM A533 and A302 are plate specifications; ASTM A508 is a forging specification.
#   20MnMoNi55 is a grade used for both plates and forgings, so the name implies nothing.
SPEC_PRODUCT_FORM = {"A533B": "plate", "A302B": "plate", "A508": "forging"}

# ---------------------------------------------------------------------------
# (b2) Text value harmonization (D-024). Keys are values after whitespace
#      stripping. Only case, spelling, spacing and one auto-fill artefact are
#      changed; values with different meanings are never merged.
# ---------------------------------------------------------------------------
TEXT_VALUE_MAPS = {
    "test_standard": {
        **{f"EN 10045-1:{y}": "EN 10045-1" for y in range(1990, 1998)},  # auto-fill artefact: year incremented per row
        "ASTM-E23": "ASTM E23", "E23": "ASTM E23", "ASTM E 23-82": "ASTM E23-82", "ASTM E 23-72": "ASTM E23-72",
        "ASTM E23 - 12c": "ASTM E23-12c", "GB/T229-2007": "GB/T 229-2007", "GB/T229-2020": "GB/T 229-2020",
    },
    "test_condition_statement": {"Reconstituted": "Reconstituted specimen"},
    "treatment": {
        "Step cooling": "Step Cooling", "hot isostatic press": "Hot Isostatic Press",
        "Conventioanal hot pierced ingots + Silicon-killing": "Conventional hot pierced ingots + Silicon-killing",
        "Conventioanal hot pierced ingots + Vacuum carbon deoxidation": "Conventional hot pierced ingots + Vacuum carbon deoxidation",
        "Conventioanal hot pierced ingots + Modified Vacuum carbon deoxidation": "Conventional hot pierced ingots + Modified Vacuum carbon deoxidation",
        "Different Quenceing Rate": "Different Quenching Rate", "Solution Annneal + HIP": "Solution Anneal + HIP",
    },
    "cooling_method": {"water quenched": "Water Quenched", "Contineous Cooling": "Continuous Cooling"},
    "microstructure": {"Baintic Structure": "Bainitic Structure", "Baintie/Martensite": "Bainite/Martensite",
                       "Ferrite/Perarlite/Tempered Bainite": "Ferrite/Pearlite/Tempered Bainite", "Tempered bainite": "Tempered Bainite"},
    "morphology": {"columnar": "Columnar", "Dentritic": "Dendritic", "Dentritic Ferrite": "Dendritic Ferrite"},
    "manufacturer": {"Addative Manufacturing (LPDED)": "Additive Manufacturing (LPDED)",
                     "Vaccum Induction Melting": "Vacuum Induction Melting",
                     "Vaccum-Induction Melting Furnace": "Vacuum Induction Melting Furnace",
                     "Silicon-Killing / Vaccum carbon deoxidation": "Silicon-Killing / Vacuum carbon deoxidation"},
}

SIMULATED_HAZ_CODES = ["CGCG", "FGCG", "ICCG", "SCCG", "FGFG", "ICIC", "SCSC"]

# ---------------------------------------------------------------------------
# (c) Reference-level evidence from citation titles (D-013, D-020).
#   grade_title        : grade/class wording in the title (reference level, not per record)
#   product_form_note  : title says weld/HAZ/joint content that records do not identify
#   specimen_note      : title or source abstract suggests non-standard specimens
#   material_note      : lab melts, model alloys, additive manufacturing, piping steel
#   forming_evidence   : explicit product form stated in the title (used for 20MnMoNi55 and additive manufacturing)
#   weld_haz_unidentified : True when the title reports weld or HAZ material that the records do not identify
#   precracked_concern : True when the source itself reports precracked specimens (title or abstract)
# Only in-scope references with something to record are listed.
# ---------------------------------------------------------------------------
REFERENCE_NOTES = {
    1: dict(precracked_concern=True, specimen_note="EPRI NP-1661 covers both Charpy V-notch and precracked Charpy data, reconstituted "
                          "specimens and a shock-hardened surrogate material. The 2025.30 release labels all of its records 'Pre-Cracked'.",
            material_note="NP-1661 reports several SA533B-1 heats (heat D; shock-hardened heat IbH; HSST Plate 02 = IbA), but every record "
                          "carries the same composition, so composition cannot distinguish them."),
    2: dict(specimen_note="Some records say 'Standard Reference Material'; whether this is a surveillance correlation-monitor plate or a "
                          "machine-verification specimen is not stated."),
    3: dict(material_note="Title: 'Four Lab-Melt Plates' (laboratory heats)."),
    4: dict(grade_title="SA 508 class 3"),
    5: dict(grade_title="SA508 Class 2a", weld_haz_unidentified=True,
            product_form_note="Title: 'Base and Heat-Affected-Zone Material'. Records do not identify which curves are HAZ."),
    6: dict(grade_title="SA 508 Mn-Mo-Ni"),
    7: dict(weld_haz_unidentified=True, product_form_note="Title: 'base metals and simulated heat-affected zones'. Records do not identify simulated-HAZ curves."),
    8: dict(grade_title="SA508 Gr.3 and Gr.4N"),
    9: dict(grade_title="Ni-Mo-Cr low alloy (Gr.4N type)"),
    10: dict(grade_title="SA508 Gr.4N", material_note="Title: 'model alloys' (laboratory heats)."),
    11: dict(grade_title="SA508 Gr.4N"),
    12: dict(grade_title="SA508 Cl.3"),
    13: dict(grade_title="SA508 Gr.4N"),
    14: dict(grade_title="SA508 Gr.4N"),
    15: dict(product_form_note="Title: 'post weld heat treatment in the HAZ of SA508'. Simulated-HAZ sub-zones identified in Treatment; "
                               "'Bulk Metal' records are base metal although the condition statement says 'Testing the HAZ'."),
    16: dict(grade_title="SA508 Gr.4N", material_note="Title: 'model alloy' (laboratory heat)."),
    17: dict(grade_title="SA508 Gr.4N"),
    18: dict(weld_haz_unidentified=True, product_form_note="Title: 'laser welded joint'. Only some records say 'Welded Area'; the rest are not identified."),
    19: dict(grade_title="SA508 Gr.4N"),
    20: dict(grade_title="SA508 Gr.4N",
             specimen_note="Abstract: Charpy tests to ASTM E23 and fracture toughness to ASTM E1921, i.e. the precracked specimens "
                           "were for the separate fracture-toughness tests. The 2025.30 release labels records 'Pre-Cracked'."),
    21: dict(specimen_note="Title: 'Preparation of reconstituted Charpy V-notch impact specimens'."),
    22: dict(grade_title="SA508 Gr.1A", material_note="SA508 Grade 1A is a carbon steel used for piping, not a vessel steel."),
    23: dict(grade_title="SA508 Gr.1A", material_note="Title: 'for main steam line piping' (piping steel, not a vessel steel)."),
    24: dict(grade_title="SA508 CL 3 and CL 3a"),
    25: dict(grade_title="SA508 Grade 3 Class 1", weld_haz_unidentified=True,
             product_form_note="Title: properties 'in its welded joint'. Records do not identify weld zones."),
    26: dict(grade_title="SA508 Gr4N"),
    27: dict(grade_title="SA508 Gr. 4N"),
    28: dict(grade_title="SA508 Gr. 4N"),
    29: dict(grade_title="SA508 Gr.4N"),
    30: dict(grade_title="SA508 Gr.1A", material_note="SA508 Grade 1A is a carbon steel used for piping, not a vessel steel."),
    31: dict(grade_title="SA508 Gr.3", forming_evidence="additively manufactured",
             material_note="Title: 'laser powder-directed energy deposition' (additively manufactured, not a forging)."),
    32: dict(grade_title="SA508 Gr.1A", material_note="Title: 'for pipeline in nuclear power plants' (piping steel)."),
    33: dict(grade_title="SA508 Gr. 4N"),
    34: dict(grade_title="SA508/SA533-B-1 weld and HAZ", weld_haz_unidentified=True,
             product_form_note="Title: 'SA508/SA533-B-1 weld and HAZ'. Records are labelled 'SA508' with no weld/HAZ identification, "
                               "so the nominal 'forging' form is probably wrong."),
    35: dict(grade_title="A508-3"),
    37: dict(grade_title="SA508 Gr.3 and SA508 Gr.4N"),
    38: dict(grade_title="SA508 Gr.4N"),
    39: dict(grade_title="SA508Gr.3"),
    40: dict(grade_title="SA508 Gr.1A", material_note="Title: 'for main steam line piping' (piping steel, not a vessel steel)."),
    41: dict(material_note="Title: 'room-temperature pre-deformation' (pre-strained material)."),
    43: dict(material_note="'A533B' records are the JSPS steel, an A533B-type plate deliberately embrittled by raised S and P (SCK-CEN BLG-1016)."),
    44: dict(precracked_concern=True, specimen_note="Title: 'using precracked Charpy specimens'. Records are not identified as precracked; see SPECIMEN_TYPE_CHECKS.",
             material_note="'A533B' records are the JSPS steel, an A533B-type plate deliberately embrittled by raised S and P (SCK-CEN BLG-1016)."),
    47: dict(forming_evidence="forging", material_note="Title: '20MnMoNi55 forging'."),
    50: dict(weld_haz_unidentified=True, product_form_note="Title: '12-in. thick A533-B steel plates and weld metal'. Records do not identify weld metal."),
    51: dict(specimen_note="Loading-rate study: 0.5 and 0.001 m/s tests identified in the condition statement."),
    53: dict(product_form_note="Title: 'weld joint of reactor pressure vessel steels'. Base metal, HAZ and weld metal identified in records; "
                               "curve 237 is labelled base metal but has the weld-metal composition (D-029)."),
    54: dict(material_note="Title: 'A533B plate and A508 forging steels'."),
    57: dict(grade_title="A533 Grade B Class 1"),
    58: dict(specimen_note="Title covers specimen size and notch geometry effects, but only one full-size curve (notch not reported) is in the data."),
    60: dict(weld_haz_unidentified=True, product_form_note="Title: 'HAZ of RPVS clad with duplex stainless steel'. Records do not identify HAZ."),
    # 2025.30 release (q4x6v-dyt25) only:
    107: dict(material_note="Title: 'un-irradiated low alloy RPV ferritic steel'; sub-size correlation study."),
    108: dict(material_note="Title: 'long-term thermal aged WWER 440 RPV steel'."),
    109: dict(material_note="Title: 'PWR RPV model steels' (laboratory heats)."),
}


# ---------------------------------------------------------------------------
# (d) Source checks made for CP1 decisions 1 and 2 (DECISIONS.md D-020, D-021, D-031).
#     Only references whose specimen type or condition labels were questioned are listed.
#     Short citations are expanded in DECISIONS.md: [NP-1661] full report (OSTI 6609271); [BLG-1016] Lucon (2005),
#     SCK-CEN open report; [Lee2014] full text; [Lee2011] and [Kim2012] abstracts.
# ---------------------------------------------------------------------------
# Specimen type of the absorbed-energy records ('ordinary CVN' = standard Charpy V-notch impact test).
# resolution: 'ordinary CVN' | 'pre-cracked' | 'unresolved'
SPECIMEN_TYPE_CHECKS = {
    1: dict(resolution="ordinary CVN",
            basis="[NP-1661]: every absorbed-energy (J) versus temperature figure for SA533B-1 is a Charpy V-notch figure (Figs 2-5, 3-14, "
                  "3-15, 3-17); precracked Charpy results appear only as fracture toughness or normalized energy."),
    8: dict(resolution="ordinary CVN",
            basis="Records cite ASTM E23 (Charpy impact standard); curve 33 is point-for-point identical to a curve of ref 29. Full text not read."),
    9: dict(resolution="ordinary CVN",
            basis="Records cite ASTM E23; curves 34 and 36 are point-for-point identical to curves of refs 37 and 15 (2025.30 curation note "
                  "for ref 15: 'No Pre-cracked Specimen'). Full text not read."),
    13: dict(resolution="ordinary CVN",
             basis="[Lee2014] section 2: Charpy impact tests on standard V-notch specimens (10x10x55 mm) to ASTM E23-07a; precracked "
                   "specimens were tested in quasi-static 3-point bending for the master-curve T0 (ASTM E1921-09c), not for absorbed energy."),
    19: dict(resolution="ordinary CVN",
             basis="Curves point-for-point identical to curves of refs 17, 27, 28 (2025.30 curation note for ref 17: 'No Pre-cracked "
                   "Specimen'); companion journal paper (ref 20) tested Charpy to ASTM E23 and fracture toughness to ASTM E1921 [Lee2011]."),
    20: dict(resolution="ordinary CVN",
             basis="[Lee2011] abstract: Charpy impact tests to ASTM E23, fracture toughness to ASTM E1921; curves identical to refs 17, 27, 28."),
    23: dict(resolution="ordinary CVN",
             basis="Records cite ASTM E23. Not checked against the source: SA508 Gr.1A piping steel is outside the primary population (CP1 decision 3)."),
    43: dict(resolution="ordinary CVN",
             basis="[BLG-1016] Tables 1-4: compositions identical to SCK-CEN's 20MnMoNi55 and JSPS steels, whose Charpy V-notch "
                   "properties (USE 181 J, T41J -76 C; USE 72 J, T41J 34 C) are consistent with these curves."),
    44: dict(resolution="ordinary CVN",
             basis="Same materials and same points as ref 43 (see ref 43); the precracked specimens of the title were used for the "
                   "paper's ductile crack-resistance tests."),
}

# Irradiation status where the two releases disagree (D-021). resolution: 'irradiated' | 'not irradiated' | 'unresolved'
IRRADIATION_LABEL_CHECKS = {
    7: dict(resolution="unresolved",
            basis="2024.206: not irradiated; 2025.30: irradiated, no fluence. 2025.30 curation note: 'checking references to add "
                  "irradiation conditions'. Full text not accessible."),
    8: dict(resolution="unresolved",
            basis="2024.206: not irradiated; 2025.30: irradiated, no fluence (curation note: 'checking references to add irradiation "
                  "conditions'). Curve 33 is point-for-point identical to an unirradiated curve of ref 29. Full text not accessible."),
    9: dict(resolution="unresolved",
            basis="2024.206: not irradiated; 2025.30: irradiated at 6e19 n/cm2. Curves 34 and 36 are point-for-point identical to "
                  "unirradiated curves of refs 37 and 15. Full text not accessible."),
    13: dict(resolution="not irradiated",
             basis="[Lee2014] full text: tempering and PWHT study of an unirradiated model alloy; 'irradiation' appears only in the title "
                   "of a cited reference. The 2024.206 label is supported; the 2025.30 label is not."),
    53: dict(resolution="unresolved",
             basis="The releases move the irradiated label between full-size HAZ curves (223, 224) and 1.5-mm base/weld curves (242, 245). "
                   "[Kim2012] abstract reports irradiated base-metal specimens (8e19 n/cm2 at 563 K), consistent with 2024.206 but not "
                   "2025.30; which specimens were irradiated is not in the abstract and the full text was not accessible."),
}

# Condition labels on specific dataset series that the source contradicts (D-031). Key: (ref_id, dataset curve ID).
#   records: 'all' records of the series, or only the records the dataset labels 'irradiated'. The label is flagged, never corrected.
_NP1661_SHOCK = ("Treatment label contradicted by [NP-1661] Table 3-1: tanh fits give USE about 136, 108 and 41 J and T0 about 13, 21 "
                 "and 7 C for the non-shocked, bottom-layer and top-layer materials; dataset curves 3, 4 and 5 (labelled bottom-surface "
                 "shock hardened, top-surface shock hardened, and untreated) carry dataset USE 132, 102, 40 J and DBTT 16, 20, 8 C, "
                 "i.e. the labels are shifted by one series.")
_NP1661_FLUENCE = ("Fluence contradicted by [NP-1661] Fig. 3-17: the irradiated HSST Plate 02 specimens received 2.5e18 n/cm2 (E > 1 MeV); "
                   "the dataset gives 3e19 n/cm2.")
SOURCE_CONTRADICTED_LABELS = {
    (1, 3): dict(records="all", reason=_NP1661_SHOCK),
    (1, 4): dict(records="all", reason=_NP1661_SHOCK),
    (1, 5): dict(records="all", reason=_NP1661_SHOCK),
    # Added when CP2 was finalized (author decision, 2026-09-13).
    (1, 6): dict(records="irradiated", reason=_NP1661_FLUENCE + " These two reconstituted records carry the series-7 label (irradiated, "
                 "3e19 n/cm2) inside unirradiated HSST Plate 02 series 6. Their energies do not fit an irradiated curve (series 7 has only "
                 "11 J at -7 C): 6.9 J at -74.8 C lies within the unirradiated data (7.4 J at -70.5 C) and 41.3 J at -59.8 C is above even "
                 "the unirradiated original specimens at -60 C (8.9-22.3 J), so the irradiation label itself is also doubtful."),
    (1, 7): dict(records="all", reason=_NP1661_FLUENCE),
}

# ---------------------------------------------------------------------------
# (e) Constant-axis-offset duplicates (DECISIONS.md D-019; CP2 approval of the author, 2026-09-13).
#     The offset test is not a generic search: it links copies only within the dataset series listed here, i.e. where the repository
#     documents evidence that two publications report the same underlying tests. Key: ((ref_id, dataset curve ID) of the earlier
#     publication, (ref_id, dataset curve ID) of the later one). Adding an entry is a judgement call to log in DECISIONS.md, and must
#     never be made because of downstream fit results.
# ---------------------------------------------------------------------------
OFFSET_DUPLICATE_PROVENANCE = {
    ((1, 6), (21, 99)): dict(
        evidence="Same research programme and author: W. L. Server co-authored both reports (ref 1: Server, Wullaert, Odette & Oldfield "
                 "1981, EPRI NP-1661; ref 21: Perrin, Fromm, Server & McConnell 1982), one year apart. Same material and specimen "
                 "population: ref 1 series 6 is unirradiated HSST Plate 02 (SA533B-1), original plus reconstituted Charpy V-notch "
                 "specimens [NP-1661] (D-031, D-032); ref 21 series 99 is unirradiated SA533B, original plus reconstituted specimens, "
                 "from a report on preparing reconstituted Charpy V-notch specimens (title). Same structure (95 + 10 versus 104 + 12 "
                 "specimens) and geometry (55x10x10 mm, 2 mm notch); no treatment recorded for either.",
        not_verified="Ref 21's full text was not checked; that its SA533B series is HSST Plate 02 is inferred from the evidence above and "
                     "from the point pattern (outputs/wp1/duplicate_offset_evidence.csv), not read from ref 21."),
}

