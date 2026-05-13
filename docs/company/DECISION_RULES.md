# Dealix Decision Rules

The 6 binding rules. Each Monday in the operating cadence, the CEO confirms
no rule is violated this week. Violations are escalated within 24 hours.

## Rule 1 — Do not sell what is not ready

A service is **Sellable** only if it scores ≥ 85 on all of:
- Offer Readiness
- Delivery Readiness
- Demo Readiness
- Sales Readiness

AND **Governance Readiness ≥ 90** (governance has a higher bar by design).

If any threshold fails, the service is **Beta** (single-pilot only with explicit pilot framing) or **Not Ready** (cannot be sold, cannot be advertised).

## Rule 2 — Beta services must be labeled

A Beta service is offered with:
- explicit "pilot" framing in writing
- discounted or fixed pilot price
- documented success criteria
- no commitment beyond the pilot

A Beta service does NOT appear in public offer pages.

## Rule 3 — No unsafe automation

Forbidden actions enforced by `dealix/trust/forbidden_claims.py` + `dealix/trust/approval_matrix.py`:

- Scraping without explicit permission.
- Cold WhatsApp / SMS outreach.
- LinkedIn automation.
- Fabricated proof or testimonials.
- Guaranteed-outcome claims ("نضمن", "100%", "best in", "risk-free").
- PII in logs.
- External communication or system writes without human approval.

A violation here triggers immediate revert + Friday QA-board review.

## Rule 4 — No report without next action

Every client-facing report must contain, in this order:
1. What we found.
2. What it means.
3. What to do next (3–7 prioritized actions).
4. Proof Pack with measured impact.
5. Recommended next Dealix engagement.

Reports missing any of the above fail Delivery QA and do not ship.

## Rule 5 — Build after repetition

A capability is promoted from manual delivery to a product feature only when:
- the task repeated ≥ 3 times across real customer projects, AND
- at least one customer has paid for an output that depends on it, AND
- automating it reduces delivery time OR improves quality OR reduces a tracked risk.

No feature is built on speculation. No feature is built because "it would be cool".

## Rule 6 — Services become products

Every repeated service step must be productized as one of:
- template (markdown / SOW / report skeleton)
- checklist (delivery / QA / governance)
- script (sales discovery / objection / outreach)
- API endpoint
- dashboard tile
- automation in `auto_client_acquisition/`

The path from "manual step" → "productized asset" is captured in the Feature Candidate Log and reviewed monthly.

## Enforcement

- **Daily**: every PR description must reference which Rule it does not violate (or which it improves).
- **Weekly**: CEO Monday review confirms zero Rule 3 violations.
- **Monthly**: Feature Candidate Log → Rule 5/6 promotions.

## Cross-links

- `DEALIX_READINESS.md` — overall readiness
- `docs/company/SELLABILITY_POLICY.md` — Rule 1/2 binding policy
- `docs/company/EVIDENCE_SYSTEM.md` — what counts as evidence per rule
- `docs/governance/FORBIDDEN_ACTIONS.md` — Rule 3 detail
- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — Rule 4 detail
- `docs/strategy/dealix_maturity_and_verification.md` §7 — Rules 5/6 detail
