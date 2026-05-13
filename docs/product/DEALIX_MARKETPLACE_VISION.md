# Dealix Marketplace Vision — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** CPO + Commercial Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_MARKETPLACE_VISION_AR.md](./DEALIX_MARKETPLACE_VISION_AR.md)

## Context
Once Dealix has accumulated playbooks, workflow templates, agent cards, governance rules, sector packs, and evaluation packs that work in production, the natural next platform is a marketplace — a curated, governed catalogue where Dealix and partners distribute approved AI operating assets to customers. The vision in this file describes the marketplace's scope, the entry standard, and the role it plays in extending the category. It sits next to the competitive view in `docs/COMPETITIVE_POSITIONING.md`, the category narrative in `docs/strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md`, and the strategic direction in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## What the marketplace offers
A curated catalogue of approved AI operating assets:

- **Playbooks** — proven sequences of agents and human steps that solve a specific business problem.
- **Workflow templates** — pre-built, pre-governed workflows for common use cases.
- **Report templates** — Dealix-grade report layouts with provenance baked in.
- **Governance rules** — policy bundles, approval matrices, and runtime checks for specific industries.
- **Agent cards** — registered, validated agents with identity, permissions, and lifecycle metadata.
- **Sector packs** — bundles of playbooks, agents, and rules tailored to a specific industry (financial services, healthcare, government, retail, real estate).
- **Evaluation packs** — eval suites that verify a workflow's quality and governance posture.

## Entry standard — the Dealix Standard
**Only assets that passed the Dealix Standard enter the marketplace.** The Standard is a published, versioned bar that covers:

- Identity and ownership (per `docs/product/AGENT_IDENTITY_OWNERSHIP.md`).
- Autonomy classification (per `docs/governance/AUTONOMY_VALIDATION_GATES.md`).
- Action class declaration (per `docs/governance/AI_ACTION_CONTROL.md`).
- Provenance and audit (per `docs/product/AI_RUN_PROVENANCE.md`).
- Rollback and mitigation (per `docs/governance/REVERSIBILITY_ROLLBACK.md`).
- Eval coverage with passing thresholds.
- Documentation in English and Arabic.
- Pricing and licensing terms compatible with enterprise procurement.

Assets that fail the Standard are returned with a remediation report; nothing reaches a customer without passing the bar.

## Roles in the marketplace
- **Dealix** — operator, curator, certifier; publishes its own first-party assets.
- **Partner firms** — independent agencies, sector specialists, and integrators who publish certified assets and earn revenue share.
- **Customer organizations** — buy and deploy assets into their workspaces, with provenance and governance preserved.

## Category implication
The marketplace is how the Dealix category — "governed AI operating capabilities" — scales beyond what Dealix alone can deliver. It is the lever that turns a services business into a category-defining platform, while keeping the governance bar non-negotiable.

## Sequencing
The marketplace ships after Dealix Cloud's first-party assets are stable, proven, and consumed across multiple customers. Premature opening would dilute the Standard and damage the category.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Asset submissions (internal + partner) | Certified marketplace listings | CPO + Governance | Per submission |
| Customer demand signals | Sector pack roadmap | Commercial + CPO | Quarterly |
| Eval and incident data per asset | Listing updates, suspensions, retirements | Governance | Continuous |

## Metrics
- Standard Pass Rate — % of submissions that pass on first review.
- Active Listings — count of certified, currently published assets.
- Marketplace Revenue Share — % of Dealix revenue routed through marketplace transactions.
- Sector Coverage — count of sectors with at least one certified sector pack.

## Related
- `docs/COMPETITIVE_POSITIONING.md` — competitive context the marketplace lives in
- `docs/strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md` — category narrative
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
