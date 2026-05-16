# Dealix 2030 — النهاية الاستراتيجية

## الرؤية

Dealix شركة **Platform-First** سعودية: Revenue OS محكوم بالأدلة، وليس CRM عامًا.

## أركان 2030

1. **North Star واحد** — [`north_star_manifest.yaml`](../../dealix/transformation/north_star_manifest.yaml) يغذي KPIs والتقارير الأسبوعية.
2. **200 مبادرة قابلة للقياس** — [`strategic_initiatives_registry.yaml`](../../dealix/transformation/strategic_initiatives_registry.yaml) (phase 1: 1–100، phase 2: 101–200).
3. **حوكمة Policy-as-Code** — لا إرسال بارد؛ approval-first؛ مسارات Fast/Governed.
4. **منصة API بملكية domains** — SLO/error budget لكل مجال.
5. **إيراد مربوط بالقيمة** — attribution + Deal Desk + Proof Pack كأصل مبيعات.

## بوابات المراجعة الربع سنوية

| بوابة | تحقق |
|-------|--------|
| مبادرات | `python3 scripts/verify_global_ai_transformation.py --check-initiatives` |
| تشغيل أسبوعي | `bash scripts/run_executive_weekly_checklist.sh` |
| جلسة CEO | `bash scripts/run_ceo_one_session_readiness.sh` |
| إيراد | `bash scripts/revenue_os_master_verify.sh` |

## ما يبقى للمؤسس

- أرقام CRM/مالية في `kpi_baselines.yaml` بمرجع مصدر حقيقي.
- قطع إنتاج ledger/stream بإشارة خارجية فقط.

## الربط بالبرنامج

- خارطة 12 شهر: [PLATFORM_FIRST_12M_ROADMAP_AR.md](PLATFORM_FIRST_12M_ROADMAP_AR.md)
- Playbook تشغيل: [DEALIX_OPERATING_PLAYBOOK_AR.md](DEALIX_OPERATING_PLAYBOOK_AR.md)
