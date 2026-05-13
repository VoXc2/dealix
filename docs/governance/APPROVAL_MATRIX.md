# Approval Matrix — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [APPROVAL_MATRIX_AR.md](./APPROVAL_MATRIX_AR.md)

## Context
The Approval Matrix turns the operating belief "no approval, no
external action" into a hard runtime rule. It classifies every action
Dealix or its AI workforce performs into one of five classes and
defines who must approve and what evidence must be recorded before the
action is taken. The matrix is referenced by
`docs/DEALIX_OPERATING_CONSTITUTION.md`, by
`docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` (the L3 sibling defining
the human-in-the-loop pattern), and by
`docs/governance/RUNTIME_GOVERNANCE.md` which enforces it at runtime.

## Matrix
| Action class | Approver | Required evidence |
|---|---|---|
| Class A — Internal insight | None (logged) | Audit event |
| Class B — Client output | QA reviewer | QA score ≥ 85 |
| Class C — Internal change | Owner | Rollback plan |
| Class D — External communication | Owner + Delivery lead | Recipient list, consent, claims check |
| Class E — Autonomous external | BLOCKED | n/a |

## Class Definitions
- **Class A — Internal insight**. AI output consumed only by the
  Dealix team for analysis. Logged in the AI Run Ledger. No approval
  required; audit event is the only evidence.
- **Class B — Client output**. Any artifact delivered to a client:
  drafts, reports, dashboards, proof packs. Requires QA review per
  `docs/quality/QUALITY_STANDARD_V1.md`. QA score must be ≥ 85.
- **Class C — Internal change**. Configuration, prompt, schema, or
  workflow changes inside Dealix or inside a client tenant. Requires
  the owner's approval and a documented rollback plan.
- **Class D — External communication**. Any outbound message, email,
  API call, or post to a third-party system. Requires both the owner
  and the delivery lead. Evidence: recipient list, consent or
  relationship status per recipient, and a claims check confirming no
  forbidden claim (per `docs/governance/FORBIDDEN_ACTIONS.md`).
- **Class E — Autonomous external action**. Any external action taken
  by an AI agent without a human approver. Permanently blocked.

## Routing Rules
- Every workflow declares the action class it produces.
- If multiple action classes apply, the highest class governs.
- A Class B output addressed to a third party automatically promotes
  to Class D.
- A Class D action with a forbidden claim downgrades to BLOCK and is
  routed to the governance lead.

## Evidence Schema
Each approval is logged as an audit event with this shape:

```json
{
  "approval_id": "APV-001",
  "action_class": "D",
  "approver_ids": ["delivery_lead_01", "owner_07"],
  "evidence": {
    "recipient_list": "RCP-091",
    "consent_record": "CSN-014",
    "claims_check": "passed"
  },
  "ai_run_id": "AIR-2031",
  "decision": "APPROVED",
  "expiry": "2026-05-20T00:00:00Z"
}
```

Approvals expire. Class D approvals expire seven days after issuance
unless explicitly extended.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| AI run output | Approval request | AI platform lead | Per output |
| Approval request | Approval record | Approver | Per request |
| Approval record | Action release or block | Governance lead | Per request |
| Expiry timer | Approval revocation | Governance lead | Daily |

## Metrics
- **Approval coverage** — share of Class B-D actions with a logged
  approval. Target: 100%.
- **Approval latency** — hours between approval request and decision.
  Target: ≤ 24 hours for Class D.
- **Expired-approval misuse** — actions executed against an expired
  approval. Target: 0.

## Related
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — sibling human-in-
  the-loop pattern (L3).
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime enforcement.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution.
- `docs/governance/FORBIDDEN_ACTIONS.md` — forbidden-action register.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
