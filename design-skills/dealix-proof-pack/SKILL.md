---
name: dealix-proof-pack
mode: report
scenario: proof
version: 1
input_requirements:
  - customer_handle
  - delivery_window
  - proof_event_ids
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
  - pii_redacted_unless_consented
approval_mode: approval_required
evidence_requirements:
  - proof_event_ids_present
  - delivery_window_specified
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - revenue guaranteed
  - ranking guaranteed
example_prompt: |
  Assemble a Proof Pack for ACME-Saudi-Pilot covering delivery
  window 2026-04-01..2026-04-30, referencing proof_event_ids
  evt_001..evt_012 from the ledger.
acceptance_checklist:
  - every claim has an evidence badge linking to the proof ledger
  - PII is redacted unless consent_for_publication=True is recorded
  - has Arabic primary section
  - has English secondary section
  - has approval banner
  - has version + locked-at stamp
design_system: dealix
---

# دليل Proof Pack

## الغرض

تقرير مُجمَّع يربط النتائج المُحققة برموز أحداث في سجل الإثبات
(Proof Ledger). كل ادعاء على الصفحة يحمل شارة دليل قابلة للنقر.
تُستخدم هذه الحزمة لإثبات الأداء أمام العميل قبل تجديد العقد أو
رفع المستوى.

## English summary

A bundled report that links every claimed outcome to a proof ledger
event. The pack is generated for a delivery window, signed with a
locked-at timestamp, and gated behind an approval pill before any
external send. PII is redacted by default; un-redacted versions
require an explicit `consent_for_publication=True` record.

## Output structure

1. **Cover page** — customer handle, window, version, approval banner.
2. **Outcome KPIs** — each tile carries an evidence badge.
3. **Delivery timeline** — table linking each delivered task to its
   ledger event id.
4. **Evidence index** — full list of `EVT-…` / `INV-…` / `PROOF-…`
   references with one-line descriptions.
5. **Next step** — recommendation for the next bundle, gated by
   `Approval Required`.

## Tone

Restrained. Numbers come from the ledger only. Any KPI without a
matching event is omitted; the renderer never invents a number.
