# نية محركات التسليم — ربط المنتج بـ Dealix Method

**المنهجية:** [`../company/DEALIX_METHOD_AR.md`](../company/DEALIX_METHOD_AR.md) — المراحل الثماني: Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand.

هذه الوثيقة تصف **نية المنتج** (ماذا يجب أن يدعم النظام) وليست واجهة API نهائية.

---

## 1) مشروع يتبع المراحل

في الواجهة/نموذج المشروع مستقبلاً:

- المرحلة الحالية (Discover … Expand).
- checklists لكل مرحلة.
- المعوّقات (blockers) وقرارات العميل.
- QA score وحالة Proof Pack وupsell المقترح.

---

## 2) Quality Engine

تقييم كل مخرج حسب محاور مثل: Business Quality، Data Quality، AI Output Quality، Arabic Quality، Compliance، Reusability، Upsell Clarity — مع حد أدنى تسليم كما في [`../quality/QA_DELIVERY_RUBRIC_AR.md`](../quality/QA_DELIVERY_RUBRIC_AR.md).

---

## 3) Governance Engine

فحوصات: مصدر البيانات، PII، أساس نظامي حيث ينطبق، مخاطر إرسال خارجي، ادعاءات غير مدعومة، حاجة موافقة، سجل تدقيق — انظر [`../governance/GOVERNANCE_SERVICE_CHECKS_AR.md`](../governance/GOVERNANCE_SERVICE_CHECKS_AR.md).

---

## 4) Proof Engine

توليد: Proof Pack، before/after، مؤشرات أثر، ملخص جاهز للعميل، توصية تجديد/upsell — انظر [`reporting_os`](../../auto_client_acquisition/reporting_os/) و[`../templates/proof_pack.md`](../templates/proof_pack.md).

---

## 5) Playbook Engine

اختيار قالب حسب: القطاع، الخدمة، حجم الشركة، الهدف، جودة البيانات، مستوى المخاطر — مصدر المحتوى: [`../strategy/VERTICAL_PLAYBOOKS.md`](../strategy/VERTICAL_PLAYBOOKS.md) + `docs/services/*/`.

---

## 6) Learning Engine

بعد الإغلاق: what worked / failed، template جديد، اعتراض مبيعات، KPI، مرشّح feature — انظر [`../strategy/CONTENT_AND_LEARNING_LOOP_AR.md`](../strategy/CONTENT_AND_LEARNING_LOOP_AR.md).

---

## 7) Growth Engine

قمع: Content → Diagnostic call → Sprint → Pilot → Retainer → Enterprise → Referral.  
سلّم العروض (مثال): audit منخفض التكلفة / تشخيص → Revenue Diagnostic → Lead Intelligence → Pilot Conversion → Monthly RevOps → Enterprise AI OS — تفاصيل في [`../company/DEALIX_AI_OS_LONG_TERM_AR.md`](../company/DEALIX_AI_OS_LONG_TERM_AR.md) (قسم «Quality / Proof / Governance / Growth»).

---

## ربط بالحزم في الريبو

| نية | حزم كود ذات صلة |
|-----|------------------|
| Data / جاهزية | `auto_client_acquisition/data_os/` |
| Revenue | `auto_client_acquisition/revenue_os/` |
| Governance | `auto_client_acquisition/governance_os/`، `compliance_os` |
| Reporting / Proof | `auto_client_acquisition/reporting_os/`، `executive_reporting/` |
| Delivery / جاهزية خدمة | `auto_client_acquisition/delivery_os/` |
| AI موحّد | [`LLM_GATEWAY_INTENT_AR.md`](LLM_GATEWAY_INTENT_AR.md)، `llm_gateway_v10/` |

خرائط أوسع: [`MODULE_MAP.md`](MODULE_MAP.md).
