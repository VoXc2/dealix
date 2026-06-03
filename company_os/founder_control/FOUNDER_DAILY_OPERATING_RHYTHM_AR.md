# إيقاع التشغيل اليومي للمؤسس — Daily Operating Rhythm

الهدف: أن يعمل Dealix كل يوم بنفس الإيقاع، لا "حسب المزاج". المصنع اليومي يحوّل
البحث إلى إرسال واتصال وعرض وتسليم، وينتهي بأمر قيادة واحد للمؤسس.

---

## الإيقاع اليومي

| الوقت | المرحلة | المخرج | المحرك |
|------|---------|--------|--------|
| 06:00 | Research Batch | شركات مستهدفة | يدوي / بحث |
| 07:00 | Company Intelligence Packs | 400 Pack | يدوي / بحث |
| 08:00 | 400 Draft Email Factory | 400 Draft + Client Need Cards | `company_os/commercial/draft_factory.json` |
| 09:00 | Quality Scoring | تقييم + Top 100 | `npm run commercial:quality` |
| 10:00 | Top 100 Approval Queue | قائمة اعتماد | `reports/quality/` |
| 11:00 | Email/Call Handoff | Call Briefs | `npm run commercial:plan` |
| 13:00 | Call Follow-up Queue | Top 30 مكالمات | `reports/sales_ops/CALL_FOLLOWUP_QUEUE.md` |
| 15:00 | Mini Proposal Queue | عروض بانتظار الاعتماد | `reports/sales_ops/` |
| 17:00 | Delivery Pipeline Update | حالة التسليم | `reports/sales_ops/SALES_OPS_BOARD_STATUS.md` |
| 19:00 | Founder Daily Super Command | أمر القيادة اليومي | `npm run commercial:brief` |

تشغيل المصنع كاملًا في أمر واحد:

```bash
npm run commercial:all   # check → plan → quality → brief
```

`commercial:check` أولًا لأنه بوابة الأمان: إذا وجد مخالفة حرجة يتوقف المصنع.

---

## القاعدة الذهبية: 8 أسئلة كل يوم

التقرير اليومي غير جاهز إذا لم يجب على:

1. من نستهدف؟
2. لماذا؟
3. ماذا نرسل؟
4. من يتصل؟
5. ماذا يقول؟
6. ما العرض؟
7. ما التسليم؟
8. ما القرار الأهم؟

`reports/founder/DAILY_SUPER_COMMAND.md` مبني خصيصًا ليجيب على هذه الأسئلة.

---

## مستويات الدليل (Evidence Levels)

نفرّق دائمًا بين معلومة مؤكدة واستنتاج وتخمين:

| المستوى | المصدر |
|---------|--------|
| L0 | تخمين قطاعي |
| L1 | موقع الشركة |
| L2 | صفحة خدمة / وظيفة / خبر |
| L3 | أكثر من مصدر عام متوافق |
| L4 | بيانات من الشركة نفسها |

عند L0/L1 نكتب: «غالبًا»، «قد يكون»، «في هذا النوع من الشركات». ولا نكتب ألمًا
كحقيقة («أنتم تعانون من...») — بوابة الجودة ترفض ذلك تلقائيًا.

---

## مرجع

- نظام أمر القيادة: `company_os/founder_control/DAILY_SUPER_COMMAND_SYSTEM_AR.md`
- بوابات القرار: `company_os/founder_control/FOUNDER_DECISION_GATES_AR.md`
- لوحة المبيعات: `company_os/sales_ops/SALES_OPS_BOARD_AR.md`
