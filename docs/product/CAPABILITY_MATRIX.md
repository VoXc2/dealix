# Product Capability Matrix

Maps each customer-visible capability to its backing code module and current
state. Used to decide which services can scale vs which must stay service-
assisted.

## Status legend
- **Ready** = production-grade (tests + audit log + cost guard + docs)
- **Partial** = MVP wired, missing tests / observability / hardening
- **Beta** = working in demos, not customer-ready
- **Not Ready** = not built

## Matrix

| Capability | Required For | Module Path | MVP | Production |
|------------|--------------|-------------|:---:|:----------:|
| CSV import preview | Lead Intelligence, Data Cleanup | `auto_client_acquisition/customer_data_plane/` | Partial | Partial |
| Field validation (Saudi CR/VAT/phone/email) | All Data OS-backed services | `customer_data_plane/validation_rules.py` | Ready | Partial |
| Data quality scoring (0–100) | All services (gate) | `customer_data_plane/data_quality_score.py` | Ready | Partial |
| Dedupe (CR / VAT / domain / fuzzy name) | Lead Intelligence, Data Cleanup | `revenue_os/dedupe.py` | Ready | Partial |
| PII detection | All services (gate) | `customer_data_plane/pii_detection.py` + `dealix/trust/pii_detector.py` | Ready | Partial |
| Source attribution | All services (gate) | Data OS quality score | Ready | Partial |
| ICP builder | Lead Intelligence, Sales | `revenue_os/icp_builder.py` | Ready | Partial |
| Lead scoring (A/B/C/D) | Lead Intelligence | `revenue_os/lead_scoring.py` | Ready | Partial |
| Outreach drafts | Lead Intelligence | (LLM-backed; via Outreach OS in Phase 2) | Beta | Not Ready |
| Pipeline / Mini CRM | Lead Intelligence | (frontend page; backend via revenue routes) | Beta | Not Ready |
| Workflow builder | AI Quick Win, Automate Operations | `auto_client_acquisition/orchestrator/runtime.py` | Partial | Partial |
| SOP builder | SOP Automation | (planned Phase 2) | Not Ready | Not Ready |
| RAG ingestion | Company Brain | `knowledge_v10/` | Beta | Not Ready |
| RAG retrieval with citations | Company Brain (HARD RULE: no source = no answer) | `knowledge_v10/retrieval.py` | Beta | Not Ready |
| Freshness policy | Company Brain | `knowledge_v10/freshness_policy.py` (planned Phase 2) | Not Ready | Not Ready |
| Suggested replies | AI Support Desk | `support_os/` + `customer_inbox_v10/` (needs consolidation) | Beta | Not Ready |
| Message classification | AI Support Desk | same as above | Beta | Not Ready |
| Forbidden claims filter | All outbound | `dealix/trust/forbidden_claims.py` | Ready | Partial |
| Approval matrix | All side-effect actions | `dealix/trust/approval_matrix.py` | Ready | Partial |
| Decision Passport | All outbound (gate) | `api/routers/decision_passport.py` | Ready | Partial |
| Event store (immutable audit) | All projects | `revenue_memory/event_store.py` + `pg_event_store.py` | Ready | Partial |
| Stage Machine (8-stage Delivery Standard) | All projects | `delivery_factory/stage_machine.py` | Ready | Partial |
| QA review (5-gate + 100-pt score) | All projects (handoff gate) | `delivery_factory/qa_review.py` | Ready | Partial |
| Executive report generator | All projects | `dealix/reporting/executive_report.py` | Ready | Partial |
| Proof Pack generator | All projects (Stage 7) | `dealix/reporting/proof_pack.py` | Ready | Partial |
| ROI calculator | Lead Intelligence sales | `revenue_os/roi_calculator.py` | Ready | Partial |
| LLM Gateway (cost / routing / cache) | All model calls | `dealix/llm_gateway/` (planned Phase 2) | Not Ready | Not Ready |
| Multi-tenant isolation | Enterprise | (ADR 0003) | Not Ready | Not Ready |
| Audit export | Enterprise | (Phase 4) | Not Ready | Not Ready |

## Decision rules

- A service that depends on a **Not Ready** capability cannot be sold as Official.
- A service that depends on a **Beta** capability can be sold as Beta only.
- All "All services (gate)" capabilities must be at least **Ready** at MVP before any sale.

## Capability → service impact

- **Outreach drafts (Beta)** → Lead Intelligence Sprint ships outputs as drafts only; no auto-send. Hard rule preserved by `forbidden_claims` + `approval_matrix`.
- **RAG retrieval (Beta)** → Company Brain Sprint ships with the keyword-match retriever from the demo as MVP; full RAG indexing comes in Phase 2 via `knowledge_v10/chunking.py` + `freshness_policy.py`.
- **Suggested replies (Beta)** → AI Support Desk Sprint stays Not Ready until `customer_os/` consolidation lands in Phase 2.

## Owner & cadence
- **Owner**: CTO.
- **Refresh**: monthly during operating-cadence quarterly module health review.
- **Escalation**: any capability flagged for use in a Sellable service that drops to Beta — Friday engineering review.
