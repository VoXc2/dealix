# مقاييس المؤسس الأسبوعية (مصادر حقيقية فقط)

**الغرض:** ربط الأسبوع بـ KPI من CRM + Truth Matrix + أحداث الإثبات — بدون اختراع أرقام.

---

## مصادر الحقيقة

| المصدر | الملف | قاعدة |
|--------|-------|--------|
| KPI تجاري | `kpi_founder_commercial_import.yaml` | من CRM فقط — gitignored |
| سجل KPI | `kpi_founder_commercial_registry.yaml` | بعد `apply_kpi_founder_commercial.py` |
| تكاملات | `founder_integration_truth.yaml` | green/yellow/red يدوياً |
| إثبات أسبوعي | `evidence_events_tracker.csv` | أحداث حقيقية فقط |

---

## أمر واحد

```bash
python scripts/founder_weekly_metrics_bundle.py --write
python scripts/apply_kpi_founder_commercial.py --status
```

**مخرج:** `data/founder_weekly/metrics_{ISO_WEEK}.yaml`

**حكم:** `FOUNDER_WEEKLY_METRICS_VERDICT=READY|BLOCKED`

---

## ضمن الحلقة الأسبوعية

```bash
bash scripts/founder_weekly_loop.sh
```

يشمل الآن حزمة المقاييس قبل أقوى خطة.

---

## مراجع

- [`AGENT_DAILY_WORK_PACKETS_AR.md`](AGENT_DAILY_WORK_PACKETS_AR.md) — حزمة `weekly_metrics_bundle`
- [`FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md`](FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md)
