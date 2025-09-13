#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r src/validator/requirements.txt
python src/validator/validate_contract.py --contract contracts/dataset_contract.yaml --data bq/sample/curated.csv --out artifacts
