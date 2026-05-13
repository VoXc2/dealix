# قالب حزمة الإثبات — برنامج حوكمة الذكاء الاصطناعي

**الطبقة:** كتالوج الخدمات · العدّة التشغيلية
**المالك:** مراجِع الجودة
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [proof_pack_template.md](./proof_pack_template.md)

## السياق
القطعة الوحيدة القابلة للتدقيق لبرنامج حوكمة AI. يُخصِّص القالب الرئيس `docs/templates/PROOF_PACK_TEMPLATE.md` لخدمة طبقة الحوكمة. يرتبط بنظام حوكمة وقت التشغيل في `docs/governance/RUNTIME_GOVERNANCE.md` وسجل ادعاءات الاستراتيجية في `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## هيكل الحزمة
يحتوي المجلد:
1. `events.jsonl` — سجل أحداث للإلحاق فقط.
2. `summary.md` — ملخص بشري.
3. `evidence/` — مقتطفات جرد مُجهَّلة، شرائح سجل المخاطر، لقطات مصفوفة الضوابط، عيّنات سجل التدقيق.
4. `signoff.md` — توقيع DL + QA + GR + CL-cap + الراعي + DPO.
5. `anonymization_rules.md`.

## الأحداث المطلوبة
| الحدث | نوع القيمة | يُلتقَط بواسطة | المرحلة |
|---|---|---|---|
| `intake_completed` | bool | مهندس المبيعات | قبل الإطلاق |
| `program_initialized` | bool | DL | T-1 |
| `ai_uses_inventoried` | integer | GR | المرحلة 1 |
| `risks_logged` | integer | GR | المرحلة 1 |
| `data_flows_mapped` | integer | GR | المرحلة 1 |
| `lawful_basis_documented` | integer | CS-comp | المرحلة 1 |
| `approvals_documented` | integer | GR | المرحلة 2 |
| `policy_updates` | integer | CS-comp | المرحلة 2 |
| `controls_implemented` | integer | GR | المرحلة 3 |
| `incidents_addressed` | integer | CS-comp | المرحلة 3 |
| `audit_dry_run_complete` | bool | QA | المرحلة 3 |
| `training_delivered` | integer (جلسات) | GR | المرحلة 4 |
| `qa_phase_complete` | bool | QA | نهاية كل مرحلة |
| `program_delivered` | bool | DL | المرحلة 4 |
| `proof_pack_signed_off` | bool | الراعي + DPO | الأسبوع الأخير |
| `upsell_motion_triggered` | bool | DL/CSM | الأسبوع الأخير |

## أحداث اختيارية
- `sensitive_data_masked` (integer).
- `clinics_overlay_applied` (bool).
- `government_overlay_applied` (bool).
- `cross_border_flag_resolved` (bool).

## قواعد التجهيل
تجري فقط على موافقة نشر صريحة. نظرًا لحساسية محتوى الحوكمة، الافتراضي **عدم النشر**؛ استخدام صفحة الثقة يستلزم موافقة كتابية إضافية.

### القواعد
1. اسم العميل → `<Sector> enterprise (<Region>)`.
2. أسماء أدوات AI → مُعمَّمة ("LLM tool", "transcription tool").
3. نص السياسة → لا يُقتبَس حرفيًا.
4. محتويات سجل المخاطر → لا تُقتبَس.
5. تفاصيل مصفوفة الضوابط → الأعداد الهيكلية فقط قابلة للنشر، لا الصفوف المحدَّدة.
6. الأعداد → تقريب لأقرب 5.
7. PII → لا تُنشَر أبدًا.
8. الطبقات القطاعية (عيادات، حكومة، مالية) → تُنشَر فقط بموافقة إضافية.

### ما يمكن نشره
- استخدامات AI المُجرَدة (مُقرَّبة).
- المخاطر المُسجَّلة (مُقرَّبة).
- الضوابط المُنفَّذة (مُقرَّبة).
- الموافقات الموثَّقة (مُقرَّبة).
- جلسات التدريب المُسلَّمة (مُقرَّبة).
- تحرّك نضج حوكمة لا قطاعي (مثلًا: "من المستوى 2 إلى المستوى 4").
- شهادة المُشتري (بموافقة إضافية).

### ما لا يمكن نشره
- نص السياسة.
- تفاصيل سجل المخاطر.
- تفاصيل مصفوفة الضوابط.
- هوية المستشار.
- تفاصيل التعامل التنظيمي.

## إعادة الاستخدام للتسويق
تُغذّي الحزمة صفحة الثقة فقط عبر سكربت التصدير المُجهَّل + موافقة قطاعية. لا استخراج يدوي.

## التخزين والاحتفاظ
- مُشفَّرة في السكون في خزنة Dealix.
- الوصول: DL، QA، GR، CL-cap، CSM، قائد القدرة.
- الاحتفاظ: المشروع + 365 يومًا؛ المجموعات الفرعية الحساسة = المشروع + 60 يومًا.
- يُسجَّل الحذف.

## قالب كتلة التوقيع
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Capability Lead: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>
- DPO: <name>, <date>, <signature>

This proof pack accurately represents the AI Governance Program delivered
for <Client>. Publication is bounded by anonymization_rules.md. This pack
does not constitute legal advice.
```

