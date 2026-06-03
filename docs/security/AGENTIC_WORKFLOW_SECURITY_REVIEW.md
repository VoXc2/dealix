# Agentic Workflow Security Review (Policy)

This is the standing checklist applied to every agentic change. The point-in-time
findings live in `reports/security/AGENTIC_WORKFLOW_SECURITY_REVIEW.md`.

## Checklist

- [ ] Untrusted input handled as data (no instruction-following).
- [ ] No secrets in prompts, logs, messages, or tool args.
- [ ] No external send without human approval + `send_enabled`.
- [ ] No final pricing / legal commitment by an agent.
- [ ] Suppression respected; no bypass.
- [ ] No workflow permission escalation; `contents: read` default.
- [ ] No `pull_request_target` agent execution; no `issue_comment` tool-exec with secrets.
- [ ] Tests/evals updated, not weakened; `pytest` green.
- [ ] Output contract fields present (incl. evidence + risk level).
- [ ] Collision policy followed; manual edits preserved.

## Sign-off levels
- **Low risk** (docs/reports): self-check + green tests.
- **Med/High risk** (data/code/outbound): + Security Red Team review + founder approval.
- **Critical** (payment/legal/secrets/deploy): founder approval mandatory; agent cannot proceed.
