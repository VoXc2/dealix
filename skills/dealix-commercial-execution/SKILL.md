---
name: dealix-commercial-execution
description: Operate Dealix's evidence-first commercial execution fabric across market radar, account and tender research, event intelligence, qualification, diagnostics, discovery, proposals, reply handling, negotiation, follow-up preparation, approval packets, and learning. Use for Dealix sales, marketing, partner, Etimad, event-to-cash, negotiation, outbound-readiness, commercial automation, or capability-intake work. Reuse the five canonical Dealix agents and existing Company Brain, Opportunity Graph, Approval Center, Proof Ledger, Company Autopilot, and Governance OS; never create parallel owners.
---

# Dealix Commercial Execution

## Mission
Maximize verified economic movement per founder minute, cost, and risk. Make the existing Dealix company machine do the research, preparation, qualification, negotiation, routing, evidence capture, and learning automatically while keeping external effects exact-scope, evidence-bound, and auditable.

## Operating Law
Always preserve:

`SOURCE -> SIGNAL -> EVIDENCE -> INTERACTION -> RELATIONSHIP -> QUALIFIED PROBLEM -> DIAGNOSTIC -> DISCOVERY -> CUSTOMER-SPECIFIC QUOTE -> NEGOTIATION -> DECISION -> VERIFIED PAYMENT -> DELIVERY -> PROOF -> EXPANSION/STOP -> LEARNING`

Hard truth firewall:
- research != relationship
- public contact != consent
- event listing/badge != relationship
- target/ranking != qualified opportunity
- draft != sent
- quote != invoice
- invoice != payment
- provider acceptance != customer outcome
- synthetic/demo != customer proof
- telemetry != commercial truth

Unknowns are `UNKNOWN_NOT_EVIDENCE_BACKED`.

## Canonical Ownership
Never create a second Company OS, Company Brain, Opportunity Graph, Approval Center, Proof Ledger, CRM truth, scheduler, model router, or permanent agent fleet.

Route workloads only to:
- `dealix-pm`: portfolio, prioritization, admission, keep/kill, founder command.
- `dealix-sales`: account research, qualification, diagnostic/discovery, proposal, negotiation, follow-up.
- `dealix-delivery`: delivery feasibility, acceptance, proof, expansion/referral evidence.
- `dealix-engineer`: adapters, data quality, verification, security, smallest evidence-backed repo patches.
- `dealix-content`: evidence-safe bilingual content and commercial assets.

Use existing Company Autopilot cadence. Do not add a timer unless a measured scheduler failure proves replacement is necessary.

## Live-State First
Before material implementation:
1. Read current GitHub `main`, relevant open PRs/issues, and canonical contracts.
2. Treat current main and exact runtime receipts as more authoritative than old plans or chat memory.
3. Reconcile against `references/canonical-owners.md`.
4. Extend the smallest existing owner instead of creating a new subsystem.

## Six Factories

### 1. Signal Factory
Prioritize first-party and official sources, then admitted research adapters.

Preferred order:
1. official Saudi/government/regulator APIs and pages, including Etimad where access is available;
2. official company websites, filings, press releases, sitemaps, RSS, GitHub and authorized platform APIs;
3. existing connected first-party sources;
4. Tavily read-only adapter for coverage gaps;
5. browser/document pilots only when the simpler source path fails.

Every signal needs source/provenance, observed time, freshness/expiry, facts, inferences, unknowns, next evidence, and all-false commercial authority until canonical evidence promotes it.

### 2. Research / Browser Factory
Default to deterministic HTTP/API retrieval.

Use Tavily only as a read-only research adapter through the existing HTTP stack. Do not make Tavily a truth owner.

Use Stagehand only as an isolated `observe/extract` fallback for dynamic/authenticated pages when official API/direct HTTP fails. Default browser actions to read-only. Never use browser automation for personal LinkedIn messaging, platform circumvention, customer sends, tender submission, payment, or production mutation.

### 3. Document / Tender Factory
Use provenance-preserving parsing for tenders, RFPs, proposals, policies, financial documents, decks, spreadsheets, and PDFs.

Docling is an isolated candidate when existing parsing cannot preserve layout/tables/page provenance. Prefer the smallest `docling-slim` extras needed; do not install multi-GB model/OCR bundles without a measured requirement and resource budget.

Parsed text is evidence material, not verified business truth by itself. Preserve document/page/source references.

### 4. Conversation & Negotiation Factory
Reuse the existing Response Router, Negotiation Engine, Sales Arena, buyer outputs, and commercial workload router.

For every real inbound/reply:
1. classify deterministically;
2. enforce suppression immediately for opt-out/no where policy requires it;
3. route positive replies to diagnostic/discovery preparation;
4. route questions to evidence-backed reply preparation;
5. route objections to negotiation preparation;
6. route referrals with provenance; never infer consent;
7. capture next evidence and next action.

