# Dealix Self-Hosted Production Plane

Goal: remove Railway as a required runtime dependency while preserving source truth, release identity, rollback, and database safety.

## Architecture

- GitHub: source/review/proof plane only.
- Dealix VPS: build + runtime execution plane.
- Docker Compose: Web/API orchestration.
- Existing reverse proxy or a separately admitted Caddy/Traefik layer: public TLS/routing.
- Runtime secrets: `/opt/dealix/control/secrets/*.env`, never committed.
- PostgreSQL: migrate only after a separate backup/restore rehearsal and explicit DB-cutover authority.

## Phases

1. Build exact-main Web/API images on the VPS.
2. Start private canaries on `127.0.0.1:13000` and `127.0.0.1:18000`.
3. Verify Web/API health and immutable Git SHA.
4. Keep Railway serving traffic during canary validation.
5. Reconcile the existing public reverse proxy and add self-host routes without deleting Railway routes first.
6. Run public smoke tests and release-parity checks.
7. Only after public parity is proven, remove Railway from the critical path.
8. Migrate PostgreSQL separately: backup -> restore rehearsal -> schema check -> controlled cutover -> rollback proof.

## Non-goals

- No blanket Railway staged-change acceptance.
- No DNS mutation from this repository runner.
- No secret copying into GitHub.
- No database mutation during Web/API canary startup.
- No claim of `PRODUCTION_GREEN` based only on HTTP 200.

## Commands

```bash
python scripts/ops/verify_selfhosted_production_plane.py
DEALIX_EXPECTED_SHA=$(git rev-parse HEAD) bash scripts/ops/deploy_selfhosted_canary.sh
```

The canary runner intentionally leaves public cutover and local PostgreSQL disabled.
