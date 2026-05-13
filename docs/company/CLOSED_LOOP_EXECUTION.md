# Closed-Loop Execution

> **Rule**: every Dealix engagement moves through 11 stations. A project is
> not "done" until the loop closes — internal learning captured, asset
> shelved, next offer proposed.

## The 11-station loop

```
Request → Qualification → Scope → Governance Check → Delivery → QA
   → Proof Pack → Client Review → Learning Review → Productization → Expansion
```

| # | Station | Output | Owner | Decision file |
|---|---------|--------|-------|---------------|
| 1 | Request | Intake form filled, classified | Sales | `docs/operations/REQUEST_INTAKE_SYSTEM.md` |
| 2 | Qualification | Qualification Score recorded | CRO | `docs/sales/QUALIFICATION_SCORE.md` |
| 3 | Scope | Signed SOW from `templates/sow/` | CRO + Customer | Service Definition of Done |
| 4 | Governance Check | Pre-action approval matrix decisions | HoLegal + Governance OS | `dealix/trust/approval_matrix.py` |
| 5 | Delivery | Stage Machine through 8 stages | Delivery Owner | `auto_client_acquisition/delivery_factory/stage_machine.py` |
| 6 | QA | 5-gate QA + ≥80 score | QA Reviewer | `docs/quality/QUALITY_REVIEW_BOARD.md` |
| 7 | Proof Pack | Stage-7 evidence written | Delivery Owner | `dealix/reporting/proof_pack.py` |
| 8 | Client Review | Handoff session + signed-off `delivery_approval.md` | HoCS | `docs/delivery/HANDOFF_PROCESS.md` |
| 9 | Learning Review | `POST_PROJECT_REVIEW.md` filed | Delivery Owner + HoCS | `docs/company/COMPOUNDING_SYSTEM.md` |
| 10 | Productization | Feature candidates added; templates filed | HoP + CTO | `docs/product/FEATURE_PRIORITIZATION.md` |
| 11 | Expansion | Retainer / second sprint / referral conversation | HoCS + CRO | `docs/growth/RETAINER_DECISION.md` |

## The closure contract

A project is officially CLOSED only when:

- [ ] Stations 1–11 each have an artifact filed in `clients/<codename>/`.
- [ ] Anonymized Proof Pack copied to `docs/assets/proof_packs/`.
- [ ] At least 1 of: new template / playbook update / feature candidate / sales asset captured.

If any item is missing, the project stays in the founder's WIP queue. The "delivered" flag is **not** the close flag.

## Why this matters

Two customers with the same service shouldn't cost 2× the effort. With the loop closing, the 2nd customer costs ~70% of the 1st, the 5th costs ~40%. The compounding lives in Stations 9–11.

## Anti-patterns this loop blocks

- "Ship it and move on" without learning capture (Compounding broken).
- "We'll get to the Proof Pack later" — by then, customer momentum is lost.
- "This was custom, no template" — every project produces at least one reusable asset, even if it's a paragraph of objection handling.
- "Next time we'll do it right" — same mistake compounds across customers.

## Cross-links
- `docs/company/COMPOUNDING_SYSTEM.md` — the 6 assets
- `docs/company/DECISION_OPERATING_SYSTEM.md` — the 8 decisions
- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — Delivery Standard 8 stages
- `docs/company/DEFINITION_OF_DONE.md` — Project DoD
