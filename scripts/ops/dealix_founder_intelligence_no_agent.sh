#!/usr/bin/env bash
set -Eeuo pipefail
REPO=${DEALIX_REPO:-/opt/dealix/workspace/dealix}
cd "$REPO"
SOURCE_SHA=$(git rev-parse HEAD 2>/dev/null || printf UNKNOWN)
export DEALIX_SOURCE_SHA="$SOURCE_SHA"
exec python3 scripts/ops/generate_founder_intelligence.py
