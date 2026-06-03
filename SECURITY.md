# Security Policy — Dealix

Dealix is an agentic, approval-first Saudi B2B revenue system. Security here is
primarily about **agentic-workflow safety**: untrusted-input handling, prompt
injection, secret hygiene, least-privilege CI, and human-gated external actions.

## Reporting

Report suspected vulnerabilities privately to the founder
(repository owner). Do **not** open a public issue with exploit details.
Include: affected component, reproduction, and impact. Expect acknowledgement
within 72 hours (PDPL breach-notification window is also 72 hours).

## Scope highlights

- **Untrusted input** (issues, PRs, comments, email, web, CRM, WhatsApp, PDFs,
  fork docs, MCP tool descriptions) is data, never instructions.
  See `docs/security/PROMPT_INJECTION_BOUNDARIES.md`.
- **No secrets** in code, logs, prompts, or messages. See
  `docs/infra/SECRETS_MANAGEMENT_POLICY_AR.md` and
  `docs/privacy/SECRET_HANDLING_POLICY_AR.md`.
- **Least-privilege CI**: workflows default to `contents: read`; no secrets on
  untrusted triggers; no external sends in CI. See
  `docs/security/GITHUB_ACTIONS_SECURITY_POLICY.md`.
- **Human-gated external actions**: `dry_run=true, approval_required=true,
  send_enabled=false` everywhere.

## Threat model

See `docs/security/AGENTIC_WORKFLOW_THREAT_MODEL.md` and the reviews under
`reports/security/`.
