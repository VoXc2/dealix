# محرك التجديد — Renewal Engine

> **السكيمة:** `schemas/renewal.schema.json` | **البيانات:** `data/renewals/renewals.jsonl` | **المستوى:** L3 Draft → L4 Act with Approval

---

## القاعدة الصارمة: لا تجديد بلا قيمة مُسلَّمة

```
┌─────────────────────────────────────────────────────────────────┐
│  HARD RULE: NO RENEWAL WITHOUT DELIVERED VALUE                  │
│  evidence_level MUST ∈ {client_data, measured, verified}        │
│  cites_delivered_value MUST be non-empty                        │
│  approval_required MUST be true (const)                         │
│  suggested_next_step: ONE step only — no pressure               │
└─────────────────────────────────────────────────────────────────┘
```

هذه القاعدة **غير قابلة للتفاوض**. تُطبَّق برمجيًا في `scripts/client_revenue_delivery_check.py` وفي الاختبارات. كل مسودة REN-* تفشل الفحص إذا خالفت أيًا من هذه الشروط.

---

## 1. بنية سجل التجديد REN-*

مستمدة من `renewal.schema.json`:

| الحقل | النوع | الوصف | هل إلزامي؟ |
|---|---|---|---|
| `id` | string | معرّف بنمط `REN-[...]` | ✅ |
| `created_at` | datetime | توقيت إنشاء المسودة | ✅ |
| `company` | string | اسم شركة العميل | ✅ |
| `product_id` | string | المنتج الحالي — يجب أن ∈ الكتالوج | ✅ |
| `trigger` | enum | المحفز من القائمة المعتمدة | ✅ |
| `cites_delivered_value` | array[string] | الأدلة — مرجع WVR + الرقم | ✅ (minItems: 1) |
| `evidence_level` | enum | يجب أن ∈ {client_data, measured, verified} | ✅ |
| `suggested_next_step` | string | خطوة واحدة فقط | ✅ |
| `approval_required` | boolean | ثابت `true` دائمًا | ✅ |
| `approved` | boolean | يبدأ `false`، يُعدَّل بموافقة المؤسس | ✅ |
| `approved_by` | string\|null | اسم المؤسس بعد الموافقة | — |
| `status` | enum | draft → pending_approval → approved → sent_manually → renewed / declined | ✅ |

---

## 2. محفزات التجديد المعتمدة

الحقل `trigger` يقبل القيم التالية فقط:

| القيمة | الحالة التي تُفعّله |
|---|---|
| `first_successful_workflow` | Workflow أول أُسلِّم وأثبت نتيجة `measured` |
| `weekly_value_proof` | WVR أسبوعي يحتوي رقمًا `measured`/`verified` |
| `positive_feedback` | العميل أعرب صراحةً عن رضاه (موثَّق) |
| `21_30_days_post_delivery` | مرت 21–30 يومًا على التسليم مع توافر القيمة |
| `new_department_need` | العميل ذكر حاجة إدارة جديدة |
| `new_campaign_or_source` | العميل أطلق حملة أو مصدر جديد |
| `delivery_milestone` | إنجاز milestone رئيسي مُوثَّق |

**قاعدة:** لا تُعيَّن قيمة `trigger` إذا لم تكن الحالة موثَّقة في البيانات.

---

## 3. دورة حياة سجل REN-*

```
draft
  ↓ (كتابة الذكاء الاصطناعي L3)
pending_approval
  ↓ (مراجعة المؤسس)
approved  ←── رفض → declined
  ↓ (إرسال يدوي L4)
sent_manually
  ↓
renewed  ←── رفض العميل → declined
```

**يُمنع التخطي:** لا يمكن الانتقال من `draft` مباشرة إلى `sent_manually` — الموافقة إلزامية.

---

## 4. شروط الانتقال بين الحالات

| من | إلى | الشرط |
|---|---|---|
| draft | pending_approval | المسودة مكتملة وتجتاز الفحص |
| pending_approval | approved | موافقة المؤسس مع تسجيل `approved_by` + `approved_at` |
| pending_approval | declined | المؤسس رفض مع توثيق السبب |
| approved | sent_manually | إرسال يدوي من المؤسس (لا إرسال آلي في v1) |
| sent_manually | renewed | العميل وافق وبدأ التجديد |
| sent_manually | declined | العميل رفض (مع توثيق السبب) |

