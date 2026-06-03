# مصفوفة العميل المثالي (ICP MATRIX) — القطاعات العشرة

> **المصدر:** [`data/commercial/icp_segments.yaml`](../../data/commercial/icp_segments.yaml) · الشخصيات: [`buyer_personas.yaml`](../../data/commercial/buyer_personas.yaml) · ربط الألم بالعرض: [`pain_to_offer.yaml`](../../data/commercial/pain_to_offer.yaml) · الكتالوج: [`PRODUCT_CATALOG_AR.md`](./PRODUCT_CATALOG_AR.md).
> العملة `ر.س` · كل الأسعار **نطاق** · **السعر النهائي بموافقة المؤسّس** · الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false`.

## الفكرة
نستهدف قطاعات B2B سعودية بحجم **leads متكرّر** ووصول لصاحب قرار وقدرة دفع.
نحن **نساعد، نرتّب، نقيس، نكشف فرص التحسين، ونقترح** المسار الأنسب — لا نَعِد بنتائج مضمونة.
الأولوية: `1` الأعلى ملاءمة، `4` الأدنى. القدرة على الدفع: `high` / `medium` / `low`.

## المصفوفة (القطاعات العشرة)

| القطاع (sector) | الاسم | أولوية | الشخصيات الأساسية | أبرز الآلام | أول عرض | قدرة الدفع | مُسقِطات (disqualifiers) |
|------------------|-------|:-----:|--------------------|--------------|:-------:|:---------:|--------------------------|
| `marketing_agencies` | وكالات التسويق | **1** | agency_owner · head_of_sales · marketing_manager | lead_leakage · follow_up_chaos · no_proof_case_study_system | `DLX-L1` | medium | no_recurring_leads · wants_mass_sending · refuses_approval_process |
| `training_companies` | شركات التدريب | **1** | training_admissions_manager · operations_manager · ceo_gm | follow_up_chaos · lead_leakage · weak_reporting | `DLX-L1` | medium | no_decision_maker_access · no_recurring_leads |
| `clinics` | العيادات | **2** | clinic_manager · operations_manager · founder_owner | follow_up_chaos · support_overload · weak_reporting | `DLX-L1` | medium | requests_pii_scraping · refuses_privacy_basics |
| `real_estate_teams` | فرق العقار | **2** | head_of_sales · operations_manager · founder_owner | lead_leakage · follow_up_chaos · crm_data_disorder | `DLX-L2` | **high** | wants_guaranteed_sales_claims · wants_mass_sending |
| `professional_services` | الخدمات المهنية | **2** | founder_owner · ceo_gm · head_of_sales | proposal_delay · no_proof_case_study_system · weak_reporting | `DLX-L1` | **high** | no_decision_maker_access · delivery_risk_too_high |
| `local_saas` | SaaS/الخدمات المحلية | **2** | founder_owner · head_of_sales · crm_sales_ops_manager | crm_data_disorder · weak_renewal_upsell · sales_team_inconsistency | `DLX-L3` | **high** | wants_guaranteed_sales_claims · refuses_approval_process |
| `recruitment_agencies` | وكالات التوظيف | **3** | operations_manager · head_of_sales · agency_owner | follow_up_chaos · crm_data_disorder · weak_reporting | `DLX-L2` | medium | no_recurring_leads · refuses_approval_process |
| `education_providers` | مزوّدو التعليم | **3** | training_admissions_manager · marketing_manager · ceo_gm | lead_leakage · follow_up_chaos · slow_onboarding | `DLX-L1` | medium | no_recurring_leads · no_ability_to_pay |
| `logistics_companies` | اللوجستيك والخدمات | **3** | operations_manager · head_of_sales · ceo_gm | sales_team_inconsistency · weak_reporting · crm_data_disorder | `DLX-L3` | **high** | no_decision_maker_access · refuses_approval_process |
| `restaurant_groups` | مجموعات المطاعم | **4** | operations_manager · founder_owner · marketing_manager | follow_up_chaos · weak_reporting · weak_renewal_upsell | `DLX-L1` | medium | no_recurring_leads · wants_mass_sending |

## كيف نقرأ المصفوفة
- **أول عرض** هو نقطة الدخول الموصى بها للقطاع، وليست الباقة الوحيدة — الصعود يتبع الدليل (`proof = observed`).
- القطاعات ذات قدرة الدفع `high` (العقار، الخدمات المهنية، local_saas، اللوجستيك) تدخل غالباً عبر بناء أعمق (`DLX-L2`/`DLX-L3`).
- **المُسقِطات** هنا خاصّة بالقطاع، وتُضاف فوق قائمة الإسقاط العامة في [`DISQUALIFICATION_RULES_AR.md`](./DISQUALIFICATION_RULES_AR.md).
- ربط الألم الكامل بالعرض في [`PAIN_TO_OFFER_MATRIX_AR.md`](./PAIN_TO_OFFER_MATRIX_AR.md) · منطق المطابقة في [`OFFER_MATCHING_RULES_AR.md`](./OFFER_MATCHING_RULES_AR.md).

## ملاحظات الاتساق
- أي ذكر لـ **P1** يعني `DLX-L1` (تشخيص تسرّب الإيرادات، 1,500–5,000 ر.س)، و**P2** يعني `DLX-L5` (الاشتراك الشهري، 3,000–15,000/شهر).
- تفصيل الشخصيات في [`BUYER_PERSONAS_AR.md`](./BUYER_PERSONAS_AR.md) · منطق الترتيب والتقسيم في [`MARKET_SEGMENTATION_AR.md`](./MARKET_SEGMENTATION_AR.md).
- الأمثلة في الوثائق ذات الصلة بأسماء افتراضية فقط (Digital Rise Agency، Growth Labs SA، TrainMe KSA، Horizon Realty Team، CloudShift Consulting، Nexus IT Solutions) ومعلّمة «مثال توضيحي».

---
*Dealix · مصفوفة العميل المثالي · المصدر: data/commercial/icp_segments.yaml · السعر النهائي بموافقة المؤسّس.*
