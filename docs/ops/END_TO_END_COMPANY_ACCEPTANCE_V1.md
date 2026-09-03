# Dealix End-to-End Company Acceptance V1

## Purpose

This is a composite acceptance layer over the existing Dealix Company Machine. It does not create another Company OS, Company Brain, CRM, Opportunity Graph, Approval Center, Proof Ledger, scheduler, permanent agent fleet, model router, or observability database.

It proves whether the existing five canonical agents and twelve canonical operating systems can carry a customer lifecycle from official/first-party signal through relationship, diagnostic, discovery, customer-specific quote, verified payment, onboarding, delivery, support, proof, expansion, and learning.

## Operating result sought

The target is the lowest practical founder intervention:

- L0-L4 observation, analysis, drafting, bounded internal execution, and Draft PR work run autonomously.
- The founder sees material cash, decisions, risks, approvals, and next action only.
- L5 effects remain action-bound: live customer dispatch, public publish, binding quote or legal commitment, payment or refund, merge, production, DNS, database, secret, or identity mutation.
- Recipient consent, suppression, channel policy, sender health, evidence, and idempotency remain independent gates. Founder delegation never creates recipient consent.

## Human-quality communication without deception

Agents may use an approved founder style profile to produce natural Arabic or English drafts: specific context, concise commercial judgment, realistic tone, and evidence-backed personalization.

When automation is material, external identity must be an authorized Dealix assistant or team representative. An agent must not falsely claim to be the human founder, invent a personal memory or relationship, fabricate experience, or hide automation in a way that misleads the recipient.

## Canonical Founder Control

Founder Control is a dependency, not a new truth store.

Current canonical path is owned by #1500:

`Telegram DM -> OpenClaw -> existing Dealix Company Machine -> durable receipt -> Founder brief`

The acceptance contract therefore uses connector id `telegram_openclaw` and requires `telegram_openclaw_e2e_receipt` at A2. Slack is an optional dormant capability and must not be a launch dependency or a substitute for a current Telegram/OpenClaw VPS receipt.

## Canonical ownership

| Customer lifecycle | Primary owner | Supporting owners |
|---|---|---|
| Market signals, research, eligibility, relationship, qualification, discovery, quote, negotiation | `dealix-sales` | `dealix-engineer`, `dealix-content`, `dealix-pm` |
| Onboarding, delivery, support, customer success, acceptance, Proof Pack | `dealix-delivery` | `dealix-engineer`, `dealix-content`, `dealix-pm` |
| Data, integrations, finance evidence, governance, security, reliability, production trust | `dealix-engineer` | all canonical agents as scoped |
| Brand, content, video, AEO/SEO, sales assets, permissioned proof reuse | `dealix-content` | `dealix-sales`, `dealix-delivery` |
| Portfolio, priorities, exceptions, authority routing, founder command, productization decisions | `dealix-pm` | all canonical agents |

## Legacy AI Workforce specialization

The repository contains valuable historical AI Workforce and Revenue Factory specialist roles. They are preserved as capabilities, but they are not additional permanent Dealix agents.

Canonical runtime truth is:

