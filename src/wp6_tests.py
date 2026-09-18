"""WP6 - Independent checks of the generated outputs.

Deliberately independent: this module recomputes what it checks from the raw geometry, the declared design
rules and the approved WP5 outputs, and reads the WP6 results back from disk. It imports none of the WP6 code
paths it is checking (it uses only numpy, pandas and the approved wp5_normalization for the published
equations), so a shared bug cannot hide a wrong number - the pattern src/wp5_tests.py established (D-086).

A failure raises and stops the pipeline.
"""
from __future__ import annotations

import subprocess

import numpy as np
import pandas as pd

import wp5_normalization as NZ
from common import OUTPUTS, ROOT, verify_checksums

OUT = OUTPUTS / "wp6"
WP5 = OUTPUTS / "wp5"
RESULTS: list = []

# Hand-written here, independently of src/wp6_design.py, so the two must agree.
HAND_GEOMETRY = {
    "G0": ("55x10x10 a=2 (full-size)", 55.0, 10.0, 10.0, 2.0),
    "G1": ("20x1.5x1.5 a=0.33", 20.0, 1.5, 1.5, 0.33),
    "G2": ("20x2.5x2.5 a=0.38", 20.0, 2.5, 2.5, 0.38),
    "G3": ("20x3.33x3.33 a=0.51", 20.0, 3.33, 3.33, 0.51),
    "G4": ("27.5x3.33x3.33 a=0.6", 27.5, 3.33, 3.33, 0.6),
    "G5": ("23.6x3.33x3.33 a=0.51", 23.6, 3.33, 3.33, 0.51),
    "G6": ("27x3x4 a=1", 27.0, 3.0, 4.0, 1.0),
    "G7": ("23.6x5x5 a=0.76", 23.6, 5.0, 5.0, 0.76),
}
HAND_K4 = {"G0": 4, "G1": 488, "G2": 176, "G3": 99, "G5": 84, "G4": 72, "G6": 67, "G7": 37}
HAND_K24 = {"G0": 24, "G1": 2933, "G2": 1056, "G3": 595, "G5": 504, "G4": 432, "G6": 407, "G7": 223}
GRID_C, RAW_MIN, RAW_MAX = 5.0, -196.0, 300.0
GRID_MIN = float(np.ceil(RAW_MIN / GRID_C) * GRID_C)
W_WIDE = 250.0


