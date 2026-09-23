"""Independent arithmetic and fresh-prefix checks for the bounded D-107 completion."""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd

from common import OUTPUTS
import wp6_checkpoint as CP
import wp6_experiment as E
import wp6_simulator as SIM
import wp6_stability as S


def rms(e):
    v = np.asarray(e, float)
    v = v[np.isfinite(v)]
    return float(np.sqrt(np.mean(v * v))) if len(v) else np.nan


def main():
    out = OUTPUTS / "wp6"
    rows = []

    def check(name, passed, detail):
        rows.append(dict(check=name, passed=bool(passed), detail=detail))
        if not passed:
            raise AssertionError(f"{name}: {detail}")

    cells = pd.read_csv(out / "cell_results.csv", float_precision="round_trip").fillna({"variant": ""})
    base = pd.read_csv(out / "paired_comparisons.csv", float_precision="round_trip").fillna({"variant": ""})
    selected = S.select_cells(cells, base)
    detail = pd.read_csv(out / "monte_carlo_stability_paired.csv", float_precision="round_trip")
    metrics = pd.read_csv(out / "monte_carlo_stability_cells.csv", float_precision="round_trip")
    check("selection and complete paired arms",
          len(selected) == 63 and selected.original_d107_subset.sum() == 11
          and len(detail) == 46 and len(metrics) == 63
          and set(detail.mini_cell_id) == set(selected.loc[selected.geom_code != "G0", "cell_id"]),
          "11 original miniature cells; 16 T1 pairs, 30 T3 pairs, 17 full-size arms")
    check("analytic crossing fixtures",
          S.crossing([5, 10], [2, -2]) == (7.5, 5., 10., "bracketed")
          and S.crossing([4, 6], [-2, -3])[-1] == "below grid",
          "independent hand-worked 7.5 crossing and below-grid case")

    arrays = {}
    for cid in selected.cell_id:
        name = hashlib.sha256(cid.encode()).hexdigest()[:16] + ".npz"
        with np.load(CP.checkpoint_root() / "stability" / name, allow_pickle=False) as z:
            arrays[cid] = {k: z[k] for k in ("errors", "deltas", "outcome_counts")}
        if len(arrays[cid]["errors"]) != 4000 or arrays[cid]["outcome_counts"].sum() != 4000:
            raise AssertionError(f"requested-replicate accounting: {cid}")
    check("requested-replicate accounting", True, "all 63 arms contain and account for 4000 programmes")

    for row in detail.itertuples():
        f, m = arrays[row.full_cell_id]["errors"], arrays[row.mini_cell_id]["errors"]
        fr, mr = rms(f), rms(m)
        diffs = [rms(f[ix]) - rms(m[ix]) for ix in np.array_split(np.arange(4000), 20)
                 if np.isfinite(f[ix]).any() and np.isfinite(m[ix]).any()]
        se = np.std(diffs, ddof=1) / np.sqrt(len(diffs))
        eligible_f, eligible_m = np.isfinite(f).mean() >= .95, np.isfinite(m).mean() >= .95
        delta, tau = fr - mr, max(2., .05 * min(fr, mr))
        label = ("INELIGIBLE" if not (eligible_f and eligible_m) else
                 "paired SE unreliable" if len(diffs) < 18 else
                 "MINIATURE WINS" if delta > max(tau, 3 * se) else
                 "FULL-SIZE WINS" if -delta > max(tau, 3 * se) else "PRACTICALLY TIED")
        if not (np.allclose([fr, mr, delta, tau, se],
                           [row.rmse_full_c_R4000, row.rmse_mini_c_R4000, row.delta_rmse_c_R4000,
                            row.tau_c_R4000, row.se_paired_c_R4000], rtol=0, atol=1e-10)
                and row.winner_R4000.startswith(label)
                and row.eligible_full_R4000 == eligible_f and row.eligible_mini_R4000 == eligible_m):
            raise AssertionError(f"independent paired decision: {row.mini_cell_id}")
    check("paired RMSE, batch SE, gates and labels", True,
          "all 46 pairs reconstructed directly from cached replicate errors without decision helpers")

    sample = detail[(detail.tier == "T1") & (detail.k_budget == 4)]
    sample = pd.concat([sample, detail[(detail.tier == "T3") & (detail.k_budget == 8)]
                        .sort_values("variant").groupby("strategy").head(1)])
    for row in sample.itertuples():
        f, m = arrays[row.full_cell_id]["errors"], arrays[row.mini_cell_id]["errors"]
        rng = np.random.default_rng(20260918)
        differences = []
        for _ in range(2000):
            ix = rng.integers(0, 4000, 4000)
            differences.append(rms(f[ix]) - rms(m[ix]))
        if not np.isclose(np.std(differences, ddof=1), row.se_paired_bootstrap_c_R4000,
                          rtol=0, atol=1e-10):
            raise AssertionError(f"independent paired bootstrap: {row.mini_cell_id}")
    check("paired-bootstrap SE cross-check", True,
          "8 representative pairs independently resampled jointly 2000 times")

    thresholds = pd.read_csv(out / "monte_carlo_stability_thresholds.csv", float_precision="round_trip")
    for row in thresholds.itertuples():
        g = detail[(detail.tier == row.tier) & (detail.strategy == row.strategy)].copy()
        if row.tier == "T3":
            g = g[g.k_budget == row.k_budget]
            g["axis"] = g.variant.str.split("=").str[-1].astype(float)
        else:
            g["axis"] = g.k_budget
        g = g.sort_values("axis")
        x = g.axis.to_numpy()
        for suffix in ("R1000", "R4000"):
            y = g["delta_rmse_c_" + suffix].to_numpy()
            indices = np.flatnonzero((y[:-1] > 0) & (y[1:] <= 0))
            if len(indices):
                j = indices[0]
                value = np.interp(0., y[j:j + 2][::-1], x[j:j + 2][::-1])
                status = "bracketed"
            else:
                value = np.nan
                status = "below grid" if (y < 0).all() else "above grid" if (y > 0).all() else "unresolved"
            labels = g["winner_" + suffix].to_numpy()
            practical = [[float(x[j]), float(x[j + 1]), labels[j], labels[j + 1]]
                         for j in np.flatnonzero(labels[:-1] != labels[1:])]
            if (not np.isclose(value, getattr(row, "value_" + suffix), equal_nan=True, atol=1e-10, rtol=0)
                    or status != getattr(row, "status_" + suffix)
                    or practical != json.loads(getattr(row, "practical_brackets_" + suffix))):
                raise AssertionError(f"Independent crossing/bracket: {row.tier}, {row.strategy}, {suffix}")
    check("numerical thresholds and practical flip brackets", len(thresholds) == 12,
          "all 4 budget and 8 SD crossings/brackets reconstructed from paired values with independent interpolation")

    # The same indexed noise stream is checked directly; the four original-strategy pairs also
    # get fresh computations in reversed order and on a different worker count from the R=4000 run.
    tiny = selected[(selected.tier == "T1") & (selected.k_budget == 4)].copy()
    tiny["replicates"] = 8
    tiny["crn_stream"] = tiny.crn_stream + "|stability-4000"
    fresh = E.run_grid(tiny.iloc[::-1], workers=1, use_cache=False)
    for row in tiny.itertuples():
        for key in ("errors", "deltas"):
            if not np.array_equal(fresh[row.cell_id][key], arrays[row.cell_id][key][:8], equal_nan=True):
                raise AssertionError(f"fresh reversed/one-worker prefix: {row.cell_id}, {key}")
    index = selected.set_index("cell_id")
    for row in detail.itertuples():
        a, b = index.loc[row.full_cell_id], index.loc[row.mini_cell_id]
        if a.crn_stream != b.crn_stream:
            raise AssertionError("paired stream mismatch")
        stream = a.crn_stream + "|stability-4000"
        hashed = lambda text: int(hashlib.sha256(text.encode()).hexdigest()[:15], 16)
        x = np.random.default_rng(np.random.SeedSequence(
            [20260918, hashed(stream), hashed("noise"), 3999])).normal(size=8)
        y = SIM.replicate_rng(b.crn_stream + "|stability-4000", "noise", 3999).normal(size=8)
        if not np.array_equal(x, y):
            raise AssertionError("paired replicate stream mismatch")
    check("fresh deterministic prefixes and paired streams", True,
          "8 arms x 8 programmes recomputed in reverse order with one worker; replicate 3999 seed reconstructed independently")
    pd.DataFrame(rows).to_csv(out / "stability_check_results.csv", index=False)
    print(f"D-107 implementation checks: {len(rows)} passed. Stability outcomes are reported separately.")


if __name__ == "__main__":
    main()
