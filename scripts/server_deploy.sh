#!/usr/bin/env bash
set -Eeuo pipefail

cat >&2 <<'EOF'
SELFHOST_LEGACY_ENTRYPOINT=HOLD
scripts/server_deploy.sh is retired and non-authoritative.
Canonical source: deploy/selfhost/compose.yml
Verify: python scripts/ops/verify_selfhosted_production_plane.py
Private exact-SHA canary: DEALIX_EXPECTED_SHA=$(git rev-parse HEAD) bash scripts/ops/run_selfhosted_private_release_canary.sh
Public ingress/deploy, production DB restore, DNS, secrets, and provider decommission require exact action-bound L5 authority.
EOF
exit 78
