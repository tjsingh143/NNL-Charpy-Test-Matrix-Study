# Charpy test matrix study — Code samples

Six excerpts from the computational study. Published measurements, fitted quantities and conditional simulations keep their distinct evidence classes. These examples do not imply physical testing by this project.

Reviewed October 11, 2026. Every code block below is a contiguous, verbatim excerpt from source at commit `f523bee`. Links pin the exact file and line range. Separate ranges have separate blocks; no code is rewritten or elided inside a block.

The older Drive source copy remains a historical archive. Current source is in GitHub; private repositories require existing access.

## 1. Bounds and identifiability diagnostics

The fitter declares physical bounds and scaling, then records near-bound parameters, Jacobian rank, condition number and spread among near-optimal starts. Optimizer success alone does not establish an identifiable transition.

[src/wp3_fitter.py, lines 184–204](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp3_fitter.py#L184-L204)

```python
def fit_curve(t, e, lse_fixed=None) -> dict:
    """Bounded ordinary least-squares tanh fit of absorbed energy e (J) against test temperature t (°C).
    lse_fixed: None to fit LSE, or the fixed LSE value (J). Returns estimates, bounds, optimizer metadata and diagnostics."""
    t, e = np.asarray(t, float), np.asarray(e, float)
    names = (["lse"] if lse_fixed is None else []) + ["rise", "t0", "c"]
    n, p = len(t), len(names)
    out = dict(n_points=n, n_parameters=p, lse_mode="fitted" if lse_fixed is None else "fixed",
               lse_fixed_j=np.nan if lse_fixed is None else float(lse_fixed))
    if n <= p or np.ptp(t) <= 0 or e.max() <= 0:
        return {**out, "optimizer_success": False, "optimizer_status": np.nan,
                "optimizer_message": "not attempted: fewer points than parameters, one test temperature, or no positive energy"}
    e_max, t_min, t_max = float(e.max()), float(t.min()), float(t.max())
    span = t_max - t_min
    bounds = dict(lse=(0.0, e_max), rise=(0.0, RISE_MAX_FACTOR * e_max),
                  t0=(max(ABSOLUTE_ZERO_C, t_min - span), t_max + span), c=(C_MIN_C, max(span, 2.0 * C_MIN_C)))
    # Scale to order one: energies by the highest measured energy, temperatures about the middle of the tested range.
    e_s, t_ref, t_s = e_max, 0.5 * (t_min + t_max), 0.5 * span
    to_scaled = dict(lse=lambda v: v / e_s, rise=lambda v: v / e_s, t0=lambda v: (v - t_ref) / t_s, c=lambda v: v / t_s)
    to_phys = dict(lse=lambda v: v * e_s, rise=lambda v: v * e_s, t0=lambda v: v * t_s + t_ref, c=lambda v: v * t_s)
    tau = (t - t_ref) / t_s
    lse_s_fixed = None if lse_fixed is None else float(lse_fixed) / e_s
```

[src/wp3_fitter.py, lines 246–274](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp3_fitter.py#L246-L274)

```python
    best_cost = min(tr["cost"] for tr in good)
    best = next(tr for tr in good if tr["cost"] <= best_cost * (1.0 + 1e-9) + 1e-15)  # earliest start among equal-cost optima
    r = best["result"]
    est = {k: to_phys[k](v) for k, v in zip(names, r.x)}
    lse = float(lse_fixed) if lse_fixed is not None else est["lse"]
    use, t0, c = lse + est["rise"], est["t0"], est["c"]
    near = [tr for tr in good if tr["cost"] <= best_cost * 1.01 + 1e-15]
    near_t0 = [to_phys["t0"](tr["result"].x[names.index("t0")]) for tr in near]
    at_low, at_high = {}, {}
    for j, k in enumerate(names):
        width = ub[j] - lb[j]
        at_low[k] = bool(r.active_mask[j] == -1 or r.x[j] - lb[j] <= NEAR_BOUND_FRACTION * width)
        at_high[k] = bool(r.active_mask[j] == 1 or ub[j] - r.x[j] <= NEAR_BOUND_FRACTION * width)
    sv = np.linalg.svd(r.jac, compute_uv=False)
    rank = int(np.sum(sv > sv.max() * max(r.jac.shape) * np.finfo(float).eps)) if sv.max() > 0 else 0
    fitted = tanh_energy(t, lse, use, t0, c)
    sse = float(np.sum((e - fitted) ** 2))
    out.update(optimizer_success=True, optimizer_status=int(r.status), optimizer_message=str(r.message),
               best_start=int(best["start"]), start_values=" | ".join(
                   ", ".join(f"{k}={to_phys[k](v):.4g}" for k, v in zip(names, tr["z0"])) for tr in trials),
               nfev=int(r.nfev), n_starts_within_1pct_of_best_cost=len(near),
               t0_spread_within_1pct_of_best_cost_c=float(np.ptp(near_t0)),
               lse_j=lse, use_j=use, t0_c=t0, c_c=c, sse=sse, rmse_j=float(np.sqrt(sse / n)),
               residual_sd_j=float(np.sqrt(sse / (n - p))), jacobian_rank=rank, jacobian_condition_number=
               float(sv.max() / sv.min()) if sv.min() > 0 else np.inf)
    for k in names:
        out[f"at_lower_bound_{k}"], out[f"at_upper_bound_{k}"] = at_low[k], at_high[k]
    out.update(coverage_diagnostics(t, e, lse, use, t0, c))
    return out
```

## 2. Matching republished curve points

Candidate temperature and energy matches are ordered by normalized distance. Each point can be used once, preventing many-to-one matches from inflating overlap. The surrounding duplicate and offset screens decide how this count is used.

[src/wp1_clean.py, lines 281–299](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp1_clean.py#L281-L299)

```python
def greedy_match(t_a, e_a, t_b, e_b, tol_t, k_e):
    tol_e = k_e * max(e_a.max(), e_b.max())
    if tol_e <= 0:
        return 0
    dt = np.abs(t_a[:, None] - t_b[None, :])
    de = np.abs(e_a[:, None] - e_b[None, :])
    ok = (dt <= tol_t) & (de <= tol_e)
    if not ok.any():
        return 0
    ii, jj = np.nonzero(ok)
    order = np.argsort(dt[ii, jj] / tol_t + de[ii, jj] / tol_e, kind="stable")
    used_i, used_j, m = set(), set(), 0
    for k in order:
        i, j = ii[k], jj[k]
        if i not in used_i and j not in used_j:
            used_i.add(i)
            used_j.add(j)
            m += 1
    return m
```

## 3. Tracing report quantities

Direct lookups and derived expressions carry a source selector or named inputs. Whitelisted table calculations make structural report claims auditable in the claim map; the later prose lint enforces evidence wording.

[src/wp7_report.py, lines 42–59](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp7_report.py#L42-L59)

```python
@dataclass(frozen=True)
class Lookup:
    """One value read from one cell of one generated table."""
    file: str                       # relative to outputs/
    where: dict                     # column -> value; must select exactly one row
    col: str
    fmt: str = "{:g}"
    note: str = ""


@dataclass(frozen=True)
class Derived:
    """A value computed from other registry keys. The expression and the inputs are printed
    in claim_source_map.csv so the arithmetic is auditable (D-114, D-123)."""
    expr: str                       # python expression over the names in `inputs`
    inputs: dict = field(default_factory=dict)   # name -> registry key
    fmt: str = "{:g}"
    note: str = ""
```

[src/wp7_report.py, lines 84–94](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp7_report.py#L84-L94)

```python
# Whitelisted table functions. Each is one readable expression so the claim map can print it.
CALCS: dict[str, tuple[str, object]] = {
    "min_k_full_size_sweeps": (
        "smallest k at which every T1 comparison is FULL-SIZE WINS",
        lambda d: min(k for k, g in d.groupby("k_budget") if (g.winner == "FULL-SIZE WINS").all())),
    "min_k_no_miniature_win": (
        "smallest k at which no T1 comparison is MINIATURE WINS",
        lambda d: min(k for k, g in d.groupby("k_budget") if not (g.winner == "MINIATURE WINS").any())),
    "n_geometries": ("distinct miniature geometries compared", lambda d: d.geom_code.nunique()),
    "n_archetypes": ("distinct true-curve archetypes", lambda d: d.archetype_id.nunique()),
}
```

## 4. Hashing resolved checkpoint inputs

The dependency manifest hashes the input files actually resolved by the readers, hashes source files, and records numerical-library versions. A cache key based on filenames alone would miss changed input values.

[src/wp6_checkpoint.py, lines 33–61](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp6_checkpoint.py#L33-L61)

```python
def input_files() -> dict[str, Path]:
    """Actual paths resolved by the calibration readers, keyed without machine-specific paths.

    Hashing their bytes covers values, pool membership and cohort data, rather than merely
    recording filenames or symbolic scenario names. A relocated identical input is equivalent.
    """
    import common
    import wp6_correction as correction
    import wp6_scatter as scatter
    paths = {f"outputs/wp5/{name}": correction.WP5 / name for name in (
        "wp6_size_correction_handoff.csv", "size_correction_summary_overall.csv",
        "normalization_sensitivity_comparison.csv", "size_correction_residuals.csv")}
    paths.update({f"outputs/wp4/{name}": scatter.OUTPUTS / "wp4" / name for name in (
        "published_residual_scatter_summary.csv", "published_residual_scatter_dataset.csv")})
    paths.update({f"outputs/wp3/{name}": scatter.OUTPUTS / "wp3" / name for name in (
        "fits_primary.csv", "fits_looser_cohort_curves.csv")})
    for rel in ("data/processed/primary/charpy_records_with_curves.csv", "data/FROZEN_COHORTS_CP2.csv"):
        paths[rel] = common.ROOT / rel
    return paths


def dependency_manifest() -> dict:
    import scipy
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(schema="WP6 input-sensitive checkpoints, D-127",
                sources={rel: digest(ROOT / rel) for rel in SOURCES},
                inputs={rel: digest(path) for rel, path in input_files().items()},
                runtime=dict(python=platform.python_version(), numpy=np.__version__,
                             scipy=scipy.__version__, pandas=pd.__version__))
```

## 5. Recomputing output checks independently

The material budget is reconstructed from the hand geometry and allowance, then checked against both output rows and hand-worked reference counts. The module deliberately avoids importing the WP6 implementation paths it checks.

[src/wp6_tests.py, lines 49–67](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp6_tests.py#L49-L67)

```python
def c1_material_budget():
    t = pd.read_csv(OUT / "material_budget_accounting.csv")
    bad = []
    for _, r in t.iterrows():
        _, L, W, B, _ = HAND_GEOMETRY[r["geometry_code"]]
        c = float(r["allowance_c_mm"])
        v = (L + 2 * c) * (W + 2 * c) * (B + 2 * c)
        n = int(np.floor(float(r["budget_k"]) * 5500.0 / v))
        if n != int(r["n_specimens"]) or abs(v - float(r["specimen_volume_mm3"])) > 1e-9:
            bad.append(f"{r['geometry_code']} k={r['budget_k']} c={c}")
    zero = t[t.allowance_c_mm == 0.0]
    for code in HAND_GEOMETRY:
        for k, hand in ((4, HAND_K4), (24, HAND_K24)):
            got = int(zero[(zero.geometry_code == code) & (zero.budget_k == k)]["n_specimens"].iloc[0])
            if got != hand[code]:
                bad.append(f"{code} k={k}: {got} != hand {hand[code]}")
    check("material budget recomputed independently", not bad,
          f"all {len(t)} rows reproduce floor(k x 5500 / (L+2c)(W+2c)(B+2c), and k = 4 and k = 24 match the "
          f"hand-worked table for all 8 geometries" + ("" if not bad else " PROBLEMS: " + "; ".join(bad)))
```

## 6. Keeping literature equations attributed

The ligament-volume normalization retains its literature references and dimensional identity. A normalized full-size equivalent remains a transformed estimate, as defined in the study documentation.

[src/wp5_normalization.py, lines 83–92](https://github.com/tjsingh143/NNL-Charpy-Test-Matrix-Study/blob/f523bee0fb7ab452b32915407943409e94e99f12/src/wp5_normalization.py#L83-L92)

```python
def nf_energy_ligament_volume(g: dict) -> float:
    """PRIMARY (D-073). Lucas et al.: absorbed energy on the upper shelf scales with the nominal fracture (ligament) volume
    B*b^2, so NF_E = (B b^2)_full-size / (B b^2)_smaller.

    Source: Lucas, Odette, Sheckherd, McConnell & Perrin (1986) ASTM STP 888:304-324 and Lucas, Odette, Sheckherd &
    Krishnadev (1986) Fusion Technology 10:728-733, as stated in NUREG/CR-6379 p.14 ("Lucas et al. also used an NF equal to
    the ratio of the FV of full-size to subsize specimens, but expressed the nominal FV as Bb^2"), in Lucon/NIST Eq. 10 (NF3),
    in the dataset descriptor's Table 2 (B(W-A)^2) and in the 2026 ML paper's Table 1.
    Dimensions: mm^3 / mm^3, dimensionless. Identity: NF_E = 1 for the full-size specimen."""
    return FULL_SIZE_LIGAMENT_VOLUME_MM3 / g["ligament_volume_mm3"]
```
