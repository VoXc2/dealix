# مصنع العروض التجارية (Proposal Factory)

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/proposal.schema.json`
> المصدر المرجعي للكتالوج: [`company_os/revenue/proposals.json`](../../company_os/revenue/proposals.json)

---

## 1. ما هو مصنع العروض؟

مصنع العروض هو العملية الموحّدة لتوليد عرض تجاري في Dealix — من الفكرة حتى الاعتماد. كل عرض:
- **يجب** أن يُربط بـ `product_id` من كتالوج المنتجات.
- **يجب** أن يحمل `evidence_level` لكل تقدير.
- **لا يُعرض** للعميل بسعر نهائي قبل `founder_approved=true`.
- **ينتهي** بكارت إجراء (`revenue_action_card`) يُطرح على المؤسس.

---

## 2. الحقول الإلزامية

| الحقل | القاعدة |
|---|---|
| `id` | `PROP-XXXX` — تسلسل فريد |
| `client` | اسم الشركة العميلة |
| `sector` | `Marketing Agency` / `Training` / `B2B Services` / `Other` |
| `problem` | المشكلة التجارية المحددة — لا عروض عامة |
| `product_id` | **يجب** أن يكون في `data/catalog/product_catalog.json` — راجع §3 |
| `scope` | قائمة تفصيلية بما يشمله العرض (مصفوفة) |
| `out_of_scope` | قائمة صريحة بما لا يشمله (مانع للتوقعات الزائدة) |
| `timeline` | مدة التسليم |
| `price_range_sar` | `{min, max, is_final}` — `is_final=false` حتى الموافقة |
| `assumptions` | كل افتراض يؤثر على السعر أو النطاق |
| `evidence_level` | مستوى الدليل الداعم للتسعير |
| `risks` | المخاطر المعروفة |
| `payment_terms` | شروط الدفع |
| `approval_status` | الحالة في مسار الاعتماد |

---

## 3. ربط الكتالوج (إلزامي)

المصدر الوحيد المعتمد لأسماء المنتجات وأسعارها هو `data/catalog/product_catalog.json`، الذي يوائم SKUs `company_os/revenue/proposals.json`:

| product_id | sku_ref | السعر (SAR) | النوع |
|---|---|---|---|
| `readiness_scan` | — | مجاني | مرّة واحدة |
| `revenue_leakage_diagnostic` | PROP-P1 | 2,500–5,000 | مرّة واحدة |
| `followup_recovery_workflow` | — | 2,500–6,000 | مرّة واحدة |
| `ai_revenue_ops_starter` | PROP-P2-SMALL | 3,000/شهر | شهري |
| `full_revenue_os` | PROP-P2-MEDIUM | 8,000/شهر | شهري |
| `monthly_optimization` | — | 1,500–4,000/شهر | شهري |
| `custom_company_os` | PROP-P2-ENTERPRISE | 20,000/شهر | شهري |
| `multi_department_rollout` | — | 20,000–100,000 | مخصص |

عرض بـ `product_id` خارج هذه القائمة = **يفشل** في `client_revenue_delivery_check.py`.

---

## 4. مسار الاعتماد (Approval Pipeline)

```
draft
  ↓ الذكاء يُعدّ المسودة
pending_founder_approval
  ↓ المؤسس يراجع في طابور الموافقات
  ↓ رفض → rejected
founder_approved
  (founder_approved=true, is_final=true, approved_by, approved_at)
  ↓ تُفعَّل جلسة البوابة للعميل → /client/proposal
```

**قاعدة `is_final`:**
- `is_final=false` طوال مرحلة المسودة والانتظار.
- `is_final=true` فقط بعد `approval_status=founder_approved`.
- عرض مع `is_final=true` و `founder_approved=false` = **تعارض منطقي — ممنوع**.

---

## 5. قواعد التسعير وسلّم الأدلة

| evidence_level | معنى التسعير |
|---|---|
| `assumption` | تقدير ابتدائي — نطاق واسع مع ملاحظة واضحة |
| `benchmark` | مرتكز على معايير السوق — موثّق |
| `client_reported` | بناءً على ما صرّح به العميل — مع تحفظ |
| `client_data` | مُستند لبيانات فعلية من العميل — موثوق |
| `measured` | مقيس من تسليم سابق — الأقوى للتجديد |

للتجديد أو الترقية: `evidence_level ∈ {client_data, measured, verified}` — أقل من ذلك يفشل.

---

## 6. أمثلة واقعية

### PROP-1001 — TrainMe KSA
- `product_id`: `revenue_leakage_diagnostic`
- `price_range_sar`: 2,500–5,000، `is_final=false`
- `approval_status`: `pending_founder_approval`
- `evidence_level`: `client_reported`
- **الحالة:** ينتظر مراجعة المؤسس. العميل لا يرى السعر النهائي بعد.

### PROP-1002 — Digital Rise Agency
- `product_id`: `revenue_leakage_diagnostic`
- `price_range_sar`: 2,500، `is_final=true`
- `approval_status`: `founder_approved` (وافق المؤسس 2026-06-02)
- `evidence_level`: `client_data`
- **الحالة:** معتمد، جاهز لتسليم الدفع.

---

## 7. الخطوات اللاحقة بعد اعتماد العرض

```
founder_approved=true
    ↓
توليد كارت إجراء: type=prepare_payment_handoff
    ↓
تحضير payment_handoff (PAY-XXXX)
    ↓
موافقة المؤسس على الدفع
    ↓
/client/payment في البوابة (يدويًا)
```

---

## 8. ما هو ممنوع في مصنع العروض

- عرض بدون `product_id` من الكتالوج.
- `is_final=true` بدون موافقة المؤسس.
- توعّد بضمان ROI أو نتيجة محددة.
- إرسال عرض للعميل خارج البوابة.
- حذف `out_of_scope` أو إبقاؤها فارغة.

---

## الروابط المرجعية

- سكيمة العرض: `schemas/proposal.schema.json`
- كتالوج المنتجات: `data/catalog/product_catalog.json`
- SKUs التجارية: [`company_os/revenue/proposals.json`](../../company_os/revenue/proposals.json)
- مراجعة العرض في البوابة: [`../client_portal/CLIENT_PROPOSAL_REVIEW_AR.md`](../client_portal/CLIENT_PROPOSAL_REVIEW_AR.md)
- بطاقات الإجراء: [`REVENUE_ACTION_CARDS_AR.md`](REVENUE_ACTION_CARDS_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
