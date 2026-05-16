# API Domain Ownership

## Domains

| Domain | Path | Owner OS | Routers (batch 1 in sales) |
|--------|------|----------|------------------------------|
| sales | `api/routers/domains/sales/` | gtm | unified_readiness, deal_desk, trust_dashboard, commercial_readiness, revenue_os |
| compliance | `api/routers/domains/compliance/` | trust | pdpl, compliance_status |
| customers | `api/routers/domains/customers/` | delivery | deliverables, customer_success |
| admin | `api/routers/domains/admin/` | platform | admin_tenants |
| agents | `api/routers/domains/agents/` | platform | agent_os, control_plane |
| analytics | `api/routers/domains/analytics/` | data | business_metrics_board |
| webhooks | `api/routers/domains/webhooks/` | platform | customer_webhooks |

## Migration policy

1. New endpoints register under `api/routers/domains/<domain>/`.
2. Legacy flat routers in `api/main.py` migrate in batches; do not duplicate routes.
3. Each domain maintains `OWNERS.yaml` with `primary_owner` and `escalation_owner`.

## Batch 1 (this program)

Moved to sales domain aggregators:

- `unified_readiness` → `/api/v1/readiness/unified`
- `deal_desk` → `/api/v1/commercial/deal-desk`
- `trust_dashboard` → `/api/v1/trust/dashboard`

## Governance council

See [API_GOVERNANCE_COUNCIL_AR.md](API_GOVERNANCE_COUNCIL_AR.md).
