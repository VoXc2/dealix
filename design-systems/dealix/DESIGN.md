# Dealix Design System — DESIGN.md

> Bilingual specification for the Dealix DesignOps surface.
> Saudi-first, Arabic-primary, English-secondary, evidence-first,
> approval-gated, no marketing claims that the service registry cannot prove.

---

## 1. Arabic-first Principles (RTL by default)

- **Default direction:** All customer-facing artefacts render in `dir="rtl"`
  with `lang="ar"`. English sub-blocks switch locally to `dir="ltr"`
  via `<section lang="en" dir="ltr">…</section>` only.
- **Reading order:** Arabic first (top of section), English second
  (sub-block under it). Never side-by-side columns on mobile.
- **Numerals:** Arabic-Indic numerals (٠١٢٣٤٥٦٧٨٩) allowed in Arabic
  prose; ASCII digits in tables/KPIs for parseability.
- **Punctuation:** Arabic comma `،` and Arabic question mark `؟`
  in Arabic blocks. Never mix.
- **Mirroring:** Status chips, evidence badges, and table arrows
  mirror under RTL. Icons that have semantic direction (forward,
  back) use logical CSS (`margin-inline-start`, not `margin-left`).
- **Tone:** Saudi-executive, calm, precise. No hype. No emojis in
  shipped artefacts unless the founder explicitly approves a pattern.

## 2. Color Tokens (named, not raw hex outside tokens)

| Token name        | Role                                            | Light     | Dark      |
|-------------------|-------------------------------------------------|-----------|-----------|
| `primary`         | Saudi green; primary actions, brand anchor      | #0A5C36   | #1F8A5A   |
| `accent`          | Sand-gold; highlights, executive accents        | #C8A86A   | #E0BE7C   |
| `success`         | Live / approved / proven                        | #1F8A5A   | #2BB07A   |
| `warn`            | Pilot / partial / needs attention               | #C28A1F   | #E0A744   |
| `block`           | Blocked / forbidden / requires approval         | #B23A3A   | #D45656   |
| `surface`         | Page background                                 | #FAFAF7   | #0E1311   |
| `surface-alt`     | Card / table-row alternate                      | #F1EFE8   | #161D1A   |
| `text-primary`    | Body / headings                                 | #14201A   | #ECEFEC   |
| `text-muted`      | Captions, helper, evidence small print          | #5A6661   | #9CA8A2   |
| `text-inverse`    | Text on `primary` / `block` fills               | #FFFFFF   | #0E1311   |

> Rule: components reference token *names*. Raw hex appears only in
> the token table above and the generated CSS variables.

## 3. Typography Tokens

| Token         | Family                                | Size  | Weight | Line-h |
|---------------|---------------------------------------|-------|--------|--------|
| `heading-ar`  | "IBM Plex Sans Arabic", system-ar     | 28px  | 600    | 1.35   |
| `heading-en`  | "Inter", system-ui                    | 26px  | 600    | 1.30   |
| `body-ar`     | "IBM Plex Sans Arabic", system-ar     | 16px  | 400    | 1.70   |
| `body-en`     | "Inter", system-ui                    | 15px  | 400    | 1.60   |
| `mono`        | "JetBrains Mono", ui-monospace        | 13px  | 400    | 1.55   |

- Arabic line-height is intentionally taller (1.70) for diacritic safety.
- Mono is reserved for evidence IDs, hashes, version stamps.
- All families have local-system fallbacks; no external font CDNs.

## 4. Spacing Scale

`4 / 8 / 12 / 16 / 24 / 32 / 48` (px)

- 4 — hairline gaps inside chips/badges
- 8 — chip→label, icon→text
- 12 — input row gaps
- 16 — paragraph rhythm, card inner padding
- 24 — section breathing inside a card
- 32 — between cards
- 48 — between major page regions

## 5. Component Recipes

### 5.1 KPI tile
- Container: `surface-alt`, radius 12, padding 24.
- Big number: `heading-ar` (or `heading-en` for English block); color `text-primary`.
- Label below in `body-ar` / `body-en`, color `text-muted`.
- Optional evidence badge at the bottom-end (logical end under RTL).
- Forbidden: trend arrows that imply growth without an evidence link.

