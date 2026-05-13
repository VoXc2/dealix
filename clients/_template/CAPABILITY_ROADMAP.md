# Capability Roadmap — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_ROADMAP_AR.md](./CAPABILITY_ROADMAP_AR.md)

## Context
This roadmap shows where `<CLIENT_NAME>` (sector: `<SECTOR>`, city:
`<CITY>`, engagement start: `<ENGAGEMENT_START>`) sits today on the
six Dealix capabilities, where they need to be in 12 months, and the
Dealix services that bridge each gap. It exists so that every client
conversation about "what comes next" is grounded in the same
vocabulary used in `docs/company/CAPABILITY_OPERATING_MODEL.md` and
`docs/company/CAPABILITY_MATURITY_MODEL.md`, not in ad-hoc
salesperson framing. It is the source of truth for the 30/60/90 plan
and for the long-term Enterprise AI OS view referenced in
`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Header
- **Client:** `<CLIENT_NAME>`
- **Sector:** `<SECTOR>`
- **City / region:** `<CITY>`
- **Engagement start:** `<ENGAGEMENT_START>`
- **Service tier:** `<SERVICE_TIER>` (Diagnostic / Sprint / Pilot / Retainer / Enterprise)
- **Primary CSM:** `<OWNER_NAME>`
- **ARR band:** `<ARR_BAND>`

## Maturity scale (shared with `CAPABILITY_SCORECARD.md`)
| Level | Name | Short description |
|---|---|---|
| 0 | Absent | Capability does not exist |
| 1 | Manual | Done by people, no system, no metrics |
| 2 | Structured | Documented process, spreadsheets, basic metrics |
| 3 | AI-Assisted | AI used in parts, human still owns the loop |
| 4 | Governed Workflow | AI in a controlled workflow with HITL and audit |
| 5 | Optimized OS | Capability runs as a productized OS, evidence-led |

## Current vs target — six capabilities
| Capability | Current | Target (12mo) | Service to bridge | Blueprint |
|---|---|---|---|---|
| Revenue | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/revenue_capability.md` |
| Customer | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/customer_capability.md` |
| Operations | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/operations_capability.md` |
| Knowledge | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/knowledge_capability.md` |
| Data | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/data_capability.md` |
| Governance | `<0–5>` | `<0–5>` | `<sprint / retainer>` | `docs/capabilities/governance_capability.md` |

Fill `<0–5>` from `CAPABILITY_SCORECARD.md`.

## First sprint
- **Capability addressed:** `<capability>`
- **Sprint name:** `<lead_intelligence_sprint / ai_quick_win_sprint / company_brain_sprint / ai_support_desk_sprint / ai_governance_program>`
- **Why this one first:** highest value, lowest risk, evidence already
  in `CAPABILITY_SCORECARD.md`. State the level move (e.g. Revenue
  Level 1 → 3) and the proof artefact expected.
- **Sprint duration:** 4–6 weeks
- **Owner pair:** CSM + capability owner
- **Linked sprint folder:** `docs/services/<sprint>/`

## 30/60/90 plan
**Day 0–30 — Diagnostic and first sprint kickoff**
- Complete `CAPABILITY_SCORECARD.md` with evidence per capability.
- Sign first service sprint and align on the proof KPI.
- Stand up `OPERATING_CADENCE.md` rhythms.
- Establish data access, security, and PDPL alignment.

**Day 31–60 — First proof**
- Deliver sprint, populate proof pack
  (`docs/templates/PROOF_PACK_TEMPLATE.md`).
- Update `VALUE_DASHBOARD.md` with measured value.
- Re-score the addressed capability; should move ≥ 1 level.
- Hold first retainer-conversion review.

**Day 61–90 — Retainer + expansion preview**
- Convert to retainer if proof + value confirmed.
- Open `EXPANSION_MAP.md` and pre-select the next capability sprint.
- Add the second sprint to this roadmap with target date.
- Begin contributing learnings to `docs/company/CAPABILITY_FACTORY_MAP.md`.

## 12-month view
| Quarter | Capability focus | Outcome | Dealix offer |
|---|---|---|---|
| Q1 | `<capability>` | First proof + retainer | Sprint → Retainer |
| Q2 | `<capability>` | Second capability sprint, governance baseline | Sprint + Governance pack |
| Q3 | `<capability>` | Cross-capability workflow live | Workflow productization |
| Q4 | `<capability>` | Enterprise AI OS pilot scope agreed | Enterprise tier |

## Long-term Enterprise AI OS view
By month 18, `<CLIENT_NAME>` should be running on at least four
capabilities at Level 4+ with one capability at Level 5 (productized
OS). At that point, this client is a reference for the Dealix
Enterprise tier (`docs/enterprise/ENTERPRISE_GOVERNANCE_LAYER.md`) and
a candidate for vertical productization
(`docs/growth/PROOF_TO_RETAINER_SYSTEM.md`).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Capability scorecard, value dashboard | Roadmap revisions | CSM Lead | Monthly |
| Sprint proof packs | New 30/60/90 entries | Delivery Lead | Per sprint |
| Retainer review | 12-month view update | CSM + Account Director | Quarterly |
| Strategy refresh (`docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`) | Long-term view adjustments | CSO | Quarterly |

## Metrics
- **Level moves per quarter** — sum of capability level increases.
- **Sprint-to-retainer conversion** — % of first sprints that convert.
- **Time to second sprint** — days from first proof to second sprint signed.
- **Roadmap drift** — variance between planned and delivered sprints.

## How to fill this
1. Sit with the client owner and the Dealix CSM together; do not
   fill alone.
2. Pull current levels from `CAPABILITY_SCORECARD.md` — never invent.
3. For each capability gap, pick the **smallest** sprint that proves
   one level of movement.
4. Keep the 12-month view to one capability focus per quarter; resist
   stacking.
5. Review monthly during retainer cadence; archive the previous
   version in a dated note.

## Related
- `docs/company/CAPABILITY_OPERATING_MODEL.md` — capability vocabulary
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — level definitions
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability-to-value mapping
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
