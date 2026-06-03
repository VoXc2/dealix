# Public Contact Channels — قنوات التواصل العامة

> القنوات التي يلتقطها المحرك، وكيف توثَّق. القناة تُسجّل فقط إن كانت **عامة**.

---

## 1. أنواع القنوات

| القناة | `channel_type` | عادةً تحمل قيمة؟ | الثقة النموذجية |
|--------|----------------|:----------------:|------------------|
| الموقع الرسمي | `website` | ✅ URL | C1–C2 |
| صفحة التواصل | `contact_page` | ✅ URL | C2 |
| إيميل عام منشور | `general_email` | أحيانًا | C3 |
| هاتف منشور | `listed_phone` | أحيانًا | C3 |
| LinkedIn (صفحة شركة) | `linkedin` | ✅ URL | C2 |
| X / Instagram / Facebook | `x` / `instagram` / `facebook` | ✅ URL | C1–C2 |
| Google Business | `google_business` | غالبًا بلا قيمة مباشرة | C1 |
| دليل عام | `public_directory` | أحيانًا | C1 |
| إعلان وظيفة | `job_post` | إشارة لا قناة | — |

> المخطط: `schemas/contact_channel.schema.json`. كل قناة تحمل `confidence`، `source`، `is_public=true`، و`consent_basis` (الأساس النظامي للاستخدام: `public_business_listing` / `founder_provided` / `client_relationship`).

---

## 2. قاعدة القيمة (Value Rule)

- روابط الصفحات/الملفات العامة (موقع، صفحة تواصل، LinkedIn، حساب اجتماعي) → تُسجَّل قيمتها (URL عام).
- الإيميل/الهاتف المباشر → يُسجَّل **فقط** إن كان منشورًا علنًا من الشركة. غير ذلك → `value = null`.
- لا قيمة مُخمَّنة إطلاقًا.

---

## 3. القنوات في العيّنة الحالية

| الحساب | القنوات الموجودة | أعلى ثقة |
|--------|------------------|:--------:|
| `ACC-001` Madar | website, contact_page, linkedin | C2 |
| `ACC-002` Tadreeb Plus | website, contact_page, instagram | C2 |
| `ACC-003` Afaq | website, instagram | C1 |
| `ACC-004` Noor Clinics | website, contact_page (booking), google_business | C2 |
| `ACC-005` Rased | website, contact_page, linkedin | C2 |
| `ACC-006` Tawteen | website | C1 |
| `ACC-007` BinaaPro | website, contact_page, linkedin | C2 |
| `ACC-008` Mohtawa | instagram | C1 |

> لاحظ: لا يوجد أي `general_email` أو `listed_phone` بقيمة في العيّنة، لأن العيّنة لا تخترع جهات اتصال. هذا هو السلوك الصحيح، ويُظهر كيف يتعامل النظام مع نقص البيانات بأمانة.

---

## 4. واتساب: قناة خدمة لا قناة استهداف بارد

- منصة WhatsApp Business مخصّصة لخدمة العملاء والتجارة الحوارية (live agents أو chatbots)، و Cloud API يتيح تكاملات مؤسسية لكنه لا يوفّر واجهة أمامية جاهزة بذاته.
- لذلك واتساب عندنا **قناة تشغيل لعملاء قائمين** (WhatsApp Client OS)، **وليس** قناة لإرسال بارد لأرقام مجمّعة — وهو ممنوع صراحةً.

---

*Public Contact Channels | الإصدار 1.0 | آخر تحديث: 2026-06-03*
