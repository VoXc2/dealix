# Compliance Guard Agent — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of AI / Head of Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [compliance_guard_agent_AR.md](./compliance_guard_agent_AR.md)

## Context
The Compliance Guard Agent is the runtime enforcer of Dealix's governance
rules. Every candidate output or queued action passes through this agent;
it returns a verdict that the workflow must honor. It implements the
runtime side of `docs/product/GOVERNANCE_AS_CODE.md` and the requirements
in `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Agent Card

- **Role:** Applies governance rules to outputs and queued actions.
- **Allowed Inputs:** candidate output, action class, source metadata,
  policy bundle id.
- **Allowed Outputs:** verdict — `allow` / `allow-with-review` /
  `require-approval` / `redact` / `block` / `escalate`.
- **Forbidden:** bypassing rules; modifying source; producing creative
  content; making revenue decisions.
- **Required Checks:**
  - policy bundle pinned by version;
  - decision trace included;
  - confidence reported;
  - escalations logged with reason.
- **Output Schema:** `GuardVerdict { decision, reasons[], policy_version,
  evidence_refs[], escalation }`.
- **Approval:** decisions are self-contained; humans handle escalations.

## Rule families enforced

- `no_cold_whatsapp` — block cold WhatsApp.
- `no_guaranteed_claims` — rewrite or block guaranteed-result language.
- `no_source_no_answer` — force "insufficient evidence" when needed.
- `pii_redaction_required` — redact or require lawful basis.
- `tenant_scope` — block cross-tenant access.

## Anti-patterns

- Returning a verdict without a reason or trace.
- Letting an output pass without checking the policy bundle version.
- Suppressing escalations.
- Using the agent for any task other than verdicts.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Candidate output | GuardVerdict | Compliance Guard | Per action |
| Action class metadata | Allow/Block decision | Workflow Agent | Per action |
| Escalations | Reviewer queue | Compliance owner | Continuous |

## Metrics
- Block Precision — % of blocks confirmed correct on review.
- Allow Recall — % of unsafe items that should have been blocked but were
  allowed (target = 0).
- Decision Latency — median ms per verdict.
- Escalation Volume — escalations per 1k actions.

## Related
- `docs/product/GOVERNANCE_AS_CODE.md` — runtime rules executed here
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval coverage
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — source of rules
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
