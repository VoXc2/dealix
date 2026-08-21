# Dealix Second-Number WhatsApp Company Operations Master

## Executive decision

Use the second number as the dedicated **Dealix Business WhatsApp identity**.

The canonical production path is the WhatsApp Business Cloud integration already present in Dealix:

- `integrations/whatsapp.py`
- `api/routers/webhooks.py` at `/api/v1/webhooks/whatsapp`
- `auto_client_acquisition/whatsapp_safe_send.py`
- `auto_client_acquisition/safe_send_gateway/`
- `docs/WHATSAPP_OPERATOR_FLOW.md`
- `docs/WHATSAPP_PRODUCTION_CUTOVER.md`
- `docs/whatsapp/*`
- `trust/WHATSAPP_OUTREACH_SAFETY_POLICY.md`

Do **not** create a second WhatsApp business engine or a parallel customer/contact database.

## Channel ownership

- **Telegram / OpenClaw:** founder command center, approvals, incidents, Daily Command, deep-work requests.
- **Second-number WhatsApp Business:** customer and prospect inbound, approved sales replies, support, booking handoff, proposal handoff, customer-success conversations.
- **Email/Gmail:** formal proposals, longer documents, contracts, formal follow-up drafts.
- **Dealix:** canonical Company Brain, Opportunity Graph, Actions, Approvals, Outcomes, Proof and Learning.
- **Hermes:** internal specialist analysis and council work.
- **n8n:** deterministic connector/workflow runner only; never a source of truth.
- **Railway:** production API and public WhatsApp webhook ingress.
- **VPS:** command/AI node; n8n and Ollama remain private/loopback.

## Non-negotiable authority model

### Automatic internal work: L0-L3

The system may automatically:

1. Receive and verify inbound WhatsApp webhook events.
2. Parse and classify inbound intent.
3. Resolve or propose company/contact identity.
4. Update internal opportunity/customer context through existing Dealix contracts.
5. Detect opt-out / suppression signals.
6. Summarize conversations.
7. Research the company and opportunity from allowed sources.
8. Score opportunity fit, urgency, value and risk.
9. Draft Arabic/English responses.
10. Draft discovery questions.
11. Draft negotiation counters and give-get options.
12. Draft booking options.
13. Draft proposal handoffs.
14. Prepare customer-support responses.
15. Prepare customer-success next actions.
16. Create Approval Cards.
17. Record internal outcomes, proof candidates and learning events.
18. Escalate security, production, commercial or customer risks to Telegram.

### External work: L5

External customer/prospect communication remains approval-first.

The system must not autonomously:

- send a new WhatsApp message,
- send a commercial counteroffer,
- promise price, discount, scope or timeline,
- accept a commercial term,
- publish anything,
- send a payment request,
- sign/accept legal terms,
- contact a cold/unknown WhatsApp number,
- bypass consent or suppression,
- enable bulk or blast messaging.

`WHATSAPP_ALLOW_LIVE_SEND` remains `false` until a specific production cutover approval is given and all existing gates are proven.

## Customer conversation operating loop

```text
Inbound WhatsApp
  -> Meta signature verification
  -> Existing Dealix webhook
  -> Contact/company resolution
  -> Company Brain context
  -> Opportunity/customer state
  -> Specialist agent analysis
  -> Draft response / negotiation / support action
  -> Approval Center
  -> Telegram Approval Card
  -> Founder APPROVE / EDIT / REJECT
  -> Controlled send through existing WhatsApp integration
  -> Delivery/reply outcome
  -> Opportunity Graph update
  -> Proof Ledger
  -> Learning
  -> Better next action
```

## Agent team responsibilities

### CEO / Sprint Orchestrator
- Resolve cross-department conflicts.
- Prioritize P0 trust, P1 money-now, customer risk and proof.
- Keep founder notifications concise.

### Revenue Intelligence
- Detect closeability and revenue leakage.
- Recommend the single highest-value next action.
- Never count revenue without payment evidence.

### Sales Intelligence
- Prepare discovery, objection handling, reply drafts, follow-up and negotiation strategy.
- Keep outbound draft-only until exact approval.

### Market Intelligence
- Research sourced company, sector, partner and Saudi/GCC signals.
- No prohibited scraping or fabricated contacts.

### Customer Acquisition
- Build approval-ready acquisition plans from qualified opportunities.
- No bulk WhatsApp or spam.

### Diagnostic Agent
- Turn conversation evidence into falsifiable pain/value hypotheses.

