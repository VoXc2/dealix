# Governed AI Operations — تشغيل الذكاء الاصطناعي بحوكمة

> Purpose: define the category Dealix occupies, why it exists above AI infrastructure, and how it differs from lead-gen agencies, AI consultants, and generic SaaS.

**AI tools are easy to buy. AI value is hard to operate.**

Saudi B2B operators in 2026 have access to abundant model APIs, hosted inference, and consumer-grade chat. What they do not have is a way to take a model output and turn it into a *governed, auditable, repeatable business action* — without leaking PII, sending cold spam, or making claims they cannot defend.

That gap is the category Dealix occupies: **Governed AI Operations**.

## What Governed AI Operations means

Governed AI Operations is the **operating layer above AI infrastructure**. It assumes that compute, models, and embeddings are commodities supplied by infrastructure providers. It then adds the seven things infrastructure does not supply:

- **Data clarity** — every input is bound to a Source Passport ([SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md)).
- **Runtime governance** — every action passes through `decide(action, context)` ([RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md)).
- **Human approval** — no external send without an approver identity.
- **Auditability** — every decision is logged with a source reference.
- **Proof** — every project assembles a Proof Pack ([PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)).
- **Value tracking** — claims are classified Estimated / Observed / Verified / Client-Confirmed ([VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md)).
- **Capital compounding** — every project deposits at least one reusable asset ([CAPITAL_LEDGER.md](../09_capital_os/CAPITAL_LEDGER.md)).

Without these seven, AI in a B2B context is either a chatbot demo or a compliance accident waiting to happen. With them, AI becomes an operating capability.

## Why this is a category, not a feature

A category exists when there is a buyer pain that no current vendor solves end-to-end. The pain here is concrete:

- A marketing agency wants to rank accounts and draft Arabic outreach without scraping or cold WhatsApp. No vendor delivers both ranking + governance + proof in one motion.
- A consulting firm wants to use AI on client documents without leaking PII into logs or third-party model providers. No vendor wraps that with a Source Passport.
- A B2B services operator wants a defensible value story for an executive committee. No vendor packages Estimated, Observed, Verified, and Client-Confirmed value separately and refuses to overstate.

Each of these is an *operating* problem, not a *tool* problem. The buyer does not need another tool. The buyer needs an operator with rules, proof, and a ledger.

## Contrast — التموضع

### vs. lead-gen agencies

Lead-gen agencies sell volume of contacts. They scrape, they cold-send, they make implicit guarantees. Dealix refuses all three. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md). Dealix replaces "1000 leads" with "10 ranked accounts + governed drafts + proof".

### vs. AI consultants

AI consultants sell hours and slide decks. They produce strategy artifacts that no one operates. Dealix replaces a strategy artifact with a *running operating loop* — workflow, drafts, approvals, governance decisions, proof score, value ledger entry, capital deposit — in a fixed sprint.

### vs. generic SaaS

Generic SaaS sells features and seats. The buyer is left to operate them. Dealix sells the operating capability itself, with a productized first offer ([REVENUE_INTELLIGENCE_SPRINT.md](../03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md)), a retainer behind an adoption gate ([ADOPTION_SCORE.md](../12_adoption_os/ADOPTION_SCORE.md)), and a refusal to grow seats without proof.

## Relationship to HUMAIN — العلاقة مع هيومن

HUMAIN is the Saudi PIF-backed AI infrastructure company launched in May 2025. HUMAIN supplies compute, models, and AI infrastructure for the Kingdom. **Dealix is not a competitor to HUMAIN.** Dealix is a tenant on Saudi AI infrastructure.

The relationship is layered:

```
HUMAIN              — AI infrastructure layer (compute, models, hosting)
Dealix              — Governed AI Operations layer (data, governance, proof, value, capital)
Saudi B2B operators — buyers of operating capability, not infrastructure
```

Dealix helps Saudi B2B operators **use Saudi AI infrastructure safely**: with Source Passports, governance decisions, approvals, proof packs, and a value ledger. As HUMAIN deepens infrastructure, Dealix deepens the operating layer above it. The two are complementary; they are not on the same shelf.

## The category test

A vendor is doing Governed AI Operations only if:

1. Every action carries a Source Passport.
2. Every external action passes through a runtime governance decision.
3. Every project produces a Proof Pack with a computed proof score.
4. Every claim is classified in the Value Ledger.
5. Every project deposits at least one Capital Asset.

A vendor missing even one of the five is either AI infrastructure, an AI consultant, or a tool — not an operating layer. Dealix is built to pass all five, every project, every time.
