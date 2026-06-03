# Market Production OS — Naming Conventions & Canonical IDs

The single source of truth for IDs and enums used across schemas, data, scripts,
and tests. Changing a value here means updating data + tests together.

## File & doc conventions
- Arabic-first operating docs end in `_AR.md`; English mirrors end in `_EN.md`.
- Reports are UPPER_SNAKE `.md` under `reports/<area>/`.
- Machine data: `data/<area>/<name>.{yaml,jsonl}`. Catalogs/config = YAML; record
  streams (drafts, signals, prospects, suppression) = JSONL (one JSON object/line).
- Schemas: `schemas/<entity>.schema.json` (JSON Schema draft 2020-12).

## Product offer IDs (the ladder)
| ID | Name | Price range (SAR) | Live alias |
|----|------|-------------------|-----------|
| `DLX-L0` | Readiness Scan | free / low-friction | — |
| `DLX-L1` | Revenue Leakage Diagnostic | 1,500–5,000 | **P1** (Revenue Intelligence Sprint) |
| `DLX-L2` | Follow-up Recovery Workflow | 8,000–18,000 | — |
| `DLX-L3` | AI Revenue Ops Starter | 18,000–35,000 | — |
| `DLX-L4` | Full Revenue OS | 35,000–90,000 | — |
| `DLX-L5` | Monthly Optimization Retainer | 3,000–15,000/mo | **P2** (AI Sales Ops Retainer) |
| `DLX-L6` | Custom Company OS | 90,000+ | — |

## Problem categories (`pain_category`)
`lead_leakage` · `follow_up_chaos` · `crm_data_disorder` · `proposal_delay` ·
`weak_reporting` · `sales_team_inconsistency` · `support_overload` ·
`no_proof_case_study_system` · `slow_onboarding` · `weak_renewal_upsell`

## ICP segment IDs (`sector`)
`marketing_agencies` · `training_companies` · `clinics` · `real_estate_teams` ·
`recruitment_agencies` · `professional_services` · `education_providers` ·
`logistics_companies` · `restaurant_groups` · `local_saas`

## Buyer persona IDs
`founder_owner` · `ceo_gm` · `head_of_sales` · `marketing_manager` ·
`operations_manager` · `support_manager` · `training_admissions_manager` ·
`clinic_manager` · `agency_owner` · `crm_sales_ops_manager`

## Pipeline stages (`stage`) — ordered
`signal_detected` → `researched` → `qualified` → `drafted` → `approved_for_outreach`
→ `contacted` → `replied` → `discovery_scheduled` → `discovery_completed` →
`proposal_needed` → `proposal_sent` → `negotiation` → `payment_handoff` → `won` →
`delivery_handoff` → `active_delivery` → `renewal_candidate` → `renewed`
Terminal/side: `lost` · `nurture` · `do_not_contact`

## Personalization tiers (`personalization_score`)
`P0` sector only · `P1` company+sector · `P2` company+signal/pain · `P3` specific
trigger · `P4` specific proof/offer alignment. **Floor for approval queue = P1.**

## Evidence levels (`evidence_level`)
`none` · `assumed` · `observed` · `verified`. Claims must cite the highest honest level.

## Risk levels (`risk_level`)
`low` · `medium` · `high`. Pricing, data-handling, and external sends default ≥ `high`.

## Draft types (`draft_type`) and daily mix
`first_touch` (100) · `follow_up_1` (75) · `follow_up_2` (50) · `proposal_intro` (15)
· `close_loop` (10) = **250/day**.

## Approval status (`approval_status`)
`pending` · `approved` · `rejected` · `needs_revision`. Default `pending`.

## Send status (`send_status`)
`not_sent` · `queued_plan` · `approved_for_send` · `sent` · `suppressed` · `bounced`.
Default `not_sent`. Real send requires deliverability verdict ≥ `LIMITED_SEND_READY`.

## Deliverability verdicts
`NOT_READY` · `DRY_RUN_ONLY` (default) · `LIMITED_SEND_READY` · `RAMP_READY` ·
`PAUSE_REQUIRED`.

## Prospect score rubric (max 100)
`sector_fit` 20 · `buying_signal` 20 · `likely_lead_flow` 15 ·
`decision_maker_clarity` 15 · `payment_ability` 15 · `personalization_signal` 10 ·
`risk_low` 5.
