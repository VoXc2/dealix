# Sending Ramp Readiness — Dealix (Phase 8)

Report template for ramp readiness: current verdict and which ramp step is permitted. No step is unlocked without founder approval for that step. Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Ramp plan: `docs/outreach/SENDING_RAMP_PLAN_AR.md`. Ramp system: `docs/outreach/SENDING_RAMP_OS_AR.md`.

---

## 1. Summary

| Field | Value |
|-------|-------|
| Review date | `____` |
| Account ID | `____` |
| Verdict | `____` |
| Warmup status | `____` (not_started / in_progress / complete) |
| Permitted ramp step | `____` |
| send_enabled | **false** until approved |

---

## 2. Step Permission Map

| Week | Daily cap | Permitted now |
|------|-----------|---------------|
| 0 | 0–20 | ☐ |
| 1 | 25–50 | ☐ |
| 2 | 50–100 | ☐ |
| 3 | 100–150 | ☐ |
| 4+ | 150–250 (only if healthy) | ☐ |

> 250 DRAFTS/day always allowed; 250 SENDS/day prohibited until all gates pass.

---

## 3. Gate Check

| Gate | Required | Met |
|------|----------|-----|
| Warmup complete | `warmup_status=complete` | ☐ |
| Auth | SPF/DKIM/DMARC pass | ☐ |
| Bounce | < 2% across current step | ☐ |
| Spam | < 0.1% across current step | ☐ |
| Verdict | ≥ LIMITED_SEND_READY (RAMP_READY to advance) | ☐ |
| Founder approval (this step) | recorded | ☐ |

---

## 4. Decision

| Field | Value |
|-------|-------|
| Step granted | `____` |
| Daily cap set | `____` |
| Approved by | `____` (null until founder signs) |

Auto-pause triggers: bounce ≥ 2%, spam ≥ 0.1%, Low reputation → `PAUSE_REQUIRED`.

---

*Dealix · Sending Ramp Readiness · founder approval per step + auto-pause · send_enabled stays false · Ref: SDAIA PDPL*
