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

## Canonical ownership

| Customer lifecycle | Primary owner | Supporting owners |
|---|---|---|
| Market signals, research, eligibility, relationship, qualification, discovery, quote, negotiation | `dealix-sales` | `dealix-engineer`, `dealix-content`, `dealix-pm` |
| Onboarding, delivery, support, customer success, acceptance, Proof Pack | `dealix-delivery` | `dealix-engineer`, `dealix-content`, `dealix-pm` |
| Data, integrations, finance evidence, governance, security, reliability, production trust | `dealix-engineer` | all canonical agents as scoped |
| Brand, content, video, AEO/SEO, sales assets, permissioned proof reuse | `dealix-content` | `dealix-sales`, `dealix-delivery` |
| Portfolio, priorities, exceptions, authority routing, founder command, productization decisions | `dealix-pm` | all canonical agents |

## Lead and signal acquisition

Priority order:

1. first-party inbound;
2. existing or warm relationships;
3. partner introductions;
4. evidenced event interactions;
5. permissioned forms/subscriptions;
6. official public signals and customer-authorized data for research.

Public data and enrichment can create a research hypothesis, not a relationship or consent. Scraping, purchased lists, cold WhatsApp, mass LinkedIn automation, identity deception, and rate-limit or platform-policy bypass remain blocked.

## Exact-head acceptance

Run from an isolated worktree at the exact candidate SHA:

```bash
export DEALIX_AUTOMATION_PYTHON=/opt/dealix/workspace/dealix/.venv/bin/python
bash scripts/ops/accept_end_to_end_company_v1.sh "$(git rev-parse HEAD)"
```

Expected terminal result:

```text
DEALIX_E2E_ACCEPTANCE=PASS
```

The receipt must contain the exact Git SHA and remain paired with an independent same-head review.

## Launch gates

A source-contract PASS is not a production or commercial-proof claim.

- `A0`: source consistency and no parallel owners.
- `A1`: exact-head five-agent/twelve-system internal runtime acceptance.
- `A2`: official channel capability and Founder Control end-to-end receipt.
- `A3`: deployed SHA, API/web health, rollback, and public truth.
- `A4`: explicitly synthetic dry run plus an inbound or consented channel canary.
- `A5`: one real path with interaction, qualified problem, customer-specific quote, verified payment, delivered scope, and customer-validated proof.
- `A6`: multiple paid cycles, measured delivery economics, low founder intervention, repeatable playbook, and renewal, expansion, or referral.

Only A5 supports a full commercial-proof claim. Only A6 supports a SaaS-scale or repeatability claim.

## Merge order and current dependency

This acceptance layer is based on current `main@7274c766dd43a23ec391b4cfbeb4fae8ae665763`. It does not supersede the open commercial-authority closure or public-truth work. Before production launch, reconcile and exact-head verify:

1. PR #1494 commercial/runtime/public-web authority;
2. Railway production and deployed SHA;
3. PR #1496 or the current canonical public-truth owner;
4. Founder Control and governed channel runtime;
5. this end-to-end company acceptance;
6. controlled commercial canary and real paid-pilot proof.
