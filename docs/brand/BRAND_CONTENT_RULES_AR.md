# Dealix — قواعد المحتوى (Brand Content Rules)

> **الموقع (AR):** «Dealix — نظام تشغيل الإيرادات للشركات السعودية».
> **Positioning (EN):** "Saudi B2B Revenue Operating System".
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`.

كيف تنطبق العلامة على المحتوى اليومي (Content OS — الطبقة 13). كل فكرة تمرّ ببوّابة
العلامة قبل النشر. لا إثبات مفبرك، لا عملاء حقيقيون، لا PII.

---

## 1. الأنواع الأربعة اليومية (Daily content types)

| النوع | الهدف | القاعدة الأساسية |
|------|-------|-------------------|
| **1. رؤية المؤسّس** (founder insight) | وجهة نظر عملية عن تشغيل الإيرادات | رأي/مبدأ، لا وعود نتائج |
| **2. ألم القطاع** (sector pain) | تسمية مشكلة قطاعية حقيقية | يبني على `pain_category`، بلا أرقام مخترَعة |
| **3. تعلّم من الإثبات** (proof-learning) | درس مُعمّم من العمل | كل رقم «مثال توضيحي» + `evidence_level` |
| **4. على شكل حالة** (case-style) | سرد توضيحي لنمط مشكلة/حل | placeholder فقط، وسم «مثال توضيحي» إلزامي |

المخرجات تُدار عبر `reports/content/CONTENT_PRODUCTION_QUEUE.md` ويمكن أن تُسجّل في `data/content/post_ideas.jsonl`.

---

## 2. قواعد إلزامية لكل منشور

- **موافقة مطلوبة:** `approval_required=true`؛ لا نشر تلقائي.
- **لا إثبات مفبرك:** لا عملاء/شعارات/أرقام حقيقية. أي مثال يحمل وسم **«مثال توضيحي»**.
- **placeholder فقط:** Digital Rise Agency · Growth Labs SA · TrainMe KSA · Horizon Realty Team · CloudShift Consulting · Nexus IT Solutions · SkillUp Arabia — أبداً كعملاء حقيقيين.
- **لا PII:** الأشخاص بالدور فقط.
- **أفعال مسموحة فقط** وصفر عبارات ممنوعة (`data/commercial/forbidden_claims.yaml`).
- **الدليل:** كل عبارة كمّية تُنسب لـ `evidence_level` صادق.
- **النبرة:** كما في `docs/brand/BRAND_VOICE_AR.md` — مؤسّسية، عربية أولاً، بلا hype.

---

## 3. جيّد مقابل سيّئ (مثال توضيحي)

| النوع | سيّئ (ممنوع) | جيّد (مسموح) |
|------|---------------|--------------|
| case-style | «ضاعفنا مبيعات وكالة X» (عميل حقيقي/ضمان) | «مثال توضيحي: وكالة Growth Labs SA لاحظت فجوة متابعة — هكذا نرتّبها» |
| proof-learning | «نتائج مضمونة في 30 يوم» | «درس: تغطية المتابعة تتحسّن عندما تُقاس — `evidence_level: observed`» |
| sector pain | «كل العيادات تخسر 50% من الـ leads» | «من أنماط القطاع: تأخّر الرد يكلّف فرصاً — نتحقّق منه بالتشخيص» |

---

## 4. بوّابة العلامة للمحتوى

كل منشور يجتاز نفس بوّابة `docs/brand/BRAND_CLAIMS_POLICY_AR.md`:
النبرة · الدليل · الادّعاء · الدعوة · ملاءمة B2B السعودي · الموافقة. أي بند يفشل ⇒ `needs_revision`.

---

*المرجع: `docs/brand/BRAND_VOICE_AR.md` · `docs/brand/BRAND_CLAIMS_POLICY_AR.md` · `docs/brand/BRAND_MESSAGING_HOUSE_AR.md`. كل محتوى عام: موافقة أولاً، إثبات أولاً.*
