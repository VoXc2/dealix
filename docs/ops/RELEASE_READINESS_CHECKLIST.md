# Release Readiness Checklist

## Purpose
Use this before any production-facing release, launch push, or major customer demo.

## Product readiness

- [ ] Critical user journeys work end to end.
- [ ] Acceptance criteria are met.
- [ ] Known bugs are classified by severity.
- [ ] Rollback or fallback path exists.
- [ ] Customer-facing copy is accurate.

## Engineering readiness

- [ ] CI is green.
- [ ] Tests pass.
- [ ] API contract is valid.
- [ ] Database migrations are reviewed.
- [ ] Docker/build surface is verified.
- [ ] Logs and metrics are available.

## Security readiness

- [ ] No secrets committed.
- [ ] Environment variables are documented.
- [ ] Access changes are reviewed.
- [ ] Security-sensitive changes have review.
- [ ] Dependencies are reviewed.

## AI readiness

- [ ] AI workflow is registered.
- [ ] Human review path exists.
- [ ] Evaluation checklist is completed.
- [ ] Fallback path exists.
- [ ] Outputs do not overclaim.

## GTM readiness

- [ ] ICP is clear.
- [ ] Pricing and packaging are current.
- [ ] Proof pack is ready.
- [ ] Sales script is aligned.
- [ ] CRM stages are clean.

## Customer readiness

- [ ] Onboarding flow is ready.
- [ ] Support owner is assigned.
- [ ] Escalation path exists.
- [ ] Customer communication is prepared.

## Final decision

| Gate | Status | Owner | Notes |
|---|---|---|---|
| Product | Pass/Hold | TBD | TBD |
| Engineering | Pass/Hold | TBD | TBD |
| Security | Pass/Hold | TBD | TBD |
| AI | Pass/Hold | TBD | TBD |
| GTM | Pass/Hold | TBD | TBD |
| Customer | Pass/Hold | TBD | TBD |

Final decision: GO / HOLD / FIX FIRST

Decision owner: Founder
