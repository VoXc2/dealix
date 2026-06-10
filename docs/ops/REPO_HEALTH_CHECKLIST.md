# Repository Health Checklist

## Purpose
Keep Dealix clean, secure, maintainable, and ready for serious customers or contributors.

## Weekly checks

- [ ] CI passes on main.
- [ ] CodeQL has no unresolved critical findings.
- [ ] OpenSSF Scorecard workflow is running.
- [ ] Dependabot alerts and PRs are reviewed.
- [ ] No stale high-priority issues are ignored.
- [ ] No secrets or customer data are committed.
- [ ] Release readiness checklist is used for production-facing changes.
- [ ] AI workflows have owners and review paths.

## Monthly checks

- [ ] Dependencies reviewed.
- [ ] Tool registry reviewed.
- [ ] CODEOWNERS still matches team reality.
- [ ] SECURITY.md is current.
- [ ] Issue templates still match the operating model.
- [ ] Founder OS artifacts are current.
- [ ] Dashboard metrics still drive decisions.
- [ ] Risk register reviewed.

## Quarterly checks

- [ ] Strategy and moat reviewed.
- [ ] Product roadmap refreshed.
- [ ] AI governance reviewed.
- [ ] Vendor and tool inventory reviewed.
- [ ] Security posture reviewed.
- [ ] Enterprise readiness reviewed.
- [ ] Data room and investor materials refreshed if needed.

## Repo operating rules

- Main branch must stay releasable.
- Every meaningful change needs a clear issue, PR, or decision record.
- Every new external tool needs an owner and review.
- Every AI workflow needs evaluation and fallback.
- Every public claim needs evidence.

## Current automation baseline

- CI workflow
- CodeQL workflow
- OpenSSF Scorecard workflow
- Dependabot config
- Security policy
- Pull request template
- Issue templates
- CODEOWNERS
