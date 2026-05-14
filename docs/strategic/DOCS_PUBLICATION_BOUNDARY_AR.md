# حدود النشر والمشاركة الخارجية للوثائق

**الغرض:** تحديد **ما يُسمح بمشاركته** مع كل جمهور دون كشف تشغيل داخلي أو بيانات حساسة.

## مستويات المشاركة

| المستوى | المعنى |
|---------|--------|
| **Public** | يمكن نشره علنًا (لغة عامة، دستور مبسّط، فئة سوق). |
| **Partner-safe** | يُرسل لشريك بعد موافقة؛ لا مفاتيح ولا بيانات عملاء. |
| **Investor-safe** | يُستخدم في diligence / deck؛ لا أسرار تشغيل دقيقة. |
| **Client-facing** | ضمن عقد Sprint أو تسليم موقّع. |
| **Internal-only** | داخل Dealix فقط. |
| **Secret / Never publish** | مفاتيح، رموز، بيانات عميل، خطوط أنابيب خاصة، أنماط تخزين إدارية. |

## أمثلة إرشادية (ليست قائمة إغلاق)

**Public (أمثلة):** لغة فئة عامة، مبادئ موافقة-أولاً، روابط صفحات عامة إن وُجدت.

**Partner-safe:** [IP_LICENSE_OUTLINE_AR.md](../40_partners/IP_LICENSE_OUTLINE_AR.md)، [BU4_TRUST_ACTIVATION_GATE_AR.md](../enterprise_trust/BU4_TRUST_ACTIVATION_GATE_AR.md)، أجزاء منستخرجة من [HOLDING_OFFER_MATRIX_AR.md](HOLDING_OFFER_MATRIX_AR.md) بعد إزالة أرقام حساسة.

**Investor-safe:** [HOLDING_VALUE_REGISTRY_AR.md](HOLDING_VALUE_REGISTRY_AR.md)، [DEALIX_EXECUTION_WAVES_AR.md](DEALIX_EXECUTION_WAVES_AR.md) (موجات)، ملخص إيراد من المصفوفة — مع مراجعة يدوية.

**Client-facing:** [PROOF_DEMO_PACK_5_CLIENTS_AR.md](../commercial/PROOF_DEMO_PACK_5_CLIENTS_AR.md)، [RETAINER_PILOT_MINI_AR.md](../commercial/RETAINER_PILOT_MINI_AR.md)، كتالوج خدمات متفق عليه في العقد.

**Internal-only:** ملاحظات تسعير خام، runbooks فيها أسماء أنظمة داخلية، `docs/ops/` غير المؤرشفة للخارج، لقطات JSON تشغيلية.

**Never publish:** مفاتيح API، tokens، قواعد بيانات عملاء، مسودات خط أنابيب شركاء خاصة.

## ربط Doctrine

لا تُشارك أي وثيقة تتعارض مع **NON_NEGOTIABLES** (لا إرسال بارد آلي، لا scraping كقناة بيع، إلخ) كوعد للعميل الخارجي.

## قائمة فحص قبل أي إرسال خارجي (Trust & Diligence OS)

قبل الضغط على «إرسال»:

1. هل الحزمة مدرجة في [EXTERNAL_PACK_REGISTRY_AR.md](EXTERNAL_PACK_REGISTRY_AR.md)؟
2. هل كل ملف فيها ضمن **Partner-safe** / **Client-facing** / **Investor-safe** حسب الجمهور؟
3. هل تخلو من أسرار (مفاتيح، pipeline خام، logs إدارية، markers داخلية)؟
4. هل تخلو من ادّعاءات «معتمد / موافق / compliant» بلا دليل؟
5. هل **usage log** جاهز لإضافة `entries` مباشرة بعد الإرسال؟

انظر أيضًا: [OS_ASSET_OPERATING_MODEL_AR.md](OS_ASSET_OPERATING_MODEL_AR.md)، واختبار دخان [tests/test_external_pack_safety.py](../../tests/test_external_pack_safety.py).

## المراجعة

أي ترقية من Internal إلى Partner-safe أو Investor-safe تمر بمراجعة شهرية أو طلب موافقة صريح (انظر [DOCS_REVIEW_CADENCE_AR.md](DOCS_REVIEW_CADENCE_AR.md)).
