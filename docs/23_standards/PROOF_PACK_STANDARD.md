# Proof Pack Standard

## معيار حزمة الإثبات

> Open Standard, version 1.0. Defines the fourteen-section schema, the scoring formula, and the tier classification that every project must produce at close.

A Proof Pack is the artifact that converts work into evidence. Every project — sprint, retainer month, sector engagement — produces exactly one Proof Pack, with a computed proof score and a tier classification. Without a Proof Pack, a project cannot be invoiced, referenced, or used to unlock the next rung.

The Dealix reference implementation lives in `auto_client_acquisition/proof_os/proof_pack.py`. The spec below is independent of that implementation; any equivalent assembler that produces the same sections, score, and tier on the same project state is conformant.

---

## 1. The fourteen sections — الأقسام الأربعة عشر

```
1.  Executive Summary
2.  Problem
3.  Inputs
4.  Source Passports
5.  Data Quality Score
6.  Work Completed
7.  Outputs
8.  Governance Decisions
9.  Blocked Risks
10. Observed Value
11. Limitations
12. Recommended Next Step
13. Retainer Recommendation
14. Capital Assets Created
```

Section content rules:

1. **Executive Summary** — one page maximum, bilingual where appropriate. Names the workflow owner, the headline outcome, the proof score, the tier.
2. **Problem** — the written problem statement the client agreed to at intake.
3. **Inputs** — the data, channels, and people involved. Counts only; no raw PII.
4. **Source Passports** — every passport used, listed by `source_id`, `source_type`, `owner`, `sensitivity`, `retention_policy`. See [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md).
5. **Data Quality Score** — the input-side DQ score: completeness, freshness, validity, passport coverage. A single number in `[0, 100]` with the breakdown shown.
6. **Work Completed** — the workflow steps actually executed, in order, with who or what executed each.
7. **Outputs** — the deliverables (ranked accounts, drafts, reports). Each output carries a `source_ref` back to a passport and a `governance_status` field.
8. **Governance Decisions** — every decision returned by the runtime, with the seven-value vocabulary defined in [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md).
9. **Blocked Risks** — every action the governance layer refused, with the reason category (no passport, no consent, guarantee language, hard-blocked tool, etc.).
10. **Observed Value** — value entries classified across four tiers: Estimated, Observed, Verified, Client-Confirmed. Each tier has a different evidence requirement.
11. **Limitations** — what the project did not do, what could not be measured, what must not be generalized.
12. **Recommended Next Step** — the deterministic recommendation (second sprint, remediation, pause).
13. **Retainer Recommendation** — whether the project qualifies to be pitched as a retainer, with the score threshold satisfied or not.
14. **Capital Assets Created** — every asset deposited into the Capital Ledger. At least one is required; assembly fails otherwise.

---

## 2. Proof score formula — معادلة درجة الإثبات

The proof score is a single number in `[0, 100]`, computed as a weighted sum of five components.

```
proof_score = round(
    0.25 * source_coverage
  + 0.25 * output_quality
  + 0.20 * governance_integrity
  + 0.15 * value_evidence
  + 0.15 * capital_asset_creation
)
```

Components:

- **source_coverage (25%)** — share of outputs that carry a valid `source_ref` to a Source Passport. Missing references reduce the score linearly.
- **output_quality (25%)** — aggregate of per-deliverable quality scores: ranking precision, draft acceptance at review, bilingual completeness.
- **governance_integrity (20%)** — share of governance decisions that resolved cleanly: no `ESCALATE` left unresolved, no `BLOCK` events on actions that should have been refusable upstream, no missing `governance_status` on outputs.
- **value_evidence (15%)** — strength of the value classification: Observed entries with measurement, Verified entries with cross-checks, Client-Confirmed entries where applicable.
- **capital_asset_creation (15%)** — count and quality of capital assets deposited. Zero deposits caps this component at 0.

Each component is itself a number in `[0, 100]`. Components are reproducible: given the same project state, two recomputations must yield the same proof score.

كل عنصر من الخمسة هو عدد في المدى صفر إلى مئة. الدرجة النهائية حاصل ضرب مرجَّح. النتيجة قابلة للتكرار: نفس المدخلات تعطي نفس الدرجة.

---

## 3. Tier classification — التصنيف

The score maps deterministically to one of four tiers.

| Score range | Tier | What it unlocks |
|-------------|------|-----------------|
| ≥ 85 | **case_candidate** | Eligible to become a public case study after client confirmation. |
| 70 – 84 | **sales_support** | May be referenced in sales conversations (anonymized) but not published. |
| 55 – 69 | **internal_learning** | Used inside Dealix for capital review and team learning. Not externally referenced. |
| < 55 | **weak** | Treated as a productization failure. Triggers a retrospective. Cannot be invoiced as a full deliverable without remediation. |

A high score does not by itself authorize external use. External use additionally requires:

- The Source Passports to have `external_use_allowed = true`, or an explicit override approval.
- A Client-Confirmed value entry, if value numbers are referenced.
- A governance decision of `ALLOW` for the specific publication action.

---

## 4. How the Proof Pack is built — كيف تُجمَّع

The pack is assembled by `proof_os.proof_pack.assemble()`. The function:

- Reads inputs, outputs, governance decisions, value entries, and capital deposits from project state.
- Renders the fourteen sections in fixed order, bilingual where applicable.
- Computes the proof score and tier.
- Writes the result to the project's proof archive with a content hash.
- Calls `capital_os.capital_ledger.add_asset(...)` for each asset, enforcing the "at least one" rule.

If the assembler cannot locate at least one capital asset, it raises and the project does not close. This enforces the constitutional rule "no project without a Capital Asset".

---

## 5. What a Proof Pack is not — ما ليست حزمة الإثبات

- Not a marketing artifact. Marketing artifacts may be derived from it, subject to tier and consent.
- Not a slide deck. The Proof Pack is structured data first, rendered second.
- Not negotiable in scope. All fourteen sections are required, every project, every time.

ليست حزمة الإثبات وثيقة تسويق ولا عرضاً تقديمياً. هي بيانات منظَّمة أولاً، ثم تُعرَض ثانياً.

---

## 6. Cross-references — مراجع متقاطعة

- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).
- [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md) — feeds section four.
- [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md) — feeds sections eight and nine.
- [AGENT_CONTROL_STANDARD.md](AGENT_CONTROL_STANDARD.md) — agent kill events appear as blocked risks.

---

## 7. Disclaimer — إخلاء مسؤولية

A Proof Pack documents what happened in a project. It does not constitute a marketing claim, a legal opinion, or a regulatory filing. References to client outcomes require the client's written confirmation, the Source Passport authorization, and a governance decision of `ALLOW` for publication.

تُوثِّق حزمة الإثبات ما حدث فعلاً في المشروع. الإشارة إلى نتائج العملاء علنياً تستلزم تأكيداً مكتوباً من العميل وإذناً صريحاً من جواز المصدر وقراراً بالسماح.
