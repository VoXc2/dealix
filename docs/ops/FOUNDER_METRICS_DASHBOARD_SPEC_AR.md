# Dealix — Founder Metrics Dashboard Spec

هذه مواصفات لوحة المؤسس التي تربط المنتج بالإيراد، التشغيل، الثقة، والجودة.

## 1) North Star

**Qualified Saudi B2B opportunities progressed to a signed/paid next step with evidence.**

المقياس لا يحتسب lead خام. يحتسب فرصة مؤهلة وصلت إلى خطوة تجارية واضحة: demo، diagnostic، proposal، paid pilot، أو retainer.

## 2) Revenue metrics

| Metric | Definition | Cadence |
|---|---|---|
| MRR | recurring monthly revenue | يومي/أسبوعي |
| ARR | MRR × 12 | أسبوعي |
| New MRR | MRR من عملاء جدد | أسبوعي |
| Expansion MRR | توسع من عملاء حاليين | أسبوعي |
| Churned MRR | إيراد مفقود | أسبوعي |
| NRR | retained + expansion / starting MRR | شهري |
| Gross margin estimate | revenue minus provider/runtime costs | شهري |

## 3) Funnel metrics

| Stage | Examples |
|---|---|
| Prospects discovered | Saudi B2B accounts found |
| ICP qualified | sector, size, urgency, budget fit |
| Contact enriched | email/phone/channel available with PDPL guard |
| Outreach queued | campaign/action ready |
| Replies | inbound response |
| Meetings booked | Calendly/manual |
| Diagnostics delivered | proof artifact delivered |
| Proposals sent | pricing/service offer sent |
| Closed won | paid/customer signed |

## 4) Product usage metrics

- Active tenants.
- Active operators/admins.
- Agent runs by class.
- Approval requests created/approved/rejected.
- Proof packs generated.
- Diagnostics generated.
- API latency and error rate.
- LLM cost per workflow.

## 5) Trust metrics

- Number of high-risk actions requiring approval.
- Approval SLA.
- Audit log coverage.
- No-overclaim violations: must be zero.
- Public endpoints without auth intentionally listed.
- DSAR/compliance requests state.

## 6) Founder daily view

Every morning:

1. Revenue movement.
2. Top 10 highest-probability opportunities.
3. Bottlenecks by funnel stage.
4. Failing integrations/deployments.
5. Top customer risk.
6. One action that increases revenue today.

## 7) Implementation map

| Surface | Existing / target |
|---|---|
| API metrics | `/api/v1/metrics`, revenue metrics routers |
| Founder summary | founder summary / daily digest scripts |
| Health | `/healthz`, `/ready`, `/healthz?deep=1` |
| Evidence | proof packs, audit exports, post deploy evidence template |
| CI state | GitHub Actions badges and artifacts |

## 8) Launch gate

A dashboard is founder-grade only when every metric has:

- owner
- source
- refresh cadence
- failure mode
- action tied to it
