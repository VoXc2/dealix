# Do Not Sell Yet — Explicit Blocklist

> This is the list of things Dealix will NOT sell today, with the reason
> and the gate that would unlock each. Sales must memorize this list. CRO
> sign-off required on any exception.

## Services blocked from sale

| Item | Why blocked | Gate that unlocks |
|------|-------------|-------------------|
| **AI Support Desk Sprint** | No demo, no consolidated `customer_os/` module yet | Build customer_os + working demo (Phase 2) |
| **Workflow Automation Sprint** | Operations OS lacks workflow_builder / SOP builder | Phase 2 |
| **Executive Reporting Automation** | No standalone product surface; only via Reporting OS internals | Phase 2 |
| **AI Governance Program** | No operational governance dashboard yet | Phase 3 |
| **Monthly RevOps OS retainer** *(as first sale)* | Retainer Decision requires a successful Sprint first | Sprint completes + Proof Pack |
| **Monthly AI Ops retainer** *(as first sale)* | Same as above | Sprint completes |
| **Enterprise AI OS** | Enterprise Decision gate not met (no 10 Sprints + 3 retainers) | `docs/enterprise/ENTERPRISE_DECISION.md` gates |
| **SaaS subscription (pure)** | Service-assisted SaaS path is correct for Year-1; pure SaaS is Year-3+ | After 15+ retainers |

## Features blocked from build

| Feature | Why blocked | Gate that unlocks |
|---------|-------------|-------------------|
| **WhatsApp Business API auto-send** | High compliance / spam risk; consent infrastructure not mature | Mature consent registry + WhatsApp Business approval + Head of CS approval |
| **LinkedIn automation** | Permanent ban — violates LinkedIn ToS and Decision Rule 3 | Never |
| **Web scraping (general-purpose)** | Permanent ban — Decision Rule 3 | Never |
| **Autonomous external outreach (no human approval)** | Permanent ban — Standard 3 (Human Approved) | Never |
| **Multi-tenant RBAC** | Premature without enterprise customer | First enterprise opportunity + ADR 0003 implementation |
| **Pure SaaS workspace (self-serve)** | Year-3+ — services teach us what to productize | After Year 2 maturity |

## Actions blocked at the trust layer

Permanently enforced by `dealix/trust/forbidden_claims.py` + `dealix/trust/approval_matrix.py`:

- Cold WhatsApp / SMS to non-consenting recipients.
- Guaranteed-outcome language ("نضمن", "100%", "best in", "risk-free").
- Fake testimonials or fabricated case studies.
- PII in logs.
- External-API writes without per-action approval.
- "Free trial" of any service without scope.

## Exception process

For each entry above:
1. Sales captures the request in writing.
2. CRO reviews against the gate.
3. If the gate is not met, CRO offers an alternative from the Sellable services.
4. Exceptions require CEO + CRO co-sign and a written 30-day plan to close the underlying gate.

## Why this list exists

Saying "yes" to the wrong customer / feature / service is the most expensive mistake a company at Dealix's stage can make. This list protects:
- Reputation (one bad delivery from a not-ready service can take 6 months to recover).
- Margins (custom enterprise without readiness has -30% margin).
- Compliance (one PII or PDPL violation can end the company).
- Focus (every "yes" to a not-ready item is a "no" to a Sellable one).

## Owner & cadence
- **Owner**: CRO + CEO.
- **Refresh**: monthly; whenever a gate opens, the item moves to Sellable in `SERVICE_REGISTRY.md`.

## Cross-links
- `docs/company/SERVICE_REGISTRY.md`
- `docs/company/SERVICE_READINESS_MATRIX.md`
- `docs/company/SELLABILITY_POLICY.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/enterprise/ENTERPRISE_DECISION.md`
