# GitHub Workflow Security Review — Findings (2026-06-03)

**At audit start:** no `.github/` directory existed — **zero CI**, hence zero
security gates. Nine least-privilege workflows were added.

## Per-workflow review

For every workflow: trigger = `push` + `pull_request` (branches `**`);
permissions = `contents: read`; secrets used = **none**; writes allowed =
**none**; untrusted-input exposure = none (no secrets, no `pull_request_target`);
deployment risk = none; external-send risk = none.

| Workflow | Recommended perms | Actual perms | Verdict |
|----------|-------------------|--------------|---------|
| agentic-security-gate | contents: read | contents: read | ✅ |
| market-agent-security-gate | contents: read | contents: read | ✅ |
| gtm-safety-evals | contents: read | contents: read | ✅ |
| privacy-outbound-review | contents: read | contents: read | ✅ |
| deliverability-review | contents: read | contents: read | ✅ |
| whatsapp-client-os-review | contents: read | contents: read | ✅ |
| proposal-proof-payment-review | contents: read | contents: read | ✅ |
| delivery-handoff-review | contents: read | contents: read | ✅ |
| finance-gtm-review | contents: read | contents: read | ✅ |

## Automated guard results (this run)
- `scripts/check_workflow_security.py` → **OK: 9 workflow(s) pass.**
- `scripts/scan_secrets.py` → **OK: no committed secrets.**
- All 9 YAML files parse; all pin `actions/*@v4`/`@v5`.

## Risky triggers / broad permissions
- None. No `pull_request_target`, no `write-all`, no secrets.

## Recommendations
- Enable GitHub **secret-scanning + push protection** (native) as a second layer.
- Add branch protection on `main` requiring `agentic-security-gate` to pass.
- If a future workflow needs to comment on PRs, give it `pull-requests: write`
  only, with no secrets, and keep it off untrusted triggers.

**Verdict:** CI is least-privilege and self-policing. No workflow can leak
secrets, escalate permissions, send externally, or deploy.
