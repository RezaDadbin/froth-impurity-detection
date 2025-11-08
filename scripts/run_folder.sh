#!/usr/bin/env bash
set -euo pipefail
python -m froth_impurity.cli --folder "${1:-data/input}" --cfg "${2:-configs/default.yaml}"
