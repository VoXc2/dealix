---
name: dealix-customer-onboarding-guide
mode: document
scenario: customer-success
version: 1
input_requirements:
  - customer_handle
  - service_id
  - delivery_milestones
  - support_channel_handle
output_format:
  - sections_ar
  - sections_en
  - checklist_ar
  - checklist_en
  - faq_ar
  - faq_en
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
approval_mode: approval_required
evidence_requirements:
  - service_id_must_exist
  - delivery_milestones_must_match_delivery_factory_plan
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
example_prompt: |
  Onboarding guide for Acme-Saudi-Pilot-EXAMPLE on svc_diagnostic_v1.
  Milestones from delivery_factory plan. Visual direction:
  saudi_executive_trust.
acceptance_checklist:
  - welcome section bilingual
  - milestone timeline matches delivery plan
  - one support channel listed
  - PII redacted in any sample
  - approval_status == approval_required
---

# dealix-customer-onboarding-guide

A bilingual onboarding document a new customer receives after
payment. Manual send only — the document is exported for the founder
or CS lead to attach.

## Why this skill exists

Onboarding is where promises become commitments. This artifact
mirrors the delivery_factory plan exactly — no extra promises, no
extra timelines. If a milestone isn't in the plan, it isn't in the
guide.

## Safety

- No "guaranteed delivery date" — only the planned date.
- All examples use `Acme-Saudi-Pilot-EXAMPLE`-style placeholders.
