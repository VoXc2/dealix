# Dealix Company Service Catalog

> Canonical service catalog for Dealix — a **Governed Revenue & AI Operations
> Company**. Supersedes the older five-rung ladder. Pricing is expressed
> as **ranges** or **`recommended_draft`**, never as a fabricated single number.
> Code source of truth: `auto_client_acquisition/service_catalog/registry.py`.

## How to read the pricing

| `price_mode` | Meaning |
|--------------|---------|
| `range` | A real min–max band the founder quotes within, based on scope. |
| `recommended_draft` | No fixed number yet — quoted per engagement until 3 paid pilots inform a real band. |
| `fixed` | A single confirmed price (used only after evidence supports it). |

**Pricing rule:** a `recommended_draft` service does not get a fixed price until
**≥ 3 paid pilots** of that service have been delivered. This protects against
pricing ahead of evidence.

## The three headline offers (lead with these)

Do not open with seven services. Internally and externally, lead with three:

1. **Governed Revenue Ops Diagnostic** — the entry service.
2. **Revenue Intelligence Sprint** — the core service after the diagnostic.
3. **Governed Ops Retainer** — the recurring engagement after the first sprint.

> Sales line: *"We start with a small diagnostic. If it proves value we move to
> a Sprint. If the workflow recurs, it becomes a Retainer."*

## The seven services

| # | Service | `price_mode` | Price (SAR) |
|---|---------|--------------|-------------|
| 1 | Governed Revenue Ops Diagnostic | `range` | 4,999 – 25,000 |
| 2 | Revenue Intelligence Sprint | `recommended_draft` | quoted per scope |
| 3 | Governed Ops Retainer | `recommended_draft` | quoted per month |
| 4 | AI Governance for Revenue Teams | `recommended_draft` | quoted per scope |
| 5 | CRM / Data Readiness for AI | `recommended_draft` | quoted per scope |
| 6 | Board Decision Memo | `recommended_draft` | quoted per scope |
| 7 | Trust Pack Lite | `recommended_draft` | quoted per scope |

### 1 — Governed Revenue Ops Diagnostic (entry)

- **Solves:** unclear CRM, unreliable pipeline, weak follow-up, ungoverned AI
  usage, inaccurate forecast, sales decisions with no evidence.
- **Deliverables:** Revenue Workflow Map, CRM / source quality review, pipeline
  risk map, follow-up gap analysis, decision passport, proof-of-value
  opportunities, recommended Sprint / Retainer.
- **Price:** `range` 4,999 – 25,000 SAR (upper band for larger orgs).
- **Why start here:** revenue is the language closest to the buyer — pipeline,
  follow-up, conversion, deal risk — so Dealix's value is understood quickly.

### 2 — Revenue Intelligence Sprint

- **Deliverables:** account prioritization, deal-risk scoring, next-best-action
  drafts, follow-up templates, revenue opportunity ledger, decision passport,
  proof pack.
- **Price:** `recommended_draft`.
- **Sold:** after a diagnostic, or when the prospect requests scope, or on a
  clear CRM / pipeline pain.

### 3 — Governed Ops Retainer

- **Monthly deliverables:** revenue review, pipeline quality review, AI decision
  review, approved follow-up queue, risk register, value report, board memo.
- **Price:** `recommended_draft` per month. This is the path to recurring revenue.

### 4 — AI Governance for Revenue Teams

- **Deliverables:** allowed AI actions, forbidden AI actions, approval
  boundaries, source rules, no-autonomous-external-send policy, evidence logging.

### 5 — CRM / Data Readiness for AI

- **Deliverables:** CRM hygiene report, source mapping, missing fields,
  duplicate accounts, bad lifecycle stages, data-readiness score, AI-readiness
  recommendation. Sold before any AI automation.

### 6 — Board Decision Memo

- **Deliverables:** top revenue decisions, pipeline risks, AI governance risks,
  capital allocation, build / hold / kill recommendations.

### 7 — Trust Pack Lite

- **Deliverables:** AI action policy, approval matrix, evidence handling,
  forbidden actions, agent safety rules, trust boundaries.
- **Sold:** only on a signal (`asks_for_security`, enterprise risk review,
  compliance reviewer) — not as a first offer.

## Forbidden across all services

- ❌ Skipping the diagnostic before a Sprint or Retainer.
- ❌ Putting a fixed price on a `recommended_draft` service before 3 paid pilots.
- ❌ Promising a metric the customer did not supply.
- ❌ Guaranteed outcomes or ROI promises.
- ❌ Public mention of a customer name without signed permission.
- ❌ Cold outreach, scraping, or live charge at any stage.

## Natural progression

```
Diagnostic -> Sprint -> Retainer -> Reusable Playbook -> Internal Platform
```

A new platform feature is built **only** when a workflow has repeated 3+ times
(Gate G7) — see [COMMERCIAL_GATES.md](commercial/COMMERCIAL_GATES.md).

## Bilingual one-liner

**English:** A governed service catalog — every engagement carries a source, an
approval, documented evidence, and a measurable outcome.

**Arabic:** كتالوج خدمات محكوم — كل ارتباط يحمل مصدراً، وموافقة، ودليلاً موثقاً،
ونتيجة قابلة للقياس.
