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
echo "All outputs regenerated."
