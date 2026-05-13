# مكتبة مخططات البيانات — الدستور · المعايير التأسيسية

**الطبقة:** الدستور · المعايير التأسيسية
**المالك:** قائد البيانات
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [DATA_SCHEMA_LIBRARY.md](./DATA_SCHEMA_LIBRARY.md)

## السياق
تعمل سيور عمل Dealix على مجموعة صغيرة من مجموعات البيانات المتكررة في
كل ارتباط. لمنع إعادة اختراع أسماء الحقول وأنواعها وقواعد التحقق في كل
مشروع، تُعرِّف هذه المكتبة المخططات المعتمدة. ترتبط بـ
`docs/BEAST_LEVEL_ARCHITECTURE.md` لخط البيانات، وبـ
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` لطبقة التخزين الخلفية،
وبـ `docs/AI_STACK_DECISIONS.md` لهندسة المطالبات والتحقق. على كل
مجموعة بيانات في ارتباط Dealix أن تُعلن أي مخطط مكتبة تتطابق معه.

## الاصطلاحات
- أسماء الحقول snake_case.
- التواريخ والطوابع الزمنية بصيغة ISO 8601.
- أرقام الهاتف بصيغة E.164.
- الحقول الإلزامية مُعلَّمة `(required)`. غيرها اختياري.
- حقول البيانات الشخصية مُعلَّمة `(PII)` وتُفعّل قواعد
  `docs/governance/PDPL_DATA_RULES.md`.

## AccountSchema
سجل حساب أعمال يُستخدم في الإيرادات والعملاء والعمليات.

```json
{
  "company_name": "string (required)",
  "sector": "string (required)",
  "city": "string (required)",
  "source_type": "enum: referral|public|enrichment|client_supplied (required)",
  "allowed_use": "enum: research|outreach|service_delivery|none (required)",
  "relationship_status": "enum: cold|consented|existing_relationship|do_not_contact (required)",
  "website": "string",
  "contact_role": "string",
  "email": "string (PII)",
  "phone": "string (PII)",
  "estimated_size": "enum: 1-10|11-50|51-200|201-1000|1000+",
  "last_interaction_date": "date",
  "notes": "string (required)"
}
```

## LeadSchema
يمتد من AccountSchema مع حقول أنبوب البيع.

```json
{
  "$extends": "AccountSchema",
  "stage": "enum: new|qualified|engaged|opportunity|won|lost (required)",
  "owner": "string (required)",
  "source_event": "string (required)"
}
```

## SupportMessageSchema
رسالة عميل واردة.

```json
{
  "message_id": "string (required)",
  "channel": "enum: whatsapp|email|web|phone (required)",
  "timestamp": "datetime (required)",
  "customer_type": "enum: existing|prospect|unknown (required)",
  "category": "string",
  "resolution_status": "enum: open|in_progress|resolved|escalated"
}
```

## DocumentSchema
وثيقة داخلية تُستخدم لعقل الشركة.

```json
{
  "doc_id": "string (required)",
  "title": "string (required)",
  "owner": "string (required)",
  "last_updated": "date (required)",
  "sensitivity": "enum: low|medium|high (required)",
  "source_type": "enum: policy|sop|playbook|contract|email|other (required)",
  "allowed_users": ["string"]
}
```

## ProjectSchema
سجل ارتباط Dealix.

```json
{
  "project_id": "string (required)",
  "client_id": "string (required)",
  "service_id": "string (required)",
  "start_date": "date (required)",
  "end_date": "date",
  "capability_targets": ["string"],
  "owners": ["string"]
}
```

## الإصدارات
- تتبع إصدارات المخطط الترقيم الدلالي. إضافة حقول اختيارية تغيير ثانوي،
  وإعادة تسمية أو إزالة الحقول تغيير رئيسي.
- التغيير الرئيسي يتطلب مذكرة ترحيل في سجل التغييرات ونشرًا متوازيًا في
  النسخة العربية.
- كل مجموعة بيانات في الإنتاج تُعلن إصدار مخططها.

## الواجهات
| المدخلات | المخرجات | المالك | الوتيرة |
|---|---|---|---|
| بيانات العميل الخام | مجموعة بيانات مُطابقة | قائد البيانات | لكل مجموعة |
| طلب تعديل المخطط | إصدار مخطط مُعتمد | قائد البيانات | لكل تغيير |
| إصدار مخطط رئيسي | خطة ترحيل خط البيانات | قائد الخلفية | لكل تغيير رئيسي |

## المقاييس
- **معدل المطابقة للمخططات** — نسبة المجموعات في الإنتاج المطابقة
  لمكتبة المخططات. المستهدف: 100%.
- **عدد التفرعات** — مخططات محلية خارج المكتبة. المستهدف: 0.
- **زمن الترحيل** — أيام من إصدار رئيسي إلى ترحيل كل الخطوط. المستهدف:
  ≤ 30 يومًا.

## ذات صلة
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — معمارية خط البيانات.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — طبقة التخزين
  الخلفية.
- `docs/AI_STACK_DECISIONS.md` — قرارات النموذج والمطالبات.
- `docs/data/DATA_READINESS_STANDARD.md` — معيار الجاهزية المرجعي.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
