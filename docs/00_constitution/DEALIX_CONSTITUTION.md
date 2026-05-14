# Dealix Constitution

> Purpose: the short, canonical statement of who Dealix is, what it sells, what it refuses, and the operating equation that makes the company defensible. This file is the entry point. The deep-dive lives in [DEALIX_OPERATING_CONSTITUTION.md](../DEALIX_OPERATING_CONSTITUTION.md).

## Identity — من نحن

Dealix is a **Saudi Governed AI Operations company**. We sell operating capability and proof, not AI tools and not spam.

Dealix **is**:

- An operating layer above AI infrastructure that turns model output into governed, auditable business action.
- A productized service that delivers ranked accounts, governed drafts, proof packs, and a monthly value report — for Saudi B2B operators.
- A capital compounding system: every project produces at least one reusable asset (scoring rule, draft template, governance rule, sector insight).

Dealix **is not**:

- ليست أداة AI تُباع بالاشتراك بدون تشغيل.
- ليست وكالة lead-gen تعتمد على scraping أو cold outreach.
- ليست استشارات شرائح بدون proof.
- ليست CRM ولا منصة marketing automation.

If a feature, prompt, agent, or sale fails this identity test, it does not ship.

## Operating Equation — معادلة التشغيل

```
data clarity
+ workflow ownership
+ AI assistance
+ human approval
+ runtime governance
+ auditability
+ proof
+ value tracking
+ operating cadence
+ capital compounding
= Dealix OS
```

Each term is a layer; none is optional.

- **Data clarity** — every input carries a Source Passport ([SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md)).
- **Workflow ownership** — a named human owns each workflow on the client side.
- **AI assistance** — models draft, rank, summarize. They do not act externally.
- **Human approval** — every external send / publish / charge requires explicit approval.
- **Runtime governance** — `decide(action, context)` returns one of seven decisions ([RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md)).
- **Auditability** — every decision, draft, approval, and send is logged with a source reference.
- **Proof** — every project assembles a 14-section Proof Pack ([PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)).
- **Value tracking** — every claim falls in Estimated / Observed / Verified / Client-Confirmed ([VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md)).
- **Operating cadence** — weekly executive brief, weekly capital review, monthly value report.
- **Capital compounding** — every project deposits ≥1 asset into [CAPITAL_LEDGER.md](../09_capital_os/CAPITAL_LEDGER.md).

Remove any term and the system collapses into a tool or a service-without-proof. Keep all ten and Dealix becomes the operating layer.

## What Dealix Sells — ماذا نبيع

Dealix sells **productized services with proof**, in a defined ladder:

1. **Revenue Intelligence Sprint** — the first paid offer. See [REVENUE_INTELLIGENCE_SPRINT.md](../03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md). Output: 10 ranked accounts, bilingual draft pack, governance decisions, full proof pack, capital asset.
2. **Monthly RevOps OS retainer** — unlocked only after adoption ≥ 70 and proof score ≥ 80. See [ADOPTION_SCORE.md](../12_adoption_os/ADOPTION_SCORE.md).
3. **Co-branded sector packages** — unlocked only after three paid pilots with verified value.

The ladder is fixed. Skipping a rung is a constitutional violation. The full commercial ladder is documented in [COMPANY_SERVICE_LADDER.md](../COMPANY_SERVICE_LADDER.md).

Each offer carries:

- An ICP and a written problem statement.
- Required inputs, with Source Passports.
- A workflow owned by a named human at the client.
- Deliverables in Arabic and English.
- A Proof Pack with proof score ≥ 70.
- A Value Ledger entry — never an unsupported claim.
- A capital asset added to the company ledger.

## What Dealix Refuses — ما نرفضه

The non-negotiables are an immutable list. Each is enforced by a test or middleware. See the full table in [NON_NEGOTIABLES.md](./NON_NEGOTIABLES.md).

Short form:

- لا scraping، لا cold WhatsApp، لا LinkedIn automation.
- No fake proof, no guaranteed sales outcomes, no source-less knowledge answers.
- No PII in logs, no external action without explicit approval.
- No agent without a registered identity.
- No project without a Proof Pack, no project without a Capital Asset.

These are not preferences. They are the perimeter inside which Dealix is allowed to operate. Any pull request that weakens this perimeter must be reverted.

## How to use this Constitution

- Builders read this file **before** designing any new capability.
- Sales reads this file **before** quoting any new offer.
- The deep operating articles (laws, gates, ladder mechanics, role briefs) live in [DEALIX_OPERATING_CONSTITUTION.md](../DEALIX_OPERATING_CONSTITUTION.md) and remain the supplementary deep-dive.
- When the two documents conflict, this file wins on **identity and refusal**; the operating constitution wins on **execution detail**.
