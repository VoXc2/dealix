# Capability Blueprint — Revenue Capability

> Canonical template. Each of the 7 capabilities has a blueprint following
> this structure. This is the seed (Revenue) — others (Customer / Operations
> / Knowledge / Data / Governance / Reporting) copy this format.

## Business purpose
Help the customer identify, prioritize, and act on revenue opportunities.

## Typical problems
- Leads scattered across Excel / WhatsApp / CRM.
- CRM not used, or "fields full" but unactionable.
- ICP unclear or undocumented.
- No prioritization between 500 leads.
- Manual follow-up; long sales cycles.
- Pipeline value unclear at month-end.

## Required inputs from customer
- Account or lead list (CSV / CRM export).
- ICP definition (or co-create on Day 1).
- Service offer description (what they sell).
- Current sales stages (or use Dealix default).
- Source attribution for each record.
- Previous outcomes if available (won / lost / no-decision).

## AI functions that build this capability
- Data cleanup + Saudi entity normalization (`data_quality_score.py`).
- ICP scoring (`icp_builder.py`).
- Lead scoring A/B/C/D with explainable features (`lead_scoring.py`).
- Segment recommendation by region / vertical / trigger.
- Outreach draft generation (AR + EN) — drafts only, never auto-send.
- Next-best-action recommendation per top-10 account.
- Revenue report generation (`dealix/reporting/executive_report.py`).

## Governance controls (binding)
- No cold WhatsApp / SMS / LinkedIn automation.
- Source required for every record; missing-source rows are research-only.
- PDPL Art. 13 notice in every outreach draft.
- Per-message human approval before any external send.
- Forbidden-claim filter on all drafts.

## KPIs (measured before/after)
- Accounts scored (count).
- Qualified accounts (score ≥ band-B).
- Data quality improvement (% delta).
- Pipeline value created (SAR).
- Next-actions completed by the customer's sales team.

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — leads scattered; no process.
- **Level 1** — manual list + manual follow-up.
- **Level 2** — pipeline stages documented; one owner.
- **Level 3** — AI scores leads + drafts outreach (Lead Intelligence Sprint).
- **Level 4** — Scoring + approvals + reports + CRM hygiene (Pilot Conversion or Monthly RevOps).
- **Level 5** — Continuous Revenue OS with dashboard, proof, optimization.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to |
|---------|----------------------------|
| Revenue Diagnostic | n/a → measured baseline |
| Lead Intelligence Sprint | L1 → L3 |
| Pipeline Setup | L2 → L3 |
| Pilot Conversion Sprint | L3 → L4 |
| Monthly RevOps OS | L4 → L5 |

## Agents involved (per `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`)
- DataQualityAgent.
- RevenueAgent (scoring).
- OutreachAgent (drafts; never sends).
- ComplianceGuardAgent (mandatory gate).
- ReportingAgent.

## Proof types produced
- **Revenue Proof** — ranked accounts, opportunities identified.
- **Quality Proof** — data quality improvement (before/after).
- **Time Proof** — hours saved per BDR week.

## Cross-links
- `docs/services/lead_intelligence_sprint/`
- `docs/services/ai_ops_diagnostic/offer.md`
- `docs/customer-success/cs_framework.md`
- `docs/customer-success/expansion_playbook.md`

---

## Template for the other 6 capabilities

Use this exact structure for: `customer_capability.md`, `operations_capability.md`, `knowledge_capability.md`, `data_capability.md`, `governance_capability.md`, `reporting_capability.md`. Each file inherits the same 9 sections; only the content changes.
