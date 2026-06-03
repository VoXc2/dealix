# Deliverability Readiness Checklist — Dealix (Phase 8)

The canonical pass/fail checklist that produces a deliverability verdict. No real send is permitted until the verdict is at least `LIMITED_SEND_READY` **and** the founder approves. Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Pairs with the policy: `docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md`. Verdict enum lives in `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`.

---

## 1. Checklist Items (pass / fail)

| # | Item | Pass criteria | Status |
|---|------|---------------|--------|
| 1 | SPF | DNS SPF record present, `spf=pass` | ☐ |
| 2 | DKIM | Key published, `dkim=pass` | ☐ |
| 3 | DMARC | Policy published, `dmarc=pass` | ☐ |
| 4 | Valid reply-to | Real monitored reply-to address | ☐ |
| 5 | Unsubscribe endpoint/process | Working opt-out link or process | ☐ |
| 6 | Suppression list | Active and enforced pre-send | ☐ |
| 7 | Bounce handling | Bounces detected and actioned | ☐ |
| 8 | Sender identity | Honest from-name and from-address | ☐ |
| 9 | Google Postmaster Tools (or equivalent) | Configured and monitored | ☐ |
| 10 | Sending domain/subdomain separation | Dedicated sending subdomain | ☐ |
| 11 | Volume ramp | Ramp plan defined and followed | ☐ |
| 12 | No purchased lists | First-party sourcing only | ☐ |

Data sources: `schemas/email_account.schema.json`, `data/outreach/email_accounts.jsonl`.

---

## 2. Verdict Mapping

| Verdict | Required state |
|---------|----------------|
| `NOT_READY` | Any of items 1–3 (SPF/DKIM/DMARC) failing, OR item 12 (no purchased lists) violated |
| `DRY_RUN_ONLY` (default) | SPF/DKIM/DMARC pass but one or more of items 4–11 still open |
| `LIMITED_SEND_READY` | All 12 items pass AND founder approval recorded |
| `RAMP_READY` | `LIMITED_SEND_READY` sustained + healthy metrics (bounce <2%, spam <0.1%) across the current ramp step |
| `PAUSE_REQUIRED` | A health threshold breached at any time (overrides all above) |

Item 12 is a hard gate: a purchased-list violation forces `NOT_READY` regardless of other items.

---

## 3. Health Thresholds (for RAMP_READY / PAUSE_REQUIRED)

| Metric | Healthy | Pause trigger |
|--------|---------|---------------|
| Bounce rate | < 2% | ≥ 2% |
| Spam complaint rate | < 0.1% | ≥ 0.1% |
| Postmaster reputation | High/Medium | Low |

See `docs/outreach/DOMAIN_HEALTH_RUNBOOK.md` and `docs/outreach/BOUNCE_UNSUBSCRIBE_HANDLING_AR.md`.

---

## 4. Sign-off

| Field | Value |
|-------|-------|
| Account ID | `____` |
| Items passing | `__ / 12` |
| Verdict | `____` |
| Founder approval | ☐ (required for `LIMITED_SEND_READY`+) |
| send_enabled | **false** until approved |

---

*Dealix · Deliverability Readiness Checklist · send_enabled stays false until verdict >= LIMITED_SEND_READY + founder approval · Ref: SDAIA PDPL*
