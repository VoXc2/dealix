# العربية

**Owner:** مالك التطوير المستمر (Continuous Evolution Lead) — قسم هندسة المنصة.

## الغرض

تصف هذه الوثيقة كيف يصل التغيير الذي اجتاز بوّابات الإصدار إلى الإنتاج عبر طرح مرحلي بدلاً من النشر الفوري الكامل. المبدأ: كل تغيير يُكشف لشريحة محدودة أولاً، يُراقَب، ثم يتوسّع — حتى تُكتشف الانحدارات قبل أن تمسّ كل العملاء.

## مراحل الطرح

| المرحلة | الشريحة | شرط الانتقال |
|---|---|---|
| 0 — المحاكاة | بيئة معزولة، لا عملاء | اجتياز التقييمات في `continuous_improvement/tests.md` |
| 1 — داخلي | حسابات الفريق فقط | لا أخطاء حرجة لمدة 24 ساعة |
| 2 — تجريبي محدود | حتى 10% من العملاء، حسابات موافِقة | استقرار إشارات المراقبة لمدة 72 ساعة |
| 3 — توسّع | حتى 50% من العملاء | لا انحدار في درجة الجاهزية ولا تصعيد في سجل الاحتكاك |
| 4 — كامل | 100% من العملاء | موافقة المالك على بطاقة الإصدار النهائية |

## بوّابة المحاكاة

قبل المرحلة 1، يُشغَّل التغيير في محاكاة عبر `auto_client_acquisition/self_growth_os/daily_growth_loop.py` على مدخلات مؤرشفة. أي محتوى موجَّه للعملاء يمرّ على `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`. لا انتقال إلى شريحة حيّة قبل محاكاة نظيفة.

## إشارات المراقبة أثناء الطرح

- درجة الجاهزية المحدَّثة لكل مرحلة (انظر `continuous_improvement/readiness.md`).
- بطاقة النمو الأسبوعية `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py`.
- اكتشاف الانحراف الساعي `.github/workflows/watchdog_drift.yml`.
- تجميع سجل الاحتكاك `auto_client_acquisition/friction_log/aggregator.py`.

## التوقّف الآلي للطرح

يُوقَف الطرح ويُجمَّد عند الشريحة الحالية إذا تحقّق أيّ من:
- اكتشف `watchdog_drift.yml` انحرافاً في إحدى البوّابات الصلبة.
- انخفضت درجة الجاهزية تحت عتبة المرحلة.
- ظهر تصعيد جديد في سجل الاحتكاك مرتبط بالتغيير.

عند التوقّف، يُتَّخذ قرار: إصلاح للأمام أو تراجع وفق `continuous_improvement/rollback_policy.md`.

## ما لا يسمح به الطرح

- لا قفز فوق مرحلة دون شرط الانتقال.
- لا توسيع شريحة بلا فترة مراقبة مكتملة.
- لا طرح لمحتوى موجَّه للعملاء بلا اجتياز بوّابة النشر الآمن.
- لا إرسال خارجي نيابة عن العميل دون موافقة صريحة.

انظر أيضاً: `continuous_improvement/release_process.md`، `continuous_improvement/rollback_policy.md`، `continuous_improvement/readiness.md`.

---

# English

**Owner:** Continuous Evolution Lead — Platform Engineering.

## Purpose

This document describes how a change that has passed the release gates reaches production through a staged rollout instead of an immediate full deploy. The principle: every change is exposed to a limited segment first, observed, then expanded — so regressions are caught before they touch all customers.

## Rollout stages

| Stage | Segment | Promotion condition |
|---|---|---|
| 0 — Simulation | Isolated environment, no customers | Pass the evals in `continuous_improvement/tests.md` |
| 1 — Internal | Team accounts only | No critical errors for 24 hours |
| 2 — Limited pilot | Up to 10% of customers, consenting accounts | Observability signals stable for 72 hours |
| 3 — Expansion | Up to 50% of customers | No regression in readiness score, no friction-log escalation |
| 4 — Full | 100% of customers | Owner approval on the final release card |

## Simulation gate

Before Stage 1, the change is run in simulation via `auto_client_acquisition/self_growth_os/daily_growth_loop.py` against archived inputs. Any customer-facing content passes `auto_client_acquisition/self_growth_os/safe_publishing_gate.py`. No promotion to a live segment before a clean simulation.

## Observability signals during rollout

- The readiness score refreshed per stage (see `continuous_improvement/readiness.md`).
- The weekly growth scorecard `auto_client_acquisition/self_growth_os/weekly_growth_scorecard.py`.
- The hourly drift detection `.github/workflows/watchdog_drift.yml`.
- The friction-log aggregation `auto_client_acquisition/friction_log/aggregator.py`.

## Automatic rollout halt

The rollout is halted and frozen at the current segment if any of the following occurs:
- `watchdog_drift.yml` detects drift in one of the hard gates.
- The readiness score drops below the stage threshold.
- A new friction-log escalation linked to the change appears.

On halt, a decision is taken: fix forward or roll back per `continuous_improvement/rollback_policy.md`.

## What the rollout does not allow

- No skipping a stage without its promotion condition.
- No segment expansion without a completed observation window.
- No rollout of customer-facing content without passing the safe-publishing gate.
- No external send on a customer's behalf without explicit approval.

See also: `continuous_improvement/release_process.md`, `continuous_improvement/rollback_policy.md`, `continuous_improvement/readiness.md`.
