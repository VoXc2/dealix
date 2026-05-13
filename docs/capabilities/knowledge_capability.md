# Capability Blueprint — Knowledge Capability

> One of the 7 capabilities Dealix builds inside customers (per
> `docs/company/CAPABILITY_OPERATING_MODEL.md`). Mirrors the structure of
> `docs/capabilities/revenue_capability.md`. Concerns turning scattered
> internal documents into a cited, governed, internal AI assistant —
> Dealix calls this the **Company Brain**.

## Business purpose
Help the customer turn scattered knowledge (PDFs, slide decks, policies,
SOPs, product specs, sales playbooks) into an internal AI assistant that
answers questions with **source-level citations**. The same answer
everyone gets. The right answer, every time. Onboarding shrinks.
"Where is that PDF?" disappears.

> **Hard rule**: *no source = no answer*. The assistant refuses to answer
> when no qualifying source exists, regardless of how confident the
> underlying model feels (per
> `docs/services/company_brain_sprint/offer.md`).

## Typical problems
- Critical SOPs live in WhatsApp chats and a senior manager's head.
- Same policy answered three different ways by three different agents.
- New-hire onboarding takes weeks because nobody can find the right deck.
- Sales reps recreate the same proposal section every week.
- Customer-facing teams quote out-of-date pricing because the latest deck
  is in someone's inbox.
- Public LLMs hallucinate when staff ask company-internal questions
  ("does our policy allow X?") — and there's no safe alternative.

## Required inputs from customer
- Document inventory (up to 500 docs for the standard Sprint).
- Source-of-truth attribution per document (who owns it, when last
  reviewed, who is allowed to read it).
- Access control tiers (3 tiers in MVP: All Staff / Department /
  Restricted).
- PII / special-category acknowledgement when HR or health documents are
  in scope (per `docs/governance/PDPL_DATA_RULES.md` §4).
- Lawful basis for processing (typically "customer contract").
- A named knowledge owner inside the customer who will own freshness.

## AI functions that build this capability
- Document ingestion + chunking + embedding (RAG pipeline).
- **PII redaction before indexing** — Saudi mobile, National ID, IBAN,
  card numbers stripped per `dealix/trust/pii_detector.py`.
- Retrieval with source-level citations (document name, page, section).
- Query interface (web / Slack / Teams) for ≤ 20 seats in MVP.
- 3-tier access enforcement at retrieval time (Permission Mirroring).
- Freshness tracking — auto-flag documents > 90 days old.
- Evaluation harness: citation rate, answer-with-source %, refusal rate
  on out-of-scope questions.
- Bilingual answers (AR / EN) matched to the source language and the
  user's query language.

## Governance controls (binding)
- **No source = no answer** — refusal is a feature, not a bug. Measured
  via the eval harness, surfaced in the Proof Pack.
- Permission Mirroring at retrieval (per
  `docs/governance/RUNTIME_GOVERNANCE.md` Check 3) — a user only sees
  passages they're allowed to read.
- Customer-facing RAG answers require an approval gate (per
  `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`).
- Special-category documents (HR / health) require explicit PDPL Art. 13
  acknowledgement before ingestion.
- Forbidden-claim filter runs on every answer ("نضمن / guarantee").
- Freshness gate: documents > 90 days flagged; > 180 days quarantined
  unless the customer's knowledge owner re-blesses them.

## KPIs (measured before/after)
- Answer-with-citation rate (target > 95%).
- Refusal rate on out-of-scope queries (target > 90% — refusals are good).
- Median time-to-answer (search minutes → seconds).
- Onboarding time for new staff (days before → days after).
- Top-10 unanswered questions (drives the next docs to write).
- Query volume per week + active seats.

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — knowledge lives in heads and WhatsApp.
- **Level 1** — documents exist but scattered across drives.
- **Level 2** — single drive structure documented; owner per folder.
- **Level 3** — Company Brain live with cited answers + 3-tier access
  (Company Brain Sprint).
- **Level 4** — Brain + Sales Knowledge / Policy / Proposal assistants
  + freshness cadence (Monthly Company Brain Management).
- **Level 5** — Knowledge OS feeding back into Support, Revenue, and
  Operations capabilities; partial self-service authoring.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to | Indicative price |
|---------|----------------------------|------------------|
| Company Brain Sprint | L1 → L3 | SAR 20,000 · 21 days |
| Sales Knowledge Assistant | L3 → L4 (revenue-side bolt-on) | scoped |
| Policy Assistant | L3 → L4 (HR / compliance bolt-on) | scoped |
| Proposal Assistant | L3 → L4 (revenue-side bolt-on) | scoped |
| Monthly Company Brain Management | L3 → L4–L5 | SAR 15,000–60,000 / mo |

## Agents involved (per `docs/product/AI_AGENT_INVENTORY.md`)
- **KnowledgeAgent** — retrieval with citations; refuses without source.
  Autonomy level 2.
- **ComplianceGuardAgent** — mandatory gate. PII before index, claims
  before answer, lawful basis on ingest.
- (Optional, post-MVP) **ReportingAgent** — freshness report and
  top-unanswered-questions monthly digest.

## Proof types produced
- **Knowledge Proof** — % answers with citation, refusal-rate on
  out-of-scope, median answer time. This is the headline.
- **Time Proof** — onboarding-time reduction; hours saved per week
  hunting for documents.
- **Risk Proof** — PII redaction count; access-tier violations blocked;
  PDPL acknowledgements logged.
- **Quality Proof** — consistency: same question, same answer, every
  time, with the same source.

## Saudi-specific notes
- AR/EN bilingual answers are default. Source language is preserved in
  citations (no silent translation).
- Documents containing PDPL personal data require lawful-basis tagging
  before ingestion. Special-category HR/health docs need explicit ack.
- ZATCA-relevant invoicing playbooks live in the customer's tenant only
  — never in Dealix's training data.
- SDAIA-aligned residency: Kingdom Residency option pins all RAG indexes
  to Kingdom-eligible regions (Enterprise plan).

## Cross-links
- `docs/services/company_brain_sprint/`
- `docs/services/company_brain_sprint/offer.md`
- `docs/services/company_brain_sprint/data_request.md`
- `docs/services/company_brain_sprint/qa_checklist.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `docs/company/AI_CAPABILITY_FACTORY.md`
- `docs/company/CAPABILITY_PACKAGES.md`
- `docs/company/VALUE_REALIZATION_SYSTEM.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/governance/PII_REDACTION_POLICY.md`
