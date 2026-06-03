# مراجعة العرض التجاري داخل البوابة

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/proposal.schema.json`
> المسار: `/client/proposal`

---

## 1. القاعدة الأساسية: لا سعر نهائي بدون موافقة المؤسس

```
السعر المعروض = تقدير مبدئي
السعر النهائي = يُفعَّل فقط عندما founder_approved=true + is_final=true
```

العميل يرى العرض في البوابة، لكن أي رقم يظهر بدون تأكيد المؤسس هو **نطاق أولي** (`price_range_sar.is_final=false`). هذا ليس تحفظًا رسميًا فحسب — بل ثابت مطبّق في النظام.

---

## 2. رحلة العرض داخل البوابة

```
[1] الذكاء يُعدّ مسودة عرض (approval_status: draft)
            ↓
[2] المؤسس يراجع في طابور الموافقات
    approval_status: pending_founder_approval
            ↓ رفض → rejected + إشعار للعميل
    موافقة → founder_approved=true
    approval_status: founder_approved
            ↓
[3] البوابة ترسل رابطًا لـ /client/proposal (مؤقت، منتهي الصلاحية)
            ↓
[4] العميل يراجع العرض (role: client_approver)
    - يرى نطاق السعر المعتمد
    - يرى النطاق + الافتراضات + أدلة التسعير
    - السعر النهائي موثّق (is_final=true)
            ↓
[5] العميل يوافق أو يطلب تعديل → يُسجَّل في البوابة
            ↓ موافقة
[6] الخطوة التالية: تحضير تسليم الدفع (→ /client/payment)
```

---

## 3. حقول العرض الأساسية (proposal.schema.json)

| الحقل | الإلزامية | الوصف |
|---|---|---|
| `id` | إلزامي | `PROP-XXXX` |
| `client` | إلزامي | اسم الشركة العميلة |
| `sector` | إلزامي | `Marketing Agency` / `Training` / `B2B Services` / `Other` |
| `problem` | إلزامي | المشكلة التجارية التي يعالجها العرض |
| `product_id` | **إلزامي** | يجب أن يكون في `data/catalog/product_catalog.json` |
| `scope` | إلزامي | قائمة ما يشمله العرض |
| `out_of_scope` | إلزامي | قائمة ما لا يشمله |
| `timeline` | إلزامي | مدة التنفيذ |
| `price_range_sar` | إلزامي | `{min, max, is_final}` |
| `assumptions` | إلزامي | الافتراضات التي يُبنى عليها السعر |
| `evidence_level` | **إلزامي** | مستوى الدليل من سلّم: `none...verified` |
| `risks` | إلزامي | المخاطر المعروفة |
| `payment_terms` | إلزامي | شروط الدفع |
| `approval_status` | إلزامي | `draft → pending_founder_approval → founder_approved / rejected` |
| `founder_approved` | إلزامي | `true` فقط بعد موافقة فعلية |
| `approved_by` + `approved_at` | يُملأ عند الموافقة | من وافق ومتى |

---

## 4. ربط العرض بالكتالوج (إلزامي)

كل عرض يجب أن يُشير إلى `product_id` موجود في `data/catalog/product_catalog.json`:

| product_id | الاسم | النوع | النطاق (SAR) |
|---|---|---|---|
| `readiness_scan` | فحص الجاهزية | مجاني/تمهيدي | 0 |
| `revenue_leakage_diagnostic` | تشخيص تسرب الإيراد | مرّة واحدة | 2,500–5,000 |
| `followup_recovery_workflow` | ورشة استرجاع المتابعة | مرّة واحدة | 2,500–6,000 |
| `ai_revenue_ops_starter` | عمليات الإيراد بالذكاء — مبتدئ | شهري | 3,000 |
| `full_revenue_os` | نظام تشغيل الإيراد الكامل | شهري | 8,000 |
| `custom_company_os` | نظام المؤسسة المخصص | شهري | 20,000 |

عرض بـ `product_id` خارج الكتالوج = **غير صالح** ويفشل في فحص `client_revenue_delivery_check.py`.

---

## 5. حالات العرض وما يعنيها للعميل

| approval_status | ما يراه العميل | الإجراء |
|---|---|---|
| `draft` | لا يُعرَض بعد | في طور الإعداد الداخلي |
| `pending_founder_approval` | لا يُعرَض بعد | ينتظر مراجعة المؤسس |
| `founder_approved` | يُعرَض في البوابة | السعر نهائي، جاهز للمراجعة |
| `rejected` | إشعار بالرفض | يحتاج تعديلًا |

---

## 6. أمثلة واقعية

### TrainMe KSA — PROP-1001
- `product_id`: `revenue_leakage_diagnostic`
- `price_range_sar`: 2,500–5,000 SAR، `is_final=false`
- `approval_status`: `pending_founder_approval`
- **العميل لا يرى العرض بعد** — ينتظر موافقة المؤسس
- `evidence_level`: `client_reported`

### Digital Rise Agency — PROP-1002
- `product_id`: `revenue_leakage_diagnostic`
- `price_range_sar`: 2,500 SAR، `is_final=true`
- `approval_status`: `founder_approved`، وافق المؤسس بتاريخ 2026-06-02
- **العميل يرى العرض النهائي** في `/client/proposal`
- `evidence_level`: `client_data`

---

## 7. ما لا يحق للعميل رؤيته في البوابة

- المفاوضات الداخلية بين Dealix والمؤسس.
- تكاليف التشغيل أو هوامش الربح.
- بيانات عملاء آخرين.
- أي `secret_ref` أو tokens.

---

## الروابط المرجعية

- سكيمة العرض: `schemas/proposal.schema.json`
- كتالوج المنتجات: `data/catalog/product_catalog.json`
- SKUs المرجعية: [`company_os/revenue/proposals.json`](../../company_os/revenue/proposals.json)
- سياسة البوابة: [`SECURE_CLIENT_PORTAL_AR.md`](SECURE_CLIENT_PORTAL_AR.md)
- الدفع عبر البوابة: [`CLIENT_PAYMENT_HANDOFF_AR.md`](CLIENT_PAYMENT_HANDOFF_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
