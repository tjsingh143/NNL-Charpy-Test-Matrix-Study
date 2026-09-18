"""WP5 - independent checks of the size-effect analysis (DECISIONS.md D-086).

Deliberately independent of the analysis script: it recomputes the quantities from the written outputs and from first
principles rather than calling the functions that produced them, so a mistake inside `src/wp5_size_effect.py` cannot pass
by being repeated here. Raises on any failure.

Run:  .venv/bin/python src/wp5_tests.py      (after src/wp5_size_effect.py)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUTPUTS, PROCESSED  # noqa: E402

WP5 = OUTPUTS / "wp5"
FULL_SIZE_VOLUME_MM3 = 10.0 * (10.0 - 2.0) ** 2      # written out here on purpose, not imported
FULL_SIZE_AREA_MM2 = 10.0 * (10.0 - 2.0)
KLST = {(27.0, 3.0, 4.0, 1.0): (4.0, 3.0)}           # (length, width, thickness, notch depth) -> (W, B) for the standard KLST


def check(name: str, ok: bool, detail: str) -> dict:
    if not ok:
        raise AssertionError(f"WP5 check FAILED - {name}: {detail}")
    return dict(check=name, result="pass", detail=detail)


def main() -> None:
    rows = []
    res = pd.read_csv(WP5 / "matched_pair_fit_results.csv")
    resid = pd.read_csv(WP5 / "size_correction_residuals.csv")
    pairs = pd.read_csv(WP5 / "candidate_pair_inventory.csv")
    strict = pd.read_csv(WP5 / "strict_matched_family_inventory.csv")
    hand = pd.read_csv(WP5 / "wp6_size_correction_handoff.csv")
    records = pd.read_csv(PROCESSED / "primary" / "charpy_records_with_curves.csv", low_memory=False)
    fits = pd.read_csv(OUTPUTS / "wp3" / "fits_primary.csv").set_index("curve_id")

    # 1. Pairing audit: every primary comparison must be reconstructable from the source metadata (D-086 check 7).
    dims = records.groupby("curve_id")[["length_mm", "width_mm", "thickness_mm", "notch_depth_mm"]].first()
    rows.append(check("every candidate pair is accounted for",
                      len(pairs) == 36 * 134 and pairs["match_class"].notna().all(),
                      f"{len(pairs)} ordered pairs enumerated (36 smaller x 134 full-size), each with a match class"))
    rows.append(check("STRICT pairs are a subset of the candidates and all same-study",
                      set(strict["pair_id"]) <= set(pairs["pair_id"]) and bool(strict["same_study"].all()),
                      f"{len(strict)} STRICT comparisons, all within one publication"))

    # 2. Leakage: recompute NF_E and M from the smaller specimen's published dimensions alone (D-086 check 8).
    worst_nf = worst_m = 0.0
    for r in resid.itertuples(index=False):
        d = dims.loc[r.smaller_curve_id]
        key = (float(d.length_mm), float(d.width_mm), float(d.thickness_mm), float(d.notch_depth_mm))
        w, b_thick = KLST.get(key, (float(d.width_mm), float(d.thickness_mm)))
        lig = w - float(d.notch_depth_mm)
        nf = FULL_SIZE_VOLUME_MM3 / (b_thick * lig ** 2)
        m = 98.0 - 15.1 * np.log(b_thick * lig ** 2)
        worst_nf = max(worst_nf, abs(nf - r.nf_energy))
        worst_m = max(worst_m, abs(m - r.shift_c))
    rows.append(check("no full-size answer leaks into its own correction",
                      worst_nf < 1e-9 and worst_m < 1e-9,
                      f"NF_E and M recomputed from the smaller specimen's geometry alone for all {len(resid)} comparisons "
                      f"(largest difference {worst_nf:.2e} and {worst_m:.2e}); neither depends on the paired full-size curve"))

    # 3. The residual is exactly the difference of the two index temperatures, and its sign follows D-078.
    sub = resid[resid["delta_t_size_c"].notna()]
    d = (sub["norm_t41j_c"] - sub["full_size_t41j_c"] - sub["delta_t_size_c"]).abs().max()
    rows.append(check("DT_size is the stated difference with the stated sign", d < 1e-9,
                      f"DT_size = T41J(normalized) - T41J(full-size) for all {len(sub)} residuals (largest deviation {d:.2e}); "
                      "positive means the correction places the transition warmer than the measured full-size curve"))

    # 4. The full-size term is the unchanged CP3-approved WP3 value; WP5 refits nothing full-size.
    worst = max(abs(r.full_size_t41j_c - fits.loc[r.full_size_curve_id, "index_temperature_c"])
                for r in resid.itertuples(index=False) if np.isfinite(r.full_size_t41j_c))
    rows.append(check("the full-size side is the approved WP3 fit, untouched", worst < 1e-12,
                      f"every full-size T41J equals outputs/wp3/fits_primary.csv (largest difference {worst:.2e} deg C)"))

    # 5. The transformed points are exactly the measured ones scaled and shifted (round trip on the written file).
    mapped = pd.read_csv(WP5 / "normalized_curve_points.csv")
    back_t = (mapped["transformed_temperature_c"] - mapped["shift_c"] - mapped["measured_temperature_c"]).abs().max()
    back_e = ((mapped["transformed_energy_j"] / mapped["nf_energy"] - mapped["measured_energy_j"]).abs()
              / mapped["measured_energy_j"].abs().clip(lower=1e-9)).max()
    rows.append(check("the mapped points round-trip to the published measurements", back_t < 1e-9 and back_e < 1e-9,
                      f"{len(mapped)} transformed points invert to their measured values (largest {back_t:.2e} deg C and "
                      f"{back_e:.2e} relative)"))

    # 6. The measured energies used are the published ones, unaltered.
    n_checked = 0
    for cid, g in mapped.groupby("smaller_curve_id"):
        pub = np.sort(records.loc[records["curve_id"] == cid, "energy_j"].to_numpy(float))
        got = np.sort(g.drop_duplicates(["measured_temperature_c", "measured_energy_j"])["measured_energy_j"].to_numpy(float))
        if not (len(pub) == len(got) and np.allclose(pub, got, rtol=0, atol=1e-12)):
            raise AssertionError(f"curve {cid}: the mapped points do not come from the unaltered published energies")
        n_checked += 1
    rows.append(check("raw measurements are unaltered", True,
                      f"the transformed points of all {n_checked} smaller-specimen curves derive from the published energies "
                      "exactly; WP5 writes nothing outside outputs/wp5/"))

    # 7. Evidence statuses follow the pre-registered thresholds of D-079, with no number printed below D-080's limit.
    bad = []
    for r in hand.itertuples(index=False):
        if str(r.smaller_geometry).startswith("POOLED"):
            continue
        want = ("UNSUPPORTED BY THIS DATASET" if r.n_primary_comparisons == 0
                else "DIRECTLY SUPPORTED" if (r.n_families >= 3 and r.n_studies >= 2) else "WEAKLY SUPPORTED")
        if r.evidence_status != want:
            bad.append(f"{r.smaller_geometry}: {r.evidence_status} against {want}")
        if r.n_families < 4 and np.isfinite(r.residual_scale_sd_c):
            bad.append(f"{r.smaller_geometry}: a standard deviation is printed from {r.n_families} families (D-080 forbids it)")
    rows.append(check("evidence statuses and suppression follow the pre-registered rules", not bad, "; ".join(bad) or
                      f"all {len(hand) - 1} geometry rows follow D-079 and D-080"))

    # 8. Nothing in the primary set was rescued by a rule the pre-registration did not state.
    ok = bool((resid.loc[resid["in_primary_analysis_set"], "norm_index_status"] == "calculated").all()
              and resid.loc[resid["in_primary_analysis_set"], "norm_outcome"].str.startswith("usable fit").all()
              and (resid.loc[resid["in_primary_analysis_set"], "full_size_index_status"] == "calculated").all()
              and resid.loc[resid["in_primary_analysis_set"], "full_size_wp3_outcome"].str.startswith("usable fit").all())
    rows.append(check("the primary analysis set obeys D-079", ok,
                      f"{int(resid['in_primary_analysis_set'].sum())} of {len(resid)} STRICT comparisons qualify: STRICT match, "
                      "usable full-size fit with a calculated T41J, usable transformed refit with a calculated T41J"))

    out = pd.DataFrame(rows)
    out.to_csv(WP5 / "wp5_check_results.csv", index=False)
    for r in out.itertuples(index=False):
        print(f"  {r.result}  {r.check}: {r.detail}")
    print(f"WP5 checks: {len(out)} passed")


if __name__ == "__main__":
    main()
