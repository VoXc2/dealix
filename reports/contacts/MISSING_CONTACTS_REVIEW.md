# Missing Contacts Review

*Run date: 2026-06-03 | Accounts with no public contact channel*

> الغرض: مراجعة يدوية للحسابات التي لم نجد لها قناة عامة — **دون اختلاق أي تواصل**.
> هذه قائمة عمل للمؤسس/الباحث، وليست قائمة إرسال.

---

## Held accounts (no public channel)

| Company | System | Evidence | Why held | Suggested manual step |
|---------|--------|----------|----------|-----------------------|
| Alpha Consulting Group | executive_command_os | L0 | لا قناة عامة منشورة (CC0); افتراض قطاعي فقط | بحث يدوي عن موقع/Google Business/LinkedIn رسمي؛ إن لم يوجد → drop |

**Count held: 1 / 10.**

---

## Handling rules (enforced)

```txt
- best_contact_route = none_found
- phone_if_public / email_if_public = null  (مفروض من المدقّق)
- status لا يتجاوز researched
- score → hold (contact_availability = 0)
- لا إرسال، لا اختلاق، لا تخمين بريد شخصي
```

---

## Why this matters

غياب التواصل **نتيجة مشروعة** وليست فشلًا يدفع للاختلاق. الحساب يُحجز حتى نجد
قناة عامة حقيقية أو يُسقط. هذا يحمي سمعة الدومين والامتثال
(`docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md`).

---

## Role-only accounts (have a channel, no named person)

هذه ليست «مفقودة» لكنها تُخاطب بالدور فقط (لا اسم):

```txt
Nexus IT Solutions · Growth Labs SA · LearnFast Academy · CloudShift Consulting
```
