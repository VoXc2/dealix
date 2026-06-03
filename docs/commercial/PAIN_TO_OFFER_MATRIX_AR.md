# مصفوفة الألم ← العرض — Dealix

> الحقيقة المرجعية: `data/commercial/pain_to_offer.yaml` (يفرضها
> `tests/test_commercial_offer_mapping.py`). المنتجات في
> `data/commercial/product_catalog.yaml`. هذا المستند عرض للقراءة ولا يكرّر الكود.

القاعدة: كل فئة ألم تُطابِق عرضاً واحداً من السلّم (DLX-L0..L6) + إجراء تالٍ +
مستوى إثبات مطلوب + اشتراط موافقة. **الموافقة مطلوبة دائماً** والقيم الافتراضية:
`dry_run=true` و`approval_required=true` و`send_enabled=false`.

---

## المصفوفة الكاملة (10 فئات ألم)

| # | فئة الألم | العرض الموصى به | السلّم | الإجراء التالي (`next_action`) | الإثبات المطلوب | موافقة |
|---|-----------|------------------|--------|-------------------------------|-----------------|--------|
| 1 | `lead_leakage` | Revenue Leakage Diagnostic | `DLX-L1` | `book_revenue_leakage_diagnostic` | `observed` | نعم |
| 2 | `follow_up_chaos` | Follow-up Recovery Workflow | `DLX-L2` | `scope_followup_recovery` | `observed` | نعم |
| 3 | `crm_data_disorder` | AI Revenue Ops Starter | `DLX-L3` | `scope_revenue_ops_starter` | `observed` | نعم |
| 4 | `proposal_delay` | Proposal Factory + Proof Pack | `DLX-L3` | `scope_proposal_factory` | `observed` | نعم |
| 5 | `weak_reporting` | Weekly Revenue Command | `DLX-L5` | `offer_weekly_revenue_command` | `observed` | نعم |
| 6 | `sales_team_inconsistency` | Sales Playbook + Draft Factory | `DLX-L3` | `scope_sales_playbook` | `observed` | نعم |
| 7 | `support_overload` | Support Triage / Draft OS | `DLX-L3` | `scope_support_draft_os` | `observed` | نعم |
| 8 | `no_proof_case_study_system` | Proof Pack Factory | `DLX-L1` | `scope_proof_pack_factory` | `observed` | نعم |
| 9 | `slow_onboarding` | Delivery Handoff OS | `DLX-L3` | `scope_delivery_handoff` | `observed` | نعم |
| 10 | `weak_renewal_upsell` | Renewal Engine | `DLX-L5` | `offer_renewal_engine` | `observed` | نعم |

> «Proposal Factory + Proof Pack»، «Weekly Revenue Command»، «Sales Playbook + Draft
> Factory»، «Support Triage / Draft OS»، «Proof Pack Factory»، «Delivery Handoff OS»،
> «Renewal Engine» هي أسماء حِزم/مخرجات داخل السلّم المُشار إليه (L1/L3/L5)، لا مستويات منفصلة.

---

## ماذا تعني الحقول

- **العرض الموصى به**: أول حِزمة نقترحها لمعالجة الألم — نقطة بداية لا التزام نهائي.
- **السلّم (`ladder_id`)**: المستوى المُسعّر في الكتالوج (`DLX-L1`/`L2`/`L3`/`L5`).
- **`next_action`**: الخطوة التشغيلية التالية فقط (حجز/تحديد نطاق/عرض) — ليست وعداً بنتيجة.
- **الإثبات المطلوب (`evidence_required`)**: الحد الأدنى لمستوى الدليل قبل التوصية.
  كلها هنا `observed` — أي نحتاج إشارة ملحوظة (عيّنة بيانات/وصف عملية)، لا افتراضاً.
- **موافقة (`approval_required`)**: دائماً `نعم`. لا إرسال ولا تسعير نهائي بلا اعتماد المؤسّس.

## مستويات الإثبات (تصاعدي)

`none` < `assumed` < `observed` < `verified`. التوصية تتطلّب `observed` فأعلى؛
وكل ادّعاء كمّي يحمل `evidence_level` صريحاً ولا يُذكر دون دليل.

---

## ملاحظات سلامة

- لغة مسموحة فقط: نساعد، نجهّز، نرتّب، نقيس، نكشف فرص التحسين، نقترح، نجهّز مسودّات بموافقة.
- ممنوع: نضمن / نضاعف الإيرادات / نتائج مضمونة / بدون مخاطرة / يبيع عنك بالكامل / 10x.
- لا أرقام أو نسب تحويل ملفّقة؛ أي مثال يُوسم «مثال توضيحي» وبأسماء افتراضية فقط
  (Digital Rise Agency، Growth Labs SA، TrainMe KSA، Horizon Realty Team،
  CloudShift Consulting، Nexus IT Solutions).
- التسعير نطاق فقط، والسعر النهائي يتطلّب موافقة المؤسّس (راجع
  `docs/commercial/QUOTE_APPROVAL_POLICY_AR.md`).

> سطر واحد: ألم واحد ← عرض واحد + إجراء + إثبات `observed` + موافقة؛ المصدر `pain_to_offer.yaml`.
