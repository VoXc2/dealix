# تقرير أولوية ICP — قالب

> قالب مراجعة دورية. الحقيقة المرجعية للقطاعات والأولويات:
> `data/commercial/icp_segments.yaml`. الترتيب أدناه يعكس `priority` الحالي؛
> حدّثه عند تغيّر المصدر. لا تُكرّر بيانات المصدر — اربط إليها.

- **التاريخ:** 2026-06-03
- **المُراجِع:** (الدور فقط — لا أسماء أشخاص)
- **النطاق:** 10 قطاعات
- **الحالة العامة:** ☐ مكتمل ☐ قيد المراجعة ☐ يحتاج تحديث

---

## ترتيب القطاعات حسب الأولوية والملاءمة

| القطاع | الأولوية | قدرة الدفع | أول عرض | أهم الآلام | الحالة |
|--------|----------|-----------|---------|-----------|--------|
| `marketing_agencies` | 1 | medium | `DLX-L1` | `lead_leakage`, `follow_up_chaos`, `no_proof_case_study_system` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `training_companies` | 1 | medium | `DLX-L1` | `follow_up_chaos`, `lead_leakage`, `weak_reporting` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `clinics` | 2 | medium | `DLX-L1` | `follow_up_chaos`, `support_overload`, `weak_reporting` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `real_estate_teams` | 2 | high | `DLX-L2` | `lead_leakage`, `follow_up_chaos`, `crm_data_disorder` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `professional_services` | 2 | high | `DLX-L1` | `proposal_delay`, `no_proof_case_study_system`, `weak_reporting` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `local_saas` | 2 | high | `DLX-L3` | `crm_data_disorder`, `weak_renewal_upsell`, `sales_team_inconsistency` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `recruitment_agencies` | 3 | medium | `DLX-L2` | `follow_up_chaos`, `crm_data_disorder`, `weak_reporting` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `education_providers` | 3 | medium | `DLX-L1` | `lead_leakage`, `follow_up_chaos`, `slow_onboarding` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `logistics_companies` | 3 | high | `DLX-L3` | `sales_team_inconsistency`, `weak_reporting`, `crm_data_disorder` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |
| `restaurant_groups` | 4 | medium | `DLX-L1` | `follow_up_chaos`, `weak_reporting`, `weak_renewal_upsell` | ☐ نشِط ☐ مراقبة ☐ مؤجّل |

---

## شرائح الأولوية (Tiers)

- **Tier 1 (أولوية 1):** `marketing_agencies`، `training_companies` — تدفّق leads واضح + ألم متابعة حاد + بداية مسار `DLX-L1`.
- **Tier 2 (أولوية 2):** `clinics`، `real_estate_teams`، `professional_services`، `local_saas` — ملاءمة عالية وقدرة دفع متوسطة–عالية.
- **Tier 3 (أولوية 3):** `recruitment_agencies`، `education_providers`، `logistics_companies` — ملاءمة جيدة بعمليات أثقل.
- **Tier 4 (أولوية 4):** `restaurant_groups` — B2B انتقائي، يُختار بحذر.

> تفصيل منطق الترتيب في `docs/commercial/MARKET_SEGMENTATION_AR.md`.

---

## مؤشّرات للمراجعة (تُملأ بأدلة — لا تخمين)

| القطاع | إشارات ملحوظة | جودة الملاءمة | `evidence_level` | ملاحظة |
|--------|----------------|----------------|-------------------|--------|
| (مثال توضيحي) Digital Rise Agency | — | ☐ عالية ☐ متوسطة ☐ منخفضة | `observed` | — |

ملاحظة: أي صف بيانات يحتاج `evidence_level` صريحاً؛ الأمثلة بأسماء افتراضية موسومة «مثال توضيحي».

---

## ملاحظات وقرارات

- (دوّن قرارات إعادة الترتيب وأسبابها — بأدلة ملحوظة)

> سلامة: لا عملاء/أرقام ملفّقة، لا بيانات شخصية (أدوار فقط)، ولا ادّعاءات مضمونة.
> سطر واحد: رتّب القطاعات بالأولوية والملاءمة من `icp_segments.yaml` فقط.
