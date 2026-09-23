"""Bounded paired completion of D-107; never replaces the accepted T1-T7 results.

The selection rule is recorded before this run in D-127. Existing independent-stream
miniature checkpoints are reusable; matching full-size arms use that same stream.
"""
from __future__ import annotations

import argparse
import json
import time

import numpy as np
import pandas as pd

import wp6_experiment as E


def select_cells(cells: pd.DataFrame, comparisons: pd.DataFrame) -> pd.DataFrame:
    """Original A5/G5 subset, adjacent flip endpoints, and padded SD* brackets.

    Selection depends only on the accepted R=1000 grid/results, never R=4000.
    One adjacent SD point on each side permits a small crossing displacement.
    """
    primary = set(E.stability_subset(cells, comparisons).cell_id)
    reasons = {cid: {"original D-107 subset"} for cid in primary}
    base = comparisons[(comparisons.archetype_id == "A5") & (comparisons.geom_code == "G5")]

    def add(rows, reason):
        for row in rows.to_dict("records"):
            reasons.setdefault(row["mini_cell_id"], set()).add(reason)
            reasons.setdefault(row["full_cell_id"], set()).add("paired full-size arm")

    add(base[base.mini_cell_id.isin(primary)], "original D-107 subset")
    for _, g in base[base.tier == "T1"].groupby("strategy"):
        g = g.sort_values("k_budget")
        for i in range(len(g) - 1):
            a, b = g.iloc[i], g.iloc[i + 1]
            if a.winner != b.winner or a.delta_rmse_c * b.delta_rmse_c <= 0:
                add(g.iloc[i:i + 2], "budget numerical/practical flip endpoints")
    sweep = base[base.tier == "T3"].copy()
    sweep["sd_c"] = sweep.variant.str.removeprefix("SD=").astype(float)
    for _, g in sweep.groupby(["strategy", "k_budget"]):
        g = g.sort_values("sd_c")
        for i in range(len(g) - 1):
            if g.iloc[i].delta_rmse_c > 0 >= g.iloc[i + 1].delta_rmse_c:
                add(g.iloc[max(0, i - 1):min(len(g), i + 3)], "SD* bracket plus adjacent points")
                break
        else:
            raise RuntimeError("Accepted A5/G5 SD* has no bracket")
    selected = cells[cells.cell_id.isin(reasons)].copy()
    selected["stability_reason"] = selected.cell_id.map(lambda x: "; ".join(sorted(reasons[x])))
    selected["original_d107_subset"] = selected.cell_id.isin(primary)
    return selected


def crossing(x, delta):
    """First positive-to-nonpositive RMSE crossing and its enclosing grid interval."""
    x, delta = np.asarray(x, float), np.asarray(delta, float)
    for i in range(len(x) - 1):
        if delta[i] > 0 >= delta[i + 1]:
            value = x[i] + (x[i + 1] - x[i]) * delta[i] / (delta[i] - delta[i + 1])
            return float(value), float(x[i]), float(x[i + 1]), "bracketed"
    status = "below grid" if np.all(delta < 0) else "above grid" if np.all(delta > 0) else "unresolved"
    return np.nan, np.nan, np.nan, status


def practical_brackets(g: pd.DataFrame, axis: str) -> str:
    g = g.sort_values(axis)
    return json.dumps([[float(a[axis]), float(b[axis]), a["winner"], b["winner"]]
                       for a, b in zip(g.to_dict("records"), g.to_dict("records")[1:])
                       if a["winner"] != b["winner"]])


