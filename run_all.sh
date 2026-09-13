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
.venv/bin/python src/wp3_validation.py                           # WP3 fitter validation on SYNTHETIC curves (about 5 minutes)
.venv/bin/python src/wp3_fit_curves.py                           # WP3 fits to the published data of the CP2-frozen cohorts
echo "All outputs regenerated."