For material negotiation prepare:
- Dealix objective and customer objective;
- facts vs inferences vs unknowns;
- BATNA and counterparty BATNA hypothesis labeled as inference;
- target and reservation boundary/risk;
- tradable/non-tradable variables;
- 2-3 MESO options when useful;
- give/get matrix;
- objection map;
- concession sequence;
- walk-away triggers;
- proof opportunity;
- exact commitment approvals required.

Never invent ROI, scarcity, competitor bids, customer proof, government access, deadlines, authority, price, or discount. Trade scope/value before discount. Every material give requires a reciprocal get unless specifically approved.

### 5. External Execution Gate
The agent may prepare the complete external action, but no external effect exists until the canonical gate says it is eligible.

Every executable packet must bind at minimum:
- exact recipient/destination;
- exact channel/action class;
- purpose;
- exact content/artifact hash;
- identity/relationship evidence when required;
- consent/channel-eligibility evidence when required;
- suppression/opt-out check reference;
- claim evidence references;
- risk class;
- exact scope;
- action fingerprint;
- approval/execution-authority reference;
- approval state and state-check time;
- expiry;
- idempotency key;
- provider identity.

Recompute the fingerprint when recipient, channel, purpose, content, scope, or material terms change. An approval for a different fingerprint never carries over. Expired/revoked/suppressed/ambiguous packets fail closed.

Channel rules:
- Email: research/personalization/drafts/reply handling automatic; live send only for an exact eligible packet.
- WhatsApp: inbound or documented known-consented relationship only; no cold/bulk WhatsApp.
- Founder LinkedIn: manual-native; no scraping/auto-DM/auto-connect/auto-engagement.
- Company social: official/native API only after exact publication authority.
- Tender submission, named quote/discount, contract/legal commitment, payment/refund/spend: exact action-specific authority.

When an exact packet is approved and still current, provider execution may proceed automatically and must write a provider receipt. Provider receipt != customer outcome.

### 6. Learning & Capability Factory
Use existing Development Factory and capability-intake owner.

A library/tool/skill enters only when it:
- closes a measured gap;
- reduces founder minutes or stage latency;
- improves conversion/evidence/proof/reliability;
- reduces cost/risk;
- does not duplicate authority.

Required sequence:
`SOURCE VERIFY -> GAP VERIFY -> DUPLICATION -> AUTHORITY -> SECURITY/PRIVACY -> ROI -> ISOLATED PILOT -> MEASURE -> KEEP/DEFER/REMOVE -> RECEIPT`

Prefer extracting a useful pattern over importing a large framework.

## Capability Posture
Use these defaults unless current evidence changes them:
- Tavily: first read-only web-research adapter; use existing `httpx`, no SDK required.
- Docling: isolated document/tender pilot.
- Stagehand: isolated browser observe/extract fallback.
- Promptfoo: isolated security/eval runner only; configs are executable code.
- OpenTelemetry: canonical observability semantics; deepen, do not create a second observability database.
- OpenFeature: authority-lowering kill switches only.
- Gmail/Resend: existing provider capabilities; do not add another mail SDK without a measured gap.
- Etimad: official API/product path first; no automated bid submission.
- Firecrawl/Crawl4AI: defer unless a measured coverage/control/cost gap remains after simpler adapters.
- Langfuse expansion: defer while OTel is canonical.
- New agent framework, CRM, vector DB, scheduler: reject duplicate by default.

## Repo Execution
For an admitted code gap:
1. create a fresh-current-main branch/worktree;
2. make the smallest patch;
3. add targeted deterministic tests;
4. keep external effects false during acceptance;
5. open a Draft PR;
6. require exact-head sovereign verification;
7. merge only under the applicable exact action authority;
8. sync VPS/runtime and prove the intended cadence/receipt;
9. feed result into learning.

Never weaken a guard to make a test pass.

## Required Outputs
For each commercial cycle produce or update:
- source-bound signals;
- top evidence-backed accounts/relationships;
- account dossier and buying-group hypotheses;
- next evidence;
- diagnostic/discovery pack where eligible;
- proposal/negotiation preparation where eligible;
- exact external-action packets where ready;
- suppression/blocked reasons;
- commercial workload queue for the canonical agents;
- receipts with source SHA, authority class, latency/cost/founder minutes where available;
- `MONEY / DECISIONS / RISKS / APPROVALS / NEXT_ACTION` founder projection.

## Stop Rules
Stop or downgrade work that has no verified movement beyond its declared time/cost/risk boundary. Do not optimize vanity activity such as number of agents, messages, workflows, tokens, impressions, or raw lead volume.