def threshold_comparison(old: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tier, keys, axis in [("T1", ["strategy"], "k_budget"),
                             ("T3", ["strategy", "k_budget"], "sd_c")]:
        a, b = old[old.tier == tier].copy(), new[new.tier == tier].copy()
        if tier == "T3":
            for t in (a, b):
                t[axis] = t.variant.str.removeprefix("SD=").astype(float)
        for key, g in a.groupby(keys):
            key = key if isinstance(key, tuple) else (key,)
            h = b
            for field, value in zip(keys, key):
                h = h[h[field] == value]
            g, h = g.sort_values(axis), h.sort_values(axis)
            ca, lo, hi, sa = crossing(g[axis], g.delta_rmse_c)
            cb, lob, hib, sb = crossing(h[axis], h.delta_rmse_c)
            movement = abs(cb - ca) if np.isfinite(ca) and np.isfinite(cb) else np.nan
            stable = (movement < hi - lo) if np.isfinite(movement) else sa == sb and sa != "unresolved"
            joined = g.set_index("mini_cell_id").join(h.set_index("mini_cell_id"), lsuffix="_old", rsuffix="_new")
            rmse_change = (joined.delta_rmse_c_new - joined.delta_rmse_c_old).abs()
            within_tau = bool((rmse_change < joined.tau_c_old).all())
            practical_old, practical_new = practical_brackets(g, axis), practical_brackets(h, axis)
            rows.append(dict(data_type=E.DATA_TYPE, tier=tier, strategy=key[0],
                             k_budget=key[1] if tier == "T3" else np.nan,
                             quantity="flip budget" if tier == "T1" else "correction SD* (deg C)",
                             value_R1000=ca, value_R4000=cb, absolute_movement=movement,
                             bracket_low_R1000=lo, bracket_high_R1000=hi,
                             bracket_low_R4000=lob, bracket_high_R4000=hib,
                             status_R1000=sa, status_R4000=sb,
                             movement_less_than_grid_spacing=bool(stable),
                             max_paired_delta_change_c=float(rmse_change.max()),
                             paired_delta_changes_below_tau=within_tau,
                             numerical_crossing_criterion_met=bool(stable or within_tau),
                             practical_brackets_R1000=practical_old,
                             practical_brackets_R4000=practical_new,
                             practical_brackets_unchanged=practical_old == practical_new))
    return pd.DataFrame(rows)


def summary_text(result: dict) -> str:
    p, t = result["pairs"], result["thresholds"]
    t1, t3 = p[p.tier == "T1"], p[p.tier == "T3"]
    original = p[p.original_d107_subset]
    changed = p[~p.winner_unchanged]
    changes = "; ".join(f"{r.tier} {r.strategy}, k={r.k_budget}, {r.variant}: "
                        f"{r.winner_R1000} -> {r.winner_R4000}" for r in changed.itertuples()) or "none"
    edge = t[(t.tier == "T1") & (t.status_R1000 != t.status_R4000)]
    edge_text = "; ".join(f"{r.strategy}: {r.status_R1000} -> {r.value_R4000:.6f} "
                         f"({r.status_R4000})" for r in edge.itertuples()) or "none"
    conclusion = ("CENTRAL labels are unchanged." if t1.winner_unchanged.all()
                  else "CENTRAL labels changed: author review is required before further work.")
    return (f"Paired Monte Carlo stability completion (D-127): {len(result['cells'])} arms at R = 4,000 on the "
            f"independent stability stream; {len(t1)} CENTRAL A5/G5 pairs and {len(t3)} supplemental T3 pairs. "
            f"Changed CENTRAL labels: {int((~t1.winner_unchanged).sum())} (original D-107 subset: "
            f"{int((~original.winner_unchanged).sum())} of {len(original)}). Changed supplemental labels: "
            f"{int((~t3.winner_unchanged).sum())}. Eligibility changes: {int((~p.eligibility_unchanged).sum())}.\n\n"
            f"Label changes: {changes}. The eight SD* estimates move by at most "
            f"{t.loc[t.tier == 'T3', 'absolute_movement'].max():.3f} deg C; "
            f"{int(t.loc[t.tier == 'T3', 'movement_less_than_grid_spacing'].sum())} of 8 are within their grid spacing. "
            f"Budget-crossing boundary changes: {edge_text}. All paired RMSE-difference movements are below "
            f"their original tau: {bool(p.within_tau.all())}; the maximum is "
            f"{p.delta_rmse_change_c.abs().max():.3f} deg C. {conclusion} "
            f"Every tested label unchanged: {bool(p.winner_unchanged.all())}. "
            "Accepted R = 1,000 results and thresholds are not replaced.\n\n"
            "See monte_carlo_stability_selection.csv, monte_carlo_stability_cells.csv, "
            "monte_carlo_stability_paired.csv and monte_carlo_stability_thresholds.csv for the exact arms, "
            "paired batch and bootstrap SEs, availability, labels and numerical/practical brackets. "
            "The original monte_carlo_stability.csv remains the eleven-arm single-arm RMSE diagnostic; "
            "it did not by itself verify paired labels.")


def run(cells: pd.DataFrame, comparisons: pd.DataFrame, workers=None) -> dict:
    """Run only the declared verification cells and emit separately named audit tables."""
    selected = select_cells(cells, comparisons)
    selected.to_csv(E.OUT / "monte_carlo_stability_selection.csv", index=False)
    big_grid = selected.copy()
    big_grid["replicates"] = E.STABILITY_REPLICATES
    big_grid["crn_stream"] = big_grid.crn_stream + "|stability-4000"
    big = E.run_grid(big_grid, workers=workers, progress_every=2, cache_subdir="stability")
    metrics = E.cell_results_table(big_grid, big)
    paired = E.paired_comparisons(metrics, big)
    if set(paired.mini_cell_id) != set(selected.loc[selected.geom_code != "G0", "cell_id"]):
        raise RuntimeError("A stability miniature arm lacks its full-size comparator")
    by_id = big_grid.set_index("cell_id")
    for row in paired.itertuples():
        if by_id.loc[row.full_cell_id, "crn_stream"] != by_id.loc[row.mini_cell_id, "crn_stream"]:
            raise RuntimeError("Stability arms do not share the same CRN stream")
        if row.n_paired_replicates != E.STABILITY_REPLICATES:
            raise RuntimeError("Stability comparison does not contain the complete shared R=4000 indices")
    old = comparisons[comparisons.mini_cell_id.isin(paired.mini_cell_id)].copy()
    fields = ["mini_cell_id", "full_cell_id", "rmse_full_c", "rmse_mini_c", "delta_rmse_c", "tau_c",
              "se_paired_c", "se_paired_bootstrap_c", "batches_used", "batches_dropped", "winner",
              "availability_full", "availability_mini", "eligible_full", "eligible_mini", "n_paired_replicates"]
    detail = old[fields].merge(paired[fields], on=["mini_cell_id", "full_cell_id"],
                              suffixes=("_R1000", "_R4000"), validate="one_to_one")
    metadata = selected.rename(columns={"cell_id": "mini_cell_id"})[
        ["mini_cell_id", "tier", "variant", "archetype_id", "geom_code", "strategy", "k_budget",
         "original_d107_subset", "stability_reason"]]
    detail = metadata.merge(detail, on="mini_cell_id", validate="one_to_one")
    detail.insert(0, "data_type", E.DATA_TYPE)
    detail["winner_unchanged"] = detail.winner_R1000 == detail.winner_R4000
    detail["eligibility_unchanged"] = ((detail.eligible_full_R1000 == detail.eligible_full_R4000)
                                        & (detail.eligible_mini_R1000 == detail.eligible_mini_R4000))
    detail["delta_rmse_change_c"] = detail.delta_rmse_c_R4000 - detail.delta_rmse_c_R1000
    detail["within_tau"] = detail.delta_rmse_change_c.abs() < detail.tau_c_R1000
    detail.to_csv(E.OUT / "monte_carlo_stability_paired.csv", index=False)
    thresholds = threshold_comparison(old, paired)
    thresholds.to_csv(E.OUT / "monte_carlo_stability_thresholds.csv", index=False)
    metrics.to_csv(E.OUT / "monte_carlo_stability_cells.csv", index=False)
    result = dict(pairs=detail, thresholds=thresholds, cells=metrics)
    (E.OUT / "monte_carlo_stability_summary.md").write_text(
        "# Bounded D-107 paired verification\n\n" + E.DATA_TYPE + "\n\n" + summary_text(result) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()
    start = time.time()
    cells = pd.read_csv(E.OUT / "cell_results.csv", float_precision="round_trip").fillna({"variant": ""})
    comparisons = pd.read_csv(E.OUT / "paired_comparisons.csv", float_precision="round_trip").fillna({"variant": ""})
    result = run(cells, comparisons, args.workers)
    t1 = result["pairs"].query("tier == 'T1'")
    print(f"Paired stability: {len(result['cells'])} arms, {len(result['pairs'])} pairs; "
          f"T1 changed labels: {int((~t1.winner_unchanged).sum())}; "
          f"elapsed {time.time() - start:.1f} s", flush=True)


if __name__ == "__main__":
    main()
