# GCC Outreach Policy — سياسة التواصل الخليجي

> سياسة القنوات والامتثال للتواصل. **Saudi-first, GCC-ready.** الأساس: **email-first**، بشري يوافق على كل إرسال.
>
> **مبني على:** الخطوط الحمراء في `company_os/governance/agent_permissions.md`، وقائمة `company_os/governance/pdpl_checklist.md`، وبنية المتابعات في `company_os/revenue/followups.json`.

---

## 1. القنوات المسموحة والممنوعة

| القناة                         | الحالة         | الشرط                                              |
| ------------------------------ | -------------- | ------------------------------------------------- |
| Cold email (email-first)       | ✅ مسموح        | مع SPF/DKIM/DMARC + unsubscribe + suppression + موافقة |
| WhatsApp **مع عميل قائم**      | ✅ مسموح        | محادثات العميل المملوكة/الواردة فقط، إرسال بشري    |
| **Cold WhatsApp automation**   | ❌ ممنوع        | لا أتمتة رسائل واتساب باردة إطلاقاً                 |
| **LinkedIn automation**        | ❌ ممنوع        | لا أتمتة LinkedIn                                   |
| **قوائم مشتراة (purchased)**   | ❌ ممنوع        | تضرّ سمعة الدومين والامتثال                         |

---

## 2. الخطوط الحمراء (مطابقة لـ `agent_permissions.md`)

```txt
1. لا إرسال خارجي بلا موافقة بشرية.            (خط أحمر #1)
2. لا PII خام في أدوات عامة.                    (خط أحمر #2)
3. لا قرارات تسعير من AI.                       (خط أحمر #3)
4. لا أتمتة واتساب باردة.
5. لا أتمتة LinkedIn.
6. لا قوائم مشتراة.
7. لا Re:/Fwd: مزيّفة.
8. لا وعود/ضمانات نتائج (No guaranteed claims).
```

---

## 3. متطلبات جاهزية الإرسال (Deliverability Readiness)

قبل تفعيل أي إرسال فوق الحد الأدنى:

| المتطلب                         | الحالة المطلوبة                               |
| ------------------------------- | -------------------------------------------- |
| SPF                             | منشور وصحيح                                  |
| DKIM                            | موقّع                                        |
| DMARC                           | منشور (للمرسلين الكبار: محاذاة)              |
| One-click unsubscribe (RFC 8058) | في كل رسالة تسويقية                          |
| Suppression list                | شغّالة وتُحترم فوراً                          |
| Bounce handling                 | إزالة hard bounces تلقائياً                  |
| Spam complaint rate             | < 0.3% (الهدف < 0.1%)                         |
| Domain health                   | مراقَب عبر Postmaster Tools                  |
| TLS + PTR (reverse DNS)         | مفعّل                                        |
| Warm-up تدريجي                  | بلا bursts                                   |

> المرجع: "Google Workspace — Email sender guidelines" (SPF أو DKIM لكل المرسلين؛ SPF+DKIM+DMARC للمرسلين الكبار؛ spam rate < 0.3%؛ one-click unsubscribe؛ تجنّب القوائم المشتراة؛ الرفع التدريجي).

---

## 4. جدول الرفع التدريجي

(مفصّل في `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md` §7)

```txt
Day 1–7: 400 drafts / 20–40 sends
Week 2 : 400 drafts / 50–100 sends
Week 3 : 400 drafts / 100–200 sends
Week 4 : 400 drafts / 200–300 sends
Stable : 400–800 drafts / 300–400 sends
```

أي ارتفاع spam/bounce ⟶ إيقاف الرفع والعودة مرحلة للخلف.

---

## 5. إيقاع المتابعة

من `revenue/followups.json` → `rules.follow_up_sequence = [3, 7, 14]`:

```txt
Touch 1 → بعد 3 أيام بلا رد
Touch 2 → بعد 7 أيام
Touch 3 → بعد 14 يوم
ثم: close-loop أو nurture (لا مطاردة).
```

---

## 6. قالب أول إيميل (معتمد)

```txt
Subject: فكرة لتحسين متابعة الفرص عندكم

السلام عليكم [الفريق/الدور]،

لاحظت أن [الشركة] تعمل في [القطاع]، وغالباً عندكم فرص/استفسارات تأتي من
[القناة/الإشارة]، لكن جزء من القيمة قد يضيع إذا المتابعة غير مرتبطة بأولوية
واضحة ورسائل جاهزة.

في Dealix نبدأ عادةً بمهمة صغيرة:
[Mission Name]

المخرج يكون:
- أين تضيع الفرص
- من يحتاج متابعة
- ماذا نقول
- ما next step لكل فرصة
- تقرير مختصر يوضّح ما حدث

إذا مناسب، أرسل لك تشخيصاً مختصراً يوضّح أول workflow ممكن يناسبكم.

تحياتي،
[الاسم]
Dealix

[رابط إلغاء الاشتراك بنقرة واحدة]
```

> القالب **لا** يعد بنتائج مضمونة، ولا يبيع "كل شيء" — يقترح Mission واحدة وخطوة صغيرة.

---

## 7. لكل سوق GCC

- **suppression list منفصلة** لكل دومين/سوق.
- محتوى ثنائي اللغة حيث يلزم (الإمارات/قطر/البحرين).
- إطار حماية البيانات لكل دولة (راجع `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md` §4).
- التحقق القانوني قرار مؤسس قبل فتح سوق جديد.

---

## 8. الربط

- المصنع اليومي: `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md`
- مصفوفة الاستهداف: `reports/outreach/GCC_TARGETING_REVIEW.md`
- استراتيجية التوسّع: `docs/commercial/GCC_EXPANSION_STRATEGY_AR.md`

*Owner: Founder · الإرسال والتسعير والتحقق القانوني قرارات بشرية.*
