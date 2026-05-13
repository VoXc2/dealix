# مصفوفة الإنسان في الحلقة — منظومة تحقيق القيمة

**الطبقة:** L3 · منظومة تحقيق القيمة
**المالك:** رئيس الامتثال
**الحالة:** مسودة
**آخر مراجعة:** 2026-05-13
**النسخة الإنجليزية:** [HUMAN_IN_THE_LOOP_MATRIX.md](./HUMAN_IN_THE_LOOP_MATRIX.md)

## السياق
مصفوفة الإنسان في الحلقة هي المرجع الأوحد لما يجوز للذكاء الاصطناعي
فعله، وأين يجب أن يعتمد الإنسان، وما هو ممنوع تماماً. تختصر عشرات
القواعد المتفرقة في مصفوفة مقروءة، وتشير إليها كل بطاقات الوكلاء.
وهي تنفّذ موقف الاستقلالية المعلَن في
`docs/DEALIX_OPERATING_CONSTITUTION.md` وانضباط الحوادث في
`docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`.

## المصفوفة

| AI Action | Risk | Human Role | Approval Required |
|---|---|---|---|
| classify data | Low | reviewer spot-checks | No |
| score leads | Medium | delivery owner reviews top accounts | Yes before delivery |
| draft email | Medium | human approves before use | Yes |
| answer from KB | Medium | source check required | For external use |
| update CRM stage | Medium | owner approval | Yes |
| send message | High | explicit approval + consent | Yes |
| publish claim | High | claim QA | Yes |
| autonomous external action | Critical | not allowed | Blocked |

## موقف MVP

- القراءة / التصنيف / الصياغة / التوصية — مسموح بها مع جودة.
- التنفيذ الخارجي — محجوب أو بموافقة فقط.
- التنفيذ الخارجي المستقل — غير مسموح.

## تدفق القرار

```
candidate action
   │
   ▼
classify by AI Action
   │
   ▼
look up row in matrix
   │
   ├── Low → run + log
   ├── Medium → run + reviewer
   ├── High → require explicit approval
   └── Critical → block
```

## الحالات الحدّية

- **الإجراءات المركّبة** — تُفكَّك إلى أوراق قبل التقييم، والأعلى مخاطر
  هو الحاكم.
- **الموافقات الزمنية** — تنتهي صلاحياتها بانتهاء نافذة التكليف.
- **التجاوز الطارئ** — يحقّ فقط لمالك التشغيل ويُسجَّل ويُراجَع.

## الواجهات
| المدخلات | المخرجات | المالكون | الإيقاع |
|---|---|---|---|
| Action class | Allow / Approve / Block | Compliance Guard Agent | Per action |
| Reviewer feedback | Matrix tuning | Head of Compliance | Quarterly |
| Incident learnings | Matrix update | Head of Compliance | After each incident |

## المقاييس
- Matrix Coverage — نسبة الإجراءات القابلة للتصنيف بلا تجاوز.
- Approval Throughput — وسيط زمن الموافقة للإجراءات عالية المخاطر.
- Override Count — تجاوزات لكل ربع (الهدف قرب الصفر).
- Block Repetition — تكرّر الحجب لنفس السبب الجذري.

## ذات صلة
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — موقف الاستقلالية
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — بروتوكول الحوادث
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — الإطار الاستراتيجي
- `docs/product/GOVERNANCE_AS_CODE.md` — القواعد التنفيذية
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — الفهرس الرئيسي

## سجل التغييرات
| التاريخ | الكاتب | التغيير |
|---|---|---|
| 2026-05-13 | سامي | مسودة أولى |
