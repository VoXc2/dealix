# Capability Scorecard — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** CSM Lead — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [CAPABILITY_SCORECARD_AR.md](./CAPABILITY_SCORECARD_AR.md)

## Context
The scorecard is the **single source of truth** for where
`<CLIENT_NAME>` sits today on the six Dealix capabilities. It feeds
`CAPABILITY_ROADMAP.md`, `EXPANSION_MAP.md`, and the company-wide
capability factory map (`docs/company/CAPABILITY_FACTORY_MAP.md`). All
scores are evidence-led — no opinion-only ratings. Vocabulary and
level definitions come from
`docs/company/CAPABILITY_MATURITY_MODEL.md` and
`docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md`.

## Header
- **Client:** `<CLIENT_NAME>` · `<SECTOR>` · `<CITY>`
- **Assessed by:** `<OWNER_NAME>` + `<client owner>`
- **Assessment date:** `<YYYY-MM-DD>`
- **Method:** `docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md`
- **Next review:** `<YYYY-MM-DD>` (monthly)

## Level definitions (shared)
| Level | Name | Definition |
|---|---|---|
| 0 | Absent | Capability does not exist |
| 1 | Manual | Done by people, no system, no metrics |
| 2 | Structured | Documented process, spreadsheets, basic metrics |
| 3 | AI-Assisted | AI used in parts, human still owns the loop |
| 4 | Governed Workflow | AI in a controlled workflow with HITL and audit |
| 5 | Optimized OS | Capability runs as a productized OS, evidence-led |

## Scorecard
| Capability | Level (0–5) | Score (0–100) | Evidence (link) | Risk | Next action |
|---|---|---|---|---|---|
| Revenue | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<sprint / fix / handoff>` |
| Customer | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<>` |
| Operations | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<>` |
| Knowledge | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<>` |
| Data | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<>` |
| Governance | `<0–5>` | `<0–100>` | `<link>` | `<low / med / high>` | `<>` |

**Score formula:** Score = Level × 20, adjusted ±5 for evidence
strength and risk. Example: Level 2 with strong evidence = 45;
Level 3 with weak evidence = 55. CSM Lead reconciles edge cases.

## Per-capability notes

### Revenue — `<level>` / `<score>`
- **What's working:** `<one or two lines>`
- **What's missing:** `<one or two lines>`
- **Evidence:** `<links: pipeline reports, CRM screenshots, win/loss>`
- **Risk note:** `<commercial risk if not addressed>`
- **Next action:** `<sprint or retainer task>`
- **Blueprint:** `docs/capabilities/revenue_capability.md`

### Customer — `<level>` / `<score>`
- **What's working:** `<>`
- **What's missing:** `<>`
- **Evidence:** `<helpdesk metrics, CSAT, NPS>`
- **Risk note:** `<>`
- **Next action:** `<>`
- **Blueprint:** `docs/capabilities/customer_capability.md`

### Operations — `<level>` / `<score>`
- **What's working:** `<>`
- **What's missing:** `<>`
- **Evidence:** `<workflow logs, SLAs, runbooks>`
- **Risk note:** `<>`
- **Next action:** `<>`
- **Blueprint:** `docs/capabilities/operations_capability.md`

### Knowledge — `<level>` / `<score>`
- **What's working:** `<>`
- **What's missing:** `<>`
- **Evidence:** `<SOP inventory, search analytics>`
- **Risk note:** `<>`
- **Next action:** `<>`
- **Blueprint:** `docs/capabilities/knowledge_capability.md`

### Data — `<level>` / `<score>`
- **What's working:** `<>`
- **What's missing:** `<>`
- **Evidence:** `<data quality report, coverage map>`
- **Risk note:** `<>`
- **Next action:** `<>`
- **Blueprint:** `docs/capabilities/data_capability.md`

### Governance — `<level>` / `<score>`
- **What's working:** `<>`
- **What's missing:** `<>`
- **Evidence:** `<audit log, HITL stats, PDPL register>`
- **Risk note:** `<>`
- **Next action:** `<>`
- **Blueprint:** `docs/capabilities/governance_capability.md`

## Overall view
- **Composite score (avg of 6):** `<0–100>`
- **Tier alignment:** `<Tier 1 / Tier 2 / Tier 3>` (per
  `docs/company/OFFER_ARCHITECTURE.md`)
- **Strongest capability:** `<capability>`
- **Weakest capability:** `<capability>`
- **Greatest leverage move (sprint with highest ROI):** `<sprint>`

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Diagnostic assessment | Initial scorecard | CSM + capability owner | Engagement start |
| Sprint outputs, eval data | Score updates | Delivery Lead + CSM | Monthly |
| `EXPANSION_MAP.md`, `CAPABILITY_ROADMAP.md` | Triggered re-scoring | CSM Lead | Per sprint close |
| QBR | Tier alignment review | Account Director | Quarterly |

## Metrics
- **Evidence completeness** — % of capability rows with valid link.
- **Score reliability** — divergence between Dealix and client owner
  scores (target ≤ 1 level).
- **Re-scoring cadence** — % of months with on-time re-score.
- **Capability movement** — sum of level moves over last 90 days.

## How to fill this
1. Run the assessment with the client owner using
   `docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md`.
2. Score only what is **evidenced**. If no evidence, the score is
   capped at the level below.
3. Update monthly during the retainer review. Never raise a score
   without a new piece of evidence.
4. Use red-flag rules: any capability with Risk = high gets surfaced
   at the next monthly review, regardless of level.

## Related
- `docs/company/CAPABILITY_MATURITY_MODEL.md` — level definitions
- `docs/services/ai_ops_diagnostic/CAPABILITY_ASSESSMENT.md` — method
- `docs/company/CAPABILITY_FACTORY_MAP.md` — cross-client map
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
