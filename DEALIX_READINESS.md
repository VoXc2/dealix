# Dealix Readiness — 11 Stage Gates

The single source of truth for "are we ready to sell, deliver, and scale?"
Every Monday in the operating cadence (W5.T30), this file is updated based
on `python scripts/verify_dealix_ready.py`. Each gate is binary
(PASS / FIX / DO-NOT-SELL) — no "almost".

> **Rule**: Sales is unlocked when Gates 0 / 1 / 2 / 4 / 5 / 6 all pass.
> Product Readiness (Gate 3) does not need to be complete — MVP is enough.

## Gate scorecard (auto-generated)

| Gate | Name | Status | Notes |
|------|------|--------|-------|
| 0 | Founder Clarity | PASS | Positioning + ICP + Mission/Vision + Operating Principles + North Star Metric all present (`docs/company/`). |
| 1 | Offer Readiness | PASS | 3 starting offers (Lead Intel / AI Quick Win / Company Brain) have full service folders with offer/scope/intake/QA/proof pack/sample output/upsell. |
| 2 | Delivery Readiness | PASS | Delivery Standard + Lifecycle + Onboarding + Scope Control + Change Request + Handoff + Renewal docs all in `docs/delivery/`. |
| 3 | Product Readiness | PASS-MVP | 5 OS modules live: Data / Revenue / Governance / Reporting / Delivery. Customer / Knowledge / Marketing OS are Phase 2/3. |
| 4 | Governance Readiness | PASS | Compliance Perimeter + PDPL Rules + Approval Matrix + PII Redaction + Audit Log + Forbidden Actions all in `docs/governance/`. |
| 5 | Demo Readiness | PASS | 3 runnable demos in `demos/` + sample executive reports per service. |
| 6 | Sales Readiness | PASS | Sales Playbook + Outbound Messages + SOW templates + ROI Calculator + Persona Matrix + Objection Bank. |
| 7 | Client Delivery Readiness | PASS | Client onboarding pack + welcome flow + handoff process documented. |
| 8 | Retainer Readiness | FIX | Monthly RevOps + Monthly AI Ops scopes exist; need first sprint-to-retainer conversion before promoting publicly. |
| 9 | Scale Readiness | FIX | 8-stage Delivery Standard + 5-gate QA + ProjectState machine in place; verify with 3rd customer that delivery doesn't depend on the founder. |
| 10 | World-Class Readiness | FIX | Targets: 10+ paid projects · 3+ retainers · 5 strong proof packs · 3 vertical playbooks · QA avg ≥ 90 · 0 PII incidents · 95% on-time · 3 case studies. None yet — pre-revenue. |

## Sales unlock decision

**Gates 0 + 1 + 2 + 4 + 5 + 6 all PASS → SALES IS UNLOCKED.**

Currently sellable services (officially):
1. Lead Intelligence Sprint — SAR 9,500
2. AI Quick Win Sprint — SAR 12,000
3. Company Brain Sprint — SAR 20,000

Do NOT sell yet (Gate 1 not met):
- Workflow Automation Sprint (Phase 2)
- Executive Reporting Automation (Phase 2)
- Monthly retainers as a standalone first-sale (require proven Sprint outcome first)
- Enterprise AI OS (Phase 4)

## Gate-by-gate detail

### Gate 0 — Founder Clarity
**Required files** (all present):
- `docs/company/POSITIONING.md`
- `docs/company/MISSION_VISION.md`
- `docs/company/OPERATING_PRINCIPLES.md`
- `docs/company/ICP.md`
- `docs/company/NORTH_STAR_METRICS.md`

**Pass criteria**: founder can explain Dealix in 20 seconds; 3 starting offers defined; primary ICP defined; North Star metric defined.

### Gate 1 — Offer Readiness
**For each of 3 starting offers**, required folder + 10 files:
- `offer.md`, `scope.md`, `intake.md`, `data_request.md`, `delivery_checklist.md`, `qa_checklist.md`, `report_template.md`, `proof_pack_template.md`, `sample_output.md`, `upsell.md`.

**Score per offer ≥ 85/100** using the rubric in `docs/quality/SERVICE_READINESS_SCORE.md`.

### Gate 2 — Delivery Readiness
**Required files** (all present in `docs/delivery/`):
- DELIVERY_STANDARD.md · DELIVERY_LIFECYCLE.md · CLIENT_ONBOARDING.md · SCOPE_CONTROL.md · CHANGE_REQUEST_PROCESS.md · HANDOFF_PROCESS.md · RENEWAL_PROCESS.md.

**Pass criteria**: every service has a delivery checklist, timeline, named owner, scope control rules, and handoff packet.

### Gate 3 — Product Readiness (MVP acceptable)
**5 OS modules required at MVP**:
- Data OS — `auto_client_acquisition/customer_data_plane/{validation_rules, data_quality_score, pii_detection}.py`.
- Revenue OS — `auto_client_acquisition/revenue_os/{lead_scoring, icp_builder, roi_calculator}.py`.
- Governance OS — `dealix/trust/{pii_detector, forbidden_claims, approval_matrix}.py`.
- Reporting OS — `dealix/reporting/{executive_report, proof_pack, weekly_summary}.py`.
- Delivery OS — `auto_client_acquisition/delivery_factory/{client_intake, scope_builder, qa_review, delivery_checklist, client_handoff, renewal_recommendation, stage_machine, event_writer}.py`.

### Gate 4 — Governance Readiness
**Required files**: COMPLIANCE_PERIMETER · PDPL_DATA_RULES · APPROVAL_MATRIX · FORBIDDEN_ACTIONS · PII_REDACTION_POLICY · AUDIT_LOG_POLICY · DATA_RETENTION (all in `docs/governance/`).

**Hard rules enforced in code**: `dealix/trust/forbidden_claims.py` (claims blocker), `dealix/trust/pii_detector.py` (PII gate), `dealix/trust/approval_matrix.py` (action × evidence → approver).

### Gate 5 — Demo Readiness
**Required**: 3 runnable demos in `demos/` (revenue_intelligence_demo.py, ai_quick_win_demo.py, company_brain_demo.py) each runnable in ≤10 minutes from a sample seed; sample executive report per service.

### Gate 6 — Sales Readiness
**Required**: SALES_PLAYBOOK · DISCOVERY_SCRIPT · offer pages · OBJECTION_HANDLING · SOW templates (3) · outbound messages · ROI calculator · persona-value matrix.

### Gate 7 — Client Delivery Readiness
**Required**: client onboarding pack, welcome message, data request templates, project timeline, RACI, review-call agenda, approval process.

### Gate 8 — Retainer Readiness
**Required**: Monthly RevOps OS scope + Monthly AI Ops scope + monthly report cadence + client health score + renewal process. **Status**: documented but not yet validated with a real retainer customer.

### Gate 9 — Scale Readiness
**Required**: templates reusable + checklists reusable + QA process documented + modules reduce manual work + another team member can deliver with the system + reports partly auto-generated + proof packs standardized.

### Gate 10 — World-Class Readiness
**Targets**: 10+ paid projects · 3+ retainers · QA avg ≥ 90 · 0 PII incidents · 95% on-time delivery · 3 vertical playbooks · 5 strong proof packs · 3 case studies · client workspace MVP · Dealix Method documented and publicly visible.

## How to refresh this file

```bash
python scripts/verify_dealix_ready.py > /tmp/dealix_ready.txt
# Manually update the scorecard above based on the output.
```

## Owner & cadence

- **Owner**: CEO.
- **Refresh**: weekly Monday in operating cadence (W5.T30).
- **Escalation**: any gate flipping from PASS to FIX is a Monday-review blocker.
