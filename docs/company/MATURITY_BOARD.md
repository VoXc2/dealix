# Dealix Maturity Board

Single dashboard for "how mature is each area of the company?" Refreshed
monthly. Each row has a target, current level, evidence link, and the
next fix the owner must complete.

## Maturity levels

- **0** = Not started
- **1** = Documented
- **2** = Demo runnable
- **3** = Beta (1–2 customers)
- **4** = Sellable (productized, repeatable)
- **5** = Scalable (delivered by someone other than the founder, repeatedly, with stable QA)

## Board (refresh monthly)

| Area | Current | Target | Evidence | Next fix |
|------|--------:|------:|----------|----------|
| Positioning | 4 | 5 | `docs/company/POSITIONING.md` + `docs/strategy/dealix_operating_partner_positioning.md` | Sharpen ICP language for clinics + logistics |
| Service Catalog | 4 | 5 | `docs/strategy/service_portfolio_catalog.md` + `docs/company/SERVICE_REGISTRY.md` | Move AI Support Desk from Designed → Beta |
| Lead Intelligence Sprint | 4 | 5 | offer/scope/intake/QA/proof_pack + demo | First paying customer → case study |
| AI Quick Win Sprint | 4 | 5 | service folder + demo + sample output | First paying customer → ROI baseline captured |
| Company Brain Sprint | 4 | 5 | service folder + demo + sample output | First paying customer + ≥95% citation eval |
| AI Support Desk Sprint | 2 | 4 | folder + intake | Build customer_os consolidation + demo |
| AI Governance Program | 2 | 4 | folder + policy templates | Build governance dashboard |
| Workflow Automation Sprint | 1 | 4 | designed only | Build workflow_builder + SOP builder |
| Data OS | 3 | 5 | validation_rules + data_quality_score + pii_detection | Add entity_resolution + warehouse adapter |
| Revenue OS | 3 | 5 | lead_scoring + icp_builder + roi_calculator + /seed endpoint | Add outreach_drafts production-grade + pipeline UI |
| Customer OS | 2 | 4 | fragmented across support_os + customer_inbox_v10 | Consolidate to unified customer_os/ |
| Knowledge OS | 2 | 4 | demo retriever | Build chunking + freshness_policy + eval framework |
| Operations OS | 3 | 5 | orchestrator/runtime.py | Add sop_builder + exception_handler + ops_dashboard |
| Governance OS | 4 | 5 | pii_detector + forbidden_claims + approval_matrix + policy.py | Add governance dashboard + audit export |
| Reporting OS | 4 | 5 | executive_report + proof_pack + weekly_summary + reports router | Add PDF export + customer-facing portal |
| Delivery OS | 4 | 5 | 6 modules + stage_machine + event_writer | Validate with 3rd paying customer |
| LLM Gateway | 0 | 4 | not built | Build model_catalog + routing_policy + cost_guard (Phase 2) |
| AI Workforce | 1 | 4 | named agents in docs | Build ComplianceGuardAgent + DeliveryManagerAgent first |
| Demos | 4 | 5 | 3 runnable demos + sample outputs | Record video walkthroughs |
| Sales motion | 3 | 5 | playbook + SOWs + outbound + ROI | First 25 customer outbound campaign |
| Governance | 4 | 5 | 7 governance docs + approval matrix | First DPO appointment by a customer |
| Trust pack | 4 | 5 | 4 trust docs + procurement pack | First procurement-led enterprise RFP response |
| QA Engine | 3 | 5 | qa_review.py (5 gates + 100-pt score) | Run on 3 real customer deliveries |
| Proof Engine | 3 | 5 | proof_pack.py + templates | Capture first 3 real Proof Ledger entries |
| Vertical Playbooks | 2 | 5 | BFSI / Retail / Healthcare drafted in W1.T01 | Validate playbooks with real customers in each vertical |
| Bilingual quality | 4 | 5 | AR companions for 9+ logical doc sets | First customer-facing report reviewed by native AR business reader |
| Client Workspace UI | 1 | 4 | mentioned in roadmap | Build skeletal frontend (Phase 2) |
| Founder Command Center | 2 | 4 | `docs/company/FOUNDER_COMMAND_CENTER.md` template | Wire to live data from event store |

## Promotion rules

- An area cannot be promoted to **Sellable (4)** without ≥ 1 paying customer evidence.
- An area cannot be promoted to **Scalable (5)** without a non-founder delivering it with stable QA across 2+ customers.
- Demotion is automatic when evidence becomes stale (no activity in 90 days) — area drops one level.

## Owner & cadence

- **Owner**: CEO with each area's named owner.
- **Refresh**: monthly in operating cadence.
- **Escalation**: any drop in maturity is a Friday QA-board agenda item.

## Cross-links

- `DEALIX_READINESS.md`
- `docs/company/SERVICE_READINESS_MATRIX.md`
- `docs/product/CAPABILITY_MATRIX.md`
- `docs/strategy/dealix_maturity_and_verification.md` (5-level Maturity Model + 7 Tests)
