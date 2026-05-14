# First Customer Onboarding — تشغيل أوّل عميل، خطوة بخطوة

> Day-by-day kit for the founder, from an accepted proposal to a delivered Proof Pack. Fourteen steps, each with action, time, tools, ledgers, governance gate, and exit criterion. Bilingual (AR + EN). No emojis. No model names.
>
> Cross-link: [03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md), [03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md), [07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md), [sales-kit/WARM_LIST_WORKFLOW.md](../sales-kit/WARM_LIST_WORKFLOW.md), [INCIDENT_RESPONSE_QUICKCARD.md](./INCIDENT_RESPONSE_QUICKCARD.md), [MOYASAR_LIVE_CUTOVER.md](../MOYASAR_LIVE_CUTOVER.md).

---

## Preconditions — متطلبات سابقة

Before Step 1 starts, the following are already true:

- The customer was qualified via `POST /api/v1/service-setup/qualify` and the decision was `ACCEPT` or `DIAGNOSTIC_ONLY`.
- A signed pilot agreement or signed sprint order is on file.
- Payment is collected (Moyasar live, or bank transfer with founder confirmation per [MOYASAR_LIVE_CUTOVER.md](../MOYASAR_LIVE_CUTOVER.md) section 4).
- An `engagement_id` exists and folder `engagements/<engagement_id>/` is created.

The sprint runs for seven calendar days. The steps below cover those seven days plus three buffer days for review and close. Each step lists founder hours; the total budget is approximately 18–22 founder hours across the cycle.

---

## Step 1 — Kickoff call / مكالمة البداية

- **Action / الإجراء:** 45-minute kickoff call with the customer's named workflow owner. Confirm the one primary workflow, confirm decision-maker, agree the success picture in one sentence.
- **Time / الوقت:** 1.0 founder hour (45 min call + 15 min notes).
- **Tools:** scheduled meeting, voice-only acceptable. `POST /api/v1/engagement/kickoff` writes the call summary.
- **Ledger:** `proof_ledger.kickoff_recorded`. `value_ledger` engagement opens at `tier=pending`. `capital_ledger` no asset yet.
- **Governance gate:** `governance_os.decide(action="open_engagement")` returns `ALLOW`.
- **Exit criterion:** named workflow owner on the customer side recorded with role and contact. If no named owner, the engagement does not advance — escalate or refund.

ملاحظة: لا توجد مكالمة افتتاح بدون مالك عمل مُسمّى من جهة العميل. هذا قيد دستوري على هويّة الوكيل.

---

## Step 2 — Source Passport agreement / اتفاق جواز المصدر

- **Action:** draft the Source Passport with the customer in writing: `source_type`, `owner`, `allowed_use`, `contains_pii`, `sensitivity`, `ai_access_allowed`, `external_use_allowed`, `retention_policy`. Customer signs (digital initials in the workspace, or PDF signature, no chat-only consent).
- **Time:** 1.5 founder hours.
- **Tools:** `POST /api/v1/data-os/source-passport` to register; the workspace generates the bilingual passport PDF for signature.
- **Ledger:** `proof_ledger.source_passport_signed`.
- **Governance gate:** `governance_os.decide(action="ingest_data", passport=<id>)` — must return `ALLOW` or `ALLOW_WITH_REVIEW`. A `BLOCK` ends the engagement at refund.
- **Exit criterion:** signed passport on file with all nine fields populated. No data is touched until this is true.

---

## Step 3 — Data import / استيراد البيانات

- **Action:** customer uploads or exports the agreed dataset. Founder runs `data_os.preview` first (non-destructive sample), then the full import after preview is sane.
- **Time:** 1.5 founder hours, plus customer's own export time.
- **Tools:**
  - `python -m cli data import --passport <passport_id> --file <path> --preview-only` then without `--preview-only`.
  - `POST /api/v1/data-os/ingest` for live connections.
- **Ledger:** `proof_ledger.import_completed` with row count, column count, and import elapsed time. No PII in the ledger entry.
- **Governance gate:** `governance_os.decide(action="run_dq")` against the passport ID.
- **Exit criterion:** all rows ingested into the engagement workspace; `engagements/<id>/raw/` contains the source file with the passport ID stamped in the file header.

---

## Step 4 — Data Quality review / مراجعة الجودة

- **Action:** run the six DQ dimensions (completeness, validity, uniqueness, consistency, timeliness, conformance). Founder reviews the dashboard, marks any dimension below 60 as a friction point.
- **Time:** 2.0 founder hours.
- **Tools:** `POST /api/v1/data-os/compute-dq?engagement=<id>`. Dashboard renders the six scores plus the overall.
- **Ledger:** `proof_ledger.dq_computed` with the scores. `friction_log` for any dimension below 60.
- **Governance gate:** if any high-sensitivity field shows `completeness < 40` or `validity < 40`, `governance_os.decide(action="proceed_to_scoring")` returns `REQUIRE_APPROVAL`. Founder either approves with a written limitation, or pauses to renegotiate scope.
- **Exit criterion:** DQ score logged. The customer-visible DQ summary page is generated bilingual.

