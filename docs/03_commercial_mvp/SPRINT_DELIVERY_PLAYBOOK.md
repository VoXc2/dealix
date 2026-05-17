# Sprint Delivery Playbook — كتاب تشغيل سبرنت ذكاء الإيرادات

> Purpose — الغرض: the 7-day, 10-step runbook for delivering the Revenue Intelligence Sprint (25,000 SAR+ per the Governed Revenue & AI Ops ladder). Every step names the module that runs, the founder checkpoint, and the ledger entry produced. Cross-link: [REVENUE_INTELLIGENCE_SPRINT.md](./REVENUE_INTELLIGENCE_SPRINT.md), [DIAGNOSTIC_DELIVERY_SOP.md](./DIAGNOSTIC_DELIVERY_SOP.md), [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md), [GOVERNED_REVENUE_AI_OPS_STRATEGY.md](../strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md), [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md), [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

كتاب تشغيل عملي لسبرنت الإيرادات المُحوكَم على مدى سبعة أيام. كل خطوة تربط بالمنهجية، بالنماذج البرمجية المفعّلة، وبسجلات الإثبات والقيمة والأصول.

---

## Day 1 — Kickoff + Source Passport — اليوم الأول: الانطلاق وجواز المصدر

**What runs:** Kickoff call (45 minutes) + `data_os.SourcePassport` draft.

**Activities — الأنشطة:**

- Confirm the named workflow owner on the client side (non-negotiable #9: agent identity, on both sides).
- Define one primary workflow for this sprint (e.g., dormant-account revival).
- Draft and sign the Source Passport: `owner`, `source_type` (must be `client_upload`, `crm_export`, or `manual_entry` — never `scraped`), `allowed_use`, `pii_flag`, `sensitivity`, `retention_days`.
- Issue an engagement ID; create folder `engagements/<engagement_id>/`.

**Founder checkpoint:** the Source Passport is the contract. If the client cannot or will not declare data ownership, the sprint does not begin.

**Ledger entries:** `proof_ledger.kickoff_recorded`, `capital_ledger` (no asset yet), `value_ledger` (engagement opened, tier=`pending`).

---

## Day 2 — Data Import + DQ Score — اليوم الثاني: استيراد البيانات وفحص الجودة

**What runs:** `data_os.preview` for a non-destructive sample read, then `data_os.compute_dq` for the full quality score across the six standard dimensions (completeness, validity, uniqueness, consistency, timeliness, conformance).

```bash
python -m cli data import --passport <passport_id> --file client.csv --preview-only
python -m cli data compute-dq --passport <passport_id> --out out/dq_<engagement_id>.json
```

**Founder checkpoint:** review the DQ score. A baseline DQ < 40 means the client has a data-readiness problem, not a sprint problem; pause the sprint and propose the **CRM/Data Readiness for AI** adjacent offer instead (scoped — see [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md)). DQ between 40 and 70 → proceed with documented caveats. DQ ≥ 70 → proceed clean.

**Ledger entries:** `proof_ledger.dq_baseline = <score>`, `proof_ledger.import_preview_recorded = true`. No external action taken.

---

## Day 3 — Account Scoring + Top 10 — اليوم الثالث: ترتيب الحسابات

**What runs:** `revenue_os.account_scoring` over the imported, deduped, DQ-checked dataset. Output: a transparent, rubric-based ranking with explicit features (fit, signal strength, governance risk).

**Founder checkpoint:** read the top 10 explanations. Each ranked account must have a human-readable justification. If any explanation is opaque or unverifiable → demote it; do not ship "magic" rankings.

**Ledger entries:** `proof_ledger.scoring_completed = true`, `proof_ledger.top_n = 10`, `capital_ledger` candidate: any new scoring feature worth reusing across customers (e.g., a sector-specific signal) is flagged as a draft capital asset.

---

## Day 4 — Draft Generation + Governance Review — اليوم الرابع: توليد الرسائل والمراجعة المُحوكَمة

**What runs:** `revenue_os.draft_pack` produces bilingual (AR + EN) outreach drafts — typically 8 AR + 4 EN, one per top account plus optional follow-ups. Then `governance_os.decide` applies the 7-decision matrix (`ALLOW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `RATE_LIMIT`, `REROUTE`).

**Founder checkpoint:** review every BLOCK and every REDACT. The governance decisions log is part of the deliverable; clients buy the *audit trail*, not just the drafts. Confirm every draft is marked `draft_only` until the client explicitly approves each send.

**Ledger entries:** `proof_ledger.drafts_generated = <n>`, `proof_ledger.governance_decisions = [...]`, `proof_ledger.blocked_count`, `proof_ledger.redacted_count`. No external send happens from Dealix infra (non-negotiables #2, #3, #8).

---

## Day 5 — Proof Pack Assembly — اليوم الخامس: تجميع حزمة الإثبات

**What runs:** `proof_os.assemble` builds the 14-section Proof Pack (intake, passport, DQ, dedupe, scoring, drafts, governance decisions, redactions, approvals, value-tier mapping, capital asset registration, limitations, methodology, signatures). Each section is required; missing sections fail the assembly.

**Founder checkpoint:** read the assembled Proof Pack end to end. Compute the proof score. A `proof_score < 70` cannot be delivered — escalate to either remediation (extra day) or partial-refund per [REFUND_SOP.md](../REFUND_SOP.md).

**Ledger entries:** `proof_ledger.assembled = true`, `proof_ledger.proof_score = <score>`, `value_ledger.tier_provisional` mapped from proof score and observed methodology evidence.

---

## Day 6 — Handoff + Retainer Readiness — اليوم السادس: التسليم وفحص جاهزية الاحتفاظ

**What runs:** Handoff call (60 minutes) walking the client through the Proof Pack section by section. Then `adoption_os.retainer_readiness` evaluates whether the client is ready to enter the Governed Ops Retainer (4,999–35,000 SAR/mo, scoped).

**Retainer eligibility (estimated criteria):**

- `proof_score >= 80` AND
- `adoption_score >= 70` AND
- Named workflow owner persists post-sprint AND
- Source Passport renewable for ongoing use AND
- At least one capital asset deposited.

**Founder checkpoint:** offer the retainer only when the criteria are met. Otherwise propose either a second sprint or graceful close-out.

**Ledger entries:** `adoption_ledger.score = <score>`, `proof_ledger.handoff_completed = true`, `value_ledger.tier_final` confirmed.

---

## Day 7 — Capital Asset Registration + Case-Safe Summary — اليوم السابع: تسجيل الأصل وكتابة الملخص الآمن

**What runs:** `capital_os.add_asset` registers at least one reusable asset (a scoring rule, draft template, governance rule, sector insight, productization signal, or proof example). Then the founder drafts a case-safe summary using the template in [docs/case-studies/](../case-studies/).

**Founder checkpoint:** the capital asset must be genuinely reusable (not a one-off transformation). The case-safe summary must be anonymized: no client name, no identifying revenue figures, no sector + city + size combinations that would re-identify the client.

**Ledger entries:** `capital_ledger.asset_id = <id>`, `proof_ledger.case_safe_summary_draft = <path>`, sprint marked `status=delivered` in the engagement registry.

---

## QA Rubric — معايير الجودة (8 dimensions)

Each Sprint delivery is scored against these 8 dimensions before close-out:

1. **Source integrity** — every input has a Source Passport.
2. **DQ transparency** — the DQ baseline and post-remediation score are visible.
3. **Scoring explainability** — every top-10 rank has a human-readable justification.
4. **Bilingual parity** — AR and EN drafts are mirror-equivalent, not summary translations.
5. **Governance auditability** — every decision is logged with a decision type and reason.
6. **Approval discipline** — no external action occurred without a logged approval.
7. **Proof completeness** — all 14 sections present, no placeholders.
8. **Capital deposit** — at least one reusable asset registered with a real reuse case.

---

## Exit Criteria — معايير الخروج

A Sprint may be **delivered** if and only if:

- `proof_score >= 70` (minimum acceptable).
- All 14 Proof Pack sections present.
- At least one Capital Ledger asset deposited.
- Founder approval logged on the final deliverable.
- Case-safe summary draft committed (publish optional).

Below `proof_score = 70`, the engagement is not delivered. Either extend (with founder discount, not client penalty) or refund per [REFUND_SOP.md](../REFUND_SOP.md).

---

## Escalation rules — قواعد التصعيد

- **Data block:** DQ < 40 at Day 2 → escalate to Data Pack offer, refund 80% of sprint fee per refund SOP. The remaining 20% is retained against the kickoff and Source Passport work already performed.
- **Governance block:** > 50% of drafts BLOCKed → escalate to scope review; the workflow chosen at Day 1 may be the wrong one. Re-scope with the client before continuing; do not silently re-write the workflow.
- **Identity block:** client cannot name a workflow owner → pause, do not generate, do not bill day 3+. This is a partnership signal, not a billing dispute; the engagement is not viable without a named owner.
- **Constitution violation request:** client asks for scraping, cold WhatsApp, LinkedIn automation, or guaranteed outcomes → refuse, log the refusal in the engagement record, end the engagement cleanly. Refund any unearned portion. This is a non-negotiable boundary, not a negotiation point.
- **Founder bandwidth block:** if a sprint hits Day 5 with the founder unable to complete the Proof Pack review, the engagement extends by up to 48 hours without additional client charge. The cost is absorbed by Dealix — the client should never pay for our capacity gap.

---

## Founder daily discipline — انضباط المؤسس اليومي

Each day of the sprint closes with three actions: (1) update the engagement record's `status_today` field, (2) commit any new ledger entries to the immutable ledger store, (3) send the client a one-paragraph daily bilingual status note (AR + EN) summarizing what ran, what's next, and whether any decision is needed from the client. Silence between days erodes trust faster than any single defect; the daily note is the cheapest insurance against silent failure.

ينتهي كل يوم بثلاثة إجراءات: تحديث حالة المشروع، إيداع سجلات الإثبات والقيمة والأصول، وإرسال ملاحظة يومية ثنائية اللغة للعميل.

---

## Cross-references — مراجع متقاطعة

- Diagnostic-to-sprint conversion: [DIAGNOSTIC_DELIVERY_SOP.md](./DIAGNOSTIC_DELIVERY_SOP.md).
- Proposal template (Jinja2): [../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2](../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2).
- Case-safe summary references: [../case-studies/case_001_anonymized.md](../case-studies/case_001_anonymized.md), [../case-studies/case_002_anonymized.md](../case-studies/case_002_anonymized.md).
- Refund handling: [../REFUND_SOP.md](../REFUND_SOP.md).
- Source Passport schema: [../04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
