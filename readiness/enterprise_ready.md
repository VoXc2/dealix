# Enterprise Ready

**Status: NOT YET REACHED.** This file states the exit criteria.

Dealix is Enterprise Ready when the Client Pilot gate
(`readiness/client_pilot_ready.md`) holds for **3 live customers** AND:

| Criterion | Required | Current |
|---|---|---|
| `verify_enterprise_control_plane.sh` green | yes | PASS |
| 3 customers with assembled Proof Packs | 3 | 0 |
| Postgres-backed control ledgers (events, runs, tickets, value) | yes | in-memory / tenant-keyed |
| CI blocks releases on a red control-plane gate | yes | workflow added — needs branch protection |
| Per-tenant policy overrides | yes | policies system-wide |
| Observability: trace per run/action/tool | yes | run trace via evidence_store; tool-level pending |

## Next steps (in order)

1. Postgres migrations + repository layer for the control ledgers.
2. Per-tenant policy registry.
3. Tool-level OpenTelemetry trace coverage.
4. Run the pilot with 3 customers; assemble Proof Packs.

Until every row is satisfied, Dealix markets only as **Client Pilot
Ready**, never "Enterprise Ready".
