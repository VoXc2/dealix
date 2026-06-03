# نظام أمر القيادة اليومي — Daily Super Command System

أهم تقرير للمؤسس. ملف واحد يُولَّد يوميًا ويقول بالضبط: أرسل لهؤلاء، اتصل بهؤلاء،
اعتمد هذه العروض، ابدأ هذه التسليمات، انتبه لهذا الخطر، خذ هذا القرار اليوم.

- **المخرج:** `reports/founder/DAILY_SUPER_COMMAND.md`
- **المحرك:** `npm run commercial:brief` (يشتق كل شيء من `company_os/commercial/*`)

---

## الأقسام الثلاثة عشر الإلزامية

1. Today's critical decision — القرار الأهم اليوم
2. 400 Draft status — حالة دفعة الـ 400
3. Top 100 Approval Queue summary — ملخص قائمة الاعتماد
4. Top 20 companies to send — أعلى 20 شركة للإرسال
5. Top 30 calls to make — أعلى 30 مكالمة
6. Mini proposals waiting approval — عروض بانتظار الاعتماد
7. Delivery pipelines status — حالة خطوط التسليم
8. Website leads — طلبات الموقع
9. Best performing system — أفضل نظام
10. Best sector — أفضل قطاع
11. Biggest risk — أكبر خطر
12. Cash / pricing opportunities — فرص النقد والتسعير
13. Tomorrow recommendation — توصية الغد

السكربت يتحقق ذاتيًا من وجود الأقسام الـ 13 وإلا يخرج بكود خطأ (exit 1).

---

## كيف تُشتق المحتويات؟

| القسم | المصدر |
|------|--------|
| القرار الأهم | النظام الأكثر تمثيلًا في `top_priority` + أوضح قطاع |
| حالة 400 | عدّ الدفعة مقابل هدف 400/يوم |
| Top 100 | `evaluateBatch` بعد بوابة الجودة |
| 20 للإرسال | أعلى Top 100 حسب النقاط |
| 30 مكالمة | فرص اللوحة في `call_due/called/interested` مع Call Brief |
| العروض المعلّقة | فرص بحالة `pending_founder_approval` |
| التسليم | فرص `won/delivery_started/active/renewal_candidate` |
| طلبات الموقع | `website_leads.json` + موجّه التشخيص |
| أكبر خطر | بوابة التحكم + نسبة الرفض + تركيز القطاع |

---

## مثال على القرار اليومي

> اعتمد 2 draft من نظام تشغيل الإيرادات الموجهة لقطاع التدريب، لأنها الأعلى وضوحًا
> في الألم والأقل تعقيدًا في التسليم اليوم.

القرار دائمًا مشتق من البيانات، لا رأي عام. والإرسال والاتصال والتسعير تبقى بقرار
بشري (انظر `FOUNDER_DECISION_GATES_AR.md`).
