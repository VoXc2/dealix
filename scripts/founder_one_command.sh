#!/usr/bin/env bash
# Dealix founder — one command for maximum governed autonomous day (no external send).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
EXTRA=()
for arg in "$@"; do
  case "$arg" in
    --evening) EXTRA+=(--evening) ;;
    --weekly) EXTRA+=(--weekly) ;;
    --skip-commercial-day) EXTRA+=(--skip-commercial-day) ;;
    --dry-run) EXTRA+=(--dry-run) ;;
    -h|--help)
      echo "Usage: bash scripts/founder_one_command.sh [--evening] [--weekly] [--skip-commercial-day] [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown flag: $arg" >&2
      exit 2
      ;;
  esac
done
python3 scripts/run_dealix_complete_autonomous_day.py "${EXTRA[@]}"
