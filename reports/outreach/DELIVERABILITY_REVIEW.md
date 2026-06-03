# Deliverability Review — Dealix (Phase 8)

Report template for a deliverability review: overall verdict plus per-item checklist status. No real send until verdict >= `LIMITED_SEND_READY` AND founder approval. Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Source checklist: `docs/outreach/DELIVERABILITY_READINESS_CHECKLIST.md`. Account data: `data/outreach/email_accounts.jsonl`.

---

## 1. Summary

| Field | Value |
|-------|-------|
| Review date | `____` |
| Account ID | `____` |
| Verdict | `____` (NOT_READY / DRY_RUN_ONLY / LIMITED_SEND_READY / RAMP_READY / PAUSE_REQUIRED) |
| Items passing | `__ / 12` |
| Founder approval | ☐ (required for LIMITED_SEND_READY+) |
| send_enabled | **false** until approved |

---

## 2. Checklist Status

| # | Item | Status |
|---|------|--------|
| 1 | SPF | ☐ |
| 2 | DKIM | ☐ |
| 3 | DMARC | ☐ |
| 4 | Valid reply-to | ☐ |
| 5 | Unsubscribe endpoint/process | ☐ |
| 6 | Suppression list | ☐ |
| 7 | Bounce handling | ☐ |
| 8 | Sender identity | ☐ |
| 9 | Google Postmaster Tools (or equivalent) | ☐ |
| 10 | Sending domain/subdomain separation | ☐ |
| 11 | Volume ramp | ☐ |
| 12 | No purchased lists | ☐ |

> Item 12 is a hard gate: a purchased-list violation forces `NOT_READY` regardless of other items.

---

## 3. Health Snapshot

| Metric | Value | Healthy |
|--------|-------|---------|
| Bounce rate | `__%` | < 2% |
| Spam complaint rate | `__%` | < 0.1% |
| Postmaster reputation | `____` | High/Medium |

Any breach → `PAUSE_REQUIRED` (see `reports/outreach/DOMAIN_HEALTH_REVIEW.md`).

---

## 4. Decision

| Field | Value |
|-------|-------|
| Verdict confirmed | `____` |
| Permitted action | `____` (e.g. dry-run only / limited send / ramp step N) |
| Approved by | `____` (null until founder signs) |

---

*Dealix · Deliverability Review · send_enabled stays false until verdict >= LIMITED_SEND_READY + founder approval · Ref: SDAIA PDPL*
