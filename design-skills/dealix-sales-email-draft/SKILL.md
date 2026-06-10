---
name: dealix-sales-email-draft
mode: email
scenario: sales
version: 1
input_requirements:
  - customer_handle
  - sector
  - pipeline_state
  - service_id
  - proof_event_ids
output_format:
  - subject_ar
  - subject_en
  - body_ar
  - body_en
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
  - at_least_one_proof_event_id
  - service_id_must_exist
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
example_prompt: |
  Draft a sales email for Acme-Saudi-Pilot-EXAMPLE in fintech sector,
  pipeline_state=diagnostic_delivered, service_id=svc_diagnostic_v1.
  Reference proof_event evt_diag_001. Arabic primary, English secondary.
  Approval required before any send. No automated send.
acceptance_checklist:
  - subject_ar present and non-empty
  - subject_en present and non-empty
  - body_ar leads
  - body_en mirrors body_ar
  - no forbidden tokens
  - one CTA, no auto-send
  - approval_status == approval_required
---

# dealix-sales-email-draft

Drafts a bilingual sales email tied to a real pipeline_state and at
least one ProofEvent. The output is a DRAFT — never sent automatically.

## Why this skill exists

Sales follow-up is high-leverage but easy to get wrong (claims, tone,
PII). This skill produces a manually-reviewable draft that a founder
or AE copy-pastes into their own email client. There is no
`send_email_live` path. There never will be in this skill.

## Inputs

- `customer_handle` (anonymized, never raw company name)
- `sector` — used for tone calibration only, never invented
- `pipeline_state` — drives which template paragraph runs
- `service_id` — must exist in the service registry
- `proof_event_ids` — at least one, references the proof_ledger

## Outputs

Bilingual draft: subject + body + CTA in Arabic primary and English
secondary. No metrics that aren't already in a ProofEvent.

## Safety

- `manual_send_only_no_automation` — this skill never wires to an
  email provider.
- All forbidden tokens (نضمن, guaranteed, blast, scrape) are
  rejected by the safety_gate before publish.
- PII is redacted via `customer_data_plane.pii_redactor`.
