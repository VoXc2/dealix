# `auto_client_acquisition/` — Inventory

**Generated:** 2026-05-12. **Subdirectory count:** 98.

This package houses the engines that power Dealix's outbound, intelligence,
revenue, customer-success, and compliance surfaces. It is **actively wired
into `api/`** — verified by `grep -rln "from auto_client_acquisition" api/`
which finds the vast majority of subpackages imported from at least one
router or dependency module.

The package grew organically through 17 product waves and now needs an
inventory so contributors know what is canonical vs legacy vs experimental.

Statuses are conservative; nothing here is marked for removal without an
import-graph audit. Where you see "verified import" it means the package
appears in at least one `api/*.py` import line.

---

## Canonical engines (active-core)

These are imported by routers tagged `active-core` in
`api/routers/INVENTORY.md` and back the Top-3 customer-facing workflows.

| Subpackage | Used by | Purpose |
| --- | --- | --- |
| `agents/` | `api/dependencies.py`, several routers | Proposal, ICP-matcher, qualification, booking. |
| `pipelines/`, `pipeline.py` | `api/dependencies.py` | LangGraph orchestration entrypoint. |
| `connectors/` | Webhooks + integrations | HubSpot, Calendly, WhatsApp, n8n. |
| `email/` | `api/routers/automation.py` | Compliance gate, daily targeting, reply classifier. |
| `compliance_os/`, `compliance_os_v12/` | `api/routers/customer_data_plane.py`, `v3.py` | PDPL ingestion, ROPA, consent. |
| `customer_data_plane/` | `api/routers/customer_data_plane.py` | Consent registry, redaction. |
| `customer_loop/` | `api/routers/customer_loop.py` | Onboarding/health loop. |
| `customer_success/` | `api/routers/customer_success.py` | Health scoring scaffolding. |
| `revenue_pipeline/`, `revenue_os/`, `revenue_memory/` | revenue routers | Pipeline state, recall, prioritisation. |
| `leadops_spine/` | `api/routers/leadops_spine.py` | Lead lifecycle backbone. |

## Active supporting

Imported by `active-supporting` or `active-internal` routers. Safe to extend;
not customer-facing.

`ai_workforce/`, `approval_center/`, `bottleneck_radar/`,
`business/`, `business_metrics_board/`, `business_ops/`,
`case_study_engine/`, `channel_policy_gateway/`, `copilot/`,
`customer_brain/`, `customer_readiness/`, `decision_passport/`,
`deliverables/`, `delivery_factory/`, `designops/`, `diagnostic_engine/`,
`diagnostic_workflow/`, `ecosystem/`, `executive_command_center/`,
`executive_reporting/`, `expansion_engine/`, `finance_os/`, `full_ops/`,
`full_ops_contracts/`, `full_ops_radar/`, `growth_beast/`,
`gtm_os/`, `integration_capability/`, `integration_upgrade/`,
`intelligence/`, `learning_flywheel/`, `market_intelligence/`,
`notifications/`, `observability_adapters/`, `orchestrator/`,
`partnership_os/`, `payment_ops/`, `personal_operator/`, `proof_engine/`,
`proof_ledger/`, `proof_to_market/`, `providers/`, `radar_events/`,
`reliability_os/`, `revenue_graph/`, `revenue_profitability/`,
`revenue_science/`, `revops/`, `role_command_os/`, `safe_send_gateway/`,
`security_privacy/`, `self_growth_os/`, `service_catalog/`,
`service_quality/`, `service_sessions/`, `support_inbox/`,
`support_journey/`, `support_os/`, `tool_guardrail_gateway/`,
`unified_operating_graph/`, `vertical_os/`, `vertical_playbooks/`,
`whatsapp_decision_bot/`.

## Versioned-legacy (freeze; do not extend)

These mirror the API's versioned-legacy routers and exist for one-shot
back-compat. Plan to retire alongside their router twins in `v2.0.0`.

| Slice | Subpackages |
| --- | --- |
| v3 | `v3/` |
| v6 | `company_brain_v6/`, `observability_v6/` |
| v7 | `service_mapping_v7/` |
| v10 | `ai_workforce_v10/`, `crm_v10/`, `customer_inbox_v10/`, `founder_v10/`, `growth_v10/`, `knowledge_v10/`, `llm_gateway_v10/`, `observability_v10/`, `platform_v10/`, `safety_v10/`, `workflow_os_v10/` |
| v12 | `compliance_os_v12/`, `executive_pack_v2/` |

## Beta / experimental

`ai/`, `company_growth_beast/`.

## Archive candidates

None confirmed without a deeper import-graph audit. The script
`scripts/audit_orphan_endpoints.py` can be extended to detect unimported
subpackages — that audit is pending and tracked in `docs/QA_REVIEW.md` S.1.

---

## How to keep this file accurate

- New subpackage → append to the right table in the same PR; explain who
  imports it.
- Deprecate → move row to `versioned-legacy` with sunset date in the
  package `__init__.py` docstring.
- Quarterly: `python scripts/audit_orphan_endpoints.py` (or
  `grep -rln "from auto_client_acquisition" api/`) and reconcile with this
  inventory.
