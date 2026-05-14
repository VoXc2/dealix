# Incident Response

Dealix تحتاج مسار استجابة **قبل** أن تصبح «كبيرة جدًا».

## أنواع حوادث شائعة

تسريب/تعامل خاطئ مع PII · سوء استخدام مصدر · إجراء خارجي غير مُعتمد · ادعاء غير مدعوم · إجابة هلوسة · خلط بيانات عميل · مخالفة شريك.

## التدفق

Detect → Contain → إشعار المالك الداخلي → تقييم الشدة → تصحيح المخرج → تسجيل الحادث → **تحديث قاعدة** → **اختبار** → **تحديث playbook**

**الكود:** `INCIDENT_RESPONSE_STEPS` و`incident_control_closure_ok` — `institutional_control_os/incident_response.py`

## القاعدة

**كل حادث** يجب أن ينتج rule أو test أو تحديث checklist — **anti-fragile**.

**صعود:** [`../enterprise/RED_TEAM_SYSTEM.md`](../enterprise/RED_TEAM_SYSTEM.md) · [`INSTITUTIONAL_GOVERNANCE.md`](INSTITUTIONAL_GOVERNANCE.md)
