# Intake — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Sales Engineer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_AR.md](./intake_AR.md)

## Context
The intake is the first gate that decides whether the Sprint can be delivered for the price quoted. It exists to expose risk factors early (data sensitivity, urgency, missing ICP, stakeholder complexity) so the price applies the correct premium from `docs/company/RISK_ADJUSTED_PRICING.md`. It is the entry point to the Dealix revenue funnel in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and feeds the proof pack initial events log per `docs/templates/PROOF_PACK_TEMPLATE.md`.

## Intake Goals
1. Confirm the client fits the buyer profile.
2. Surface premium triggers (sensitivity, urgency, complexity).
3. Capture the ICP at sufficient detail to score accounts.
4. Identify the single sponsor and the single reviewer.
5. Produce a signed intake summary that becomes Appendix A of the SOW.

## 15-Question Discovery Form
Each question has an **owner**, a **required** flag, and a **validation** rule. The Sales Engineer fills the form jointly with the client during a 45-minute call.

### Section 1 — Buyer & Sponsor
1. **What is the legal entity name and trading name?** (required) — Validate against ZATCA tax record format.
2. **Who is the sprint sponsor?** (required, single name + role + email).
3. **Who is the daily reviewer if different?** (optional, single name).
4. **What outcome would make the sprint a success in your eyes?** (required, free text ≤ 200 chars).

### Section 2 — Current Data State
5. **Where does your account/lead data currently live?** (required, multi-select: HubSpot, Salesforce, Excel, Sheets, Notion, other).
6. **Approximate row count of the primary export?** (required, integer 100–10,000; if >10,000, escalate to scoped engagement).
7. **Can you export to CSV/XLSX within 1 business day?** (required, yes/no).

### Section 3 — ICP & Sales Process
8. **Describe your ICP in 2–3 sentences.** (required, free text).
9. **Top 3 target sectors?** (required, multi-select from KSA-NACE list).
10. **Top 3 target cities/regions?** (required).
11. **What is your current sales process?** (required, free text).
12. **What is your current CRM tool?** (required, single-select).

### Section 4 — Previous Outreach & Risk
13. **Share one previous outreach example (anonymized OK).** (required, free text or file).
14. **Does any of your data fall under sensitive categories (health, minors, government, financial)?** (required, yes/no; if yes, apply +20-40% sensitivity premium).
15. **What is the success metric you'll report internally?** (required, free text; this becomes the headline of the proof report).

## Validation Rules
- All required fields must be present before SOW is generated.
- Sensitivity = yes → triggers `RISK_ADJUSTED_PRICING` sensitivity premium and a mandatory PDPL pre-check (`docs/ops/PDPL_RETENTION_POLICY.md`).
- Row count > 10,000 → escalate to scoped engagement, not the fixed-fee sprint.
- ICP description shorter than 50 chars → flag for sales engineer to expand in the call.
- Sponsor and reviewer must each have a verifiable corporate email; free webmail addresses (gmail, hotmail) trigger a verification check.

## Form Fields (Notion DB / Airtable schema)
| Field | Type | Required | Notes |
|---|---|---|---|
| `client_id` | autogen | yes | Internal |
| `legal_name` | string | yes | ZATCA format |
| `trading_name` | string | no | |
| `sponsor_name` | string | yes | |
| `sponsor_email` | email | yes | Validated |
| `reviewer_name` | string | no | |
| `success_outcome` | text | yes | ≤ 200 chars |
| `data_location` | multi-select | yes | |
| `row_count` | integer | yes | 100–10000 |
| `csv_export_ready` | bool | yes | |
| `icp_description` | text | yes | ≥ 50 chars |
| `target_sectors` | multi-select | yes | Up to 3 |
| `target_regions` | multi-select | yes | Up to 3 |
| `sales_process` | text | yes | |
| `crm_tool` | single-select | yes | |
| `prev_outreach_sample` | file/text | yes | |
| `sensitive_data` | bool | yes | Premium trigger |
| `success_metric` | text | yes | Proof report headline |
| `urgency_days` | integer | no | If < 10, urgency premium |
| `stakeholder_count` | integer | no | If > 3, complexity premium |

## Premium Triggers (auto-computed from intake)
- **Sensitivity = yes** → +20–40% (per `RISK_ADJUSTED_PRICING.md`).
- **Urgency < 10 calendar days** → +20–50%.
- **Stakeholder_count > 3** → +15–30%.
- **Multi-source merge requested** → +SAR 2,500 per extra source.

## Output of Intake
- Signed **Intake Summary** (1 page, PDF) including all 15 answers and the computed premium.
- Auto-generated SOW with the right price band.
- Initial **proof pack event**: `intake_completed` with timestamp.
- Internal Notion record in the **Sales Pipeline** database.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Inbound qualified lead | Intake call scheduled | Sales Engineer | Within 2 business days |
| 45-min discovery call | Filled intake form | Sales Engineer + Client | One session |
| Form data | Premium-adjusted SOW | Sales Engineer + Margin Controller | Same day |
| Signed SOW | Kickoff scheduled | Ops + Delivery Lead | Within 5 business days |

## Metrics
- **Intake-to-SOW conversion** — `% intakes that lead to signed SOW`. Target ≥ 50%.
- **Intake completeness** — `% intakes with all 15 fields present at SOW generation`. Target = 100%.
- **Premium accuracy** — `% sprints where computed premium matches delivery reality`. Target ≥ 90%.

## Related
- `docs/capabilities/revenue_capability.md` — parent capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability placement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers source
- `docs/company/MARGIN_CONTROL.md` — pricing floor enforcement
- `docs/quality/QUALITY_STANDARD_V1.md` — intake quality bar
- `docs/templates/PROOF_PACK_TEMPLATE.md` — initial proof events
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic funnel placement
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — sprint conversion playbook
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — canonical pricing
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
