# من الإيراد إلى التسليم — Revenue-to-Delivery System (عربي أولًا)

> العمود الفقري الذي يربط *الاهتمام* بـ *الإيراد* بـ *التسليم* بـ *التجديد* — مع بوابات الموافقة والكيانات والبيانات في كل وصلة.

---

## السلسلة الكاملة (مع الكيانات الحقيقية)

```
رد إيجابي / تقييم
   → عرض  (schemas/proposal · data/proposals)            [موافقة المؤسس على السعر]
   → Proof Pack (schemas/proof_pack · data/proof_packs)   [evidence_level لكل رقم]
   → تسليم دفع (schemas/payment_handoff · data/payments)  [موافقة + تسليم بشري]
   → صفقة مربوحة
   → Sales→Delivery Handoff (schemas/delivery_handoff)    [إلزامي لكل صفقة مربوحة]
   → إعداد أول 14 يوم (schemas/client_onboarding)
   → تقرير قيمة أسبوعي (schemas/weekly_value_report)      [بعد بدء التسليم]
   → قبول (schemas/delivery_acceptance)
   → صحة العميل (schemas/client_health)
   → تجديد/ترقية (schemas/renewal · upsell_opportunity)   [قيمة مُسلَّمة + موافقة]
```

## الوصلات الحرجة (Invariants — يفرضها الفحص والاختبارات)

| الوصلة | القاعدة | يفرضها |
|---|---|---|
| رد إيجابي → ؟ | لا يذهب للدفع المباشر؛ بل حجز/واتساب/إثبات | `test_reply_classification_actions` |
| عرض | يُطابَق بالكتالوج (`product_id`) | `test_proposal_maps_to_product_catalog` |
| سعر نهائي | فقط بموافقة المؤسس | فحص `no_final_price_without_approval` |
| تسليم دفع | لا إرسال بلا موافقة | `test_payment_handoff_requires_approval` |
| صفقة مربوحة | تنتج handoff دائمًا | `test_customer_success_handoff_required` |
| بدء تسليم | يتطلب قالب تقرير أسبوعي | `test_delivery_handoff_required` |
| تجديد/ترقية | قيمة مُسلَّمة (`client_data`+) + استشهاد | `test_renewal_requires_delivered_value` |

## مثال متّسق عبر السلسلة
PROP-1002 (Digital Rise, معتمد) → PRF-1001 (تسرب موثّق) → PAY-1001 (دفعة 1250 ريال، بانتظار الموافقة) → DHO-1001 (handoff) → ONB-1001 (إعداد) → WVR-1001 (المتابعة 43%→61% `measured`) → ACC-1001 (مقبول) → CHS-1001 (صحة 82، أخضر) → REN-1001/UPS-1001 (مبنيّان على WVR-1001).

## الكتالوج كمصدر حقيقة للربط
`data/catalog/product_catalog.json` يوائم SKUs القائمة في `company_os/revenue/proposals.json` مع سلّم الترقية. كل عرض/تسليم/تجديد يشير إلى `product_id` منه.

---
*المرجع الحاكم: `AGENTS.md` · الخريطة: `reports/business_os/COMPLETE_BUSINESS_OS_MAP.md`.*
