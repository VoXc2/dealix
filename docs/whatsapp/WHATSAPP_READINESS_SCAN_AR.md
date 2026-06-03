# فحص الجاهزية (Readiness Scan)
## الأبعاد العشرة، الدرجات الثلاث، والتوصية

> **الغرض:** يشرح هذا المستند كيفية عمل فحص الجاهزية داخل محادثة واتساب — الأبعاد العشرة التي تُقيَّم، الدرجات الثلاث المركّبة، مستوى المخاطرة، المنتج الموصى به، والخطوة التالية الأفضل (`next_best_action`).  
> مرجع السكيمة: `schemas/client_assessment.schema.json`.  
> مثال حقيقي: تقييم `CAS-0002` لـ TrainMe KSA.

---

## 1. كيف يبدأ الفحص؟

يُفعَّل تدفق `readiness_scan` من:
- اختيار "ابدأ فحص الجاهزية" في الترحيب (`welcome_after_consent`)
- تدفق "ما أعرف — اقترح علي" (`dont_know_suggest`)

**الشرط المسبق:** جلسة `WAS-xxxx` نشطة بـ`consent_basis` موثّق.

---

## 2. الأبعاد العشرة (dimensions)

كل بُعد يُقيَّم من 0 إلى 5 بناءً على ردود العميل في واتساب أو استيراد البيانات.

| # | اسم البُعد (schema) | السؤال الموجّه في واتساب |
|---|---|---|
| 1 | `lead_flow` | تدفّق العملاء المحتملين — كيف يصلكم العملاء؟ |
| 2 | `followup_maturity` | كيف متابعتكم للعملاء بعد أول رد؟ |
| 3 | `crm_data_readiness` | هل لديكم CRM أو قاعدة بيانات منظّمة؟ |
| 4 | `reporting_maturity` | هل عندكم تقارير دورية عن المبيعات؟ |
| 5 | `urgency` | ما مدى استعجالكم للتحسين؟ |
| 6 | `budget_fit` | هل الميزانية متاحة لاستثمار في النمو؟ |
| 7 | `decision_maker_access` | هل صاحب القرار يشارك في هذا النقاش؟ |
| 8 | `compliance_sensitivity` | هل صناعتكم لها متطلبات امتثال خاصة؟ |
| 9 | `automation_readiness` | هل جرّبتم أي أتمتة للعمليات؟ |
| 10 | `first_workflow_fit` | ما العملية الأسهل للأتمتة أولًا؟ |

**ملاحظة:** أسئلة واتساب التفاعلية تغطي أبعاد 1-5 مباشرةً (وهي الحد الأدنى). الأبعاد 6-10 قد تُستكمل في البوابة أو من بيانات العميل.

---

## 3. الدرجات الثلاث المركّبة (scores) — كل منها 0-100

| الدرجة (schema) | ما تقيسه | يُؤثر على |
|---|---|---|
| `revenue_readiness` | الجاهزية العامة لتحسين الإيراد | اختيار نوع المنتج (P1 vs P2) |
| `followup_maturity` | نضج عملية المتابعة | الحاجة لـ`followup_recovery_workflow` |
| `automation_readiness` | قدرة تبني الأتمتة | الحاجة لـ`ai_revenue_ops_starter` |

**قانون الحساب (مُبسَّط):**
```
revenue_readiness  = وزن(lead_flow + followup_maturity + crm_data_readiness + reporting_maturity) × 5
followup_maturity  = followup_maturity × 20
automation_readiness = (automation_readiness + first_workflow_fit) × 10
```
الحساب الفعلي يُنفَّذ في خطوة `compute_scores` في تدفق `readiness_scan`.

---

## 4. جدول التفسير والتوصية

| revenue_readiness | followup_maturity | المنتج الموصى به | product_id |
|---|---|---|---|
| 0–40 | أي | تشخيص تسرب الإيراد (P1 Sprint) | `revenue_leakage_diagnostic` |
| 41–60 | < 40 | سير عمل استرداد المتابعة | `followup_recovery_workflow` |
| 41–60 | ≥ 40 | فحص الجاهزية + استشارة | `readiness_scan` |
| 61–80 | أي | نظام عمليات الإيراد بالذكاء | `ai_revenue_ops_starter` |
| 81–100 | أي | نظام الإيراد الكامل | `full_revenue_os` |

**قاعدة:** `recommended_product_id` يجب أن يكون في كتالوج المنتجات `data/catalog/product_catalog.json`.

---

## 5. مستوى المخاطرة (risk_level)

| الحالة | risk_level |
|---|---|
| درجات مرتفعة، قرار سريع غير موثّق | `high` |
| بيانات عميل متوسطة، متطلبات امتثال | `medium` |
| فحص استكشافي فقط | `low` |
| بيانات PII حساسة أو صناعة مالية/صحية | `critical` |

يُسجَّل `risk_level` في `client_assessment` ويؤثر على مسار الموافقة.

---

## 6. مستوى الدليل (evidence_level)

كل تقييم يحمل `evidence_level` إلزامي:

- فحص واتساب فقط → `client_reported`
- بيانات CRM فعلية مُستوردة → `client_data`
- قياس أثناء التسليم → `measured`

**لا يجوز استخدام `none` كأساس لتوصية.** انظر `AGENTS.md §6`.

---

## 7. next_best_action

حقل نصي يصف الخطوة التالية الموصى بها، مثل:
- `"book_discovery_or_start_sprint"` — (TrainMe KSA، CAS-0002)
- `"schedule_scoping_call"`
- `"upload_crm_data_to_portal"`

يظهر في رسالة `service_recommendation` في واتساب.

---

## 8. مثال حقيقي — CAS-0002 (TrainMe KSA)

```json
{
  "id": "CAS-0002",
  "company": "TrainMe KSA",
  "dimensions": {
    "lead_flow": 4,
    "followup_maturity": 1,
    "crm_data_readiness": 2,
    "reporting_maturity": 1,
    "urgency": 4
  },
  "scores": {
    "revenue_readiness": 52,
    "followup_maturity": 30,
    "automation_readiness": 40
  },
  "risk_level": "medium",
  "recommended_product_id": "revenue_leakage_diagnostic",
  "next_best_action": "book_discovery_or_start_sprint",
  "evidence_level": "client_reported"
}
```

**تفسير:** درجة الجاهزية 52 مع نضج متابعة ضعيف (30) → يوصى بتشخيص تسرب الإيراد أولًا. الدليل مصدره العميل (client_reported).

---

## 9. ماذا يحدث بعد التقييم؟

```
CAS-xxxx مُكتمل
      │
      ▼
service_recommendation (واتساب)
  "الخطوة المقترحة: {product_name} | الدليل: {evidence_level}"
      │
      ├─ [ابغى التفاصيل]      → proposal_review (البوابة)
      ├─ [رتّبوا مكالمة]      → book_call → human_handoff
      └─ [ما أعرف — اقترح علي] → dont_know_suggest
```

---

## مراجع

- `schemas/client_assessment.schema.json`
- `data/whatsapp/client_assessments.jsonl` (مثال: CAS-0002)
- `data/whatsapp/flows.yaml` (تدفق: `readiness_scan`, `service_recommendation`)
- `data/catalog/product_catalog.json`
- `AGENTS.md §6` (evidence_level) و`§9` (كتالوج المنتجات)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
