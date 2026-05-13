# Dealix IP Registry — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [IP_REGISTRY_AR.md](./IP_REGISTRY_AR.md)

## Context
The IP Registry is the canonical list of Dealix intellectual property:
methodologies, templates, playbooks, datasets, benchmarks, software
modules, standards, and training materials. It is the consolidated
view that turns the Capital Ledger and the Asset Graduation System
into a single defensible asset table — the one used in investor
conversations, partner negotiations, and the competitive positioning
referenced by `docs/COMPETITIVE_POSITIONING.md` and the strategic
narrative in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Schema

| Column | Description |
|---|---|
| IP Asset | Canonical name |
| Type | Methodology / Template / Playbook / Dataset / Benchmark / Software Module / Standard / Training Material |
| Description | One-line definition |
| Used In | Services, products, or content where the asset appears |
| Status | Core / Building / Sunset |

## Initial registry

| IP Asset | Type | Description | Used In | Status |
|---|---|---|---|---|
| Dealix Method | Methodology | Diagnose → Design → Build → Validate → Deliver → Prove → Expand | All services | Core |
| Proof Pack Template | Template | Standard proof of delivery and impact | All services | Core |
| Arabic QA Guide | Standard | Arabic business writing quality | Reports / drafts | Core |
| Saudi B2B Playbook | Playbook | Sector-specific revenue ops | Sales / Revenue | Building |
| Governance Matrix | Policy | Risk and approval rules | All services | Core |

These five rows are the anchor IP. Every additional asset is added as
it reaches Stage 3 in `docs/assets/ASSET_GRADUATION_SYSTEM.md`.

## IP types — full taxonomy

- **Methodology** — End-to-end process (e.g., Dealix Method).
- **Template** — A reusable document or report skeleton.
- **Playbook** — A step-by-step operational guide for a sector or motion.
- **Dataset** — Curated data Dealix owns rights to use and reference.
- **Benchmark** — Quantitative reference (e.g., support-reply baselines).
- **Software Module** — Code packaged for repeated internal or client use.
- **Standard** — A quality rule the company applies consistently.
- **Training Material** — Course content or certification curriculum.

## Add / promote / sunset rules

- **Add** when an asset reaches Stage 3 in the Graduation System.
- **Promote to Core** when used in 3+ services and validated by client
  delivery feedback.
- **Sunset** when an asset has not been used for two consecutive
  quarters or a superior replacement reaches Core status.

All changes are recorded in this file's Change log and mirrored in the
Notion canonical registry.

## Defensibility lens

Each row is reviewed annually against four questions:

1. Is the asset unique to Dealix or commodity?
2. Can a competitor reproduce it in under one quarter?
3. Does it materially affect win-rate or delivery cost?
4. Does it carry Arabic-first quality, governance, or KSA-specific
   value that imports cannot match?

Assets failing all four questions are candidates for sunset.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Graduation decisions | New registry rows | Founder | Quarterly |
| Reuse stats from ledger | Status updates | Founder | Quarterly |
| Annual defensibility review | Promote / sunset list | Founder | Annual |
| Sales and content needs | Stage-5 candidate list | Founder | Quarterly |

## Metrics
- Core asset count — number of rows at Core status; target ≥ 10 within 12 months.
- Building → Core conversion rate — share of Building rows promoted within four quarters; target ≥ 50%.
- Defensibility score — share of rows passing ≥ 2 of the four defensibility questions; target ≥ 80%.
- Sunset rate — rows sunset per year; target ≤ 15% of total.

## Related
- `docs/COMPETITIVE_POSITIONING.md` — uses IP Registry to articulate moat.
- `docs/BRAND_PRESS_KIT.md` — pulls Stage-5 IP into external collateral.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan that depends on IP buildup.
- `docs/assets/ASSET_GRADUATION_SYSTEM.md` — feeder pipeline for the registry.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
