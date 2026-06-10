# Agent #14 — Saudi Localization Gap Audit

**Date:** 2026-06-03
**Auditor:** Agent #14 (Saudi Localization & Arabic Experience)

---

## 1. Executive Summary

The repo has **two skeleton docs** (`ARABIC_TONE_LIBRARY.md` and
`SAUDI_MENA_LOCALIZATION_SYSTEM.md`) and a small set of Arabic content
templates. The system has **no formal glossary, no brand-voice guide, no
proposal-style guide, no WhatsApp UX rules in Arabic, and no
bilingual-style consistency rules**. Agent #14 is therefore not
"translating" — it is **codifying the language standards** that every
client-facing artifact must follow.

## 2. Existing Inventory

| File | Lines | Status | Gap |
| --- | --- | --- | --- |
| `docs/localization/ARABIC_TONE_LIBRARY.md` | 21 | skeleton | Needs tone specifics per context |
| `docs/localization/SAUDI_MENA_LOCALIZATION_SYSTEM.md` | 18 | skeleton | Needs sectors + cities + PDPL wording |
| `data/templates/warm_intro_whatsapp_ar.md` | exists | template | needs style enforcement |
| `data/templates/proposal_499_sar_ar.md` | exists | template | needs style enforcement |
| `data/templates/proof_pack_ar.md` | exists | template | needs style enforcement |
| `data/templates/whatsapp_templates_collection.md` | exists | collection | needs UX policy |
| `docs/WHATSAPP_OPERATOR_FLOW.md` | exists | operator flow | needs Arabic UX overlay |
| `docs/observability/posthog_dashboard.json` | exists | EN | needs AR labels |
| `frontend/` | exists | Next.js | needs AR locale review |

## 3. Missing

| Doc | Priority |
| --- | --- |
| `docs/localization/SAUDI_LOCALIZATION_OS_AR.md` | High — overall OS |
| `docs/localization/ARABIC_BRAND_VOICE_AR.md` | High — voice |
| `docs/localization/BILINGUAL_STYLE_GUIDE_AR.md` | High — AR/EN consistency |
| `docs/localization/SAUDI_B2B_TONE_GUIDE_AR.md` | High — formal/semi-formal rules |
| `docs/localization/WHATSAPP_ARABIC_UX_AR.md` | High — channel UX |
| `docs/localization/PROPOSAL_ARABIC_STYLE_AR.md` | High — proposal tone |
| `docs/localization/REPORTING_ARABIC_STYLE_AR.md` | Medium — report tone |
| `docs/localization/TERMINOLOGY_GLOSSARY_AR.md` | **Critical** — single source of truth for terms |
| `reports/localization/SAUDI_LOCALIZATION_REVIEW.md` | Medium — review |
| `reports/localization/LOCALIZATION_FINAL_REPORT.md` | Final |

## 4. Key Gaps

1. **No glossary.** The same concept (e.g. "approval") might be rendered
   as "اعتماد", "موافقة", "إقرار" inconsistently across the system. The
   agent definition has a starter glossary that should be promoted to
   `TERMINOLOGY_GLOSSARY_AR.md`.
2. **No sector-specific terminology.** KSA has 13+ regulated sectors; each
   has its own jargon (health: MoH, NPHIES; finance: SAMA, CMA; etc.).
3. **No brand voice decision.** Is Dealix "أنت" (informal) or "أنتم"
   (plural formal) or "حضرتك" (respectful)? Currently inconsistent.
4. **No WhatsApp UX rules.** WhatsApp in KSA is high-context, mobile-first,
   prefers short messages + lists, dislikes long paragraphs.
5. **No PDPL-aware Arabic privacy wording.** Standard Arabic privacy
   notices are either too academic or too Western.
6. **No SAR / Riyadh-time conventions** for date/time/price display.

## 5. Recommendations

1. **Phase 1 priority:** Glossary + Brand Voice + Saudi B2B Tone Guide.
2. **Phase 2 priority:** WhatsApp Arabic UX + Proposal Style + Reporting
   Style + Bilingual Style Guide.
3. **Phase 3 priority:** Saudi Localization OS synthesis + final report.
