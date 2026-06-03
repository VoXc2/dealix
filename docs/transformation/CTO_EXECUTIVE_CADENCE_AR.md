# إيقاع CTO التنفيذي — Dealix

مرجع تشغيل أسبوعي للمؤسس/CTO يكمّل [EXECUTIVE_OPERATING_CHECKLIST_AR.md](EXECUTIVE_OPERATING_CHECKLIST_AR.md) و[CEO_ONE_SESSION_MASTER_PLAN_AR.md](CEO_ONE_SESSION_MASTER_PLAN_AR.md).

## أسبوعي (15–25 دقيقة)

```bash
bash scripts/run_cto_weekly_anchor.sh
```

| خطوة | ماذا يفعل |
| --- | --- |
| 1 | `run_executive_weekly_checklist.sh` — proof pack + تحقق التحول + سجل `weekly_ops_checklist.log` |
| 2 | `populate_kpi_baselines_platform_signals.py` — إشارات منصة فقط |
| 3 | `apply_kpi_founder_commercial.py --status` — حالة الحقول التجارية المعلّقة |
| 4 | سطر في `evidence/cto_weekly_anchor.log` |

بعد التشغيل:

1. راجع [dealix/transformation/kpi_founder_commercial_registry.yaml](../../dealix/transformation/kpi_founder_commercial_registry.yaml) وعبّئ أي قيمة جاهزة من CRM/المالية.
2. شغّل `python3 scripts/apply_kpi_founder_commercial.py` (بدون `--status`) لتطبيق القيم على `kpi_baselines.yaml`.
3. حدّث `executive_review.last_ownership_matrix_review_iso` في [ownership_matrix.yaml](../../dealix/transformation/ownership_matrix.yaml).

## شهري / قبل توسع

```bash
bash scripts/run_ceo_one_session_readiness.sh
bash scripts/run_pre_scale_gate_bundle.sh
bash scripts/run_cto_pillar_verify_bundle.sh
bash scripts/run_compliance_gtm_gate_bundle.sh
```

## قبل أي قطع هندسي (JSONL→Postgres / OTEL)

- [ENGINEERING_CUTOVER_RUNBOOK_AR.md](ENGINEERING_CUTOVER_RUNBOOK_AR.md)
- [CUTOVER_PR_CHECKLIST_AR.md](CUTOVER_PR_CHECKLIST_AR.md)
- حقول PR: `external_signal:` و`contract_or_pilot_ref:`

## منتج Dealix Cloud

- خارطة الواجهة: [docs/product/DEALIX_CLOUD_UI_MAP.md](../product/DEALIX_CLOUD_UI_MAP.md)
- مسار UI: `/[locale]/cloud`

## مرتبط

- [CTO_12_PILLAR_BACKLOG.md](CTO_12_PILLAR_BACKLOG.md)
- [README.md](README.md)
