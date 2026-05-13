# Arabic Business Quality — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CSO + Arabic Quality Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ARABIC_BUSINESS_QUALITY_AR.md](./ARABIC_BUSINESS_QUALITY_AR.md)

## Context

Arabic quality is the most under-served axis in Saudi B2B AI. Most
LLM output reads as literal translation, marketing exaggeration, or
broken register. Dealix wins or loses every enterprise deal on this
dimension. This file defines the modes, forbidden phrases, preferred
phrases, and the scoring rubric used inside Language QA layer of
`docs/quality/QA_SYSTEM.md`. It pairs with the brand voice in
`docs/BRAND_PRESS_KIT.md` and the design language in
`docs/DEALIX_DESIGN_LANGUAGE.md`.

## The 4 Modes

Every Arabic asset must be written in one of four modes. Mixing
modes is a fail.

| Mode | Use case | Tone |
|---|---|---|
| **Executive Formal** (تنفيذي رسمي) | Board decks, executive proposals, regulator letters | Formal, terse, evidence-led, no idioms |
| **Sales Professional** (مبيعات احترافية) | Proposals, sales pages, partner pitches | Confident, specific, outcome-language, no superlatives |
| **Support Friendly** (دعم ودود) | Client emails, CSM follow-ups, support replies | Warm, plain, problem-solving, respectful |
| **Technical Clear** (تقني واضح) | Internal docs, runbooks, technical responses | Precise, unambiguous, code/term in English when needed |

## Forbidden Phrases

These are blocked at QA. Their presence drops Language QA score by
20 points each.

| Phrase | Why it fails |
|---|---|
| نضمن لك | Guarantees results — contractual and regulatory risk |
| نتائج مضمونة | Same guarantee problem |
| أفضل نظام في العالم | Unverifiable superlative |
| ثوري / ثورة | Hype register, unprofessional in B2B Saudi |
| غيّر حياتك / غيّر شركتك | Spam register |
| بنقرة واحدة | Misrepresents complexity |
| الذكاء الاصطناعي السحري | Marketing fluff |
| أرخص سعر | Compete on margin, not price wars |
| ترجمة حرفية لمصطلحات إنجليزية | Reads broken |

## Preferred Phrases

The Dealix register prefers outcome-and-discipline language.

| Phrase | When to use |
|---|---|
| نرتب الفرص (we rank the opportunities) | Lead Intelligence outputs |
| نقيس الأثر (we measure impact) | Proof Pack and dashboards |
| نوضح الخطوة التالية (we clarify the next step) | Sales/CSM conversations |
| نخفض المخاطر (we reduce risk) | Governance and PDPL talk |
| ننتج Proof Pack (we produce a Proof Pack) | End-of-engagement |
| نحوّل البيانات إلى قرارات (we turn data into decisions) | Pitch language |
| نُمنتج العمل المتكرّر (we productize repeated work) | Retainer talk |
| ندير بالاعتماد (we operate with approval) | Enterprise / governance |

## Arabic QA Score Components

The Language QA layer in `docs/quality/QA_SYSTEM.md` computes the
Arabic score from these weighted components:

| Component | Weight | What it checks |
|---|---:|---|
| Clarity (وضوح) | 25 | Sentence length, parsability, terminology consistency |
| Tone (نبرة) | 20 | Mode matches the asset, no mode-mixing |
| Business fit (ملاءمة الأعمال) | 20 | Vocabulary fits the buyer (banking, retail, government, etc.) |
| Localization (توطين) | 15 | Saudi/Gulf register, dates, currency, names |
| No exaggeration (لا مبالغة) | 20 | No forbidden phrases, no superlatives, no hype |
| **Total** | **100** | |

Pass threshold: **≥ 85** on every client-visible Arabic artifact.

## Reviewer Checklist (Quick)

- [ ] Single mode throughout the document.
- [ ] No forbidden phrases present.
- [ ] At least one preferred phrase reflects the actual outcome.
- [ ] Saudi/Gulf register (الرياض instead of عمّان idioms, ريال
      sentence framing).
- [ ] Numbers and KPIs are in LTR cells when in tables; the prose is RTL.
- [ ] All product/technical terms have a consistent translation (or
      stay in English with first-mention clarification).
- [ ] No exaggeration or guarantee.
- [ ] Tone consistent with the destination audience.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Arabic client-visible artifacts | Language QA score, Required Fixes | Arabic Quality Reviewer | Per artifact |
| Style updates, new vertical vocabulary | Updated phrasebook | CSO | Quarterly |
| Reviewer disagreements | Style guide arbitration | CSO | As needed |

## Metrics

- **Arabic QA score (average)** — target ≥85.
- **% Arabic artifacts ≥85** — target 100% client-visible.
- **Forbidden-phrase incident rate** — target 0 in delivered work.
- **Mode-mixing incident rate** — target ≤2 per 100 artifacts.

## Related

- `docs/BRAND_PRESS_KIT.md` — brand voice.
- `docs/DEALIX_DESIGN_LANGUAGE.md` — design language sibling.
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` — master operating model in Arabic.
- `docs/strategic/DEALIX_MARKET_DIFFERENTIATION_AR.md` — market differentiation sibling.
- `docs/quality/QA_SYSTEM.md` — overall QA framework.
- `docs/quality/QUALITY_STANDARD_V1.md` — quality standard sibling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
