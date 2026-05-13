# Dealix Company Readiness Scorecard

The single, canonical "are we ready?" checklist. Run weekly in the operating
cadence (W5.T30). Automated by `scripts/verify_company_ready.py`.

## How to use
```bash
python scripts/verify_company_ready.py
```
Exit code 0 = ready, non-zero = blockers exist (printed line-by-line).

## Five-category readiness

### 1. Company readiness
- [x] Positioning clear → `docs/strategy/dealix_operating_partner_positioning.md`
- [x] Service catalog ready → `docs/strategy/service_portfolio_catalog.md`
- [x] Pricing ready → `docs/pricing/pricing_packages_sa.md`
- [x] ICP ready → `docs/go-to-market/icp_saudi.md`
- [x] Operating principles → `docs/company/OPERATING_PRINCIPLES.md`
- [x] Maturity model → `docs/strategy/dealix_maturity_and_verification.md`

### 2. Service readiness (3 starting offers)
For each of `lead_intelligence_sprint` / `ai_quick_win_sprint` / `company_brain_sprint`:
- [x] `offer.md`
- [x] `scope.md`
- [x] `intake.md`
- [x] `qa_checklist.md`
- [x] `proof_pack_template.md`
- [x] SOW template in `templates/sow/`

### 3. Product readiness (5 Phase-1 OS modules)
- [x] Delivery OS — 8 files in `auto_client_acquisition/delivery_factory/`
- [x] Data OS gap-fills — `customer_data_plane/{validation_rules,data_quality_score,pii_detection}.py`
- [x] Governance OS gap-fills — `dealix/trust/{pii_detector,forbidden_claims,approval_matrix}.py`
- [x] Reporting OS — `dealix/reporting/`
- [x] Revenue OS extensions — `lead_scoring`, `icp_builder`, `roi_calculator`, `POST /seed`, `POST /leads/rank`

### 4. Delivery readiness
- [x] 3 runnable demos — `demos/{revenue_intelligence,ai_quick_win,company_brain}_demo.py`
- [x] Sample data — `demos/data/sample_saudi_accounts.csv`
- [x] 8-stage state machine — `delivery_factory/stage_machine.py`
- [x] Event store wiring — `delivery_factory/event_writer.py`
- [x] Outbound message templates — `templates/outbound_messages.md`

### 5. Trust readiness
- [x] PII detection — `customer_data_plane/pii_detection.py` + `dealix/trust/pii_detector.py`
- [x] Forbidden claims filter — `dealix/trust/forbidden_claims.py`
- [x] Approval matrix — `dealix/trust/approval_matrix.py`
- [x] Audit / event store — `auto_client_acquisition/revenue_memory/event_store.py` + delivery events in taxonomy
- [x] Source attribution — every Data OS record carries `source`; quality score downgrades records without it

## The single Final Test Question (from W6.T37 §13)

> **"Can I hand this service to a new customer at the same quality, in the
> same timebox, with the same report / proof / QA, without the founder being
> the bottleneck?"**

Today's answer (one of): not_yet · pilot · yes · scaling.

## Owner & cadence
- **Owner**: CEO.
- **Review**: weekly with HoCS + CTO.
- **Escalation**: any FAIL category opens a Monday-review item until cleared.
