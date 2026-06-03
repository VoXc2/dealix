# Domain Health Runbook — Dealix (Phase 8)

Operational runbook for keeping sending domains healthy: SPF/DKIM/DMARC verification, Postmaster monitoring, and the conditions that force `PAUSE_REQUIRED`. This runbook does not enable spam-filter evasion; its goal is honest, well-configured infrastructure.

Pairs with: `docs/outreach/DELIVERABILITY_READINESS_CHECKLIST.md`. Account data: `data/outreach/email_accounts.jsonl` (`schemas/email_account.schema.json`).

---

## 1. Authentication Setup (one-time per domain)

| Record | Purpose | Pass state |
|--------|---------|-----------|
| SPF | Authorize sending hosts | `spf=pass` |
| DKIM | Cryptographically sign mail | `dkim=pass` |
| DMARC | Policy + alignment + reporting | `dmarc=pass` |
| Reply-To | Real, monitored mailbox | `reply_to_valid=true` |
| Sending subdomain | Isolate reputation from root domain | `separated_sending_subdomain=true` |

Record each result on the email account object. Any of SPF/DKIM/DMARC failing keeps the account at `NOT_READY`.

---

## 2. Monitoring (ongoing)

| Source | What to watch | Cadence |
|--------|---------------|---------|
| Google Postmaster Tools (or equivalent) | Domain/IP reputation, spam rate, auth pass % | Daily during ramp |
| DMARC aggregate reports | Alignment + unauthorized sources | Weekly |
| Bounce stream | Hard/soft bounce ratio | Per batch |
| Spam complaints | Complaint rate | Per batch |

`postmaster_configured=true` is required before any send.

---

## 3. Health Thresholds

| Metric | Healthy | Action |
|--------|---------|--------|
| Auth pass (SPF+DKIM+DMARC) | 100% | Below 100% → investigate, hold ramp |
| Bounce rate | < 2% | ≥ 2% → `PAUSE_REQUIRED` |
| Spam complaint rate | < 0.1% | ≥ 0.1% → `PAUSE_REQUIRED` |
| Reputation | High/Medium | Low → `PAUSE_REQUIRED` |

---

## 4. PAUSE_REQUIRED Procedure

1. Set `deliverability_verdict=PAUSE_REQUIRED` on the affected account(s).
2. Set `send_enabled=false` and `daily_cap=0`.
3. Stop the active ramp step; mark any open batch `paused`.
4. Diagnose root cause (auth break, content, list quality, volume spike).
5. Remediate; re-run `DELIVERABILITY_READINESS_CHECKLIST.md`.
6. Resume only after metrics recover and the founder re-approves.

---

## 5. Recovery → Resume Criteria

| Condition | Required |
|-----------|----------|
| Auth | SPF/DKIM/DMARC all pass |
| Bounce | < 2% sustained |
| Spam | < 0.1% sustained |
| Verdict | Re-evaluated to ≥ `LIMITED_SEND_READY` |
| Approval | Founder sign-off |

Report results into `reports/outreach/DOMAIN_HEALTH_REVIEW.md`.

---

## 6. Privacy Note

No PII in monitoring logs or reports. Reference domains and role accounts only (e.g. `optout-example.sa`). Aligns with `company_os/governance/pdpl_checklist.md`.

---

*Dealix · Domain Health Runbook · health breach → PAUSE_REQUIRED, send_enabled=false · Ref: SDAIA PDPL*