---

## Step 5 — Scoring / الترتيب

- **Action:** run the account scoring rule on the cleaned dataset to produce the 10 ranked accounts (sprint default). Tune weights only inside the bands the engagement defines; do not introduce a custom rule per customer without depositing it to `capital_ledger`.
- **Time:** 2.0 founder hours.
- **Tools:** `POST /api/v1/data-os/score?engagement=<id>&rule=<rule_id>`. The rule library is in the `capital_ledger`.
- **Ledger:** `proof_ledger.scoring_completed`. If a new scoring rule was authored, `capital_ledger` gets an asset.
- **Governance gate:** `governance_os.decide(action="emit_ranking")`. Returns `DRAFT_ONLY` by default — the ranking is not externally shared until founder review.
- **Exit criterion:** 10 ranked accounts in `engagements/<id>/scored/`. Each row carries the `source_ref` to the originating passport.

---

## Step 6 — Draft pack generation / توليد المسوّدات

- **Action:** generate bilingual outreach drafts for the top accounts. Drafts are templates per scoring tier; no automation sends them. Customer-facing language is reviewed by the founder line by line.
- **Time:** 2.5 founder hours.
- **Tools:** `POST /api/v1/draft-os/generate?engagement=<id>&accounts=top10`. The output is text only; the system does not push to any channel.
- **Ledger:** `proof_ledger.drafts_generated` with count. No draft content is logged in clear; the ledger records the hash plus the rule used.
- **Governance gate:** every draft is born `DRAFT_ONLY`. Customer must explicitly approve before any channel-bound action.
- **Exit criterion:** 10 drafts (AR + EN pairs) in `engagements/<id>/drafts/`. Each draft has the `source_ref` chain visible at the top.

---

## Step 7 — Governance review / مراجعة الحوكمة

- **Action:** founder runs the governance summary for the engagement. Every action that touched data is listed with its decision. Anomalies (a `BLOCK` that was overridden, a `REQUIRE_APPROVAL` that took longer than the customer success patience window) are flagged.
- **Time:** 1.0 founder hour.
- **Tools:** `GET /api/v1/governance-os/summary?engagement=<id>` returns the full decision table.
- **Ledger:** `proof_ledger.governance_summary` snapshot. `friction_log` for any anomaly.
- **Governance gate:** `governance_os.decide(action="approve_proof_pack_assembly")`.
- **Exit criterion:** governance summary is clean (no unresolved BLOCKs) or each anomaly has a written rationale.

---

## Step 8 — Proof Pack assembly / تجميع حزمة الإثبات

- **Action:** assemble the 14-section Proof Pack from the artifacts already produced. The score is computed by the system; the founder does not type the score by hand.
- **Time:** 2.0 founder hours.
- **Tools:** `POST /api/v1/proof-os/assemble?engagement=<id>`. Output is `engagements/<id>/proof_pack.pdf` (bilingual) and the JSON snapshot.
- **Ledger:** `proof_ledger.assembly_completed` with the computed score and the tier (`case_candidate | sales_support | internal_learning | weak`).
- **Governance gate:** `governance_os.decide(action="finalize_proof_pack")`. If `weak` is computed, the gate returns `REQUIRE_APPROVAL` and the founder must write a remediation note.
- **Exit criterion:** Proof Pack PDF generated, all 14 sections populated, score computed.

---

## Step 9 — Founder review / مراجعة المؤسس

- **Action:** founder reads the Proof Pack end to end. Bilingual review: AR and EN sections compared for parity. Limitations section is rewritten in plain language. Capital assets list verified against `capital_ledger`.
- **Time:** 1.5 founder hours.
- **Tools:** internal viewer at `/workspace/engagements/<id>/proof_pack`. Edits go via `PATCH /api/v1/proof-os/sections/<section>`.
- **Ledger:** `proof_ledger.founder_review_signed` with timestamp and initials.
- **Governance gate:** `governance_os.decide(action="release_to_customer")`. Returns `ALLOW` only after the founder signature is captured.
- **Exit criterion:** Proof Pack signed off by the founder, bilingual parity confirmed, no draft language left in the limitations section.

---

## Step 10 — Customer handoff call / مكالمة التسليم

