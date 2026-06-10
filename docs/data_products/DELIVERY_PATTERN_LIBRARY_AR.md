# مكتبة أنماط التسليم — Delivery Pattern Library

> **خمس مراحل تسليم**، مع مُدد نموذجية، معوقات شائعة، معايير نجاح،
> ومستندات تسليم. + معادلة تعقيد التسليم (delivery complexity score).

**الحالة:** Phase 1 من Agent #31  
**التاريخ:** 2026-06-03  
**الإصدار:** v1.0  
**Schema:** `schemas/delivery_pattern.schema.json`  
**البيانات:** `data/data_products/delivery_patterns.jsonl` (13 صف)

---

## 1. المراحل الخمس (Phases)

| # | المرحلة | المدة النموذجية | المالك |
| - | --- | --- | --- |
| 1 | **Kickoff** | 1–10 أيام | CSM + Sales |
| 2 | **Setup** | 1–7 أيام | Delivery |
| 3 | **Pilot** | 5–14 يوم | Delivery + Client |
| 4 | **Optimization** | 4–60 يوم | Delivery (متكرر) |
| 5 | **Handover** | 2–90 يوم | CSM + Client |

---

## 2. المرحلة ١ — Kickoff

- **المدة:** 1–10 أيام حسب العرض (diagnostic = 1–2، custom_company_os = 14–30).
- **المعوقات الشائعة:** `client_access_delay`, `missing_owner`, `approval_loop`.
- **معايير النجاح:**
  - توقيع NDA للوصول إلى البيانات.
  - جدولة ٣ discovery calls.
  - مشاركة leakage map template.
- **مستندات التسليم:** Diagnostic scope doc, Stakeholder map, Data access form.
- **إشارات فشل مبكرة:** لا رد من العميل > 48 ساعة على access، أو stakeholder map بمُقرِّر واحد بدون champion.

---

## 3. المرحلة ٢ — Setup

- **المدة:** 1–7 أيام (simple) حتى 30–60 يوم (custom_company_os).
- **المعوقات:** `data_quality`, `integration_block`, `approval_loop`.
- **معايير النجاح:** CRM export مُستلم، WhatsApp Business access مُعتمد، Top 3 leak hypotheses مُسوّدة.
- **مستندات التسليم:** Leakage map v1, Hypothesis list, Data review notes, Workflow catalog v1, Approvals matrix.
- **إشارات فشل مبكرة:** بيانات CRM > 30 يوم stale، IT > 7 أيام لمنح API access، لا workflow owner مُسمّى.

---

## 4. المرحلة ٣ — Pilot

- **المدة:** 5–14 يوم.
- **المعوقات:** `integration_block`, `stakeholder_change`, `low_engagement`.
- **معايير النجاح:** 20 lead مُستعاد عبر الـ workflow الجديد، recovery rate > 12%، العميل يوقّع على v1.
- **مستندات التسليم:** Workflow spec v1, Recovery dashboard, Pilot results report.
- **إشارات فشل مبكرة:** العميل لا يراجع الأرقام أسبوعياً، < 5 leads في الأسبوع الأول، تغيّر sales owner.

---

## 5. المرحلة ٤ — Optimization

- **المدة:** 4–60 يوم (متكررة شهرياً أو ربع سنوياً).
- **المعوقات:** `scope_creep`, `stakeholder_change`, `low_engagement`.
- **معايير النجاح:** +5pp على recovery rate من baseline، negative-reply handling مُضاف، العميل يملك weekly review.
- **مستندات التسليم:** Workflow v2, Negative-reply playbook, Weekly review template, Optimization backlog.
- **إشارات فشل مبكرة:** regression week-over-week، طلب قنوات خارج النطاق، غياب sales lead عن weekly review.

---

## 6. المرحلة ٥ — Handover

- **المدة:** 2–4 أيام (starter) حتى 30–90 يوم (custom_company_os).
- **المعوقات:** `missing_owner`, `low_engagement`.
- **معايير النجاح:** العميل يدير weekly review بمفرده، كل workflows مملوكة لمستخدم عنده، بدء محادثة renewal.
- **مستندات التسليم:** Handover doc, Operating rhythm deck, Renewal trigger baseline, Renewal MSA, Operating handoff manual.
- **إشارات فشل مبكرة:** العميل يطلب Dealix أن يستمر في weekly review، لا workflow owner مُسمّى، لم يُناقَش renewal قبل أسبوع 6.

---

## 7. معادلة تعقيد التسليم (Complexity Score)

```
complexity_score = Σ (phase_complexity_weight × phase_risk_factor) / Σ weights
```

حيث:
- `phase_complexity_weight` من `delivery_patterns.jsonl` (مثلاً kickoff=0.1, optimization=0.4).
- `phase_risk_factor` = 1 + (عدد blockers / 5).
- النتيجة ∈ [1, 5]:
  - **1–2:** low (delivery مباشر، 1–2 أسابيع).
  - **2–3.5:** medium (يحتاج governance rhythm).
  - **3.5–5:** high (يتطلب steering committee).

### مثال
- عرض `full_revenue_os`:
  - kickoff (0.15 × 1.2) + setup (0.30 × 1.4) + pilot (0.20 × 1.6) + optimization (0.40 × 2.0) + handover (0.15 × 1.2)
  - = 0.18 + 0.42 + 0.32 + 0.80 + 0.18 = 1.90
  - **complexity_score = 1.90 / 1.20 = 1.58** → low (لكن optimization عالية risk)

> معادلة مرجعية. تُعدَّل عند توفر بيانات حقيقية.

---

## 8. أوضاع الفشل الشائعة (Common Failure Modes)

| الوضع | كيف يُكتشف مبكراً | التدخل |
| --- | --- | --- |
| **Setup stall** | لا API access في 7 أيام | escalate إلى IT sponsor |
| **Pilot drift** | weekly review ضائع 2× | CSM يتدخل شخصياً |
| **Scope creep** | change request > 20% | تحويل إلى upsell |
| **Champion loss** | stakeholder change | founder call |
| **Quality drop** | KPIs ترجع week-over-week | optimization cycle |
| **Handover rejection** | العميل يطلب Dealix يستمر | توثيق صريح، شرط زمني |

---

## 9. صاحب التسليم حسب العرض

| العرض | Lead | Setup | Pilot | Optimization | Handover |
| --- | --- | --- | --- | --- | --- |
| revenue_leakage_diagnostic | sales | csm | csm | — | sales |
| follow_up_recovery_workflow | sales | delivery | delivery | delivery | csm |
| ai_revenue_ops_starter | sales | delivery | delivery | csm | csm |
| full_revenue_os | founder | delivery | delivery | delivery | csm |
| monthly_optimization | csm | csm | csm | delivery | csm |
| custom_company_os | founder | delivery | delivery | delivery | founder |

---

## 10. مؤشرات الصحة (Health Signals)

- **Green:** كل مرحلة في معايير النجاح + weekly review منتظم.
- **Yellow:** blocker واحد أو أكثر، يُعالَج في 7 أيام.
- **Orange:** blockers متعددة + stakeholder change.
- **Red:** العميل طلب إنهاء أو لا رد > 14 يوم.

---

## 11. المراجع (References)

- `schemas/delivery_pattern.schema.json`
- `data/data_products/delivery_patterns.jsonl`
- `docs/PILOT_DELIVERY_SOP.md`
- `docs/CUSTOMER_SUCCESS_SOP.md`
- `docs/delivery/SCOPE_CONTROL.md`
- `docs/data_products/OFFER_PERFORMANCE_MODEL_AR.md`
