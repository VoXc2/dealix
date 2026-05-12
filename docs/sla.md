# Dealix Service Level Agreement (SLA)

**Status:** v1 — initial publication, effective 2026-05-12.
**Owner:** founder@ai-company.sa
**Contract scope:** Applies to paying customers on the Growth and Scale tiers.
Starter / pilot tier customers receive best-effort support; this document still
governs how the platform behaves and how we respond.

> **Trust signal.** This SLA exists because enterprise buyers ask for it. The
> targets here are the *floor* — we measure and report against them publicly
> at `/api/v1/status` and at [/trust](../landing/trust/index.html).

---

## 1. Availability

| Metric | Target | Measurement window | Exclusions |
| --- | --- | --- | --- |
| API uptime (`api.dealix.me`) | **99.5 %** | Rolling 30 days | Scheduled maintenance announced ≥48 h in advance; force majeure; upstream LLM provider outages clearly attributed in incident timeline. |
| Public landing (`dealix.me`) | **99.9 %** (static, GitHub Pages) | Rolling 30 days | GitHub Pages outages. |

**Calculation.** Uptime = `(total_minutes - downtime_minutes) / total_minutes * 100`, where downtime is the cumulative period during which `/healthz` returns non-2xx for ≥3 consecutive probes (probe interval ≤60 s).

## 2. Latency

| Endpoint class | p50 | p95 | p99 |
| --- | --- | --- | --- |
| Public health probes (`/healthz`, `/ready`, `/live`) | ≤ 50 ms | ≤ 150 ms | ≤ 300 ms |
| Authenticated read API (e.g. `/api/v1/leads`, `/api/v1/sales/*`) | ≤ 200 ms | ≤ 500 ms | ≤ 1 200 ms |
| Authenticated write API | ≤ 350 ms | ≤ 800 ms | ≤ 2 000 ms |
| LLM-backed endpoints | best-effort (depends on upstream provider) | — | — |

Latency is measured server-side, excluding network/internet round-trip.

## 3. Incident severity

| Severity | Definition | MTTA (acknowledge) | MTTR (restore) |
| --- | --- | --- | --- |
| **SEV-1** | Complete outage of any customer-facing endpoint, or confirmed security breach. | 15 min, 24×7 | 2 h |
| **SEV-2** | Degraded performance (>3× p95 baseline), partial feature unavailability, or successful exploit attempt without breach. | 30 min business hours | 8 h |
| **SEV-3** | Cosmetic, minor functional bug, or single-customer issue with workaround. | Next business day | 5 business days |

**Business hours:** 09:00–18:00 Asia/Riyadh, Sun–Thu.

## 4. Change management

- All production deploys go through CI (`.github/workflows/ci.yml`); failed
  Codecov, ruff, mypy, or Trivy checks block merge.
- Customer-impacting schema migrations are announced at least 24 h before
  rollout via the status page.
- Rollback target: ≤10 min from decision to previous-known-good image.

## 5. Maintenance windows

- **Preferred:** Sunday 02:00–04:00 Asia/Riyadh (off-peak Saudi business).
- **Notification:** at minimum 48 h in advance, via status page + email to
  account contacts.
- Maintenance time **does not** count against availability targets.

## 6. Support response

| Channel | Coverage | Response target |
| --- | --- | --- |
| `support@ai-company.sa` (email) | 24 × 7 (acknowledgement); business hours (substantive) | 1 business day |
| `security@ai-company.sa` (vulnerability) | 24 × 7 | 48 h acknowledgement, 7-day resolution timeline (per [SECURITY.md](../SECURITY.md)) |
| In-app banner / status page | Continuous | Updated within 30 min of any SEV-1/2 |

## 7. Data, backups, disaster recovery

- **RPO** (max data loss): 24 h.
- **RTO** (max restore time): 4 h for SEV-1, 24 h for region-wide loss.
- Postgres logical backups run nightly via `scripts/backup_pg.sh`, retained 14
  days. Quarterly **restore drill** documented in [`docs/ops/dr_drill.md`](ops/dr_drill.md).

## 8. Sub-processors

Dealix relies on the following sub-processors for production workloads. The
list is also published at [/trust](../landing/trust/index.html):

| Sub-processor | Purpose | Data residency |
| --- | --- | --- |
| Anthropic | LLM inference | US |
| OpenAI | LLM inference (fallback) | US |
| Supabase | Postgres + RLS-protected document store | EU / US — see project config |
| Railway | Application hosting | US |
| Sentry | Error monitoring | US |
| Resend | Transactional email | US |
| HubSpot | CRM integration (optional, per-customer) | US |
| Calendly | Booking link (public landing only) | US |

PDPL-sensitive data (Saudi residents) is processed under the cross-border
transfer addendum documented in [docs/CROSS_BORDER_TRANSFER_ADDENDUM.md](CROSS_BORDER_TRANSFER_ADDENDUM.md).

## 9. Reporting and reviews

- The status page (`/api/v1/status`) is the authoritative real-time view.
- Monthly availability report emailed to Growth/Scale customers within 7 days
  of month end.
- Quarterly business review (QBR) with each Scale-tier customer covers SLA
  attainment, incidents, roadmap.

## 10. Changes to this SLA

This document is versioned in git. Changes that *reduce* customer protection
require 30-day advance notice; changes that *increase* protection take effect
immediately upon merge.
