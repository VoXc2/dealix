# Dealix Ready-to-Launch Checklist — قائمة الجاهزية للإطلاق

> *آخر تحديث: 2026-06-03*
> الملف الأب: `DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md`
> النتيجة المباشرة محسوبة في `reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md`.

لا ننزل السوق إلا بعد تحقّق الأبواب التالية. كل بند له **شرط قبول واضح** و**مصدر
تحقّق** يمكن فحصه.

---

## بنود القائمة

| # | البند | المطلوب | مصدر التحقّق |
|---|-------|---------|--------------|
| 1 | **Website** | 5 صفحات أنظمة + صفحة أسعار + صفحة Diagnostic + CTAs | `src/pages/`, `docs/operating_factory/` |
| 2 | **Account Intelligence** | بنية 400 Account Pack موثّقة + ترتيب Top 100 | الدستور §4–5 + `reports/account_intelligence/` |
| 3 | **Contacts** | مستويات ثقة C0–C4 + معالجة الناقص | `QUALITY_GATES_AR.md` §1 |
| 4 | **Emails** | 6 بوابات + Email Quality Score | `QUALITY_GATES_AR.md` §2 |
| 5 | **Calls** | Call Briefs + Call Outcomes | `QUALITY_GATES_AR.md` §3 |
| 6 | **Mini Proposals** | Proposal Approval Gate | `QUALITY_GATES_AR.md` §4 |
| 7 | **Delivery** | 5 Delivery Packs + Acceptance Gates | `QUALITY_GATES_AR.md` §5 |
| 8 | **Finance** | Cash Priority Score | `QUALITY_GATES_AR.md` §6 |
| 9 | **Founder Command** | تقرير قيادي يومي | `DAILY_LOOP_AR.md` (19:00) |
| 10 | **Security** | سياسة المحتوى الخارجي كبيانات غير موثوقة | `docs/security/` |
| 11 | **Privacy** | تقليل البيانات + Suppression/Do-Not-Contact | `docs/privacy/` |

---

## شروط القبول التفصيلية

### 1. Website
- [ ] 5 صفحات لكل نظام (Revenue / Follow-up Recovery / Executive Command / WhatsApp Client / Proposal & Proof).
- [ ] صفحة أسعار واضحة بأسعار "ابتداءً من".
- [ ] صفحة Diagnostic (تشخيص مجاني — حجز مكالمة 20 دقيقة).
- [ ] CTAs واضحة في كل صفحة.
- [ ] لا أسماء داخلية في النسخة (راجع بوابة §7 في Quality Gates).

### 2. Account Intelligence
- [ ] بنية Account Pack موثّقة (الدستور §5).
- [ ] توزيع الـ 400 موثّق (الدستور §4).
- [ ] ترتيب Top 100 معرّف (Cash Priority + Email Score).

### 3. Contacts
- [ ] مستويات C0–C4 معرّفة.
- [ ] قاعدة "C0/C1 → لا إرسال" مفعّلة.
- [ ] منع اختلاق جهات الاتصال موثّق.

### 4–8. Gates & Finance
- [ ] Email: 6 بوابات + Score.
- [ ] Calls: Brief + Outcomes → Next Action.
- [ ] Mini Proposals: Approval Gate.
- [ ] Delivery: 5 Packs + Acceptance/Start Gates.
- [ ] Finance: Cash Priority Score.

### 9. Founder Command
- [ ] خطوة 19:00 في الحلقة اليومية تُنتج قرارات الغد.

### 10. Security
- [ ] المحتوى الخارجي = بيانات فقط، لا تعليمات.
- [ ] لا استدعاء أدوات من نص موقع.
- [ ] لا أسرار في prompts/logs.

### 11. Privacy
- [ ] تقليل البيانات (Data Minimization).
- [ ] قائمة Suppression + Do-Not-Contact.
- [ ] حذف/تجهيل عند الطلب.

---

## نظام التقييم (Launch Scoring)

كل بند من الأحد عشر يُقيَّم: **مكتمل (نقاط كاملة)**، **جزئي (نصف)**، **مفقود (صفر)**.
النتيجة من 100.

```txt
90–100 = Launch Ready          (جاهز للإطلاق)
75–89  = Soft Launch Ready     (إطلاق محدود)
60–74  = Internal Dry Run      (تشغيل تجريبي داخلي)
<60    = Not Ready             (غير جاهز)
```

النتيجة الحالية ومبرراتها في:
`reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md`.

---

*Dealix Ready-to-Launch Checklist | Version 1.0 | 2026-06-03*
