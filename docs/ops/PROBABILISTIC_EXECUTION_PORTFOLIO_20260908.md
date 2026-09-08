# Dealix Probabilistic Execution Portfolio

Date: 2026-09-08
Owner: existing Strategy Execution Orchestrator / Company Machine
Mode: draft-only / internal execution

## Goal

Maximize the probability of verified economic movement while minimizing founder minutes, cost, risk and irreversible actions.

This is **not** a new agent, scheduler, CRM, Company Brain, Opportunity Graph, approval authority or model router. It is a decision policy for the existing Company Machine.

## Core objective

For each internal candidate action `a`:

`Utility(a) = P(success|evidence) * EconomicValue * EvidenceConfidence - Cost - FounderMinutes - RiskPenalty - IrreversibilityPenalty`

The numeric result is an **internal attention score only**. It is never buyer intent, consent, send authority, production authority, payment authority or customer proof.

## Maximum-attempt interpretation

Dealix should maximize attempts where attempts are cheap, reversible and internal:

- search-query variants;
- independent source verification;
- parser/tool/model fallbacks;
- hypothesis generation;
- solution-route alternatives;
- pricing/scoping simulations;
- deterministic retries after transient failures;
- local/test benchmark variants;
- partner/build/integrate/refer alternatives;
- draft variants and objection simulations;
- test fixtures and synthetic failure injection.

Dealix must **not** maximize attempts by multiplying:

- cold WhatsApp/SMS/voice calls;
- mass LinkedIn DMs;
- unsolicited repeated email sends;
- public posts;
- paid spend;
- bids/submissions;
- production changes;
- DB/DNS/secret mutations;
- payment/refund attempts.

Those remain governed by Consent, Suppression, ChannelEligibility and exact material authority.

## Exploration policy

Use a bounded exploration/exploitation policy rather than always choosing the current highest static score.

Recommended initial policy:

- 70% exploitation: strongest evidence-backed candidates.
- 20% adjacent exploration: plausible alternatives with enough evidence to learn cheaply.
- 10% frontier exploration: novel but bounded hypotheses with clear stop conditions.

When verified cash is not yet proven, exploration may be slightly broader inside research/draft lanes, but WIP limits remain unchanged.

Do not add an external bandit service initially. A deterministic seeded local selector plus durable receipts is sufficient until enough real outcomes exist to justify Thompson Sampling/contextual bandits.

## Attempt budget

Every candidate must define:

- `attempt_budget`
- `attempts_used`
- `stop_condition`
- `success_event`
- `failure_event`
- `evidence_refs`
- `expected_value`
- `founder_minutes_budget`
- `risk_class`
- `rollback`

Default attempt budgets:

- public research/source resolution: up to 5 independent approaches per entity/source family;
- parser/extractor fallback: up to 3 methods;
- internal draft/hypothesis variants: up to 5;
- local/test transient retry: up to 3 with backoff;
- capability benchmark: ONE active benchmark, up to 3 bounded runs;
- external recipient action: never inferred from this policy; exact channel/action authority applies.

## Learning / posterior update

After every bounded experiment, write a receipt containing:

- prior confidence;
- action selected and why;
- observed result;
- evidence quality;
- time/cost/founder minutes;
- failure class;
- posterior confidence;
- keep / modify / kill / defer decision.

Do not update probabilities from vanity events. Examples:

- page view != buyer intent;
- public contact found != relationship;
- draft generated != sent;
- reply != qualified problem;
- quote != payment;
- deployment != correct release;
- HTTP 200 != exact release identity.

## Portfolio constraints

Existing Company Machine constraints remain authoritative:

- top actions per cycle <= 3;
- deep qualified <= 10;
- diagnostics in preparation <= 3;
- live project cells <= 2;
- venture experiments <= 2;
- capability benchmarks <= 1;
- material approval packets <= 1.

Probability never overrides these limits.

## Tooling posture

Start with repository-native deterministic logic and JSON/CSV receipts. External libraries are candidates, not dependencies:

- Vowpal Wabbit / contextual bandits: DEFER until Dealix has enough labeled outcomes and contextual decision volume.
- MABWiser: DEFER until a multi-armed-bandit benchmark has a real decision dataset.
- Optuna: use only for bounded offline parameter/threshold tuning when a concrete objective exists; never as company authority.

The first requirement is clean outcome data, not a more sophisticated optimizer.

## Immediate application

1. TRUST: explore multiple non-material root-cause paths for CI/Railway release parity, but do not deploy/mutate production without exact authority.
2. MONEY_NOW: research wide across official Saudi sources, then probabilistically allocate attention among evidence-backed accounts/tenders/partners while preserving Top-3 WIP.
3. COMPOUNDING: use one capability benchmark slot to attack the current measured gap, not to install a catalog.

## Permanent truth

`More attempts` is valuable only when each attempt is bounded, evidence-producing, reversible and non-harmful.

`L5_EXECUTED=NONE`
