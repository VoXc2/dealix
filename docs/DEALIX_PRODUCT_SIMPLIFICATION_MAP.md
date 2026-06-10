# Dealix — Product Simplification Map (Phase 1)

**Date:** 2026-05-07
**Audience:** founder + sales + customer
**Rule:** customers see ONLY 4 names. All ~32 internal modules map to one of these.

---

## The 4 customer-facing names

1. **Dealix Radar** — strategic visibility (سيرى ماذا يحدث في شركتي + ماذا يجب أن أفعل)
2. **Dealix AI Team** — operational delivery (٥ وكلاء AI ينفّذون الأعمال اليوميّة)
3. **Dealix Portal** — customer interface (لوحة العميل + Operations Console)
4. **Dealix Proof** — accountability + evidence (سجلّ ما حدث ولماذا — لا ادّعاء بدون دليل)

Internal names (V11/V12/V12.5/V13/V14/beast/growth_beast/revops/customer_inbox_v10/etc.) NEVER appear in customer HTML/JSON.

---

## Master mapping table

| Internal name | Customer-facing name | Where it appears | Show/Hide | Business value | Proof metric | Readiness |
|---|---|---|---|---|---|---|
| `leadops_spine` | Dealix AI Team — Lead qualification | server only | hide | new leads scored + drafted | leads_today, drafts_pending | LIVE Wave 3 |
| `leadops_reliability` (Wave 5) | Dealix Radar — Lead pipeline health | internal-only | hide | "where am I leaking?" | reliability_score | Wave 5 P4 |
| `customer_brain` | Dealix AI Team — Customer memory | server only | hide | per-customer ICP/channels/risks | snapshot_built | LIVE Wave 3 |
| `service_sessions` | Dealix Portal — Service in flight | customer portal | show with safe label | track delivery progress | sessions_active | LIVE Wave 3 |
| `approval_center` | Dealix AI Team — Decisions queue | `/decisions.html` (founder) | hide internally | every external action gated | drafts_pending | LIVE V12 + extended Wave 3 |
| `payment_ops` | Dealix Portal — Payment state | customer portal | show | revenue truth (no fake) | payment_confirmed | LIVE Wave 3 |
| `proof_ledger` | Dealix Proof — Evidence trail | customer portal | show | every claim has source | proof_events_count | LIVE V11 + extended Wave 3 |
| `support_inbox` + `support_os` | Dealix AI Team — Support replies | server only | hide | classified, escalated, drafted | tickets_open | LIVE V12 + Wave 3 |
| `support_journey` (Wave 5) | Dealix Portal — Support timeline | customer portal | show | pre_sales/onboarding/delivery/billing/proof/renewal stages | stage_distribution | Wave 5 P7 |
| `executive_pack_v2` | Dealix Radar — Executive brief | exec dashboard | show | daily/weekly summary | pack_built | LIVE Wave 3 |
| `case_study_engine` | Dealix Proof — Case studies | sales library | show after consent | published proof | library_size | LIVE Wave 3 |
| `unified_operating_graph` | Dealix Radar — Operating graph | exec dashboard | show indirectly | cross-layer map | graph_node_count | LIVE Wave 4 |
| `full_ops_radar` | Dealix Radar — Full-Ops Score | exec + customer portal | show | one number CEO understands | score_0_100 | LIVE Wave 4 |
| `executive_command_center` | Dealix Radar — Executive Command Center | `/executive-command-center.html` | show | 15 sections in one view | sections_populated | LIVE Wave 4 |
| `whatsapp_decision_bot` | Dealix AI Team — WhatsApp brief (admin) | internal admin | hide | ask the system in Saudi Arabic | decisions_briefed | LIVE Wave 4 |
| `channel_policy_gateway` | Dealix AI Team — Send policy | server only | hide | every channel pre-checked | policies_evaluated | LIVE Wave 4 |
| `tool_guardrail_gateway` (Wave 5) | Dealix AI Team — Tool guardrails | server only | hide | every tool call audited | guardrails_passed | Wave 5 P8 |
| `radar_events` | Dealix Radar — Event backbone | server only | hide | analytics without external dep | events_recorded | LIVE Wave 4 |
| `agent_observability` | Dealix AI Team — Trace + cost | server only | hide | "what did the AI cost?" | total_cost_usd | LIVE Wave 4 |
| `revenue_profitability` (Wave 5) | Dealix Radar — Profitability radar | internal-only | hide | "which package bleeds?" | gross_margin_per_service | Wave 5 P6 |
| `customer_company_portal` | Dealix Portal | `/customer-portal.html` | show | the 8-section view | sections_populated | LIVE V12.5 + Wave 4 |
| `revenue_graph` | Dealix Radar — Revenue graph (internal) | internal | hide | leak detection + maturity | maturity_score | LIVE older |
| `growth_beast` / `company_growth_beast` | Dealix Radar — Growth radar | internal | hide | sector + signal scanning | opportunities_count | LIVE older |
| `founder_beast_command_center` | Dealix Radar — Founder dashboard | `/founder.html` (founder-tier) | hide internally | top-3 decisions / risks | sections_populated | LIVE older |
| `role_command_os` / `role_command` | Dealix Radar — Role briefs | internal | hide | per-role daily brief | briefs_built | LIVE older |
| `executive_reporting` | Dealix Radar — Reporting | internal | hide | weekly/monthly reports | reports_built | LIVE older |
| `proof_to_market` | Dealix Proof — Sales snippets | internal | hide | proof → social/sales | snippets_built | LIVE older |
| `crm_v10` | Dealix Portal — CRM model | server only | hide | accounts/contacts/deals | accounts_count | LIVE V10 |
| `customer_inbox_v10` | Dealix AI Team — Conversations | internal | hide | unified conversation model | conversations_count | LIVE V10 |
| `knowledge_v10` | Dealix AI Team — Knowledge | internal | hide | knowledge base | sources_count | LIVE V10 |
| `workflow_os_v10` | Dealix AI Team — Workflows | internal | hide | service session workflows | workflows_defined | LIVE V10 |
| `safety_v10` | Dealix Radar — Safety | internal | hide | gate enforcement | gates_active | LIVE V10 |
| `observability_v10` | Dealix AI Team — Observability | internal | hide | trace recording | traces_count | LIVE V10 |
| `compliance_os_v12` | Dealix Radar — Compliance | internal | hide | PDPL + 8 gates | findings_count | LIVE V12 |
| `consent_table` | Dealix Radar — Consent | internal | hide | consent records | consents_recorded | LIVE older |
| `whatsapp_safe_send` | Dealix AI Team — Safe send | internal | hide | 6-gate WhatsApp orchestration | gates_evaluated | LIVE older |
| `designops/safety_gate` | Dealix Radar — Safety gate | internal | hide | content scrub | findings_count | LIVE older |
| `integration_upgrade` (Wave 4) | Dealix Radar — Adapter shim | internal only | hide | safe_call + degraded fallback | degraded_count | LIVE Wave 4 |

