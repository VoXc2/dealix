# Dealix — قائمة أصول العلامة (Brand Asset Checklist)

> **الموقع (AR):** «Dealix — نظام تشغيل الإيرادات للشركات السعودية».
> **Positioning (EN):** "Saudi B2B Revenue Operating System".
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`.

جرد أصول العلامة مع جدول بوّابة لكل أصل. كل أصل يجب أن يجتاز بوّابة العلامة قبل
الاستخدام العام. لا أرقام/عملاء حقيقيين؛ الأمثلة بـ placeholder المعتمد فقط.

---

## 1. أصول العلامة الأساسية (Asset inventory)

| الأصل | المرجع | الحالة |
|------|--------|--------|
| الهوية (Identity System) | `docs/brand/BRAND_IDENTITY_SYSTEM_AR.md` | موجود |
| بيت الرسائل (Messaging House) | `docs/brand/BRAND_MESSAGING_HOUSE_AR.md` | موجود |
| التوجيه البصري (Visual Direction) | `docs/brand/BRAND_VISUAL_DIRECTION_AR.md` | موجود |
| الصوت والنبرة (Voice & Tone) | `docs/brand/BRAND_VOICE_AR.md` | موجود |
| سياسة الادّعاءات (Claims Policy) | `docs/brand/BRAND_CLAIMS_POLICY_AR.md` | موجود |
| العلامة في الـ Outbound | `docs/brand/BRAND_OUTBOUND_SYSTEM_AR.md` | موجود |
| قواعد المحتوى (Content Rules) | `docs/brand/BRAND_CONTENT_RULES_AR.md` | موجود |
| الـ Press & Brand Kit | `docs/BRAND_PRESS_KIT.md` | موجود |
| One-pager | `company_os/marketing/one_pagers/one_pager_arabic.md` | موجود |
| كتالوج المنتجات (مصدر الأسماء/الأسعار) | `data/commercial/product_catalog.yaml` | مصدر |
| قائمة الحظر (مصدر الادّعاءات الممنوعة) | `data/commercial/forbidden_claims.yaml` | مصدر |

---

## 2. جدول بوّابة العلامة لكل أصل (Per-asset brand-gate)

> البنود من `docs/brand/BRAND_CLAIMS_POLICY_AR.md`: النبرة · الدليل · الادّعاء · الدعوة · ملاءمة B2B السعودي · الموافقة.

| الأصل | النبرة | الدليل | الادّعاء | الدعوة | B2B سعودي | الموافقة | النتيجة |
|------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| Identity System | ✅ | ✅ | ✅ | n/a | ✅ | ✅ | PASS |
| Messaging House | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| Visual Direction | ✅ | ✅ | ✅ | n/a | ✅ | ✅ | PASS |
| Voice & Tone | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| Claims Policy | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| Outbound System | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| Content Rules | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| Press & Brand Kit | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |
| One-pager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PASS |

> أي أصل جديد يبدأ بحالة `needs_revision` حتى تكتمل كل الأعمدة. أصل يفشل أي عمود ⇒ FAIL ⇒ لا استخدام عام.

---

## 3. قواعد القبول

- **placeholder فقط** في الأمثلة (Digital Rise Agency · Growth Labs SA · TrainMe KSA · Horizon Realty Team · CloudShift Consulting · Nexus IT Solutions · SkillUp Arabia)، ووسم «مثال توضيحي».
- **لا PII**، **لا عناوين `Re:/Fwd:` وهمية**، **صفر عبارات** من `data/commercial/forbidden_claims.yaml`.
- كل عبارة كمّية تحمل `evidence_level` صادقاً.
- الأسماء/الأسعار من الكتالوج فقط؛ لا بدائل مخترَعة.

---

*المرجع: `docs/brand/BRAND_CLAIMS_POLICY_AR.md` · `docs/brand/BRAND_IDENTITY_SYSTEM_AR.md` · `docs/BRAND_PRESS_KIT.md`. الموافقة أولاً، الإثبات أولاً.*
