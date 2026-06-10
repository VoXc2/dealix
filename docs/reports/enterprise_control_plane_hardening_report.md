# Enterprise Control Plane Hardening Report

## What was already strong
- Systems 26–35 conceptual layers existed in architecture and docs.
- Control Plane and approval-first patterns existed.
- Agent governance primitives existed.
- Runtime safety and self-evolving guard patterns existed.

## What was broken
- Missing `governance_os.runtime_decision.decide` runtime implementation.
- Tenant scope was not consistently enforced across operational objects.
- Enterprise control-plane persistence tables were incomplete.
- No single E2E enterprise proof test and verify script.
- Missing dedicated enterprise release workflow.

## What was fixed
- Added `runtime_decision.decide` with risk-aware escalation behavior.
- Added tenant-aware repositories for control plane, agent mesh, assurance, runtime safety, value, self-evolving.
- Added Postgres migration for control-plane persistence tables.
- Added approval-gated rollback/policy edit and self-evolving apply gates.
- Added targeted enterprise tests, including end-to-end workflow proof.
- Added verification script and CI workflow for enterprise control-plane gate.
- Added minimal control surfaces scaffold in `apps/web`.

## What remains MVP
- In-memory repositories remain available for dev/test fallback.
- JSONL and non-Postgres legacy paths still exist outside control-plane modules.
- UI surfaces are minimal and meant for operator visibility bootstrap.
- Production deployment wiring for new tables still depends on env-specific rollout.

## Definition of Done
- `scripts/verify_enterprise_control_plane.sh` prints `ENTERPRISE CONTROL PLANE: PASS`.
