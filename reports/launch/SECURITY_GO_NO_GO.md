# Security Go / No-Go

Security & privacy gate. Must pass before any launch mode above Internal Dry Run.
Because Dealix uses agents and Claude Code (read/write tooling), this gate is
foundational, not optional.

**Date:** 2026-06-03 · **Decision: PASS (for Internal Dry Run); required again before Soft Launch.**

---

## Required proofs

| # | Requirement | Status | Evidence |
|---|-------------|:------:|----------|
| 1 | External content = untrusted data | ✅ | `company_os/governance/external_content_policy.md` |
| 2 | No secrets in prompts / logs / reports | ✅ | Policy + `.gitignore` excludes `.env*`; no secrets committed |
| 3 | No external sending by agents | ✅ | `agent_permissions.md` red lines (send = human only) |
| 4 | No tool execution based on external content | ✅ | `external_content_policy.md` rule #5 |
| 5 | GitHub Actions least-privilege permissions | ✅ | `launch-readiness.yml` → `permissions: contents: read` |
| 6 | Each workflow uses `contents: read` unless write needed | ✅ | Only one workflow; read-only |
| 7 | No secrets appear in logs | ✅ | Workflow installs/builds/checks only; prints no secrets |

---

## Why this gate matters at launch

- **Prompt injection / tool poisoning:** AI-assisted development tools and MCP
  clients can be steered by malicious external content into calling unauthorized
  tools or leaking data via hidden parameters. Mitigation: treat all external
  content as data, never instructions; never execute tools because external text
  said so.
- **GitHub Actions permissions:** studies of Actions usage show frequent gaps in
  permission scoping. Mitigation: default `contents: read`, escalate only where a
  job genuinely needs write.

## Privacy (PDPL / SDAIA)

- `company_os/governance/pdpl_checklist.md` — lawful basis, purpose limitation,
  data minimization, 90-day retention, breach process, data-subject rights.
- `company_os/governance/data_handling_checklist.md` — no PII in public AI tools,
  anonymize before analysis, secure transfer.
- `company_os/governance/suppression_policy.md` — do-not-contact + unsubscribe
  honored within 24h.

## Runnable check

```bash
python scripts/governance_check.py   # founder snapshot of governance posture
```

> Note: this script exits non-zero whenever items are **awaiting approval** (e.g.
> a pending pricing offer or an unapproved draft). During a dry run that is the
> expected, healthy state — it means "approvals pending," not "security broken."
> It is therefore run as an **informational, non-blocking** step in CI; the hard
> gate is `scripts/checks/check_launch_readiness.py`.

## Decision

- **Internal Dry Run:** ✅ PASS — no external sending, policies enforced.
- **Soft Launch and above:** re-run this gate AND add deliverability controls
  (SPF/DKIM/DMARC + one-click unsubscribe + spam-rate monitoring) before enabling
  any manual sending.

- Approved by: ____________________  (Founder)
- Date: ____________________
