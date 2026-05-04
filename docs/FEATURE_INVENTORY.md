# Dealix — Feature Inventory

> **Layer-1 verification** (per the 6-layer Doctrine). Every feature claimed
> here has a parseable ```inventory``` block listing its files. The script
> `scripts/feature_inventory.py` reads each block and asserts every referenced
> path exists. Lying breaks CI.

The 14 vision systems + the verification spine, mapped to concrete files.

---

## Workflow Diagram (canonical — repeated in 3 docs)

```
[Website / wa.me / LinkedIn warm]
        ↓
[Operator Intent Router]
        ↓
[Company Brain Created or Loaded]
        ↓
[Service Recommendation]
        ↓
[Prospect Tracker + Stage Machine v2 (14 stages)]
        ↓
[Role Cards: CEO / Sales / Growth / RevOps / CS / Finance / Compliance / Agency / Meeting]
        ↓
[Safe Action Gateway — channel policy + consent + forbidden claims]
        ↓
[Draft / Call Script / Meeting Brief / Invoice]
        ↓
[Approval Queue (per role)]
        ↓
[Manual or Safe Execution]
        ↓
[RWU Emitted → Proof Ledger]
        ↓
[Customer Workspace updated]
        ↓
[Proof Pack (HMAC-signed HTML/PDF)]
        ↓
[Upsell Recommendation]
        ↓
[Weekly Learning Loop]  ↺
```

---

## Inventory blocks (parsed by `scripts/feature_inventory.py`)

```inventory
feature_id           | file_paths
public_website       | landing/index.html,landing/services.html,landing/pricing.html,landing/trust-center.html,landing/proof-pack.html,landing/onboarding.html
service_tower        | api/routers/services.py,auto_client_acquisition/service_tower/contracts.py,auto_client_acquisition/service_tower/excellence_score.py
ai_operator          | api/routers/operator.py,landing/operator.html,landing/assets/js/operator.js
prospect_tracker     | api/routers/prospects.py,db/models.py
stage_machine_v2     | api/routers/prospects.py
role_briefs          | auto_client_acquisition/revenue_company_os/role_brief_builder.py,api/routers/role_briefs.py
ceo_command_os       | auto_client_acquisition/revenue_company_os/ceo_command_os.py
sales_manager_os     | auto_client_acquisition/revenue_company_os/sales_manager_os.py
growth_manager_os    | auto_client_acquisition/revenue_company_os/growth_manager_os.py
revops_os            | auto_client_acquisition/revenue_company_os/revops_os.py
customer_success_os  | auto_client_acquisition/customer_ops/customer_success_os.py
finance_os           | auto_client_acquisition/customer_ops/finance_os.py
compliance_os        | auto_client_acquisition/customer_ops/compliance_os.py
agency_partner_os    | auto_client_acquisition/partner_os/agency_partner_os.py
meeting_intel_os     | auto_client_acquisition/revenue_company_os/call_meeting_intelligence_os.py,api/routers/meetings.py
whatsapp_layer       | api/routers/whatsapp_briefs.py,auto_client_acquisition/revenue_company_os/whatsapp_brief_renderer.py,landing/assets/js/whatsapp-preview.js
safe_action_gateway  | auto_client_acquisition/revenue_company_os/role_action_policy.py,api/middleware.py
forbidden_claims     | auto_client_acquisition/compliance/forbidden_claims.py,scripts/forbidden_claims_audit.py
proof_ledger         | auto_client_acquisition/revenue_company_os/proof_ledger.py,auto_client_acquisition/revenue_company_os/proof_pack_builder.py,auto_client_acquisition/revenue_company_os/proof_pack_pdf.py,api/routers/proof_ledger.py
revenue_work_units   | auto_client_acquisition/revenue_company_os/revenue_work_units.py
payments             | api/routers/payments.py
customer_workspace   | api/routers/companies.py,landing/client.html,landing/assets/js/client-workspace.js
company_brain        | api/routers/companies.py,db/models.py
approval_queue       | api/routers/actions.py
learning_engine      | auto_client_acquisition/revenue_company_os/self_growth_mode.py,api/routers/learning.py,api/routers/self_growth.py
daily_ops_cron       | auto_client_acquisition/revenue_company_os/daily_ops_orchestrator.py,scripts/cron_daily_ops.py,railway.json
cli_tools            | scripts/dealix_cli.py
acceptance_tooling   | scripts/full_acceptance.sh,scripts/feature_inventory.py,scripts/check_routes_registered.py,scripts/launch_readiness_check.py,scripts/repo_architecture_audit.py,scripts/forbidden_claims_audit.py
```

---

## Per-feature acceptance (the 17-checkpoint DoD)

| # | Check | Evidence (where to look) |
|---|---|---|
| 1 | All files non-empty | `find . -type f -size 0` returns nothing in `api/`, `auto_client_acquisition/`, `landing/`, `scripts/`, `tests/` |
| 2 | Imports OK | `python -c "from api.main import app"` returns without error |
| 3 | Routers registered | `python scripts/check_routes_registered.py` exits 0 |
| 4 | `/healthz` returns 200 | live request |
| 5 | `/docs` opens | live request |
| 6 | services catalog returns 6 bundles + each contract | `GET /api/v1/services/catalog` + `GET /api/v1/services/{id}/contract` |
| 7 | Operator handles 4 scenarios | `POST /api/v1/operator/chat/message` with the 4 from `full_acceptance.sh` |
| 8 | Cold WhatsApp blocked at draft level | `assert_safe()` raises on `"نضمن ..."` and `"cold whatsapp"` |
| 9 | Prospect E2E + RWUs | `dealix first-customer-flow` |
| 10 | Stage v2 forward-only | `tests/test_os_foundation.py::test_stage_machine_forward_only` |
| 11 | Invoice 499 SAR | `POST /api/v1/payments/invoice` with manual fallback |
| 12 | Payment confirm auto-creates Customer + Brain | `tests/test_os_foundation.py::test_workspace_returns_full_shape` |
| 13 | Proof Pack with HMAC | `GET /api/v1/proof-ledger/customer/{id}/pack.html` |
| 14 | Role briefs for 9 roles | `GET /api/v1/role-briefs/daily?role=*` |
| 15 | WhatsApp brief Arabic + send-internal returns 403 | `GET /api/v1/whatsapp/brief?role=ceo` + `POST /api/v1/whatsapp/brief/send-internal` → 403 |
| 16 | All 8 gates default-False | `dealix gates` → `8/8 FALSE ✓` |
| 17 | No secrets in code | grep extended in `full_acceptance.sh` Layer-5 |
