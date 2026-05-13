# Company Brain Sprint — Executive Report Skeleton / هيكل التقرير التنفيذي

Bilingual PDF + PPT, <= 14 slides. Compiled on Day 20, delivered at Day-21 handoff. Audience: department head (Sales / HR / Support / Ops) + COO.

## 1. Headline / العنوان
- AR + EN one-liner (e.g., "Sales team's average search time fell from 22 minutes to 1.4 minutes, with 97% of answers carrying source citations.").
- Team scoped, sprint window, document count ingested.

## 2. Executive Summary / الملخص التنفيذي
- 3 bullets: docs ingested + sensitive-doc handling, citation coverage + PII-surfacing rate (=0), search-time delta.
- One sentence the CEO can repeat: "We saved X hours/week and have 100% audit-log coverage."

## 3. Corpus Health / صحة المعرفة
| KPI | Value | Notes |
|---|---|---|
| Documents ingested | n | base cap 500 |
| Sensitive docs flagged | n | restricted tier |
| PII findings auto-redacted | n | `dealix/trust/pii_detector.py` |
| Docs > 90 days old (flagged stale) | n | freshness rule |
| Chunks indexed | n | embedding count |

Visual: corpus pie by category, sensitivity stacked bar, freshness histogram.

## 4. Eval Results / نتائج التقييم
| KPI | Target | Achieved | Method |
|---|---|---|---|
| Citation coverage | >= 95% | n% | eval harness |
| "No source = no answer" rate (out-of-corpus) | 100% | n% | 3-question harness |
| PII surfacing in answers | 0% | 0% | 50-question harness |
| Restricted-access correctness | 100% | n% | 3-persona test |
| Mean answer latency (s) | <= 3s | n s | trace logs |

Visual: bar chart "with citation / without citation", persona-access matrix.

## 5. Business Impact / الأثر التشغيلي
| KPI | Before | After | Delta | Method |
|---|---|---|---|---|
| Search time (min) | n | n | -n | timesheet survey |
| Repeated employee questions / week | n | n | -n | manager log |
| Document-owner interruptions / week | n | n | -n | SME survey |
| Hours saved / week (team-wide) | — | n | +n | calc |
| SAR saved / month | — | n | +n | hours * loaded rate |

Visual: before/after bar, hours-saved trendline.

## 6. Access & Governance / الصلاحيات والحوكمة
- Access-tier matrix (Admin / Team / Read-only).
- Audit-log snapshot (last 7 days).
- Right-to-erasure SLA (< 72 hours) test result.
- PDPL Art. 13/14 footer applied to any externally-shared answer.

## 7. 30-Day Adoption Plan / خطة التبني
- Week 1: shadow mode (compare assistant vs. SME).
- Week 2-3: open beta to the team, twice-weekly feedback loop.
- Week 4: steady state + first refresh batch.

## 8. Risks & Open Items / المخاطر والبنود المفتوحة
- Categories with low coverage (recommend adding docs).
- Owners not yet identified per category.
- Suggested expansion: second team, additional channel (Slack/Teams).

## Recommended Visuals
- Corpus pie (category) + stacked bar (sensitivity).
- Freshness histogram (age in days).
- Citation-coverage bar chart per category.
- Persona access matrix heatmap.
- Search-time before/after bar.

## Cross-links
- Proof pack: `docs/services/company_brain_sprint/proof_pack_template.md`
- Handoff agenda: `docs/services/company_brain_sprint/handoff.md`
- Renewal pathways: `docs/services/company_brain_sprint/upsell.md`
- Embeddings pipeline: `docs/EMBEDDINGS_PIPELINE.md`
- Company Brain module: `auto_client_acquisition/company_brain/`
- Data governance: `docs/trust/data_governance.md`
