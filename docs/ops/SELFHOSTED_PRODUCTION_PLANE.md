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

Railway PostgreSQL is a separate migration lane from Web/API cutover. Minimum proof before DB cutover:

- current provider backup captured without logging credentials using `scripts/ops/backup_postgres_snapshot.sh` or equivalent governed evidence;
- checksum verifies;
- `pg_restore --list` succeeds;
- isolated restore succeeds on a PostgreSQL image that supplies every required extension (including pgvector when the dump contains `vector`);
- structural checks succeed;
- the target production database and backup/restore schedule are defined;
- rollback/RPO are explicit.

A backup is evidence, not permission to restore into production.

## Public cutover gate

Only after exact private acceptance and an action-bound approval packet:

1. Prepare the self-host production runtime from the exact accepted SHA.
2. Keep Railway healthy as last-good while the new origin is staged.
3. Admit public ingress/TLS under its bounded production action.
4. Change Cloudflare/DNS origin under a separate exact mutation if required.
5. Verify public Web/API full SHA parity, health, critical routes, TLS, and observability.
6. Abort immediately to the Railway last-good path if any acceptance gate fails.
7. Soak before provider decommission.

## Commands

```bash
python scripts/ops/verify_selfhosted_production_plane.py
SHA=$(git rev-parse HEAD)
DEALIX_EXPECTED_SHA="$SHA" DEALIX_SELFHOST_API_PORT=18001 DEALIX_SELFHOST_WEB_PORT=13001 DEALIX_SELFHOST_LOCAL_DB=1 bash scripts/ops/deploy_selfhosted_canary.sh
DEALIX_EXPECTED_SHA="$SHA" DEALIX_SELFHOST_API_PORT=18001 DEALIX_SELFHOST_WEB_PORT=13001 DEALIX_SELFHOST_INGRESS_PORT=18081 bash scripts/ops/verify_selfhosted_ingress_canary.sh
```

## Single-plane public cutover controller

The same `deploy/selfhost/compose.yml` owns private canary, stage, and public ingress. There is no second runnable production Compose graph. `public-ingress` is a `public-cutover` profile whose default bindings are loopback-only (`127.0.0.1:18080/18443`).

Source preflight (safe, no public bind):

```bash
DEALIX_EXPECTED_SHA="$(git rev-parse HEAD)" bash scripts/ops/selfhost_public_cutover.sh --preflight
```

`--stage` additionally requires `DEALIX_STAGE_PRODUCTION=YES` and `CONFIRM_SHA=<exact accepted SHA>`. `--cutover` additionally requires `DEALIX_PUBLIC_CUTOVER=YES`; only that path replaces the safe loopback defaults with `0.0.0.0:80/443`. Running either material mode remains an exact action-bound L5 operation. The controller never mutates DNS or decommissions Railway, and it reports `PRODUCTION_GREEN=NOT_PROVEN` until public parity is independently proven.

## Definition of done

`SOURCE SHA = BUILT SHA = RUNNING WEB SHA = RUNNING API SHA`, plus health, critical routes, TLS, backup/restore, rollback, and public release receipt.

Until every term is proven, report `PRODUCTION_GREEN=NOT_PROVEN`.
