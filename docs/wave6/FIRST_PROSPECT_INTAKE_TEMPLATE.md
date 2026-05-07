# First Prospect Intake Template (Wave 6 Phase 2)

**This is a TEMPLATE.** Real prospect data NEVER goes here.
The script `scripts/dealix_first_prospect_intake.py` writes your live
intake to `docs/wave6/live/first_prospect_intake.json` (gitignored).

---

## Fields (placeholders)

| Field | Placeholder | Notes |
|---|---|---|
| `company_name` | `<COMPANY-NAME-PLACEHOLDER>` | Public company name only — no internal entity codes |
| `sector` | `<real_estate|agencies|services|consulting|training|construction|hospitality|logistics>` | One of the supported KSA sectors |
| `region` | `<Riyadh|Jeddah|Eastern|other>` | KSA region |
| `website` | `<optional URL>` | Optional |
| `current_growth_problem` | `<1-sentence>` | E.g. "leads from forms not converted to demos" |
| `current_sales_problem` | `<1-sentence>` | E.g. "team responds 4-6 hours late, leads go cold" |
| `current_support_problem` | `<1-sentence>` | E.g. "WhatsApp inquiries pile up, no SLA" |
| `current_channels` | `<["whatsapp","email","website","linkedin","calls"]>` | Subset |
| `team_size` | `<integer>` | Total full-time staff |
| `decision_maker` | `<role + name placeholder>` | E.g. "GM (Sami)" — DO NOT include phone/email |
| `known_relationship` | `<warm_intro|cold>` | Wave 6 only proceeds with warm_intro |
| `consent_status` | `<pending|granted_for_diagnostic|granted_for_demo|withdrawn>` | Tracks PDPL consent |
| `preferred_language` | `<ar|en|both>` | Demo language |
| `notes` | `<free text>` | Founder's prep notes |

## Hard rules

- ❌ NEVER commit a real `first_prospect_intake.json` to the repo
- ❌ NEVER include raw email/phone/Saudi-ID in this file
- ❌ NEVER include this template's PII fields in any test fixture
- ✅ Only `warm_intro` accepted (cold = blocked by Wave 5 tool guardrails)
- ✅ `decision_maker` is a role + first-name only (no full PII)
- ✅ Consent must be explicitly recorded BEFORE diagnostic generation

## Workflow

1. Founder runs `python3 scripts/dealix_first_prospect_intake.py` interactively
2. Script writes `docs/wave6/live/first_prospect_intake.json` (gitignored)
3. Founder uses the JSON as input to `dealix_ai_ops_diagnostic.py` (Phase 3)
4. Founder generates pilot brief via `dealix_pilot_brief.py` (Phase 4)

## Sample (template values only)

```json
{
  "company_name": "<COMPANY-NAME-PLACEHOLDER>",
  "sector": "<SECTOR-PLACEHOLDER>",
  "region": "<REGION-PLACEHOLDER>",
  "website": null,
  "current_growth_problem": "<1-sentence-placeholder>",
  "current_sales_problem": "<1-sentence-placeholder>",
  "current_support_problem": "<1-sentence-placeholder>",
  "current_channels": [],
  "team_size": 0,
  "decision_maker": "<ROLE-PLACEHOLDER>",
  "known_relationship": "warm_intro",
  "consent_status": "pending",
  "preferred_language": "ar",
  "notes": "<placeholder>",
  "intake_version": "wave6_v1",
  "is_real_data": false,
  "is_template": true
}
```
