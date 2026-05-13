---
doc_id: company.ip_registry
title: Dealix IP Registry — Owned Intellectual Property Catalog
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
---

# Dealix IP Registry

> Dealix's long-term moat is not the services it sells, it is the
> compounding library of methods, templates, playbooks, datasets,
> standards, software, and training material it owns and refines. This
> registry is the single source of truth for what Dealix owns.

## Why this file exists

Every compounded asset (per `COMPOUNDING_SYSTEM.md`) eventually graduates
into IP. Without a registry the IP becomes invisible; with it, the IP
becomes sellable, citable, defendable in RFPs, and trainable for new
hires and partners.

## IP catalog

| Type | Asset | Description | Used In | Status |
|------|-------|-------------|---------|--------|
| Methodology | Dealix Method | 8-stage Delivery Standard (Intake → Diagnose → Design → Prepare → Ship → Govern → Prove → Expand) | Every project | Active |
| Methodology | Capability Operating Model | 7 customer capabilities x 5 maturity levels | Every Sprint scope | Active |
| Template | Proof Pack v6 | Bilingual, consent-gated, HMAC-signed evidence package | Stage 7 of every project | Active |
| Template | SOWs (3) | Revenue Sprint, Quick Win, Company Brain SOWs in `templates/sow/` | Every quote | Active |
| Template | Executive Report | Weekly CEO/sales/ops report skeleton (`dealix/reporting/executive_report.py`) | Reporting Automation, retainers | Active |
| Template | Capability Roadmap | Per-client 7-capability assessment + sprint/retainer/enterprise path | Every paying customer | Active |
| Playbook | Saudi Verticals | B2B Services, Clinics, Logistics, Real Estate, Multi-Branch Retail playbooks in `docs/playbooks/` | Sales targeting, sprint scoping | Active (5 written) |
| Playbook | Objection Handling v6 | 12-objection bilingual handler | Every sales call | Active |
| Dataset | Anonymized Benchmarks | Aggregated lead conversion, hours-saved, QA scores per sector | Annual Saudi AI Operations Benchmark report | Building |
| Dataset | Proof Ledger | Cross-project before/after measurements | Sales reframe + pricing power | Active |
| Standard | 8 Dealix Standards | Data Ready / Process Clear / Human Approved / Source Grounded / Quality Scored / Governance Checked / Proof Delivered / Expansion Planned | Every delivery gate | Active |
| Standard | 100-Point QA Score | 5-gate QA in `auto_client_acquisition/delivery_factory/qa_review.py` | Every output | Active |
| Standard | 11-Gate Readiness System | Gate sequence from Offer to Sales | Service promotion Designed → Sellable | Active |
| Software | 10 AI Agents | DataQuality, Revenue, Outreach, Support, Knowledge, Workflow, Reporting, ComplianceGuard, DeliveryManager, Strategy | Inside every Sprint and retainer | 7 MVP / 2 Beta / 1 Designed |
| Software | 9 OS Modules | Intake, Data, Revenue, Customer, Operations, Knowledge, Governance, Reporting, Delivery Factory | Internal engine room | 6 live / 2 Phase-2 / 1 Phase-3 |
| Software | LLM Gateway | Routed, cost-bounded model calls per `AI_MODEL_ROUTING_STRATEGY.md` | Every AI call | Active |
| Training | Dealix Academy curriculum | 5 courses + Certified AI Ops Practitioner exam | External partners + customers | Planned (gate: 10 projects + 3 case studies) |
| Brand | Category Claim | "AI Operating Partner" — see `CATEGORY_DESIGN.md` | All marketing, all proposals | Active |

## Ownership rules

1. Every asset above has a named owner (CEO unless reassigned).
2. No external delivery may rely on an asset whose Status is not `Active` or `Beta`.
3. Promotion from `Building` to `Active` requires 3 supervised uses + a
   QA score of 85+ on the artifacts produced from it.
4. IP is logged in `docs/ledgers/PRODUCT_LEDGER.md` and reviewed quarterly.

## Cross-links

- `docs/company/COMPOUNDING_SYSTEM.md` — how IP is produced project by project
- `docs/company/ASSET_GRADUATION_SYSTEM.md` — stages from raw output to market asset
- `docs/company/DEALIX_STANDARD.md` — the 8 standards
- `docs/strategy/FROM_SERVICE_TO_STANDARD.md` — IP roadmap by company stage
- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — method detail
- `docs/product/AI_AGENT_INVENTORY.md` — agent catalog
- `docs/product/internal_os_modules.md` — OS module catalog
