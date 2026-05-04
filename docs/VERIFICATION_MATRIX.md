# Dealix — Verification Matrix

> Per-system acceptance row. Generated for the 14 vision systems + the 6
> verification layers. Replaces the ad-hoc 14_SYSTEMS_MAP.md status with
> a strict System | Files | API | Test | CLI | Status table.

## Workflow Diagram (canonical)

```
[Website / wa.me / LinkedIn warm]
        ↓
[Operator Intent Router] → [Company Brain] → [Service Recommendation]
        ↓
[Prospect Tracker + Stage Machine v2 (14 stages)]
        ↓
[Role Cards (9 roles)]
        ↓
[Safe Action Gateway]
        ↓
[Approval Queue]
        ↓
[Manual or Safe Execution]
        ↓
[RWU → Proof Ledger → Customer Workspace]
        ↓
[Proof Pack (HMAC) → Upsell → Weekly Learning]  ↺
```

## The Matrix

| # | System | Files | API | Test | CLI | Status |
|---|---|---|---|---|---|---|
| 1 | CEO Command OS | `revenue_company_os/ceo_command_os.py` | `GET /api/v1/role-briefs/daily?role=ceo` | `tests/test_pr_commercial_close.py::test_role_brief_ceo` | `dealix today` | ✅ live |
| 2 | Sales Manager OS | `revenue_company_os/sales_manager_os.py` | `GET /api/v1/sales-os/pipeline-snapshot` | `tests/test_pr_commercial_close.py` | — | ✅ live |
| 3 | Growth Manager OS | `revenue_company_os/growth_manager_os.py` | `GET /api/v1/growth-os/daily-plan` | `tests/test_pr_commercial_close.py` | — | ✅ live |
| 4 | RevOps OS | `revenue_company_os/revops_os.py` | `GET /api/v1/revops/funnel` | `tests/test_pr_commercial_close.py` | — | ✅ live |
| 5 | WhatsApp Layer | `whatsapp_brief_renderer.py`, `assets/js/whatsapp-preview.js` | `GET /api/v1/whatsapp/brief?role=X` + send-internal returns 403 | `tests/test_pr_vision_close.py::test_a4_*` | — | ✅ live (preview) |
| 6 | Call & Meeting Intelligence | `call_meeting_intelligence_os.py`, `routers/meetings.py` | `POST /api/v1/meetings/log`, `/closed`, `GET /brief` | `tests/test_pr_vision_close.py::test_b1_*` | — | ✅ live |
| 7 | Service Tower (with Contracts) | `routers/services.py`, `service_tower/contracts.py` | `GET /api/v1/services/catalog`, `/{id}/contract` | `tests/test_os_foundation.py::test_1_3_*` | — | ✅ live (contracts NEW) |
| 8 | Proof Ledger + Pack | `proof_ledger.py`, `proof_pack_builder.py`, `proof_pack_pdf.py` | `POST /events`, `GET /customer/{id}/pack.html` | `tests/test_pr_vision_close.py::test_a3_*` | `dealix proof <cus_id>` | ✅ live + HMAC |
| 9 | Revenue Work Units (14) | `revenue_work_units.py` | `GET /api/v1/proof-ledger/units` | `tests/test_os_foundation.py::test_1_2_two_new_rwus_in_catalog` | — | ✅ 14 RWUs |
| 10 | Partner / Agency OS | `partner_os/agency_partner_os.py` | `GET /api/v1/role-briefs/daily?role=agency_partner` | — | — | ✅ live |
| 11 | Customer Success OS | `customer_ops/customer_success_os.py` | `GET /api/v1/customer-success/health` | — | — | ✅ live |
| 12 | Finance / Billing OS | `customer_ops/finance_os.py`, `routers/payments.py` | `GET /payments/state`, `POST /payments/invoice` | `tests/test_pr_vision_close.py` | `dealix invoice` | ✅ live |
| 13 | Compliance & Safety OS | `customer_ops/compliance_os.py`, `compliance/forbidden_claims.py`, `role_action_policy.py` | `GET /api/v1/compliance/blocked-actions` | `tests/test_os_foundation.py::test_1_9_*` | `dealix gates` | ✅ live + draft-time |
| 14 | Self-Growth + Learning Engine | `self_growth_mode.py`, `routers/learning.py` | `GET /api/v1/learning/weekly`, `/today` | `tests/test_os_foundation.py::test_1_6_*`, `test_learning_weekly_endpoint` | `dealix learning weekly` | ✅ live |
| + | **Customer Workspace** (foundation) | `routers/companies.py`, `landing/client.html` | `GET /api/v1/companies/{id}/workspace` | `tests/test_os_foundation.py::test_workspace_returns_full_shape` | `dealix workspace <cus_id>` | ✅ NEW |
| + | **Company Brain** (foundation) | `routers/companies.py`, `db/models.py:CustomerRecord` | `GET/PATCH /api/v1/companies/{id}/brain` | `tests/test_os_foundation.py::test_1_7_*` | `dealix brain <cus_id>` | ✅ NEW |
| + | **Approval Queue** (foundation) | `routers/actions.py` | `GET /api/v1/actions/pending`, `POST /approve\|reject`, `GET /funnel` | `tests/test_os_foundation.py::test_1_5_*`, `test_actions_pending_endpoint` | `dealix approvals` | ✅ NEW |

## 6-Layer Verification

| Layer | What it checks | How to run | Expected |
|---|---|---|---|
| 1. Feature Inventory | every claimed file exists | `python scripts/feature_inventory.py` | `OK: N feature(s) · M file(s) all present` |
| 2. Empty Files | no zero-byte files in critical dirs | `find api auto_client_acquisition landing scripts tests -type f -size 0` | empty output |
| 3. Imports | every router + module imports cleanly | `python -c "from api.main import app"` | no error |
| 4. Router Registration | every `*.py` in `api/routers/` is included in `api/main.py` | `python scripts/check_routes_registered.py` | exit 0 |
| 5. Secrets Scan | no live secrets committed | `grep -RniE '(sk_live\|ghp_\|MOYASAR_SECRET=)' api auto_client_acquisition` | empty |
| 6. Live Gates Sanity | all 8 gates default-False | `python scripts/launch_readiness_check.py` | `GO_PRIVATE_BETA` |

All 6 layers are wrapped in `bash scripts/full_acceptance.sh` — single command,
single exit code.

## 17-Checkpoint Definition of Done

The system is "done" when **every** one of these is green via `full_acceptance.sh`:

1. ✅ Files non-empty
2. ✅ Imports clean
3. ✅ Routers registered
4. ✅ `/healthz` 200
5. ✅ `/docs` opens
6. ✅ Catalog 6 bundles + each `/contract`
7. ✅ Operator 4 scenarios (3 recommend + 1 BLOCKED)
8. ✅ Cold WhatsApp blocked at API + draft level
9. ✅ Prospect E2E with RWUs
10. ✅ Stage v2 forward-only enforced
11. ✅ Invoice 499 SAR (Moyasar or fallback)
12. ✅ Payment confirm auto-creates CustomerRecord + Brain
13. ✅ Proof Pack with HMAC
14. ✅ Role briefs 9 roles
15. ✅ WhatsApp brief renders Arabic + send-internal 403
16. ✅ 8/8 gates FALSE
17. ✅ No secrets in code
