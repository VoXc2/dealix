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
python3 scripts/validate_commercialization.py
python3 scripts/validate_monetization.py
python3 scripts/validate_agent_profiles.py
python3 scripts/final_launch_verify.py
