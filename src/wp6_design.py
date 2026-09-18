"""WP6 - Test-programme design: specimen geometries, the fixed-material-volume accounting, the physical
temperature frame and the five temperature-placement strategies.

Pure functions, no file I/O, no random numbers and - critically - **no access to the truth**. The strategy
functions receive only the prior (`t_assumed_fse`, `c_assumed`), the specimen count and, for the adaptive
strategies, the results of specimens already tested. They take no geometry argument: the specimen geometry
enters only through `place_raw()`, which is the single point where the temperature shift M is subtracted
(DECISIONS.md D-101, validation tests 7 and 19).

Temperature frame (D-101, author's review round 3). The envelope and the 5 deg C grid are physical properties
of the RAW specimen, not of the full-size-equivalent analysis frame:

    1. the strategy proposes a desired full-size-equivalent temperature T_fse_desired
    2. convert to raw:      T_raw_desired = T_fse_desired - M          (M = 0 for full-size)
    3. snap the RAW temperature to the 5 deg C grid
    4. clip the RAW temperature to the physical envelope
    5. the specimen is tested at that snapped, clipped raw temperature
    6. for analysis:        T_fse_actual  = T_raw_actual + M

M is subtracted exactly once, in step 2.
"""
from __future__ import annotations

import numpy as np

import wp5_normalization as NZ
from wp3_fitter import criterion_temperature

# ---------------------------------------------------------------------------
# 1. The physical raw-specimen temperature frame (D-101)
# ---------------------------------------------------------------------------
GRID_C = 5.0                     # physical raw test-temperature grid
T_RAW_MIN_C = -196.0             # liquid-nitrogen floor; also the cold end of Marini (2020)'s RPV matrix
T_RAW_MAX_C = 300.0              # hot end of the same range and of this cohort's tested temperatures

# The floor is not a multiple of the grid step, so the coldest raw temperature that is BOTH inside the physical
# envelope AND on the declared grid is -195 deg C. Clipping to the innermost grid points is the only reading
# under which both approved requirements of validation test 16 hold at once (16a inside the envelope, 16b on the
# grid). It is an implementation clarification, fixed before any result and recorded in D-101: no specimen is
# ever tested below the physical floor, and the 1 deg C difference is far below every tolerance in the study
# (tau = 2 deg C, grid = 5 deg C).
GRID_MIN_C = float(np.ceil(T_RAW_MIN_C / GRID_C) * GRID_C)    # -195.0
GRID_MAX_C = float(np.floor(T_RAW_MAX_C / GRID_C) * GRID_C)   # +300.0

# Prior information available to every strategy (D-101). Never the true C.
C_ASSUMED_C = 40.0               # declared nominal transition half-width (cohort median 46 deg C)
W_WIDE_C = 250.0                 # UNIFORM span (cohort median tested span 268 deg C; p10 175, p90 365)
W_CLUST_FACTOR = 3.0             # CLUSTERED span = 3 * C_assumed = 120 deg C
ANCHOR_FACTOR = 3.0              # shelf anchors at +/- 3 * C_assumed
ANCHOR_SHARE = 0.10              # 10 % of the specimens at each anchor
ADAPTIVE_SEED_MIN = 4            # seed block: max(4, round(N/3))
ADAPTIVE_SEED_DIVISOR = 3.0
ADAPTIVE_BLOCK_DIVISOR = 6.0     # block size: max(1, round(N/6))
ADAPTIVE_FALLBACK_STEP = 0.75    # fallback step, in units of C_assumed
STAIRCASE_STEP_FACTOR = 0.5      # SS step = 0.5 * C_assumed = 20 deg C
CRITERION_J = 41.0               # the full-size criterion; SS compares in the full-size-equivalent frame


def _round_half_up(x):
    """Deterministic rounding (numpy's rint uses banker's rounding, which would make a .5 tie depend on parity)."""
    return np.floor(np.asarray(x, float) + 0.5)


def snap_raw(t_raw):
    """Step 3: round a RAW specimen temperature to the physical 5 deg C grid."""
    return _round_half_up(np.asarray(t_raw, float) / GRID_C) * GRID_C


