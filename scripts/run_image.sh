#!/usr/bin/env bash
set -euo pipefail
python -m froth_impurity.cli --image "${1:-data/input/sample.jpg}" --cfg "${2:-configs/default.yaml}"
