# Public Contact Channels — القنوات العامة المسموحة

*أنواع القنوات التي نخزّنها، وكلها عامة ومنشورة من الشركة نفسها.*
*المرجع الآلي: `schemas/contact_channel.schema.json` · البيانات: `data/contacts/contact_channels.jsonl`.*
*آخر تحديث: 2026-06-03*

---

## أنواع القنوات (`channel_type`)

| النوع | مثال | عادةً confidence |
|------|------|------------------|
| `generic_email` | info@company.sa | CC1 |
| `role_email` | sales@ / proposals@ | CC2 |
| `main_phone` | الخط الرئيسي المنشور | CC1–CC2 |
| `whatsapp_business_public` | wa.me link منشور | CC2 |
| `contact_form` | نموذج صفحة Contact | CC1 |
| `linkedin_company` | صفحة الشركة العامة | CC2 |
| `x_profile` / `instagram_profile` / `facebook_page` | ملفات عامة | CC1 |
| `google_business` | Google Business listing | CC2 |
| `directory_listing` | دليل عام | CC1 |

---

## القواعد

```txt
- is_public يجب أن تكون true لكل قناة (المدقّق يرفض غير ذلك).
- is_personal = true فقط إذا نشرت الشركة اسم شخص على صفحة عامة (نادر) — وإلا false.
- value يجب أن تكون قيمة عامة حقيقية (بريد عام / رقم منشور / رابط).
- source توضّح المصدر: official_website | contact_page | public_social |
  public_directory | public_job_post | public_news | google_business.
- لا بريد شخصي مخمَّن، لا رقم مخمَّن.
```

---

## العلاقة بالباقة

- `public_contact_channels` في الباقة = قائمة `channel_id` تشير لهذه القنوات.
- `phone_if_public` لا تُملأ إلا إذا وُجدت قناة `main_phone` للشركة.
- `email_if_public` لا تُملأ إلا إذا وُجدت قناة `generic_email` أو `role_email`.

> المدقّق يتحقق أن كل `channel_id` مُشار إليه موجود فعلاً، وأن حقول الهاتف/البريد
> مدعومة بقناة عامة مطابقة (لا اختلاق).

---

## ملاحظة على بيانات العيّنة

البيانات الحالية في `contact_channels.jsonl` هي **عيّنات توضيحية لشركات افتراضية**
(نفس أسماء `company_os/revenue/prospects.csv`). في الإنتاج، يجب أن تأتي كل قيمة من
مصدر عام حقيقي تم التحقق منه، مع `source_url` و `verified_at`.
