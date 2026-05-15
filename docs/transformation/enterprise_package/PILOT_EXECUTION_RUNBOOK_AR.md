# تشغيل بايلوت المؤسسة — دليل تنفيذي

هذا الدليل يربط قوالب `docs/transformation/enterprise_package/` بتشغيل حقيقي داخل Dealix مع الإبقاء على سياسة **الموافقة أولًا** و**عدم الإرسال الخارجي التلقائي**.

## قبل بدء البايلوت

1. أكمل النطاق باستخدام [pilot_scope_template.md](pilot_scope_template.md).
2. جهّز حزمة الثقة من [trust_compliance_pack_template.md](trust_compliance_pack_template.md).
3. جهّز إجابات المشتريات من [procurement_response_kit_template.md](procurement_response_kit_template.md).
4. جهّز رواية تحقيق القيمة من [roi_realization_narrative_template.md](roi_realization_narrative_template.md).

## ربط Golden Chain والجواز

| المرحلة | مرجع API |
|---------|----------|
| مرجعية القرار | `GET /api/v1/decision-passport/golden-chain` |
| مستويات الأدلة | `GET /api/v1/decision-passport/evidence-levels` |
| مسار intake للتحقق السريع | `POST /api/v1/leads` |
| كتالوج Revenue OS | `GET /api/v1/revenue-os/catalog` |

## سياسات تشغيلية إلزامية

- أي إجراء خارجي أو عالي المخاطر يبقى **مسودة** حتى تظهر تذكرة موافقة في Human-AI / Approval Center.
- أي مقياس “ measured ” للقيمة يجب أن يحمل `source_ref` (انظر اختبارات قيمة المحرك).
- كل نشاط بايلوت يُربَط بـ `tenant_id` واضح (ولا يُستخدم `default` في الإنتاج).

## خطوات أسبوعية موثقة (Operating Proof)

1. ولّد حزمة الأسبوع:  
   `python3 scripts/generate_weekly_operating_proof_pack.py --out docs/transformation/evidence/weekly_proof_latest.md`
2. حدّث الحقول الرقمية لكل KPI في لوحة الداخلية وفق الحقول المذكورة في [`../../../dealix/transformation/kpi_registry.yaml`](../../../dealix/transformation/kpi_registry.yaml) (لا تُعدّل الحقول الآلية إلا عبر PR موافَق عليه).
3. ثبّت أسماء الملاك البشر في [`../../../dealix/transformation/ownership_matrix.yaml`](../../../dealix/transformation/ownership_matrix.yaml).

## التحقق

- `python3 scripts/verify_global_ai_transformation.py --check-enterprise-package`
- `bash scripts/verify_global_ai_transformation.sh`

## تعريف اكتمال البايلوت

- نطاق موقّع + Decision Passport محفوظ لكل مرحلة حاسمة.
- Proof Pack أولي مرفوع ومراجع (`pytest tests/test_proof_pack.py` عند الاستخدام).
- لا مخالفات للحواجز الثلاثة في [`../../../dealix/transformation/kpi_registry.yaml`](../../../dealix/transformation/kpi_registry.yaml).