## مثال عملي (توضيحي)
```
{"event":"ai_uses_inventoried","timestamp":"2026-05-22T17:00:00Z","actor_role":"GR","value":22,"notes":"Across 4 depts"}
{"event":"risks_logged","timestamp":"2026-05-23T17:00:00Z","actor_role":"GR","value":28,"notes":"Top 30 attempted; 28 ranked"}
{"event":"lawful_basis_documented","timestamp":"2026-05-26T15:00:00Z","actor_role":"CS-comp","value":15,"notes":"15 datasets"}
{"event":"approvals_documented","timestamp":"2026-06-05T16:00:00Z","actor_role":"GR","value":34,"notes":"34 use case patterns"}
{"event":"policy_updates","timestamp":"2026-06-10T15:00:00Z","actor_role":"CS-comp","value":5,"notes":""}
{"event":"controls_implemented","timestamp":"2026-06-19T17:00:00Z","actor_role":"GR","value":41,"notes":""}
{"event":"audit_dry_run_complete","timestamp":"2026-06-20T16:00:00Z","actor_role":"QA","value":true,"notes":"3 uses audited"}
{"event":"training_delivered","timestamp":"2026-07-03T15:00:00Z","actor_role":"GR","value":4,"notes":"exec, owner, builder, user"}
{"event":"program_delivered","timestamp":"2026-07-10T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| إصدار أحداث في الوقت الحقيقي | events.jsonl | كل الأدوار | مستمر |
| مراجعة الأسبوع الأخير | signoff.md | كل الموقّعين | الأسبوع الأخير |
| موافقة النشر | تصدير مُجهَّل | DL + التسويق | بعد التسليم |

## المقاييس
- **اكتمال التقاط الأحداث** — الهدف = 100%.
- **تأخر التوقيع** — الهدف ≤ 5 أيام عمل.
- **تدقيق التجهيل** — الهدف = 100%.
- **تسرّب النشر** — `count of publications without dual consent`. الهدف = 0.

## ذات صلة
- `docs/templates/PROOF_PACK_TEMPLATE.md` — الهيكل الرئيس
- `docs/quality/QUALITY_STANDARD_V1.md` — نظام الجودة
- `docs/capabilities/governance_capability.md` — مخطط القدرة
- `docs/governance/RUNTIME_GOVERNANCE.md` — حوكمة وقت التشغيل
- `docs/governance/AI_ACTION_TAXONOMY.md` — نظام الإجراءات
- `docs/governance/AI_ACTION_CONTROL.md` — ضبط الإجراءات
- `docs/enterprise/CONTROLS_MATRIX.md` — ضوابط المؤسسة
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/ops/PDPL_RETENTION_POLICY.md` — احتفاظ PDPL
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — الامتثال
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الخطة الاستراتيجية
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
