# Contact Discovery Policy — سياسة اكتشاف قنوات التواصل

*كيف نجد الجهة والقناة العامة — بشكل قانوني وآمن، وبدون اختلاق.*
*المرجع الآلي: `schemas/contact_discovery.schema.json` + `schemas/contact_channel.schema.json`.*
*آخر تحديث: 2026-06-03*

---

## المبدأ

> نستخدم **معلومات الشركة العامة فقط** + ما يقدّمه المؤسس/العميل. لا نختلق اسمًا
> ولا بريدًا ولا رقمًا. إن لم نجد قناة عامة → نستهدف **الدور** فقط أو نحجز الحساب.

---

## مصادر مسموحة وواقعية

```txt
- موقع الشركة الرسمي
- صفحة Contact
- Google Business Profile / نتائج البحث العامة
- LinkedIn public company page
- X / Instagram / Facebook public profiles
- directories العامة
- job posts العامة
- press / news pages
```

## ممنوع أو عالي الخطورة

```txt
- شراء قوائم إيميلات
- قواعد بيانات مسرّبة
- scraping مخالف لشروط المواقع
- تخمين إيميلات شخصية بكميات كبيرة
- إرسال واتساب cold لأرقام مجمَّعة
```

> إرشادات مرسلي البريد (Google) تحذّر من شراء العناوين أو الإرسال لمن لم يشتركوا،
> لأن ذلك يرفع احتمال تصنيف الرسائل spam ويضرّ سمعة الدومين. وتوصي بمصادقة
> SPF/DKIM و DMARC للمرسلين الكبار، ومراقبة Postmaster Tools، وتجنّب Re:/Fwd
> المضلِّلة. لذلك سياستنا: قنوات عامة فقط + موافقة بشرية قبل أي إرسال.

---

## القاعدة الذهبية: لا اختلاق

```txt
phone_if_public / email_if_public تُملأ فقط إذا وُجدت قناة عامة مطابقة فعلاً.
إذا لم يوجد اسم شخص عام → استخدم الدور:
    «إلى فريق المبيعات / فريق الإدارة / فريق العمليات …»
ولا تخترع اسمًا أبدًا.
```

المدقّق يرفض أي `phone_if_public`/`email_if_public` لا تقابله قناة عامة في
`data/contacts/contact_channels.jsonl`.

---

## نتائج الاكتشاف (Discovery Outcomes)

| status | المعنى | السلوك |
|--------|--------|--------|
| `contact_found` | وُجدت قناة عامة واضحة | جاهز للمسودة |
| `role_only` | وُجدت قناة لكن بلا شخص مُسمّى | استهدف الدور فقط |
| `no_public_channel` | لا قناة عامة | احجز للبحث اليدوي (hold) — لا إرسال |
| `do_not_contact` | استبعاد | لا تواصل |

> «غياب التواصل» نتيجة من الدرجة الأولى — تُعالَج بسلاسة ولا تدفع للاختلاق.

---

## المعالجة السلِسة لغياب التواصل (Graceful Handling)

```txt
1. best_contact_route = none_found
2. لا تُملأ phone/email
3. الحالة لا تتجاوز researched/need_card_ready
4. التقييم: contact_availability = 0 → غالبًا hold
5. تظهر في reports/contacts/MISSING_CONTACTS_REVIEW.md للبحث اليدوي
```

مثال حقيقي: *Alpha Consulting Group* (L0, CC0) — حُجز تلقائيًا (score 29 → hold).
