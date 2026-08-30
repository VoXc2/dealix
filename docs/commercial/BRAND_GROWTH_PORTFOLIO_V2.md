# Dealix Brand & Growth Portfolio V2

This is the execution contract for the multi-arm growth portfolio above the
bounded Universal Market Radar (#1405). It reuses the existing Company Machine
owners; it is not a second Marketing OS.

## Runtime slice

The first executable slice is intentionally deterministic and read-only:

- data/commercial/brand_growth_portfolio_v2.json is the strategic portfolio
  contract and arm registry.
- dealix/commercial/brand_growth_portfolio.py validates source receipts,
  compiles draft-only ContentOpportunity records, gates Proof reuse, scores
  internal portfolio attention and maps arms to the five canonical workers.
- scripts/commercial/run_brand_growth_portfolio_v2.py compiles a bounded
  input snapshot into an internal output snapshot.
- scripts/verify_brand_growth_portfolio_v2.py protects the strategic
  contract; tests/test_brand_growth_portfolio_v2.py covers the runtime gates.

The runner does not create a database, scheduler, agent, CRM, Company Brain,
Opportunity Graph, Approval Center, Proof Ledger or analytics truth store.
Persisting any output remains the responsibility of the existing canonical
runner/owner.

## Input shape

    {
      "generated_at": "2026-08-30T00:00:00+00:00",
      "as_of": "2026-08-30T00:00:00+00:00",
      "signals": [
        {
          "signal_id": "signal-1",
          "source_id": "FIRST_PARTY_OFFICIAL",
          "source_ref": "https://example.test/source/1",
          "provenance_ref": "receipt://source/1",
          "fresh_until": "2026-09-05T00:00:00+00:00",
          "sector_family": "ICT",
          "business_archetype": "RECURRING_SAAS_OR_SERVICES",
          "evidence_refs": ["evidence://source/1"],
          "facts": ["Source-bound fact"],
          "inferences": ["Buyer problem hypothesis"],
          "unknowns": ["Owner and urgency require validation"],
          "authority": {
            "relationship": false,
            "consent": false,
            "offer": false,
            "price": false,
            "quote": false,
            "contract": false,
            "external_send": false,
            "public_publish": false,
            "payment": false,
            "customer_proof": false,
            "execution": false,
            "production": false
          }
        }
      ],
      "proof_candidates": [],
      "allocation_items": [],
      "experiments": []
    }

signals are research receipts. They require provenance, freshness, evidence
and zero authority. A valid signal can produce a content draft, but it cannot
produce a relationship, consent, opportunity, quote, payment or proof.

## Output behavior

Run:

    PYTHONPATH=. python scripts/commercial/run_brand_growth_portfolio_v2.py \
      --input /path/to/snapshot.json \
      --out /path/to/portfolio-run.json

The output includes:

- admitted and rejected source receipts;
- draft-only content opportunities with source/evidence references;
- Proof reuse candidates marked REUSE_READY_PENDING_CHANNEL_APPROVAL or
  BLOCKED;
- at most five internal allocation items;
- evidence-gated SCALE, ITERATE, STOP or INVALID experiment decisions;
- workload routes to dealix-pm, dealix-sales, dealix-content,
  dealix-delivery or dealix-engineer;
- a compact truth firewall and zero-authority object.

PARTIAL_FAIL_CLOSED means one or more inputs were rejected. It is a safe
diagnostic result, not permission to skip the missing evidence.

## Operating rules

The portfolio loop is:

source-bound signal -> evidence-backed thesis -> draft asset -> governed
distribution -> real interaction -> canonical relationship -> qualified
problem -> bounded package -> payment evidence -> delivery -> customer
validated proof -> permissioned reuse -> learning

The execution layer enforces these rules:

- research, attention and score are not relationship or purchase probability;
- a thesis remains a hypothesis until fact, brand, commercial, claim and
  channel QA;
- Founder LinkedIn remains manual-native;
- email and WhatsApp remain relationship/consent/channel-policy governed;
- a customer proof candidate needs validation, limitations, evidence, recorded
  permission and supplied claim units;
- a reusable proof result is still a draft candidate and has no public-publish
  authority;
- SCALE requires a verified outcome and outcome evidence refs;
- only existing canonical workers receive workloads;
- paid media is readiness-only;
- external sends, public publishing, spend, payments, contracts, tender
  submission, production changes and main merge remain blocked.

## Activation sequence

1. Accept #1405 with exact-head sovereign evidence.
2. Run the focused runtime and strategic verifiers on a trusted exact-head
   worktree.
3. Feed only admitted first-party/official/read-only receipts through the
   existing market_radar workload.
4. Use Big 5, LEAP and DeepFest as real-interaction tests; never promote lists,
   badges or directory rows to relationships.
5. Reconcile the output with the existing canonical Relationship, Revenue,
   Proof, Channel and President owners.
6. Promote a channel only after capability, policy, consent, QA and
   approval evidence exists.
7. Productize only from repeated paid deployments and customer-accepted proof.

This slice is complete when it can be run repeatedly with fresh inputs,
produce deterministic bounded output, and fail closed whenever provenance,
freshness, permission, customer validation or outcome evidence is missing.
