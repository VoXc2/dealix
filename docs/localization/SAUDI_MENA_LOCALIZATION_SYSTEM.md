# Saudi/MENA Localization System — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Localization
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SAUDI_MENA_LOCALIZATION_SYSTEM_AR.md](./SAUDI_MENA_LOCALIZATION_SYSTEM_AR.md)

## Context
Dealix's category advantage in MENA rests on doing what global AI vendors
cannot — operate inside Saudi and Gulf business norms. This file defines
the localization areas Dealix actively manages and the quality rule that
Arabic output is business-native, not translation. It complements
`docs/strategic/DEALIX_MARKET_DIFFERENTIATION_AR.md`, the ZATCA work in
`docs/INVOICING_ZATCA_READINESS.md`, and PDPL guardrails in
`docs/ops/PDPL_RETENTION_POLICY.md`.

## Localization areas

- **Arabic business tone** — formal vs semi-formal, executive vs sales.
- **Bilingual executive reporting** — parallel structure, identical numbers,
  matching tone.
- **Local sales etiquette** — opening, follow-up cadence, greetings.
- **Sector-specific terms** — finance, government, retail, real estate.
- **City/region awareness** — local references and naming conventions.
- **PDPL-aware data handling** — lawful basis, retention, transfer rules.
- **WhatsApp sensitivity** — service vs cold; consent always required for
  outbound.
- **Formal vs semi-formal tone** — pick by audience and channel.

## Quality rule

> Arabic output is **not translation**; it must be **business-native**.

This rule is enforced by the tone library
(`docs/localization/ARABIC_TONE_LIBRARY.md`) and by the Quality as Code
discipline (`docs/product/QUALITY_AS_CODE.md`).

## Operating practices

- All client-facing artifacts ship in EN + AR with the same content.
- A native Arabic reviewer signs every external Arabic artifact.
- Tone is selected per piece (executive / sales / support).
- Arabic numerals follow local convention; dates follow Hijri/Gregorian
  per client.

## Anti-patterns

- Machine-literal Arabic.
- Mixed code-switching in formal executive reports.
- "Translate later" — Arabic added at the end without tone review.
- Western-style outbound applied to Gulf channels.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client artifact draft | Bilingual artifact | Reporting Agent + reviewer | Per artifact |
| Sector context | Term recommendations | Localization owner | Per engagement |
| Tone library | Per-piece tone selection | Reviewer | Per artifact |
| Reviewer feedback | Library updates | Localization owner | Monthly |

## Metrics
- Bilingual Parity — % of artifacts shipped EN + AR.
- Native-Tone Pass Rate — % passing reviewer first time.
- Sector Term Coverage — % of sector-specific terms found in library.
- Translation-Style Defects — defects per 100 Arabic artifacts.

## Related
- `docs/strategic/DEALIX_MARKET_DIFFERENTIATION_AR.md` — market differentiation
- `docs/INVOICING_ZATCA_READINESS.md` — ZATCA readiness
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL posture
- `docs/localization/ARABIC_TONE_LIBRARY.md` — tone library
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
