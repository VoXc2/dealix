# Complete Agent Operating Model — Dealix

**Core principle:** _AI drafts. Human approves. System logs. Company learns._

This document defines how all Dealix agents operate together safely. It is the
narrative layer over the machine-enforced registry in
`core/safety/permissions.py` (rendered to `docs/agents/AGENT_ROLE_CATALOG_AR.md`
and `AGENT_PERMISSION_MATRIX_AR.md`, enforced by
`tests/test_agent_permissions_market.py`).

## 1. Operating posture

Every external-action surface defaults to:

```
dry_run = true · approval_required = true · send_enabled = false
```

Agents are organized as a pipeline with explicit handoffs and gates:

```
Sector Intel → Signal Detection → Prospect Research
      → Draft Factory → Personalization Guard → Compliance Gate
      → Deliverability → Approval Queue → (HUMAN APPROVES) → Sending Ramp
      → Reply Handling → WhatsApp Concierge → Client Assessment
      → Proposal → Proof Pack → (HUMAN) → Payment Handoff
      → Delivery Handoff → Customer Success → Renewal
Cross-cutting: Brand Guard · Privacy Guard · Security Red Team · QA/Eval ·
               Metrics · Finance · Legal/Compliance · Founder Command
```

## 2. Permission levels (L0–L6)

| Level | Meaning |
|-------|---------|
| L0 | Read only |
| L1 | Docs/reports only |
| L2 | Data/schema updates |
| L3 | Code changes in branch |
| L4 | Staging-only ops |
| L5 | Sensitive planning only |
| L6 | Forbidden autonomous action |

No agent operates above **L4** autonomously. Anything at L5/L6 is a *planning
artifact for the founder*, never an autonomous act.

## 3. Gates (hard stops)

1. **Personalization gate** — drafts below **P1** never become send-ready.
2. **Compliance gate** — no guaranteed claims, no fake subjects, no missing
   unsubscribe, no PII/secret leaks.
3. **Deliverability gate** — SPF/DKIM/DMARC + suppression + ramp verified.
4. **Approval gate** — a human records approval; agents cannot self-approve.
5. **Commercial gate** — proposal maps to catalog + qualified; final price &
   payment handoff need approval.
6. **Delivery gate** — won deals require delivery + CS handoff before work.
7. **Privacy/legal gate** — legal/complaint/privacy → human handoff.

## 4. Forbidden for every agent

`external_send`, `final_pricing`, `legal_commitment`, `bypass_suppression`,
`secrets_edit`, `production_deploy`, `workflow_permission_escalation`,
`treat_untrusted_as_instructions` (+ agent-specific extras in the registry).

## 5. Logging & review

- Every action → `company_os/governance/ai_action_ledger.jsonl`.
- Approvals/rejections → `company_os/governance/approval_queue.json`.
- Weekly governance review (`scripts/governance_check.py`) + security review.

## 6. Documents in this set

`AGENT_ROLE_CATALOG_AR.md` · `AGENT_PERMISSION_MATRIX_AR.md` ·
`AGENT_HANDOFF_PROTOCOL_AR.md` · `AGENT_COLLISION_POLICY_AR.md` ·
`AGENT_OUTPUT_CONTRACT_AR.md` · `MARKET_AGENT_*` · `COMMERCIAL_AGENT_*`.
