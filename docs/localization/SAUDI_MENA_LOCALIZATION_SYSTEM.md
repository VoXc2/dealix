# Saudi / MENA Localization System

> Dealix's Arabic-first quality is not "translation". It is a **product
> feature** measured, evaluated, and enforced. Customers in Saudi and MENA
> can tell the difference within 30 seconds of reading any output.

## Localization areas (each is scored at QA)

| Area | What it means |
|------|---------------|
| **Arabic business tone** | فصحى رسمية suitable for Saudi enterprise readers — not literal MT, not colloquial. |
| **Bilingual executive reporting** | Every executive artifact has AR + EN sections that match in meaning, not in word-count. |
| **Local sales etiquette** | Greetings, hierarchy awareness, formal vs semi-formal cues. |
| **Sector terminology** | BFSI vocabulary differs from healthcare differs from logistics. Use the right one. |
| **City / region awareness** | Riyadh vs Jeddah vs Eastern — phrasing and context differ. |
| **PDPL-aware language** | Consent / lawful basis terms used correctly in Arabic. |
| **WhatsApp sensitivity** | Different tone from email; tighter; never spammy. |
| **Formal vs semi-formal modes** | Executive AR (formal) vs operations AR (clearer, shorter sentences). |

## The hard rule

> Arabic output is not translation. It must be business-native.

A literal Google-Translate-style Arabic output fails QA's Arabic gate. The
review question is: *"would a Saudi business reader send this themselves?"*
If no → revise. If yes → ship.

## Tone Library (see `ARABIC_TONE_LIBRARY.md`)

Pre-approved tone modes:

- **Executive Formal** — CEO reports, governance docs, board-level summaries.
- **Sales Professional** — outreach drafts, proposals, follow-ups.
- **Support Friendly** — customer replies, FAQ entries.
- **Operations Direct** — runbooks, SOPs, internal notes.

Each mode has example openings, closings, and forbidden phrases.

## Forbidden Arabic patterns (auto-flagged by `dealix/trust/forbidden_claims.py`)

- مبالغة (exaggeration without evidence).
- "نضمن" / "أفضل" / "الأقوى" / "الوحيد" / "100%" — any guaranteed-outcome claim.
- ترجمة حرفية للمصطلحات الإنجليزية حين توجد مقابلات سعودية أعمالية واضحة.
- لغة سبام (multiple exclamation marks, urgency tricks, fake scarcity).
- وعود غير مثبتة (unproven promises).
- استخدام لهجة عامية في سياق تنفيذي.

## Bilingual layout rule

For every customer-facing artifact:

1. AR section comes first (audience-first ordering for Saudi enterprise).
2. EN section follows.
3. Same meaning — not same length. AR is typically shorter for the same content.
4. Tables use bilingual labels (AR / EN) per column header.
5. Numbers, dates, currencies in AR section use Arabic-numeral form (1, 2, 3) for clarity in business contexts.

## QA enforcement

Per `docs/quality/QUALITY_REVIEW_BOARD.md` AI QA gate, every output is scored on Arabic Quality (15 / 100 weight). Below 12/15 → REVISE. Hard Fail on:

- PII surfacing.
- Forbidden claim language.
- Wrong register (e.g., colloquial in an executive report).
- Inconsistency between AR and EN versions.

## Why this matters

90% of global AI tools produce Arabic that reads like translation. The Saudi enterprise buyer can tell. **Arabic-first is a moat** — it takes years to build, costs almost nothing to maintain once tone library + forbidden-claims filter are in place, and it's invisible to competitors until they lose deals over it.

## Cross-links
- `docs/localization/ARABIC_TONE_LIBRARY.md` (below)
- `docs/quality/ARABIC_QUALITY_GUIDE.md` (Wave 4)
- `docs/localization/bilingual_operating_assets.md` (W3.T20)
- `dealix/trust/forbidden_claims.py`
- `docs/strategy/CATEGORY_DESIGN.md` — Arabic-first as a category claim
