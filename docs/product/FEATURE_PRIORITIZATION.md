# Feature Prioritization

The single backlog rule: a feature only gets built when it has earned its
place in real customer delivery. No speculation. No "would be cool".

## Scoring rubric

| Criterion | Weight |
|-----------|------:|
| Repeated across projects (≥ 2 = score full) | 25 |
| Saves delivery time | 20 |
| Reduces a tracked risk (PII, governance, hallucination) | 20 |
| Improves output quality (clarity, citation, accuracy) | 15 |
| Helps sales close (proof, demo, asset) | 10 |
| Quick to build (≤ 2 person-weeks) | 10 |
| **Total** | **100** |

## Decision

- **80+ — Build now**. Lands in the next sprint cycle.
- **60–79 — Backlog**. Re-scored monthly; promoted when score crosses 80.
- **< 60 — Ignore**. Not even backlog.

## Hard gate (regardless of score)

Per `docs/company/DECISION_RULES.md` Rule 5:
- Must have repeated ≥ 2 times in real customer delivery, AND
- At least one customer must have paid for an output that depends on it.

Score-based promotion is a tie-breaker, not an override.

## How a candidate enters the backlog

Captured during Stage 8 (Expand) of every project, in the
`POST_PROJECT_REVIEW.md` file under section 5 "Feature Candidate". The HoP
copies entries here monthly.

## Backlog (refresh monthly)

| Candidate | Source projects (count) | Repeat | Time saved | Risk reduced | Quality | Sales | Effort | Score | Decision |
|-----------|------------------------|:------:|:----------:|:------------:|:-------:|:-----:|:------:|------:|---------|
| (example) Outreach draft generator | 0 | — | — | — | — | — | — | — | new — needs first 2 projects |
| (example) RAG freshness watchdog | 0 | — | — | — | — | — | — | — | new — needs first 2 projects |
| (example) PDF export for executive report | 0 | — | — | — | — | — | — | — | new — needs first 2 projects |

> Pre-revenue: every row is a placeholder. The first 3 customer projects
> populate this table with real entries. Until then, engineering capacity
> goes to the 5 Phase-1 OS modules (already MVP) and the LLM Gateway
> (Phase 2 planned).

## Anti-patterns blocked by this rubric

- "AI fad" features (RAG everywhere, agents everywhere) without paid demand.
- Architectural rewrites without measured customer benefit.
- Premature optimization for scale we don't have yet.
- "Make it look more like Notion / Linear / etc." without a tied KPI.

## Cross-links

- `docs/company/DECISION_RULES.md` — Rule 5 binding
- `docs/strategy/dealix_maturity_and_verification.md` §7 — "Build only after repetition"
- `docs/company/COMPOUNDING_SYSTEM.md` — where candidates come from
- `docs/product/PRODUCT_ROADMAP.md` — phase plan
- `docs/product/CAPABILITY_MATRIX.md` — current capability state
