# الحوكمة كرمز — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الامتثال
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [GOVERNANCE_AS_CODE.md](./GOVERNANCE_AS_CODE.md)

## السياق
الوثائق وحدها لا توقف السلوك غير الآمن للذكاء الاصطناعي. يجب أن تكون
الحوكمة قابلة للتنفيذ في زمن التشغيل عبر وكيل حارس الامتثال وفي CI.
يحدّد هذا الملف نحو القواعد الذي تستخدمه ديلكس وتخطيط المحرّك المستهدف.
يكمل دستور `docs/DEALIX_OPERATING_CONSTITUTION.md` وانضباط التقييم في
`docs/AI_OBSERVABILITY_AND_EVALS.md` و`docs/EVALS_RUNBOOK.md`.

## المبدأ

> يجب أن تكون قواعد الحوكمة **قابلة للتنفيذ** و**مُؤرَّخة** و**قابلة
> للاختبار** — لا مجرد ملفات سياسة.

## نحو القواعد (تمثيلي)

- `no_cold_whatsapp`
  - IF `channel = whatsapp` AND `relationship_status != consented_or_existing`
  - THEN `block`.
- `no_guaranteed_claims`
  - IF `output contains guaranteed_sales_language`
  - THEN `rewrite_or_block`.
- `no_source_no_answer`
  - IF `answer has no source`
  - THEN `insufficient_evidence`.
- `pii_redaction_required`
  - IF `output contains phone | email | person_name`
  - AND `destination in {report, public}`
  - THEN `redact_or_require_basis`.

## البنية المستقبلية

```
governance_os/
  rules/
    no_cold_whatsapp.yaml
    no_guaranteed_claims.yaml
    no_source_no_answer.yaml
    pii_redaction_required.yaml
  engine.py
  tests/
```

- `rules/*.yaml` — قواعد إقرارية بمعرّف وإصدار ومحفّز وفعل.
- `engine.py` — يقيّم القواعد ويُصدر `GuardVerdict`.
- `tests/` — اختبارات تثبّت السلوك وتُشغَّل في CI عند كل تغيير.

## دورة حياة القاعدة

```
propose → review → test → publish → pin → monitor → deprecate
```

كل قاعدة لها مالك ومعرّف علني وإصدار. التغييرات تشحن عبر PR مع اختبارات
جديدة. يحمّل وكيل حارس الامتثال حزمة سياسة مثبّتة ويعلن إصدارها داخل كل
حكم.

## الأنماط الخاطئة

- قواعد خفية مدمجة في الموجِّهات.
- قواعد بلا اختبارات.
- قواعد بلا مالك.
- تغيير القواعد في الإنتاج بدون حزمة مُؤرَّخة.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Rule proposals | Reviewed YAML rules | Head of Compliance | Per change |
| Engine + rules | GuardVerdict | Compliance Guard Agent | Per action |
| Test fixtures | CI pass/fail | Eng + Compliance | Per PR |
| Production runs | Rule effectiveness telemetry | Control Tower | Continuous |

## المقاييس
- Rule Coverage — نسبة فئات الإجراءات المربوطة بقاعدة واحدة على الأقل.
- Test Coverage — نسبة القواعد ذات الاختبارات.
- Rule Drift — الفرق بين السياسة المقصودة والـ YAML المشحون.
- Block-to-Cause Closure — القواعد التي تُحذف أو تُعاد هيكلتها بعد إصلاح الجذر.

## ذات صلة
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — مصدر القواعد
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — تغطية التقييم
- `docs/EVALS_RUNBOOK.md` — تشغيل التقييمات
- `docs/product/agent_cards/compliance_guard_agent.md` — منفّذ زمن التشغيل
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
