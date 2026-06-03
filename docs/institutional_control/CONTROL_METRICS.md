# Control Metrics

قِس **الحوكمة** نفسها — وإلا التوسع يكون هشًا.

## مؤشرات مقترحة

- نسبة مصادر بيانات بها Source Passport  
- نسبة AI runs المسجّلة  
- نسبة المخرجات ذات governance status  
- نسبة مخرجات العملاء التي اجتازت QA  
- نسبة إجراءات خارجية بموافقة مثبتة  
- PII flags · إجراءات غير آمنة المحظورة · تغطية التدقيق · اكتمال Proof Pack  

## عتبات اتجاهية (صارمة للتوسع enterprise)

- تسجيل runs: اتجاه **كامل** قبل توسع خارجي واسع  
- إجراءات خارجية: **موافقة** لكل إطلاق حساس  
- متوسط QA: هدف **≥ 85** قبل scale عدواني  
- Proof Pack: **إلزامي** لإغلاق مشروع / قصص عميل  
- أصل رأس مال لكل مشروع: يقلل **خطر وكالة**  

**الكود:** `enterprise_control_blockers` — `institutional_control_os/control_metrics.py`

**صعود:** [`INSTITUTIONAL_GOVERNANCE.md`](INSTITUTIONAL_GOVERNANCE.md)
