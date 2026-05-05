---
name: dealix-linkedin-warm-intro-draft
mode: email
scenario: sales
version: 1
input_requirements:
  - customer_handle
  - mutual_connection_handle
  - sector
  - service_id
output_format:
  - intro_ar
  - intro_en
  - cta_ar
  - cta_en
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
  - manual_send_only_no_automation
approval_mode: approval_required
evidence_requirements:
  - mutual_connection_must_be_real
  - service_id_must_exist
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
example_prompt: |
  Draft a LinkedIn warm intro to Acme-Saudi-Pilot-EXAMPLE through
  mutual connection Mutual-EXAMPLE. Service: svc_diagnostic_v1.
  Manual send only. Arabic primary.
acceptance_checklist:
  - intro_ar < 600 characters
  - intro_en < 600 characters
  - mutual connection mentioned by handle
  - one CTA, no auto-send
  - approval_status == approval_required
---

# dealix-linkedin-warm-intro-draft

Drafts a bilingual LinkedIn warm intro. Manual send only — no
LinkedIn API integration.

## Why this skill exists

Warm intros convert ~10x better than cold outreach but only when the
mutual connection is real and the language is calibrated. This skill
produces a draft the founder pastes manually after the mutual
connection has agreed to be referenced.

## Inputs

- `customer_handle` (anonymized)
- `mutual_connection_handle` (anonymized; must be real)
- `sector`, `service_id`

## Safety

- `manual_send_only_no_automation` — no LinkedIn automation.
- No invented metrics; no guarantee language.
- All forbidden tokens are blocked by safety_gate.
