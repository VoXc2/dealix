# Arabic Tone Library — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Localization
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ARABIC_TONE_LIBRARY_AR.md](./ARABIC_TONE_LIBRARY_AR.md)

## Context
Arabic output is the most visible expression of Dealix's localization
quality. This library defines the three primary tones, what each is for,
the writing rules they share, and the things to avoid. It is referenced
by the Reporting Agent, Outreach Agent, and the broader Localization
System in
`docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md`, and is grounded in
the brand voice in `docs/BRAND_PRESS_KIT.md` and the design system in
`docs/DEALIX_DESIGN_LANGUAGE.md`.

## Tones

- **Executive Formal** — CEO reports, board summaries, regulatory
  communication.
- **Sales Professional** — outreach drafts, proposals, follow-ups.
- **Support Friendly** — customer replies, helpdesk, post-sale.

## Shared writing rules

- Lead with the decision or the value, not the preamble.
- Cite numbers with units; never round without source.
- Use sector-correct terms; prefer the precise word over the generic.
- Keep sentences medium length; avoid English transliteration unless it
  is the standard term.
- Match the formality of the audience.

## Things to avoid (forbidden patterns)

- مبالغة (exaggeration).
- ضمان نتائج (guaranteed-result language).
- لغة سبام (spam-style writing).
- ترجمة حرفية (literal machine translation).
- وعود غير مثبتة (unproven promises).

These map to executable Compliance Guard rules in
`docs/product/GOVERNANCE_AS_CODE.md`.

## Per-tone notes

### Executive Formal
- Open with a one-line decision.
- Numbers in a small table when possible.
- Closing line is a next action with an owner.

### Sales Professional
- Personal, respectful, brief.
- Reference a relevant signal (event, prior conversation).
- One clear call-to-action.

### Support Friendly
- Acknowledge the issue first.
- Offer a concrete next step.
- Sign with the team identity.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Audience + channel | Recommended tone | Reviewer | Per artifact |
| Draft text | Tone-passing edit | Reviewer | Per artifact |
| Forbidden-pattern detection | Block / rewrite | Compliance Guard | Per draft |
| Reviewer feedback | Library updates | Localization owner | Monthly |

## Metrics
- Tone Selection Accuracy — % of artifacts using the right tone.
- Forbidden Pattern Rate — instances per 100 artifacts.
- Reviewer First-Pass Rate — % approved on first review.
- Localization Defect Escape — defects found post-delivery.

## Related
- `docs/BRAND_PRESS_KIT.md` — brand voice
- `docs/DEALIX_DESIGN_LANGUAGE.md` — design language
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` — operating context
- `docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md` — localization system
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