- **5 permanent canonical agents:** `dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, `dealix-content`.
- **12 runtime specialist role handlers:** bounded workloads delegated to one of the five canonical agents.
- **15 Revenue Factory specialist contracts:** bounded workloads delegated to one of the five canonical agents.
- **30 Revenue Factory automation plays:** preserved as reusable plays; their execution owner, budget, authority, evidence, and receipts remain attached to a canonical agent.

Every specialist task must emit a `canonical_owner`. Unknown specialist roles fail closed rather than silently becoming new agent owners. Compatibility fields such as historical `assigned_agents`, `agents_registered`, or `agents_total` may remain for callers, but their semantics are explicitly specialist-role counts, not permanent-agent truth.

The AI Workforce may research, analyze, draft, compose diagnostics, prepare delivery plans, summarize proof, and recommend next actions. It may not independently create relationship consent, public prices, discounts, invoices, charges, payment authority, binding commitments, customer-facing sends, public publish, merge, deploy, DNS/DB/secret mutation, or any new L5 authority.

Active commercial motion inside the specialist runtime is restricted to:

`Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> 30-Day Revenue Command Pilot -> Verified Payment / Start Evidence -> Delivery -> Customer-Validated Proof -> Stop / Expand / Redesign`

Legacy `499 SAR`, `growth_starter_pilot`, fixed tiers, and 7-Day paid offers are acceptance failures. Finance remains blocked until an approved customer-specific quote exists; Delivery remains blocked until accepted scope and verified payment/start authority exist.

## Lead and signal acquisition

Priority order:

1. first-party inbound;
2. existing or warm relationships;
3. partner introductions;
4. evidenced event interactions;
5. permissioned forms/subscriptions;
6. official public signals and customer-authorized data for research.

Public data and enrichment can create a research hypothesis, not a relationship or consent. Scraping, purchased lists, cold WhatsApp, mass LinkedIn automation, identity deception, and rate-limit or platform-policy bypass remain blocked.

## Exact-head source/internal acceptance

Run from an isolated worktree at the exact candidate SHA:

```bash
export DEALIX_AUTOMATION_PYTHON=/opt/dealix/workspace/dealix/.venv/bin/python
bash scripts/ops/accept_end_to_end_company_v1.sh "$(git rev-parse HEAD)"
```

Expected terminal result:

```text
DEALIX_E2E_ACCEPTANCE=PASS
```

The exact-head runner must pass the Company Machine, Continuous Operations, Governed Channel Runtime, Commercial Fabric, the end-to-end lifecycle contract, canonical AI Workforce delegation tests, and Revenue Factory ownership tests. Its receipt records 5 canonical agents, 12 runtime specialist roles, 15 Revenue Factory specialist roles, 30 automation plays, 12 systems, and 18 lifecycle stages.

The receipt must contain the exact Git SHA and remain paired with an independent same-head review. This source/internal PASS is A0/A1 evidence only; it does not prove A2-A6.

## Launch gates

A source-contract PASS is not a production or commercial-proof claim.

- `A0`: source consistency and no parallel owners.
- `A1`: exact-head five-agent/twelve-system internal runtime acceptance, including specialist-role delegation and retired-commercial-motion guards.
- `A2`: official channel capability + **current Telegram/OpenClaw Founder Control E2E receipt** + sender health/idempotency.
- `A3`: canonical `dealix-apps-web` deployed SHA, API/web health, rollback, and Public Truth.
- `A4`: explicitly synthetic dry run plus an inbound or consented channel canary.
- `A5`: one real path with interaction, qualified problem, customer-specific quote, verified payment, delivered scope, and customer-validated proof.
- `A6`: multiple paid cycles, measured delivery economics, low founder intervention, repeatable playbook, and renewal, expansion, or referral.

Only A5 supports a full commercial-proof claim. Only A6 supports a SaaS-scale or repeatability claim.

## Merge order and current dependencies

This acceptance layer is based on current `main@7274c766dd43a23ec391b4cfbeb4fae8ae665763`. It does not supersede the current owners. Before production launch, reconcile and exact-head verify:

1. #1494 commercial/runtime/public-web authority;
2. #1497 canonical Railway Production/Front Door identity: `dealix-apps-web / Dealix-sa/dealix / apps/web / exact deployed SHA` plus generated-domain and custom-domain/certificate evidence;
3. #1496 or the current canonical Public Truth owner;
4. #1500 Telegram/OpenClaw Founder Control current VPS receipt;
5. this #1501 end-to-end company acceptance;
6. controlled commercial canary and real paid-pilot proof.

A legacy Railway service named `web` or a legacy `frontend/` build does not substitute for #1497 canonical production evidence. Hosted workflow failures before repository steps do not substitute for exact-head acceptance.
