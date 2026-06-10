# Company OS PR Rollup Index

## Purpose
This file exists to make the Company OS expansion reviewable as a Pull Request.

The main Company OS files were already committed directly to `main`. This PR adds a review index that points reviewers to the operating layers now available in the repository.

## Related programs

- Founder Launch OS: issue #472
- Future OS: issue #503
- Company OS expansion: issue #514

## Company OS files

- `docs/company-os/README.md`
- `docs/company-os/01-company-command-center.md`
- `docs/company-os/02-gtm-sales-system.md`
- `docs/company-os/03-customer-success-system.md`
- `docs/company-os/04-data-governance-system.md`
- `docs/company-os/05-security-incident-system.md`
- `docs/company-os/06-risk-decision-system.md`
- `docs/company-os/07-enterprise-readiness-system.md`
- `docs/company-os/08-kpi-dashboard-system.md`
- `docs/company-os/09-weekly-business-review.md`
- `docs/company-os/10-operating-calendar.md`

## Supporting operating docs

- `docs/ops/FOUNDER_DAILY_RUNBOOK.md`
- `docs/ops/RELEASE_READINESS_CHECKLIST.md`
- `docs/ops/VENDOR_AND_TOOL_ADOPTION_POLICY.md`
- `docs/ops/EXECUTIVE_DASHBOARD_SPEC.md`
- `docs/ops/REPO_HEALTH_CHECKLIST.md`

## AI and automation docs

- `docs/ai-tools/AI_TOOL_REGISTRY.md`
- `docs/ai-tools/AI_EVALUATION_CHECKLIST.md`
- `docs/ai-tools/AI_AND_AUTOMATION_TOOLING_BACKLOG.md`

## GitHub governance additions

- `CODEOWNERS`
- `.github/ISSUE_TEMPLATE/founder_task.yml`
- `.github/ISSUE_TEMPLATE/ai_risk_review.yml`
- `.github/ISSUE_TEMPLATE/deal_review.yml`
- `.github/ISSUE_TEMPLATE/security_review.yml`

## Review checklist

- [ ] Company OS structure is clear.
- [ ] Each file is usable as an operating artifact.
- [ ] No unlicensed external content is copied blindly.
- [ ] AI and vendor adoption are gated by review.
- [ ] Founder, GTM, CS, data, risk, incident, and KPI systems are covered.

## Next recommended PRs

1. Convert dashboard specs into implementation issues.
2. Add tests or scripts that verify required Company OS files exist.
3. Add automated docs index generation.
4. Add issue links from each operating file to its owning execution issue.
