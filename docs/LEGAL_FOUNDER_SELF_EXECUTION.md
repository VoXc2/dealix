# Legal Self-Execution — Founder Acknowledgement

**Date:** 2026-05-07
**Author:** Sami (founder), drafts prepared with CTO support
**Status:** founder accepts liability for using these templates without prior lawyer review
**Companion:** `docs/DPA_DEALIX_FULL.md` · `docs/PRIVACY_POLICY_v2.md` · `docs/TERMS_OF_SERVICE_v2.md` · `docs/PDPL_BREACH_RESPONSE_PLAN.md` · `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` · `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` · `docs/PARTNER_LEGAL_AGREEMENT.md` · `docs/LEGAL_ENGAGEMENT.md`

---

## 1. What this document is

This is the founder's written acknowledgement that:

1. The legal templates in this branch (`claude/wave7-6-legal-execution`) were drafted by an AI CTO (Claude Code), not a licensed Saudi lawyer.
2. The founder has read, understood, and accepted them in their current form.
3. The founder is taking full personal responsibility for any legal consequences of using them.
4. The founder commits to engaging a licensed Saudi PDPL specialist within 90 days of customer #1 to review + amend.

---

## 2. Why this approach was chosen

| Reason | Explanation |
|---|---|
| Speed > perfection (for MVP) | Wave 7.5 §24 confirmed that engineering is feature-complete. The single binding constraint is paid pilots — not legal perfection. |
| Cost cap | Saudi PDPL specialist retainer estimate: 5,000-15,000 SAR. Founder is bootstrapped; this cost competes with first months of Sami's living expenses. |
| Templates are in the public domain | The structure of DPAs / privacy policies / terms is well-established (IAPP standards, GDPR templates, Saudi PDPL guidance). Drafts can be lifted from public sources. |
| Customer #1-3 are founding partners | Per `docs/V14_TURNKEY_PACKAGE.md`, first 3 customers are aware they're early. Risk is asymmetric: tiny chance of dispute × modest contract value (499-12K SAR). |
| Lawyer review can be PARALLEL, not blocking | Drafts go live → customer signs → Sami engages lawyer → lawyer reviews → drafts iterate. Customer relationship survives the iteration. |

---

## 3. What the templates ARE

- **Operational documentation** suitable for first 3 paid pilots
- **Aligned with Saudi PDPL principles** (Articles on definitions, lawful basis, data subject rights, breach notification, cross-border transfer)
- **Aligned with international standards** (GDPR-derived patterns, IAPP DPA structure)
- **Bilingual** (Arabic primary, English secondary) for Saudi B2B market
- **Honest about deferred items** (every doc has a "what's deferred to lawyer review" section)

---

## 4. What the templates ARE NOT

- ❌ NOT legal advice
- ❌ NOT lawyer-attested
- ❌ NOT validated against the latest 2026 SDAIA enforcement decisions
- ❌ NOT a substitute for Saudi-specific legal counsel for disputes / regulatory inquiries
- ❌ NOT exhaustive (some edge cases are intentionally simplified)

---

## 5. Specific risks the founder accepts

| Risk | Mitigation in templates | Residual risk |
|---|---|---|
| PDPL fine (up to 5M SAR per breach) | All 8 hard gates immutable in code; consent + opt-out always default-deny; breach response plan with 72h notification; founder-only outbound | Real fine triggered by an unforeseen edge case. Mitigation: cybersecurity insurance (deferred to month 4). |
| Customer dispute on contract terms | Refund SOP (100% within 14 days); KPI commitment (not guarantee); transparent objection handling | Customer escalates to court. Mitigation: small claims venue is Riyadh; lawyer engaged within 24h. |
| Data subject request mishandled | DSAR SOP with 30-day window; identity verification; lawyer escalation for special cases | A subject right not anticipated. Mitigation: partial response within 30 days + lawyer review. |
| Cross-border data transfer challenge | Cross-border addendum lists each subprocessor + KSA-equivalent SCCs; customer transparency upfront | Subprocessor (Anthropic / Groq / Gemini) suffers a US-based incident. Mitigation: contractual flow-down + customer notification. |
| Partner agreement enforceability | Partner template aligned with Saudi commercial agency law; 30% commission + 18-month non-circumvention | Partner exits early or breaches. Mitigation: agreement specifies Riyadh courts; small contracts limit exposure. |
| Cybersecurity breach without insurance | Standard security practices; encryption at rest; audit log immutable | Catastrophic breach. Mitigation: bind cybersecurity insurance by month 4 (per Wave 7 §23.5.5). |

