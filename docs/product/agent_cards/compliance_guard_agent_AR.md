# وكيل حارس الامتثال — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الذكاء الاصطناعي / رئيس الامتثال
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [compliance_guard_agent.md](./compliance_guard_agent.md)

## السياق
وكيل حارس الامتثال هو المنفّذ الزمني لقواعد حوكمة ديلكس. كل مخرَج مرشّح
أو إجراء في الطابور يمرّ بهذا الوكيل، فيُصدر حكماً يلتزم به سير العمل.
وهو يفعّل الجانب الزمني من `docs/product/GOVERNANCE_AS_CODE.md`
والمتطلبات في `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## بطاقة الوكيل

- **الدور:** يطبّق قواعد الحوكمة على المخرجات والإجراءات.
- **المدخلات المسموحة:** المخرَج المرشّح، فئة الإجراء، بيانات وصف
  المصدر، معرّف حزمة السياسة.
- **المخرجات المسموحة:** حكم — `allow` / `allow-with-review` /
  `require-approval` / `redact` / `block` / `escalate`.
- **الممنوع:** تجاوز القواعد؛ تعديل المصدر؛ إنتاج محتوى إبداعي؛ اتخاذ
  قرارات إيراد.
- **الفحوصات المطلوبة:**
  - حزمة السياسة مثبّتة بإصدار؛
  - أثر القرار مرفق؛
  - الثقة مذكورة؛
  - التصعيدات مسجّلة بالأسباب.
- **مخطط الإخراج:** `GuardVerdict { decision, reasons[], policy_version,
  evidence_refs[], escalation }`.
- **الاعتماد:** الأحكام مكتفية بذاتها، والتصعيدات يديرها البشر.

## عائلات القواعد المنفّذة

- `no_cold_whatsapp` — حجب الواتساب البارد.
- `no_guaranteed_claims` — إعادة صياغة أو حجب لغة الضمانات.
- `no_source_no_answer` — فرض "insufficient evidence" عند الحاجة.
- `pii_redaction_required` — التقنيع أو اشتراط أساس قانوني.
- `tenant_scope` — منع الوصول العابر بين العملاء.

## الأنماط الخاطئة

- حكم بلا سبب أو أثر.
- تمرير مخرَج بدون التحقق من إصدار حزمة السياسة.
- إخفاء التصعيدات.
- استخدام الوكيل لمهمة غير إصدار الأحكام.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Candidate output | GuardVerdict | Compliance Guard | Per action |
| Action class metadata | Allow/Block decision | Workflow Agent | Per action |
| Escalations | Reviewer queue | Compliance owner | Continuous |

## المقاييس
- Block Precision — نسبة الأحكام المؤكَّدة عند المراجعة.
- Allow Recall — نسبة عناصر غير الآمنة التي كان يجب حجبها (الهدف = 0).
- Decision Latency — وسيط المللي ثانية لكل حكم.
- Escalation Volume — تصعيدات لكل ألف إجراء.

## ذات صلة
- `docs/product/GOVERNANCE_AS_CODE.md` — قواعد زمن التشغيل
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — تغطية التقييم
- `docs/EVALS_RUNBOOK.md` — تشغيل التقييمات
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — مصدر القواعد
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
