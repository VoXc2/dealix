# Client Template — Operational Kit

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [README_AR.md](./README_AR.md)

## Context
This directory is the **canonical per-client kit** used by every Dealix
delivery team. It removes the "blank page" problem at engagement start
and forces every client engagement into the same operating shape that
the rest of Dealix runs on (Capability Operating Model → Service Sprint
→ Proof Pack → Retainer → Productization). The kit plugs directly into
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and
`docs/DEALIX_OPERATING_CONSTITUTION.md`: every client engagement uses
the same capability scorecard, the same value ledger, the same cadence,
so the company can read across all clients on a single Monday morning.

## What is in this kit
Seven templates that together describe one client engagement:

| # | Template | Purpose |
|---|---|---|
| 1 | `CAPABILITY_ROADMAP.md` | Current → target capability levels and the bridge sprints |
| 2 | `EXPANSION_MAP.md` | After current proof, which offer comes next |
| 3 | `OPERATING_CADENCE.md` | Daily / weekly / monthly review rhythm |
| 4 | `VALUE_DASHBOARD.md` | Revenue, time, quality, risk, knowledge value |
| 5 | `AI_OPERATING_MODEL.md` | Client-specific AI operating model |
| 6 | `CAPABILITY_SCORECARD.md` | Score 0–5 across 6 capabilities, with evidence |
| 7 | `CAPABILITY_BACKLOG.md` | Prioritized capability gap backlog |

Each template has an Arabic mirror (`*_AR.md`).

## Workflow
1. **Copy** the directory to a new client folder:
   ```
   cp -r clients/_template clients/<client_slug>
   ```
   Use a lowercase, dash-separated slug (e.g. `clients/acme-clinic`,
   `clients/north-mall-retail`). The slug must NOT contain the client's
   real legal name if the repo is public.
2. **Fill placeholders** marked `<CLIENT_NAME>`, `<CITY>`, `<SECTOR>`,
   `<OWNER_NAME>`, `<ENGAGEMENT_START>`, `<ARR_BAND>`, `<SERVICE_TIER>`.
3. **Link** each filled template to the matching capability blueprint
   in `docs/capabilities/<x>_capability.md` and to the active service
   sprint folder in `docs/services/<sprint>/`.
4. **Maintain** the templates on the cadence defined in
   `OPERATING_CADENCE.md`: scorecard and value dashboard monthly,
   backlog weekly, roadmap quarterly.
5. **Close out** on engagement end with a Proof Pack
   (`docs/templates/PROOF_PACK_TEMPLATE.md`) and archive the client
   folder under `clients/_archive/<client_slug>/` once anonymized.

## Privacy and PII rules
- **Never** commit personally identifiable information (PII), customer
  data, financial statements, tokens, API keys, contracts, or names of
  individual employees inside this repository.
- The on-repo client folder contains **structure only**: capability
  levels, value categories, cadence notes, anonymized metrics
  (e.g. "monthly recurring revenue +18%" instead of absolute SAR).
- Sensitive data (contracts, dumps, raw spreadsheets, customer lists)
  lives in the private Dealix workspace (`workspace/clients/<slug>/`
  outside git, or in the encrypted drive) — never here.
- If a placeholder asks for a name, leave it as `<CLIENT_NAME>` for
  public clients or use a project codename (e.g. `BLUE-FALCON`) for
  enterprise NDA clients. Only the codename appears in commits.
- Run `scripts/scan_client_pii.py` (or equivalent) before any push;
  align with `docs/ops/PDPL_RETENTION_POLICY.md` and
  `docs/DATA_RETENTION_POLICY.md`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Capability diagnostic results | Capability scorecard | CSM Lead + Capability Owner | Engagement start |
| Sprint outputs | Value dashboard, proof pack | Delivery Lead | Weekly + monthly |
| Retainer review | Updated roadmap, expansion map | CSM Lead | Monthly |
| Quality and incident events | Backlog updates | Quality Lead | Weekly |

## Metrics
- **Template completeness** — % of the 7 templates filled at day 14.
- **Cadence adherence** — % of weekly + monthly reviews logged.
- **Value capture rate** — % of value items in `VALUE_DASHBOARD.md`
  evidenced in the client's `proof_pack/` folder.
- **Expansion conversion** — clients where `EXPANSION_MAP.md` next-best
  offer converted within 90 days of proof.

## How to fill this
- Pair the new CSM with a capability owner on day 1 and complete the
  scorecard and roadmap together within 48 hours.
- Use `docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md` as
  the evidence-collection script.
- Re-read `docs/company/CAPABILITY_OPERATING_MODEL.md` so the
  vocabulary on the scorecard matches the rest of the company.

## Related
- `docs/company/CAPABILITY_OPERATING_MODEL.md` — capability vocabulary
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — five-layer model
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — wider CSM playbook
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
