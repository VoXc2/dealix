# Deliverability Readiness Checklist — Dealix

A send is permitted only when this checklist passes **and** a human approves.
Verdicts: `NOT_READY · DRY_RUN_ONLY · LIMITED_SEND_READY · RAMP_READY · PAUSE_REQUIRED`.

## Checklist

| # | Item | Required | Status (today) |
|---|------|----------|----------------|
| 1 | SPF record | ✅ | ☐ TBD (founder) |
| 2 | DKIM signing | ✅ | ☐ TBD |
| 3 | DMARC policy (≥ `p=quarantine`) | ✅ | ☐ TBD |
| 4 | Custom tracking domain (if tracking) | if used | ☐ TBD |
| 5 | Valid reply-to (monitored) | ✅ | ☐ TBD |
| 6 | Unsubscribe endpoint/process | ✅ | 🟢 enforced in content |
| 7 | Suppression list (durable + synced) | ✅ | 🟡 engine ready; store TBD |
| 8 | Bounce handling | ✅ | 🟢 routing ready |
| 9 | Sender identity (real person/company) | ✅ | ☐ TBD |
| 10 | Postmaster Tools / equivalent | ✅ | ☐ TBD |
| 11 | Domain/subdomain separation | ✅ | ☐ TBD |
| 12 | Volume ramp plan | ✅ | 🟢 `SENDING_RAMP_PLAN_AR.md` |
| 13 | No purchased lists | ✅ | 🟢 enforced |

## Verdict logic
- Any of 1–3, 5, 9, 11 missing → **NOT_READY / DRY_RUN_ONLY**.
- All infra present, low volume, monitored → **LIMITED_SEND_READY**.
- Stable reputation + warmed mailbox → **RAMP_READY**.
- Bounce spike / spam complaints / blocklist → **PAUSE_REQUIRED** (hard stop).

## Current verdict: **DRY_RUN_ONLY**
Reason: email infra (SPF/DKIM/DMARC, sender identity, Postmaster, domain
separation) not yet provisioned. Content-level guards are already enforced.
