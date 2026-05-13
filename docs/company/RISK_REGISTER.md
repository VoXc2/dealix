# Risk Register — Standing Risks and Controls

**Layer:** L7 · Execution Engine
**Owner:** Founder / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [RISK_REGISTER_AR.md](./RISK_REGISTER_AR.md)

## Context
This is the standing risk register for Dealix as a founder-led AI
operations company in MENA. Each entry names a recurring failure mode,
its business impact, and the control that contains it. The register is
the operational complement to the incident runbook in
`docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` and the constitution
in `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Standing Risks

| Risk | Impact | Control |
|---|---|---|
| Overbuilding | Burns time and capital without revenue. | Build after 3 repetitions of the same client request. |
| Weak sales | No revenue; runway compression. | Focus on one ICP; weekly Sales Loop minimums. |
| Scope creep | Low margin; founder burnout. | Strict SOW + written change request. |
| Poor data | Bad output; client blames AI. | Data readiness gate before AI implementation. |
| Compliance issue | Trust damage; legal exposure. | Governance OS; PDPL gate. |
| Low-quality Arabic | Weak buyer trust; regional credibility loss. | Arabic QA guide; native review on every Arabic artifact. |
| No proof | No upsell; no case study fuel. | Proof pack mandatory per delivery. |
| Founder bottleneck | No scale; quality regress. | `delivery_os` + hiring triggers (`docs/HIRING_CSM_FIRST.md`). |
| AI cost | Margin loss; pricing pressure. | LLM gateway + cost guard; routing strategy. |

## Risk Tiers

| Tier | Definition | Review cadence |
|---|---|---|
| Standing | In this file; recurring across the company. | Quarterly |
| Engagement | Specific to a single SOW. | Per sprint |
| Incident | Realized; tracked in incident runbook. | As triggered |

## Risk Lifecycle

```
Identify ─► Classify ─► Add control ─► Monitor ─► Review
                                          │
                                          ▼
                                       Incident (if realized)
```

A risk is not closed when its control exists — only when the control
has run for one full quarter without a breach. Until then it remains
*Open with mitigation*.

## Control Ownership

Every control above maps to a named asset:

| Risk | Control asset |
|---|---|
| Overbuilding | Capability backlog gate (Phase 4 of roadmap). |
| Weak sales | `docs/sales/ONE_PAGER.md`, weekly loops. |
| Scope creep | SOW template; change-request form. |
| Poor data | `data_os.data_quality_score`. |
| Compliance | `governance_os.policy_check`. |
| Arabic quality | Arabic QA checklist. |
| No proof | `reporting_os.proof_pack`. |
| Founder bottleneck | `delivery_os` runbook. |
| AI cost | `docs/COST_OPTIMIZATION.md`, LLM gateway. |

## Adding a New Risk

A new entry needs:
- Plain-language name.
- One-sentence impact.
- A named control or a draft control plus owner.
- A monitoring metric.

Risks without a control or monitoring metric are not allowed in this
file — they live in the incident runbook as open items until they
mature.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement observations, incidents | New risk entries | Founder | As surfaced |
| Risk + control | Monitoring metric | Founder | Quarterly |
| Realized risk | Incident entry | Founder | As triggered |

## Metrics
- Open risks with mitigation — count.
- Risk-to-incident conversion — % of risks that became incidents.
- Control coverage — % of risks with a named control.
- Quarterly review completion — boolean.

## Related
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — incident runbook that catches realized risks.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitution this register operates inside.
- `docs/COST_OPTIMIZATION.md` — AI cost control referenced by the AI cost risk.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
