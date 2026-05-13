---
title: <Document Title>
doc_id: W<wave>.T<task>.<slot>
owner: <CEO|CRO|CTO|HoP|HoCS|HoLegal|HoData>
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: []
kpi:
  metric: <name>
  target: <numeric>
  window: <e.g., 90d>
rice:
  reach: 0
  impact: 1
  confidence: 0.7
  effort: 1
  score: 0
---

# <Title>

## 1. Context
Why this document exists. Saudi GTM linkage. Problem solved.

## 2. Audience
Who reads this and what decision they make.

## 3. Decisions / Content
The substantive content. Numbered subsections recommended.

## 4. KPIs
Measurable outcomes (mirror frontmatter, plus measurement method and owner of the metric).

## 5. Dependencies
Upstream docs/code this depends on. Reference `doc_id` and file paths.

## 6. Cross-links
- Existing repo docs cross-linked (`docs/...`)
- New Wave-N docs cross-linked by `doc_id`
- Code anchors (`auto_client_acquisition/...`, `api/routers/...`, `dealix/trust/...`)

## 7. Owner & Review Cadence
Owner role, review interval (monthly / quarterly), escalation path.

## 8. Change Log
| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | — | Initial draft |

---

## Variants

- **ADR**: replace sections 1–4 with Nygard form (`Context / Decision / Status / Consequences`); keep frontmatter.
- **Trust docs**: add `## 9. External Attestations`.
- **Pricing docs**: add `## 9. SAR Examples`.
- **AR companions**: same frontmatter with `language: ar` and `ar_companion` pointing back to the English file.
