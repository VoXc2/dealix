# Security — Rollback

## Blast radius

Risk tier **critical**. A failure here affects: enterprise_safe, governable.

## Procedure

1. Detect via the alerts in `observability.md`.
2. Freeze new traffic to this system (feature flag / route disable).
3. Roll the implementing modules back to the last known-good version
   (`releases/`, `versions/`, `auto_client_acquisition/enterprise_rollout_os`).
4. Re-run this system's `tests/` and Phase 1 evals before un-freezing.
5. Record the incident in `changelogs/` and `auto_client_acquisition/auditability_os`.

## Approval

Rollback of a **critical**-tier system is authorized by the system owner;
critical-tier rollbacks also notify the founder (humans above the loop).
