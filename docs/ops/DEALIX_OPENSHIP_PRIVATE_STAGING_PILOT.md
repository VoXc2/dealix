# Dealix OpenShip Private Staging Pilot

Related: Issue #1171.

## Decision

Railway remains the production core. OpenShip is a private staging / preview pilot on the Dealix Command VPS.

This is not a production migration and not a second Company OS. GitHub remains the code source of truth; OpenShip is only a deployment-control surface.

The reviewed pilot pins the OpenShip CLI to `0.4.8`. The governed runtime script deliberately does **not** execute `get.openship.io`, `bun.sh/install`, or another mutable network installer. Installation is a separate operator prerequisite; the pilot verifies the exact CLI version before it can start.

## Why bare mode first

The Dealix VPS already runs Docker, Ollama, OpenClaw, n8n, Tailscale, and the Company Autopilot. On Linux with Docker, OpenShip can otherwise default to a Compose stack that includes Postgres, Redis, API, dashboard, a host-network edge on ports 80/443, and host Docker-socket access.

The first Dealix pilot therefore forces `openship up --bare` to reduce blast radius and prevent the pilot from taking ownership of 80/443 or the host Docker socket through the full Compose deployment plane.

OpenShip can choose alternate control-plane ports when its defaults are occupied. Dealix deliberately refuses that fallback in this tranche: ports 3001 and 4000 must be completely free before start, and after start the pilot requires those exact ports to be bound only to loopback (`127.0.0.1`/`::1`) and owned by the `dealix` OS account. This keeps the dashboard/API/MCP network proof deterministic and auditable.

## Fixed safety boundary

The pilot does not authorize:

- Railway or Vercel production mutation;
- DNS/domain changes;
- attaching `dealix.me`;
- copying production database credentials or secrets;
- external customer email/WhatsApp/LinkedIn sends;
- publishing;
- payment/refund/live checkout;
- destructive database or customer-data deletion.

Merge to `main` remains a separate source-control release decision and does not itself authorize any production mutation.

## Runtime prerequisites

Before starting OpenShip:

1. The canonical Dealix repository exists at `/opt/dealix/workspace/dealix`.
2. The VPS has at least 6 GiB `MemAvailable` by default.
3. Ports 3001 and 4000 are completely free. Dealix refuses OpenShip dynamic-port fallback and then requires those exact ports to bind loopback-only (`127.0.0.1`/`::1`).
4. Existing 80/443 listeners are inventory only; the pilot never takes ownership of them.
5. OpenClaw/Hermes/Company Autopilot remain independent execution surfaces and must not be replaced by OpenShip.
6. OpenShip CLI `0.4.8` is already installed for the `dealix` OS user. The governed pilot verifies this exact version and fails closed otherwise.

## Commands

The governed runner is:

```bash
sudo bash scripts/ops/dealix_openship_private_pilot.sh preflight
sudo bash scripts/ops/dealix_openship_private_pilot.sh install
sudo bash scripts/ops/dealix_openship_private_pilot.sh start
sudo bash scripts/ops/dealix_openship_private_pilot.sh status
sudo bash scripts/ops/dealix_openship_private_pilot.sh mcp-guard
sudo bash scripts/ops/dealix_openship_private_pilot.sh synthetic-scaffold
sudo bash scripts/ops/dealix_openship_private_pilot.sh stop
```

`install` is intentionally verification-only: it confirms the pinned prerequisite rather than downloading or executing an installer.

One bounded first-cycle command is also available:

```bash
sudo bash scripts/ops/dealix_openship_private_pilot.sh full-private-pilot
```

It performs only:

- resource/network preflight;
- exact pinned CLI verification;
- private bare-mode control-plane start;
- CLI + direct API health acceptance;
- deterministic loopback-port acceptance on 3001/4000 plus process-owner proof;
- explicit anonymous MCP authentication-denial guard (`401`/`403` only);
- disposable root-staged synthetic-app scaffold;
- proof manifest.

A startup timeout is never accepted from listener presence alone. A timeout may proceed only to strict readiness verification; unhealthy or ambiguous status triggers a verified stop. Transport errors or ambiguous MCP statuses also trigger a verified stop.

It intentionally does **not** initialize or deploy a real project.

## Proof

Each run writes under:

```text
/opt/dealix/executive-proof/openship/<mode>-<timestamp>/
```

Proof includes the current Dealix repository head/branch, memory/swap/disk state, important listeners, OpenShip status and direct health output, network ownership, MCP guard result, rollback evidence when applicable, and a SHA-256 manifest.

## MCP policy

OpenShip exposes an MCP endpoint for agent operations. Dealix must not provide an unrestricted admin token to Hermes/OpenClaw or another model.

The initial policy is:

1. anonymous MCP access must return an explicit authentication denial (`401` or `403`); transport failures, redirects, server errors, or success all fail acceptance;
2. create the first OpenShip admin through the private dashboard only after the control plane is proven private;
3. if an agent token is later created, scope it to read-only project/deployment/log inspection first;
4. any future deploy permission is staging-only and remains subject to Dealix approval rules;
5. no production secret may be stored in an agent-visible prompt or proof log.

## Synthetic phase

The script creates a unique disposable fixture under:

```text
/opt/dealix/openship-pilot/synthetic-app-<timestamp>
```

The fixture is assembled inside a root-owned temporary directory and atomically published before ownership is transferred to `dealix`, preventing rerun symlink overwrite races. It contains no customer data, production URL, production database, or secret. Deployment is deliberately a later acceptance step after private admin/context setup is verified.

## Promotion criteria

OpenShip may become a permanent Dealix staging plane only after a disposable project proves:

- build success;
- private health check;
- log retrieval;
- deterministic redeploy;
- rollback;
- acceptable resource footprint;
- clean failure handling;
- zero production/customer secrets;
- no regression to OpenClaw, Ollama, n8n, or Company Autopilot.

Only after that may Dealix prepare a private staging deployment. Railway remains production until a separate, explicit migration decision is made.

## Rollback

The immediate pilot rollback is:

```bash
sudo bash scripts/ops/dealix_openship_private_pilot.sh stop
```

`stop` is not allowed to report success until the command returns successfully and the OpenShip control listeners have disappeared within the bounded shutdown window.

No production/domain/database rollback is needed because this tranche never mutates those surfaces.