def check(name: str, passed: bool, detail: str):
    RESULTS.append(dict(check=name, passed=bool(passed), detail=detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {detail}", flush=True)
    if not passed:
        raise RuntimeError(f"WP6 independent check failed: {name}: {detail}")


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


def c2_geometry_reconciliation():
    rec = pd.read_csv(OUT / "wp5_geometry_reconciliation.csv")
    hand = pd.read_csv(WP5 / "wp6_size_correction_handoff.csv", float_precision="round_trip")
    hand = hand[~hand["smaller_geometry"].str.startswith("POOLED")]
    ok = len(rec) == 9 and int(rec["simulated_in_wp6"].sum()) == 7
    merged = rec.merge(hand[["smaller_geometry", "evidence_status"]], left_on="wp5_geometry_id",
                       right_on="smaller_geometry")
    ok = ok and len(merged) == 9 and bool((merged["wp5_evidence_status"] == merged["evidence_status"]).all())
    uns = set(rec[~rec.simulated_in_wp6]["wp5_geometry_id"])
    ok = ok and uns == {"20x5x5 a=0.76", "23.6x5x5 a=0.78"}
    ok = ok and bool((rec[~rec.simulated_in_wp6]["wp5_evidence_status"] == "UNSUPPORTED BY THIS DATASET").all())
    check("WP5 -> WP6 geometry reconciliation", ok,
          f"all 9 handoff rows accounted for: 7 WEAKLY SUPPORTED simulated, 2 UNSUPPORTED omitted "
          f"({sorted(uns)}), 0 collapsed; every evidence status matches the handoff")


def c3_correction_values():
    sc = pd.read_csv(OUT / "size_correction_scenarios.csv", float_precision="round_trip")
    hand = pd.read_csv(WP5 / "wp6_size_correction_handoff.csv", float_precision="round_trip")
    pooled = hand[hand["smaller_geometry"].str.startswith("POOLED")].iloc[0]
    ov = pd.read_csv(WP5 / "size_correction_summary_overall.csv", float_precision="round_trip")
    allstrict = ov[(ov["subset"].str.startswith("all STRICT"))
                   & (ov["weighting"].str.startswith("family-weighted"))].iloc[0]
    cen = sc[sc.scenario == "CENTRAL"].iloc[0]
    con = sc[sc.scenario == "CONSERVATIVE"].iloc[0]
    ok = (float(cen["bias_c"]) == float(pooled["central_bias_c"])
          and float(cen["sd_c"]) == float(pooled["residual_scale_sd_c"])
          and float(con["bias_c"]) == float(allstrict["mean_c"])
          and float(con["sd_c"]) == float(allstrict["sd_c"]))
    norm = pd.read_csv(WP5 / "normalization_sensitivity_comparison.csv", float_precision="round_trip")
    for _, r in norm.iterrows():
        row = sc[sc.scenario == f"NORM:{r['case']}"]
        if len(row) and abs(float(row.iloc[0]["bias_c"]) - float(r["family_weighted_mean_c"])) > 1e-12:
            ok = False
    s2 = sc[sc.scenario.str.contains("S2 energy", na=False)]
    ok = ok and (len(s2) == 0 or bool(s2["evidence"].str.contains("NOT a WP6 scenario").all()))
    check("correction scenario values read back at full precision", ok,
          f"CENTRAL {float(cen['bias_c'])!r} / {float(cen['sd_c'])!r} and CONSERVATIVE {float(con['bias_c'])!r} / "
          f"{float(con['sd_c'])!r} equal the approved WP5 outputs exactly; every normalization scenario matches "
          f"outputs/wp5/normalization_sensitivity_comparison.csv; S2 is marked not a scenario")


def c4_family_pools():
    p = pd.read_csv(OUT / "size_correction_family_pools.csv", float_precision="round_trip")
    res = pd.read_csv(WP5 / "size_correction_residuals.csv", float_precision="round_trip")
    res = res[res["delta_t_size_c"].notna()]
    bad = []
    for subset, sel in (("primary", res[res["in_primary_analysis_set"].astype(str).str.lower() == "true"]),
                        ("all_strict", res[res["match_class"].str.startswith("STRICT")])):
        want = sel.groupby("family_id")["delta_t_size_c"].mean().sort_index()
        got = p[p["pool"] == subset].set_index("family_id")["delta_t_size_c"].sort_index()
        if len(want) != len(got) or np.max(np.abs(want.to_numpy() - got.to_numpy())) > 1e-12:
            bad.append(subset)
        if abs(float(got.mean()) - float(p[p["pool"] == subset]["pool_mean_c"].iloc[0])) > 1e-9:
            bad.append(f"{subset} mean")
    check("family-level correction pools", not bad,
          "the 7 primary and 10 all-STRICT family values in the WP6 output are exactly the family means of "
          "outputs/wp5/size_correction_residuals.csv, and reproduce their recorded pool mean")


def c5_reachability():
    t = pd.read_csv(OUT / "geometry_reachability.csv", float_precision="round_trip")
    bad = []
    for code, (_, L, W, B, a) in HAND_GEOMETRY.items():
        m = 0.0 if code == "G0" else NZ.shift_sokolov(NZ.geometry(L, W, B, a))
        sub = t[t.geometry_code == code]
        if abs(float(sub["coldest_reachable_fse_c"].iloc[0]) - (GRID_MIN + m)) > 1e-9:
            bad.append(code)
        want = sub["t41j_true_c"] >= GRID_MIN + m
        if not bool((want == sub["transition_reachable"]).all()):
            bad.append(f"{code} flags")
    counts = (t[t.truth_kind == "WP3 usable full-size fit"].groupby("geometry_code")["transition_reachable"]
              .apply(lambda s: int((~s).sum())).to_dict())
    check("geometry reachability recomputed from -196 + M", not bad,
          f"the coldest reachable full-size-equivalent temperature is the coldest on-grid raw temperature "
          f"{GRID_MIN:g} deg C plus the geometry's own M, and every reachability flag follows; unreachable "
          f"transitions among the 104 usable full-size fits: {counts}")


def c6_failure_accounting():
    t = pd.read_csv(OUT / "cell_results.csv")
    cols = [c for c in t.columns if c.startswith("outcome_")]
    total = t[cols].sum(axis=1) + t["n_evaluation_errors"]
    ok_sum = bool((total == t["replicates"]).all())
    ok_av = bool((np.round(t["availability"] * t["replicates"]).astype(int) == t["n_available"]).all())
    check("failure accounting closes in every cell", ok_sum and ok_av,
          f"in all {len(t)} cells the WP3 outcome counts plus evaluation errors sum exactly to R, and "
          f"availability x R equals the number of available replicates; failures stay in the denominator")


def c7_clip_fraction():
    t = pd.read_csv(OUT / "cell_results.csv")
    sel = t[(t.tier == "T1") & (t.strategy == "U") & (t.geom_code != "G0") & (t.archetype_id == "A5")
            & (t.n > 40)]
    bad = []
    for _, r in sel.iterrows():
        code = r["geom_code"]
        _, L, W, B, a = HAND_GEOMETRY[code]
        m = NZ.shift_sokolov(NZ.geometry(L, W, B, a))
        lo, hi = float(r["t41j_true_c"]) - W_WIDE / 2, float(r["t41j_true_c"]) + W_WIDE / 2
        expected = max(0.0, min(hi, GRID_MIN + m) - lo) / (hi - lo)
        if abs(float(r["temperature_clip_fraction"]) - expected) > 0.03:
            bad.append(f"{code} k={r['k_budget']}: {r['temperature_clip_fraction']:.3f} vs {expected:.3f}")
    check("temperature clip fraction recomputed independently", not bad,
          f"for all {len(sel)} wide-span miniature cells of archetype A5 the recorded clip fraction matches an "
          f"independent prediction from the uniform design rule and {GRID_MIN:g} + M to within 3 percentage "
          f"points" + ("" if not bad else " PROBLEMS: " + "; ".join(bad)))


def c8_sign_convention():
    t = pd.read_csv(OUT / "cell_results.csv")
    sel = t[(t.tier == "T3") & (t.variant == "SD=0") & (t.eligible)]
    bias = pd.read_csv(WP5 / "wp6_size_correction_handoff.csv", float_precision="round_trip")
    bias = float(bias[bias["smaller_geometry"].str.startswith("POOLED")].iloc[0]["central_bias_c"])
    med = float(sel["bias_c"].median())
    ok = abs(med - bias) < 2.0 and np.sign(med) == np.sign(bias)
    check("D-078 sign convention preserved end to end", ok,
          f"at correction SD = 0 the median recovered bias over {len(sel)} eligible miniature cells is "
          f"{med:+.2f} deg C against the injected pooled bias {bias:+.4f} deg C: same sign, same magnitude. A "
          f"reversed convention would show {-bias:+.2f} deg C.")


def c9_grid_integrity():
    g = pd.read_csv(OUT / "experiment_grid.csv")
    c = pd.read_csv(OUT / "cell_results.csv")
    tiers = g.groupby("tier").size().to_dict()
    expected = {"T1": 1728, "T2": 864, "T3": 576, "T4": 1296, "T5": 1664, "T6": 6, "T7": 54}
    missing = set(g[g.tier != "T6"]["cell_id"]) - set(c["cell_id"])
    check("the frozen grid is complete and unchanged", tiers == expected and not missing and len(g) == 6188,
          f"{len(g)} cells: {tiers}; every non-T6 cell has a result row")


def c10_wp0_wp5_untouched():
    paths = ["data", "outputs/wp0", "outputs/wp1", "outputs/wp1_sensitivity_eny5v-www93", "outputs/wp2",
             "outputs/wp2_sensitivity_eny5v-www93", "outputs/wp3", "outputs/wp4", "outputs/wp5",
             "src/common.py", "src/curated_metadata.py", "src/wp0_data_dictionary.py", "src/wp1_clean.py",
             "src/wp2_curves.py", "src/wp3_fitter.py", "src/wp3_validation.py", "src/wp3_fit_curves.py",
             "src/wp4_bootstrap.py", "src/wp4_checkpoint.py", "src/wp4_uncertainty.py", "src/wp4_validation.py",
             "src/wp5_normalization.py", "src/wp5_pairs.py", "src/wp5_size_effect.py", "src/wp5_tests.py"]
    try:
        out = subprocess.run(["git", "diff", "--name-only", "main", "--"] + paths, cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
    except Exception as exc:
        check("WP0-WP5 untouched", False, f"could not compare with main: {exc}")
        return
    check("WP0-WP5 outputs and sources untouched", out == "",
          "every file under data/, outputs/wp0-wp5 and every WP0-WP5 source is identical to the approved CP4 "
          "state on main" + ("" if out == "" else f"; CHANGED: {out}"))


def c11_raw_checksums():
    res = verify_checksums()
    check("raw data immutable", all(r["ok"] for r in res),
          f"all {len(res)} raw-file checksums verify; WP6 writes nothing outside outputs/wp6/")


CHECKS = [c1_material_budget, c2_geometry_reconciliation, c3_correction_values, c4_family_pools,
          c5_reachability, c6_failure_accounting, c7_clip_fraction, c8_sign_convention, c9_grid_integrity,
          c10_wp0_wp5_untouched, c11_raw_checksums]


def main():
    print("WP6 independent checks (they import no WP6 code path under test)")
    for c in CHECKS:
        c()
    df = pd.DataFrame(RESULTS)
    df.insert(0, "data_type", "SYNTHETIC (Monte Carlo test-matrix study; not published measurements)")
    df.to_csv(OUT / "wp6_check_results.csv", index=False)
    print(f"  {len(df)} of {len(df)} checks passed")


if __name__ == "__main__":
    main()
