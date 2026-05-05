---
name: dealix-customer-room-dashboard
mode: prototype
scenario: operations
version: 1
input_requirements:
  - customer_handle
  - active_bundles
  - proof_event_ids
output_format:
  - html
  - markdown_ar
  - markdown_en
safety_rules:
  - approval_required_before_external_share
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
  - pii_redacted_unless_consented
approval_mode: approval_required
evidence_requirements:
  - active_bundles_listed
  - proof_event_ids_present
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - revenue guaranteed
example_prompt: |
  Render the Customer Room Dashboard for ACME-Saudi-Pilot showing
  active bundles, the latest proof events, and pending approvals.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - status chip per bundle (Live/Pilot/Partial/Blocked)
  - every KPI has an evidence badge
  - has approval banner for any external-share action
design_system: dealix
---

# دليل Customer Room Dashboard

## الغرض

لوحة تحكم خاصة بكل عميل: الباقات النشطة، آخر الأحداث المُسجَّلة
في سجل الإثبات، الموافقات المعلَّقة، والمخاطر. اللوحة قابلة للقراءة
على الجوال، وتعرض حالة لكل باقة باستخدام شرائح الحالة الموحَّدة.

## English summary

A per-customer operations dashboard surfacing active bundles, the
last 10 proof ledger events for the engagement, and any pending
approvals. Mobile-first; every bundle row carries a canonical
status chip (Live, Pilot, Partial, Blocked, Approval Required,
Draft Only, Internal Only, Target).

## Output structure

1. **Header** — customer handle, locked-at, approval banner.
2. **Bundle cards** — one card per active bundle, status chip top-end.
3. **Recent events** — table of the last 10 ledger events, each with
   an evidence badge.
4. **Pending approvals** — list of items currently in
   `Approval Required` state.
5. **Risk panel** — items where `Blocked` or `Partial` requires
   founder action.

## Tone

Operator-facing primarily; customer-shareable views require the
approval flow. Numbers come from the ledger only — the dashboard
refuses to render a tile that has no backing event.
