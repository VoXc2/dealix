# برج المراقبة التجاري / Commercial Control Tower
<!-- COMMERCIAL EMPIRE | Owner: Founder | Date: 2026-05-17 -->

> القانون / Canonical: see [AI_CONTROL_TOWER.md](../product/AI_CONTROL_TOWER.md)

برج المراقبة التجاري هو لوحة القيادة اليومية والأسبوعية للمؤسس. إنه نسخة تجارية من برج المراقبة المنتَجي: نفس مبدأ الرؤية الواحدة، لكنه يتتبع الطلب والبيع لا التشغيل الداخلي.
The Commercial Control Tower is the founder's daily and weekly command dashboard. It is the commercial sibling of the product control tower: one pane of glass, but it tracks demand and selling rather than internal operations.

## 1. العرض اليومي / The Daily View

كل بند يحمل وسم حقيقة. اللمسات والمتابعات مُلاحَظة؛ الالتزامات مؤكَّدة من العميل؛ الفواتير المدفوعة مؤكَّدة بالدفع.
Every line carries a truth label. Touches and follow-ups are Observed; commitments are Client-confirmed; paid invoices are Payment-confirmed.

| البند / Field | التعريف / Definition | وسم الحقيقة / Truth label |
|---|---|---|
| الحسابات المستهدفة / Target accounts | حسابات في قائمة اليوم | Estimate |
| اللمسات / Touches | رسائل أولى أُرسلت بموافقة / first messages sent with approval | Observed |
| المتابعات / Follow-ups | رسائل متابعة على حوار قائم | Observed |
| الردود / Replies | ردود مستلمة فعليًا | Observed |
| الديمو / Demos | عروض حية محجوزة أو منفّذة | Client-confirmed |
| النطاقات / Scopes | عروض نطاق مكتوبة ومُرسَلة | Observed |
| الفواتير / Invoices | فواتير صادرة بانتظار الدفع | Client-confirmed |
| المدفوع/الالتزامات / Paid and commitments | دفع مؤكَّد أو التزام مكتوب | Payment-confirmed / Client-confirmed |
| حزم الإثبات / Proof packs delivered | Proof Packs سُلِّمت اليوم | Observed |
| أحاديث الشركاء / Partner conversations | محادثات وكالات هذا اليوم | Observed |
| عملاء الإحالة / Affiliate leads | leads واردة عبر شريك (لا بريد عشوائي) | Observed |
| مخاطر مُعطِّلة / Blocked risks | ما يوقف صفقة الآن | Observed |
| أفضل رسالة / Best message | الصياغة الأعلى ردًّا اليوم | Observed |
| أسوأ قناة / Worst channel | القناة الأضعف عائدًا اليوم | Observed |
| أولوية الغد / Tomorrow's priority | بند واحد فقط | Estimate |

## 2. الأسئلة الأسبوعية / The Weekly Questions

تُجاب هذه الأسئلة كل يوم خميس على بطاقة واحدة. الإجابة بدليل من العرض اليومي لا بالانطباع.
These are answered every Thursday on one card. Each answer cites evidence from the daily view, not impressions.

```text
1. ما أفضل شريحة؟              / Best segment?
2. ما أفضل رسالة؟              / Best message?
3. ما أفضل عرض؟               / Best offer?
4. ما أفضل قناة؟              / Best channel?
5. أين توقّف القمع؟           / Where did the funnel stop?
6. أي اعتراض تكرّر؟           / Which objection repeated?
7. أي شريك جلب جودة؟          / Which partner brought quality?
8. أي إحالة جلبت ضوضاء؟       / Which affiliate brought noise?
9. ما الذي نضاعفه؟            / What do we double?
10. ما الذي نوقفه؟            / What do we stop?
11. ما الذي لا نبنيه؟         / What do we NOT build?
```

السؤال الحادي عشر يحمي العقيدة: لا نبني ميزة لأن عميلًا واحدًا طلبها. نبني فقط ما يثبته الطلب المتكرر.
Question 11 protects the doctrine: we do not build a feature because one customer asked. We build only what repeated demand proves.

## 3. الإيقاع اليومي للمؤسس / The Founder Daily Rhythm

```text
الصباح / Morning:
  - 10 رسائل/يوم        / 10 messages per day (each human-approved, draft_only first)
  - 5 متابعات           / 5 follow-ups on live threads

منتصف اليوم / Midday:
  - 1 منشور LinkedIn     / 1 LinkedIn post
  - 1 منشور X            / 1 X post
  - 1 حديث شراكة         / 1 partner conversation

نهاية اليوم / End of day:
  - تحديث بطاقة النتائج  / end-of-day scorecard update
  - تحديد أولوية الغد    / set tomorrow's single priority
```

لا تُرسل أي رسالة خارجية قبل الموافقة البشرية. كل صياغة تبدأ draft_only. لا واتساب بارد ولا كشط ولا بريد إحالات عشوائي.
No external message is sent before human approval. Every draft starts draft_only. No cold WhatsApp, no scraping, no affiliate spam.

## 4. قاعدة التصعيد / The Escalation Rule

| الإشارة / Signal | الإجراء / Action |
|---|---|
| 3 أيام بلا ردود / 3 days no replies | راجع الرسالة لا حجم الإرسال / review message not volume |
| اعتراض تكرّر 3 مرات / objection x3 | أضِفه لكتاب البيع المرجعي / add to canonical playbook |
| شريك يجلب ضوضاء / noisy partner | أوقف الإحالة، وثّق السبب / pause referral, document why |
| فاتورة بلا دفع 14 يومًا / invoice unpaid 14d | غيّر الحالة لا تطارد / change status, do not chase |

## 5. الربط بالعقيدة / Doctrine Link

برج المراقبة لا يعرض عائدًا مضمونًا. يعرض ما حدث فعلًا بوسم حقيقة، ويترك القرار للمؤسس. أي رقم بلا وسم حقيقة يُعتبر غير صالح.
The Control Tower never displays guaranteed return. It displays what actually happened with a truth label and leaves the decision to the founder. Any unlabeled number is treated as invalid.

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
