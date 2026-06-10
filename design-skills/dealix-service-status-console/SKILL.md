---
name: dealix-service-status-console
mode: prototype
scenario: operations
version: 1
input_requirements:
  - service_registry_snapshot
  - readiness_state
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
approval_mode: approval_required
evidence_requirements:
  - service_registry_snapshot_present
  - readiness_state_described
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
  - cold WhatsApp
  - fully automated external send
example_prompt: |
  Render the Service Status Console for the current service registry
  snapshot, mapping each service to a status chip and a readiness note.
acceptance_checklist:
  - has Arabic primary section
  - has English secondary section
  - every service has one of the canonical status chips
  - has approval banner for external share
  - no guaranteed-outcome wording anywhere
design_system: dealix
---

# دليل Service Status Console

## الغرض

لوحة حالة الخدمات: لكل خدمة مسجَّلة في `service_registry`، تُعرض
شريحة الحالة (Live / Pilot / Partial / Target / Blocked / Approval
Required / Draft Only / Internal Only)، ومُلاحظة جاهزية في سطر
واحد، ورابط دليل عند الإمكان.

## English summary

A console listing every service in the registry with its current
status chip and a one-line readiness note. The console is mobile-
first, sortable by status, and gated behind the approval flow for
any external share. Mirrors the public `landing/status.html` page
but adds operator-only annotations.

## Output structure

1. **Header** — snapshot timestamp, approval banner.
2. **Service rows** — name, status chip, readiness note, evidence
   link if applicable.
3. **Legend** — the canonical status chip definitions, in both
   Arabic and English.
4. **Footer** — link to the underlying registry record and the
   approval log.

## Tone

Plain, operational, no marketing wording. The console exists to
make the boundary between "what we sell" and "what we have proven"
visible at a glance.