---

## Summary by customer-facing name

### Dealix Radar (strategic)
- Full-Ops Score
- Weakness Radar
- Executive Command Center (15 sections)
- Unified Operating Graph
- Executive Pack v2
- Founder Beast Command Center
- Growth Beast / Company Growth Beast
- Role Command briefs
- Compliance + Safety
- (Wave 5) LeadOps Reliability + Revenue Profitability + Tool Guardrails

### Dealix AI Team (operational)
- LeadOps Spine
- Customer Brain
- Approval Center
- Support Inbox + Support OS
- WhatsApp Decision Bot
- Channel Policy Gateway
- Agent Observability
- Customer Inbox V10
- Knowledge V10
- Workflow OS V10
- Observability V10

### Dealix Portal (customer interface)
- Customer Company Portal API + frontend
- Service Sessions
- Payment Ops
- (Wave 5) Support Journey

### Dealix Proof (accountability)
- Proof Ledger
- Case Study Engine
- Proof-to-Market
- Audit trail across all routers

---

## Customer-visible language rules

| Internal term | Customer-facing replacement |
|---|---|
| `LeadOps Spine` | "Lead qualification" |
| `Service Session` | "Service in flight" / "جلسة خدمة" |
| `Approval Center` | "Decisions queue" / "مركز القرارات" |
| `Payment Ops` | "Payment state" / "حالة الدفع" |
| `Proof Ledger` | "Evidence trail" / "سجلّ الأدلّة" |
| `Executive Command Center` | "Executive Command Center" / "مركز القيادة التنفيذي" |
| `Full-Ops Score` | "Full-Ops Score" / "مؤشّر العمليّات الكاملة" |
| `Weakness Radar` | "Where to fix next" / "أولويّات التحسين" |
| `WhatsApp Decision Bot` | "Internal command brief" / "ملخّص داخلي للقرارات" |
| `Tool Guardrail Gateway` | "Send policy" / "سياسة الإرسال" (when surfaced) |

---

## Test enforcement

`tests/test_customer_safe_product_language.py` (added in Phase 1) asserts:
- No customer-facing HTML contains: `v10`, `v11`, `v12`, `v13`, `v14`, `beast`, `growth_beast`, `revops`, `customer_inbox_v10`, `compliance_os_v12`, `auto_client_acquisition`, `_safe`, `stacktrace`, `pytest`, `internal_error`, `endpoint`
- No customer-facing API response (e.g. `customer_company_portal.py` payload) contains the same forbidden tokens (already covered by `test_constitution_closure.py::test_portal_no_internal_leakage`)
- Documentation files in `docs/` are EXEMPT (engineers read those)
