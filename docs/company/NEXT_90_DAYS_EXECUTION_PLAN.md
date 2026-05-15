# Next 90 Days Execution Plan

ترتيب تنفيذي — لا محاولة بناء كل شيء دفعة واحدة.

## Days 1–14: Sellable spine

- تثبيت المرجع: [`MASTER_OPERATING_BLUEPRINT.md`](MASTER_OPERATING_BLUEPRINT.md)، [`SERVICE_READINESS_BOARD.md`](SERVICE_READINESS_BOARD.md)  
- جودة: [`QUALITY_STANDARD_V1.md`](../quality/QUALITY_STANDARD_V1.md)  
- قالب Proof: [`PROOF_PACK_TEMPLATE.md`](../templates/PROOF_PACK_TEMPLATE.md)  
- كود: `data_os.import_preview`، `data_os` جودة الجداول، `governance_os.policy_check`، `revenue_os.scoring`، `reporting_os.proof_pack` — مع pytest  

**Exit:** ثلاث خدمات رئيسية لديها offer + scope + checklists + proof path (حسب المجلدات تحت `docs/services/`).

## Days 15–45: أول مبيعات

- هدف: **3 sprints مدفوعة** (Lead Intelligence / Quick Win / Company Brain حسب ICP)  
- لكل عميل: proof pack + قيد في Capital/Value ledgers (يدوي Markdown إن لزم)  
- عمود واحد playbook قطاعي مسودّة  

**Exit:** 3 عملاء مدفوعين، 3 proof packs، QA متوسط ≥ 85 حسب المعيار.

## Days 46–75: Productize & retainer prep

- تكرار التسليم: نفس الـ checklists، أقل احتكاك  
- مسار upsell موثّق: `docs/growth/PROOF_TO_UPSELL_MAP.md`  
- عميل واحد **يمكن** أن يكون pilot لـ monthly cadence (`clients/<slug>/OPERATING_CADENCE.md`)  

**Exit:** مسار retainer واضح لعميل واحد على الأقل؛ قائمة feature مرشحة من التكرار.

## Days 76–90: ضبط ونمو

- مراجعة هامش، تسعير، وسعة تسليم: `DELIVERY_CAPACITY_MODEL.md`، `MARGIN_CONTROL.md`  
- محتوى: منشورات حسب `docs/growth/CONTENT_ENGINE.md`  
- تحديث `SERVICE_READINESS_BOARD` وقرار: ماذا نوقف / نضاعف  

**Exit:** لوحة داخلية بسيطة (Markdown أو جدول) للإيراد، التسليم، QA، ورأس المال.

---

## المطلوب منك هذا الأسبوع فقط (أول 7 أيام)

1. اقرأ Master Blueprint وSERVICE_READINESS_BOARD.  
2. ثبّت قالب PROOF_PACK_TEMPLATE لكل sprint جديد.  
3. شغّل: `pytest tests/test_data_os_helpers.py tests/test_governance_policy_check.py tests/test_revenue_scoring.py tests/test_reporting_os_proof_pack.py -q`  
4. جهّز عرضاً واحداً لـ Lead Intelligence مع demo من بيانات وهمية redacted.  

لا تضف منصة كاملة قبل تكرار التسليم مرتين بنفس الجودة.
