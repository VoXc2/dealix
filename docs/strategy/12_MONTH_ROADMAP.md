---
doc_id: strategy.12_month_roadmap
title: Dealix 12-Month Roadmap — Q1 to Q4 Milestones
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal, board]
language: en
---

# 12-Month Roadmap

> Quarter-by-quarter milestones: logos, MRR, modules shipped, content.
> Long-form 2026 strategy in `docs/STRATEGIC_MASTER_PLAN_2026.md`.
> 90-day plan in `docs/strategy/90_DAY_PLAN.md`. 12-month GTM in
> `docs/go-to-market/saudi_gtm_12m.md`.

## Headline numbers (annual target)

| Indicator | Target by 2026-12-31 |
|-----------|----------------------|
| Paying customers (cumulative) | **20 logos** |
| MRR (end of Q4) | **SAR 300,000** (~ SAR 3.6M ARR) |
| Pipeline (cumulative) | **SAR 100M** |
| Closed-won (cumulative) | **SAR 20M** |
| OS modules in production | **8 / 8** (all shared modules live) |
| Active partners | **8+** (90d KPI maintained or grown) |
| Productized revenue share | **≥ 80%** |
| Quality Score floor | **≥ 80** on 100% of projects |

## Q1 — Foundation & first anchors (Months 1–3)

**Logos goal:** 2 anchor logos (1 BFSI + 1 Retail OR Healthcare).
**MRR goal:** SAR 30,000 (2 retainers).
**Pipeline goal:** SAR 15M cumulative; SAR 1.5M closed.

**Engineering milestones (5 modules live):**
- Data OS, Revenue OS, Governance OS, Reporting OS, Delivery OS.
- Lead Engine in production with ≥ 25 Saudi data sources.
- 5-gate Quality System operational; 8-stage Delivery Standard wired.

**Commercial milestones:**
- 3 starting offers operating (sprint factory).
- ABM playbook on 50 Tier-1 accounts.
- 6 published bilingual content pieces.
- 1 industry conference (LEAP or Money 20/20 Riyadh) + 2 roundtables.

**Hiring (cumulative):** Enterprise AE #1 (BFSI), SDR #1, CS Lead,
Marketing manager.

**Channel mix:** outbound 60% / events 25% / inbound 15%.

## Q2 — Repeatability (Months 4–6)

**Logos goal:** 4 more (cumulative **6**); 2 paid pilots converted.
**MRR goal:** SAR 80,000.
**Pipeline goal:** SAR 30M cumulative; SAR 4M closed.

**Engineering milestones (7 of 8 modules):**
- Customer OS (consolidation done) + Knowledge OS depth + Operations OS.
- Multi-tenant hardening (`tenant_id` row-level isolation per
  `docs/adr/0003-multi-tenant-isolation.md`).
- Audit-export endpoint (`GET /api/v1/audit/export`) for procurement.
- A/B framework live; first 3 winning variants in sales sequences.

**Commercial milestones:**
- 2 channel partners signed (1 SI + 1 sectoral reseller).
- Sales enablement v1 launched; 100% rep certification.
- Bilingual ROI model adoption per deal.
- Procurement pack used in 100% of enterprise opps.
- AI Support Desk and Company Brain sprints proven (≥ 1 customer each).
- First Vertical Playbook published (BFSI).

**Hiring:** AE #2 (Retail focus), Partner manager.

**Channel mix:** outbound 50% / partner 20% / events 15% / inbound 15%.

## Q3 — Expansion (Months 7–9)

**Logos goal:** 6 more (cumulative **12**); first land-and-expand.
**MRR goal:** SAR 180,000.
**Pipeline goal:** SAR 60M cumulative; SAR 10M closed.

**Engineering milestones (8 of 8 modules):**
- Strategy OS + Marketing OS launched (Phase 3 of 90-day plan).
- Self-serve onboarding for SME tier live (Starter).
- SLA dashboard live per `docs/sre/slo_framework.md`.
- Sovereign-tier single-tenant deployment proven (1 customer).

**Commercial milestones:**
- Open Jeddah field presence (1 AE remote + monthly visits).
- Healthcare vertical at full ramp.
- First customer summit (15–25 Saudi customers in person, Riyadh).
- 3 case studies published; bilingual landing site refresh.
- Begin Vision 2030 alignment narrative on Dealix.sa.

**Hiring:** SDR #2 (Jeddah), AE #3 (Healthcare), DPO / Trust officer.

**Channel mix:** outbound 40% / partner 30% / events 15% / inbound 15%.

## Q4 — Scale (Months 10–12)

**Logos goal:** 8 more (cumulative **20**); 2 multi-year enterprise
renewals.
**MRR goal:** SAR 300,000.
**Pipeline goal:** SAR 100M cumulative; SAR 20M closed.

**Engineering milestones:**
- Enterprise AI OS reference implementation deployed (1 logo).
- Full multi-tenant partner portal (auto-provisioned tenants).
- Public Trust Center (procurement pack auto-served).
- Decision Passport public attestation API (read-only).

**Commercial milestones:**
- Second customer summit.
- 5 public reference customers / quotable logos.
- 24 published bilingual content pieces (cumulative).
- Begin GCC expansion scoping (UAE / Bahrain via Saudi anchors'
  subsidiaries).
- 2 enterprise multi-year renewals.

**Hiring:** SE / Solutions consultant.

**Channel mix:** outbound 35% / partner 30% / events 15% / inbound 20%.

## Year-end gates (binding)

- NRR ≥ 110% by Month 12.
- Productized revenue share ≥ 80% by Month 12.
- Gross Margin ≥ 65% by Month 18 (Q4 trending).
- ≥ 3 of 5 customer pillars with paying customers by Month 9; all 5 by
  Month 18.
- Zero PDPL enforcement incidents; zero forbidden-claim violations in
  production.

## Funding & spend (cumulative)

- Q1 budget: SAR 2.5M (people 60% / events 20% / marketing 15% / tools 5%).
- Q2–Q4 each: SAR 3M baseline; + SAR 1M if Q-1 pipeline target met.
- Hiring gate: do not hire AE #N+1 unless AE #N has SAR 3M closed in
  trailing 6 months.

## Risks and mitigations

1. **Hiring slip.** Mitigation: partner program (Q2) absorbs sales
   capacity; SI partners deliver implementation.
2. **PDPL incident.** Mitigation: Approval Matrix + forbidden claims +
   Decision Passport on every action; DPO hired Q3.
3. **Enterprise procurement cycles slip past Q4.** Mitigation: Sprint +
   retainer model self-funds the company; enterprise is upside.
4. **LLM cost overruns.** Mitigation: FinOps gates per
   `docs/finops/model_cost_governance.md`; per-workflow cost ceiling.

## Cross-links

- 2026 strategic master plan: `docs/STRATEGIC_MASTER_PLAN_2026.md`
- 12-month GTM (W2.T04): `docs/go-to-market/saudi_gtm_12m.md`
- 90-day execution: `docs/strategy/90_DAY_PLAN.md`
- Master 90-day plan: `/root/.claude/plans/mighty-plotting-moore.md`
- Saudi 30-task master plan (W0.T00): `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- North-star metrics: `docs/company/NORTH_STAR_METRICS.md`
- Business model: `docs/company/BUSINESS_MODEL.md`
- Partnerships: `docs/strategy/PARTNERSHIPS.md`
- Executive KPI spec (W4.T13): `docs/analytics/executive_kpi_spec.md`
- ADR set: `docs/adr/`
