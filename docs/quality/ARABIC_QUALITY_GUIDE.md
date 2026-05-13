---
title: Arabic Quality Guide — Business Tone, Sector Terms, Forbidden Phrases
doc_id: W6.T36.arabic-quality
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W3.T20, W1.T01]
kpi:
  metric: ar_tone_eval_pass_rate
  target: 90
  window: rolling_28d
rice:
  reach: 0
  impact: 3
  confidence: 0.85
  effort: 1
  score: quality-localization
---

# Arabic Quality Guide

## 1. Context

Arabic is not a translation layer — it is the primary business language for
Saudi customers. Dealix's defensible position is *Saudi-localized AI*, which
means AR outputs must read as if a senior Saudi business writer composed them.
This guide is the operator standard for AR output quality.

## 2. Audience

Engineers writing prompts, content reviewers, CSMs proofreading reports,
HoCS approving release of customer-facing AR artifacts.

## 3. The Tone Bands

Three bands, mapped to buyer level:

| Band | Use case | Example traits |
|------|----------|---------------|
| **Formal MSA** (الفصحى الرسمية) | C-suite reports, government, BFSI exec | No colloquial, proper agreement, محرّر بأسلوب رسمي |
| **Business MSA** (الفصحى التجارية) | Mid-management reports, day-to-day correspondence | MSA grammar, business idioms, fewer literary flourishes |
| **Light Saudi Business** (مهنية مع نكهة محلية) | WhatsApp from CS, short status messages | MSA backbone, light Saudi expressions where natural; never colloquial alone |

Outreach defaults to Business MSA unless the sector playbook specifies
otherwise.

## 4. Sector Term Lookups

Each vertical playbook maintains a sector glossary. Engineers must use the
sector's preferred term — not a generic translation. Examples:

| Vertical | Generic EN | Sector AR (correct) | Generic AR (wrong) |
|----------|-----------|---------------------|--------------------|
| BFSI | "Onboarding" | استكمال المتطلبات | تأهيل |
| Retail | "Customer journey" | رحلة العميل | مسار العميل |
| Healthcare | "Patient" | المراجع / المريض (per sector) | الزبون |
| Real Estate | "Tenant" | المستأجر | السكان |
| Logistics | "Last-mile" | التسليم النهائي | الميل الأخير |

Sector glossaries live in `docs/strategy/` per-vertical files and in the
prompt library.

## 5. Forbidden Phrases

A hard "no" list enforced in code via `dealix/trust/forbidden_claims.py`.
Examples of banned AR terms (non-exhaustive — code is authoritative):

- أفضل / الأفضل / الأقوى (superlatives without proof)
- ضمان / نضمن (guarantees not contractually backed)
- 100% (unverifiable absolute claims)
- ربح مضمون / بدون مخاطر (guaranteed returns / risk-free)
- حصري / الوحيد (exclusivity claims)

Any AR output containing a forbidden phrase fails the AI gate and the
Compliance gate. The scan happens before send via `scan_text` and
`assert_clean`.

## 6. Required Practices

- **Numbers**: Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) in body text; Western digits
  acceptable in tables and financial figures. Be consistent within a
  document.
- **Names**: use the company's own AR rendering, not a guess.
- **Honorifics**: المهندس / الأستاذ / الدكتور when known.
- **Direction**: RTL throughout; mixed AR/EN runs use bidi-safe spacing.
- **Spelling**: maintain ة vs ه correctly; ى vs ي per MSA standard.

## 7. Review Workflow

1. Engineer drafts AR output via the prompt + sector glossary.
2. Second reviewer (a native AR business writer) edits for tone + sector
   fit. Cannot be the author.
3. `forbidden_claims.scan_text` runs as a pre-send check.
4. For customer-facing reports: HoCS final pass.

Sample rate for eval: 50 AR outputs per week through the second-reviewer
loop until rolling pass rate ≥ 90% for four consecutive weeks; then drop
to 20/week sample with rotating spot-checks.

## 8. Anti-Patterns

- **Machine-translate-then-ship**: never. AR is generated natively or
  edited by a native writer.
- **EN-as-source assumption**: customers see the AR first. Treat AR as
  primary, EN as companion.
- **Phrase blending**: mixing MSA and Saudi colloquial mid-sentence reads
  as careless. Pick a band per artifact.

## 9. Cross-links

- Forbidden claims code: `dealix/trust/forbidden_claims.py`
- AI evals: [`AI_OUTPUT_EVALS.md`](AI_OUTPUT_EVALS.md)
- Quality Standard: [`QUALITY_STANDARD.md`](QUALITY_STANDARD.md)
- Bilingual assets index: `docs/localization/`
- Vertical playbooks: `docs/strategy/`

## 10. Owner & Review Cadence

- **Owner**: HoCS (with native-speaker editor on retainer).
- **Review**: quarterly sector-glossary refresh; ongoing forbidden-phrase
  updates as the code list evolves.

## 11. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial AR tone bands + sector terms + forbidden phrases |
