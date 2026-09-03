# Dealix — Canonical Company Control Center

**Status:** ACTIVE OPERATING CONTRACT  
**Authority:** Founder-controlled; this page is the compact command surface, not a second OS.  
**Last reconciled:** 2026-09-01 UTC  
**Repository truth:** `Dealix-sa/dealix` → `main@2d39f58fb438d50cf3a99f6a1c643773944c4cf0`

## Executive objective

> **Verified Economic Movement per Founder Minute / Cost / Risk**

Dealix is measured by movement from evidence to money, proof, and repeatability—not agents, commits, posts, raw leads, or generated signals.

## One company loop

`Market Signal → Source-Bound Evidence → Real Interaction → Qualified Problem → Mini Diagnostic → Discovery → Customer-Specific Quote → 30-Day Pilot → Payment Evidence → Delivery → Customer-Validated Proof → Expansion / Referral / Productization`

Every record must keep research, relationship, consent, commercial commitment, payment, outcome, and proof distinct.

## Current control state

| Control | Current state | Rule |
|---|---|---|
| Main | `2d39f58` | Current repository head; re-check before every decision |
| Main protection | NOT VERIFIED AS ACTIVE | Do not treat policy text as a technical barrier |
| Trust Kernel | PR #1466, Draft | First merge-train priority; current-head sovereign verification and independent review required |
| PostCSS remediation | PR #1469, Draft | Second priority; exact-head install/typecheck/build/audit required |
| LEAP capability harvest | PR #1463, Draft | Research/capability hypotheses only; no relationship or runtime authority |
| Hosted CI | NON-AUTHORITY UNTIL JOB STEPS RUN | `steps=[]` / `runner_id=0` is infrastructure non-evidence |
| Production owner | Railway | Require deployment SHA → runtime `/version` SHA → public front door parity |
| External effects | FAIL-CLOSED | No send, publish, spend, payment, legal commitment, or production mutation by default |
| Commercial truth | UNVERIFIED UNTIL EVIDENCE | Research and drafts never count as contact, quote, payment, outcome, or proof |

## Authority boundary

L0–L4 may run automatically for internal work: read, research, analysis, drafts, tests, local verification, evidence organization, queues, branch creation, and Draft PR preparation.

L5 always requires a fresh, action-bound founder approval and a reversible receipt:

- merge or update `main`;
- external email, LinkedIn, WhatsApp, SMS, or public publication;
- customer-specific price, scope, or legal commitment;
- payment, refund, tender submission, or spend;
- production, Railway, DNS, database, secret, or destructive mutation;
- any action that creates or changes an external relationship.

A broad delegation is not a current approval. Any material payload, target, environment, evidence basis, or SHA change invalidates prior approval.

## Canonical account record

One account row only, owned by the existing commercial/Company Brain path:

`company | stage | consent_state | evidence_refs | pain | economic_impact | package_hypothesis | owner | next_action | due | approval | blocker | expiry`

The `stage` field uses the existing `CanonicalOpportunity.stage` state machine exactly:

`research → qualify → approval → conversation → pilot → proof → commercial → won | lost | parked`

The adapter event mapping is normative: `warm_intro_selected|message_drafted→research`, `founder_sent_manually|replied→qualify`, `diagnostic_requested|diagnostic_delivered→approval`, `pilot_offered→conversation`, `commitment_received→pilot`, `payment_received→proof`, `delivery_started|delivered|proof_pack_delivered→commercial`, `upsell_offered|closed_won→won`, `closed_lost→lost`. Unknown events fail closed to `research`.

No transition may be inferred from a web page, exhibitor/speaker listing, badge scan, public contact, social engagement, generated text, draft, quote marker, invoice marker, paid-pilot marker, or synthetic record. Each transition requires evidence appropriate to that exact state.

## Four commercial offers

The Package Router may route only to these bounded offers:

