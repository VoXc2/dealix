# Capital Ledger Strategy

Every Dealix engagement must leave the firm with at least one **reusable asset**. The Capital Ledger is the system that captures, classifies, and compounds these assets across the company.

## 1. Capital types

| Type | Examples |
| --- | --- |
| **Service Capital** | Checklists, SOPs, templates, scripts |
| **Product Capital** | Reusable modules, dashboards, evaluators |
| **Knowledge Capital** | Playbooks, sector patterns, objection libraries |
| **Trust Capital** | Proof Packs, audit reports, testimonials |
| **Market Capital** | Content assets, benchmarks, partner signals |
| **Standard Capital** | Method definitions, QA rubrics, certification material |
| **Venture Capital** | Unit playbooks and product modules that can become standalone ventures |

## 2. Minimum per engagement

Every closed engagement must produce **at least**:

- 1 Trust Asset
- 1 Product or Knowledge Asset
- 1 Expansion Path documented

If the engagement does not produce these, it is recorded as **strategically incomplete**, regardless of revenue.

## 3. Ledger schema

```
capital_id (PK)
type
title
description
source_engagement_id
business_unit
owner
created_at
last_used_at
reuse_count
public_ok (bool)
linked_proof_ids[]
maturity: draft | reviewed | productized
status: active | archived
```

## 4. Workflow

1. At project close, Reporting OS emits the Proof Pack.
2. Capital OS scans the artifacts and proposes ledger rows.
3. The BU owner accepts or amends.
4. Maturity advances as the asset is reused.
5. When reuse count crosses a threshold, Intelligence OS proposes promotion into a Product Module.

## 5. Compounding behavior

- An asset reused 3+ times across engagements becomes a candidate for `core_os` module.
- An asset reused 5+ times becomes a Product Module candidate (`BUSINESS_UNITS.md`).
- A Product Module + retainer base ≥ N becomes a Venture candidate (`VENTURE_FACTORY.md`).

## 6. Anti-patterns

- Asset hoarding inside a single operator’s files.
- Re-deriving the same artifact for every client.
- Promoting assets to “productized” without QA review.
- Recording assets without a named owner.
- Marketing a capital asset publicly without the underlying Proof Pack’s consent level.

## 7. Quarterly rituals

- **Capital Review** — audit the ledger, retire stale assets, promote ripe ones.
- **Productization Sprint** — convert top assets into Core OS modules.
- **Method Update** — fold accepted patterns into the Dealix Method.

The Capital Ledger is the difference between selling time and **building a company**.
