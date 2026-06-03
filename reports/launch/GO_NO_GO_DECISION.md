# Dealix Go / No-Go Decision

The gate that must be signed before any launch. Do not launch without this file.

**Date:** 2026-06-03 · **Prepared by:** Launch Readiness Finalizer · **Decides:** Founder

---

## Decision

- [ ] GO
- [x] CONDITIONAL GO
- [ ] NO-GO

> **CONDITIONAL GO — Internal Dry Run only.** NO-GO for Soft, Controlled, and Full
> Launch until the Launch Score reaches the required band and the open executable
> gates are built.

## Launch Mode

- [x] Internal Dry Run
- [ ] Soft Launch
- [ ] Controlled Launch
- [ ] Full Launch

## Required Evidence

| Evidence | Status | Source |
|----------|:------:|--------|
| Launch score | ⚠ 44.6 / 100 (< 60) | `LAUNCH_SCORECARD.md` |
| GitHub Actions | ✅ present | `.github/workflows/launch-readiness.yml` |
| Site build | ✅ passes | `npm run build` |
| Data contracts | ⚠ no standalone schema check | — |
| Security / privacy | ✅ pass | `SECURITY_GO_NO_GO.md` |
| Delivery readiness | 🟡 SOPs only | `company_os/delivery/*` |
| Email safety | 🟡 policy only, no executable gate | `LAUNCH_BLOCKERS.md` #2 |
| Contact discovery | ✅ no invented contacts | checker scan |
| Founder approval | ⬜ pending signature | below |

## No-Go Reasons (for modes above Internal Dry Run)

- Launch Score 44.6 is below the Soft Launch band (75).
- Executable Email Quality Gate not built (blocker #2).
- Executable Mini Proposal approval gate not built (blocker #6).
- Per-system Delivery Packs incomplete (blocker #1).

## Why Internal Dry Run is a GO

- Safety hard-gates **pass**: no external sending by agents, no invented contacts,
  no guaranteed claims, suppression + untrusted-content policies in place.
- Internal Dry Run is review-only, so the open executable gates do not apply.

## Conditions on this CONDITIONAL GO

1. No external sending of any kind during Dry Run.
2. Every outreach draft stays `pending_approval`.
3. Re-run `python scripts/checks/check_launch_readiness.py` before re-deciding.

## Founder Decision

- Approved by: ____________________  (Founder)
- Mode authorized: Internal Dry Run
- Date: ____________________
- Notes: ____________________

> Update this block on every re-evaluation. Higher modes require a fresh signature.
