# Intelligence Quality Controls

## لماذا؟

الذكاء المركّب **يضخّم** جودة المدخلات؛ إذا كانت المدخلات سيئة، تصبح الأخطاء أسرع وأوسع.

## ضوابط (checklist)

- إخفاء هوية قبل benchmark  
- فصل بيانات العميل عن بيانات الأنماط  
- مراجعة بشرية للرؤى الحساسة  
- لا PII في طبقة الذكاء  
- لا مقاييس سرية في محتوى عام  
- درجة ثقة لكل نمط  

## نطاقات الثقة (مثال تشغيلي)

Low: 1–2، Medium: 3–5، High: 6+ عبر عملاء/قطاعات — راجع `pattern_confidence_band` في `data_intelligence.py`.

## قواعد ذهبية

لا تحوّل نمطًا ضعيفًا إلى benchmark. لا تحوّل anecdote إلى استراتيجية. لا تنشر رؤية بدون anonymization.

## روابط

- [INTELLIGENCE_TO_BENCHMARK_SYSTEM.md](INTELLIGENCE_TO_BENCHMARK_SYSTEM.md) · [INTELLIGENCE_COMPOUNDING_SYSTEM.md](INTELLIGENCE_COMPOUNDING_SYSTEM.md)