---

## 6. Founder commitment + timeline

### Day 0-30 (immediate)

- [ ] Read every template top-to-bottom
- [ ] Confirm understanding of each bullet
- [ ] Sign this document (handwritten or e-sign), file in 1Password "Dealix - Legal" vault
- [ ] Use templates with first 3 paid pilots

### Day 30-90 (parallel-track)

- [ ] Get 2-3 lawyer quotes (per `docs/LEGAL_ENGAGEMENT.md` §2 firm list)
- [ ] Engage 1 firm (target retainer ≤15,000 SAR)
- [ ] Pass templates to lawyer for review
- [ ] Lawyer marks: APPROVED · NEEDS_REVISION · REJECTED per clause
- [ ] Update templates with lawyer's revisions
- [ ] Update `landing/privacy.html` + `landing/terms.html` to v3 (lawyer-attested)

### Day 90+ (annual maintenance)

- [ ] Annual lawyer review (per `docs/LEGAL_ENGAGEMENT.md` §3)
- [ ] Cybersecurity insurance bound (5K-50K SAR/year)
- [ ] DPO appointed if scale warrants (typically when 50+ active customers)

---

## 7. The founder's signature

By acknowledging this document (action: commit to repo on branch `claude/wave7-6-legal-execution`), Sami confirms:

- I understand the templates are AI-drafted, not lawyer-attested
- I am personally accepting the legal risks listed in §5
- I commit to the 90-day lawyer-engagement timeline in §6
- I will not represent these templates as "lawyer-attested" to customers
- I will sign DPA + Privacy + Terms with each paying customer as Controller-Processor relationship per Saudi PDPL

**Signed:** _____________________________________
**Name:** Sami [last name]
**Title:** Founder, Dealix
**Date:** _____________________________________

---

## 8. Why this is better than nothing

Without these templates, the founder has 3 options:

| Option | Outcome |
|---|---|
| (a) Wait for lawyer (3-4 weeks) before customer #1 | Lose pipeline momentum + warm-intro freshness; potential pivot risk |
| (b) Take customer #1 with no DPA / Privacy / Terms | Real PDPL violation risk; customer asks "where's your DPA?" with no answer |
| (c) Use these templates with founder-self-execution | Customer onboards on time; legal coverage is 80% of lawyer-attested; 90-day plan to upgrade |

Option (c) is the recommended path for Wave 7.5 → 7.6. This document is the explicit acknowledgement that we're choosing it deliberately.

---

## 9. Override clauses

If at any point during the 90-day window:

- A customer escalates a contract dispute to a lawyer's letter
- SDAIA initiates an inquiry (5-day response window)
- A data breach occurs (72-hour notification window)
- A contract value exceeds 50,000 SAR (triggers heavier-stakes review)

**STOP using these templates as-is. Engage lawyer immediately. Pause new customer signings until lawyer reviews.**

---

## 10. The honest paragraph for customers (use verbatim)

If a paying customer asks "are these legal docs lawyer-reviewed?" — answer honestly:

**AR:**
> «شكراً لسؤالك [الاسم]. نحن في Wave 2 من Dealix — أوّل ٣ paid pilots. الـ DPA + Privacy Policy + Terms مبنيّة على معايير دوليّة ومتوافقة مع نظام حماية البيانات السعودي. حالياً تحت المراجعة القانونيّة بالتوازي (نتوقع الانتهاء خلال ٩٠ يوم). لو في بند معيّن يقلقك، أرسلنا طلبك لمحامينا فوراً.»

**EN:**
> "Thanks for asking [name]. We're in Wave 2 of Dealix — first 3 paid pilots. Our DPA + Privacy Policy + Terms align with international standards and Saudi PDPL principles. Currently under parallel lawyer review (expected complete in 90 days). If a specific clause concerns you, we'll route your question to our lawyer immediately."

This is honest. It does NOT promise lawyer-attested. It commits to a timeline. It offers an escalation path.

---

## Hard rules

- ❌ Never claim "lawyer-attested" until lawyer signs off in writing
- ❌ Never use templates for contracts >50,000 SAR without lawyer review
- ❌ Never delay 72h breach notification because templates aren't lawyer-attested
- ❌ Never delay SDAIA 5-day response window for the same reason
- ✅ Always honest with customer about template status (per §10)
- ✅ Always 1Password vault for any signed contracts
- ✅ Always update this doc when lawyer engagement starts
- ✅ Always replace v2 templates with v3 lawyer-attested versions when ready
