# Product Telemetry

> What Dealix measures to know whether the product is working — for the
> customer, for governance, and for the business. Phase-1 captures these as
> spreadsheet rows; Phase-2 surfaces them in the AI Control Tower
> (`AI_CONTROL_TOWER.md`) and the business KPI dashboard
> (`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`).

## Five families of telemetry

Every metric belongs to one of: **Usage**, **Quality**, **Governance**,
**Value**, **Economics**. If a metric doesn't fit, it's noise.

## Usage

| Metric | Why it matters | Source | Cadence |
|--------|----------------|--------|--------:|
| Active clients (30-day) | Are paying customers still active? | Billing + project state | Weekly |
| Active workflows / week | Are services being delivered, not just sold? | Event store | Weekly |
| Reports generated | Customer-facing artefacts shipped | `dealix/reporting/executive_report.py` | Weekly |
| Proof packs published | Auditable evidence created | `dealix/reporting/proof_pack.py` | Weekly |
| Approvals issued | Human-in-loop is actually running | `dealix/trust/approval.py` | Weekly |
| Active agents | Agents that ran a customer workflow this week | `agent_observability` | Weekly |

## Quality

| Metric | Why it matters | Source | Cadence |
|--------|----------------|--------|--------:|
| QA score per service (1–5) | Customer-grade output | Reviewer rubric | Per-delivery |
| Eval pass rate | Agent quality regression | `EVALUATION_REGISTRY.md` runners | Nightly |
| Rework rate (% reopened) | Rework eats margin | Project state machine | Weekly |
| Citation present rate (Company Brain) | Source-grounded answers | Ragas | Nightly |
| Arabic-tone score | Saudi-grade language quality | Human rubric / DeepEval | Per-batch |

## Governance

| Metric | Why it matters | Source | Cadence |
|--------|----------------|--------|--------:|
| Blocked actions | Policy is enforced, not advisory | `dealix/trust/policy.py` | Daily |
| PII flags (with outcome) | PDPL exposure caught early | `dealix/trust/pii_detector.py` | Daily |
| Forbidden-claim blocks | No "نضمن / guarantee" reaching customer | `dealix/trust/forbidden_claims.py` | Daily |
| Approvals overdue | Workflow stalls + customer pain | Approval matrix | Daily |
| Source-missing incidents | Data hygiene risk | Runtime governance check | Weekly |

## Value (delivered to the customer)

| Metric | Why it matters | Source | Cadence |
|--------|----------------|--------|--------:|
| Proof events written | Each one is auditable customer value | event store | Per-delivery |
| Hours saved (est.) | Customer-side ROI for case studies | Customer-confirmed estimate | Per-engagement |
| Opportunities surfaced | Leads / accounts / decisions teed up | RevenueAgent output + customer confirmation | Per-engagement |
| Customer NPS / CSAT | Did they actually like it? | Post-delivery survey | Per-engagement |

## Economics

| Metric | Why it matters | Source | Cadence |
|--------|----------------|--------|--------:|
| Cost per run (SAR) | Margin protection | LLM gateway + `MODEL_PORTFOLIO.md` | Daily |
| Cost per project (SAR) | Did this engagement clear margin? | Aggregated runs + delivery time | Per-engagement |
| Margin per service (%) | Service-level profitability | Pricing − delivered cost | Monthly |
| Cost over budget incidents | Discipline indicator | Gateway alerts | Weekly |

## Phase-2 wiring

- All five families flow into the AI Control Tower under `frontend/`.
- The event store
  (`auto_client_acquisition/revenue_memory/event_store.py`) is the source
  of truth for Usage, Value, and Governance.
- LiteLLM + Langfuse provide Economics and Quality telemetry.
- The Business KPI dashboard (`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`)
  consumes the same feed for revenue-side metrics.

## Hard rules

- No new service ships without its rows in this telemetry doc.
- A metric without a source path and a named owner is dropped.
- Customer-facing value metrics are always corroborated by a Proof event,
  never by an AI estimate alone.

## Cross-links

- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/product/SERVICE_RUNTIME_TABLE.md`
- `/home/user/dealix/docs/BUSINESS_KPI_DASHBOARD_SPEC.md`
- `/home/user/dealix/dealix/reporting/executive_report.py`
- `/home/user/dealix/dealix/reporting/proof_pack.py`
- `/home/user/dealix/auto_client_acquisition/revenue_memory/event_store.py`
- `/home/user/dealix/auto_client_acquisition/agent_observability/`
