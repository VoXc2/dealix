# Dealix Targeting Intelligence Engine V1

Status: draft implementation contract  
Date: 2026-09-06  
North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`  
Owner: `dealix-sales`  
Machine owner: existing Dealix Company Machine / Opportunity Graph / Revenue Communications Runtime

## Mission

Improve Dealix's probability of reaching the right Saudi B2B accounts without turning the company into a lead scraper or spam engine.

```text
Signals -> Entity Resolution -> Evidence Dossier -> Target Value
-> Actionability / Eligibility -> Buyer or Partner Route -> Proofability
-> Priority Queue -> Draft / Diagnostic -> Governed Channel Execution
-> Real Conversation -> Qualified Problem -> Customer-Specific Quote
-> Verified Payment -> Outcome -> Customer-Validated Proof -> Learning
```

This is an intelligence layer inside the existing Company Machine. It does not create a second CRM, Opportunity Graph, revenue engine, scheduler, proof model, vector owner, or agent fleet.

## Truth firewall

- `research != relationship`
- `public contact != consent`
- `draft != sent`
- `quote != invoice != payment`
- `synthetic proof != customer-validated proof`
- a high target score never grants channel authority
- 50-200/day is internal qualification/draft capacity, not a sending quota

## Target Value Score (0-100)

Keep commercial attractiveness separate from channel/action eligibility.

| Dimension | Weight |
| --- | ---: |
| ICP / Saudi fit | 15 |
| Problem evidence | 20 |
| Why-now trigger | 20 |
| Offer fit | 10 |
| Buyer or partner route | 10 |
| Measurable baseline / proofability | 10 |
| Expected economic value | 10 |
| Evidence confidence / provenance | 5 |

Bands: `85-100 P0`, `70-84 P1`, `55-69 P2`, `<55 defer/watch`.

## Actionability state

Every target must explicitly carry:

```text
relationship = UNKNOWN | RESEARCH_ONLY | KNOWN | WARM | INBOUND | ACTIVE_CONVERSATION
consent = UNKNOWN | NOT_REQUIRED_FOR_INTERNAL_RESEARCH | OPTED_IN | OPTED_OUT | SUPPRESSED
email = BLOCKED | DRAFT_ONLY | ELIGIBLE
whatsapp = BLOCKED | INBOUND_ONLY | TEMPLATE_ELIGIBLE | ELIGIBLE
voice = BLOCKED | INBOUND_ONLY | CALLBACK_REQUESTED | ELIGIBLE
```

`TargetValue >= 85` plus `RESEARCH_ONLY` still means research/draft-only.

## Evidence hierarchy

1. **Tier A — direct Dealix interaction truth:** website inbound, Gmail inbound/replies, occurred meetings, known contacts, discovery/customer docs, verified payment/delivery/proof.
2. **Tier B — first-party and official sources:** company website/newsroom/careers/docs, official Saudi government/regulator/procurement sources, official company reports.
3. **Tier C — licensed enrichment:** connected providers such as Apollo and lawful business directories; useful for firmographics/entity resolution, never consent/buyer intent inference.
4. **Tier D — open web/archive:** allowlisted crawls, Common Crawl, RDAP, public technical metadata; secondary evidence and discovery only.
5. **Tier E — social/public chatter:** weak signal unless corroborated; public profile/attendance/contact details never create relationship or consent.

## Signal families

Prioritize signals that can map to a bounded problem and measurable outcome:

- execution fragmentation and manual handoffs;
- revenue leakage / slow lead-to-quote / weak follow-up;
- proof, AI-governance, PDPL, auditability or executive reporting pressure;
- Saudi expansion, funding, new business unit, hiring burst, partner launch;
- procurement / B2G readiness / supplier prequalification;
- ERP/CRM/cloud/AI/automation transition;
- support/inbound/voice/WhatsApp service pressure;
- partner fit with implementation/data/agency/system-integrator firms.

Every signal resolves to:

`WHAT_CHANGED / SOURCE / OBSERVED_AT / ACCOUNT / WHY_IT_MATTERS / PROBLEM_HYPOTHESIS / OFFER_ROUTE / PROOF_BASELINE / CONFIDENCE / EXPIRY`.

## Capacity funnel

Capacity is a funnel, not a quota:

```text
200-500 raw signals/day
-> entity resolution + dedupe + suppression
-> 50-200 account qualifications/dossiers/day
-> 20-40 deep evidence refreshes/day
-> 5-20 highest-value draft candidates/day by default
-> live action only when separately eligible/authorized
```

Never lower evidence or eligibility thresholds to hit a number.

## Mandatory pre-draft gate

Before entering the existing Revenue Communications Runtime, require:

- resolved entity identity;
- attributable source and observed timestamp;
- specific `WHY THEM`;
- time-bounded `WHY NOW` or explicit inbound/relationship rationale;
- falsifiable problem hypothesis;
- bounded Dealix offer/diagnostic route;
- measurable proof baseline or discovery plan;
- relationship, consent, suppression and channel state;
- no duplicate active thread/opportunity.

Every draft is backed by:

`WHY THEM / WHY NOW / EVIDENCE / PROBLEM HYPOTHESIS / BUSINESS COST / ONE CTA`.

## Entity resolution / dedupe

Use deterministic keys first: canonical domain, normalized legal/company name, provider IDs, verified company URLs, parent/subsidiary mapping. Then fuzzy/probabilistic matching only for unresolved cases. Ambiguous matches remain `HOLD_ENTITY_AMBIGUITY`.

## Semantic fit — reuse existing pgvector

Reuse the existing Postgres/pgvector owner for semantic ranking of account dossiers against ICP/problem/diagnostic/proof patterns. Semantic similarity is only a feature and never replaces evidence or eligibility.

## Open-source admission decisions

### Adopt / pilot inside current owners

- **Firecrawl — PILOT:** structured allowlisted account/source extraction and evidence snapshots.
- **Crawl4AI — PILOT:** self-hosted extraction for approved domains where local control adds value.
- **Scrapy or Crawlee — ADMIT_AS_LIBRARY:** choose one per bounded collector; do not install both by default.
- **RapidFuzz — ADOPT:** fast normalization/fuzzy duplicate candidates.
- **Splink — DEFER_UNTIL_SCALE:** probabilistic linkage only when ambiguity volume justifies it.
- **existing pgvector — ADOPT_EXISTING:** semantic fit; no new vector owner.
- **Sentence Transformers — PILOT_MODEL_GATED:** optional local embeddings with model license/privacy/quality review.
- **ICANN RDAP — ADOPT_AS_WEAK_SIGNAL:** domain metadata only.
- **Common Crawl — SECONDARY:** historical/background discovery, never current why-now without re-verification.

### Defer / reject for this phase

- **Qdrant — DEFER:** duplicates current pgvector unless a measured limitation appears.
- **Twenty — DEFER:** duplicates current Opportunity Graph/CRM owner.
- **Mautic — DEFER:** duplicates Company Machine marketing/orchestration and splits consent/proof truth.
- **EvolutionAPI live outbound — DEFER:** WhatsApp remains official, inbound-first, consent/suppression gated.
- **SalesGPT/autonomous sales agents — PATTERNS_ONLY:** no live commercial authority.
- **anti-bot/terms-restricted browser automation — REJECT_FOR_TARGETING.**
- **vulnerability scanning as prospecting — REJECT.**

## Saudi privacy/commercial boundary

Targeting research and direct marketing are separate actions. Retain source provenance, relationship state, consent/eligibility evidence where required, suppression/opt-out, draft/send/action receipts, and applicable purpose/retention controls. A public email, phone number, exhibitor listing, attendee badge or employee page is not marketing consent.

WhatsApp stays inbound-first. Voice stays inbound receptionist/support and requested/warm callback first. Outbound authority is governed independently of target score.

## Learning objective

After every real interaction record:

`signal_family / source_quality / score_at_selection / route_used / reply / qualified_problem / quote_created / payment_verified / outcome_delivered / proof_validated / founder_minutes / cost`.

Do not optimize on raw leads, drafts, sends, opens or meetings alone.

Long-run objective:

`maximize P(Verified Payment + Customer-Validated Proof | evidence, target, route) while minimizing Founder Minute / Cost / Risk`.

## Metrics

Commercial: real interactions/week, qualified problems/week, customer-specific quotes/week, verified-payment conversion, signal->interaction time, problem->quote time, quote->payment time, paid outcomes, customer-validated proof packs, repeat cycles/founder hour.

Targeting: top-20 precision, stale-signal rate, duplicate/entity-error rate, research->interaction, interaction->qualified problem, qualified problem->quote, false buyer-intent rate, consent/eligibility violations (target zero).

## Initial execution order

1. Extend the existing Revenue Communications Runtime upstream with this targeting gate.
2. Keep Opportunity Graph canonical.
3. Reuse Postgres/pgvector.
4. Pilot Firecrawl on an allowlist; use Crawl4AI only where self-hosting adds value.
5. Add deterministic normalization + RapidFuzz; Splink only after measured ambiguity.
6. Add signal expiry/recency and evidence-confidence to the dossier before increasing volume.
7. Rank Lighthouse accounts using Target Value separately from Actionability.
8. Generate diagnostics/drafts only after the pre-draft gate.
9. Log research->interaction->cash->proof transitions to Proof Ledger.
10. Reweight scoring only from real outcomes after customer-validated proof exists.

## Definition of Done — V1

- Existing Revenue Communications Runtime consumes a canonical targeting dossier instead of raw names.
- Every target has Target Value plus separate Actionability/eligibility.
- Dedupe prevents duplicate active threads.
- Evidence is attributed and time-stamped.
- Semantic fit reuses pgvector.
- 50-200/day internal qualification capacity is measurable without a sending quota.
- Top candidates can produce bounded Execution Diagnostic drafts.
- Zero public-contact-to-consent inference.
- Proof Ledger can attribute first interaction, qualified problem, quote, verified cash and customer proof to originating targeting evidence.
- No parallel CRM/revenue engine/vector store is introduced.
