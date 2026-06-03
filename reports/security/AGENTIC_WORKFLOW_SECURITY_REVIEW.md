# Agentic Workflow Security Review — Findings (2026-06-03)

Applied the checklist in `docs/security/AGENTIC_WORKFLOW_SECURITY_REVIEW.md`.

| Check | Status | Note |
|-------|--------|------|
| Untrusted input = data | ✅ | `core/safety/untrusted.py` + tests |
| No secrets in prompts/logs/messages | ✅ | detectors + policy; `.env*` git-ignored |
| No external send w/o approval | ✅ | `send_enabled=false`; no sender code exists |
| No final pricing/legal by agent | ✅ | `core/safety/commercial.py` + tests |
| Suppression respected | ✅ | append-only `SuppressionList` |
| No workflow perm escalation | ✅ | new workflows `contents: read`; gate workflow greps for broad perms |
| No `pull_request_target` agent exec | ✅ | none added |
| Tests/evals green, not weakened | ✅ | 132 passed |
| Output contract present | ✅ | `docs/agents/AGENT_OUTPUT_CONTRACT_AR.md` |
| Collision policy followed | ✅ | duplicate tree flagged, not overwritten |

## Critical residual
🔴 **R1:** Approval endpoint unauthenticated (`api/governance-router.ts`). Recommend
`authedQuery`/`adminQuery`. Not changed at runtime (founder approval needed to
avoid breaking the app/frontend).

**Verdict:** Hardened to **approval-first / dry-run** posture. Cleared for
draft-and-review operation; not cleared for autonomous sending or production.
