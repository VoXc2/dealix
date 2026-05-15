# ROI Discipline

ثلاث مستويات — **لا تخلطها في العرض العلني**.

## Estimated Value

تقدير بناءً على assumptions واضحة (مسودة داخلية / نقاش).

## Observed Value

لوحظ أثناء المشروع (مثال: عدد duplicates في الملف).

## Verified Value

أكدها العميل أو قيست بعد التشغيل.

## قواعد Dealix

لا تخلط Estimated مع Verified في نفس جملة «نتيجة مضمونة».  
لا تستخدم Estimated كدعاية أو case علني.  
**Verified** فقط لـ case studies رسمية.

**الكود:** `RoiConfidence` · `roi_safe_for_public_case` (عامة / case فقط **verified**) · `roi_observed_ok_for_internal_report` (داخلية: observed أو verified) · `roi_must_label_distinct` — `proof_architecture_os/roi_discipline.py`

**صعود:** [`CASE_SAFE_PROOF_SUMMARY.md`](CASE_SAFE_PROOF_SUMMARY.md)
