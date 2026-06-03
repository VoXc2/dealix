# Approval Gates

What requires a human (founder) decision before it can happen. Everything in this
list defaults to `requires_approval=true`, `dry_run=true`, `send_enabled=false`.

---

## Always-gated actions

| Action | Gate | Approver | Enforced by |
|--------|------|----------|-------------|
| Send any external message (email / WhatsApp) | A4 + approval | Founder | `safety_gate.py`, `test_governance_data.py` |
| Final pricing / quote | A4 + approval | Founder | `approval_item.schema.json` (risk=high) |
| Discount beyond published range | A4 + approval | Founder | `PRICING_GUARDRAILS.md` |
| Payment link / invoice dispatch | A4 + approval | Founder | `payment_handoff.schema.json` |
| Contract / legal commitment | Human handoff | Founder + review | `approval_gates.md` |
| Named case study | Written permission | Founder + client | `untrusted_input_policy.md` |
| Partner revenue-share agreement | A4 + approval | Founder | — |
| Processing client PII / CRM data | PDPL check | Founder + checklist | `pdpl_checklist.md` |
| Production deploy / secret change | Human only | Founder | `agent_permissions.md` |

---

## Approval levels (pricing & quotes)

| Level | Trigger | Approver |
|-------|---------|----------|
| L1 | Within published range | Founder (fast) |
| L2 | Discount < 15% | Founder |
| L3 | Discount ≥ 15% | Founder + reason logged |
| L4 | Custom / enterprise quote | Founder + 24h cooling |
| L5 | Legal / sensitive contract | Founder + review |

---

## Approval workflow

```
AI drafts (A2)  →  staged in approval_queue (A3)  →  human reviews
      → approve  →  execute the specific action (A4)  →  log in ai_action_ledger
      → reject   →  revise or discard
```

## Human-handoff triggers (never AI-only)

Complaints · sensitive data · low confidence · pricing finalization · legal issues ·
privacy/deletion requests · payment disputes.

---

## Invariants (checked in CI)

- No `outreach_message` is missing `requires_approval=true`.
- No `pricing_offer` / `payment_handoff` / `contract` is `risk != high`.
- No item is `approved=true` without a `reviewed_by` human.
- No suppressed recipient appears in any outbound item.

---

*Version 1.0 | 2026-06-03 | Enforced via `scripts/safety_gate.py` + `tests/`*
