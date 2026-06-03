# Market Production OS — File Map

The canonical index of the Market + Commercial layer. Paths are relative to the
repo root. Status: `live` = present & maintained here, `seed` = pre-existing asset
reused, `protected` = must not be overwritten (see audit §12).

## docs/gtm — Foundation & command room
- `MARKET_PRODUCTION_OS_AR.md` — master system definition
- `MARKET_PRODUCTION_SYSTEM_BOUNDARIES.md` — trust boundaries
- `MARKET_PRODUCTION_FILE_MAP.md` — this file
- `MARKET_PRODUCTION_NAMING_CONVENTIONS.md` — IDs & vocabulary
- `FOUNDER_GTM_COMMAND_CENTER_AR.md` — founder control room
- `GTM_OPERATING_RHYTHM_AR.md` — daily/weekly rhythm
- `GTM_METRICS_AR.md` — metric definitions

## docs/brand — Brand OS
`BRAND_IDENTITY_SYSTEM_AR` · `BRAND_MESSAGING_HOUSE_AR` · `BRAND_VISUAL_DIRECTION_AR` ·
`BRAND_VOICE_AR` · `BRAND_CLAIMS_POLICY_AR` · `BRAND_OUTBOUND_SYSTEM_AR` ·
`BRAND_CONTENT_RULES_AR` · `BRAND_ASSET_CHECKLIST_AR`

## docs/commercial — Catalog, ICP, sales
Catalog: `PRODUCT_CATALOG_AR` · `OFFER_LADDER_AR` · `PACKAGING_STRATEGY_AR` ·
`SCOPE_AND_OUT_OF_SCOPE_AR` · `DELIVERABLES_LIBRARY_AR` · `PRICING_GUARDRAILS_AR` ·
`DISCOUNT_POLICY_AR` · `PAYMENT_TERMS_AR` · `QUOTE_APPROVAL_POLICY_AR`
ICP: `ICP_MATRIX_AR` · `MARKET_SEGMENTATION_AR` · `BUYER_PERSONAS_AR` ·
`DISQUALIFICATION_RULES_AR` · `PAIN_TO_OFFER_MATRIX_AR` · `OFFER_MATCHING_RULES_AR` ·
`PROBLEM_CATEGORY_MAP_AR`
Sales: `SALES_PROCESS_AR` · `PIPELINE_STAGES_AR` · `QUALIFICATION_RULES_AR` ·
`DISCOVERY_PROCESS_AR` · `NEXT_STEP_RULES_AR` · `PROPOSAL_STRATEGY_AR` ·
`PROPOSAL_APPROVAL_POLICY_AR` · `PROOF_PACK_COMMERCIAL_GUIDE_AR` · `CASE_STUDY_POLICY_AR` ·
`OBJECTION_BANK_AR` · `SALES_ENABLEMENT_PLAYBOOK_AR` · `COMPETITOR_POSITIONING_AR` ·
`ROI_CONVERSATION_GUIDE_AR` · `RISK_REVERSAL_POLICY_AR` · `COMMERCIAL_RISK_REGISTER_AR` ·
`WALK_AWAY_RULES_AR` · `BAD_FIT_CLIENT_POLICY_AR` · `SCOPE_CREEP_POLICY_AR`

## docs/sectors — 10 playbooks
`MARKETING_AGENCIES_AR` · `TRAINING_COMPANIES_AR` · `CLINICS_AR` · `REAL_ESTATE_TEAMS_AR` ·
`RECRUITMENT_AGENCIES_AR` · `PROFESSIONAL_SERVICES_AR` · `EDUCATION_PROVIDERS_AR` ·
`LOGISTICS_COMPANIES_AR` · `RESTAURANT_GROUPS_AR` · `LOCAL_SAAS_AR`

## docs/signals & docs/outreach
Signals: `SIGNAL_DETECTION_OS_AR` · `JOB_SIGNAL_PLAYBOOK_AR` · `WEBSITE_SIGNAL_PLAYBOOK_AR` ·
`EXPANSION_SIGNAL_PLAYBOOK_AR` · `CONTENT_SIGNAL_PLAYBOOK_AR`
Outreach: `PROSPECT_RESEARCH_OS_AR` · `COLD_EMAIL_DRAFT_FACTORY_AR` ·
`PERSONALIZATION_RULES_AR` · `COLD_EMAIL_SEQUENCES_AR/EN` · `OUTBOUND_RISK_GATES_AR` ·
`DRAFT_REJECTION_REASONS_AR` + deliverability/compliance set (see docs/outreach)

## docs/content · docs/press · docs/partnerships · docs/privacy · docs/evals
See each directory; tracked in the gap matrix.

## schemas/ (JSON Schema 2020-12)
`product_offer` · `pricing_rule` · `icp` · `buyer_persona` · `pain_signal` ·
`offer_match` · `company_signal` · `job_signal` · `prospect` · `outreach_draft` ·
`email_account` · `sending_batch` · `suppression` · `partner_opportunity` ·
`content_asset` · `opportunity` · `discovery_note` · `commercial_proposal` ·
`commercial_proof_pack`

## data/ (source of truth)
`commercial/` (product_catalog.yaml, pricing_rules.yaml, icp_segments.yaml,
buyer_personas.yaml, pain_to_offer.yaml, objections.yaml, opportunities.jsonl,
discovery_notes.jsonl) · `sectors/sectors.yaml` · `signals/*.jsonl` ·
`prospects/*.jsonl` · `outreach/*.jsonl` · `content/post_ideas.jsonl` ·
`partners/partner_opportunities.jsonl` · `evals/*.jsonl`

## scripts/ (executable, Node — fixes broken commercial:* npm scripts)
`commercial-control-check.js` · `commercial-daily-plan.js` · `draft-quality-gate.js` ·
`commercial-daily-brief.js` · `_lib/dealix.js` (shared loaders)

## tests/ (pytest)
`test_gtm_quality_gate` · `test_outreach_no_guaranteed_claims` ·
`test_outreach_unsubscribe_required` · `test_outreach_suppression_blocks_send` ·
`test_commercial_offer_mapping` · `test_pricing_requires_approval` ·
`test_no_guaranteed_revenue_claims` · `test_proposal_requires_qualified_opportunity` ·
`test_walk_away_rules` · `test_partner_model_margin_rules`

## Protected (never overwrite)
`company_os/governance/*` · `company_os/company_os/**` (stale dup) ·
`company_os/revenue/*` · `src/**` · `api/**` · `db/**` · `contracts/**` ·
`package-lock.json` · existing `scripts/*.py`
