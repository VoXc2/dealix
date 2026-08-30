# Dealix Universal Market Radar — Working Templates V1

Parent: #1403  
Owner model: existing Company Brain + Market Intelligence + Portfolio Router + Governance + Proof owners only.  
Authority: internal research/drafting only unless an existing canonical downstream gate grants a specific action.

## Universal truth header

Every artifact below must declare:

```yaml
artifact_id:
schema_version:
generated_at:
source_sha:
market:
company_or_subject:
source_refs: []
evidence_refs: []
fresh_until:
facts: []
inferences: []
unknowns: []
risk_class:
authority_class: INTERNAL_RESEARCH_OR_PREPARATION_ONLY
next_evidence: []
next_action:
```

Rules:
- `research != relationship`
- `public contact != consent`
- `signal score != purchase probability`
- `draft != sent`
- `proposal != revenue`
- `invoice != payment`
- `provider acceptance != delivery`
- `technical PASS != customer value`
- `synthetic/demo != customer proof`
- missing evidence = `UNKNOWN_NOT_EVIDENCE_BACKED`

---

## 1. Sector playbook

```yaml
sector_family:
operating_cluster:
priority_tier:
market_context:
  official_sources: []
  freshness:
business_archetypes: []
pain_taxonomy: []
buyer_map:
  economic_buyer: []
  workflow_owner: []
  technical_buyer: []
  trust_or_procurement: []
source_map: []
regulatory_and_policy_profile: []
evidence_required_before_qualification: []
package_hypotheses: []
company_brain_workflow_packs: []
channel_hypotheses: []
event_partner_routes: []
proof_methods: []
known_unknowns: []
priority_factors:
  economic_pain:
  measurable_outcome:
  buyer_access:
  data_availability:
  repeatability:
  readiness:
  distribution_density:
  regulatory_friction:
  integration_complexity:
  founder_minutes:
next_evidence:
experiment:
  hypothesis:
  baseline_ref:
  target_metric:
  stop_rule:
```

---

## 2. Account dossier

```yaml
account_id:
company_name:
sector_family:
business_archetype:
market:
source_refs: []
observed_signals:
  - signal_family:
    observed_at:
    evidence_ref:
    fact:
company_context:
  products_services:
  operating_model:
  geography:
  technology_context:
  current_change_or_trigger:
likely_pains: []
buyer_hypotheses:
  - role:
    why_this_role:
    evidence_ref:
package_hypotheses: []
workflow_hypotheses: []
relationship_state: UNKNOWN_NOT_EVIDENCE_BACKED
consent_state: UNKNOWN_NOT_EVIDENCE_BACKED
risk_class:
missing_evidence: []
next_evidence:
next_action: RESEARCH_ONLY_UNTIL_CANONICAL_INTERACTION_OR_INBOUND
```

Never turn a public person, email, job title, event attendee, exhibitor listing, CRM row or social interaction into a relationship.

---

## 3. Event target card

```yaml
event_id:
event_name:
company_name:
booth_or_location:
priority_reason:
source_refs: []
company_snapshot:
likely_problem_hypothesis:
likely_buyers: []
package_hypothesis:
three_questions:
  -
  -
  -
interaction_state: RESEARCH_TARGET_ONLY
interaction_receipt_required:
  counterparty_ref: true
  timestamp: true
  event_or_channel_source: true
  substantive_two_way_context: true
  pain_or_goal: true
  follow_up_permission_state: true
post_interaction_next_evidence:
```

Success = a small number of substantive real conversations with receipts, not list volume.

---

## 4. Tender / procurement brief

```yaml
tender_id:
source_id:
source_ref:
observed_at:
deadline:
buyer_entity:
sector_family:
summary:
requirements:
  mandatory: []
  scored_or_optional: []
submission_constraints: []
required_documents: []
evidence_matrix:
  - requirement:
    evidence_ref:
    status: VERIFIED_OR_GAP
unknowns: []
fit_hypothesis:
package_or_partner_hypothesis:
risk_and_legal_review: REQUIRED_AS_APPLICABLE
next_evidence:
next_action: INTERNAL_PREPARATION_ONLY
```

The radar may discover and brief a tender. It may not submit, bid, price, sign or claim government access.

---

## 5. Competitor battlecard

```yaml
competitor:
market:
source_refs: []
last_verified_at:
positioning:
target_buyers:
claims_observed: []
products_or_workflows_observed: []
pricing_observed:
  state: PUBLIC_OBSERVATION_ONLY
  source_ref:
strengths: []
weakness_hypotheses: []
Dealix_differentiation:
  - evidence + relationship truth
  - action-specific authority
  - Saudi/Arabic operating context
  - payment/delivery/customer-value proof separation
  - one horizontal core + bounded playbooks
response_guidance: []
unknowns: []
next_check:
```

Do not copy competitor claims or prices into Dealix commercial authority.

---

## 6. Search-intent cluster

