# Revenue Capability — AI Capability Factory

**Layer:** L4 · AI Capability Factory
**Owner:** Head of Revenue
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [revenue_capability_AR.md](./revenue_capability_AR.md)

## Context

The Revenue capability is the most common entry point into Dealix and
the most directly measurable. It exists to help a client company
identify, prioritize, and act on revenue opportunities. This file is
the operating blueprint that turns a "messy leads" complaint into a
structured, governed revenue workflow. It is anchored to
`docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` and to
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, and it follows the
Constitution rules in `docs/DEALIX_OPERATING_CONSTITUTION.md`.
Maturity is scored using
[docs/company/CAPABILITY_MATURITY_MODEL.md#factory-application](../company/CAPABILITY_MATURITY_MODEL.md#factory-application).

## Business Purpose

Help the company identify, prioritize, and act on revenue
opportunities with measurable lift in pipeline value and conversion.

## Typical Problems

- Messy leads — duplicates, missing fields, inconsistent sources.
- Weak CRM — unused fields, no stage discipline, manual updates.
- Unclear ICP — sales chases everyone.
- No prioritization — every lead treated the same.
- Manual follow-up — drops between WhatsApp, email, and calls.
- Poor pipeline visibility — pipeline value not trustworthy.

## Required Inputs

- Account / lead list (CSV or CRM export).
- Ideal Customer Profile (ICP) definition.
- Current offer and pricing.
- Sales stages and stage definitions.
- Source attribution.
- Previous outcomes if available (won / lost / no-decision).

## AI Functions

- Clean and deduplicate data.
- Score accounts against ICP.
- Segment opportunities by tier and stage.
- Draft outreach copy for human approval.
- Recommend next actions per account.
- Generate revenue report on demand.

## Governance Controls

- No cold WhatsApp; no LinkedIn automation.
- Source required for every claim in outreach.
- Claims review before any external use.
- Human approval gate before any send.
- Logged in `docs/DEALIX_OPERATING_CONSTITUTION.md` audit trail.

## KPIs

- Accounts scored — count and % of total list.
- Qualified accounts — count passing the ICP threshold.
- Data quality improvement — before/after score on completeness, dedup, source.
- Pipeline value — SAR weighted by stage probability.
- Next actions completed — count per week against plan.

## Services

- Revenue Diagnostic — paid assessment of the capability.
- Lead Intelligence Sprint — first capability build.
- Pilot Conversion Sprint — operate the workflow for 30 days.
- Monthly RevOps OS — recurring operating retainer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Lead list + ICP | Cleaned + scored list | Delivery | Per sprint |
| Top accounts | Outreach drafts | Delivery | Weekly |
| Approved drafts | Sent outreach (client owns send) | Client | Weekly |
| Pipeline events | Revenue report + next actions | Delivery | Weekly |

## Metrics

- Accounts scored, qualified accounts (see KPIs above).
- Data quality lift — composite score 0–100.
- Pipeline coverage — pipeline value / target.
- Sprint-to-retainer conversion for revenue clients.

## Related

- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — playbook this capability operationalizes.
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — autonomous revenue OS reference.
- `docs/V7_REVENUE_FACTORY_LAUNCH_BOARD.md` — launch board the capability feeds.
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — maturity anchor (`#factory-application`).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
