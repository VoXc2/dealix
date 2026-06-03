# GitHub Actions Security Policy — Dealix

Principles: **least privilege, no secrets on untrusted triggers, no external
sends in CI, no production deploy from an agent branch, dry-run only.**

## Mandatory rules

1. **Default token = `permissions: contents: read`.** Add a narrower scope
   (e.g. `pull-requests: write`) only when a job must comment, and only when
   that job uses **no secrets**.
2. **No `pull_request_target`.** It runs with repo secrets in the context of an
   untrusted PR — banned.
3. **No `issue_comment` / `issues` jobs that execute agent tools with secrets or
   write access.**
4. **No `${{ secrets.* }}` on untrusted triggers** (`pull_request`, `issues`,
   `issue_comment`).
5. **No external sends in CI** (no email/WhatsApp/HTTP-POST to third parties).
6. **No production deploy from a feature/agent branch.** No prod secrets in CI.
7. **Pin actions** to a major version (`@v4`) from trusted publishers.
8. **Fail closed on safety violations** (the gate exits non-zero).

## Enforcement (self-checking)

`scripts/check_workflow_security.py` runs in `agentic-security-gate.yml` and
fails the build on: `pull_request_target`, `permissions: write-all`, secrets on
untrusted triggers, or write-perms combined with secrets.
`scripts/scan_secrets.py` blocks committed `.env`/private keys.

## Workflow inventory (all `contents: read`, no secrets)

| Workflow | Purpose |
|----------|---------|
| `agentic-security-gate.yml` | Master gate: workflow check, secret scan, pytest, governance, docs-drift |
| `market-agent-security-gate.yml` | Agent permission matrix tests |
| `gtm-safety-evals.yml` | GTM claims/personalization/outreach + eval runner |
| `privacy-outbound-review.yml` | Suppression + schema validation + privacy docs presence |
| `deliverability-review.yml` | Outreach safety + deliverability docs presence |
| `whatsapp-client-os-review.yml` | WhatsApp + reply routing |
| `proposal-proof-payment-review.yml` | Commercial gates |
| `delivery-handoff-review.yml` | Delivery/CS/renewal gates |
| `finance-gtm-review.yml` | Claim-free outbound content + finance docs |
