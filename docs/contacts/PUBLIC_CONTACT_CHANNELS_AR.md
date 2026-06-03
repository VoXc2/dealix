# Public Contact Channels — قنوات التواصل العامة

أنواع القنوات التي يتعامل معها النظام، ومتى تُعتبر صالحة للإرسال.

---

## 1. أنواع القنوات (`channel_type`)

| النوع | الوصف | يحمل قيمة؟ |
|-------|-------|-----------|
| `public_email` | إيميل منشور رسميًا | نعم (إن كان عامًا) |
| `public_phone` | هاتف منشور رسميًا | نعم (إن كان عامًا) |
| `contact_form` | نموذج تواصل على الموقع | رابط الصفحة |
| `public_social` | صفحة عامة على وسائل التواصل | رابط عام |
| `role_based_outreach` | استهداف بالدور (لا شخص محدد) | لا قيمة شخصية |
| `founder_provided` | قناة زوّدنا بها المؤسس | نعم (موثّقة) |

---

## 2. العقد

المرجع: `schemas/contact_channel.schema.json`. كل قناة تحمل:

```
pack_id · company_name · channel_type · channel_value(null إن غير منشور)
is_public · verified · source · confidence(C0…C4)
```

في بيانات الـseed: **كل القنوات `channel_value=null` و`verified=false`** — لأننا لا نخترع قيمًا، ويلزم تحقق بشري قبل أي استخدام.

---

## 3. شروط الصلاحية للإرسال

تُعتبر القناة صالحة للإرسال فقط إذا:

```
is_public = true   (أو founder_provided)
verified = true    (تحقق بشري)
الشركة ليست في قائمة المنع
الرسالة تحترم بوابة الجودة (نظام واحد، بلا ادعاء مضمون)
```

`role_based_outreach` مسار مشروع للاستهداف، لكنه يتطلب الوصول لقناة عامة فعلية قبل الإرسال.

---

## 4. المصادر المعتمدة (`source`)

```
official_website · contact_page · public_social · public_directory
public_job_post · public_news · founder_provided · none
```

أي مصدر خارج هذه القائمة (قوائم مشتراة/مسرّبة) **مرفوض**.

---

*Version 1.0*
