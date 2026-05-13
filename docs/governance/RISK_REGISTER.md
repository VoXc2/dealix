# Dealix Operational Risk Register

> Distinct from `docs/legal/enterprise_risk_register.md` (which tracks
> contractual/legal risks for enterprise procurement). This register tracks
> **operational** risks across delivery, governance, AI quality, and growth.

Refresh: monthly. Owner: CEO. Each risk has a control, an owner, and a status.

## Risk Heat Map (current)

| Risk | Severity | Likelihood | Services affected | Control | Owner | Status |
|------|:--------:|:----------:|-------------------|---------|-------|:------:|
| PII leak in deliverable | High | Medium | All | `dealix/trust/pii_detector.py` + Compliance QA gate | HoLegal | Active |
| Unsupported / exaggerated claims in outreach | Medium | Medium | Revenue, Marketing | `dealix/trust/forbidden_claims.py` + AI QA gate | CRO | Active |
| Poor data quality blocks project | High | High | All | Data Readiness Gate (W4.T25 + `data_quality_score.py`) | HoData | Active |
| Scope creep | Medium | High | All | `docs/delivery/SCOPE_CONTROL.md` + `CHANGE_REQUEST_PROCESS.md` | HoCS | Active |
| Hallucinated answers in Company Brain | High | Medium | Company Brain | "no source = no answer" rule + eval framework | CTO | Active |
| Unsafe outbound (cold WhatsApp / LinkedIn auto) | High | Medium | Revenue, Customer | Approval Matrix + Forbidden Actions | HoLegal | Active |
| Customer with no decision-maker | Medium | High | Sales | Qualification Score (`docs/sales/QUALIFICATION_SCORE.md`) | CRO | Active |
| Quality drops as customer count rises | High | Medium | All | 5-gate QA + 80 floor non-negotiable | HoCS | Active |
| Engineering builds speculative features | Medium | Medium | Product | Decision Rule 5 + Feature Prioritization Score | CTO | Active |
| Demos go stale (>90 days, talking about old features) | Low | High | Sales | Freshness review monthly | HoP | Active |
| Branch divergence (engineering vs strategy docs) | Medium | Medium | Engineering | Open PR from strategy branch + separate engineering branch off main | CTO | Active |
| AI cost runaway per project | Medium | Medium | All AI-backed services | LLM Gateway cost guard (Phase 2) + FinOps governance (W4.T24) | CTO | Active |
| Founder bottleneck | High | High | All | Compounding System + Definition of Done + Stage Machine | CEO | Active |
| Sprint→Retainer conversion below target | Medium | Medium | Growth | Stage 8 Expand mandatory + Renewal Recommender | CRO | Active |
| Customer dissatisfaction discovered too late | Medium | Low | All | Mid-sprint check-in + Daily Delivery Command refresh | HoCS | Active |
| Reputation hit from bad early case | High | Low | All | Quality Score 85+ target + careful first-customer selection | CEO | Active |

## Severity scale
- **High**: PR-stopping, customer-trust-destroying, or PDPL-violating.
- **Medium**: degrades quality, slows delivery, requires rework.
- **Low**: cosmetic or schedule-only.

## Likelihood scale
- **High**: ≥ 1 in 2 projects.
- **Medium**: 1 in 5.
- **Low**: rare.

## Status values
- **Active** — control in place and operating.
- **Watch** — control partial; monitor closely.
- **Open** — no control yet; build one in next 30 days.
- **Closed** — risk no longer applies.

## Review process

- **Monthly**: CEO walks the register, marks any change in likelihood or severity, captures new risks.
- **Quarterly**: HoLegal + CTO review controls — are they actually firing? Are they being bypassed?
- **Yearly**: full re-baseline.

## How a new risk gets added

1. Observed in a Red Team scenario, a project, or an audit.
2. Documented with severity / likelihood / affected services.
3. Control proposed.
4. Owner assigned (and accepts).
5. Added to register in the next monthly review.

## Cross-links

- `docs/legal/enterprise_risk_register.md` — contractual/legal risks (different scope)
- `docs/governance/FORBIDDEN_ACTIONS.md` — what we never do
- `docs/governance/APPROVAL_MATRIX.md` — who approves what
- `docs/quality/RED_TEAM_SCENARIOS.md` — how we self-test controls
- `docs/finops/model_cost_governance.md` (W4.T24) — AI cost risk
