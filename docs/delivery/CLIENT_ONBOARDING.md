---
title: Client Onboarding — First Week for a New Paying Customer
doc_id: W6.T36.client-onboarding
owner: HoCS
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W6.T36, W5.T10, W3.T07b]
kpi:
  metric: signed_scope_to_kickoff_days
  target: 3
  window: per_customer
rice:
  reach: 0
  impact: 2
  confidence: 0.9
  effort: 0.5
  score: delivery-operating
---

# Client Onboarding — First Week

## 1. Context

The first seven days after a customer signs the SOW set the tone for the
relationship and the quality of every later stage. Onboarding is a productized
ritual, not a sales follow-up: the customer should feel they have *already
joined a company* by Day 5, not "waiting for things to start". This doc is the
checklist for that first week.

## 2. Audience

CS lead (project owner), AE who closed the deal, assigned engineer,
customer's day-to-day owner. The customer's economic buyer and exec sponsor
appear at kickoff only.

## 3. Day-by-Day

### 3.1 Day 0 — Intake & Routing

- AE forwards signed SOW + intake form to CS within 4 working hours of signature.
- CS triggers `client_intake.process_intake` — creates the project row,
  fingerprints the offer, opens Stage 1 (Discover) in the Stage Machine.
- Slack channel created: `#cust-<short_name>`; the day-to-day owner is added
  on Day 1, not before.
- DPA / PDPL Art. 13 notice attached to the customer's portal.

### 3.2 Day 1 — Welcome Email + Kickoff Slot

- Bilingual (AR/EN) welcome email signed by HoCS goes out within 24h of
  intake. Includes: assigned CSM name and contact, the 8-stage map, the
  weekly cadence, the support email.
- A Day 3 or Day 4 kickoff slot is booked. Three customer roles required:
  economic buyer, exec sponsor, day-to-day owner.

### 3.3 Day 2 — Access & Governance Acks

- Customer portal access provisioned (read-only). Sub-processor list shared.
- Data Processing Addendum executed (electronic signature OK; legal copy
  archived in `docs/legal/`).
- PDPL Art. 13 acknowledgement captured in writing.
- If integrations are part of scope: credentials request + BYOK note sent
  ([`../governance/PII_REDACTION_POLICY.md`](../governance/PII_REDACTION_POLICY.md)).

### 3.4 Day 3–4 — Kickoff Call

- 60-minute video call. Walk the Delivery Standard's 8 stages.
- Confirm success metrics (numeric, dated).
- Capture data sources + access list.
- Transition Discover → Diagnose.

### 3.5 Day 5–7 — Discover Sprint

- Diagnostic scoring runs. First weekly status update (≤ 5 lines) sent
  Friday end-of-day.
- Risk + scope items raised here (not later) per
  [`SCOPE_CONTROL.md`](SCOPE_CONTROL.md).

## 4. Acceptance — "Onboarded" Definition

A customer is **onboarded** when ALL of: signed SOW, executed DPA, PDPL ack
captured, kickoff held, success metrics signed, day-to-day owner identified,
first data source connected or shared.

## 5. Cross-links

- Delivery Standard: [`DELIVERY_STANDARD.md`](DELIVERY_STANDARD.md)
- Lifecycle: [`DELIVERY_LIFECYCLE.md`](DELIVERY_LIFECYCLE.md)
- Scope control: [`SCOPE_CONTROL.md`](SCOPE_CONTROL.md)
- CS framework: [`../customer-success/cs_framework.md`](../customer-success/cs_framework.md)
- PDPL rules: [`../governance/PDPL_DATA_RULES.md`](../governance/PDPL_DATA_RULES.md)
- Code: `auto_client_acquisition/delivery_factory/client_intake.py`

## 6. Owner & Review Cadence

- **Owner**: HoCS.
- **Review**: monthly until first 10 customers onboarded; quarterly thereafter.

## 7. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoCS | Initial first-week onboarding checklist |
