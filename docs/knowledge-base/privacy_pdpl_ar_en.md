# Dealix — Privacy & PDPL Policy / سياسة الخصوصيّة

> **Authoritative.** Aligned with Saudi PDPL (Personal Data
> Protection Law). Support OS privacy_pdpl category routes here.

## Canonical state

```
PDPL_ALIGNED = yes
DATA_RIGHTS_ENABLED = access, correct, delete, export, withdraw
COLD_OUTREACH = blocked (always)
SCRAPING = blocked (always)
PII_REDACTION_ON_WRITE = enabled
DEFAULT_AUDIENCE = internal_only
```

## Arabic — العربيّة

### حقوق صاحب البيانات (PDPL)

- **الوصول**: تطلب نسخة من بياناتك → خلال 30 يوم.
- **التصحيح**: تطلب تصحيح بيانات → خلال 30 يوم.
- **الحذف**: تطلب حذف بياناتك → خلال 30 يوم (مع استثناءات قانونيّة).
- **التصدير**: تطلب نسخة قابلة للنقل → خلال 30 يوم.
- **سحب الموافقة**: تطلب إيقاف معالجة بياناتك → فوريّاً.

### ما لا نفعله

- لا نشارك بياناتك مع أي طرف ثالث بدون موافقتك الصريحة.
- لا نخزّن بياناتك خارج المملكة بدون اتّفاقيّة معالجة بيانات.
- لا نستخدم بياناتك لتدريب نماذج LLM.
- لا نُرسل واتساب بارد، ولا إيميلات تسويقيّة بدون موافقة.

### كيف تطلب حقّك

أرسل بريد إلى المؤسس مع وصف الطلب. كل طلب من هذه الفئة يُصعَّد
فوريّاً ولا يُجاب آليّاً.

## English

### Data subject rights (PDPL)

- **Access**: request a copy of your data → within 30 days.
- **Correct**: request data correction → within 30 days.
- **Delete**: request data deletion → within 30 days (with legal
  exceptions).
- **Export**: request a portable copy → within 30 days.
- **Withdraw consent**: request to stop processing → immediately.

### What we don't do

- We don't share your data with third parties without your explicit
  consent.
- We don't store your data outside KSA without a data processing
  agreement.
- We don't use your data to train LLMs.
- No cold WhatsApp, no marketing email without consent.

### How to exercise rights

Email the founder with the description of the request. Every
request in this category is **immediately escalated** and is never
answered automatically.

## Mandatory escalation triggers

If a customer message contains any of:
- "delete my data" / "احذف بياناتي" / "حذف بيانات"
- "opt out" / "إلغاء الموافقة"
- "GDPR" / "PDPL" / "privacy" / "خصوصيّة"
- "data export" / "تصدير بيانات"

Support OS escalates **immediately** to the founder; no automated
reply is sent.

## Hard rules

- ❌ NO live customer outreach without active consent record
- ❌ NO storing card data
- ❌ NO PII in logs (redaction-on-write enabled in observability_v6
  + observability_v10)
- ❌ NO sharing customer name publicly without signed permission