def place_raw(t_fse_desired, m_shift_c: float):
    """Steps 2-5 of D-101, the ONLY place where M is subtracted.

    Returns (t_raw_actual, t_raw_desired, clipped) with clipped True where the physical envelope moved the
    specimen. `m_shift_c` is 0.0 for the full-size geometry, so full-size passes through unchanged apart from
    the grid.
    """
    t_raw_desired = np.asarray(t_fse_desired, float) - float(m_shift_c)
    snapped = snap_raw(t_raw_desired)
    actual = np.clip(snapped, GRID_MIN_C, GRID_MAX_C)
    return actual, t_raw_desired, actual != snapped


def to_fse(t_raw_actual, m_shift_c: float):
    """Step 6: normalize the ACTUAL raw temperature back into the analysis frame."""
    return np.asarray(t_raw_actual, float) + float(m_shift_c)


def coldest_reachable_fse_c(m_shift_c: float) -> float:
    """The coldest full-size-equivalent temperature this geometry can physically reach (D-092)."""
    return GRID_MIN_C + float(m_shift_c)


# ---------------------------------------------------------------------------
# 2. Specimen geometries (D-092)
# ---------------------------------------------------------------------------
# Every miniature class that DECISIONS.md D-083 hands over as WEAKLY SUPPORTED, and only those. The two classes
# marked UNSUPPORTED BY THIS DATASET are omitted because the dataset does not support a correction for them -
# not because any other geometry is equivalent to them. Dimensions are as recorded in the dataset; the KLST
# width/thickness reading of D-072 is applied by wp5_normalization.geometry(), and the gross prism volume
# L*W*B is unaffected by that swap.
GEOMETRY_DIMENSIONS = {
    # code: (wp5 geometry id, length_mm, width_mm as recorded, thickness_mm as recorded, notch depth mm)
    "G0": ("55x10x10 a=2 (full-size)", 55.0, 10.0, 10.0, 2.0),
    "G1": ("20x1.5x1.5 a=0.33", 20.0, 1.5, 1.5, 0.33),
    "G2": ("20x2.5x2.5 a=0.38", 20.0, 2.5, 2.5, 0.38),
    "G3": ("20x3.33x3.33 a=0.51", 20.0, 3.33, 3.33, 0.51),
    "G4": ("27.5x3.33x3.33 a=0.6", 27.5, 3.33, 3.33, 0.6),
    "G5": ("23.6x3.33x3.33 a=0.51", 23.6, 3.33, 3.33, 0.51),
    "G6": ("27x3x4 a=1", 27.0, 3.0, 4.0, 1.0),
    "G7": ("23.6x5x5 a=0.76", 23.6, 5.0, 5.0, 0.76),
}
FULL_SIZE_CODE = "G0"
MINIATURE_CODES = ["G1", "G2", "G3", "G5", "G4", "G6", "G7"]   # ordered by gross volume
ALL_CODES = [FULL_SIZE_CODE] + MINIATURE_CODES

# D-083: the two geometry classes WP6 must not simulate, with the reason recorded beside them.
UNSUPPORTED_GEOMETRIES = {
    "20x5x5 a=0.76": "UNSUPPORTED BY THIS DATASET (D-083): no matched comparison reaches the WP5 primary "
                     "analysis set. Omitted because the dataset does not support a correction for it, NOT "
                     "because another geometry is physically equivalent.",
    "23.6x5x5 a=0.78": "UNSUPPORTED BY THIS DATASET (D-083): as above. Not treated as covered by "
                       "'23.6x5x5 a=0.76' despite the 0.02 mm notch-depth difference.",
}


def geometry_info(code: str, klst_reading: bool = True) -> dict:
    """Geometry, normalization factor and temperature shift, all from the approved WP5 module.

    NF_E and M are recomputed from the specimen's own published dimensions and fixed published constants only
    (D-074, WP5 leakage check 8): nothing about any full-size answer enters.
    """
    wp5_id, length, width, thickness, notch = GEOMETRY_DIMENSIONS[code]
    g = NZ.geometry(length, width, thickness, notch, apply_klst_correction=klst_reading)
    full_size = code == FULL_SIZE_CODE
    return dict(
        code=code, wp5_geometry_id=wp5_id, is_full_size=full_size,
        length_mm=length, width_recorded_mm=width, thickness_recorded_mm=thickness, notch_depth_mm=notch,
        W_mm=g["W_mm"], B_mm=g["B_mm"], ligament_mm=g["ligament_mm"],
        ligament_volume_mm3=g["ligament_volume_mm3"], fracture_area_mm2=g["fracture_area_mm2"],
        nf_energy=1.0 if full_size else NZ.nf_energy_ligament_volume(g),
        m_shift_c=0.0 if full_size else NZ.shift_sokolov(g),
        gross_volume_mm3=length * width * thickness,
        geometry_note=g["geometry_note"],
    )


