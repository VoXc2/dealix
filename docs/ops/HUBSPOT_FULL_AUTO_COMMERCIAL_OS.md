# Dealix HubSpot Commercial OS

## Purpose

Use **Dealix Company OS / Revenue Mesh as the commercial source of truth** and use HubSpot as an operational **CRM mirror** for verified contacts, qualified opportunities, tasks, notes, calls, meetings, and approved commercial metadata.

HubSpot must never promote a record into relationship, opportunity, payment, proof, or revenue truth by itself.

This is not an uncontrolled sending system. It is a controlled commercial operating system that can become more automated only when evidence, consent, channel, and approval gates are satisfied.

## Authority order

1. `docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md` — product/platform authority.
2. Dealix Company OS / Revenue Mesh / Evidence + Proof state — commercial truth authority.
3. Approval / governance / consent / suppression state — execution authority.
4. HubSpot — CRM mirror and workflow surface.
5. Analytics/renderers/connectors — observation or presentation only.

If HubSpot conflicts with verified Dealix evidence, **Dealix truth wins** and the connector must reconcile the CRM rather than mutate Dealix truth to match the CRM.

## Truth invariants

- CRM contact != verified relationship.
- CRM deal != verified opportunity.
- CRM amount != verified revenue.
- `closedwon` != payment unless payment evidence exists in Dealix.
- invoice != payment.
- proposal draft != proposal sent.
- directory/research record != real contact.
- enrichment != consent.
- public email/phone != permission to market on a channel.
- sample/demo/synthetic/self-test != customer evidence.

## Current connected HubSpot capability

Available write objects may include:

- companies
- contacts
- deals
- tasks
- notes
- emails
- calls
- meetings
- tickets
- products
- line items

Availability is not authority. Every write must still pass the Dealix mirror policy.

## Required Dealix mirror envelope

A trusted internal adapter must verify and stamp the commercial envelope before HubSpot contact/deal mirroring is allowed.

Minimum contact mirror evidence:

- `authority_verified = true`
- `truth_class = REAL`
- `relationship_state` at or after `real_relationship`
- source-bound `evidence_id`
- an actual email or phone
- no `self_test`, `synthetic`, `suppressed`, or `opted_out` flag

A deal additionally requires:

- relationship/opportunity state at or after `qualified`
- `opportunity_id`

`closedwon` additionally requires:

- `payment_verified = true`
- `payment_evidence_id`

A customer-specific quote amount may be mirrored as expected deal value only when `quote_evidence_id` exists. Lead budget must not be copied into HubSpot amount automatically.

## Recommended HubSpot truth fields

Create/use validated HubSpot custom properties only after confirming the portal schema and permissions:

- `dealix_truth_class`
- `dealix_relationship_state`
- `dealix_evidence_id`
- `dealix_consent_state`
- `dealix_channel_status`
- `dealix_opportunity_id`
- `dealix_next_evidence`

Until those properties are proven available, keep the authoritative values in Dealix and avoid inventing random HubSpot fields.

## Existing commercial CRM signals

HubSpot may contain useful target groups, work items, historical records, samples, placeholders, career/personal records, and real customer records.

Therefore reconciliation must classify before mutation. Never bulk-promote or bulk-delete records merely because they exist in the CRM.

Recommended classes:

- `REAL`
- `SAMPLE`
- `PLACEHOLDER`
- `HISTORICAL`
- `PERSONAL_NON_DEALIX`
- `UNKNOWN`

Only evidence-backed `REAL` records are candidates for relationship/opportunity mirroring.

## Operating model

### 1. CRM intake / reconciliation

Read companies, contacts, deals, tasks, calls, emails, notes, and meetings. Classify each record against Dealix evidence.

### 2. Dealix scoring

Dealix may analyze:

- sector
- likely pain
- buyer type
- best first offer
- urgency
- readiness
- risk
- next evidence
- next action

Scores are analytical inputs only. A high score never creates relationship or pipeline truth.

### 3. Drafting

Dealix may generate internally:

- first-message drafts
- follow-up drafts
- discovery questions
- objection responses
- negotiation guardrails
- proposal briefs

Draft != sent.

### 4. Approval / channel policy

External communication remains subject to the current Dealix authority, consent, suppression, cadence, claim, and channel rules. No connector may silently broaden those rules.

### 5. HubSpot write-back

After the truth gate permits it, Dealix may mirror:

- verified contact context
- approved tasks
- notes
- qualified deal state
- call summaries
- meeting notes
- sales-pack links

HubSpot write-back is downstream of evidence, not a substitute for evidence.

## Automation stages

### Stage 0 — Read-only intelligence
Analyze HubSpot and generate reconciliation reports. No CRM writes.

### Stage 1 — Proposed write-back
Generate proposed classification/tasks/notes for review.

### Stage 2 — Truth-gated contact mirror
Mirror only evidence-backed real relationships with actual contact identifiers.

### Stage 3 — Truth-gated deal mirror
Mirror only qualified opportunities with `opportunity_id`; no fit-score-only deals.

### Stage 4 — Controlled communication queue
Prepare channel-eligible communication according to current Dealix governance.

### Stage 5 — Production communication
Only when the specific recipient/channel is eligible and the current execution authority permits it.

## Commercial path

Canonical buying path:

`Free Mini Diagnostic -> Qualified Discovery -> customer-specific quote -> 30-Day Revenue Command Pilot -> verified payment -> delivery -> proof -> Stop/Expand/Recurring`

Retired public fixed-price / 7-day / checkout models are not authority.

## Financial tracking

Track evidence-backed metrics such as:

- real relationships
- qualified problems
- diagnostics
- discoveries
- customer-specific proposals sent with delivery evidence
- pilot agreements
- verified payments
- delivery proof
- referrals / expansions

Do not treat CRM amount, weighted pipeline, invoice value, or `closedwon` alone as verified revenue.

## Safety rule

**Dealix owns truth; HubSpot mirrors it.** Research, fit scores, CRM objects, analytics events, drafts, invoices, and synthetic records cannot promote economic state without the required Dealix evidence.
