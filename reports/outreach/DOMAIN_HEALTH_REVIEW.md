# Domain Health Review — Dealix (Phase 8)

Report template for domain health: SPF/DKIM/DMARC status plus bounce/spam metrics. A health breach forces `PAUSE_REQUIRED`, `send_enabled=false`, `daily_cap=0`. Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Runbook: `docs/outreach/DOMAIN_HEALTH_RUNBOOK.md`. Account data: `data/outreach/email_accounts.jsonl`.

---

## 1. Summary

| Field | Value |
|-------|-------|
| Review date | `____` |
| Domain | `____` (use placeholder, e.g. `optout-example.sa`) |
| Account ID | `____` |
| Verdict | `____` |
| send_enabled | **false** until approved |

---

## 2. Authentication Status

| Record | State | Pass |
|--------|-------|------|
| SPF | `____` | pass / fail / pending |
| DKIM | `____` | pass / fail / pending |
| DMARC | `____` | pass / fail / pending |
| Reply-To valid | `____` | true / false |
| Sending subdomain separated | `____` | true / false |
| Postmaster configured | `____` | true / false |

> Any of SPF/DKIM/DMARC failing keeps the account at `NOT_READY`.

---

## 3. Health Metrics

| Metric | Value | Healthy | Pause trigger |
|--------|-------|---------|---------------|
| Auth pass (SPF+DKIM+DMARC) | `__%` | 100% | < 100% → hold ramp |
| Bounce rate | `__%` | < 2% | ≥ 2% → PAUSE_REQUIRED |
| Spam complaint rate | `__%` | < 0.1% | ≥ 0.1% → PAUSE_REQUIRED |
| Reputation | `____` | High/Medium | Low → PAUSE_REQUIRED |

---

## 4. Action

| Field | Value |
|-------|-------|
| Breach detected | `____` (yes/no) |
| Action taken | `____` (e.g. PAUSE_REQUIRED, daily_cap=0) |
| Resume criteria met | `____` |
| Approved by | `____` (null until founder signs) |

PAUSE procedure + resume criteria: `docs/outreach/DOMAIN_HEALTH_RUNBOOK.md`.

---

*Dealix · Domain Health Review · health breach → PAUSE_REQUIRED, send_enabled=false · no PII (role/domain only) · Ref: SDAIA PDPL*
