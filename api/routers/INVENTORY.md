# API Routers — Inventory

**Generated:** 2026-05-12. **Count:** 113 router modules (excluding `__init__.py`).

The repository has accumulated routers across multiple "waves" of development.
This inventory classifies every router so contributors can answer two
questions fast:

1. *Should I be using this in 2026?* → check the **Status** column.
2. *What does it actually do?* → check the **Surface** column for the URL prefix.

Statuses:

- `active-core` — part of one of the Top-3 customer-facing workflows (see
  [`docs/product/CORE_WORKFLOWS.md`](../../docs/product/CORE_WORKFLOWS.md)).
- `active-supporting` — supports core workflows or platform health.
- `active-internal` — founder/ops/admin surface, not customer-facing.
- `beta` — shipped, used by ≤2 internal callers, not promised to customers.
- `versioned-legacy` — a `_v3 / _v6 / _v7 / _v10 / _v11` slice retained for
  backwards compatibility; freeze; do not extend.
- `archive-candidate` — no inbound imports detected; review for removal.

> Conservative classification: when in doubt, a router is marked `beta` not
> `archive-candidate`. Removal requires a follow-up audit confirming no
> external API consumers and one minor-version deprecation cycle.

---

## Quick stats

| Status | Count | Note |
| --- | --- | --- |
| active-core | 6 | The customer-facing spine. |
| active-supporting | ~30 | Sales, customer ops, agents, integrations. |
| active-internal | ~30 | Founder / admin / observability. |
| beta | ~15 | New features under iteration. |
| versioned-legacy | ~25 | `*_v3`, `*_v6`, `*_v7`, `*_v10`, `*_v11`. |
| archive-candidate | TBD | Founder review pending. |

Exact mapping below.

---

## active-core (Top-3 workflows)

| Router | URL prefix | Surface |
| --- | --- | --- |
| `public.py` | `/api/v1/public/*` | Landing entry, demo request, partner application. |
| `leads.py` | `/api/v1/leads/*` | Lead intake + lifecycle. |
| `sales.py` | `/api/v1/sales/*` | Pipeline, opportunities, outreach kickoff. |
| `pricing.py` | `/api/v1/pricing/*` | Plans, quotes, checkout link generation. |
| `customer_success.py` | `/api/v1/customer-success/*` | Onboarding, health, renewal. |
| `webhooks.py` | `/api/v1/webhooks/*` | Inbound HMAC-verified events. |

## active-supporting

`auth.py`, `agents.py`, `agent_governance.py`, `agent_observability.py`,
`approval_center.py`, `automation.py`, `business.py`,
`business_metrics_board.py`, `command_bus.py`, `command_center.py`,
`customer_company_portal.py`, `customer_data_plane.py`, `customer_loop.py`,
`customer_success_scores.py`, `data.py`, `decision_passport.py`,
`deliverables.py`, `delivery_factory.py`, `delivery_os.py`, `drafts.py`,
`email_send.py`, `executive_reporting.py`, `expansion_engine.py`,
`integration_capability.py`, `intelligence_layer.py`, `jobs.py`,
`outreach.py`, `payment_ops.py`, `pdpl.py`, `proof_ledger.py`,
`prospect.py`, `revenue.py`, `revenue_pipeline.py`,
`revenue_os_catalog.py`, `sectors.py`, `service_catalog.py`,
`service_quality.py`, `service_sessions.py`, `support_journey.py`,
`vertical_playbooks.py`, `whatsapp_decision_bot.py`, `zatca.py`,
`health.py`.

## active-internal (founder / admin / observability)

`admin.py`, `bottleneck_radar.py`, `case_study_engine.py`,
`channel_policy_gateway.py`, `company_brain.py`, `customer_brain.py`,
`customer_success_os.py`, `designops.py`, `diagnostic.py`,
`diagnostic_workflow.py`, `dominance.py`, `ecosystem.py`,
`executive_command_center.py`, `executive_os.py`,
`executive_pack_per_customer.py`, `finance_os.py`, `founder.py`,
`founder_beast_command_center.py`, `full_ops.py`, `full_ops_radar.py`,
`full_os.py`, `growth_beast.py`, `growth_os.py`, `gtm_os.py`,
`leadops_reliability.py`, `leadops_spine.py`, `partnership_os.py`,
`personal_operator.py`, `proof_to_market.py`, `radar_events.py`,
`reliability_os.py`, `revenue_os.py`, `revenue_profitability.py`,
`revops.py`, `role_command.py`, `role_command_os.py`, `sales_os.py`,
`search_radar.py`, `security_privacy.py`, `self_growth.py`,
`self_improvement_os.py`, `support_os.py`, `support_webhook.py`,
`tool_guardrail_gateway.py`, `unified_operating_graph.py`.

## beta

`ai_workforce.py`, `autonomous.py`, `company_growth_beast.py`.

## versioned-legacy (freeze; do not extend)

| Slice | Members |
| --- | --- |
| v3 | `v3.py` |
| v6 | `company_brain_v6.py`, `observability_v6.py` |
| v7 | `service_mapping_v7.py` |
| v10 | `ai_workforce_v10.py`, `crm_v10.py`, `customer_inbox_v10.py`, `founder_v10.py`, `growth_v10.py`, `knowledge_v10.py`, `llm_gateway_v10.py`, `observability_v10.py`, `safety_v10.py`, `v10_status.py`, `workflow_os_v10.py` |
| v11 | `v11_status.py` |

These are wired through `api.routers.domains.deprecated` and are tagged
`Deprecated` in the OpenAPI schema. Plan to remove the v3/v6/v7 slices in
the next major version (`v2.0.0`) once internal consumers migrate.

## archive-candidate

None until import-graph audit completes. Pending follow-up — see
`docs/QA_REVIEW.md` S.1.

---

## How to keep this file accurate

- When adding a router, append it to the right table here in the same PR.
- When deprecating a router, move it to `versioned-legacy` and add a sunset
  date in its module docstring.
- Quarterly: re-run `grep -rln "from api.routers" api/ | sort -u` to detect
  unmapped routers.
