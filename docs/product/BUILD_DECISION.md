# Product Build Decision

> Rule: don't build because it's exciting. Build because it earned its place
> in real customer delivery.

## When this decision fires
- A backlog item is proposed (engineer, founder, customer request).
- A capability scores ≥ 60 in `docs/product/FEATURE_PRIORITIZATION.md`.
- Monthly product review.

## Mandatory gate (per Decision Rule 5)

Even with a high score, build is blocked unless:
- The underlying step repeated ≥ 2 times in real customer delivery, AND
- At least one customer has paid for an output that depends on it.

## Scoring rubric

| Criterion | Weight |
|-----------|------:|
| Repetition (≥ 3 projects) | 25 |
| Revenue impact (a paying customer needs it) | 20 |
| Delivery-time reduction | 20 |
| Governance risk reduction | 15 |
| Output quality improvement | 15 |
| Build simplicity (≤ 2 person-weeks for MVP) | 5 |
| **Total** | **100** |

## Decision bands

- **Build now (≥ 80)** — lands in next sprint, with Feature DoD.
- **Backlog (60–79)** — revisit monthly; promoted when score crosses 80.
- **Do not build (< 60)** — closed; revisit only if evidence changes.

## Risk review (mandatory)

For every "Build now":
1. What does it depend on? (other modules, external APIs)
2. What could break it in production?
3. What's the rollback?
4. What's the FinOps impact (LLM cost, infra)?
5. Who is the named owner?

## Example decisions

| Candidate | Score | Decision | Rationale |
|-----------|------:|----------|-----------|
| Import Preview (CSV) | 90 | Build now | Repeated in every Lead Intel sprint; paid; saves 2h/project |
| Production-grade Outreach Drafts | 75 | Backlog | Repeated, but no paid customer signal yet |
| Autonomous outbound agent | 35 | Do not build | Violates Decision Rule 3 + Forbidden Actions |
| WhatsApp Business API integration | 50 | Do not build | High compliance/spam risk, not in Phase 1 scope |
| LLM Gateway (cost guard) | 78 | Backlog (promoted Phase 2) | Needed as soon as model spend >5K SAR/mo |
| Multi-tenant RBAC | 45 | Do not build | Premature — no enterprise customer yet |

## Owner & cadence
- **Owner**: HoP + CTO co-sign every "Build now".
- **Cadence**: monthly product review; ad-hoc when a strong candidate emerges.

## Cross-links
- `docs/product/FEATURE_PRIORITIZATION.md` — backlog scoring
- `docs/company/DECISION_RULES.md` — Rule 5/6 binding
- `docs/product/CAPABILITY_MATRIX.md` — current state per capability
- `docs/finops/model_cost_governance.md` — FinOps impact (W4.T24)
