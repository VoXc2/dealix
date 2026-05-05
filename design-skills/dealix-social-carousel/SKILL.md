---
name: dealix-social-carousel
mode: social
scenario: growth
version: 1
input_requirements:
  - topic
  - sector
  - proof_event_ids
output_format:
  - slide_titles_ar
  - slide_titles_en
  - slide_bodies_ar
  - slide_bodies_en
  - cover_palette
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
approval_mode: approval_required
evidence_requirements:
  - at_least_one_proof_event_or_planned_label
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
example_prompt: |
  6-slide carousel on "diagnostic-led GTM for Saudi B2B" tied to
  proof_event evt_diag_001. Arabic primary; English secondary.
  Visual direction: warm_founder_led_beta.
acceptance_checklist:
  - 5–8 slides
  - slide 1 = hook (no claim)
  - last slide = CTA, no live link
  - all slides bilingual
  - no metric without a ProofEvent ref
---

# dealix-social-carousel

Bilingual social carousel, founder-voice. Used for distribution on
LinkedIn / X. Carousel images are NOT auto-published — exported to a
folder for the founder to upload manually.

## Why this skill exists

Public proof drives inbound. The carousel format compresses one
ProofEvent into a 5–8 slide story. If no ProofEvent backs a claim,
the slide is labeled `planned / not yet proven`.

## Safety

- No "guaranteed", no "blast", no "scrape".
- Every quantitative claim must point to a ProofEvent ID.