def geometry_table(klst_reading: bool = True) -> list:
    return [geometry_info(c, klst_reading) for c in ALL_CODES]


# ---------------------------------------------------------------------------
# 3. Fixed-material-volume accounting (D-091)
# ---------------------------------------------------------------------------
# An IDEALIZED FINISHED-SPECIMEN MATERIAL-ONLY accounting. NOT a prediction of how many specimens physically fit
# in, or can be machined from, a real surveillance capsule: capsule layout, holder geometry, orientation,
# archive requirements, broken-half reconstitution and machining yield are not modelled. This sentence is
# carried on every generated table that shows a specimen count.
IDEALIZED_ACCOUNTING_NOTE = (
    "idealized finished-specimen material-only accounting (D-091): gross rectangular volume L*W*B, integer "
    "floor, unused remainder discarded, notch volume not recovered; NOT a prediction of how many specimens fit "
    "in or can be machined from a real surveillance capsule"
)
FULL_SIZE_VOLUME_MM3 = 55.0 * 10.0 * 10.0        # 5500 mm^3, the budget unit
BUDGET_MULTIPLES_K = [4, 6, 8, 12, 18, 24]       # V_budget = k * 5500 mm^3, so N_full = k
MACHINING_ALLOWANCES_MM = [0.0, 0.5, 1.0]        # c = 0 central; 0.5 and 1.0 are the labelled sensitivity


def specimen_volume_mm3(code: str, allowance_c_mm: float = 0.0) -> float:
    """Gross rectangular finished-specimen volume, with an optional uniform linear allowance per face (D-091)."""
    _, length, width, thickness, _ = GEOMETRY_DIMENSIONS[code]
    c = float(allowance_c_mm)
    return (length + 2 * c) * (width + 2 * c) * (thickness + 2 * c)


def budget_volume_mm3(k: int) -> float:
    return float(k) * FULL_SIZE_VOLUME_MM3


def specimen_count(code: str, k: int, allowance_c_mm: float = 0.0) -> int:
    """N = floor(V_budget / V_specimen): integer floor, unused remainder discarded (D-091)."""
    return int(np.floor(budget_volume_mm3(k) / specimen_volume_mm3(code, allowance_c_mm)))


# ---------------------------------------------------------------------------
# 4. Temperature-placement strategies (D-101)
# ---------------------------------------------------------------------------
STRATEGIES = ["U", "C", "A", "S", "SS"]
STRATEGY_LABELS = {
    "U": "uniform / wide span (250 deg C)",
    "C": "clustered near the expected transition (3 * C_assumed = 120 deg C)",
    "A": "clustered with shelf anchors (Marini RCC-M shape)",
    "S": "adaptive, model-based and batched",
    "SS": "simple up/down staircase (raw space)",
}


def _evenly_spaced(centre: float, span: float, n: int) -> np.ndarray:
    if n <= 0:
        return np.empty(0, float)
    if n == 1:
        return np.array([float(centre)])
    return float(centre) + float(span) * (np.arange(n, dtype=float) / (n - 1) - 0.5)


