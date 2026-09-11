# Dealix Omnichannel Founder Command Room V1

## Mission

Make the VPS-resident Dealix Company OS the default operator of Dealix. Chat sessions are not the operating system. The founder should primarily issue commands, inspect proof, resolve exceptions, and grant exact material authority where needed.

North Star: `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

This command room inherits the Fast Compression Constitution and Arm Registry. It does not create a second Company Brain, CRM, scheduler, model router, approval center, proof ledger, or permanent agent fleet.

## Permanent operating model

Exactly five permanent agents remain:

- `dealix-pm` — company command, priorities, scorecard, approval queue, founder brief.
- `dealix-sales` — market signals, Opportunity Graph, conversations, diagnostics, discovery, proposal/quote preparation, partnerships and B2G intelligence.
- `dealix-delivery` — commercial handoff, delivery, support, acceptance, customer health and proof.
- `dealix-engineer` — Production Trust, connectors, security, data/identity policy, CI, Railway, observability and runtime.
- `dealix-content` — evidence-backed content, website/social drafts, distribution and publishing packets.

All governed arms map to one of those agents. Temporary specialists are bounded workloads only.

## Execution pipeline

Every event follows one traceable path:

```text
Channel Event
-> Identity / Thread Resolution
-> Evidence
-> Intent / Commercial Stage
-> Arm + Owner Agent
-> Work Queue
-> Authority Classification
-> Action Packet
-> Current Authority Resolution
-> Provider Boundary
-> Receipt
-> Proof Ledger
-> Learning
```

The command room must optimize for verified business movement, not message volume.

## Canonical queues

- `signal_queue`
- `work_queue`
- `conversation_queue`
- `approval_queue`
- `execution_queue`
- `proof_queue`
- `learning_queue`
- `dead_letter_queue`

Any item that can eventually create a side effect also needs idempotency and reconciliation metadata.

## Command surfaces

- Slack `#dealix-command` — primary internal executive room.
- Telegram founder proof plane — mobile command and receipts.
- VPS control plane — actual agent execution, queues, local-first model routing and scheduled reconciliation.
- GitHub — source truth for code, issues, PRs and acceptance evidence.
- Airtable — operational mirrors for sorting/assignment; not authority truth.

## Omnichannel architecture

The target architecture uses one conversation gateway rather than custom state machines per social channel. A gateway may normalize Website Chat, Email, WhatsApp, Facebook, Instagram, Telegram, TikTok, SMS, LINE and API inbox events, while Dealix remains the decision/authority/proof layer above it.

Current research candidate: Chatwoot. Admission state is `CANDIDATE`, not production authority. It is useful because its current public channel model can cover a broad set of inbound/outbound inboxes and exposes conversation/message APIs. Provider admission still requires a bounded benchmark, security/data review, tenancy decision, recovery plan and exact production acceptance.

Do not confuse gateway channel support with Dealix live-send authority.

## Current execution-readiness truth

| Channel | Current V1 state | Meaning |
|---|---|---|
| Slack command | INTERNAL_READY | Internal command surface exists. |
| Telegram founder | INTERNAL_READY | Founder control/proof surface exists in the current VPS architecture. |
| Website forms / diagnostic | INBOUND_READY | Existing inbound bridge is part of the Company OS path. |
| Gmail | PROVIDER_QUARANTINED | Existing guarded provider intentionally refuses live execution until provider-owned authority/idempotency dependencies are wired. |
| WhatsApp Business | ADAPTER_PRESENT_AUTHORITY_NOT_PROVEN | Repository adapters exist; command-room V1 does not claim current production sender authority. |
| Website chat / Facebook / Instagram / TikTok / customer Telegram / SMS / LINE / API inbox | NOT_WIRED | Target channels are registered but no live Dealix provider claim is made. |
| Voice | NOT_WIRED | Target supports AI/automated handling only after a verified voice provider, disclosure and exact authority gate exist. |
| Founder LinkedIn | MANUAL_ONLY | Research/draft support only; no autonomous personal LinkedIn outreach. |

`NOT_WIRED`, `QUARANTINED`, or `AUTHORITY_NOT_PROVEN` must never be promoted to PASS.

## Founder Delegation Sessions

A founder delegation session lets the Company OS handle a bounded, known conversation on behalf of the Founder Office while preserving exact action-bound control.

