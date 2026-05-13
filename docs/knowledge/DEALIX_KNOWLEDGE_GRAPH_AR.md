# الرسم المعرفي لديلكس — طبقة رأس المال

**الطبقة:** L1 · Capital Model
**المالك:** المؤسس
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [DEALIX_KNOWLEDGE_GRAPH.md](./DEALIX_KNOWLEDGE_GRAPH.md)

## السياق
Knowledge Graph هو الخريطة المفاهيمية التي تربط القطاعات،
والمشكلات، والخدمات، والمدخلات، والمخرجات، و KPIs، والأدلة،
والمخاطر، والحوكمة، و Playbooks. هي البنية التي تمنع الشركة من حلّ
المشكلة نفسها مرّتَين، وتضمن أن كل مشروع جديد يلتحم بالمعرفة
المتراكمة. تُكمّل `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` بجعل
الاستراتيجية قابلة للقراءة الآلية، وتدعم موقف الرصد المُعرَّف في
`docs/AI_OBSERVABILITY_AND_EVALS.md`.

## العلاقات الأساسية

- **Sector** لديه **Problems**.
- **Problems** ترتبط بـ **Services**.
- **Services** تتطلّب **Inputs**.
- **Services** تُنتج **Outputs**.
- **Outputs** ترتبط بـ **KPIs**.
- **KPIs** تُولّد **Proof**.
- **Risks** تتطلّب **Governance Controls**.
- الأنماط المتكرّرة تصبح **Playbooks**.

## سلسلة مثال

> B2B Services → messy leads → Lead Intelligence Sprint → CSV / CRM
> export → top 50 accounts + drafts → pipeline clarity → source /
> consent risk → B2B Services Playbook.

تُقرأ من البداية إلى النهاية: قطاع (خدمات B2B) يحمل مشكلة متكرّرة
(Leads فوضوية). تُحال المشكلة إلى خدمة (Lead Intelligence Sprint).
تستهلك الخدمة مُدخلاً (تصدير CRM) وتُنتج مُخرَجاً (أفضل 50 حساباً مع
مسوّدات). يُقاس المُخرَج بـ KPI (وضوح Pipeline). يُولّد الـ KPI
دليلاً. يظهر في الأثناء خطر (المصدر / الموافقة) يتطلّب ضابط حوكمة.
وعند تكرار النمط لدى 3+ عملاء يصبح Playbook.

## أنواع العقد

| العقدة | أمثلة |
|---|---|
| Sector | B2B Services, Clinics, Retail, Manufacturing, Finance |
| Problem | Messy leads, slow support, lost knowledge, manual reporting |
| Service | Lead Intelligence Sprint, Company Brain Sprint, Support Desk Sprint |
| Input | CRM export, support tickets, internal documents, financial logs |
| Output | Ranked accounts, indexed answers, automated replies |
| KPI | Hours saved, qualified accounts, response time, error rate |
| Proof | Proof pack, case study, audit log, benchmark snapshot |
| Risk | Source quality, consent, PII exposure, vendor lock-in |
| Governance | Approval gates, retention rules, audit logging |
| Playbook | دليل تشغيلي خاص بالقطاع |

## قواعد الحواف

- كل Service يجب أن يحمل حافة خارجة واحدة على الأقل إلى Output.
- كل Output يجب أن يحمل حافة خارجة واحدة على الأقل إلى KPI.
- كل Risk يجب أن يحمل حافة خارجة واحدة على الأقل إلى Governance.
- يُنشَأ Playbook تلقائياً عند تكرار سلسلة Sector → Service → Output
  بنجاح في 3+ مشاريع.

## التخزين والأدوات

يعيش الرسم ابتداءً كجدول مهيكل في مساحة العمل الداخلية. يُصدَّر
ربعياً إلى تمثيل قابل للاستعلام (JSON / Graph DB) حين يبرّر الحجم
الجهد الهندسي. حتى ذلك الحين، يخدم كنموذج ذهني مشترك ومصدر تغذية لـ
IP Registry.

## الواجهات
| المدخلات | المخرجات | الملاك | الإيقاع |
|---|---|---|---|
| موجز استلام المشروع | عقد Sector / Problem جديدة | المؤسس | لكل مشروع |
| تقرير الإقفال | عقد Output / KPI / Proof جديدة | قائد التسليم | لكل مشروع |
| مراجعة الحوكمة | عقد Risk / Control جديدة | المؤسس | لكل مشروع |
| مراجعة الأنماط | عقد Playbook جديدة | المؤسس | ربعياً |

## المقاييس
- Node growth — عقد جديدة لكل ربع؛ الهدف ≥ 20.
- Coverage — نسبة الخدمات النشطة ذات سلسلة Sector → Problem → Service → Output → KPI → Proof مكتملة؛ الهدف ≥ 80%.
- Playbook conversion — نسبة أنماط Sector→Service المتكرّرة التي أنتجت Playbook؛ الهدف ≥ 70%.
- Risk coverage — نسبة عقد Risk بضابط حوكمة واحد على الأقل؛ الهدف 100%.

## ذات صلة
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — بيانات الرصد التي تصبح عقد Proof.
- `docs/AI_STACK_DECISIONS.md` — مكدّس الذكاء الاصطناعي الذي يعتمد عليه الرسم في الاسترجاع.
- `docs/COMPETITIVE_POSITIONING.md` — الرسم يميّز ديلكس عن البائعين العامّين للذكاء الاصطناعي.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — رأس مال المعرفة الذي يُجسّده هذا الرسم.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي.

## سجل التغييرات
| التاريخ | المؤلف | التغيير |
|---|---|---|
| 2026-05-13 | سامي | المسودة الأولى |
