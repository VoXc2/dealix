# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تصف هذه الوثيقة كيف تتحوّل ملاحظات العملاء وإشارات التشغيل إلى بنود تحسين تدخل دورة الإصدار. المبدأ: لا تُهمَل ملاحظة — كل إشارة تُسجَّل، تُصنَّف، وتدخل سجل التحسين أو تُغلَق بسبب موثَّق.

## مصادر التغذية الراجعة

| المصدر | القناة | الطبيعة |
|---|---|---|
| ملاحظات العملاء | سجل الاحتكاك `auto_client_acquisition/friction_log/` | نوعية، من تجربة فعلية |
| إشارات التشغيل | بطاقة النمو الأسبوعية `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py` | مجمَّعة، أنماط |
| اكتشاف الانحراف | `.github/workflows/watchdog_drift.yml` | تنبيهات آلية |
| التحسين الأسبوعي الآلي | `.github/workflows/weekly_self_improvement.yml` | اقتراحات مولَّدة |

## دورة الحلقة

1. **الالتقاط.** تُسجَّل الملاحظة في سجل الاحتكاك عبر `auto_client_acquisition/friction_log/store.py`.
2. **التعقيم.** تُزال أي بيانات تعريف شخصية عبر `auto_client_acquisition/friction_log/sanitizer.py` — لا إيميل ولا هاتف ولا اسم حقيقي.
3. **التجميع.** يجمّع `auto_client_acquisition/friction_log/aggregator.py` الملاحظات في أنماط مجمَّعة.
4. **الترتيب.** يرتّب `auto_client_acquisition/full_ops/prioritizer.py` الأنماط حسب الأثر والتكرار.
5. **التحويل لبند.** يصبح النمط ذو الأولوية بنداً في `continuous_improvement/improvement_backlog.md`.
6. **الإغلاق.** كل ملاحظة تُغلَق إمّا ببند تحسين أو بسبب موثَّق لعدم المتابعة.

## قواعد الحوكمة

- لا تُحفظ بيانات تعريف شخصية في سجل الاحتكاك — التعقيم إلزامي قبل التخزين.
- لا تُوصف ملاحظة عميل كوعد بنتيجة؛ تُوصف كنمط قابل للملاحظة.
- كل ملاحظة قابلة للتتبّع من مصدرها إلى بند أو سبب إغلاق.
- لا يُرسَل أي ردّ خارجي على العميل نيابةً عنه دون موافقة صريحة.

## القياس

- زمن الالتقاط حتى تحويله لبند.
- نسبة الملاحظات المُغلَقة ببند مقابل المُغلَقة بسبب موثَّق.
- عدد الأنماط المتكرّرة التي صارت بنوداً عالية الأولوية.

انظر أيضاً: `continuous_improvement/improvement_backlog.md`، `continuous_improvement/change_management.md`، `continuous_improvement/readiness.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document describes how customer feedback and operational signals become improvement items that enter the release cycle. The principle: no feedback is dropped — every signal is recorded, classified, and either enters the backlog or is closed with a documented reason.

## Feedback sources

| Source | Channel | Nature |
|---|---|---|
| Customer feedback | Friction log `auto_client_acquisition/friction_log/` | Qualitative, from real experience |
| Operational signals | Weekly growth scorecard `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py` | Aggregated, patterns |
| Drift detection | `.github/workflows/watchdog_drift.yml` | Automated alerts |
| Automated weekly improvement | `.github/workflows/weekly_self_improvement.yml` | Generated suggestions |

## Loop cycle

1. **Capture.** The feedback is recorded in the friction log via `auto_client_acquisition/friction_log/store.py`.
2. **Sanitize.** Any personally identifying data is removed via `auto_client_acquisition/friction_log/sanitizer.py` — no email, no phone, no real name.
3. **Aggregate.** `auto_client_acquisition/friction_log/aggregator.py` aggregates feedback into pooled patterns.
4. **Prioritize.** `auto_client_acquisition/full_ops/prioritizer.py` ranks patterns by impact and frequency.
5. **Convert to item.** A prioritized pattern becomes an item in `continuous_improvement/improvement_backlog.md`.
6. **Close.** Every piece of feedback is closed either with an improvement item or a documented reason for no follow-up.

## Governance rules

- No personally identifying data is stored in the friction log — sanitization is mandatory before storage.
- Customer feedback is never described as a promised outcome; it is described as an observable pattern.
- Every piece of feedback is traceable from its source to an item or a closure reason.
- No external reply is sent to the customer on their behalf without explicit approval.

## Measurement

- Time from capture to conversion into an item.
- Ratio of feedback closed with an item versus closed with a documented reason.
- Count of recurring patterns that became high-priority items.

See also: `continuous_improvement/improvement_backlog.md`, `continuous_improvement/change_management.md`, `continuous_improvement/readiness.md`.