### Managed Ops / Customer Success
- Triage service requests, blockers, onboarding, adoption and expansion signals.

### Governance
- Enforce consent, suppression, claims, quiet-hours, approval, proof and commercial limits.

### Data Architect / Company Brain
- Preserve source lineage and canonical company/contact/opportunity state.

## Negotiation contract

For any request involving price, discount, scope, timeline, exclusivity, payment terms or contractual language, prepare an Approval Card containing:

- counterparty,
- opportunity ID,
- current stage,
- customer request,
- proposed response,
- price/discount delta,
- scope delta,
- timeline delta,
- give-get condition,
- floor / walk-away recommendation if known,
- evidence and rationale,
- risk,
- expiry,
- decisions: `APPROVE`, `EDIT`, `REJECT`.

No commercial commitment is sent before approval.

## Founder experience

The founder should normally receive only:

1. Morning Daily Command.
2. Urgent Production/Security alert.
3. Highest money-now opportunity.
4. Exact WhatsApp Approval Cards.
5. Major customer/delivery risk.
6. Weekly Proof/Revenue report.

Avoid duplicate Telegram + WhatsApp founder notifications by default.

## WhatsApp workflows to implement using existing Dealix contracts

- `WA_01_Inbound_Triage`
- `WA_02_Identity_Opportunity_Update`
- `WA_03_Lead_Qualification`
- `WA_04_Sales_Reply_Draft`
- `WA_05_Negotiation_Approval`
- `WA_06_Approved_Send`
- `WA_07_Delivery_Reply_Proof`
- `WA_08_Customer_Support`
- `WA_09_Appointment_Proposal_Handoff`
- `WA_10_Suppression_Consent`
- `WA_11_Customer_Success_Expansion`
- `WA_12_Conversation_Learning`

These are workflow labels, not new sources of truth.

## Activation sequence

### Gate A — Current implementation proof

Verify existing assets and tests before changing anything:

- WhatsApp Cloud API client exists.
- webhook route exists.
- signature verification exists.
- live-send flag defaults false.
- opt-in / safe-send policies exist.
- approval-card/operator flow exists.

### Gate B — Dedicated number / Meta Business setup

Founder-owned external setup:

- dedicated second number,
- Meta Business / WhatsApp Business account,
- app and phone-number registration,
- webhook configuration,
- credentials stored only in the production secret manager/Railway variables,
- no token pasted into chat or committed.

### Gate C — Staging verification

- GET webhook verification passes.
- signed POST webhook passes.
- invalid signature fails closed.
- inbound test message creates/updates the expected canonical internal record.
- no outbound message occurs.

### Gate D — Internal real-number pilot

Use only founder/controlled test recipients with known consent.

- inbound -> triage -> draft -> approval card,
- explicit approval -> one controlled send,
- delivery/reply -> proof,
- opt-out -> permanent suppression.

### Gate E — Production cutover

Requires a specific founder approval immediately before:

- setting or changing production credentials,
- enabling `WHATSAPP_ALLOW_LIVE_SEND=true`,
- any production deploy/mutation,
- first external customer send.

## Success metrics

Do not optimize for message volume.

Track:

- inbound conversations processed,
- qualified opportunities,
- draft-to-approval quality,
- approval edit rate,
- response time,
- reply rate for consented conversations,
- meeting/proposal progression,
- customer support resolution time,
- opt-outs / complaints,
- negotiation outcomes,
- payment evidence,
- delivery/value proof,
- founder minutes saved,
- learning events that improve the playbook.

## Proof contract

Every meaningful run records:

- run ID,
- timestamp,
- source event/message ID,
- company/contact/opportunity IDs when resolved,
- decision,
- draft/action,
- approval status/ID if applicable,
- execution result,
- delivery/reply outcome,
- proof/evidence reference,
- risk,
- learning event.

Synthetic data is never commercial proof.

## Master instruction for any Dealix agent

> Operate the dedicated Dealix WhatsApp business number as a governed customer-operations channel, not as a spam bot. Reuse the existing WhatsApp Cloud API, webhook, safe-send, approval, Company Brain, Opportunity Graph, Proof and Learning systems. Process inbound work automatically; research, qualify, draft, negotiate internally, support customers, prepare bookings/proposals, and create exact approval cards. Never cold-message, blast, invent consent, invent customer facts, promise commercial terms, or execute an external send without the required approval. Optimize for qualified conversations, customer value, closeability, proof and founder time saved — not message volume. Every action must leave verifiable evidence and feed the learning loop.