---

## 5. الفحص الآلي (Validation)

`scripts/client_revenue_delivery_check.py` يرفض أي سجل REN-* إذا:

```python
# شروط الرفض الآلي:
if evidence_level not in {"client_data", "measured", "verified"}:
    FAIL("evidence_level ضعيف")

if not cites_delivered_value or len(cites_delivered_value) == 0:
    FAIL("cites_delivered_value فارغ")

if not approval_required:
    FAIL("approval_required يجب أن يكون true")

if product_id not in valid_product_ids:
    FAIL("product_id غير موجود في الكتالوج")

if trigger not in VALID_TRIGGERS:
    FAIL("trigger غير معتمد")
```

---

## 6. ربط التجديد بالمنتجات (product_id)

كل سجل REN-* يشير إلى `product_id` من `data/catalog/product_catalog.json`. التجديد يعني الاستمرار بنفس المنتج أو الانتقال للتالي في السلّم.

| product_id | الاسم | التجديد الطبيعي |
|---|---|---|
| `revenue_leakage_diagnostic` | تشخيص تسرب الإيراد (P1) | الانتقال لـ `followup_recovery_workflow` أو `ai_revenue_ops_starter` |
| `ai_revenue_ops_starter` | باقة مبتدئ (3,000 SAR/شهر) | الاستمرار شهريًا أو الترقية لـ `full_revenue_os` |
| `full_revenue_os` | باقة كاملة (8,000 SAR/شهر) | الاستمرار شهريًا أو إضافة `monthly_optimization` |
| `custom_company_os` | مخصص (20,000 SAR/شهر) | الاستمرار أو `multi_department_rollout` |

---

## 7. ربط التجديد بصحة العميل

محرك التجديد يعمل دائمًا بالتوازي مع سجل CHS-*:

```
CHS-* (health_band: green, value_proof: true, evidence_level: measured)
                          ↓
             تقييم renewal_fit (strong/possible)
                          ↓
             [strong] → فتح باب التجديد فورًا
             [possible] → انتظر WVR إضافي
             [not_yet / at_risk] → لا تجديد الآن
```

---

## 8. مثال حقيقي — REN-1001

من `data/renewals/renewals.jsonl`:

**العميل:** Digital Rise Agency
**المحفز:** `weekly_value_proof` — WVR-1001 أثبت تحسّن نسبة المتابعة من 43% إلى 61% (measured)
**الحالة:** `draft` — تنتظر موافقة المؤسس

```
health_score: 82 (CHS-1001, green, renewal_fit: strong)
       ↓
trigger: weekly_value_proof
       ↓
cites_delivered_value: ["WVR-1001: 43%→61% measured", "12 فرصة مُستردّة"]
       ↓
evidence_level: measured ✅
       ↓
suggested_next_step: "الاستمرار بباقة شهرية لتثبيت المكسب."
       ↓
approval_required: true → انتظار موافقة المؤسس
```

---

## 9. مراجع مرتبطة

| المستند | الدور |
|---|---|
| `docs/customer_success/RENEWAL_PLAYBOOK_AR.md` | متى وكيف يُفتح باب التجديد |
| `docs/renewal/CLIENT_VALUE_PROOF_AR.md` | كيف نوثّق القيمة المُسلَّمة |
| `docs/renewal/RENEWAL_MESSAGING_AR.md` | صياغة رسائل التجديد |
| `docs/renewal/UPSELL_LADDER_AR.md` | الترقية بعد التجديد |
| `schemas/renewal.schema.json` | السكيمة الكاملة |
| `data/renewals/renewals.jsonl` | سجلات التجديد الحقيقية |

---

*آخر تحديث: 2026-06-03 | السكيمة: [renewal.schema.json](../../schemas/renewal.schema.json) | مرجع: [AGENTS.md](../../AGENTS.md)*
