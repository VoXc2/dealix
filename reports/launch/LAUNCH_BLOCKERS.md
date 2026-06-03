# Launch Blockers

The 10 critical No-Go blockers. Any **open** blocker = **No-Go** for modes above
Internal Dry Run, even if everything else is ready.

**Status key:** ✅ resolved · 🟡 policy resolved / executable pending · 🔴 open

---

## No-Go blockers

| # | Blocker | Status | Evidence / Gap |
|---|---------|:------:|----------------|
| 1 | No Delivery Pack for each core system | 🟡 | `company_os/delivery/p1_delivery_sop.md` exists; per-system packs for all 5 incomplete |
| 2 | No Email Quality Gate | 🔴 | `draft-quality-gate.js` referenced in `package.json` but **file missing**; policy documented only |
| 3 | No Contact Discovery Policy | ✅ | `data_handling_checklist.md` + `suppression_policy.md` + role-based contacts |
| 4 | System invents numbers/emails | ✅ | `prospects.csv` role-based; checker scan passes (no personal email/phone) |
| 5 | No suppression / do-not-contact | ✅ | `company_os/governance/suppression_policy.md` + `suppression_list.csv` |
| 6 | No Mini Proposal approval gate | 🟡 | Policy in `agent_permissions.md` (founder approves pricing/proposals); executable gate not built |
| 7 | No external-content untrusted policy | ✅ | `company_os/governance/external_content_policy.md` |
| 8 | No Founder Daily Command | ✅ | `reports/founder/DAILY_SUPER_COMMAND.md` (template; live generator pending) |
| 9 | No Launch Score | ✅ | `scripts/checks/check_launch_readiness.py` + `LAUNCH_SCORECARD.md` |
| 10 | No GitHub Actions / checks | ✅ | `.github/workflows/launch-readiness.yml` + checker |

---

## Summary

- **Resolved (✅): 6** — discovery policy, invented-contact prevention, suppression,
  untrusted-content policy, founder command, launch score, CI checks.
- **Policy resolved / executable pending (🟡): 2** — per-system delivery packs (#1),
  mini proposal gate (#6).
- **Open (🔴): 1** — executable Email Quality Gate (#2).

## Impact on launch modes

- **Internal Dry Run:** allowed — no external sending, so #1/#2/#6 do not gate it.
- **Soft / Controlled / Full:** **blocked** until #1, #2, #6 are closed
  *executably* (not just by policy) and the Launch Score reaches the mode's band.

## Why #2 and #10 are emphasized

Cold email without deliverability discipline harms the domain fast: Google
requires SPF/DKIM (and DMARC for larger senders), requires one-click unsubscribe
for bulk marketing mail, and expects senders to keep spam rates low. So real
launch needs **gates before sending**, not just draft generation. AI-assisted
tooling/MCP clients are also a documented prompt-injection / tool-poisoning
surface, and GitHub Actions studies show frequent permission gaps — hence the
CI + least-privilege requirement (#10).

See remediation order in `LAUNCH_SCORECARD.md` and the signed decision in
`GO_NO_GO_DECISION.md`.
