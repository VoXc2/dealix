# Data Readiness Assessment — Upsell — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [upsell_AR.md](./upsell_AR.md)

## Context
A Data Readiness Assessment that does not lead to a clear next step is
revenue left on the table. This file maps each common readiness
finding to the next service in the Dealix ladder. It operates inside
the Capability Operating Model
(`docs/company/CAPABILITY_OPERATING_MODEL.md`) and is the conversion
engine that ties the readiness work to the service ladder in
`docs/COMPANY_SERVICE_LADDER.md` while respecting the data rules in
`docs/DPA_DEALIX_FULL.md` and `docs/DATA_RETENTION_POLICY.md`.

## Mapping: Finding → Recommended Next Service

| Finding | Recommended Next Service | Why |
|---|---|---|
| Strong sales data, weak ranking | Lead Intelligence Sprint | Raises Revenue Capability from L1 to L3. |
| Scattered knowledge, missing citations | Company Brain Sprint | Raises Knowledge Capability from L1 to L3. |
| Repetitive manual operations | AI Quick Win | Raises Operations Capability from L0/L1 to L2. |
| No AI policy, unclear approvals | AI Readiness Review (Governance) | Raises Governance Capability from L0 to L2. |
| Many sources, low completeness | Data Cleanup engagement | Raises Data Capability before any AI Sprint. |
| Manual executive reports | Executive Reporting Sprint | Raises Reporting Capability from L1 to L3. |
| WhatsApp / email reply overload | AI Support Desk Sprint | Raises Customer Capability from L1 to L3. |

## Decision Logic
- Use the readiness composite from `scoring_model.md` to gate the
  recommendation.
- If the composite is below 60, the recommendation is always a Data
  Cleanup or process service first.
- If the composite is 60–79, the recommendation is a light Data
  Cleanup paired with the highest-value AI Sprint from the table above.
- If the composite is ≥ 80, the recommendation is the highest-value
  AI Sprint that addresses the client's strongest business pain.

## Commercials
- Pricing for each recommended service follows
  `docs/OFFER_LADDER_AND_PRICING.md`.
- If the client commits within 30 days, part or all of the assessment
  fee may be credited per the offer ladder rules.
- For repeat clients, the recommendation is stacked into a Pilot or
  Retainer where appropriate.

## Anti-patterns
- **Selling everything at once.** The recommendation is one Sprint,
  not three.
- **Recommending against the score.** A "Ready" score plus an "AI
  Readiness Review" is a misfit and must not be sold.
- **Skipping governance.** When governance risk is High, governance
  must be addressed before or alongside any external-action service.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Readiness report findings | Named recommended service | Founder | Per engagement |
| Commercial terms | Sprint proposal | Founder | Per engagement |
| Won Sprints | Conversion tracking | Founder | Monthly |

## Metrics
- **Recommendation-to-Sprint Conversion** — share of recommendations
  that become a paid Sprint within 30 days (target ≥ 50%).
- **Recommendation Accuracy** — share of recommendations that match
  what the client would have chosen with full information (target ≥
  85%).
- **Cross-Capability Conversion** — share of clients who buy a second
  capability service within 90 days (target ≥ 30%).
- **Average Deal Size Uplift** — SAR uplift per assessment-led deal vs.
  baseline (track, not bound).

## Related
- `docs/DPA_DEALIX_FULL.md` — data rules respected during follow-on
  work.
- `docs/DATA_RETENTION_POLICY.md` — retention rules.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture the next Sprints
  plug into.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
