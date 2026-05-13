# Expansion Map — <CLIENT_NAME>

**Layer:** Client Template · Operational Kit
**Owner:** Account Director — <OWNER_NAME>
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [EXPANSION_MAP_AR.md](./EXPANSION_MAP_AR.md)

## Context
The expansion map is the **disciplined upsell brain** for one client.
Every Dealix engagement starts narrow (one sprint, one proof). The
expansion map then translates the *kind* of proof produced into the
*next* best offer, instead of letting account teams improvise. It
plugs into the wider growth machine: `docs/growth/PROOF_TO_UPSELL_MAP.md`
defines the playbook in general, and this template is the per-client
instance. Timing is deliberately anchored to the monthly retainer
cadence call so we don't pitch faster than proof accumulates.

## Header
- **Client:** `<CLIENT_NAME>` · `<SECTOR>` · `<CITY>`
- **Account Director:** `<OWNER_NAME>`
- **Current tier:** `<SERVICE_TIER>`
- **Current ARR band:** `<ARR_BAND>`
- **Active proof artefact(s):** `<links to proof pack(s)>`

## Proof → next offer mapping
The matrix below is the **default routing**. Override only with a
written reason in the "decision log" section.

| Proof signal (from current sprint) | Next-best offer | Capability moved | Trigger to surface |
|---|---|---|---|
| Pipeline / revenue lift evidenced | Monthly RevOps OS retainer | Revenue 2→3 / 3→4 | Lift confirmed for 2 consecutive months |
| Lead quality + scoring delta | Lead Intelligence retainer | Revenue + Customer | Conversion lift ≥ 15% |
| Data quality / coverage gaps surfaced | Data OS retainer + Data Readiness | Data 1→3 | Diagnostic flagged > 30% gaps |
| Recurring support themes / SLA pressure | AI Support Desk retainer | Customer + Operations | Volume baseline + recurring themes |
| Knowledge / SOP fragmentation observed | Company Brain retainer | Knowledge 1→3 | More than 3 teams asking the same questions |
| Audit / approval friction observed | AI Governance Program | Governance 1→3 | First HITL exception or audit ask |
| Multi-team workflow bottleneck | Workflow productization sprint | Operations 3→4 | Two capabilities at L3+ touching same workflow |
| Repeat reference + case-study readiness | Enterprise tier upgrade | All capabilities | 3 proofs across 2 capabilities |

## Decision log
| Date | Signal observed | Recommended offer | Decision | Owner | Notes |
|---|---|---|---|---|---|
| `<YYYY-MM-DD>` | `<signal>` | `<offer>` | `<accepted / parked / declined>` | `<OWNER_NAME>` | `<note>` |

Add rows monthly during the retainer cadence call. Never delete rows —
parked offers re-surface in 90 days.

## Pricing and offer references
- Offer catalogue: `docs/company/OFFER_ARCHITECTURE.md`
- Sprint → retainer mechanics: `docs/growth/PROOF_TO_RETAINER_SYSTEM.md`
- Pricing bands: `docs/OFFER_LADDER_AND_PRICING.md`
- Retainer SLA: `docs/services/<sprint>/` per-service folders

## Timing discipline
Expansion conversations happen **only** at three moments:
1. **Proof checkpoint** (end of current sprint) — present the proof,
   *do not* pitch the next offer.
2. **Retainer cadence call** (monthly) — surface 1 (max 2) offers
   from the matrix above with the matching evidence.
3. **Quarterly business review** — set the next quarter's capability
   focus and lock the next sprint.

If the matching trigger has not fired, **wait**. Pitching without
trigger is logged as a discipline breach in the account note.

## Anti-patterns to avoid
- Pitching multiple offers in the same call.
- Pitching governance before any operational sprint has shipped.
- Pitching enterprise tier before 3 proofs across 2 capabilities.
- Pitching off the matrix without a written override.
- Bundling a discounted retainer to "close faster" — kills price
  integrity (`docs/UNIT_ECONOMICS_AND_MARGIN.md`).

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sprint proof pack | Recommended next offer | Account Director | Per sprint close |
| Value dashboard, scorecard | Decision log rows | CSM Lead | Monthly retainer call |
| QBR | Next-quarter capability focus | Account Director + Capability Owner | Quarterly |
| Win/loss data | Override patterns into `PROOF_TO_UPSELL_MAP.md` | Growth Lead | Quarterly |

## Metrics
- **Trigger-respect rate** — % of expansion pitches that follow a
  matrix trigger (target ≥ 90%).
- **Proof-to-pitch latency** — days from proof confirmed to offer
  surfaced (target ≤ 14).
- **Expansion close rate** — % of triggered offers signed within 60 days.
- **Net retention** — ARR_t+12 / ARR_t (target ≥ 1.25 for Tier 1 clients).

## How to fill this
1. Pre-fill header at engagement start.
2. After each sprint proof, add a decision-log row even if no offer
   surfaces — empty signals matter.
3. Use the matrix exactly; do not add bespoke offers without
   updating `docs/growth/PROOF_TO_UPSELL_MAP.md`.
4. Review with growth lead quarterly to identify pattern overrides.

## Related
- `docs/growth/PROOF_TO_UPSELL_MAP.md` — global proof-to-upsell rules
- `docs/growth/PROOF_TO_RETAINER_SYSTEM.md` — retainer mechanics
- `docs/company/OFFER_ARCHITECTURE.md` — offer catalogue
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
