# Agent Governance Review

**Date:** 2026-06-03 · **Reviewer:** Security/QA Agent

## Summary
Agent governance moved from prose-only (`company_os/governance/agent_permissions.md`)
to a **code-backed, test-enforced** registry of **40 agents**
(`core/safety/permissions.py`). Docs are generated from that registry, so the
permission matrix cannot drift from what tests enforce.

## What was verified (via `tests/test_agent_permissions_market.py`)
- ✅ All 40 agents present with all required fields.
- ✅ Every agent carries the 8 global forbidden actions.
- ✅ No agent can perform any forbidden action (`can_perform` denies them).
- ✅ No agent sits at L6; permission/risk levels are valid.
- ✅ Send-related agents require approval.
- ✅ No agent may change workflow permissions.

## Open conflicts / risks
1. 🔴 **Duplicate governance tree.** `company_os/company_os/` duplicates
   `company_os/` but with **divergent** `agent_permissions.md` (5-level model
   vs the matrix elsewhere) and extra files (`scripts/`, `revenue/payments.csv`).
   - **Risk:** agents may read/modify the wrong copy; reviewers see conflicting rules.
   - **Action:** NOT auto-deleted (founder-authored). **Recommend** consolidating
     to `company_os/` and removing the nested copy — *founder decision required*.
2. 🟡 **Prose ↔ code mismatch.** The legacy doc uses Observe/Advise/Draft levels;
   the new L0–L6 matrix supersedes it. Recommend updating the legacy doc to
   point at `docs/agents/AGENT_PERMISSION_MATRIX_AR.md`.
3. 🟡 **Unauthenticated approval endpoint** (`api/governance-router.ts` `approve`
   uses `publicQuery`). Governance approvals must be authenticated. (See audit §18.)

## Recommendations
- Treat `core/safety/permissions.py` as the single source of truth.
- Run `python3 scripts/generate_agent_docs.py` in CI to keep docs in sync.
- Resolve the duplicate tree and the auth gap before any production use.
