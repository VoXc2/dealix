# الإيقاع التشغيلي اليومي للمؤسس (Founder Daily Operating Rhythm)

> Dealix يشتغل كل يوم بنفس الإيقاع، لا «حسب المزاج».
> AI drafts. Human approves. System logs.

---

## 1. التشغيل اليومي

| الوقت | المرحلة | المخرج |
|-------|---------|--------|
| 06:00 | Research Batch | شركات جديدة للبحث (مصادر حقيقية فقط) |
| 07:00 | Company Intelligence Packs | حِزم معلومات الشركات |
| 08:00 | 400 Draft Email Factory | مسودات الإيميل |
| 09:00 | Quality Scoring | `npm run commercial:quality` → `DAILY_QUALITY_GATE_REVIEW.md` |
| 10:00 | Top 100 Approval Queue | قائمة الاعتماد |
| 11:00 | Email/Call Handoff | تسليم لكل إيميل → Call Brief |
| 13:00 | Call Follow-up Queue | `npm run commercial:plan` → `SALES_OPS_BOARD_STATUS.md` |
| 15:00 | Mini Proposal Queue | عروض مصغّرة (بانتظار اعتماد المؤسس) |
| 17:00 | Delivery Pipeline Update | حالة التسليم |
| 19:00 | Founder Daily Super Command | `npm run commercial:brief` → `DAILY_SUPER_COMMAND.md` |

تشغيل كامل بأمر واحد: `npm run commercial:all` (quality → plan → brief → check).

---

## 2. المخرجات اليومية المطلوبة

| الوقت | المخرج |
|-------|--------|
| 07:00 | Company Intelligence Packs |
| 08:00 | Client Need Cards |
| 09:00 | Email Drafts (مع Score) |
| 10:00 | Top Approval Queue |
| 11:00 | Call Brief Queue |
| 15:00 | Mini Proposal Queue |
| 17:00 | Delivery Status |
| 19:00 | Daily Super Command |

---

## 3. القاعدة الذهبية

كل يوم يجب أن يجاوب النظام على:

```txt
من نستهدف؟ لماذا؟ ماذا نرسل؟ من يتصل؟ ماذا يقول؟ ما العرض؟ ما التسليم؟ ما القرار الأهم؟
```

---

## 4. أين تُخزَّن المخرجات

| المخرج | المسار |
|--------|--------|
| تقييم المسودات | `reports/quality/DAILY_QUALITY_GATE_REVIEW.md` |
| لوحة المبيعات | `reports/sales_ops/SALES_OPS_BOARD_STATUS.md` |
| الأمر اليومي الأعلى | `reports/founder/DAILY_SUPER_COMMAND.md` |
| مراجعة الأمان | `reports/security/DAILY_AGENT_SECURITY_REVIEW.md` |
| بيانات آلية | `company_os/commercial/*.json` |

---

## 5. ملاحظة على الواقعية

السعة المستهدفة (400/يوم) هي طاقة المصنع لا وعد بعدد شركات. الحجم الفعلي اليوم يعتمد على ما في خط الأنابيب من بحث حقيقي. لا قوائم مشتراة، ولا اتصال آلي، ولا واتساب بارد آلي.

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
