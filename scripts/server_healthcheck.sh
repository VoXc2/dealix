#!/usr/bin/env bash
set -Eeuo pipefail

cat >&2 <<'EOF'
SELFHOST_LEGACY_ENTRYPOINT=HOLD
scripts/server_healthcheck.sh targeted retired service names and is no longer authority.
Canonical verification: python scripts/ops/verify_selfhosted_production_plane.py
Canary release identity must prove the same exact Web/API SHA; HTTP 200 alone is insufficient.
Use docs/ops/SELFHOSTED_PRODUCTION_PLANE.md for the current acceptance order.
EOF
exit 78
