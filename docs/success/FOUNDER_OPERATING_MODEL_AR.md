# نموذج تشغيل المؤسس — Founder Operating Model

> القاعدة: المؤسس يتحكم بكل شيء عبر **قرار يومي واحد** و**مراجعة أسبوعية واحدة**.
> الذكاء الاصطناعي يجهّز، والمؤسس يقرّر.

---

## 1. مبدأ التحكم

```txt
AI prepares.        ← يجهّز ويرتّب ويحلّل
Human approves.     ← المؤسس يوافق على ما هو خارجي/مالي
System logs.        ← كل إجراء موثّق في السجل
Founder controls.   ← القرار النهائي للمؤسس دائماً
```

هذا المبدأ مطبّق في `company_os/governance/` (مصفوفة الصلاحيات + سجل الإجراءات + قائمة الموافقات).

---

## 2. مستويات استقلالية الوكلاء (Agent Autonomy Levels)

| Level | الاسم | مسموح | ممنوع |
|:---:|------|-------|-------|
| L1 | Observe | قراءة وتحليل | كتابة خارجية |
| L2 | Advise | توصية وتقييم | تنفيذ |
| L3 | Draft | إنشاء drafts | إرسال |
| L4 | Act with Approval | تنفيذ بعد موافقة | تنفيذ مستقل |
| L5 | Internal Autonomous | تقارير داخلية فقط | أي إجراء خارجي |

> متّسق مع `company_os/governance/agent_permissions.md`. لا وكيل يتجاوز L4 لأي إجراء خارجي،
> ولا يصل L5 إلا لإجراءات داخلية بحتة (تقارير).

---

## 3. بوابات الموافقة (Approval Gates)

الإجراءات التالية **لا تتم بلا موافقة المؤسس صراحةً**:

```txt
- الإرسال الخارجي (إيميل/رسائل).
- العروض (Mini Proposals).
- تغيير التسعير.
- بدء التسليم.
```

قائمة الموافقات الحيّة: `company_os/governance/approval_queue.json`،
وسجل الإجراءات: `company_os/governance/ai_action_ledger.jsonl`.

---

## 4. War Room اليومي (Daily)

تقرير يومي واحد يتحكم بكل شيء:

```txt
1.  Launch/Scale mode today
2.  Top blockers
3.  Top 10 revenue opportunities
4.  Top 20 send candidates
5.  Top 30 call candidates
6.  Mini proposals waiting approval
7.  Delivery blockers
8.  Domain/deliverability status
9.  Agent risk status
10. Cash opportunity
11. Founder critical decision
```

> يُولّد جزء من هذا اليوم عبر `scripts/generate_war_room.py` ويُخزَّن في
> `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md`. البنود الأمنية والوصولية تُضاف عند تفعيل الإرسال.

---

## 5. War Room الأسبوعي (Weekly)

```txt
best sector
best need
best sprint
best email angle
best call angle
best price point
highest conversion
lowest delivery friction
top objections
next experiments
```

هذه هي مدخلات حلقة التعلّم — تعيد ضبط اختيار السوق والعرض والتسعير كل أسبوع.
المرجع الأسبوعي القائم: `company_os/war_room/WEEKLY_CEO_BRIEF.md`.

---

## 6. إدارة عبء المؤسس

| المبدأ | التطبيق |
|--------|---------|
| قرار واحد في اليوم | كل شيء يتلخّص في "Founder critical decision" |
| لا قرارات صغيرة متكررة | الوكلاء يجهّزون البدائل، المؤسس يختار |
| دفعات الموافقة | راجع قائمة الموافقات دفعة واحدة، لا واحدة واحدة |
| الأتمتة قبل التوسّع | كل خطوة متكررة تُؤتمت قبل رفع الحجم |

عبء المؤسس مؤشر نجاح (البُعد #9): إذا كان القرار اليومي غير واضح أو القرارات الصغيرة تتكاثر،
فالنموذج يحتاج ضبطاً قبل التوسّع.

---

## 7. أنماط التشغيل (Operating Modes)

```txt
Launch Mode  → تركيز على أول صفقات + إثبات + تسليم يدوي مضبوط
Scale Mode   → رفع الحجم بعد تحقّق Launch Score و Scale Score
```

لا انتقال إلى Scale Mode قبل تحقّق شروط الجاهزية (راجع
[30_DAY_EXECUTION_PLAN_AR](./30_DAY_EXECUTION_PLAN_AR.md) و
[DEALIX_SUCCESS_READINESS_REVIEW](../../reports/success/DEALIX_SUCCESS_READINESS_REVIEW.md)).

---

## 8. الربط بباقي البنية

- المخاطر التي يتحكم بها المؤسس: [FAILURE_MODES_AND_COUNTERMEASURES_AR](./FAILURE_MODES_AND_COUNTERMEASURES_AR.md).
- ما يوافق عليه المؤسس قبل التسليم: [DELIVERY_BEFORE_SALES_POLICY_AR](./DELIVERY_BEFORE_SALES_POLICY_AR.md).
- خطة التنفيذ اليومية/الأسبوعية: [30_DAY_EXECUTION_PLAN_AR](./30_DAY_EXECUTION_PLAN_AR.md).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Status: Active*
