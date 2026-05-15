# Enterprise Readiness Model

Three readiness tiers for the Dealix Enterprise Control Plane. A tier is
"reached" only when its proof artifact is green — not by file count or
by feeling.

## Tier 1 — Client Pilot Ready

The control plane is stable, tenant-aware, governed, and proven by an
end-to-end test.

- Proof: `bash scripts/verify_enterprise_control_plane.sh` → `PASS`.
- Reached: **yes** on the hardening branch.

## Tier 2 — Enterprise Ready

Tier 1 holding for 3 live customers, plus Postgres persistence and CI
blocking bad releases.

- Proof: Tier 1 green + Postgres-backed ledgers + 3 customer Proof Packs.
- Reached: **no** — persistence is in-memory/tenant-keyed this round
  (see scorecard "Postgres persistence: DEFERRED").

## Tier 3 — Mission Critical Ready

Tier 2 plus full observability trace coverage, frontend control
surfaces, and an incident-response runbook exercised at least once.

- Proof: Tier 2 green + trace coverage report + control UI in `frontend/`.
- Reached: **no**.

## Principle

"Reached" means the system is governed, measured, and auditable — not
that the AI merely responds. Each tier upgrades the *proof*, not the
prose.
