# كتيّب المحتوى حسب القطاع — Sector Content Playbook (AR)

زوايا محتوى لكل قطاع مستهدَف، مبنية على أنماط ألم حقيقية نلاحظها — لا أرقام مُخترَعة،
ولا أسماء عملاء. القطاعات والآلام مرجعها
`docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md` و`docs/sectors/*`.

## كيف تُستخدم
- لكل قطاع (`sector`) زاوية ألم (`pain_category`) ونوع محتوى مقترَح من الأنواع الأربعة.
- المخرج يدخل `reports/content/CONTENT_PRODUCTION_QUEUE.md` بحالة `draft` وبموافقة قبل النشر.
- أي رقم يحتاج `evidence_level` حقيقياً؛ غير الموثَّق يُحذف.

## الزوايا حسب القطاع
| `sector` | `pain_category` الأساسي | الزاوية (إطار صادق) | نوع المحتوى |
|----------|--------------------------|----------------------|-------------|
| `marketing_agencies` | `follow_up_chaos` | التسرّب غالباً في المتابعة لا في الطلب | `founder_insight` |
| `training_companies` | `lead_leakage` | استفسارات التسجيل التي تموت في واتساب | `sector_pain` |
| `clinics` | `support_overload` | المواعيد والاستفسارات تتكدّس بلا نظام | `sector_pain` |
| `real_estate_teams` | `follow_up_chaos` | مسار استرجاع متابعات مرتّب (نمط عام) | `case_style` |
| `recruitment_agencies` | `proposal_delay` | بطء الترشيح يكلّف فرصاً | `sector_pain` |
| `professional_services` | `proposal_delay` | ما نتعلّمه عن زمن تجهيز العروض | `proof_learning` |
| `education_providers` | `slow_onboarding` | بطء التحاق الطلاب الجدد | `sector_pain` |
| `logistics_companies` | `weak_reporting` | غياب رؤية موحّدة للطلبات | `sector_pain` |
| `restaurant_groups` | `crm_data_disorder` | بيانات العملاء مبعثرة بين الفروع | `sector_pain` |
| `local_saas` | `weak_renewal_upsell` | ضعف نظام التجديد والترقية | `founder_insight` |

## قواعد السلامة للقطاعات
- زاوية الألم **عامة وقابلة للملاحظة**، لا تنسب نتيجة لعميل بعينه.
- محتوى `case_style` يبقى نمطاً موسوماً «مثال توضيحي» بأسماء افتراضية فقط
  (Digital Rise Agency، CloudShift Consulting، Horizon Realty Team).
- لا عبارات محظورة («نضمن»، «نضاعف الإيرادات»، «بدون مخاطرة»، «10x» ...).
- الأفعال المسموحة فقط: نساعد، نقلّل، نرتّب، نحلّل، نوضّح، نلاحظ.
- PII: الأدوار فقط؛ لا أسماء أشخاص/شركات حقيقية.

## الربط
- المحرّك: `docs/content/CONTENT_ENGINE_AR.md`.
- تحويل الإثبات الحقيقي: `docs/content/PROOF_TO_CONTENT_SYSTEM_AR.md`.
- خط دراسات الحالة: `docs/content/CASE_STUDY_PIPELINE_AR.md`.
- كتيّبات القطاعات التفصيلية: `docs/sectors/*`.

## مراجعة أسبوعية
أوقف الزوايا الأضعف تفاعلاً، ضاعف الأقوى، حدّث الجدول. أي تحديث يبقى ضمن
حصر الأنواع الأربعة وبوّابة الموافقة.
