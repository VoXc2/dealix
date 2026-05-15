# Post-Launch Scorecard (T+1 / T+7 / T+30)

> Filled by the release captain (currently founder). Single source of truth for "did GA actually go well".

## How to use
- At each milestone (T+1, T+7, T+30), copy the template block at the bottom into a new dated section above it.
- Hard numbers only. No vibes-based assessment.
- Any RED row triggers an action-item with owner + due date.

---

## T+30 — _<fill date>_

### Business (revenue + acquisition)

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| MRR (excluding pilots) | ≥ 10,000 SAR | _fill_ | ⚪️ |
| Paying customers (Starter+) | ≥ 10 | _fill_ | ⚪️ |
| Active pilots | ≥ 30 | _fill_ | ⚪️ |
| Pilot → Paid conversion | ≥ 25% | _fill_ | ⚪️ |
| Landing → Demo conversion | ≥ 2% | _fill_ | ⚪️ |
| Demo → Pilot conversion | ≥ 30% | _fill_ | ⚪️ |
| CAC (blended) | ≤ 500 SAR | _fill_ | ⚪️ |
| LTV / CAC | ≥ 3.0 | _fill_ | ⚪️ |
| Net revenue churn | ≤ 5% | _fill_ | ⚪️ |
| NPS (sampled) | ≥ +40 | _fill_ | ⚪️ |

### Reliability

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Uptime (30-day) | ≥ 99.5% | _fill_ | ⚪️ |
| P95 API latency | < 500ms | _fill_ | ⚪️ |
| SEV-1 incidents | 0 | _fill_ | ⚪️ |
| SEV-2 incidents | ≤ 2 | _fill_ | ⚪️ |
| Mean time to recover (SEV-1/2) | < 30 min | _fill_ | ⚪️ |
| Webhook success rate | ≥ 99% | _fill_ | ⚪️ |
| DLQ depth max in window | ≤ 5 | _fill_ | ⚪️ |
| Backups: 30/30 hourly successful | yes | _fill_ | ⚪️ |
| Restore drill passed (this quarter) | yes | _fill_ | ⚪️ |

### Security & Compliance

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Critical CVEs in deps | 0 | _fill_ | ⚪️ |
| Secrets leaked (gitleaks finds) | 0 | _fill_ | ⚪️ |
| Failed admin-auth attempts (anomalies) | ≤ 5 / day | _fill_ | ⚪️ |
| DSAR requests received | n/a | _fill_ | ⚪️ |
| DSAR responded within 30 days | 100% | _fill_ | ⚪️ |
| PDPL incidents | 0 | _fill_ | ⚪️ |
| Sentry events with PII | 0 | _fill_ | ⚪️ |

### Channels

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| Email send-day total | ≤ 50 / sender | _fill_ | ⚪️ |
| Email bounce rate | < 5% | _fill_ | ⚪️ |
| Email reply rate | ≥ 8% | _fill_ | ⚪️ |
| WhatsApp delivery rate | ≥ 95% | _fill_ | ⚪️ |
| WhatsApp opt-out rate | < 5% | _fill_ | ⚪️ |
| Calendly bookings | ≥ 20 / month | _fill_ | ⚪️ |

### Action items

| # | Item | Owner | Due |
|---|------|-------|-----|
| 1 | _fill_ | _fill_ | _fill_ |

### Notes
_Free-text retro of the month._

---

## T+7 — _<fill date>_

(same template, week scope; bar: 1/4 of T+30 numbers)

---

## T+1 — _<fill date>_

(same template, day scope; bar: 1/30 of T+30 numbers, plus mandatory 100% backup success, 0 SEV-1)

---

## Status legend

- 🟢 met or beat target
- 🟡 within 10% below target
- 🔴 > 10% below target — triggers action item
- ⚪️ not yet measured

---

## Template (copy when filling)

```markdown
## T+N — YYYY-MM-DD

### Business
| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| ... |

### Reliability
...

### Security & Compliance
...

### Channels
...

### Action items
| # | Item | Owner | Due |

### Notes
```
