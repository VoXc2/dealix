---
name: dealix-executive-weekly-pack
mode: report
scenario: executive
version: 1
input_requirements:
  - week_iso
  - portfolio_handles
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
  - internal_only_unless_approved
approval_mode: approval_required
evidence_requirements:
  - proof_event_ids_present
  - week_iso_specified
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - revenue guaranteed
example_prompt: |
  Build the Executive Weekly Pack for week 2026-W18 across
  portfolio_handles=[ACME-Saudi-Pilot, BETA-Riyadh-Pilot] with
  evidence drawn from the proof ledger.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - every KPI has an evidence badge
  - has approval banner
  - has Internal Only chip when not yet approved for board distribution
design_system: dealix
---

# دليل Executive Weekly Pack

## الغرض

ملخص أسبوعي يُقدَّم للقيادة التنفيذية: لوحة مؤشرات لكل عميل في
المحفظة، الأحداث المُسجَّلة في سجل الإثبات، والمخاطر التي تتطلب
تدخلًا من المؤسس. يبدأ كل عنصر بحالة (Live / Pilot / Blocked /
Target) قبل عرض الأرقام.

## English summary

A weekly executive pack covering every active engagement in the
portfolio. KPIs come from the proof ledger only; unproven items
default to `Pilot` or `Target`. Until the founder approves the pack
for distribution it carries the `Internal Only` chip.

## Output structure

1. **Cover** — week ISO, portfolio handles, locked-at, approval banner.
2. **Per-engagement row** — handle, sector, status chip, KPI tiles,
   evidence badges.
3. **Risk panel** — items needing founder action.
4. **Distribution state** — defaults to `Internal Only`; only flips
   to a customer-shareable state via the approval flow.

## Tone

Brief, calm, evidence-linked. Bullet points over prose. No
forward-looking claims that cannot be backed by a recorded event.
