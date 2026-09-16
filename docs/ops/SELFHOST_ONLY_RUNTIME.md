# Dealix self-host-only runtime authority

Dealix production runtime, build, release, database, ingress, TLS, rollback, and scheduled company execution are server-owned.

Canonical production plane: `deploy/selfhost/compose.yml`.
Canonical public ingress: Caddy from `ops/caddy/Caddyfile`.
Canonical release identity: exact Git SHA injected into API and Web images.
Canonical scheduling: systemd timers on the Dealix VPS.

GitHub may remain a source-code remote/backup and collaboration surface, but GitHub Actions is not a runtime, CI, deployment, scheduling, or release dependency. The repository intentionally contains no `.github/workflows` directory.

Vercel and Railway are not production authorities and their provider configuration files are intentionally absent. Historical migration/verification material may mention a former provider only as provenance; it must never be required to build, boot, serve, schedule, back up, restore, or roll back current production.

Verification:

```bash
python3 scripts/ops/verify_selfhost_only_runtime.py
python3 scripts/ops/verify_selfhosted_production_plane.py
python3 scripts/ops/verify_selfhost_production_cutover_contract.py
```
