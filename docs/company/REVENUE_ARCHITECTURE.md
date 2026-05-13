# Revenue Architecture — Capital Model

**Layer:** L1 · Capital Model
**Owner:** Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [REVENUE_ARCHITECTURE_AR.md](./REVENUE_ARCHITECTURE_AR.md)

## Context
Revenue Architecture defines the seven channels through which Dealix
generates revenue and the strategic role each channel plays. It
operationalizes the revenue strategy described in
`docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and aligns with the launch
priorities in `docs/V7_REVENUE_FACTORY_LAUNCH_BOARD.md`. Every pricing
and packaging decision in `docs/revenue/PRICING_AND_PACKAGING.md`
inherits from this file.

## The seven revenue channels

1. **Diagnostics** — Low-risk entry; builds trust and exposes the
   real problem. Typically a one to two week paid scoping.
2. **Sprints** — The main cash engine. Time-boxed implementations with
   defined KPIs and proof packs.
3. **Pilots** — Operational proof. A short managed run of a system in
   a real environment, sized to validate that it works at the client's
   scale.
4. **Retainers** — Recurring revenue. Monthly operating systems that
   continue value delivery after a sprint or pilot.
5. **Enterprise** — High-value custom implementation. Sold only after
   trust is proven through smaller engagements.
6. **Academy** — Training and certification. Converts the Dealix
   Method into a product that scales without consuming delivery
   capacity.
7. **Platform** — SaaS workspace and usage-based modules. The long-term
   leverage layer once enough sprints have hardened into reusable
   software.

## Strategic role of each channel

| Goal | Channel |
|---|---|
| Cash now | Sprints |
| Stability | Retainers |
| Scale | Platform |
| Authority | Academy |
| Large deals | Enterprise |
| Trust entry | Diagnostics |
| Operational proof | Pilots |

The architecture is intentionally over-provisioned: not all channels
are active in every quarter. The point is that no important goal is
missing a channel.

## Activation sequencing

- **Year 1 focus** Sprints + Diagnostics + Retainers.
- **Year 2 expansion** Pilots + Enterprise (after proof base is solid).
- **Year 2–3** Academy launch once 10+ projects, 3+ case studies, and
  a stable method exist.
- **Year 3+** Platform path begins only when the conditions in
  `docs/product/PLATFORM_PATH.md` are satisfied.

## Channel concentration risk

If any single channel exceeds 70% of revenue for two consecutive
quarters, the team triggers a diversification review. Over-reliance on
any one channel — especially Enterprise — exposes the company to
contractual shock.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Pipeline forecast | Channel mix forecast | Founder | Weekly |
| Closed-won data | Channel mix actuals | Founder | Monthly |
| Strategic plan | Channel activation decisions | Founder | Quarterly |
| Capacity model | Channel capacity limits | Founder | Quarterly |

## Metrics
- Channel-mix concentration — share of revenue from largest channel; target ≤ 60%.
- Recurring share — share of revenue from Retainers + Platform; target ≥ 35% by end of year 2.
- Pilot conversion — share of pilots converting to retainer; target ≥ 60%.
- Academy revenue ramp — quarter-over-quarter growth once launched; target ≥ 25%.

## Related
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue motion this architecture sits on top of.
- `docs/V7_REVENUE_FACTORY_LAUNCH_BOARD.md` — launch board for the channels.
- `docs/revenue/PRICING_AND_PACKAGING.md` — pricing and packaging that inherit from this architecture.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model the architecture funds.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
