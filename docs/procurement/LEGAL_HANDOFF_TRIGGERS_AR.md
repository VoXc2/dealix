# محفّزات التسليم القانوني (Legal Handoff Triggers)

أي من هذه → **تسليم بشري فوري** (لا التزام آلي، لا نصيحة قانونية ملزمة).
مفروض عبر `core/safety/untrusted.py: requires_human_handoff` و`schemas/legal_review.schema.json`.

| المحفّز | مثال |
|---------|------|
| `contract_terms` | تعديل بنود عقد/اتفاقية خدمة |
| `pricing_commitment` | طلب سعر/خصم نهائي ملزم |
| `data_processing_agreement` | توقيع DPA |
| `refund_dispute` | نزاع استرجاع |
| `regulatory_question` | سؤال تنظيمي/امتثال ملزم |
| `ip_or_confidentiality` | ملكية فكرية/سرية |
| `case_study_permission` | إذن نشر اسم/شعار/اقتباس |
| `complaint_escalation` | شكوى مُصعّدة |
| `privacy_request` | طلب وصول/حذف بيانات |

## الإجراء
```
كشف المحفّز → إيقاف أي رد آلي → فتح legal_review (status=open, requires_human=true,
ai_may_commit=false) → إشعار المؤسس → حل بشري → تدوين
```

## ممنوع
- ❌ التزام قانوني/تعاقدي من وكيل. ❌ سعر نهائي. ❌ نصيحة قانونية ملزمة للعميل.