def place_temperatures(strategy: str, t_assumed_fse: float, c_assumed: float, n: int,
                       history: dict | None = None) -> np.ndarray:
    """Desired FULL-SIZE-EQUIVALENT temperatures for a non-adaptive strategy (U, C, A).

    No truth argument and no geometry argument: the design cannot see the true curve, and M is applied later by
    place_raw(). `history` is accepted for interface symmetry with the adaptive strategies and is unused here.
    """
    if strategy not in ("U", "C", "A"):
        raise ValueError(f"place_temperatures handles the fixed designs U, C and A; got {strategy!r}")
    n = int(n)
    if n <= 0:
        return np.empty(0, float)
    if strategy == "U":
        return _evenly_spaced(t_assumed_fse, W_WIDE_C, n)
    if strategy == "C":
        return _evenly_spaced(t_assumed_fse, W_CLUST_FACTOR * c_assumed, n)
    # A: clustered with shelf anchors
    n_anchor = int(max(1, _round_half_up(ANCHOR_SHARE * n)))
    n_anchor = min(n_anchor, n // 2)
    cold = t_assumed_fse - ANCHOR_FACTOR * c_assumed
    hot = t_assumed_fse + ANCHOR_FACTOR * c_assumed
    middle = _evenly_spaced(t_assumed_fse, W_CLUST_FACTOR * c_assumed, n - 2 * n_anchor)
    return np.concatenate([np.full(n_anchor, cold), middle, np.full(n_anchor, hot)])


def adaptive_seed_size(n: int) -> int:
    return int(min(int(n), max(ADAPTIVE_SEED_MIN, int(_round_half_up(int(n) / ADAPTIVE_SEED_DIVISOR)))))


def adaptive_block_size(n: int) -> int:
    return int(max(1, int(_round_half_up(int(n) / ADAPTIVE_BLOCK_DIVISOR))))


def _delta_cycle(k: int) -> np.ndarray:
    """0, -0.5, +0.5, -1.0, +1.0, -1.5, +1.5, ... (D-101)."""
    out = [0.0]
    step = 0.5
    while len(out) < k:
        out.append(-step)
        if len(out) < k:
            out.append(+step)
        step += 0.5
    return np.array(out[:k], float)


def adaptive_block_targets(fit: dict | None, t_fse_actual, e_fse, t_assumed_fse: float, c_assumed: float,
                           k: int) -> np.ndarray:
    """Desired full-size-equivalent temperatures for the next adaptive block (strategy S, D-101).

    Sees only the approved fit of the specimens already tested and their analysed temperatures and energies -
    never the truth. An out-of-range crossing MAY be used for design: D-044's tested-range rule governs
    reporting, not the choice of the next test temperature.
    """
    k = int(k)
    if k <= 0:
        return np.empty(0, float)
    t_fse_actual = np.asarray(t_fse_actual, float)
    e_fse = np.asarray(e_fse, float)
    if fit is not None and fit.get("optimizer_success", False):
        value, status = criterion_temperature(fit["lse_j"], fit["use_j"], fit["t0_c"], fit["c_c"], CRITERION_J)
        if status == "defined" and np.isfinite(value) and np.isfinite(fit["c_c"]):
            return float(value) + _delta_cycle(k) * float(fit["c_c"])
    # Fallbacks, in the order D-101 fixes them.
    if len(e_fse) == 0 or fit is None or not fit.get("optimizer_success", False):
        return np.full(k, float(t_assumed_fse))
    if np.all(e_fse >= CRITERION_J):
        return np.full(k, float(np.min(t_fse_actual)) - ADAPTIVE_FALLBACK_STEP * c_assumed)
    if np.all(e_fse < CRITERION_J):
        return np.full(k, float(np.max(t_fse_actual)) + ADAPTIVE_FALLBACK_STEP * c_assumed)
    return np.full(k, float(t_assumed_fse))


def staircase_start_raw(t_assumed_fse: float, c_assumed: float, m_shift_c: float) -> float:
    """SS start (D-101): the ONE deliberate raw-space exception, still a single subtraction of M."""
    raw, _, _ = place_raw(np.array([float(t_assumed_fse)]), m_shift_c)
    return float(raw[0])


def staircase_next_raw(current_raw: float, e_fse: float, c_assumed: float) -> tuple:
    """SS step (D-101). E_fse < 41 J -> warmer; E_fse >= 41 J (including exact equality) -> colder.

    Returns (next_raw_actual, clipped). Snapping and clipping happen in raw space, and a clipped step leaves the
    next specimen at the boundary temperature (repeats are allowed and counted).
    """
    step = STAIRCASE_STEP_FACTOR * float(c_assumed)
    proposed = float(current_raw) + (step if float(e_fse) < CRITERION_J else -step)
    snapped = float(snap_raw(proposed))
    actual = float(np.clip(snapped, GRID_MIN_C, GRID_MAX_C))
    return actual, actual != snapped