- **Action:** 30-minute handoff call. Founder walks the customer through the Executive Summary, the DQ score, the 10 ranked accounts, the limitations, and the recommended next step. No surprises; the pack was the pre-read.
- **Time:** 1.0 founder hour.
- **Tools:** scheduled meeting. Recording only with explicit consent; otherwise notes-only.
- **Ledger:** `proof_ledger.handoff_completed`. `value_ledger` entry promoted from `pending` to its honest tier (`data_support` by default for a first sprint).
- **Governance gate:** `governance_os.decide(action="record_handoff")`.
- **Exit criterion:** customer acknowledges receipt of the Proof Pack and the deliverables, in writing.

---

## Step 11 — Value events recording / تسجيل أحداث القيمة

- **Action:** within seven days of handoff, capture any value events the customer reports (meetings booked from the drafts, accounts re-classified, decisions changed). Each event lands in the value_ledger at its tier.
- **Time:** 1.0 founder hour across the week.
- **Tools:** `POST /api/v1/value-os/event` with `tier`, `description`, `customer_confirmation` (`pending | confirmed | declined`), `source_engagement`.
- **Ledger:** `value_ledger` entries, tier-correct. Customer confirmation is requested in writing.
- **Governance gate:** `governance_os.decide(action="publish_value_number")` — numbers cannot be referenced externally without `customer_confirmation=confirmed`.
- **Exit criterion:** at least one value event recorded, tier-honest. Zero events is also a valid outcome and is logged as such.

---

## Step 12 — Capital asset registration / تسجيل الأصل الرأسمالي

- **Action:** the engagement must deposit at least one reusable asset. A scoring rule tweak, a draft template, a sector insight, or a governance rule — one of them, at least.
- **Time:** 1.0 founder hour.
- **Tools:** `POST /api/v1/capital-os/asset` with `asset_type`, `title`, `description`, `reuse_potential` (`high | medium | low`), `source_engagement`.
- **Ledger:** `capital_ledger` entry. Cross-reference back into the Proof Pack section 14.
- **Governance gate:** `governance_os.decide(action="register_asset")`. If the asset description contains any PII, the gate returns `REDACT` and the founder rewrites.
- **Exit criterion:** at least one asset registered, reusable across engagements. A project that fails to deposit an asset triggers a retrospective per the constitution.

---

## Step 13 — Retainer eligibility check / مراجعة أهلية الاشتراك الشهري

- **Action:** decide whether to propose Managed Ops (2,999–4,999 SAR/mo) to the customer. The decision is structured, not gut. Three questions: does value recur, is there a named owner on the customer side, is the governance load steady enough for a monthly cadence.
- **Time:** 0.5 founder hour.
- **Tools:** `POST /api/v1/service-setup/retainer-check?engagement=<id>` returns one of `propose | hold | not_a_fit`.
- **Ledger:** `proof_ledger.retainer_decision` with the three answers and the resulting recommendation.
- **Governance gate:** `governance_os.decide(action="send_retainer_proposal")` — `ALLOW` only if `propose` was returned.
- **Exit criterion:** decision logged. If `propose`, the proposal is sent within 48 hours of handoff, while attention is still fresh.

---

## Step 14 — Case-safe summary commit / حفظ ملخص آمن دون أسماء

- **Action:** generate the anonymized case summary for internal reuse. No customer name, no sector-identifying detail that narrows below three peers. The summary goes into the case-safe library for sales support.
- **Time:** 0.5 founder hour.
- **Tools:** `POST /api/v1/case-os/anonymize?engagement=<id>` produces the draft. Founder reviews. `POST /api/v1/case-os/commit` writes the final.
- **Ledger:** `capital_ledger` entry as a `case_safe_summary` asset. If the Proof Pack tier was `case_candidate` and the customer consented in writing, a separate named case study can be drafted later — a separate workflow.
- **Governance gate:** `governance_os.decide(action="commit_case_safe_summary")` includes a PII scan.
- **Exit criterion:** anonymized summary committed, searchable in the internal library, ready to reuse on the next qualification call.

---

## Total time budget — ميزانية الوقت الكاملة

Approximately 18–22 founder hours over a seven-day delivery + three-day close window. The largest blocks are scoring, drafts, and Proof Pack assembly. The biggest hidden cost is the bilingual review — budgeted at 1.5 hours but consistently consumes the most slippage. Founder is expected to track actual hours per step in `friction_log` and to reduce slippage to ten percent or less by the fifth engagement.

---

## What this kit refuses — ما يرفضه هذا الكتيب

- **No customer onboarded without a signed Source Passport.** Step 2 is not optional.
- **No Proof Pack issued without the computed score.** No hand-written score.
- **No retainer proposed without the retainer-check decision.** No "let me upsell while attention is hot."
- **No public mention of the customer until the customer signs an external-use consent**, even if the score is `case_candidate`.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
