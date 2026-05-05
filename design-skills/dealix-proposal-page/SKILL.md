---
name: dealix-proposal-page
mode: document
scenario: sales
version: 1
input_requirements:
  - customer_handle
  - bundle_name
  - sector
  - duration_weeks
output_format:
  - markdown_ar
  - markdown_en
  - html
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
approval_mode: approval_required
evidence_requirements:
  - bundle_referenced_in_service_registry
  - sector_provided
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - revenue guaranteed
  - ranking guaranteed
  - fully automated external send
example_prompt: |
  Draft a Proposal Page for ACME-Saudi-Pilot, bundle=growth_starter,
  sector=b2b_services, duration_weeks=8.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - bundle linked to service registry entry
  - has scope, exclusions, evidence link
  - has approval banner
  - no guaranteed-outcome wording
design_system: dealix
---

# دليل Proposal Page

## الغرض

عرض تقديمي قصير لصفقة محددة: نطاق العمل، الاستثناءات، الجدول الزمني،
السعر، وروابط الدليل. الصفحة قابلة للقراءة على الجوال وتنتهي بزر CTA
موسوم بـ `Approval Required`.

## English summary

A single-page proposal anchored to a registered service bundle.
The page lists scope, explicit exclusions, evidence references, and
a price block. Every external claim links to the proof ledger; the
send button starts in `Approval Required` state.

## Output structure

1. **Header** — customer, bundle, duration, locked-at, approval banner.
2. **Scope** — three bullets, each tied to a deliverable.
3. **Exclusions** — explicit list of what is *not* in scope.
4. **Evidence** — links to prior proof packs or ledger entries.
5. **Price** — single number, currency, payment terms.
6. **Next step** — single CTA, defaulting to `Approval Required`.

## Tone

Saudi-executive. Short sentences. No marketing adjectives. Price is
shown as a single number, not a range; ranges go in pricing pages.
