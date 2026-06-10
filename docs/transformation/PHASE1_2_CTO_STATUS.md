# Phase 1–2 — حالة CTO (staging + private beta)

مرجع التتبع الرئيسي: [`PHASE_COMPLETION_TRACKER.md`](../PHASE_COMPLETION_TRACKER.md)

## Phase 1 — Staging + Supabase + مراقبة

| بند | حالة CTO | تحقق |
| --- | --- | --- |
| نشر staging | موثّق | [`STAGING_DEPLOYMENT.md`](../STAGING_DEPLOYMENT.md) · `scripts/smoke_staging.py` |
| Supabase | موثّق | [`SUPABASE_STAGING_RUNBOOK.md`](../SUPABASE_STAGING_RUNBOOK.md) |
| Embeddings | placeholder → جاهزية | `python3 scripts/check_embeddings_readiness.py` |
| مراقبة | موثّق | [`OBSERVABILITY_ENV.md`](../OBSERVABILITY_ENV.md) |

**أمر:** بعد نشر staging: `python scripts/smoke_staging.py --base-url $STAGING_BASE_URL`

## Phase 2 — Private beta

| بند | حالة CTO | تحقق |
| --- | --- | --- |
| قائمة beta | مرجع | [`PHASE2_PRIVATE_BETA_CHECKLIST.md`](../PHASE2_PRIVATE_BETA_CHECKLIST.md) |
| GTM | مرجع | [`GTM_PLAYBOOK.md`](../GTM_PLAYBOOK.md) |
| واتساب | مسودة فقط | [`WHATSAPP_OPERATOR_FLOW.md`](../WHATSAPP_OPERATOR_FLOW.md) |
| PDPL | بوابة | [`SECURITY_PDPL_CHECKLIST.md`](../SECURITY_PDPL_CHECKLIST.md) · `run_compliance_gtm_gate_bundle.sh` |
| Dealix Cloud hub | منفّذ | `/[locale]/cloud` |

## تعريف «Phase 1–2 مكتملة» للـ CTO

- Staging `/health` 200 + smoke staging PASS
- `run_compliance_gtm_gate_bundle.sh` PASS
- Cloud hub + trust-check + approvals مستخدمة داخليًا
- لا إطلاق عام — Paid Private Beta فقط
