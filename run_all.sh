#!/usr/bin/env bash
# Regenerate every output of this repository from the vendored raw data.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install --quiet -r requirements.txt
fi

# Refuse to run with package versions other than the pinned ones (DECISIONS.md D-002).
.venv/bin/python - <<'EOF'
import importlib.metadata as md, pathlib, sys
bad = []
for line in pathlib.Path("requirements.txt").read_text().splitlines():
    line = line.split("#")[0].strip()
    if "==" in line:
        name, version = line.split("==")
        if md.version(name) != version:
            bad.append(f"{name} {md.version(name)} (pinned {version})")
if bad:
    sys.exit("Package versions differ from requirements.txt: " + ", ".join(bad))
EOF

.venv/bin/python src/wp0_data_dictionary.py                      # WP0 (also verifies checksums)
.venv/bin/python src/wp1_clean.py                                # WP1, primary dataset (Materials Cloud 2025.30)
.venv/bin/python src/wp1_clean.py --dataset eny5v-www93          # WP1, version-sensitivity dataset (2024.206)
.venv/bin/python src/wp2_curves.py                               # WP2, both releases, version comparison, example figure
.venv/bin/python src/wp3_validation.py                           # WP3 fitter validation on SYNTHETIC curves: pre-registered lower-shelf rule
                                                                 # (Block L); final method and all-fitted sensitivity case (Blocks A-E); minutes
.venv/bin/python src/wp3_fit_curves.py                           # WP3 fits to the published data of the CP2-frozen cohorts: final primary method
                                                                 # (full-size LSE 2.7 J, miniature LSE fitted; D-042) and all-fitted sensitivity case
.venv/bin/python src/wp4_validation.py                           # WP4 SYNTHETIC checks of the bootstrap: zero scatter, determinism, failure
                                                                 # accounting, coverage of WP3 scenarios (D-060); 47-60 min measured with 3 workers
.venv/bin/python src/wp4_uncertainty.py                          # WP4 per-curve bootstrap uncertainty of the 170 primary curves: pairs (primary) and
                                                                 # fixed-design wild (sensitivity), B = 2,000 each; stability, scatter, cross-check; 41-76 min measured
.venv/bin/python src/wp5_pairs.py                                # WP5 specimen-size pair inventory: which published curves are genuinely the same material and
                                                                 # condition at two specimen geometries, and the data-sufficiency assessment (D-068 to D-071); seconds
.venv/bin/python src/wp5_size_effect.py                          # WP5 classical size normalization of the matched pairs, residual DT_size, sensitivities and the
                                                                 # WP6 handoff (D-072 to D-086); runs the normalization self-checks first; seconds
.venv/bin/python src/wp5_tests.py                                # WP5 independent checks: pairing audit, leakage, sign convention, round trip, raw-data
                                                                 # immutability and the pre-registered evidence thresholds (D-086); seconds
.venv/bin/python src/wp6_validation.py                           # WP6 simulator validation: 19 tests (zero scatter, estimator identity, no truth leakage,
                                                                 # raw-temperature feasibility, geometry equivalence and non-equivalence, single subtraction
                                                                 # of M, ...) plus the declared runtime/memory benchmark (D-111); 1-2 min of tests, plus 1.5-2.5 min of
                                                                 # benchmark on a cold cache (skipped on a warm one)
.venv/bin/python src/wp6_experiment.py                           # WP6 Monte Carlo test-matrix study: the frozen 6,188-cell grid T1-T7, the paired
                                                                 # comparisons, the correction-uncertainty threshold, the interval-coverage sub-study, the
                                                                 # stability subset, nine figures and wp6_summary.md; 381 min measured from a cold cache
                                                                 # with 3 workers on the 8 GB development Mac (6.4 h; a first
                                                                 # cold run took 389 min), peak memory 321 MB
                                                                 # WP6 reuses fingerprinted checkpoints in the git-ignored cache/wp6/, so a repeat run takes
                                                                 # about 1.5 min (measured 86 s); delete cache/wp6/ to force a full recomputation.
.venv/bin/python src/wp6_tests.py                                # WP6 independent checks: budget arithmetic, the nine-row geometry reconciliation, the
                                                                 # correction values and family pools read back at full precision, reachability, failure
                                                                 # accounting, clip fractions, the D-078 sign convention and that WP0-WP5 is untouched; seconds
.venv/bin/python src/wp7_report.py                               # WP7 report: substitutes every number from the regenerated tables, emits the
                                                                 # claim and constant source maps, and typesets report/charpy_test_matrix_study.pdf.
                                                                 # Fails on an unresolved, unused or stale placeholder, an unregistered literal
                                                                 # number, an untagged figure or table, or a forbidden phrase (D-113 to D-126); seconds
.venv/bin/python src/wp7_tests.py                                # WP7 independent checks of the built report: placeholders, claim-map re-reads,
                                                                 # figure digests, evidence classes, constant provenance, the honesty lint, the
                                                                 # README definition-of-done, and the PDF delivery-integrity text check; seconds
echo "All outputs regenerated."
