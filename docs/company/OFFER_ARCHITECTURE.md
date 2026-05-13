# Offer Architecture — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OFFER_ARCHITECTURE_AR.md](./OFFER_ARCHITECTURE_AR.md)

## Context
Offer Architecture is the structural blueprint of every commercial
proposition Dealix puts in front of a client. It defines four tiers,
the role each plays in the buyer journey, and the strict rule that
governs progression between them. It is the strategic spine of
`docs/OFFER_LADDER_AND_PRICING.md` and the pilot motion in
`docs/business/MANAGED_PILOT_OFFER.md`, and operates in service of the
capital accumulation defined in
`docs/company/DEALIX_CAPITAL_MODEL.md`.

## The four tiers

### 1. Front-end Offers — small, clear, low-risk entry
- AI Ops Diagnostic
- Revenue Diagnostic
- AI Quick Win Sprint

These offers exist to qualify the buyer, surface real problems, and
produce a proof pack with minimum commitment from either side.

### 2. Core Offers — high-value implementation
- Lead Intelligence Sprint
- Company Brain Sprint
- Workflow Automation Sprint
- AI Support Desk Sprint

These are the main cash engines. They deliver visible business impact
inside a finite window and produce the proof artifacts the
Proof-to-Upsell Map depends on.

### 3. Continuity Offers — recurring
- Monthly RevOps OS
- Monthly AI Ops
- Monthly Support AI
- Monthly Company Brain

These convert proven sprints into ongoing operating systems and
provide the recurring revenue base needed for Academy and Platform
investments.

### 4. Enterprise Offers — custom
- Enterprise AI OS
- AI Governance Program
- Multi-Branch RevOps

These are only sold to clients who have already proven trust through
Front-end or Core offers, and they carry separate pricing, scoping,
and compliance treatment.

## The progression rule

> Entry Offer → Core Sprint → Pilot → Retainer → Enterprise.
> Do not jump to Enterprise before proof.

Skipping tiers — for example, accepting an Enterprise mandate from a
new prospect without an upstream sprint — is forbidden. The rule
exists because Enterprise risk requires evidence of fit, and because
selling Enterprise too early starves the proof-pack pipeline that
sustains all other revenue.

## Why tiering matters

Every tier creates a different kind of capital:

- Front-end → Trust Capital (proof packs)
- Core → Service Capital (refined offers and templates)
- Continuity → Market Capital (audience and references)
- Enterprise → IP Capital (governance, integration, depth)

A balanced portfolio across all four tiers is how the company
compounds.

## Offer-design checklist

For any new offer to enter the architecture, it must:

1. Sit clearly inside one of the four tiers.
2. Have a defined primary KPI in
   `docs/company/SERVICE_KPI_MAP.md`.
3. Have a pricing row in
   `docs/OFFER_LADDER_AND_PRICING.md` with margin in line with
   `docs/UNIT_ECONOMICS_AND_MARGIN.md`.
4. Identify the canonical upsell from
   `docs/growth/PROOF_TO_UPSELL_MAP.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Proposal request | Tier classification | Founder | Per deal |
| New offer proposal | Tier placement decision | Founder | Per offer |
| Quarterly review | Tier rebalancing actions | Founder | Quarterly |
| Sales pipeline | Tier-mix actuals | Founder | Weekly |

## Metrics
- Tier mix — share of revenue from Front-end / Core / Continuity / Enterprise; target Continuity ≥ 30% by year-end.
- Progression rate — share of Front-end clients that progress to Core within 6 months; target ≥ 40%.
- Premature-Enterprise count — number of Enterprise deals accepted without upstream proof; target 0.
- Continuity attach rate — share of Core deliveries that attach a Continuity offer; target ≥ 40%.

## Related
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing layer for the architecture.
- `docs/business/MANAGED_PILOT_OFFER.md` — pilot motion bridging Core to Continuity.
- `docs/COMPANY_SERVICE_LADDER.md` — service catalog mapped to tiers.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model the architecture serves.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
