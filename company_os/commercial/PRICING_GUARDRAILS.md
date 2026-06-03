# Pricing Guardrails

Pricing is a **founder decision**. AI drafts ranges and anchors; it never finalizes a
price, sends a quote, or commits to terms.

---

## Hard rules

- Never quote a final price without founder approval.
- Never discount without a reason and (usually) a scope reduction.
- Never sell below the delivery-cost / margin floor.
- Never sell custom scope at a starter price.
- Never promise unlimited revisions.
- Always include **out of scope**.
- Always tie price to deliverables + timeline.
- Never tie price or discount to **guaranteed results** (forbidden claim).

---

## Approval levels

| Level | Trigger | Approver |
|-------|---------|----------|
| L1 | Within published range | Founder |
| L2 | Discount < 15% | Founder |
| L3 | Discount ≥ 15% | Founder + logged reason |
| L4 | Custom / enterprise quote | Founder + 24h cooling |
| L5 | Legal / sensitive contract | Founder + review |

> Repo baseline: the founder approves **all** pricing above 2,500 SAR (see
> `war_room/RISKS.md`, rule G003).

---

## Discounts

**Allowed for:** fast payment · pilot→retainer path · partner referral · case-study
permission · reduced scope.

**Not allowed for:** prospect hesitation · no scope reduction · below margin floor ·
anything tied to guaranteed results.

---

## Payment terms

| Offer type | Terms |
|------------|-------|
| Diagnostic / Sprint | Upfront |
| Workflow implementation | 50/50 or upfront |
| Retainer | Monthly upfront |
| Custom | Milestone-based |

Payment-link / invoice dispatch is a separate gate — always `requires_approval=true`
(`schemas/payment_handoff.schema.json`), never auto-sent, never stores card/secret
data.

---

*Version 1.0 | 2026-06-03 | Enforced via `approval_item.schema.json` (sensitive types must be risk=high) + `tests/test_governance_data.py`*
