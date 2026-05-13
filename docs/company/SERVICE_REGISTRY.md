# Dealix Service Registry

Canonical database of every service. One entry per service. Sales,
marketing, and CS read from here — not from emails or proposals.

## How to read this file
- **Status** must equal the value in `SERVICE_READINESS_MATRIX.md`.
- **Sellable** = quote freely from the SOW template.
- **Beta** = pilot only with explicit framing.
- **Designed / Idea / Not Ready** = do not quote; offer the closest Sellable alternative.

---

## Lead Intelligence Sprint

- **Status**: Sellable
- **Pillar**: Grow Revenue
- **Price**: SAR 9,500–18,000
- **Duration**: 10 business days
- **Primary ICP**: B2B services, clinics, logistics, real estate, multi-branch retail
- **Promise**: Turn messy account data into ranked revenue opportunities and safe outreach drafts.
- **Deliverables**: Data quality report · cleaned account list · top 50 ranked accounts · top 10 next actions · outreach draft pack · Mini CRM board · executive report · Proof Pack
- **Required modules**: data_os · revenue_os · governance_os · reporting_os · delivery_os
- **Required gates**: Offer · Delivery · Governance · Demo · Sales
- **SOW**: `templates/sow/revenue_intelligence_sprint.md`
- **Upsell**: Pilot Conversion Sprint / Monthly RevOps OS

## AI Quick Win Sprint

- **Status**: Sellable
- **Pillar**: Automate Operations
- **Price**: SAR 12,000
- **Duration**: 7 business days
- **Primary ICP**: Ops leaders frustrated by recurring manual work
- **Promise**: Automate one painful, recurring process with human-in-the-loop approval.
- **Deliverables**: Live automation · approval workflow · audit log · runbook · 1-hour training · ROI baseline · Proof Pack
- **Required modules**: operations_os (orchestrator) · reporting_os · governance_os
- **SOW**: `templates/sow/ai_quick_win_sprint.md`
- **Upsell**: Workflow Automation Sprint / Monthly AI Ops Retainer

## Company Brain Sprint

- **Status**: Sellable
- **Pillar**: Build Company Brain
- **Price**: SAR 20,000
- **Duration**: 21 business days
- **Primary ICP**: Teams with rich documents and "where is that PDF" pain
- **Promise**: Files → internal AI assistant with cited answers. **Hard rule**: no source = no answer.
- **Deliverables**: Document inventory · PII redaction · RAG index · query interface (≤20 seats) · 3-tier access rules · freshness report · 2-hour training · Proof Pack
- **Required modules**: knowledge_os · governance_os · reporting_os · intake
- **SOW**: `templates/sow/company_brain_sprint.md`
- **Upsell**: Sales Knowledge Assistant / Policy Assistant / Enterprise Company Brain

## AI Support Desk Sprint

- **Status**: Not Ready (Beta candidate after Phase-2 customer_os consolidation)
- **Pillar**: Serve Customers
- **Price (target when ready)**: SAR 12,000–30,000 · 14 days
- **Gating gap**: no demo, no consolidated customer_os module
- **Cross-link**: `docs/services/ai_support_desk_sprint/`

## AI Governance Program

- **Status**: Not Ready (Beta candidate after Phase-3 governance dashboard)
- **Pillar**: Govern AI
- **Price (target when ready)**: SAR 35,000–150,000 · 1–3 months
- **Gating gap**: no demo, no operational governance dashboard yet
- **Cross-link**: `docs/services/ai_governance_program/`

## Workflow Automation Sprint

- **Status**: Designed (Phase 2)
- **Pillar**: Automate Operations
- **Price (target)**: SAR 15,000–50,000 · 2–4 weeks
- **Gating gap**: requires workflow builder + SOP builder in Operations OS Phase 2

## Executive Reporting Automation

- **Status**: Designed (Phase 2)
- **Pillar**: Executive Reporting
- **Price (target)**: SAR 12,000–40,000 setup + SAR 5,000–15,000 / mo

## Monthly RevOps OS (retainer)

- **Status**: Designed (Phase 3 retainer-machine stage)
- **Pillar**: Grow Revenue
- **Price**: SAR 15,000–60,000 / mo
- **Activation rule**: only offered AFTER a Sellable Sprint has been delivered to the customer.

## Monthly AI Ops (retainer)

- **Status**: Designed (Phase 3)
- **Pillar**: Automate Operations / Build Company Brain
- **Price**: SAR 15,000–60,000 / mo
- **Activation rule**: same as Monthly RevOps OS — post-Sprint only.

## Enterprise AI OS

- **Status**: Idea (Phase 4)
- **Pillar**: Enterprise AI OS
- **Price (target)**: SAR 85,000–300,000+ setup + SAR 35,000–150,000 / mo
- **Activation rule**: requires 10+ paid Sprints + 3+ retainers + zero governance incidents per `docs/enterprise/ENTERPRISE_READINESS.md` (when published).

## Owner & cadence

- **Owner**: CEO + CRO co-own.
- **Refresh**: weekly with Service Readiness Matrix.
- **Authority**: only Sellable services may be quoted. Promotion from Designed → Beta → Sellable requires evidence in the readiness matrix.
