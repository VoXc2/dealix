# Output QA Scorecard — كل مخرج قبل التسليم

**Pass = 85/100** إجمالي. أي **Hard Fail** = رفض التسليم حتى لو ارتفع المجموع.

## الأوزان المقترحة

| المحور | نقاط |
|--------|-----:|
| Business usefulness | 20 |
| Clarity | 10 |
| Data grounding | 15 |
| AI accuracy | 15 |
| Arabic quality | 10 |
| Compliance | 15 |
| Actionability | 10 |
| Visual / report quality | 5 |

(يمكن مواءمتها مع [`QA_DELIVERY_RUBRIC_AR.md`](QA_DELIVERY_RUBRIC_AR.md) داخلياً.)

## Hard Fail — مرفوض

- تسريب PII  
- ادعاء غير مدعوم ببيانات/مصدر  
- proof مزيف  
- لا خطوة تالية واضحة  
- إجابة معرفة بلا مصدر (عندما تكون الخدمة Company Brain)  
- أتمتة غير آمنة أو إرسال خارجي بلا موافقة  
- لغة مبيعات مضمونة النتائج  

## التوثيق

سجّل الـscore في أداة التسليم أو في ملاحظات المشروع قبل handoff.