```yaml
cluster_id:
market:
source: SEARCH_CONSOLE_OR_AHREFS_OR_AUTHORIZED_TRENDS
source_refs: []
keywords_or_queries: []
intent:
  informational:
  commercial:
  transactional:
  navigational:
parent_topics: []
observed_demand_metrics: []
buyer_problem_hypotheses: []
sector_or_archetype_fit: []
package_hypotheses: []
content_assets:
  - page_or_article:
  - diagnostic_or_tool:
  - proof_asset:
CTA_hypothesis:
measurement:
  baseline_ref:
  qualified_action:
  attribution_method:
stop_rule:
```

Search demand is a content/market signal, not a lead or purchase probability.

---

## 7. Content opportunity card

```yaml
content_id:
source_signals: []
audience:
problem:
angle:
evidence_refs: []
allowed_claims: []
blocked_claims: []
buying_stage:
primary_package_hypothesis:
formats: []
channels: []
CTA:
attribution:
expiry:
brand_QA:
commercial_QA:
claim_QA:
channel_QA:
status: DRAFT
```

Every asset should trace to a real problem, question, objection, proof gap or source-bound market signal.

---

## 8. Partner card

```yaml
partner_id:
organization:
partner_type: SI_OR_MSP_OR_CONSULTANCY_OR_AGENCY_OR_DISTRIBUTOR_OR_ASSOCIATION
source_refs: []
observed_capabilities: []
market_access: []
mutual_value_hypothesis:
Dealix_role_hypothesis:
partner_role_hypothesis:
customer_boundary:
proof_and_attribution_rules:
relationship_state: UNKNOWN_NOT_EVIDENCE_BACKED
commercial_state: RESEARCH_ONLY
risk_class:
missing_evidence: []
next_evidence:
```

A company is not a partner until a real relationship and mutual intent are evidenced.

---

## 9. Regulatory / platform change card

```yaml
change_id:
source_id:
source_ref:
published_or_observed_at:
verified_at:
market_or_platform:
change_summary:
affected_Dealix_systems: []
affected_channels_or_sources: []
required_behavior_change:
prohibited_behavior: []
compliance_or_policy_owner:
engineering_gap:
  proven: false
  evidence_refs: []
kill_switch_or_stop_action:
next_review:
```

Regulatory/platform changes can lower authority immediately; they cannot increase authority without the canonical policy owner.

---

## 10. Weekly market brief

```yaml
brief_id:
period_start:
period_end:
truth_as_of:
market:
TOP_SIGNALS:
  - signal_id:
    why_it_matters:
    evidence_ref:
    freshness:
TOP_SECTOR_MOVES: []
TOP_ACCOUNT_OR_PARTNER_RESEARCH: []
TOP_SEARCH_DEMAND: []
TOP_TENDERS_OR_EVENTS: []
TOP_COMPETITOR_CHANGES: []
TOP_REGULATORY_OR_PLATFORM_CHANGES: []
PACKAGE_DEMAND:
  revenue_command:
  company_brain_governed_ai:
  saudi_market_access:
  partner_implementation_proof:
EXPERIMENTS:
  scale: []
  iterate: []
  stop: []
  invalid: []
RISKS: []
APPROVALS: []
NEXT_EVIDENCE: []
NEXT_ACTIONS: []
```

The weekly brief is an internal decision surface. It does not create opportunity, relationship, quote, spend or send authority.

---

## 11. Company Brain & Governed AI Sprint intake card

Use when a legitimate interaction/inbound says anything equivalent to AI, automation, Company Brain, company knowledge, agents, decision intelligence, tender/proposal intelligence, customer operations, or a bounded technical capability request.

```yaml
company:
interaction_or_inbound_ref:
relationship_state:
problem_statement:
requested_capability:
named_business_outcome:
current_workflow:
manual_steps: []
source_registry_seed:
  - source_id:
    source_type:
    system_owner:
    tenant_scope:
    purpose:
    authority_or_lawful_basis:
    access_class:
    freshness_sla:
    last_verified_at:
    provenance_ref:
    retention_or_expiry:
    allowed_claims: []
    prohibited_uses: []
workflow_candidates:
  - workflow_id:
    single_named_outcome:
    input_contract:
    deterministic_steps: []
    ai_reasoning_steps_if_needed: []
    tool_allowlist: []
    authority_class:
    approval_points: []
    output_contract:
    evidence_receipt:
    idempotency_key:
    retry_policy:
    rollback_or_safe_failure:
    human_handoff:
    evaluation_cases: []
baseline_or_evidence_gap:
proof_method:
customer_validation_method:
risk_and_regulatory_class:
missing_evidence: []
next_action: RUN_CANONICAL_COMPANY_BRAIN_SPRINT_ASSESSMENT
```

The default deliverable is never an unlimited custom consultancy, generic chatbot or unlimited agent build. It is one bounded business outcome with explicit sources, authority, workflow, evaluation, handover and proof.

---

## 12. Experiment card

```yaml
experiment_id:
hypothesis:
segment_or_account:
funnel_stage:
source_signals: []
baseline_ref:
target_metric:
qualified_business_movement:
founder_minutes_budget:
tool_cost_budget:
risk_class:
start_at:
end_or_review_at:
evidence_refs: []
result:
verdict: SCALE_OR_ITERATE_OR_STOP_OR_INVALID
next_action:
```

`SCALE` requires verified movement or a proven trust/cycle-time/cost improvement. Vanity metrics alone cannot scale a workload.