### 5.2 Evidence badge
- Pill, height 24, padding-inline 8, radius 12.
- Background `surface-alt`, border 1px `text-muted`.
- Text `mono`, format `EVT-<id>` or `INV-<id>` or `PROOF-<id>`.
- Always links to the proof ledger record. Never decorative.

### 5.3 Safety badge
- Pill, height 24, padding-inline 8, radius 12.
- States: `Approval Required` (color `block`), `PDPL-redacted`
  (color `warn`), `Internal Only` (color `text-muted`).
- Never auto-removed. Removal requires human approval action.

### 5.4 Status chip
- Inline pill, height 22, padding-inline 8, radius 11.
- Solid fill from the token map below; text `text-inverse` or
  contrast-checked `text-primary`.
- Canonical names (must match exactly):
  - `Live`              — `success`
  - `Pilot`             — `warn`
  - `Partial`           — `warn`
  - `Target`            — `accent`
  - `Blocked`           — `block`
  - `Approval Required` — `block`
  - `Draft Only`        — `text-muted`
  - `Internal Only`     — `text-muted`

### 5.5 Approval pill
- Slightly larger than a status chip (height 28).
- Always co-located with the artefact's primary action.
- Default state for any send/publish action: `Approval Required`.
- Cannot be disabled by configuration.

### 5.6 Table
- Header row: `surface-alt`, `body-ar/en` 600 weight.
- Body rows: alternate `surface` / `surface-alt`.
- Sticky header from 720px upward; on mobile it scrolls.
- Numeric columns right-aligned in LTR, start-aligned in RTL
  (handled via `text-align: end`).

### 5.7 CTA button
- Primary: fill `primary`, text `text-inverse`, radius 10.
- Secondary: outline 1px `primary`, fill transparent.
- Destructive / approval-blocking: outline 1px `block`,
  text `block`. Never solid red — solid red is reserved for
  the safety badge.
- Disabled state never silent — always paired with a one-line
  reason (e.g. "approval required", "evidence missing").

## 6. Status Chip Names (canonical)

The following eight names are the *only* permitted status chip
labels. Localisation strings exist for each but the token name is
fixed in code:

`Live`, `Pilot`, `Partial`, `Target`, `Blocked`,
`Approval Required`, `Draft Only`, `Internal Only`

## 7. Forbidden Copy List (verbatim)

The following strings must never appear in a *positive* (asserted,
non-negation) context inside any rendered artefact, page, email,
proposal, deck, or dashboard:

- `نضمن`
- `guaranteed`
- `blast`
- `scrape`
- `cold WhatsApp`
- `revenue guaranteed`
- `ranking guaranteed`
- `fully automated external send`

A negation context — for example, "Dealix never does
*fully automated external send*" — is permitted, must be
allowlisted in `tests/test_landing_forbidden_claims.py`, and
stays under founder review.

## 8. Mobile-first Patterns

- Base width: `max-width: 720px`, centred.
- Below 560px: single column, stack KPI tiles vertically, hide
  decorative side-rails, keep status chips inline with their row.
- Tap targets: minimum 44×44 px.
- Tables: convert to stacked key/value list under 560px.
- All numbers and evidence badges remain visible at the smallest
  breakpoint — they are never the first thing dropped.

## 9. Saudi Executive Trust — tone notes

- Open with the *outcome* (one line), then the *evidence*
  (badge + link), then the *next step* (CTA with approval state).
- Use specific numbers from the proof ledger; never round up to a
  marketing-friendly figure.
- Avoid hype verbs. Prefer: "delivered", "verified", "approved",
  "in pilot", "blocked pending review".
- Bilingual rule: any external-facing string must have both
  Arabic and English. Internal-only screens may be English-only,
  flagged with the `Internal Only` chip.
- Evidence-first: every customer-facing claim links to a proof
  ledger record. Pages without a record cannot ship the claim.
