# Contact Discovery Policy — سياسة اكتشاف قنوات التواصل

> هدف المحرك: إيجاد **قنوات تواصل عامة** والدور الأنسب للتواصل — دون اختراع أي اسم أو رقم أو إيميل.

---

## 1. المصادر المسموحة (Allowed)

```
Official website
Contact page
Google Business / public search snippets
LinkedIn public company page
X / Instagram / Facebook public profiles
Public directories
Public job posts
Public news
Founder-provided / client-confirmed data
```

## 2. الممنوع (Forbidden)

```
Purchased lists                ← قوائم بريد مشتراة
Leaked databases               ← قواعد بيانات مسرّبة
Scraping يخالف شروط الموقع
تخمين إيميلات شخصية بالجملة
Cold WhatsApp لأرقام مجمّعة
حفظ بيانات شخصية بلا حاجة
```

> سياسات مزوّدي البريد (مثل Google/Yahoo) تحذّر صراحة من شراء القوائم والإرسال لمن لم يشتركوا لأنه يضرّ السمعة ويرفع احتمال التصنيف كـ spam، وتشترط مصادقة SPF/DKIM وDMARC للمرسلين الكبار وآلية إلغاء اشتراك بنقرة واحدة. التزامنا بالمصادر العامة فقط يحمي السمعة من البداية.

---

## 3. قاعدة "لا اختراع" (No-Invention Rule)

| الحالة | السلوك الصحيح |
|--------|----------------|
| لا يوجد اسم شخص منشور | استهدف **الدور** (مثل Head of Sales) |
| لا يوجد رقم منشور | `phone_if_public = null` + `best_contact_route = contact_form_or_general_email` |
| لا يوجد إيميل منشور | `email_if_public = null`؛ استخدم نموذج التواصل |
| لا توجد أي قناة | `contact_confidence = C0`؛ يُستبعد من الإرسال |

```
phone_if_public: null
email_if_public: null
best_contact_route: "contact_form_or_general_email"
```

النظام **لا يملأ الفراغات بالتخمين**.

---

## 4. الناتج (Discovery Record)

المخطط: `schemas/contact_discovery.schema.json` — البيانات: `data/contacts/contact_discovery.jsonl`.

كل سجل يوثّق: `target_role`، `best_contact_route`، `contact_confidence`، `sources` (مصدر عام واحد على الأقل)، `missing` (ما لم يُوجد)، و`do_not_contact`.

---

## 5. قائمة الكبت (Suppression / Do-Not-Contact)

- أي حساب عليه `do_not_contact = true` **يُستبعد كليًا** ولا يدخل أي طابور.
- طلبات "أوقفوا التواصل" تُضاف فورًا للقائمة (راجع `docs/privacy/DATA_MINIMIZATION_AND_DO_NOT_CONTACT_AR.md`).

---

## 6. التحقق الآلي

`scripts/account-factory-check.mjs` يفرض:
- كل سجل اكتشاف له مصدر عام واحد على الأقل.
- السجلات منخفضة الثقة (C0/C1) **لا تحمل** إيميلًا/هاتفًا مباشرًا (أي لم يُختلق شيء).
- كل `account_id` في الاكتشاف موجود فعلاً في حزم الحسابات.

---

*Contact Discovery Policy | الإصدار 1.0 | آخر تحديث: 2026-06-03 | بيانات عامة فقط*
