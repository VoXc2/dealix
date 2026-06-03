# Contact Targeting Rules — دليل التشغيل (AR)

> من نتواصل معه، ولماذا. هذه القواعد تضمن أن نصل للدور الأنسب لكل نظام عبر **قنوات عامة فقط**، مع احترام do-not-contact والـ suppression list.
> مرجع الحقول: `schemas/contact_target.schema.json`. مرجع المصطلحات: `AGENTS.md §3`.

---

## 1. الغرض (Purpose)

اختيار جهة الاتصال الخاطئة يهدر أفضل pack. القاعدة الأساسية:

> **`best_contact_role` يجب أن يكون ضمن الأدوار المسموحة للنظام `recommended_system`. أول دور في القائمة = الأفضلية.**

هذا فحص آلي: كل `recommended_system` في أي pack أو contact_target يجب أن يكون له `best_contact_role` ضمن القائمة المعتمدة أدناه.

---

## 2. جدول النظام → الأدوار المسموحة

| `system_id` | الأدوار المسموحة (best → alternates) |
|---|---|
| `revenue_os` | **Head of Sales** → Founder, GM, Marketing Manager |
| `executive_command_os` | **Founder** → CEO, GM, Operations Manager |
| `followup_recovery_os` | **Sales Manager** → Marketing Manager, Founder |
| `whatsapp_client_os` | **Operations Manager** → Customer Service Manager, Founder |
| `proposal_proof_os` | **Founder** → Sales Lead, BD Manager, Marketing Manager |

> الأدوار المسموحة في الـ enum (لكل الأنظمة): `Founder, CEO, GM, Head of Sales, Sales Manager, Sales Lead, Marketing Manager, Operations Manager, Customer Service Manager, BD Manager`.

---

## 3. لماذا هذه الأدوار لكل نظام (Rationale)

| النظام | المنطق |
|---|---|
| `revenue_os` | الألم في مسار الفرص والـ next action — **Head of Sales** يملك المشكلة والقرار مباشرة. المؤسس/GM للشركات الصغيرة، ومدير التسويق إن كان يملك توليد الفرص. |
| `executive_command_os` | الألم في وضوح القرار اليومي للإدارة — هذا قرار **Founder/CEO/GM**. مدير العمليات للتشغيل اليومي. |
| `followup_recovery_os` | الألم في متابعة ما بعد أول تواصل — **Sales Manager** يملك المتابعة. مدير التسويق إن كان التسجيل تحت التسويق (شائع في التدريب). المؤسس للشركات الصغيرة. |
| `whatsapp_client_os` | الألم في تشغيل واتساب وتصنيف الطلبات والتصعيد — **Operations Manager** أو **Customer Service Manager** هما من يديران القناة فعليًا. |
| `proposal_proof_os` | الألم في جودة العروض والإثبات — غالبًا **Founder** يوافق على العروض في الشركات الصغيرة، ثم Sales Lead/BD Manager، ومدير التسويق لمواد الإثبات. |

---

## 4. كيف تختار `best_contact_role` مقابل `alternate_roles`

خطوات عملية:

```txt
1. حدّد recommended_system من الـ pack/need card.
2. افتح قائمة الأدوار المسموحة لهذا النظام (الجدول §2).
3. best_contact_role = أول دور تتوفر له قناة تواصل عامة في هذه الشركة.
4. alternate_roles = بقية الأدوار المسموحة، بالترتيب، التي قد نلجأ لها إن تعذّر الأول.
5. تحقق: هل الدور المختار ضمن القائمة؟ إن لا → الاختيار غير صالح.
```

قواعد ترجيح إضافية:

- **حجم الشركة:** في الشركات الصغيرة، المؤسس غالبًا يملك كل شيء → قدّم `Founder` حتى لو لم يكن أول الترتيب نظريًا، طالما هو ضمن القائمة.
- **توفّر القناة العامة:** لا نخترع جهة اتصال؛ نختار الدور الذي له قناة عامة فعلية (صفحة تواصل، حساب عام).
- **القطاع:** في التدريب التسجيل غالبًا تحت التسويق → `Marketing Manager` أعلى ترجيحًا ضمن `followup_recovery_os`.

### مثال

```txt
recommended_system: whatsapp_client_os
أدوار النظام:        Operations Manager → Customer Service Manager → Founder
الشركة:              عيادة في جدة (واتساب قناة رئيسية)
القناة العامة المتاحة: صفحة تواصل عامة فقط (لا يظهر دور محدد)

النتيجة:
best_contact_role: Operations Manager
alternate_roles:   ["Customer Service Manager", "Founder"]
preferred_channel: public_contact_form
do_not_contact:    false
```

---

## 5. الحقول الأساسية في Contact Target

| الحقل | الشرح |
|---|---|
| `recommended_system` | النظام الذي يحدد الأدوار المسموحة. |
| `best_contact_role` | الدور الأفضل (ضمن القائمة). |
| `alternate_roles` | بدائل بالترتيب (كلها ضمن القائمة). |
| `public_contact_channels` | قنوات عامة فقط (≥ 1). |
| `preferred_channel` | `email` / `public_contact_form` / `linkedin_public` / `phone_published_business_line`. |
| `do_not_contact` | boolean — إن `true` لا نتواصل إطلاقًا. |
| `risk_level` | `low` / `medium` / `high`. |
| `evidence_level` | `L0`–`L4`. |

> `preferred_channel = phone_published_business_line` يعني **خط عمل منشور علنًا فقط** — لا أرقام جوال شخصية، ولا اتصال آلي.

---

## 6. احترام do-not-contact والـ Suppression List

قواعد صارمة لا يجوز تجاوزها:

```txt
- إذا do_not_contact = true  → لا تواصل عبر أي قناة. نهائي.
- إذا الشركة في suppression list → لا تواصل، ولا تُحتسب send-ready.
- قنوات عامة فقط: website contact page, public social profiles, خط عمل منشور.
- ممنوع: purchased lists, leaked databases, scraping مخالف, أي بيانات خاصة, emails غير موثقة.
- لا أرقام جوال شخصية (نمط 05XXXXXXXX) في أي contact target.
```

الـ suppression list والـ do_not_contact يُفحصان قبل أي إرسال. أي مسودة لشركة في القائمة **ليست send-ready** بغضّ النظر عن جودتها (راجع `AGENTS.md §8`).

---

## 7. التحقق

- التحقق: `schemas/contact_target.schema.json`.
- الفاحص: `scripts/acquisition_delivery_check.py` (يتحقق أن `best_contact_role` ضمن أدوار النظام). تشغيل: `npm run os:check`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
