# قواعد مطابقة العرض — Dealix

> الحقيقة المرجعية: `data/commercial/pain_to_offer.yaml` +
> `data/commercial/product_catalog.yaml` + `data/commercial/icp_segments.yaml`.
> يفرض المطابقة `tests/test_commercial_offer_mapping.py`؛ وتسبقها بوابة الانسحاب
> `tests/test_walk_away_rules.py`. هذا المستند يشرح المنطق ولا يكرّر البيانات.

المبدأ: لكل عميل **ألم رئيسي واحد ← عرض واحد**. لا نكدّس عروضاً ولا نبيع المستوى الأعلى.
كل توصية تُسجَّل بخمسة عناصر: **(المنتج، فئة الألم، مستوى الإثبات، الإجراء التالي، اشتراط الموافقة)**.

---

## الخطوات

1. **بوابة الاستبعاد أولاً.** مرّر العميل على `evaluate_fit`
   (`DISQUALIFICATION_RULES_AR.md`). إن استُبعد ⇐ توقّف، لا مطابقة.
2. **حدّد الألم الرئيسي.** من إشارات العميل صنّفه ضمن فئة واحدة من العشر
   (`PROBLEM_CATEGORY_MAP_AR.md`). عند تعدّد الآلام: اختر الأعلى أثراً على الإيراد والأقرب لبداية المسار.
3. **طابِق العرض** عبر `pain_to_offer.yaml` (انظر جدول التثبيت أدناه).
4. **تحقّق من ملاءمة القطاع.** قارن العرض الناتج بـ `first_offer` للقطاع في
   `icp_segments.yaml`؛ إن اختلف فالسبب يجب أن يكون إشارة ملحوظة لا تخميناً.
5. **افحص الإثبات.** لا توصية دون `observed` فأعلى. الناقص ⇐ ابدأ بـ `DLX-L0`/`DLX-L1` لجمع الدليل.
6. **سجّل التوصية بالخمسة عناصر** واحفظ `approval_required=true`.

---

## جدول التثبيت (الألم ← العرض)

| فئة الألم | المنتج | السلّم | الإثبات | الإجراء التالي |
|-----------|--------|--------|---------|----------------|
| `lead_leakage` | Revenue Leakage Diagnostic | `DLX-L1` | `observed` | `book_revenue_leakage_diagnostic` |
| `follow_up_chaos` | Follow-up Recovery Workflow | `DLX-L2` | `observed` | `scope_followup_recovery` |
| `crm_data_disorder` | AI Revenue Ops Starter | `DLX-L3` | `observed` | `scope_revenue_ops_starter` |
| `proposal_delay` | Proposal Factory + Proof Pack | `DLX-L3` | `observed` | `scope_proposal_factory` |
| `weak_reporting` | Weekly Revenue Command | `DLX-L5` | `observed` | `offer_weekly_revenue_command` |
| `sales_team_inconsistency` | Sales Playbook + Draft Factory | `DLX-L3` | `observed` | `scope_sales_playbook` |
| `support_overload` | Support Triage / Draft OS | `DLX-L3` | `observed` | `scope_support_draft_os` |
| `no_proof_case_study_system` | Proof Pack Factory | `DLX-L1` | `observed` | `scope_proof_pack_factory` |
| `slow_onboarding` | Delivery Handoff OS | `DLX-L3` | `observed` | `offer/scope: scope_delivery_handoff` |
| `weak_renewal_upsell` | Renewal Engine | `DLX-L5` | `observed` | `offer_renewal_engine` |

كل صف هنا = تعيين 1:1 من `pain_to_offer.yaml`. لا تخترع تعييناً خارجه.

---

## قواعد الترجيح والتعارض

- **ألم واحد فقط لكل توصية.** عند تعدّد الإشارات، رتّب بأثر الإيراد ثم بقرب بداية المسار
  (`DLX-L0` → `L1` → `L2` …) وابدأ بالأدنى المناسب لا الأعلى.
- **مدخل افتراضي عند الغموض:** `DLX-L1` (Revenue Leakage Diagnostic, alias **P1**) لكشف
  التسرّب وترتيب الأولويات قبل أي بناء.
- **التجديد/التوسعة (`DLX-L5`, alias P2):** فقط لعميل لديه نظام قائم أو ناتج من L2/L3/L4
  (راجع `requirements` في الكتالوج)، لا كأول عرض لعميل بارد.
- **التخصيص (`personalization_score`):** P0..P4، والحد الأدنى لطابور الموافقة **P1**
  (شركة + قطاع). دون P1 لا يدخل الطابور.
- **التسعير نطاق فقط**، والسعر النهائي يتطلّب موافقة المؤسّس
  (`docs/commercial/QUOTE_APPROVAL_POLICY_AR.md`).

---

## مثال توصية (مثال توضيحي)

> العميل: **Growth Labs SA** (مثال توضيحي) — وكالة تسويق، الإشارة: leads تدخل ثم تُهمَل.
> - المنتج: Revenue Leakage Diagnostic — فئة الألم: `lead_leakage` — الإثبات: `observed`
>   (وصف العميل لعملية المتابعة) — الإجراء: `book_revenue_leakage_diagnostic` — الموافقة: مطلوبة.
> - الصياغة: «نساعدك نكشف أين تضيع الفرص ونرتّب الأولويات» — لا وعد بنتيجة مضمونة.

---

## سلامة

- لغة مسموحة فقط: نساعد، نجهّز، نرتّب، نقيس، نكشف فرص التحسين، نقترح، نجهّز مسودّات بموافقة.
- ممنوع: نضمن / نضاعف الإيرادات / نتائج مضمونة / بدون مخاطرة / يبيع عنك بالكامل / 10x.
- لا عملاء أو أرقام ملفّقة؛ الأمثلة بأسماء افتراضية موسومة «مثال توضيحي». لا بيانات شخصية — أدوار فقط.

> سطر واحد: استبعِد، ثم طابِق ألماً واحداً بعرض واحد بالخمسة عناصر دائماً.
