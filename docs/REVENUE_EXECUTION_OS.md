# Dealix — Revenue Execution OS (ربط المراحل بالكود)

مسار واحد من **warm intro** إلى **proof**. كل خطوة: endpoint أو سكربت أو إجراء يدوي.

| المرحلة | المخرج | كيف في Dealix |
|---------|--------|-----------------|
| Warm intro اختيار | قائمة 10 خانات بدون PII | `python scripts/dealix_first10_warm_intros.py` → `docs/revenue/live/` (مُتجاهَل من git) |
| رسالة مسودة | نص عربي/إنجليزي | `POST /api/v1/sales/script` — [`api/routers/sales.py`](api/routers/sales.py) |
| موافقة قبل إرسال | طابور | `GET /api/v1/approvals/pending` — [`api/routers/approval_center.py`](api/routers/approval_center.py) |
| تصنيف دعم | مسودة / تصعيد | `POST /api/v1/support-os/classify` — [`api/routers/support_os_mode.py`](api/routers/support_os_mode.py) |
| فحص سياسة إجراء | blocked / approval_required | `POST /api/v1/compliance-os/action-check` — [`api/routers/compliance_action.py`](api/routers/compliance_action.py) |
| تشخيص مصغّر | Markdown أو JSON | `python scripts/dealix_diagnostic.py --company "..." --json` — [`scripts/dealix_diagnostic.py`](scripts/dealix_diagnostic.py) |
| لوحة الشركة (بدون jargon تقني) | JSON واحد | `GET /api/v1/company-service/command-center` — [`api/routers/company_service.py`](api/routers/company_service.py) |
| لوحة المشغّل / CEO يومية | JSON واحد | `GET /api/v1/full-ops/daily-command-center` — [`api/routers/revenue_execution.py`](api/routers/revenue_execution.py) |
| Command Center v3 | لقطة | `GET /api/v1/v3/command-center/snapshot` |
| خطط تسليم | حسب service_id | `GET /api/v1/delivery-os/session/{service_id}` (نفس منطق delivery_factory) |
| Proof events | تسجيل / قائمة | `POST/GET /api/v1/proof-ledger/events` — [`api/routers/proof_ledger.py`](api/routers/proof_ledger.py) |
| حزمة إغلاق Pilot 499 | Markdown | `python scripts/dealix_pilot_499_close_pack.py --write` |
| مراحل Pipeline (حقيقة الإيراد) | مرجع | `GET /api/v1/revenue-pipeline/summary` — [`api/routers/revenue_pipeline.py`](api/routers/revenue_pipeline.py) |
| نشر + تحقق | Smoke | `STAGING_BASE_URL=https://api.dealix.me python scripts/launch_readiness_check.py` |

**قاعدة الإيراد:** لا تُسمّى «إيراداً» إلا مع `payment_received` أو التزام مكتوب موثّق — راجع [`docs/revenue/09_MANUAL_PAYMENT_AND_COMMITMENT_POLICY.md`](revenue/09_MANUAL_PAYMENT_AND_COMMITMENT_POLICY.md).

**ممنوع:** cold WhatsApp، إرسال Gmail حي، شحن Moyasar live، scraping، أتمتة LinkedIn، proof مزيف.
