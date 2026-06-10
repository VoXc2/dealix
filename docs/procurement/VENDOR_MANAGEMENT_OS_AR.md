# نظام إدارة الموردين — Dealix Vendor Management OS

> **المصدر الوحيد للحقيقة للموردين في Dealix.** كل vendor جديد يُسجَّل
> في `data/procurement/vendors.jsonl`، كل API call cost يُسجَّل في
> `api_costs.jsonl`، كل اشتراك شهري في `subscriptions.jsonl`.

**الحالة:** مسودة — Phase 1 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. المبادئ (Principles)

1. **سجل واحد فقط.** أي vendor يُذكر في `.env.example` يجب أن يكون له
   entry في `vendors.jsonl`.
2. **كل secret مرتبط بـ vendor.** `secrets_registry.vendor_id` يشير
   إلى entry في `vendors.jsonl`.
3. **كل تكلفة API تُسجَّل.** agent قبل استخدام API عالي التكلفة يحتاج
   budget approval.
4. **استبدال دائم.** كل vendor critical له **replacement option**
   محدّث في `vendors.jsonl`.
5. **مراجعة شهرية للمشتريات.** `SUBSCRIPTION_REVIEW_AR.md` يحدد
   الإيقاع.

## 2. Schema لكل Vendor (vendors.jsonl)

```json
{
  "vendor_id": "v_moyasar",
  "name": "Moyasar",
  "purpose": "Payments (SAR)",
  "owner": "founder",
  "monthly_cost_sar_estimate": null,
  "monthly_cost_sar_actual": null,
  "usage_metric": "transaction_count",
  "data_risk": "high",
  "data_risk_reason": "processes payment data + PII",
  "secrets_required": ["MOYASAR_SECRET_KEY", "MOYASAR_WEBHOOK_SECRET"],
  "replacement_option": "Tap Payments, HyperPay",
  "replacement_effort": "medium",
  "cancellation_difficulty": "low",
  "business_criticality": "critical",
  "review_date": "2026-09-01",
  "contract_end": null,
  "pdpl_compliant": true,
  "soc2_certified": false,
  "data_residency": "Saudi Arabia (me-south-1)"
}
```

## 3. تصنيف Data Risk

| المستوى | الوصف | أمثلة |
| --- | --- | --- |
| **low** | no PII, no payment, public data | Tavily, Google CSE |
| **medium** | pseudonymized data | PostHog, Sentry |
| **high** | PII or payment data | HubSpot, WhatsApp providers, SendGrid, Gmail, Gmail OAuth |
| **critical** | PII + financial + cross-border | Moyasar, CRM with full customer data |

## 4. Business Criticality

| المستوى | الوصف | SLA |
| --- | --- | --- |
| **low** | nice-to-have, manual fallback | no SLA |
| **medium** | productivity, degraded if down | best-effort |
| **high** | revenue-adjacent, manual workaround | 99% uptime target |
| **critical** | revenue-blocking, no workaround | 99.5%+ target + alert |

## 5. Cancellation Difficulty

| المستوى | الوصف | أمثلة |
| --- | --- | --- |
| **low** | cancel anytime, no fee | PostHog, Sentry (monthly) |
| **medium** | cancel monthly, fee on annual | HubSpot (annual contract) |
| **high** | locked annual + early-term fee | enterprise Sentry, SDAIA filings |
| **locked** | regulatory, can't cancel | ZATCA, CR, VAT |

## 6. Tool Selection Policy (مختصر)

قبل إضافة vendor جديد، اسأل:

1. **هل يوجد vendor حالي يفعل ذلك؟** ⇒ لا تضيف.
2. **هل هو critical أو nice-to-have؟** ⇒ critical يحتاج founder approval.
3. **ما data risk؟** ⇒ high+ يحتاج DPO + legal review.
4. **هل التكلفة ضمن budget؟** ⇒ لا ⇒ رفض أو defer.
5. **هل هو monthly cancellable؟** ⇒ يفضّل.
6. **هل يدعم Saudi data residency؟** ⇒ critical/high يحتاج.

## 7. Build vs Buy (مختصر)

- **Buy if:** commodity SaaS, low differentiation, fast setup.
- **Build if:** core moat, no good off-shelf, data-sensitive.
- **Hybrid if:** buy core، build integrations.

**أمثلة Dealix:**

- **Buy:** PostHog, Sentry, SendGrid, Calendly.
- **Build:** Revenue OS, proof ledger, governance engine.
- **Hybrid:** WhatsApp integration (buy provider، build governance).

## 8. Vendor Risk Policy

- أي vendor critical يجب أن يكون له **backup vendor** (hot standby)
  أو **runbook** (manual fallback) موثّق.
- أي vendor high يجب أن يكون له replacement effort مقدر.
- أي vendor يخالف PDPL ⇒ استبدال فوري + legal review.

## 9. مراجعة شهرية (Monthly Subscription Review)

كل شهر:
1. اقرأ `data/procurement/subscriptions.jsonl`.
2. تحقق من:
   - هل الـ subscription لا يزال مستخدماً؟
   - هل السعر تغيّر؟
   - هل هناك tier أرخص متاح؟
3. ألغِ أي subscription غير مستخدم.
4. سجّل في `reports/procurement/SUBSCRIPTION_REVIEW.md`.

## 10. API Cost Control (مختصر)

- LLM spend: target <$10/day (SLO.md Tier 3).
- أي LLM call > 10K tokens يحتاج caching أو summarization.
- أي vendor API > 1000 calls/day يحتاج rate limit + alert.
- API costs تُسجَّل يومياً في `api_costs.jsonl`.

## 11. الأدوار

| الدور | المسؤول |
| --- | --- |
| **Procurement Owner** | المؤسس (حالياً) |
| **Vendor Manager** | المؤسس + Agent #17 (read + recommendations) |
| **API Cost Analyst** | Agent #17 + scripts |
| **Agent #17 (Procurement)** | يبني النظام، لا يوقّع على عقود |

## 12. مخاطر

1. **Single-vendor dependency** في WhatsApp providers ⇒ multi-provider
   chain (already implemented).
2. **API cost spike** ⇒ daily monitor + budget cap.
3. **Vendor outage** ⇒ runbook per critical vendor.
4. **Secret sprawl** ⇒ secret rotation policy.
5. **Contract auto-renew** surprise ⇒ monthly review.

## 13. الربط مع agents أخرى

- **Agent #12 (Infra):** vendor hosting = Railway + AWS S3.
- **Agent #13 (Legal):** vendor PDPL compliance = legal review.
- **Agent #15 (Services):** API cost per service = service pricing.
- **Agent #16 (Data Room):** vendor list = due diligence section.

## 14. المراجع

- `data/procurement/vendors.jsonl` — catalog
- `data/procurement/api_costs.jsonl` — API costs
- `data/procurement/subscriptions.jsonl` — subscriptions
- `schemas/vendor.schema.json` — schema
- `docs/COST_OPTIMIZATION.md` — cost rules
- `docs/V7_COST_CONTROL_POLICY.md` — V7 cost policy
- `docs/SLO.md` (Tier 3 cost) — SLO cost
- `docs/finance/FOUNDER_UNIT_ECONOMICS_MODEL_AR.md` — unit economics
- `docs/SUPPLIER_MASTER_LIST.md` — existing reference
- `docs/infra/SECRETS_MANAGEMENT_AR.md` — secrets policy
