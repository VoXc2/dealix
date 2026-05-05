---
name: dealix-partnership-one-pager
mode: document
scenario: partnership
version: 1
input_requirements:
  - partner_handle
  - partner_sector
  - proposed_collaboration
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
  - partner_sector_provided
  - proposed_collaboration_described
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - revenue guaranteed
example_prompt: |
  Draft the Partnership One-Pager for partner_handle=GULF-ANALYTICS,
  partner_sector=consultancy, proposed_collaboration=joint b2b services
  pilot in Riyadh.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - mutual fit, scope, evidence, next step blocks
  - has approval banner
  - no guaranteed-outcome wording
design_system: dealix
---

# دليل Partnership One-Pager

## الغرض

صفحة واحدة تُلخِّص فرصة شراكة محتملة: ملاءمة كل طرف، النطاق
المقترح، الدليل المتاح، والخطوة التالية. تُكتَب بطريقة تَقرَأها
القيادة في خمس دقائق وتقرر فيها الانتقال إلى نقاش رسمي.

## English summary

A one-page partnership brief covering mutual fit, proposed scope,
evidence references, and next step. Designed to be read in five
minutes by an executive considering whether to schedule a formal
discussion. Approval-gated; never sent externally without sign-off.

## Output structure

1. **Header** — partner handle, sector, locked-at, approval banner.
2. **Mutual fit** — two short paragraphs, one per side.
3. **Proposed collaboration** — three bullets, each tied to a
   measurable outcome.
4. **Evidence** — links to prior proof packs or service registry
   entries that back the proposal.
5. **Next step** — single CTA, defaulting to `Approval Required`.

## Tone

Respectful, peer-to-peer. Avoids both deference and overreach.
Saudi business etiquette applies: name the relationship before the
deal, evidence before the price.
