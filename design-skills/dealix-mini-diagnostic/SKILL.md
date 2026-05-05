---
name: dealix-mini-diagnostic
mode: document
scenario: sales
version: 1
input_requirements:
  - company_handle
  - sector
  - region
  - pipeline_state
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
  - sector_provided
  - pipeline_state_described
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - cold WhatsApp
  - revenue guaranteed
example_prompt: |
  Generate a Mini Diagnostic for ACME-Saudi-Pilot, sector=b2b_services,
  region=riyadh, with a one-line pipeline state describing current
  outbound and conversion practice.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - has 3 named gaps
  - has bundle recommendation linked to a service registry entry
  - has approval banner at the top of the artefact
  - no forbidden marketing token in positive context
design_system: dealix
---

# دليل Mini Diagnostic

## الغرض

نسخة قصيرة من تشخيص قناة المبيعات لدى عميل محتمل، مكتوبة في صفحة
واحدة قابلة للقراءة على الجوال. تستهدف رئيسًا تنفيذيًا أو مديرًا
عامًا يقرأ خلال ست دقائق ويحتاج إلى ثلاثة أرقام: ما الذي يعمل، ما
الذي لا يعمل، وما الحزمة الموصى بها.

## English summary

A one-page diagnostic that names three concrete gaps in the
prospect's pipeline and recommends a single Dealix bundle. It is
*always* approval-gated; no diagnostic is sent externally without a
named human approver.

## Output structure

1. **Header** — customer handle, sector, region, locked-at timestamp,
   approval banner showing `Approval Required`.
2. **Arabic block** — 3 gaps + 1 recommendation, in Arabic prose.
3. **English block** — same content, English prose.
4. **Evidence** — every gap references either a public signal
   (the customer-supplied pipeline state) or `null` (in which case the
   gap is marked `Pilot` not `Live`).
5. **Next step** — a single CTA. Default state: `Approval Required`.

## Tone

Calm, specific, Saudi-executive. No hype, no guarantees. The
recommendation must be backed by a service registry entry; the
diagnostic refuses to render if no matching service exists.
