#!/usr/bin/env bash
# Wrapper — use run_founder_commercial_day.sh as canonical (includes Business NOW).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec bash "$ROOT/scripts/run_founder_commercial_day.sh" --with-business-now "$@"
