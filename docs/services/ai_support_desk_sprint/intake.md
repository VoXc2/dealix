# Intake — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Sales Engineer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_AR.md](./intake_AR.md)

## Context
Intake surfaces volume, sensitivity, language mix, and escalation logic — the four dimensions that decide whether a 14-day Sprint is realistic. It feeds the initial `intake_completed` event in the proof pack per `docs/templates/PROOF_PACK_TEMPLATE.md` and computes premiums per `docs/company/RISK_ADJUSTED_PRICING.md`. Clinics/healthcare clients are routed through additional checks per `docs/playbooks/clinics_playbook.md`.

## Intake Goals
1. Confirm message volume is in the 200–2,000/week range.
2. Surface sensitive-case categories.
3. Lock the escalation logic at design time, not runtime.
4. Identify the named support lead.
5. Produce a signed intake summary.

## 14-Question Discovery Form

### Section 1 — Sponsor & Support Lead
1. **Legal entity + sponsor name + role.** (required)
2. **Support lead name + role + email.** (required — usually Head of Customer Care)

### Section 2 — Channels & Volume
3. **Which channels do you support?** (required, multi-select: WhatsApp Business / email / Instagram DM / web chat / SMS / phone / other)
4. **What is the average inbound volume per week (across all channels)?** (required, integer 200–2,000)
5. **What is the language mix?** (required, structured: % Arabic, % English, % other)
6. **How many human agents triage today?** (required, integer 1–10)

### Section 3 — Categories Already In Use
7. **Do you already use categories or tags?** (required, yes/no + list)
8. **What is your current FAQ?** (required, file or link or "none — we'll define one")

### Section 4 — Sensitivity & Escalation
9. **What counts as a sensitive case in your industry?** (required, free text — clinics/healthcare must list health-data triggers)
10. **What is your escalation logic today?** (required, free text)
11. **Does any case type require legal review before reply?** (required, yes/no + list)

### Section 5 — Response Times
12. **What is your target first-response time?** (required, integer minutes/hours)
13. **What is your target resolution time?** (required, integer hours/days)

### Section 6 — Success Metric
14. **What metric would you report for this Sprint?** (required, free text)

## Validation Rules
- Volume < 200/week → not enough signal; route to lighter offer.
- Volume > 2,000/week → route to scoped engagement.
- Clinics/healthcare → mandatory `clinics_playbook` pre-check; +30–50% premium.
- Government clients → governance pre-check + multi-jurisdiction posture review.
- Sensitive data = yes → +20–40% premium.

## Form Fields (Notion DB schema)
| Field | Type | Required |
|---|---|---|
| `client_id` | autogen | yes |
| `legal_name` | string | yes |
| `sponsor_name`, `sponsor_email` | string, email | yes |
| `support_lead_name`, `support_lead_email` | string, email | yes |
| `channels` | multi-select | yes |
| `weekly_volume` | integer | yes |
| `language_mix` | structured | yes |
| `agent_count` | integer | yes |
| `current_categories` | text | yes |
| `current_faq` | file/text | yes |
| `sensitive_case_triggers` | text | yes |
| `escalation_logic` | text | yes |
| `legal_review_required` | bool | yes |
| `target_first_response_minutes` | integer | yes |
| `target_resolution_hours` | integer | yes |
| `success_metric` | text | yes |
| `industry` | single-select | yes |
| `urgency_days` | integer | no |

## Premium Triggers
- Clinics / healthcare → +30–50% premium + `clinics_playbook` checklist.
- Other sensitive data → +20–40%.
- Multilingual (> 2 languages) → +15%.
- Urgency < 14 days → +20–50%.
- Volume > 1,500/week → +15%.
- Agent count > 5 → +10–20% (more reviewers to onboard).

## Output
- Signed Intake Summary (1 page PDF).
- Auto-generated SOW with band + premiums.
- Initial `intake_completed` proof event.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Qualified lead | Intake call scheduled | Sales Engineer | ≤ 2 days |
| 45-min discovery call | Filled intake | Sales Engineer + Client | One session |
| Filled intake | SOW | Sales Engineer + Margin Controller | Same day |

## Metrics
- **Intake-to-SOW conversion** — Target ≥ 50%.
- **Intake completeness** — Target = 100%.
- **Premium accuracy** — Target ≥ 90%.
- **Clinics pre-check coverage** — `% clinics intakes with clinics_playbook completed`. Target = 100%.

## Related
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
