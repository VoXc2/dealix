# سياسة مخاطر الموردين — Dealix Vendor Risk Policy

> **كل vendor له risk profile.** هذا الـ doc يحدد التصنيف والـ
> mitigation.

**الحالة:** مسودة — Phase 3 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. مستويات المخاطر (Risk Tiers)

| Tier | الوصف | التكرار |
| --- | --- | --- |
| **R0** | لا تأثير | review سنوي |
| **R1** | تأثير محدود | review ربع سنوي |
| **R2** | تأثير متوسط | review شهري |
| **R3** | تأثير عالي | review أسبوعي |
| **R4** | حرج | daily monitoring + runbook |

## 2. عوامل الخطر (Risk Factors)

1. **Data risk** (PII, financial, cross-border)
2. **Business criticality** (revenue-blocking)
3. **Vendor stability** (startup vs enterprise)
4. **PDPL/SOC2** (certification status)
5. **Data residency** (where)
6. **Lock-in** (replacement difficulty)
7. **Concentration** (single vs multiple)

## 3. تصنيف R4 (Critical Risk)

أي vendor يجتمع فيه **اثنان** من:
- critical business
- critical data risk
- concentration (no backup)
- non-PDPL compliant

⇒ **R4.** يحتاج:
- daily monitoring
- runbook موثّق
- backup vendor or manual fallback
- incident drill ربع سنوي

## 4. قائمة R4 الحالية

- **Moyasar** (payments + PII) — backup: HyperPay
- **Railway** (hosting + all data) — backup: Render, Fly.io
- **1Password** (all secrets) — backup: Bitwarden (read-only mirror)
- **AWS S3** (backups) — backup: Cloudflare R2
- **WhatsApp Meta Cloud** (messaging) — backup: Green API / Ultramsg

## 5. Mitigations

1. **Multi-provider chain:** WhatsApp، LLM، search.
2. **Manual fallback runbook:** لكل R4 vendor.
3. **Quarterly drill:** محاكاة vendor outage.
4. **Secret rotation:** ربع سنوي.
5. **Data export:** ability to leave vendor within 30 days.

## 6. حادثة (Incident)

عند حادثة vendor:
1. **Detect:** monitor (Sentry/PostHog/UptimeRobot).
2. **Isolate:** أوقف الـ integration.
3. **Communicate:** للعميل (إذا تأثر).
4. **Fallback:** فعّل backup vendor.
5. **Document:** incident report.
6. **Review:** retro + تحسين.

## 7. المراجع

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/SECURITY_RUNBOOK.md`
- `docs/ON_CALL.md`
- `docs/SLO.md`
- `data/procurement/vendors.jsonl`
- `docs/infra/SECRETS_MANAGEMENT_AR.md`
