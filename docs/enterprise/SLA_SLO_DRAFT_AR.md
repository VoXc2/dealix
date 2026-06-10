# SLA / SLO Draft — Dealix (AR)

> **Note:** هذه **مسودة أولية**. أي SLA نهائي يحتاج مراجعة قانونية وتوقيع العميل.

---

## 1. Definitions

- **SLO (Service Level Objective):** هدف داخلي قد نتجاوزه أو نقصر عنه
- **SLA (Service Level Agreement):** التزام تعاقدي، التقصير فيه = service credit
- **Downtime:** الفترة التي الـ API غير متاح للعميل (نستثني scheduled maintenance)
- **Planned Maintenance:** مُعلنة قبل 48 ساعة، خارج ساعات الذروة

## 2. Service Level Objectives (SLOs)

| Service | SLO | Measurement |
|---------|-----|-------------|
| API availability (monthly) | 99.5% | uptime_minutes / total_minutes |
| API latency (p95) | < 500ms | excluding cold start |
| AI inference (p95) | < 10s | excluding model outage |
| Webhook delivery | 99.0% within 1 min | retries included |
| Data durability | 99.9% | per provider guarantee |
| Backup RPO | < 24h | daily |
| Backup RTO | < 4h | per recovery test |

## 3. Service Level Agreements (SLAs) — قابل للتفاوض

| Tier | Uptime SLA | Credit إذا قصر |
|------|-----------|----------------|
| Standard | 99.0% | 5% monthly fee credit |
| Priority | 99.5% | 10% credit |
| Enterprise | 99.9% | 15% credit + root cause report |

**Calculation:** credit = (SLA - actual) / SLA × monthly_fee (capped)

## 4. Exclusions

- Client-side issues
- Third-party (LLM, email provider) outages (نبلّغ العميل، لا نضمن)
- Force majeure
- Beta features explicitly marked
- Scheduled maintenance

## 5. Reporting

- **Monthly:** availability report to all clients
- **Quarterly:** SLA review meeting (Enterprise)
- **Incident:** root cause within 5 business days for Sev1/Sev2

## 6. Incident Severity Matrix

| Sev | Impact | Response | Resolution target |
|-----|--------|----------|-------------------|
| Sev1 | Service down | < 1h | < 4h |
| Sev2 | Major feature broken | < 4h | < 24h |
| Sev3 | Minor issue | < 1 business day | < 5 business days |
| Sev4 | Cosmetic | next release | next release |

## 7. Client Responsibilities

- Monitor own integrations
- Report issues with context
- Designate authorized contacts
- Comply with usage limits

## 8. Data & Compliance

- Backup RPO/RTO per above
- DPA terms govern data handling
- Breach notification per Privacy Overview

## 9. Termination

- For cause: 30 days cure period
- For convenience: 60 days notice
- Data return: 30 days post-termination
- Audit log retention: per DPA

## 10. Changes to SLA

- 30 days notice for material changes
- Material adverse changes = termination right

---

> **Status:** Draft · **Owner:** Founder + Legal
> **Reviewer:** Operating Council · **Cadence:** كل 6 أشهر
