# Dealix Decision Operating System

> **Principle**: Dealix makes decisions through evidence, not opinion. Every
> recurring decision has a written rubric, a score, a risk review, an owner,
> and a next action.

## The 8 decision types

| # | Decision | When fired | Owner | Doc |
|---|----------|-----------|-------|-----|
| 1 | Sellability | A service is being considered for the catalog | CEO + CRO | `docs/company/SELLABILITY_POLICY.md` |
| 2 | Delivery | An output is about to ship to a customer | HoCS (QA Reviewer) | `docs/quality/QUALITY_REVIEW_BOARD.md` |
| 3 | Governance | An action touches data, outreach, or claims | HoLegal + Governance OS | `docs/governance/APPROVAL_MATRIX.md` + `dealix/trust/approval_matrix.py` |
| 4 | Product Build | A feature candidate is proposed | HoP + CTO | `docs/product/FEATURE_PRIORITIZATION.md` + `docs/product/BUILD_DECISION.md` |
| 5 | Pricing | List price under review or discount requested | CRO + CFO | `docs/company/PRICING_DECISION.md` |
| 6 | Retainer | Retainer should/should-not be offered | HoCS + CRO | `docs/growth/RETAINER_DECISION.md` |
| 7 | Scale | First hire / partner / outsource decision | CEO | `docs/company/SCALE_DECISION.md` |
| 8 | Enterprise | A 100K+ SAR enterprise opportunity opens | CEO + CTO + HoLegal | `docs/enterprise/ENTERPRISE_DECISION.md` |

## The decision contract

Every recurring decision must record:

1. **Evidence** — facts cited from the artifact registry (Service Matrix, Capability Matrix, Operating Scorecard, Proof Ledger, Risk Register).
2. **Score** — numeric per the rubric in the relevant doc.
3. **Risk review** — what could break? mitigated how?
4. **Owner** — single named person accountable for the decision.
5. **Next action** — concrete with deadline.

A decision without all five is invalid and must be re-run.

## Decision log

All non-trivial decisions are captured in `docs/company/decisions/<YYYY-MM-DD>-<slug>.md` (Architecture Decision Record-style for non-engineering choices). Engineering ADRs live in `docs/adr/`.

Template:

```markdown
# Decision: <name>
Date: YYYY-MM-DD · Owner: __
## Context
## Options
## Evidence
## Score
## Risk review
## Decision
## Next action(s) + deadline
```

## Auto-prompts (the system reminds you)

These trigger a decision check:
- New service proposed → Sellability Decision.
- Project enters Stage 5 (Validate) → Delivery Decision.
- Any outbound message → Governance Decision.
- Any backlog candidate → Build Decision.
- 3 clean closes of the same service at list price → Pricing Decision.
- Sprint exits Stage 7 with Quality ≥ 85 → Retainer Decision.
- Founder hits 60+ delivery hours/week → Scale Decision.
- Customer asks for "everything, custom, big contract" → Enterprise Decision.

## Cross-links

- `docs/company/DEALIX_OPERATING_KERNEL.md` — the runtime
- `docs/company/DECISION_RULES.md` — 6 binding rules
- `docs/company/DEALIX_STANDARD.md` — 8 standards
- `docs/company/EVIDENCE_SYSTEM.md` — what counts as evidence
- `docs/company/OPERATING_FLYWHEEL.md` — how good decisions compound