A session binds:

- verified founder identity reference;
- exact channel/provider;
- conversation/thread and/or recipient set;
- allowed purposes and action classes;
- start and expiry;
- message/call budgets;
- commercial limits;
- prohibited commitments;
- current relationship/consent/channel-eligibility evidence;
- current suppression state;
- sender identity;
- kill switch;
- canonical approval reference.

V1 only permits a session to make ordinary `EMAIL_SEND` or `WHATSAPP_SEND` actions for `INBOUND_REPLY`, `REQUESTED_FOLLOWUP`, or `TRANSACTIONAL` purposes **eligible for exact action-bound approval**. It does not execute the provider call by itself.

A delegation session cannot authorize a binding quote, contract commitment, payment/refund, paid spend, public publishing, merge, deployment, DNS, production database, or secret mutation.

A new recipient, different message material, different purpose, different channel/provider, expired session or altered commercial scope requires new authority. The canonical `ACTION_HASH` contract remains authoritative.

## Founder identity and phone number

The repository stores only an environment-variable reference such as `DEALIX_FOUNDER_PHONE_E164`; the number itself belongs in the VPS secret/runtime layer, not Git.

For text channels, automated messages should be represented as coming from `Dealix Founder Office` or clearly on behalf of the founder. The system must not assert that the founder personally typed a message when an agent generated it.

For automated voice, the assistant must identify itself as an automated/AI Dealix assistant acting for the Founder Office before substantive business discussion, unless the human founder takes over the call.

## Commercial behavior

Canonical progression:

```text
Signal
-> Real Interaction
-> Qualified Problem
-> Free Mini Diagnostic
-> Qualified Discovery
-> Customer-Specific Quote
-> Verified Payment
-> Governed 30-Day Delivery
-> Customer-Validated Proof
-> Expand / Refer / Redesign / Stop
```

Rules:

- `research != relationship`
- `public_contact != consent`
- `draft != sent`
- `quote != invoice`
- `invoice != payment`
- `synthetic != customer proof`
- `HTTP 200 != correct release`
- `merge != Production Green`

## Server-side cycle

Canonical entrypoint:

```bash
python scripts/commercial/run_dealix_command_room_v1.py --mode draft-only
```

Optional proof-pack inclusion:

```bash
python scripts/commercial/run_dealix_command_room_v1.py --mode draft-only --include-proof-pack
```

The runner delegates to the existing Company OS, autonomous growth and self-improvement runners. It writes command-room receipts under:

```text
reports/company_os/command_room/
```

The VPS installer places one wrapper into the already-existing autonomous-company control plane. It deliberately creates **no new scheduler**:

```bash
bash scripts/ops/install_dealix_command_room_v1.sh
```

The existing canonical scheduler should only be repointed after exact acceptance of this branch and reconciliation with its current service definition.

## CEO views

The internal room should render:

1. CEO Now — top five decisions, blockers and money movements.
2. Production Trust.
3. Revenue / Opportunity Graph.
4. Conversations requiring action.
5. Delivery / Customer Health.
6. Proof Ledger.
7. Approval + Founder Delegation sessions.
8. Content / Distribution.
9. Partner / B2G.
10. Finance / Economic Truth.
11. Learning / failures / experiments.
12. Runtime / connectors / model cost and reliability.

## Acceptance gates

Before the server scheduler calls this runner:

1. command-room verifier passes;
2. focused command-room tests pass;
3. no sixth permanent agent;
4. every governed arm has a canonical owner;
5. every channel has explicit readiness and authority policy;
6. zero unproven channel is marked live-ready;
7. delegation expiry/revocation/budget/scope tests pass;
8. exact action hash changes when message material changes;
9. provider execution remains owned by the canonical external execution gate;
10. PR #1600 Production Trust is neither weakened nor declared green by this feature.

## Production boundary

This V1 builds the command and delegation plane. It does not claim that customer-facing live providers are ready today. Each provider moves through:

```text
NOT_WIRED
-> ADAPTER_PRESENT
-> PROVIDER_QUARANTINED
-> EXACT ACCEPTANCE
-> CURRENT AUTHORITY RESOLVER
-> IDEMPOTENCY + RECONCILIATION
-> CONTROLLED LIVE SESSION
-> VERIFIED RECEIPTS
```

Only evidence promotes state.
