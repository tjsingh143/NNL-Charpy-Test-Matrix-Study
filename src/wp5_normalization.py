"""WP5 - Classical specimen-size normalization: geometry, the literature equations, and their self-checks.

PRE-REGISTERED. This module was written and committed BEFORE any normalization residual existed (DECISIONS.md D-072 to
D-078, D-085 step 2). Pure functions, no file I/O, so the same code serves the checks and the analysis.

Nomenclature, identical to this project's D-008 and to every source used here:
    W   specimen width (mm)     - the dimension the notch is cut into and the crack grows through
    B   specimen thickness (mm) - the dimension parallel to the notch root
    a   notch depth (mm)
    b   = W - a, the remaining ligament below the notch (mm)
    B*b     fracture area (mm^2)             - Corwin's first factor; Sokolov's brittle normalization factor
    B*b^2   nominal fracture volume (mm^3)   - Lucas's ligament-volume measure; written B(W-A)^2 by the dataset descriptor
Sources agreeing on this nomenclature: NUREG/CR-6379 Fig. 12 and Table 2; Lucon, McCowan & Santoyo (NIST/JPVT) footnote 3
("we will call 'thickness' (B) the dimension parallel to the machined notch ... In current Charpy standards, this dimension
is referred to as specimen width"); the 2026 Scientific Reports ML paper ("b = W - A is the ligament size, W is the specimen
width, and A is the notch depth"); the Scientific Data descriptor Table 2 (B(W-A)^2).

What this module does NOT do, and why (D-076):
  * Sokolov & Alexander's own proposed procedure, Eq. (11), weights a brittle and a ductile normalization factor by the
    measured percent shear fracture of each specimen. The dataset has no shear-fracture-appearance column at all (WP0 data
    dictionary: 56 columns, none is shear or lateral expansion). Shear is not partly missing here, it is absent. It is not
    imputed, not derived from test temperature and not assumed to be 0 % or 100 %, so Eq. (11) cannot be run at all.
  * Louden's and Kayano's factors need an elastic stress-concentration factor K_t (and Kayano's plastic Q) whose published
    values exist only for particular geometries; Kumar's method needs precracked-specimen energies, which this dataset has
    none of; Uehira's and Wallin's USE power laws need exponents calibrated against the very full-size USE values a size
    correction would be evaluated against.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# 1. The full-size reference specimen (ASTM E23 / ISO 148-1 standard Charpy V-notch)
# ---------------------------------------------------------------------------
FULL_SIZE = dict(length_mm=55.0, width_mm=10.0, thickness_mm=10.0, notch_depth_mm=2.0,
                 notch_angle_deg=45.0, notch_root_radius_mm=0.25)
FULL_SIZE_B = FULL_SIZE["thickness_mm"]                       # 10 mm
FULL_SIZE_LIGAMENT = FULL_SIZE["width_mm"] - FULL_SIZE["notch_depth_mm"]   # 8 mm
FULL_SIZE_FRACTURE_AREA_MM2 = FULL_SIZE_B * FULL_SIZE_LIGAMENT             # 80 mm^2
FULL_SIZE_LIGAMENT_VOLUME_MM3 = FULL_SIZE_B * FULL_SIZE_LIGAMENT ** 2      # 640 mm^3

# ---------------------------------------------------------------------------
# 2. Which recorded dimension is the notched one (D-072)
# ---------------------------------------------------------------------------
# The dataset records the KLST-type specimens of refs 107 and 109 as length 27 mm, width 3 mm, thickness 4 mm, notch depth
# 1.0 mm, 60 deg, root radius 0.1 mm. Read with D-008's convention (width = the notched dimension) that gives a 2 mm ligament
# and a/W = 0.33, which is not any KLST specimen. The KLST of ISO 14556 / DIN 50115, adopted by ASTM E2248, puts the 1 mm
# notch in the 4 mm face: W = 4 mm, B = 3 mm, ligament 3 mm, a/W = 0.25. Three independent authorities state it:
#   - Lucon, McCowan & Santoyo (NIST): "KLST ... has thickness B = 3 mm, width W = 4 mm, notch depth N = 1 mm and length L = 27 mm";
#   - NUREG/CR-6379 type 4 (26 x 4 x 3 mm, a = 1.0 mm, 60 deg, span 22 mm): "a/W = 0.25", "the specimen thickness is only 3 mm";
#   - ref 107's own text describes 27 x 3 x 4 mm KLST specimens, 60 deg, 1 mm deep, R = 0.1 mm, anvil span 22 mm - the same
#     span as NUREG's type 4.
# PRIMARY reading: for these records the notched dimension is 4 mm and the thickness 3 mm. No raw value is altered; this is a
# decision about which recorded dimension is which. The as-recorded reading is a pre-declared sensitivity (D-075 S6).
SWAPPED_WIDTH_THICKNESS = {
    # (length_mm, width_mm, thickness_mm, notch_depth_mm): why
    (27.0, 3.0, 4.0, 1.0): "KLST (ISO 14556 / DIN 50115, ASTM E2248): the 1 mm notch is in the 4 mm face, so W = 4 mm, "
                           "B = 3 mm, ligament 3 mm, a/W = 0.25 (D-072)",
}


def geometry(length_mm, width_mm, thickness_mm, notch_depth_mm, apply_klst_correction: bool = True) -> dict:
    """W, B, ligament, fracture area and ligament volume of one specimen geometry, in mm, mm^2 and mm^3."""
    key = (float(length_mm), float(width_mm), float(thickness_mm), float(notch_depth_mm))
    w, b_thick, note = float(width_mm), float(thickness_mm), ""
    if apply_klst_correction and key in SWAPPED_WIDTH_THICKNESS:
        w, b_thick = b_thick, w
        note = SWAPPED_WIDTH_THICKNESS[key]
    a = float(notch_depth_mm)
    if not np.isfinite(a):
        raise ValueError("notch depth is not reported: the ligament b = W - a cannot be computed (nothing is assumed, D-009)")
    ligament = w - a
    if ligament <= 0:
        raise ValueError(f"non-physical geometry: ligament W - a = {ligament} mm")
    return dict(W_mm=w, B_mm=b_thick, notch_depth_mm=a, ligament_mm=ligament,
                fracture_area_mm2=b_thick * ligament, ligament_volume_mm3=b_thick * ligament ** 2,
                notch_depth_over_width=a / w, geometry_note=note)


# ---------------------------------------------------------------------------
# 3. Energy normalization factors:  E_full-size-equivalent = NF_E * E_measured   (D-073 primary, D-075 sensitivities)
# ---------------------------------------------------------------------------
def nf_energy_ligament_volume(g: dict) -> float:
    """PRIMARY (D-073). Lucas et al.: absorbed energy on the upper shelf scales with the nominal fracture (ligament) volume
    B*b^2, so NF_E = (B b^2)_full-size / (B b^2)_smaller.

    Source: Lucas, Odette, Sheckherd, McConnell & Perrin (1986) ASTM STP 888:304-324 and Lucas, Odette, Sheckherd &
    Krishnadev (1986) Fusion Technology 10:728-733, as stated in NUREG/CR-6379 p.14 ("Lucas et al. also used an NF equal to
    the ratio of the FV of full-size to subsize specimens, but expressed the nominal FV as Bb^2"), in Lucon/NIST Eq. 10 (NF3),
    in the dataset descriptor's Table 2 (B(W-A)^2) and in the 2026 ML paper's Table 1.
    Dimensions: mm^3 / mm^3, dimensionless. Identity: NF_E = 1 for the full-size specimen."""
    return FULL_SIZE_LIGAMENT_VOLUME_MM3 / g["ligament_volume_mm3"]


def nf_energy_fracture_volume_three_halves(g: dict) -> float:
    """SENSITIVITY S1 (D-075). Corwin et al.: nominal fracture volume expressed as (B b)^{3/2}.
    Source: Corwin, Klueh & Vitek (1984) J. Nucl. Mater. 122-123:343-348; Corwin & Hougland (1986) ASTM STP 888:325-338;
    stated in NUREG/CR-6379 p.14 ("use of the NF (Bb)^{3/2} gave good correspondence") and Lucon/NIST Eq. 10 (NF2).
    The descriptor reports this form as an adequate match for ductile materials with USE above 150 J."""
    return (FULL_SIZE_FRACTURE_AREA_MM2 ** 1.5) / (g["fracture_area_mm2"] ** 1.5)


def nf_energy_fracture_area(g: dict) -> float:
    """SENSITIVITY S2 (D-075). Fracture-area scaling B*b: Corwin's first factor, and exactly Sokolov & Alexander's
    NF_brittle (their Eqs 9-10), the factor their procedure applies to the LOWER shelf, where fracture is by low-energy
    cleavage and absorbed energy per unit fracture surface is taken to be constant.
    NUREG/CR-6379 p.14 records that on the UPPER shelf "normalization by Bb gave poor agreement for USE data"; it is carried
    here because the primary method must apply one factor to a whole curve that spans both regimes."""
    return FULL_SIZE_FRACTURE_AREA_MM2 / g["fracture_area_mm2"]


# ---------------------------------------------------------------------------
# 4. Temperature corrections:  T_full-size-equivalent = T_measured + M   (D-074 primary, D-075 sensitivities)
# ---------------------------------------------------------------------------
def shift_sokolov(g: dict) -> float:
    """PRIMARY (D-074). Sokolov & Alexander, NUREG/CR-6379 (ORNL-6888, 1997) Eq. (22) and Fig. 27:

        M = 98 - 15.1 * ln(B b^2)        M in deg C, B b^2 the nominal fracture volume in mm^3

    applied as DBTT_full-size = DBTT_subsize + M (their Eq. 17). Its form follows their Eq. (16),
    DBTT = 1 / (R - S ln V), from Davidenkov's picture of a temperature-dependent yield stress meeting a
    volume-dependent Weibull cleavage strength; "the equation was forced to give a correction factor of 0 for the
    full-size specimen". The report offers it beyond its own four specimen types: "the form of the dependence may be
    used as guidance to estimate size corrections for subsize specimens", while stating plainly that "deviations from
    this dependence reflect the constraint effects of different notch dimensions"."""
    return 98.0 - 15.1 * np.log(g["ligament_volume_mm3"])


def shift_lucon(g: dict) -> float:
    """SENSITIVITY S3 (D-075). Lucon, Chaouadi, Fabry, Puzzolante & van Walle (2000), ASTM STP 1380:146-163:
        M = 92.7 - 14.34 * ln(B b^2)
    The same functional form as Sokolov's, refitted on RPV steels over several sub-size geometries including KLST.
    Read here from the dataset descriptor's Table 3 and the 2026 ML paper's Table 2, which both tabulate it; the ASTM STP
    volume itself is paywalled and was not read."""
    return 92.7 - 14.34 * np.log(g["ligament_volume_mm3"])


def shift_towers(g: dict) -> float:
    """SENSITIVITY S4 (D-075). Towers (1983, TWI Research Report 219/1983; 1986, Metal Construction):
        M = 0.7 (10 - B)^2        B = specimen thickness in mm
    A thickness-only correlation, developed for sub-size specimens of reduced thickness (SCVN). Its transition temperature
    is defined at an energy density of 0.25 J/mm^2 (20 J for a full-size specimen), not at 41 J. Quoted with these exact
    coefficients by Lucon/NIST Eq. (2), the descriptor's Table 3 and the 2026 ML paper's Table 2."""
    return 0.7 * (FULL_SIZE_B - g["B_mm"]) ** 2


def shift_wallin(g: dict) -> float:
    """SENSITIVITY S5 (D-075). Wallin (1994, Jernkontorets Forskning, Working Group 4013/89):
        M = -51.4 * ln[ 2 (B / 10)^0.25 - 1 ]        B = specimen thickness in mm
    Also thickness-only; fitted over transition temperatures at energy densities of 0.25-0.5 J/mm^2 (20-40 J full-size).
    Quoted with these coefficients by Lucon/NIST Eq. (3) and the 2026 ML paper's Table 2. Undefined once
    2 (B/10)^0.25 <= 1, i.e. below B = 10/16 = 0.625 mm; NaN is returned there rather than a number."""
    inner = 2.0 * (g["B_mm"] / FULL_SIZE_B) ** 0.25 - 1.0
    return float(-51.4 * np.log(inner)) if inner > 0 else float("nan")


# Sokolov & Alexander's per-specimen-type shifts, Eqs (18)-(21), with their +/- 2 sigma intervals. They apply ONLY to the four
# specimen types built in that report, so they are matched on the actual cross-section, notch angle and notch root radius, and
# never extrapolated to a geometry the report did not build (D-075 S7, D-076).
SOKOLOV_TYPES = {
    "type 1": dict(W_mm=5.0, B_mm=5.0, notch_depth_mm=0.762, notch_angle_deg=30.0, notch_root_radius_mm=0.08,
                   shift_c=30.0, two_sigma_c=28.0, length_mm=25.4, span_mm=20.0),
    "type 2": dict(W_mm=3.33, B_mm=3.33, notch_depth_mm=0.508, notch_angle_deg=30.0, notch_root_radius_mm=0.08,
                   shift_c=53.0, two_sigma_c=24.0, length_mm=25.4, span_mm=20.0),
    "type 3": dict(W_mm=5.0, B_mm=5.0, notch_depth_mm=1.0, notch_angle_deg=45.0, notch_root_radius_mm=0.25,
                   shift_c=34.0, two_sigma_c=20.0, length_mm=27.0, span_mm=20.0),
    "type 4": dict(W_mm=4.0, B_mm=3.0, notch_depth_mm=1.0, notch_angle_deg=60.0, notch_root_radius_mm=0.08,
                   shift_c=38.0, two_sigma_c=30.0, length_mm=26.0, span_mm=22.0),
}
NOTCH_DEPTH_TOLERANCE_MM = 0.05     # 0.76 as recorded against 0.030 in = 0.762 mm, 0.51 against 0.020 in = 0.508 mm
RADIUS_TOLERANCE_MM = 0.03          # 0.1 mm as recorded for KLST against the 0.08 mm drawn in NUREG/CR-6379 Fig. 1


def sokolov_type(g: dict, notch_angle_deg, notch_root_radius_mm) -> tuple:
    """Which of Sokolov & Alexander's four specimen types a geometry is, on cross-section and notch alone (their conclusion 2
    reports that span and impact velocity, over the ranges they studied, do not affect USE or DBTT, and that changing the notch
    angle between 30 and 45 deg has no effect). Returns (type name or None, reason)."""
    for name, t in SOKOLOV_TYPES.items():
        if (np.isclose(g["W_mm"], t["W_mm"], atol=0.01) and np.isclose(g["B_mm"], t["B_mm"], atol=0.01)
                and abs(g["notch_depth_mm"] - t["notch_depth_mm"]) <= NOTCH_DEPTH_TOLERANCE_MM
                and np.isfinite(notch_root_radius_mm) and abs(notch_root_radius_mm - t["notch_root_radius_mm"]) <= RADIUS_TOLERANCE_MM):
            same_angle = np.isfinite(notch_angle_deg) and np.isclose(notch_angle_deg, t["notch_angle_deg"], atol=0.1)
            return name, ("cross-section, notch depth, angle and root radius match" if same_angle else
                          f"cross-section, notch depth and root radius match; notch angle {notch_angle_deg:g} deg against "
                          f"{t['notch_angle_deg']:g} deg (NUREG/CR-6379 conclusion 2: 30 vs 45 deg changes neither USE nor DBTT)")
    return None, "not one of the four specimen types NUREG/CR-6379 built; Eqs (18)-(21) are not extrapolated to it"


# Applicability limit carried through every table (NUREG/CR-6379 p.16 and p.29): the report restricted its upper-shelf analysis
# to full-size USE below 200 J, because tougher specimens deform against the anvils instead of fracturing and absorb energy that
# is not fracture energy. Rosinski et al., as cited by the dataset descriptor, report the same 200 J limit for irradiated
# materials. Flagged, never used to drop a comparison.
USE_APPLICABILITY_LIMIT_J = 200.0

# Kurishita et al.'s diagnostic: DBTT of a sub-size specimen approaches the full-size value once the notch depth to root radius
# ratio a/rho reaches about 15 (descriptor Table 3; 2026 ML paper Table 2). Reported for every geometry, never used as a rule.
KURISHITA_RATIO = 15.0

PRIMARY_ENERGY_METHOD = "ligament volume B b^2 (Lucas et al.)"
PRIMARY_TEMPERATURE_METHOD = "M = 98 - 15.1 ln(B b^2) (Sokolov & Alexander, NUREG/CR-6379 Eq. 22)"
ENERGY_METHODS = {
    PRIMARY_ENERGY_METHOD: nf_energy_ligament_volume,
    "fracture volume (B b)^3/2 (Corwin et al.)": nf_energy_fracture_volume_three_halves,
    "fracture area B b (Corwin first factor; Sokolov NF_brittle)": nf_energy_fracture_area,
}
TEMPERATURE_METHODS = {
    PRIMARY_TEMPERATURE_METHOD: shift_sokolov,
    "M = 92.7 - 14.34 ln(B b^2) (Lucon et al.)": shift_lucon,
    "M = 0.7 (10 - B)^2 (Towers)": shift_towers,
    "M = -51.4 ln(2 (B/10)^0.25 - 1) (Wallin)": shift_wallin,
}


def normalize(t_c, e_j, g: dict, energy_method: str = PRIMARY_ENERGY_METHOD,
              temperature_method: str = PRIMARY_TEMPERATURE_METHOD) -> tuple:
    """Map measured smaller-specimen points into the full-size-equivalent domain.

    The result is NOT new measurement data: it is a transformed estimate of full-size-equivalent behaviour derived from
    published smaller-specimen measurements. Nothing about the paired full-size curve enters here - only the smaller
    specimen's own published dimensions and fixed published constants - so no full-size answer can leak into its own
    correction (D-078, D-086 check 7)."""
    nf = ENERGY_METHODS[energy_method](g)
    m = TEMPERATURE_METHODS[temperature_method](g)
    return np.asarray(t_c, float) + m, np.asarray(e_j, float) * nf, nf, m


# ---------------------------------------------------------------------------
# 5. Self-checks (D-086 checks 1-5): run on import-time demand by the analysis script and by the test module
# ---------------------------------------------------------------------------
def self_checks() -> list:
    """Dimensional consistency, the identity at full size, a hand-calculated factor, the round trip and the no-op shift.
    Returns one row per check. Raises on failure, so a broken equation stops the pipeline instead of producing numbers."""
    rows = []
    fs = geometry(FULL_SIZE["length_mm"], FULL_SIZE["width_mm"], FULL_SIZE["thickness_mm"], FULL_SIZE["notch_depth_mm"])

    # 1. Dimensions. B [mm] * b [mm] = mm^2; B * b^2 = mm^3; every NF is a ratio of like quantities, so dimensionless; every
    #    shift is deg C. ln() takes B b^2 in mm^3, so the constants 98 and 15.1 carry the unit choice: the checks below confirm
    #    the numerical identity that fixes them.
    assert np.isclose(fs["fracture_area_mm2"], 80.0) and np.isclose(fs["ligament_volume_mm3"], 640.0)
    rows.append(dict(check="dimensional consistency",
                     detail="B b has units mm^2 and B b^2 mm^3; full-size 10 mm x 8 mm = 80 mm^2 and 10 mm x (8 mm)^2 = 640 mm^3; "
                            "every NF is a ratio of like quantities (dimensionless); every shift is in deg C; "
                            "ln(B b^2) takes mm^3, which is the unit the published constants were fitted in",
                     result="pass"))

    # 2. Identity: feeding the full-size geometry into each full-size-to-full-size normalization must give NF = 1 exactly and
    #    a shift of 0 (exactly where the source forced it, or to the rounding of the published coefficients otherwise).
    for name, fn in ENERGY_METHODS.items():
        nf = fn(fs)
        assert np.isclose(nf, 1.0, atol=1e-12), f"{name}: NF = {nf} for the full-size specimen"
        rows.append(dict(check="identity: energy NF at full size", detail=f"{name}: NF = {nf:.12g}", result="pass (exactly 1)"))
    for name, fn in TEMPERATURE_METHODS.items():
        m = fn(fs)
        forced = abs(m) < 1e-12
        assert abs(m) <= 0.5, f"{name}: shift = {m} deg C for the full-size specimen"
        rows.append(dict(check="identity: temperature shift at full size",
                         detail=f"{name}: M = {m:+.4f} deg C",
                         result="pass (exactly 0)" if forced else
                                f"pass (|M| = {abs(m):.2f} deg C, the rounding of the published coefficients; the source states "
                                f"the fit was forced through zero at the full-size specimen)"))

    # 3. Hand-calculated example, written out so a reader can repeat it with a calculator (D-086 check 3).
    half = geometry(23.6, 5.0, 5.0, 0.76)
    nf_hand = 640.0 / (5.0 * (5.0 - 0.76) ** 2)
    m_hand = 98.0 - 15.1 * np.log(5.0 * (5.0 - 0.76) ** 2)
    assert np.isclose(nf_energy_ligament_volume(half), nf_hand, rtol=1e-12)
    assert np.isclose(shift_sokolov(half), m_hand, rtol=1e-12)
    rows.append(dict(check="hand-calculated example (23.6 x 5 x 5 mm, a = 0.76 mm)",
                     detail=f"b = W - a = 5.00 - 0.76 = 4.24 mm; B b^2 = 5.00 x 4.24^2 = 5.00 x 17.9776 = {5.0 * 4.24 ** 2:.4f} mm^3; "
                            f"NF_E = 640 / {5.0 * 4.24 ** 2:.4f} = {nf_hand:.4f}; "
                            f"M = 98 - 15.1 x ln({5.0 * 4.24 ** 2:.4f}) = 98 - 15.1 x {np.log(5.0 * 4.24 ** 2):.4f} = {m_hand:.2f} deg C",
                     result=f"pass (code gives NF_E = {nf_energy_ligament_volume(half):.4f}, M = {shift_sokolov(half):.2f} deg C)"))

    # 4. Round trip: dividing back by NF and subtracting M must return the measured values to machine precision.
    t = np.array([-120.0, -60.0, 0.0, 25.0])
    e = np.array([1.5, 4.0, 9.0, 12.0])
    tn, en, nf, m = normalize(t, e, half)
    assert np.allclose(tn - m, t, atol=1e-12) and np.allclose(en / nf, e, rtol=1e-12)
    rows.append(dict(check="round trip", detail="T_fse - M and E_fse / NF_E return the measured temperatures and energies",
                     result=f"pass (max |dT| = {np.max(np.abs(tn - m - t)):.2e} deg C, max relative |dE| = "
                            f"{np.max(np.abs(en / nf - e) / e):.2e})"))

    # 5. No-op temperature shift: a geometry whose published shift is zero must leave the temperatures unchanged.
    tn0, en0, nf0, m0 = normalize(t, e, fs)
    assert np.allclose(tn0 - t, shift_sokolov(fs)) and np.isclose(nf0, 1.0)
    rows.append(dict(check="no-op shift", detail=f"the full-size geometry gives NF_E = {nf0:.12g} and M = {m0:+.4f} deg C, so the "
                                                 f"transformed temperatures move by {m0:+.4f} deg C and the energies not at all",
                     result="pass"))

    # 6. Monotonicity sanity: a smaller ligament volume must give a larger energy factor and a larger temperature shift.
    vols = [geometry(20.0, w, w, a) for w, a in [(5.0, 0.76), (3.33, 0.51), (2.5, 0.38), (1.5, 0.33)]]
    nfs = [nf_energy_ligament_volume(v) for v in vols]
    shifts = [shift_sokolov(v) for v in vols]
    assert all(np.diff(nfs) > 0) and all(np.diff(shifts) > 0)
    rows.append(dict(check="monotonicity", detail="over the 5.0, 3.33, 2.5 and 1.5 mm cross-sections the energy factor rises "
                                                  f"{nfs[0]:.1f} -> {nfs[-1]:.1f} and the shift rises {shifts[0]:.1f} -> "
                                                  f"{shifts[-1]:.1f} deg C as the ligament volume falls",
                     result="pass"))

    # 7. Reproduce the published source's own numbers. NUREG/CR-6379 Table 2 tabulates the full-size-to-subsize ratios of Bb,
    #    Bb^2 and (Bb)^{3/2} for its four specimen types, and Eqs (18)-(21) give the per-type temperature shifts that Eq. (22)
    #    was fitted through. Recomputing both from the type dimensions is an end-to-end check that this implementation is the
    #    published one and that the geometry convention (which dimension is notched) is read the same way.
    published_table2 = {"type 1": dict(Bb=3.77, Bb2=7.12, Bb32=7.33), "type 2": dict(Bb=8.52, Bb2=24.2, Bb32=24.8),
                        "type 3": dict(Bb=4.0, Bb2=8.0, Bb32=8.0), "type 4": dict(Bb=8.9, Bb2=23.7, Bb32=26.5)}
    for name, t in SOKOLOV_TYPES.items():
        g = geometry(t["length_mm"], t["W_mm"], t["B_mm"], t["notch_depth_mm"])
        got = dict(Bb=nf_energy_fracture_area(g), Bb2=nf_energy_ligament_volume(g), Bb32=nf_energy_fracture_volume_three_halves(g))
        want = published_table2[name]
        worst = max(abs(got[k] - want[k]) / want[k] for k in want)
        assert worst < 0.02, f"{name}: recomputed {got} against published Table 2 {want}"
        m22, m_type = shift_sokolov(g), t["shift_c"]
        rows.append(dict(check=f"reproduces NUREG/CR-6379 for its {name}",
                         detail=f"Table 2 ratios published Bb {want['Bb']}, Bb^2 {want['Bb2']}, (Bb)^3/2 {want['Bb32']}; "
                                f"recomputed {got['Bb']:.2f}, {got['Bb2']:.2f}, {got['Bb32']:.2f}. "
                                f"Eq. (22) gives M = {m22:.1f} deg C against the type-specific Eq. shift {m_type:+.0f} "
                                f"(+/- {t['two_sigma_c']:.0f}) deg C",
                         result=f"pass (largest Table 2 difference {worst * 100:.1f} %)"))
    return rows


if __name__ == "__main__":
    for row in self_checks():
        print(f"{row['result']:>12s}  {row['check']}: {row['detail']}")
