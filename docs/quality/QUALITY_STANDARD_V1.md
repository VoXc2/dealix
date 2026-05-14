# Quality Standard v1

النسخة المرجعية للتسليم. متوافقة مع [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md) مع تفاصيل الأوزان والعبور.

## QA Score (من 100)

| Area | Weight |
|------|-----:|
| Business impact | 20 |
| Data quality | 15 |
| AI output quality | 15 |
| Arabic/English quality | 10 |
| Compliance | 15 |
| Reusability | 15 |
| Upsell potential | 10 |

## Pass rule

- **Overall ≥ 85**  
- **Governance / Compliance = 100** (لا تساهل على PII، إرسال خارجي، ادعاءات محظورة، إجابة بلا مصدر عندما تُلزم السياسة)  
- لا مخاطر حرجة غير محلولة  

## Hard failures (تلقائي fail)

- تسرب PII  
- cold WhatsApp أو إرسال خارجي بلا موافقة  
- ادعاء ضمان مبيعات / وعود غير مثبتة  
- proof مزيف  
- إجابة معرفية بلا مصدر عندما المصدر مطلوب  
- أتمتة غير آمنة (إرسال تلقائي، scraping بلا إذن)  
- تقرير نهائي بلا إجراء تالي  
- proof pack بلا مدخلات/مخرجات/خطوة تالية  
- أخطاء تشغيلية حرجة مُ fabrication  

## QA workflow

انظر [`QA_REVIEW_PROCESS.md`](QA_REVIEW_PROCESS.md)، [`AI_OUTPUT_EVALS.md`](AI_OUTPUT_EVALS.md) إن وُجد، و[`docs/product/EVALUATION_REGISTRY.md`](../product/EVALUATION_REGISTRY.md).
