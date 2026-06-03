#!/usr/bin/env bash
# Governed founder full autopilot — morning + evening check + weekly (Fri) + brief
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/run_founder_full_autopilot.py "$@"
