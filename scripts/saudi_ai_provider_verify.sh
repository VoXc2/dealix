#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 -m saudi_ai_provider verify
python3 scripts/validate_catalog.py
python3 scripts/validate_pricing.py
python3 scripts/validate_kpis.py
python3 scripts/validate_playbooks.py
python3 scripts/validate_governance.py
python3 scripts/validate_runtime.py
