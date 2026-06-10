# قائمة جاهزية التدشين التجاري (Soft Launch)

**الهدف:** صفحة بيع عامة + funnel + آلة يومية موحّدة — **بدون** ادعاء إطلاق مدفوعات Moyasar أو HubSpot live.

## بوابة تحقق واحدة (ابدأ هنا)

**مراجعة سريعة (وثائق ↔ تنفيذ):** [COMMERCIAL_OPS_QUICK_REFERENCE_AR.md](COMMERCIAL_OPS_QUICK_REFERENCE_AR.md)

```bash
bash scripts/verify_dealix_commercial_go_live.sh
# Windows:
powershell -File scripts/verify_dealix_commercial_go_live.ps1
```

يشمل: Founder OS · soft launch · company ready (بدون go-live طويل).

```bash
py -3 scripts/verify_commercial_launch_ready.py
py -3 scripts/verify_commercial_launch_ready.py --strict   # قبل Paid Launch (≥80 target)
py -3 scripts/verify_commercial_launch_ready.py --strict --with-api --with-frontend-build
# Windows صباح واحد:
powershell -File scripts/founder_morning.ps1
```

## حالة Soft Launch (تتبع)

| بند | أمر / مسار | ملاحظة |
|-----|------------|--------|
| توسيع الاستهداف | `py -3 scripts/expand_agency_targets_seed.py` | ≥80 صف في CSV |
| استيراد War Room | `py -3 scripts/import_war_room_targets.py --apply` | بعد تحديث CSV |
| حزمة عميل | [operations/CLIENT_PACK_SOP_AR.md](operations/CLIENT_PACK_SOP_AR.md) | War Room → **حزمة عميل** |
| فرونت اند محلي | `frontend/.env.local` ← `.env.local.example` | Admin key + API URL |
| موعد Soft معلن | **2026-05-17** | إعلان مدفوع بعد 3–5 اجتماعات |
| إنتاج كامل | [PHASE_C_PRODUCTION_LAUNCH_AR.md](../ops/PHASE_C_PRODUCTION_LAUNCH_AR.md) | Moyasar + `official_launch_verify` |

## ابدأ البيع اليوم (~25 دقيقة)

| وقت | المؤسس | النظام |
|-----|--------|--------|
| صباح (~20 د) | `powershell -File scripts/founder_morning.ps1` (أو `run_founder_commercial_day`) + `/ar/ops/founder` | 10 P0 · مسودات لمسة · سوشال · digest |
| نهار | 3–5 لمسات بعد الموافقة | War Room |
| مساء | سطر في evidence CSV | تذكير digest |
| أحد | `/ar/ops/approvals` | CI `weekly-founder-content.yml` |

**مرجع تشغيل:** [FOUNDER_OPERATING_SYSTEM_AR.md](../ops/FOUNDER_OPERATING_SYSTEM_AR.md)

## GTM عام (زائر)

| # | بند | تحقق |
|---|-----|------|
| 1 | `/ar` يعرض 5 أقسام + CTAs | يدوي |
| 2 | Risk Score → `/ar/risk-score` | يدوي |
| 3 | Proof Pack → `/ar/proof-pack` | يدوي |
| 4 | Diagnostic → `/ar/dealix-diagnostic` | يدوي |
| 5 | Partners → `/ar/partners` | يدوي |
| 6 | Learn AEO → `/ar/learn` (فهرس + 6 مقالات) | يدوي |

## آلة المؤسس (يومياً)

```bash
bash scripts/run_founder_commercial_day.sh
```

يشمل: brief · KPI · war_room_sync · import CSV · touch drafts · digest + index.json · social (12w) · AEO verdict.

`py -3 scripts/generate_war_room_touch_drafts.py --dry-run` · `py -3 scripts/expand_social_queue_12w.py`

## War Room + استهداف

- Pool: `docs/commercial/operations/targeting/agency_accounts_seed.csv` (هدف ≥80 صف)
- تدوير: `python scripts/rotate_agency_targets.py --dry-run`
- UI: `/ar/ops` · `/ar/ops/war-room` · `/ar/ops/founder`

## أول Diagnostic مدفوع

- DoD: [operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md)

## Paid Launch (لاحقاً — منفصل عن Soft PASS)

- **ابدأ هنا بعد Soft:** [PAID_LAUNCH_AFTER_SOFT_PASS_AR.md](PAID_LAUNCH_AFTER_SOFT_PASS_AR.md)
- `py -3 scripts/verify_paid_launch_readiness.py` → `PAID_LAUNCH_READINESS=ROADMAP_OK`
- [PAID_LAUNCH_TRACKER_AR.md](PAID_LAUNCH_TRACKER_AR.md) · [../LAUNCH_GATES.md](../LAUNCH_GATES.md)
- لا واتساب بارد · لا LinkedIn آلي

## مراجع

- **[LAUNCH_EXECUTION_NOW_AR.md](LAUNCH_EXECUTION_NOW_AR.md)** — صفحة تنفيذ واحدة (استراتيجية + تكتيك + يومي)
- [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)
- [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md)
- بعد Soft PASS: [PAID_LAUNCH_AFTER_SOFT_PASS_AR.md](PAID_LAUNCH_AFTER_SOFT_PASS_AR.md)
