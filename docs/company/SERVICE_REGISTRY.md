# Dealix Service Registry

النسخة القانونية للمجلدات: `docs/services/<folder>/` + `SERVICE_ID_MAP.yaml`.  
الحالة **Sellable/Beta** آلياً: `python scripts/print_service_readiness_matrix.py`.

> **CANONICAL CATALOG (2026-05-16):** الكتالوج الرسمي هو **Governed Revenue & AI
> Operations** بسبع خدمات — انظر
> [`SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md`](SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md).
> العرض الأول للسوق: **Governed Revenue Ops Diagnostic**.

---

## Canonical 7-service catalog (Governed Revenue & AI Operations)

| # | Service | service_id | Tier |
|---|---------|-----------|------|
| 1 | Governed Revenue Ops Diagnostic | `governed_revenue_ops_diagnostic` | Entry offer |
| 2 | Revenue Intelligence Sprint | `revenue_intelligence_sprint` | Flagship sprint |
| 3 | Governed Ops Retainer | `governed_ops_retainer` | Retainer |
| 4 | AI Governance for Revenue Teams | `ai_governance_for_revenue_teams` | Add-on |
| 5 | CRM / Data Readiness for AI | `crm_data_readiness_for_ai` | Add-on |
| 6 | Board Decision Memo | `board_decision_memo` | Add-on |
| 7 | Trust Pack Lite | `trust_pack_lite` | On request only |

Full spec: [`SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md`](SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md).

---

## Superseded services (retained for history)

> **SUPERSEDED by the Governed Revenue Ops catalog** — see
> `SERVICE_CATALOG_GOVERNED_REVENUE_OPS.md`. The entries below are kept for
> delivery history and code-mapping continuity; they are not the canonical
> commercial offers.

## Lead Intelligence Sprint

| Field | Value |
|-------|--------|
| **folder** | `lead_intelligence_sprint` |
| **service_id** | `lead_intelligence_sprint` |
| **Status** | Sellable (repo baseline) |
| **Category** | Grow Revenue |
| **Price** | انظر `offer.md` + [`PRICING.md`](PRICING.md) |
| **Duration** | 10 أيام عمل (typical) |
| **ICP** | B2B، عيادات، لوجستيات، عقار، بيانات مبعثرة |

**Promise:** ترتيب حسابات/فرص + مسودات آمنة + تقرير تنفيذي + proof.

**Modules:** data_os, revenue_os, governance_os, reporting_os, delivery_os

**Gates:** Offer, Delivery, Governance, Demo, Sales

**Upsell:** Pilot Conversion، Monthly RevOps (انظر `upsell.md`)

---

## AI Quick Win Sprint

| Field | Value |
|-------|--------|
| **folder** | `ai_quick_win_sprint` |
| **service_id** | `quick_win_ops` |
| **Status** | Sellable |
| **Category** | Automate Operations |

**Modules:** delivery_os، reporting_os، governance_os + عملية عميل

**Upsell:** Workflow Automation، Monthly AI Ops

---

## Company Brain Sprint

| Field | Value |
|-------|--------|
| **folder** | `company_brain_sprint` |
| **service_id** | `company_brain_sprint` |
| **Status** | Sellable |
| **Category** | Build Company Brain |

**Modules:** knowledge_os، governance_os، reporting_os، delivery_os

**Upsell:** Monthly Brain Management، Policy/Sales assistants

---

## AI Support Desk Sprint

| Field | Value |
|-------|--------|
| **folder** | `ai_support_desk_sprint` |
| **service_id** | `support_desk_sprint` |
| **Status** | Sellable (readiness 90؛ **demo pack اختياري لقوة التسويق**) |
| **Category** | Serve Customers |

**Modules:** support_os، governance_os، reporting_os

---

## AI Governance Program

| Field | Value |
|-------|--------|
| **folder** | `ai_governance_program` |
| **service_id** | `ai_governance_program` |
| **Status** | Sellable |
| **Category** | Govern AI |

**Modules:** governance_os، compliance_os، reporting_os

---

## Executive report structure (all)

1. Executive Summary · 2. Client Goal · 3. What We Received · 4. Data/Process Quality · 5. Key Findings · 6. Priority Opportunities · 7. Risks · 8. Actions · 9. Proof Pack · 10. Next Step (A self / B pilot / C monthly OS)
