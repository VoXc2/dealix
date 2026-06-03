# سلّم العروض (OFFER LADDER) — منطق الصعود

> **المصدر:** [`data/commercial/product_catalog.yaml`](../../data/commercial/product_catalog.yaml) · التفاصيل الكاملة في [`PRODUCT_CATALOG_AR.md`](./PRODUCT_CATALOG_AR.md).
> ربط الألم بالعرض: [`data/commercial/pain_to_offer.yaml`](../../data/commercial/pain_to_offer.yaml).
> العملة `ر.س` · كل الأسعار **نطاق** · **السعر النهائي بموافقة المؤسّس**.

## الفكرة
السلّم يبدأ بدخول منخفض الاحتكاك، ثم يصعد بحسب حجم الألم والجاهزية والميزانية.
نحن **نساعد ونرتّب ونقيس ونقترح** المسار المناسب — لا نقفز بالعميل لمستوى أعلى من حاجته.

## ترتيب السلّم (ladder order)
`DLX-L0` → `DLX-L1` → `DLX-L2` → `DLX-L3` → `DLX-L4` → `DLX-L5` → `DLX-L6`

## مسار الدخول والصعود (entry → ascent)
| المستوى | دوره في السلّم | يصعد عادةً إلى |
|---------|----------------|----------------|
| `DLX-L0` Readiness Scan | باب الدخول: درجة جاهزية + مسار | `DLX-L1` |
| `DLX-L1` Revenue Leakage Diagnostic (**P1**) | تشخيص يكشف نقاط التسرّب ويرتّب الأولويات | `DLX-L2` |
| `DLX-L2` Follow-up Recovery Workflow | أول بناء تشغيلي: طابور متابعة + قوالب | `DLX-L3` (أو `DLX-L5`) |
| `DLX-L3` AI Revenue Ops Starter | نظام أساسي: workflow + dashboard + تقارير | `DLX-L4` (أو `DLX-L5`) |
| `DLX-L4` Full Revenue OS | طبقة تشغيل أوسع متعددة الـ workflows | `DLX-L5` |
| `DLX-L5` Monthly Optimization Retainer (**P2**) | استمرارية: تحسين شهري + تقارير + تجارب | `DLX-L4` (توسعة) / تجديد `DLX-L5` |
| `DLX-L6` Custom Company OS | نطاق مخصّص موقّع لحالات كبيرة | تجديد عبر `DLX-L5` |

## متى نوصي بكل مستوى
- **`DLX-L0`:** العميل محتار أو لا يعرف من أين يبدأ — نريد درجة جاهزية ومسار سريع.
- **`DLX-L1` (P1):** يوجد شكّ بتسرّب فرص لكن بلا دليل مرتّب — نحتاج تشخيص observed قبل أي بناء.
- **`DLX-L2`:** الألم واضح في المتابعة/استرجاع الفرص ويُراد بناء طابور وقوالب وworkflow موافقة.
- **`DLX-L3`:** يُراد نظام أساسي متكامل (بيانات pipeline مرتّبة + dashboard + تقارير + مسودّات بموافقة) خلال 14–30 يوم.
- **`DLX-L4`:** المؤسسة جاهزة لطبقة تشغيل أوسع عبر عدة فرق مع حوكمة وتقارير تنفيذية.
- **`DLX-L5` (P2):** بعد بناء قائم — استمرارية تحسين شهري وتقارير وتجارب مُقاسة.
- **`DLX-L6`:** متطلّبات مخصّصة كبيرة تتجاوز الباقات، ببيان نطاق موقّع وميزانية معتمدة.

## قاعدة الصعود (لا تخطٍّ بلا دليل)
- لا نبيع مستوى أعلى قبل وجود **proof = observed** يبرّره (ما عدا `DLX-L0` الذي إثباته `assumed`).
- لا نبيع نطاقاً مخصّصاً بسعر باقة مبتدئة — الحالات المخصّصة تذهب إلى `DLX-L6` (قاعدة PR-004).
- `DLX-L1` غالباً بوابة قبل `DLX-L2`+: التشخيص يحدّد ما إذا كان البناء مبرّراً وبأي حجم.
- التجديد والاستمرارية يصبّان في `DLX-L5` لمعظم المسارات (`L2`→`L5`، `L3`→`L5`، `L4`→`L5`، `L6`→`L5`).

## خريطة الألم → العرض الموصى به (مختصر، المصدر pain_to_offer.yaml)
| الألم (pain_category) | العرض الموصى به | المستوى |
|-----------------------|------------------|---------|
| lead_leakage | Revenue Leakage Diagnostic | `DLX-L1` |
| follow_up_chaos | Follow-up Recovery Workflow | `DLX-L2` |
| crm_data_disorder | AI Revenue Ops Starter | `DLX-L3` |
| proposal_delay | Proposal Factory + Proof Pack | `DLX-L3` |
| weak_reporting | Weekly Revenue Command | `DLX-L5` |
| sales_team_inconsistency | Sales Playbook + Draft Factory | `DLX-L3` |
| support_overload | Support Triage / Draft OS | `DLX-L3` |
| no_proof_case_study_system | Proof Pack Factory | `DLX-L1` |
| slow_onboarding | Delivery Handoff OS | `DLX-L3` |
| weak_renewal_upsell | Renewal Engine | `DLX-L5` |

## خريطة الـ Alias (مهمّة للاتساق)
| Alias حيّ | يساوي | الاسم |
|-----------|-------|------|
| **P1** — Revenue Intelligence Sprint | ↔ | `DLX-L1` Revenue Leakage Diagnostic |
| **P2** — AI Sales Ops Retainer | ↔ | `DLX-L5` Monthly Optimization Retainer |

> أي ذكر لـ **P1** يعني `DLX-L1`، وأي ذكر لـ **P2** يعني `DLX-L5`. لا توجد aliases أخرى.

---
*Dealix · سلّم العروض · المصدر: data/commercial/product_catalog.yaml + pain_to_offer.yaml · السعر النهائي بموافقة المؤسّس.*
