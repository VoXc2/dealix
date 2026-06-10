---
name: dealix-pricing-page
mode: document
scenario: sales
version: 1
input_requirements:
  - bundle_name
  - sector
  - currency
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
  - no_hidden_fees
approval_mode: approval_required
evidence_requirements:
  - bundle_referenced_in_service_registry
  - currency_specified
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - revenue guaranteed
  - ranking guaranteed
example_prompt: |
  Render the Pricing Page for bundle=growth_starter, sector=b2b_services,
  currency=SAR.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - all bundles tie to service registry entries
  - has FAQ block addressing common buyer concerns
  - has approval banner
  - no guaranteed-outcome wording
design_system: dealix
---

# دليل Pricing Page

## الغرض

صفحة تسعير مُحدَّدة لباقة معينة. تعرض الباقة، السعر بالعملة
المحلية، الباقات المجاورة (للسياق)، والأسئلة الشائعة. لا تَعِد
بأرقام لا يدعمها سجل الإثبات.

## English summary

A pricing page for one bundle, with adjacent bundles shown for
context. Every price ties to a service registry entry; FAQs address
buyer concerns (refunds, scope changes, approval flow). No
guaranteed-outcome phrasing anywhere on the page.

## Output structure

1. **Header** — bundle, sector, currency, approval banner.
2. **Headline price** — single number, currency code visible.
3. **Adjacent bundles** — two cards: cheaper and richer.
4. **FAQ** — bilingual, includes the refund clause and approval flow.
5. **Footer** — links to evidence, terms, PDPL notice.

## Tone

Specific. Numerical. No "starting from" wording without a defined
ceiling. The page reads as a contract preview, not a marketing
brochure.
