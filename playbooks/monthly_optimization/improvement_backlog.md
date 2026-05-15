# العربية

# سجل التحسينات — Layer 10 / مرحلة التحسين الشهري

**المالك:** قائد نجاح العملاء (Customer Success Lead)
**الجمهور:** فريق التسليم الذي يجمع ويرتّب فرص التحسين عبر العملاء
**المراجع:** `playbooks/monthly_optimization/monthly_review.md` · `clients/_TEMPLATE/CAPABILITY_BACKLOG.md` · `clients/_TEMPLATE/EXPANSION_MAP.md` · `docs/scorecards/SERVICE_SCORECARD.md`

> الغرض: سجل واحد منظَّم لفرص التحسين — حتى يتحوّل التعلّم من كل عميل إلى تحسين منهجي بدل أن يضيع.

## 1. متى يُستخدم هذا السجل

بشكل مستمر: تُضاف البنود من المراجعات الشهرية ومن ملاحظات الجودة ومن طلبات الدعم المتكررة.

## 2. مصادر بنود التحسين

- المراجعة الشهرية لكل عميل (1–3 بنود شهرياً).
- المخالفات المتكررة في فحص الجودة.
- أنواع طلبات الدعم المتكررة.
- ملاحظات العملاء وأسباب الـ churn.

## 3. حقول بند التحسين

| الحقل | الوصف |
|---|---|
| المعرّف | رمز فريد للبند |
| المصدر | من أين جاء (مراجعة / جودة / دعم) |
| الوصف | فرصة التحسين بجملة واضحة |
| الأثر | مرتفع / متوسط / منخفض (تقديري) |
| الجهد | مرتفع / متوسط / منخفض (تقديري) |
| الحالة | `new` / `prioritized` / `in_progress` / `done` |
| المالك | الدور المسؤول عن التنفيذ |

## 4. خطوات الإدارة (خطوة بخطوة)

1. أضف كل بند جديد بحقوله كاملة عند ظهوره.
2. صنّف الأثر والجهد بتقدير معلَن — لا أرقام مؤكدة.
3. رتّب البنود: أثر مرتفع وجهد منخفض أولاً.
4. عيّن مالكاً وحالة لكل بند مرتَّب.
5. راجع السجل شهرياً مع المراجعات وحدّث الحالات.
6. عند إغلاق بند، وثّق ما تغيّر في الدليل أو العملية.

## 5. القواعد الحاكمة (Non-negotiables)

- تقدير الأثر والجهد معلَن كتقدير — لا يُقدَّم كحقيقة.
- لا بيانات شخصية ولا أسماء عملاء حقيقية في بنود السجل.
- التحسينات لا تُدخِل خدمات ممنوعة (كشط، رسائل باردة، أتمتة LinkedIn).
- بنود الدرجات الأعلى لا تُنفَّذ قبل استيفاء شروط سُلَّم الخدمات.

## 6. معايير القبول (قائمة الجاهزية)

- [ ] كل بند له المعرّف والمصدر والوصف.
- [ ] الأثر والجهد مصنَّفان بتقدير معلَن.
- [ ] البنود المرتَّبة لها مالك وحالة.
- [ ] السجل رُوجِع في آخر مراجعة شهرية.
- [ ] البنود المغلقة موثَّق أثرها.

## 7. المقاييس

- عدد البنود المُضافة والمغلقة شهرياً.
- زمن دورة البند: من `new` إلى `done`.
- نسبة البنود مرتفعة الأثر المُنجزة.

## 8. خطافات المراقبة (Observability)

- سجّل السجل وحدّثه مع كل مراجعة شهرية.
- علّم حالة كل بند: `new` / `prioritized` / `in_progress` / `done`.
- مراجعة ربعية لاتجاهات مصادر التحسين المتكررة.

## 9. إجراء التراجع (Rollback)

إذا أدخل بند تحسين عيباً أو خدمة ممنوعة:
1. أوقف البند وأرجِع الحالة إلى `prioritized` مع ملاحظة السبب.
2. سجّل الحادثة في سجل الحوكمة.
3. راجع معيار الفرز لمنع قبول بند مماثل.

# English

# Improvement Backlog — Layer 10 / Monthly Optimization Stage

**Owner:** Customer Success Lead
**Audience:** The delivery team gathering and prioritizing improvement opportunities across clients
**References:** `playbooks/monthly_optimization/monthly_review.md` · `clients/_TEMPLATE/CAPABILITY_BACKLOG.md` · `clients/_TEMPLATE/EXPANSION_MAP.md` · `docs/scorecards/SERVICE_SCORECARD.md`

> Purpose: a single, structured backlog of improvement opportunities — so learning from each client becomes systematic improvement instead of being lost.

## 1. When to use this backlog

Continuously: items are added from monthly reviews, QA findings, and recurring support requests.

## 2. Sources of improvement items

- The monthly review for each client (1–3 items per month).
- Recurring violations in QA checks.
- Recurring support request types.
- Client feedback and churn causes.

## 3. Improvement item fields

| Field | Description |
|---|---|
| ID | A unique code for the item |
| Source | Where it came from (review / QA / support) |
| Description | The improvement opportunity in one clear sentence |
| Impact | High / medium / low (estimated) |
| Effort | High / medium / low (estimated) |
| State | `new` / `prioritized` / `in_progress` / `done` |
| Owner | The role responsible for delivery |

## 4. Management steps (step by step)

1. Add every new item with its full fields when it appears.
2. Classify impact and effort as a declared estimate — no confirmed figures.
3. Prioritize the items: high impact and low effort first.
4. Assign an owner and a state to each prioritized item.
5. Review the backlog monthly alongside the reviews and update states.
6. When an item is closed, document what changed in the playbook or process.

## 5. Governance rules (non-negotiables)

- Impact and effort estimates are declared as estimates — never stated as fact.
- No PII and no real client names in backlog items.
- Improvements do not introduce forbidden services (scraping, cold messaging, LinkedIn automation).
- Higher-rung items are not executed before the service ladder conditions are met.

## 6. Acceptance criteria (readiness checklist)

- [ ] Every item has an ID, source, and description.
- [ ] Impact and effort classified as a declared estimate.
- [ ] Prioritized items have an owner and a state.
- [ ] The backlog was reviewed at the last monthly review.
- [ ] Closed items have their impact documented.

## 7. Metrics

- Count of items added and closed monthly.
- Item cycle time: from `new` to `done`.
- Share of high-impact items completed.

## 8. Observability hooks

- Maintain and update the backlog with every monthly review.
- Tag each item state: `new` / `prioritized` / `in_progress` / `done`.
- Quarterly review of recurring improvement-source trends.

## 9. Rollback procedure

If an improvement item introduces a defect or a forbidden service:
1. Stop the item and return its state to `prioritized` with a note of the cause.
2. Record the incident in the governance log.
3. Review the triage criterion to prevent a similar item being accepted.
