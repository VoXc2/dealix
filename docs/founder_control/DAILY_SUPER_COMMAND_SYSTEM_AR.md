# نظام الأمر اليومي الأعلى للمؤسس (Daily Super Command System)

> القاعدة الحاكمة: **AI drafts. Human approves. System logs.**
> الذكاء الاصطناعي يجهّز، المؤسس يقرّر، النظام يسجّل.

---

## 1. الهدف

تقرير واحد يومي يجاوب على كل ما يحتاجه المؤسس ليتخذ قرارات اليوم دون فوضى:

```txt
من نرسل له؟ من نتصل به؟ ماذا نعتمد؟ ماذا نبدأ تسليمه؟ ما المخاطر؟ ما القرار الأهم اليوم؟
```

إذا لم يجاوب التقرير على هذه الأسئلة، فالنظام غير جاهز.

الملف المُولّد: `reports/founder/DAILY_SUPER_COMMAND.md`
يُنتَج عبر: `npm run commercial:brief` (أو `npm run commercial:all`).

---

## 2. الأقسام الثلاثة عشر الإلزامية

| # | القسم | المصدر |
|---|-------|--------|
| 1 | Today's Critical Decision (قرار اليوم الأهم) | مُشتق من بيانات اليوم |
| 2 | 400 Draft Factory — Status | `draft_scores.json` |
| 3 | Top Approval Queue — Summary | `draft_scores.json` |
| 4 | Top 20 Companies to Send | Top Queue |
| 5 | Top 30 Calls to Make | `sales_board.json` |
| 6 | Mini Proposals Waiting Approval | `sales_board.json` |
| 7 | Delivery Pipelines — Status | `pipeline.json` |
| 8 | Website Leads | `website_leads.json` |
| 9 | Best Performing System | تجميع حسب النظام |
| 10 | Best Sector | تجميع حسب القطاع |
| 11 | Biggest Risk | `RISKS.md` + خط الأنابيب |
| 12 | Cash / Pricing Opportunities | `proposals.json` |
| 13 | Tomorrow's Recommendation | مُشتق |

> الفاحص `scripts/commercial-control-check.js` يتحقق من وجود هذه الأقسام الثلاثة عشر، وإلا يفشل (exit 1).

---

## 3. مثال على «قرار اليوم الأهم»

```txt
Approve the top 5 Follow-up Recovery OS drafts targeting Training Companies —
أعلى وضوح للألم وأقل تعقيد تسليم في دفعة اليوم. أوقف كل ما هو أقل من 75.
```

القرار يُشتق آليًا من: النظام الأكثر تمثيلًا في Top Queue + أفضل قطاع + أقل تعقيد تسليم.

---

## 4. حدود الأمانة (لا مبالغة)

- الأرقام تعكس **الواقع الفعلي** للبيانات اليوم، لا الطموح. السعة المستهدفة (400 مسودة/يوم) تُعرض كهدف، لا كعدد شركات مؤكدة.
- لا قوائم مشتراة. النمو يأتي من بحث حقيقي فقط.
- لا يتضمّن التقرير أي ادعاء مضمون للإيرادات.
- جميع قرارات التسعير والإرسال تتطلب اعتماد المؤسس (لا قرار تسعير من الـ AI).

---

## 5. الإيقاع

يُولَّد يوميًا الساعة 19:00 ضمن الإيقاع التشغيلي (انظر `FOUNDER_DAILY_OPERATING_RHYTHM_AR.md`).
المراجعة الأسبوعية في `reports/founder/WEEKLY_BOARD_REVIEW.md`.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03 | مُفعّل: نعم*
