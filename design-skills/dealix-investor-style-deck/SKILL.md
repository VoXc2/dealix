---
name: dealix-investor-style-deck
mode: deck
scenario: executive
version: 1
input_requirements:
  - company_handle
  - stage
  - service_ids
  - proof_event_ids
  - financials_summary_handle
output_format:
  - slide_titles_ar
  - slide_titles_en
  - slide_bodies_ar
  - slide_bodies_en
  - palette_tokens
  - typography_tokens
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
approval_mode: approval_required
evidence_requirements:
  - every_metric_must_link_to_proof_event_or_finance_record
  - no_invented_financials
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - revenue guaranteed
  - 10x revenue
example_prompt: |
  10-slide investor-style deck (internal review only). Stage: pre-seed.
  service_ids=[svc_diagnostic_v1]. Proof events: evt_diag_001.
  Visual direction: partnership_boardroom.
acceptance_checklist:
  - exactly one cover slide
  - problem/solution/proof/team/ask slides present
  - every chart references a finance_record_id or ProofEvent
  - no projection beyond what is recorded
  - Arabic primary copy
---

# dealix-investor-style-deck

Internal-review investor-style deck. NOT auto-shared with investors.
The artifact is a draft a founder reviews + manually sends.

## Why this skill exists

Investor decks are the most common place for inflated metrics. This
skill enforces: every number references a finance record OR a
ProofEvent. If neither exists, the slide says `planned / not yet
proven`.

## Safety

- All metrics MUST be evidence-linked.
- Forbidden: "10x revenue", "guaranteed growth", projection-only
  charts without a "projection" disclaimer.
