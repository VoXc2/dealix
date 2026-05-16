# قائمة التشغيل التنفيذية الأسبوعية (Dealix)

## الغرض

ربط **إثبات السوق** (أرقام + أدلة + ملكية) بـ **البوابات التقنية** دون عكس الترتيب: التشغيل أولاً، القطع الهندسي عند الإشارة فقط.

## 1) أسبوعياً (كل أسبوع تشغيل)

1. شغّل:
   ```bash
   bash scripts/run_executive_weekly_checklist.sh
   ```
   - يولّد حزمة إثبات بتاريخ عبر [`../scripts/run_ceo_signal_weekly_loop.sh`](../scripts/run_ceo_signal_weekly_loop.sh).
   - يشغّل [`scripts/verify_global_ai_transformation.py`](../scripts/verify_global_ai_transformation.py) ويسجّل نتيجة في [`evidence/weekly_ops_checklist.log`](evidence/weekly_ops_checklist.log).
   - عند **PASS** يحدّث تلقائياً حقل `weekly_ops.last_checklist_run_iso` في [`dealix/transformation/kpi_baselines.yaml`](../dealix/transformation/kpi_baselines.yaml) عبر [`scripts/sync_weekly_ops_from_checklist_log.py`](../scripts/sync_weekly_ops_from_checklist_log.py).

2. عبّئ الأرقام الفعلية في [`dealix/transformation/kpi_baselines.yaml`](../dealix/transformation/kpi_baselines.yaml) (`value_numeric` + `source_ref` غير فارغ + `updated_period_iso` عند تغيّر الأرقام).

3. راجع الملاك البشرية في [`dealix/transformation/ownership_matrix.yaml`](../dealix/transformation/ownership_matrix.yaml) وحدّث `executive_review.last_ownership_matrix_review_iso` بعد المراجعة.

## 2) قبل أي توسع قطاعي أو إقليمي

```bash
bash scripts/run_pre_scale_gate_bundle.sh
```

(يجمع بوابات التوسع + `verify_ceo_signal_readiness.sh category_gates`.)

## 3) بوابات تحقق انتقائية (حسب ما تغيّر)

```bash
bash scripts/verify_ceo_signal_readiness.sh          # افتراضي = transformation
bash scripts/verify_ceo_signal_readiness.sh all
bash scripts/verify_ceo_signal_readiness.sh control_plane
bash scripts/verify_ceo_signal_readiness.sh revenue_os
bash scripts/verify_ceo_signal_readiness.sh category_gates
```

## 4) قطع تقني (Postgres / مرآة / OTel)

اتبع [ENGINEERING_CUTOVER_RUNBOOK_AR.md](ENGINEERING_CUTOVER_RUNBOOK_AR.md) ولا تفعّل في الإنتاج بدون إشارة خارجية في وصف PR (`external_signal:`) وفق [`dealix/transformation/engineering_cutover_policy.yaml`](../dealix/transformation/engineering_cutover_policy.yaml).

## 5) إغلاق فجوات وموثوقية

- فهارس أدلة المصفوفة: [`evidence/gap_closure_*.md`](evidence/) مرتبطة بـ [`02_gap_closure_matrix.md`](02_gap_closure_matrix.md).
- تدريبات الموثوقية: [`scripts/reliability_drills_scorecard.py`](../scripts/reliability_drills_scorecard.py) + قالب سجل [`evidence/reliability_drill_log.template.txt`](evidence/reliability_drill_log.template.txt) (السجل البشري للتنفيذ لا يُغني عن الـ scorecard وحده).

## 6) تحقق شامل (عند تغيير واسع أو قبل إصدار)

```bash
bash scripts/verify_global_ai_transformation.sh
```
