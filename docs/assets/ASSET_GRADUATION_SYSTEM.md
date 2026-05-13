# Asset Graduation System — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder / Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ASSET_GRADUATION_SYSTEM_AR.md](./ASSET_GRADUATION_SYSTEM_AR.md)

## Context
Raw client outputs are not yet capital. They become capital only when
they are generalized, standardized, and eventually productized. The
Asset Graduation System defines the five stages an artifact passes
through on its way from one-off deliverable to market-facing IP. It is
the mechanism that turns the Capital Ledger from a list of files into
a pipeline of compounding assets, in line with the strategic
positioning declared in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the architecture
ambitions in `docs/BEAST_LEVEL_ARCHITECTURE.md`.

## The five stages

| Stage | Name | Definition |
|---|---|---|
| 1 | Raw Output | Created for one specific client; not reusable as-is. |
| 2 | Reusable Template | Cleaned, anonymized, generalized for the next similar client. |
| 3 | Standard Asset | Used across 3+ projects; canonical for its category. |
| 4 | Productized Asset | Supported by a tool, script, UI, or API; effort to apply is near-zero. |
| 5 | Market Asset | Used in sales, content, case studies, or benchmark reports; visible outside the company. |

## Worked example

Client report → report template → executive report standard →
`reporting_os/executive_report.py` → sample report on the public
website. This is the canonical illustration of the transformation
**from delivery to IP**. The same path applies to every other asset
class: dashboards, evaluation scripts, lead scoring rules, Arabic QA
checks, governance memos, and so on.

## Promotion criteria

A raw output may be promoted to the next stage only when all of the
following are true:

- **Stage 1 → 2** Cleaned of client identifiers, generalized, reviewed
  by the delivery lead.
- **Stage 2 → 3** Used successfully on three or more projects without
  major rewrite.
- **Stage 3 → 4** A repeatable script, tool, or UI exists; manual
  application time drops by ≥ 60%.
- **Stage 4 → 5** Cleared by legal for external exposure; integrated
  into a sales deck, case study, or public benchmark.

Demotion is allowed: if a Stage-3 asset stops being used for two
quarters, it is demoted to Stage 2 and reviewed.

## Graduation cadence

The founder runs a Graduation Review every quarter. Inputs are the
Capital Ledger and the IP Registry. Outputs are promotion or demotion
decisions, recorded as Change-log rows in
`docs/company/IP_REGISTRY.md`.

## What graduation is not

It is not a vanity exercise. The goal is not to push everything to
Stage 5. Most assets should live happily at Stage 2 or 3. Only assets
with clear repeated demand should consume engineering effort to reach
Stage 4, and only assets that materially shift positioning should
reach Stage 5.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Capital Ledger rows | Promotion / demotion decisions | Founder | Quarterly |
| Reuse statistics | Stage transition events | Delivery lead | Per reuse |
| Engineering capacity | Stage-4 build backlog | Founder | Quarterly |
| Legal review | Stage-5 external clearance | Founder | Per asset |

## Metrics
- Stage-mix — percentage of ledger rows at each stage; target Stage ≥ 3 share ≥ 40% by year-end.
- Time-to-Stage-3 — median quarters from first creation to canonical adoption; target ≤ 2.
- Stage-4 conversion rate — share of Stage-3 assets that become productized within one year; target ≥ 30%.
- Stage-5 portfolio size — number of market-facing assets; target ≥ 6 within 12 months.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — engineering ambitions Stage-4 assets feed into.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic frame that prioritizes graduation.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — governance rules around external (Stage-5) exposure.
- `docs/company/IP_REGISTRY.md` — registry where graduated assets are recorded.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
