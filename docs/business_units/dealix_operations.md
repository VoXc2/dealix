# Dealix Operations — Business Unit

**Layer:** Holding · Compound Holding Model
**Owner:** Dealix Operations GM
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [dealix_operations_AR.md](./dealix_operations_AR.md)

## Context
Dealix Operations is the Business Unit that turns manual, error-prone processes into governed, repeatable workflows. It is the BU that **takes the customer's most painful internal SOP and ships an AI-augmented version of it** that is auditable and PDPL-aligned. It sits in the BU layer of [`docs/holding/DEALIX_HOLDING_OS.md`](../holding/DEALIX_HOLDING_OS.md), is paired with `docs/capabilities/operations_capability.md`, and applies the methodology in `docs/standards/DEALIX_METHOD.md`.

## Function
Operations diagnoses where the customer spends repetitive hours, designs a workflow that combines deterministic steps with AI assistance, ships it inside Core OS, instruments quality and approvals, and retains it on a monthly basis.

## Services offered

| Service | Duration | Outcome |
|---|---|---|
| AI Quick Win | 1–2 weeks | Diagnostic + 1 small workflow shipped |
| Workflow Automation | 2–6 weeks | 1–3 governed workflows live |
| Executive Reporting Automation | 2–4 weeks | Scheduled reports with citations and approvals |
| Monthly AI Ops (retainer) | Ongoing | Workflow tuning, new workflows, monthly value report |

## Product modules (in Core OS)

| Module | Function |
|---|---|
| Workflow Builder | Compose workflows from approved steps |
| Approval Flow | Configurable per-workflow approval routing |
| SOP Generator | Turn meeting notes / docs into an SOP draft |
| Ops Dashboard | Throughput, error rate, time saved |

## KPIs

- **Hours saved per workflow per week.**
- **Manual steps reduced** — count of steps replaced or assisted.
- **Workflow completion rate** — % of started workflows reaching done.
- **Error reduction** — defect rate after deployment vs baseline.
- **Workflow adoption** — # users / # licensed users actively running.

## Core OS dependencies

| OS module | How Operations consumes it |
|---|---|
| Data OS | Source registry per workflow input |
| LLM Gateway | AI-assist steps routed through gateway |
| Governance Runtime | Approval flow + audit log per workflow |
| Proof Ledger | Time-saved evidence per project |
| Capital Ledger | Reusable workflow templates and step libraries |
| AI Control Tower | Cost per workflow run, eval scores on AI steps |

## Owner

| Role | Responsibility |
|---|---|
| Operations BU GM | P&L, service ladder, retainer pull-through |
| Operations Delivery Lead | Sprint execution + QA |
| Operations CSM | Adoption + retainer health |
| Workflow Product Owner | Module backlog into Core OS |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client SOPs / process maps | Workflow diagram + scope | Ops Delivery | Per sprint |
| Live workflow runs | Telemetry to Ops Dashboard | Workflow Builder | Daily |
| Time-saved evidence | Proof Pack | Ops GM | Per project |
| Retainer renewal | Monthly AI Ops contract | Ops CSM | Monthly |

## Metrics
- **MRR (Ops BU)** — retainer monthly recurring revenue.
- **Gross margin** — service margin after delivery cost.
- **Time-saved-per-dollar** — hours saved per SAR spent on the retainer.
- **Workflow uptime** — % of run windows the workflow met SLA.
- **Audit coverage** — % of workflow runs with full audit log.

## Related
- `docs/capabilities/operations_capability.md` — capability spec for this BU.
- `docs/COMPANY_SERVICE_LADDER.md` — group service ladder.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing.
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — sell + convert plays.
- `docs/holding/DEALIX_HOLDING_OS.md` — umbrella holding model.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
