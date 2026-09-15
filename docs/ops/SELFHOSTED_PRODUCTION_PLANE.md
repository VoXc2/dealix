# Dealix Self-Hosted Production Plane

Goal: remove Railway as a required runtime dependency without weakening exact release identity, data safety, rollback, or L5 governance.

## Canonical authority

- GitHub is source/review/proof only.
- Dealix VPS is the build/runtime plane.
- `deploy/selfhost/compose.yml` is the single Compose authority.
- `docker-compose.prod.yml` and legacy `scripts/server_*` entrypoints are retired and intentionally fail closed.
- Runtime secrets stay outside Git in the governed host secret plane.
- Public ingress, DNS, production DB restore, secrets, and provider cancellation require exact action-bound L5 authority.

## Private acceptance

1. Resolve and freeze the exact candidate SHA.
2. Run `python scripts/ops/verify_selfhosted_production_plane.py`.
3. Build Web/API from that exact checkout.
4. Start loopback canaries using free `DEALIX_SELFHOST_API_PORT` and `DEALIX_SELFHOST_WEB_PORT` values.
5. Verify API `/version` and Web `/healthz` report the exact same full SHA.
6. If needed, bootstrap only the isolated canary Postgres profile; never mutate production DB here.
7. Run ingress canary on `DEALIX_SELFHOST_INGRESS_PORT` and verify host-based API/Web routing.
8. Assert this path did not bind public 80/443.

## Database exit gate

Railway PostgreSQL is a separate L5 lane from Web/API ingress. The canonical database target is the `production-db` profile in `deploy/selfhost/compose.yml`, under the stable Compose project `dealix-production`. It is PostgreSQL 18 + pgvector, password authenticated, and only binds PostgreSQL to loopback.

Required evidence order:

1. Capture a **fresh** Railway source backup with `scripts/ops/backup_postgres_snapshot.sh`, `DEALIX_BACKUP_ROLE=railway-source`, and the exact accepted release SHA. The runner fingerprints the database before and after `pg_dump`; any write during capture fails the backup.
2. Verify checksum and `pg_restore --list`, then restore that dump only into an isolated PostgreSQL 18 + pgvector scratch database.
3. Prepare the self-host production database with `selfhost_prepare_production_database.sh`. Its default is `--preflight`; `--execute` requires exact SHA confirmation and explicit production-DB authority.
4. Migrate only from the **restored backup**, never directly from Railway. `migrate_railway_backup_to_selfhost.py` rejects Railway/rlwy source hosts, makes the source read-only, requires exact backup/release provenance, preserves all legacy non-empty rows, and never infers publication consent.
5. Capture a post-migration `selfhost-target` backup and restore-list proof.
6. Immediately before public ingress, prove Railway quiescence: the live Railway database fingerprint must still equal the captured source fingerprint. The quiescence receipt expires after five minutes.
7. `verify_selfhost_cutover_receipts.py` must validate the complete receipt chain, row parity, exact release SHA, PG18+pgvector authority, artifact checksums, ordering, and TTLs.

A backup, migration receipt, or green canary is evidence only; none grants public cutover authority by itself.

## Public cutover gate

Only after exact private acceptance and the complete database receipt chain:

1. Stage Web/API from the exact accepted SHA with `selfhost_public_cutover.sh --stage`. Stage refuses Railway as the app database and verifies the live self-host DB Alembic head and migrated row counts against the production migration receipt.
2. Keep Railway serving public traffic as last-good while stage acceptance runs.
3. Capture the post-migration self-host backup and then a fresh Railway quiescence receipt.
4. Verify all cutover receipts before any public port is opened.
5. Under a separate exact L5 public-ingress action, run `--cutover`; only then may the canonical Caddy profile bind `0.0.0.0:80/443`.
6. DNS/Cloudflare origin mutation remains a separate exact L5 action. The controller deliberately reports `DNS_MUTATION=NOT_EXECUTED`.
7. After DNS, verify public Web/API full SHA parity, health, critical routes, TLS, observability, and rollback.
8. Soak on self-host while Railway remains recoverable.
9. Decommission Railway services and cancel billing only after public parity + data safety + rollback evidence are current. Provider decommission is never implied by source merge or ingress start.

## Commands

```bash
python scripts/ops/verify_selfhosted_production_plane.py
SHA=$(git rev-parse HEAD)
DEALIX_EXPECTED_SHA="$SHA" bash scripts/ops/run_selfhosted_private_release_canary.sh
```

## Single-plane public cutover controller

The same `deploy/selfhost/compose.yml` owns private canary, stage, and public ingress. There is no second runnable production Compose graph. `public-ingress` is a `public-cutover` profile whose default bindings are loopback-only (`127.0.0.1:18080/18443`).

Source preflight (safe, no public bind):

```bash
DEALIX_EXPECTED_SHA="$(git rev-parse HEAD)" bash scripts/ops/selfhost_public_cutover.sh --preflight
```

`--stage` additionally requires `DEALIX_STAGE_PRODUCTION=YES`, `CONFIRM_SHA=<exact accepted SHA>`, and a current production migration receipt whose Alembic head and migrated counts match the live self-host database. `--cutover` additionally requires `DEALIX_PUBLIC_CUTOVER=YES` plus fresh Railway-source, self-host-target, and quiescence receipts; `verify_selfhost_cutover_receipts.py` runs before the controller is allowed to replace the safe loopback defaults with `0.0.0.0:80/443`. Running either material mode remains an exact action-bound L5 operation. The controller never mutates DNS or decommissions Railway, and it reports `PRODUCTION_GREEN=NOT_PROVEN` until public parity is independently proven.

## Definition of done

`SOURCE SHA = BUILT SHA = RUNNING WEB SHA = RUNNING API SHA`, plus health, critical routes, TLS, backup/restore, rollback, and public release receipt.

Until every term is proven, report `PRODUCTION_GREEN=NOT_PROVEN`.
