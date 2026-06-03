# Dealix — متتبع الإطلاق المدفوع (Paid Launch)

**القاعدة:** لا ادعاء «إطلاق رسمي كامل» حتى **≥24/30** بوابة في [LAUNCH_GATES.md](../LAUNCH_GATES.md).

**Soft Launch (الآن):** `bash scripts/verify_dealix_commercial_go_live.sh` — funnel + آلة يومية بدون Moyasar live.

---

## بوابات تقنية — أمر تحقق

| ID | البوابة | الحالة | تحقق / FOUNDER_ACTION |
|----|---------|--------|------------------------|
| T1 | `/health/deep` green | راجع LAUNCH_GATES | `curl $API/health/deep` |
| T6 | k6 load prod | مفتوح | `tests/load/k6_smoke.js` + hostname |
| T7 | Rollback tested | مفتوح | RUNBOOK scenario 2 |
| T8 | Backup restore staging | مفتوح | RUNBOOK scenario 5 |
| O3 | PostHog 7 events | **FOUNDER_ACTION** | مفتاح PostHog في `.env` |
| B1 | Moyasar live + webhook | **FOUNDER_ACTION** | [DEPLOYMENT.md](../DEPLOYMENT.md) |
| B2 | HubSpot sync | **FOUNDER_ACTION** | `HUBSPOT_*` |
| B3 | Calendly | **FOUNDER_ACTION** | `CALENDLY_*` |
| C1 | KPI من CRM حقيقي | **FOUNDER_ACTION** | `kpi_founder_commercial_import.yaml` |

---

## بوابات تجارية — تشغيل يومي

| بند | تحقق |
|-----|------|
| صباح canonical | `bash scripts/run_founder_commercial_day.sh` |
| بوابة موحّدة | `bash scripts/verify_dealix_commercial_go_live.sh` |
| استهداف ≥80 | `py -3 scripts/verify_commercial_launch_ready.py --strict` |
| محتوى أسبوعي | CI `weekly-founder-content.yml` |
| أول Diagnostic مدفوع | [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md) |

---

## مراجع

- [COMMERCIAL_LAUNCH_CHECKLIST_AR.md](COMMERCIAL_LAUNCH_CHECKLIST_AR.md)
- [FOUNDER_OPERATING_SYSTEM_AR.md](../ops/FOUNDER_OPERATING_SYSTEM_AR.md)
- [LAUNCH_GATES.md](../LAUNCH_GATES.md)