1. Revenue Command Pilot
2. Company Brain & Governed AI Sprint
3. Saudi Market Access Sprint
4. Partner Implementation & Proof

The Free Mini Diagnostic is the entry point into the existing `DIAGNOSTIC` path, not a fifth offer. A request outside the four bounded offers routes to Discovery, Reject, or Partner handling—not an ungoverned package.

## Production acceptance

Railway is the production core unless live evidence proves a cutover. Before claiming production readiness, record one immutable receipt containing:

`deployment_status | intended_sha | railway_sha | runtime_version_sha | /health | /healthz | /ar | / | dns/certificate | three_consecutive_smokes | rollback_target`

Missing direct evidence is `UNKNOWN`, never PASS. Railway deployment health is readiness evidence; it is not a substitute for continuous independent monitoring.

## Founder Approval Digest

Show the founder only high-value decisions:

| Type | Minimum packet |
|---|---|
| Merge | PR, exact head SHA, verifier receipt, independent review, merge method, `ACTION_HASH`, expiry |
| External send/publish | recipient/audience, exact content hash, consent/suppression, `ACTION_HASH`, expiry |
| Quote | customer, scope, price, assumptions, `ACTION_HASH`, expiry |
| Payment | amount, destination, evidence, reconciliation state, `ACTION_HASH`, expiry |
| Production | SHA, mutation, blast radius, rollback, `ACTION_HASH`, expiry, rollback target |
| DNS/data/legal | before/after, authority, reversibility, `ACTION_HASH`, expiry |

All approvals expire and are invalidated by relevant state or payload changes. Every L5 packet must bind `action_type | target | environment | payload` and carry the canonical `ACTION_HASH`; a missing, stale, or mismatched hash is BLOCKED. A broad delegation is never a packet.

Record verification as independent axes, not one collapsed result:

- `LOCAL_VERIFIED`: exact-head local verifier passed.
- `REMOTE_CI_GREEN`: hosted jobs actually executed and passed.
- `REMOTE_CI_EXECUTION_PLANE_BLOCKED`: hosted jobs were unavailable/non-executing (for example `steps=[]` or `runner_id=0`).
- `PRODUCTION_VERIFIED`: deployment SHA, runtime SHA, front-door health, and required consecutive smokes are evidenced.
- `PRODUCTION_UNKNOWN`: production acceptance evidence is missing or stale.
- `PASS`: reserved for the complete applicable acceptance packet; it must never hide a missing remote-CI or production axis.
- `LOCAL_VERIFIED_REMOTE_CI_BLOCKED`: a compact composite label only when local verification passed and remote CI itself is unavailable; it does not describe a merely pending production acceptance.

## Company scorecard

Track only:

`exact_head_acceptance | production_sha_parity | real_interactions | qualified_problems | diagnostics | discoveries | customer_specific_quotes | verified_payments | accepted_proof_packs | expansion_or_referral | founder_minutes_per_stage_move | time_to_evidence`

Use `MONEY / DECISIONS / RISKS / APPROVALS / NEXT_ACTION` as the executive output.

## Stop rules

Kill, pause, or downgrade any initiative that fails two reviews to produce at least one of:

`TRUST_GAIN | REVENUE_MOVEMENT | PROOF_GAIN | FOUNDER_TIME_SAVING | COST_REDUCTION`

No new agent, scheduler, CRM, Company Brain, Approval Center, Proof Ledger, router, or production owner may be added to solve a gap that an existing canonical owner can handle.

## Canonical references

- `docs/ops/GITHUB_RULESET_AND_IDENTITY_PROPOSAL.md`
- `docs/ops/APPROVAL_FINGERPRINT_CONTRACT.md` (when present on the accepted Trust Kernel)
- `docs/ops/DAILY_OPERATING_LOOP.md`
- `docs/commercial/`
- `data/ops/`
- `scripts/verify_*`

This page governs operating interpretation. Live GitHub, Railway, runtime, and evidence receipts override any stale prose.
