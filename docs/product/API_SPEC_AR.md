# مواصفات الواجهة البرمجية — الدستور · المعايير التأسيسية

**الطبقة:** الدستور · المعايير التأسيسية
**المالك:** قائد الخلفية
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [API_SPEC.md](./API_SPEC.md)

## السياق
هذا الملف عقد نقاط النهاية الأدنى لمنصة Dealix. كل نقطة تحكمها بوابة
النماذج ومصفوفة الموافقات وحوكمة وقت التشغيل. تكمّل المرجع
`docs/API_REFERENCE.md` وخطة التقوية
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`، والشقيق
`docs/product/MANAGEMENT_API_SPEC.md` (L2). العملاء الخارجيون يستهلكون
v1 فقط؛ v0 داخلية.

## الاصطلاحات
- المسار الأساسي: `/api/v1`.
- المصادقة: رمز bearer مربوط ببيئة.
- الإيدمبوتنسي: كل نقطة تعديل تقبل ترويسة `Idempotency-Key`.
- الأخطاء: JSON يحوي `error_code` و`message` و`correlation_id`.
- الوقت: ISO 8601 UTC.

## نقاط النهاية
- `POST /api/v1/data/import-preview` — معاينة بيانات قبل الالتزام،
  ترجع المطابقة للمخطط وقيمة DRS مبدئية.
- `POST /api/v1/data/quality-score` — حساب DRS لمجموعة مُسجَّلة.
- `POST /api/v1/governance/check` — تشغيل حوكمة وقت التشغيل ضد فعل
  مرشَّح.
- `POST /api/v1/revenue/score-accounts` — تقييم حسابات لقدرة
  الإيرادات.
- `POST /api/v1/revenue/draft-pack` — إنتاج مسودة إيرادات (تخضع
  للجودة والموافقة).
- `POST /api/v1/reporting/proof-pack` — توليد حزمة إثبات من أحداث
  التدقيق والذكاء والجودة.
- `POST /api/v1/delivery/qa-score` — تسجيل درجة جودة لمسودة.
- `POST /api/v1/capital/assets` — تسجيل أو عرض الأصول الرأسمالية.
- `GET  /api/v1/founder/command-center` — لوحة قيادة المؤسس.

## شكل الاستجابة الموحد
كل نقطة تُرجع الغلاف التالي. الحقول الخاصة بالنتيجة تحت `result`،
وبقية المفاتيح حوكمة يجب على كل مستهلك احترامها.

```json
{
  "result": {},
  "risk_status": "medium",
  "governance_status": "approved_with_review",
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

`risk_status`: `low | medium | high | critical`.
`governance_status`: `approved | approved_with_review | draft_only |
requires_approval | redacted | blocked | escalated`.
`next_action`: `none | human_review | request_approval | remediate |
block_and_alert`.

## حدود المعدل
- 60 طلبًا في الدقيقة لكل بيئة للقراءة.
- 20 طلبًا في الدقيقة لكل بيئة للكتابة.
- نقاط مدعومة ببوابة النماذج (الإيرادات، التقارير) تخضع لضابط تكلفة
  البوابة.

## الإصدارات
- التغييرات الجارفة تتطلب مسار إصدار جديد (`/api/v2`).
- الإضافات داخل v1 عبر علم `min_capability` في الطلب.

## التدقيق والإيدمبوتنسي
- كل طلب يكتب `AuditEvent` ويُرجع `audit_event_id`.
- إعادة تشغيل بنفس `Idempotency-Key` تُرجع نفس الاستجابة لمدة 24
  ساعة.

## الواجهات
| المدخلات | المخرجات | المالك | الوتيرة |
|---|---|---|---|
| طلب تعديل OpenAPI | إصدار مواصفات | قائد الخلفية | لكل تغيير |
| مسودة نقطة نهاية | سجل مراجعة حوكمة | قائد الحوكمة | لكل نقطة |
| سياسة ضابط التكلفة | تفعيل البوابة | قائد منصة الذكاء | لكل تغيير |
| تكامل عميل | مذكرة ترحيل | قائد الخلفية | لكل تغيير |

## المقاييس
- **توافر النقطة p99** — المستهدف: ≥ 99.5%.
- **زمن الاستجابة الوسيط** — ≤ 800 مللي ثانية لغير LLM.
- **معدل الحظر الحوكمي** — يُرفع أسبوعيًا.
- **صحة إعادة الإيدمبوتنسي** — 100%.

## ذات صلة
- `docs/API_REFERENCE.md` — المرجع العام.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — تقوية الخلفية.
- `docs/product/MANAGEMENT_API_SPEC.md` — واجهة الإدارة (L2).
- `docs/product/LLM_GATEWAY.md` — رفيق بوابة النماذج.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
