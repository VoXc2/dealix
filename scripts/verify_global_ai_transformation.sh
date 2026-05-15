#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="$(command -v python3)"

echo "== Verify transformation artifacts =="
"$PYTHON_BIN" scripts/verify_global_ai_transformation.py

echo "== Verify enterprise control plane baseline =="
bash scripts/verify_enterprise_control_plane.sh

echo "GLOBAL AI TRANSFORMATION: PASS"
