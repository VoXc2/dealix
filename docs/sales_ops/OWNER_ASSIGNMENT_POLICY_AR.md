# سياسة إسناد الملكية (Owner Assignment Policy)

> لكل شركة خمسة ملّاك عبر دورة حياتها، حتى يمكن تفويض المتابعة بدون فوضى.
> AI drafts. Human approves. System logs.

---

## 1. الأدوار الخمسة

| الدور | المسؤولية | المرحلة |
|-------|-----------|---------|
| `research_owner` | بحث الشركة وبطاقة الاحتياج | researched → need_card_ready |
| `email_owner` | صياغة المسودة والإرسال بعد الاعتماد | draft_ready → sent |
| `call_owner` | الاتصال والمتابعة | call_due → interested |
| `proposal_owner` | العرض المصغّر والإغلاق | mini_proposal_ready → won/lost |
| `delivery_owner` | التسليم والتجديد | delivery_started → renewal_candidate |

---

## 2. الوضع الحالي

في مرحلة المشغّل الواحد، المالك الافتراضي لكل الأدوار هو **Founder**. عند التوسّع:

```txt
أنت تجيب العلاقة (research/email).
شخص ثانٍ يتابع بالاتصال (call_owner).
المؤسس يبقى مالك القرار (approve/price).
```

> هذا يحقق ما طلبه المؤسس: «ممكن أرسل الإيميلات وأخلّي غيري يتابع بالاتصال».

---

## 3. قاعدة الحوكمة

- المؤسس يبقى **دائمًا** مالك قرارات الاعتماد والتسعير والإرسال والتسليم (الخطوط الحمراء).
- الـ AI لا يملك أي دور؛ هو يجهّز فقط (Observe / Advise / Draft).
- كل تسليم متابعة لشخص آخر يُوثَّق في اللوحة (عمود Owner) وفي سجل القرارات.

---

## 4. Email → Call Handoff

كل إيميل يُنتج Call Brief (انظر `docs/quality/CALL_BRIEF_QUALITY_GATE_AR.md`) يحوي: opening line, questions, expected objection, next step. يُسلَّم لـ `call_owner` عبر `SALES_OPS_BOARD_STATUS.md`.

أولوية الاتصال:

```txt
P1 = ملاءمة عالية + ألم واضح + قدرة دفع
P2 = مناسبة لكن الدليل متوسط
P3 = تحتاج nurture
P4 = لا تتصل الآن
```

---

*الإصدار: 1.0 | آخر تحديث: 2026-06-03*
