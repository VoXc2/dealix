# العربية

# المراجعة الشهرية — Layer 10 / مرحلة التحسين الشهري

**المالك:** قائد نجاح العملاء (Customer Success Lead)
**الجمهور:** عضو الفريق الذي يدير المراجعة الشهرية لعميل اشتراك
**المراجع:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `docs/scorecards/CLIENT_SCORECARD.md` · `clients/_TEMPLATE/VALUE_DASHBOARD.md` · `playbooks/monthly_optimization/improvement_backlog.md` · `playbooks/delivery/operations_os_delivery.md`

> الغرض: مراجعة شهرية موحّدة تثبت قيمة الشهر بأدلة وتحدّد تحسينات الشهر التالي — حتى لا يكون التجديد قراراً غامضاً.

## 1. متى تُستخدم هذه المراجعة

شهرياً لكل عميل اشتراك Managed Ops، قبل تاريخ التجديد بأسبوع.

## 2. مكوّنات المراجعة

| المكوّن | الوصف |
|---|---|
| ملخص قيمة الشهر | المخرجات وأحداث الإثبات الموثقة |
| مقاييس نجاح العميل | مقارنة بأهداف الاشتراك |
| إشارات المخاطر والتجديد | فحص إشارات churn |
| تحسينات الشهر القادم | بنود مرشَّحة للـ backlog |

## 3. خطوات المراجعة (خطوة بخطوة)

1. اجمع مخرجات الشهر وأحداث الإثبات من سجل الإثبات.
2. حدّث `docs/scorecards/CLIENT_SCORECARD.md` و`VALUE_DASHBOARD.md`.
3. قارن المقاييس بأهداف الاشتراك (مسودات موافق عليها، رضا، أحداث إثبات).
4. افحص إشارات المخاطر والتجديد (راجع `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` القسم 4).
5. حدّد 1–3 تحسينات للشهر القادم وأضفها إلى `improvement_backlog.md`.
6. أجرِ اجتماع مراجعة 30 دقيقة مع العميل وسلّم الملخص.
7. سجّل قرار التجديد: مواصلة / تعديل / تجميد محترم.

## 4. القواعد الحاكمة (Non-negotiables)

- كل قيمة مذكورة مدعومة بدليل من سجل الإثبات — لا إثبات مختلق.
- لا أرقام أداء كحقيقة — «تقديري» فقط، و«فرص مُثبتة بأدلة».
- لا ضغط تجديد — قرار العميل يُحترَم.
- لا بيانات شخصية في ملخص المراجعة.
- لا upsell لدرجة أعلى دون 3 أشهر تشغيل متواصل.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] ملخص قيمة الشهر مكتمل ومدعوم بأدلة.
- [ ] بطاقات الأداء محدَّثة.
- [ ] المقاييس قُورنت بأهداف الاشتراك.
- [ ] إشارات المخاطر فُحصت.
- [ ] 1–3 تحسينات أُضيفت للـ backlog.
- [ ] اجتماع المراجعة الشهري تمّ وموثَّق.

## 6. المقاييس

- نسبة المراجعات المُجراة في موعدها (الهدف 100%).
- رضا العميل الشهري (الهدف ≥ 4/5).
- معدل التجديد (يُتتبَّع بلا هدف وعد).
- عدد التحسينات المُضافة شهرياً للـ backlog.

## 7. خطافات المراقبة (Observability)

- سجّل المراجعة في `clients/<client>/VALUE_DASHBOARD.md`.
- علّم الحالة: `review_done` / `renewal_decided`.
- مراجعة ربعية لاتجاهات الرضا وإشارات المخاطر عبر العملاء.

## 8. إجراء التراجع (Rollback)

إذا فاتت مراجعة شهرية أو ذُكرت قيمة بلا دليل:
1. أجرِ المراجعة الناقصة خلال 3 أيام عمل.
2. صحّح أي قيمة غير مدعومة وأبلغ العميل.
3. سجّل الحادثة في سجل الحوكمة وراجع السبب.

# English

# Monthly Review — Layer 10 / Monthly Optimization Stage

**Owner:** Customer Success Lead
**Audience:** Team member running the monthly review for a subscription client
**References:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `docs/scorecards/CLIENT_SCORECARD.md` · `clients/_TEMPLATE/VALUE_DASHBOARD.md` · `playbooks/monthly_optimization/improvement_backlog.md` · `playbooks/delivery/operations_os_delivery.md`

> Purpose: a standard monthly review that proves the month's value with evidence and sets the next month's improvements — so renewal is never a vague decision.

## 1. When to use this review

Monthly for every Managed Ops subscription client, one week before the renewal date.

## 2. Review components

| Component | Description |
|---|---|
| Month value summary | Deliverables and documented proof events |
| Client success metrics | Compared against subscription targets |
| Risk and renewal signals | Churn signal check |
| Next-month improvements | Items nominated for the backlog |

## 3. Review steps (step by step)

1. Gather the month's deliverables and proof events from the proof ledger.
2. Update `docs/scorecards/CLIENT_SCORECARD.md` and `VALUE_DASHBOARD.md`.
3. Compare metrics against subscription targets (drafts approved, satisfaction, proof events).
4. Check risk and renewal signals (see `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` Section 4).
5. Set 1–3 improvements for next month and add them to `improvement_backlog.md`.
6. Run a 30-minute review meeting with the client and deliver the summary.
7. Record the renewal decision: continue / adjust / graceful freeze.

## 4. Governance rules (non-negotiables)

- Every value stated is backed by evidence from the proof ledger — no fake proof.
- No performance figures as fact — "estimated" only, and "evidenced opportunities".
- No renewal pressure — the client's decision is respected.
- No PII in the review summary.
- No upsell to a higher rung without 3 consecutive months of operation.

## 5. Acceptance criteria (readiness checklist)

- [ ] Month value summary complete and evidence-backed.
- [ ] Scorecards updated.
- [ ] Metrics compared against subscription targets.
- [ ] Risk signals checked.
- [ ] 1–3 improvements added to the backlog.
- [ ] Monthly review meeting completed and documented.

## 6. Metrics

- Share of reviews run on time (target 100%).
- Monthly client satisfaction (target ≥ 4/5).
- Renewal rate (tracked with no promised target).
- Count of improvements added to the backlog monthly.

## 7. Observability hooks

- Log the review in `clients/<client>/VALUE_DASHBOARD.md`.
- Tag the state: `review_done` / `renewal_decided`.
- Quarterly review of satisfaction trends and risk signals across clients.

## 8. Rollback procedure

If a monthly review is missed or a value is stated without evidence:
1. Run the missed review within 3 working days.
2. Correct any unsupported value and inform the client.
3. Record the incident in the governance log and review the cause.
