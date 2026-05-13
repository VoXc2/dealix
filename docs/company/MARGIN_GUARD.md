# Margin Guard — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CFO / CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [MARGIN_GUARD_AR.md](./MARGIN_GUARD_AR.md)

## Context

Margin is the only renewable resource Dealix has. Underpricing,
hidden integration work, scope creep, and unlimited revisions destroy
margin faster than missing a sales target. Margin Guard is the daily
guardrail that prevents margin erosion at proposal, kickoff, and
delivery. It operationalizes the unit economics in
`docs/UNIT_ECONOMICS_AND_MARGIN.md`, feeds
`docs/FINANCE_DASHBOARD.md`, and is the last gate before pricing
goes to a client per `docs/company/PRICING_ENGINE.md`.

## Target Gross Margins

| Track | Minimum gross margin | Healthy band |
|---|---:|---:|
| Sprint (fixed-fee, 2-6 weeks) | **70%** | 70-85% |
| Retainer (monthly cadence) | **65%** | 65-80% |
| Enterprise (custom, governed scale) | **50%** | 50-70% |

Below the minimum, the engagement cannot be signed without CEO
written override and a Strategic Discount entry per Pricing Engine
(`docs/company/PRICING_ENGINE.md`).

## Cost Components To Track

Every engagement opens a cost record with the following lines:

- **Founder hours** — at internal opportunity cost rate (default
  SAR 1,200/hr until updated).
- **Contractor / team hours** — direct cost + 20% overhead.
- **AI cost** — gateway-tracked model spend
  (`docs/AI_MODEL_ROUTING_STRATEGY.md`).
- **Tools cost** — pro-rated subscriptions used in the engagement.
- **Revision cost** — hours spent on re-work beyond two free revisions.
- **Delay cost** — opportunity cost of slipping a sprint into the
  next month.
- **Governance cost** — legal/compliance review time.

Engagement margin = Price − Sum(cost components).

## Red Flags

The following situations are explicit margin killers. Any one of
them is a stop-the-line signal.

- **Unlimited revisions** in the SOW. Cap at two; further revisions
  billed at standard rate.
- **Unclear data source** — likely 20-50% time burn on cleaning.
- **Too many stakeholders** (4+ approvers) without a single
  decision-maker — slow approvals burn the timeline.
- **Hidden integration** — "by the way, you'll connect to our old
  Oracle…" — re-price or reject.
- **Custom work inside a fixed sprint** — the sprint is a product,
  not a custom build. Custom must be priced separately.
- **AI cost not modeled** — runaway model usage on long contexts;
  cap and route per `docs/AI_MODEL_ROUTING_STRATEGY.md`.
- **Free pilots** — only with strategic asset commitment per
  Pricing Engine discount rule.
- **Founder-only delivery** — no team coverage, no margin scaling.

## Workflow

1. **Proposal stage** — Sales fills the cost projection. CFO
   verifies projected margin ≥ track minimum. If not, premium rises,
   scope reduces, or proposal stops.
2. **Kickoff stage** — actual hours and AI spend logged from day 1.
   Weekly burn vs. budget review.
3. **Mid-engagement** — at 50% milestone, projected margin updated.
   If projection drops below floor, COO triggers scope conversation.
4. **Close-out** — actual margin entered into Finance Dashboard.
   Variance analyzed in retro.

## Margin Recovery Levers

When an engagement is bleeding margin:

- Move tasks to the lowest-cost capable model
  (`docs/AI_MODEL_ROUTING_STRATEGY.md`).
- Shift contractor work to template-based execution.
- Cut to bounded scope; document the rest as Phase 2.
- Invoice approved revision overages.
- Activate cost optimization actions in
  `docs/COST_OPTIMIZATION.md`.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Cost record, hours log, AI gateway spend | Projected and actual margin | CFO + Delivery Lead | Daily (during engagement) |
| Pricing Engine output | Margin projection at proposal | CFO + CEO | Per project |
| Retro notes | Trend analysis | CFO | Quarterly |

## Metrics

- **Sprint margin (actual)** — target ≥70%.
- **Retainer margin (actual)** — target ≥65%.
- **Enterprise margin (actual)** — target ≥50%.
- **% projects breaching floor** — target ≤5%.
- **Median variance (projected vs actual)** — target ±5%.

## Related

- `docs/UNIT_ECONOMICS_AND_MARGIN.md` — unit economics base.
- `docs/FINANCE_DASHBOARD.md` — live margin dashboard.
- `docs/COST_OPTIMIZATION.md` — recovery levers.
- `docs/V7_COST_CONTROL_POLICY.md` — cost control policy sibling.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — AI cost levers.
- `docs/company/PRICING_ENGINE.md` — upstream pricing.
- `docs/company/MARGIN_CONTROL.md` — finer-grain margin sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
