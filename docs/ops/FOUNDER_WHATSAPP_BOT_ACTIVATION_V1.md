# Dealix Founder WhatsApp Bot — Activation Runbook V1

## Objective

Connect an owned business number to the existing Dealix Company OS so inbound WhatsApp conversations can be classified, drafted, negotiated safely, approved when required, dispatched through the canonical provider, and written back as provider receipts + proof.

This runbook does **not** contain secret values and does not authorize live sending by itself.

## Canonical architecture

`Meta webhook -> normalized inbound event -> conversation queue -> Founder Reply Brain -> ExternalActionPacket -> Founder Delegation / canonical authority resolver -> Meta transport -> provider receipt -> Proof Ledger -> learning`

Use the existing components. Do not create a second CRM, model router, approval authority, scheduler, or messaging gateway.

## Canonical components

- Inbound Meta webhook: `POST /api/v1/webhooks/whatsapp`
- Transitional GREEN-API webhook: `POST /api/v1/webhooks/green-api`
- Official Meta client: `integrations/whatsapp.py`
- Governed provider adapter: `auto_client_acquisition/email/whatsapp_multi_provider.py`
- Reply / negotiation brain: `dealix/company_os/founder_reply_bot.py`
- Queue-friendly worker: `scripts/commercial/prepare_founder_whatsapp_reply_v1.py`
- Exact material authority: `dealix/commercial/external_execution_gate.py`
- Bounded founder delegation: `dealix/company_os/founder_delegation.py`

## Runtime references — names only

Store values in the approved runtime secret store, never in Git.

Required Meta Cloud references:

- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_VERIFY_TOKEN`
- `WHATSAPP_APP_SECRET`
- `WHATSAPP_GRAPH_API_VERSION=v26.0`
- `DEALIX_FOUNDER_PHONE_E164`

Keep these fail-closed until exact activation:

- `WHATSAPP_ALLOW_LIVE_SEND=0`
- `DEALIX_EXTERNAL_SEND=0`
- `MODE=draft-only`

Optional transitional provider references already supported by the repository:

- `GREEN_API_INSTANCE_ID`
- `GREEN_API_TOKEN`
- `GREEN_API_WEBHOOK_TOKEN`

Do not silently fall back from a configured Meta sender to an unofficial provider after a Meta failure.

## Phase 0 — source acceptance

Before attaching the number:

1. #1600 Production Trust must be resolved independently.
2. #1605/#1607 exact-head source acceptance must be green on an execution environment that actually ran the tests.
3. Confirm the command-room verifier reports zero live-ready customer channels unless separately proven.
4. Confirm the Meta Graph API version tests pass and no `graph.facebook.com/v20.0` hardcode remains in WhatsApp send paths.

## Phase 1 — inbound-only canary

Configure the owned test number and Meta webhook. Keep outbound switches at zero.

Acceptance evidence:

- Meta webhook verification succeeds.
- Production/staging rejects missing or invalid `X-Hub-Signature-256` when app secret is configured.
- One founder-generated inbound test message produces exactly one normalized event.
- Duplicate webhook delivery does not create duplicate downstream effects.
- No provider send occurs.

## Phase 2 — 24/7 draft intelligence

Wire the normalized event into `conversation_queue` and invoke:

```text
python scripts/commercial/prepare_founder_whatsapp_reply_v1.py --input EVENT.json --out DRAFT.json --local-only
```

On the VPS, the preferred model path is the existing Dealix Model Router with local Ollama first. The worker never sends. It returns only draft metadata and an optional `ExternalActionPacket`.

The Reply Brain must:

- detect Arabic vs English;
- recognize pricing, objections, meetings, support, and general intent;
- answer as `Dealix Founder Office`, not falsely as personally typed by the founder;
- avoid fabricated proof or buyer intent;
- avoid binding price, discount, contract, payment, refund, tender, or guarantee terms;
- ask one useful qualifying question when context is insufficient;
- degrade to review when model output is unavailable or low-confidence.

## Phase 3 — bounded autonomous reply eligibility

A draft can move to the execution queue only when the exact conversation has current evidence for:

- identity / relationship or inbound-thread eligibility;
- channel/purpose authority;
- fresh suppression check and `suppression_clear=true`;
- sender identity;
- action hash and packet integrity;
- expiry;
- idempotency key;
- provider selection;
- evidence references.

A Founder Delegation Session may cover a finite known conversation, purpose, recipient set, time window and message/call budget. It does not create universal send authority.

Any new recipient, new purpose, material commercial term, quote, contract, payment, public publish, paid spend, tender, or scope change requires a new exact authority decision.

## Phase 4 — one-conversation live canary

This phase is a separate action-bound production authorization. Do not infer it from repository merge or provider credentials.

For the canary:

- one owned/test conversation only;
- one exact approved reply packet;
- `WHATSAPP_ALLOW_LIVE_SEND` and `DEALIX_EXTERNAL_SEND` enabled only through the canonical runtime authority for the bounded action;
- no unofficial fallback;
- capture Meta message ID / provider receipt;
- append receipt to Proof Ledger;
- verify duplicate execution is rejected by idempotency;
- restore/confirm fail-closed switches after the bounded canary.

## Phase 5 — production autonomous replies

Only after Phase 4 evidence:

- inbound and explicitly requested follow-up are the highest automation priority;
- every effect is limited to a current approved/delegated conversation scope;
- suppression/opt-out is rechecked immediately before dispatch;
- reply packet expires quickly;
- material commitments still escalate;
- retries reuse the same idempotency identity;
- every provider effect produces a receipt;
- model failure never becomes a fabricated successful reply.

## Negotiation policy

The bot may autonomously prepare and, within a valid bounded delegation, reply about:

- needs discovery;
- workflow symptoms;
- qualification questions;
- scheduling;
- non-binding capability explanation;
- objections;
- next-step framing;
- diagnostic scope clarification.

It must not autonomously bind Dealix to:

- customer-specific price or discount;
- contract/legal terms;
- guaranteed outcomes;
- payment/refund commitments;
- tender submission;
- public claims;
- paid spend.

For price requests, use the canonical path: `Execution Diagnostic / Qualified Discovery -> Customer-Specific Quote`.

## Voice / phone extension

Voice is a separate provider and authority surface. When added, the automated agent must identify itself as an automated/AI Dealix assistant acting for the Founder Office unless the human founder takes over. Calls require a finite delegation/call budget, recipient/thread eligibility, recording/transcription policy where applicable, provider receipts, and a kill switch.

## 24/7 operating loop

Do not create one cron per channel. Use the existing canonical scheduler and queues:

- event-driven wakeup for inbound conversations;
- queue reconciliation and dead-letter recovery;
- priority by customer/revenue risk, not message volume;
- local-first model routing;
- proof/receipt append;
- learning event after failure or override;
- founder surfaced only for material authority, low confidence, unresolved risk, or high-value decision.

## Definition of ready

The bot is production-ready only when all of the following are true for the exact running release:

- source acceptance green;
- correct running SHA proven;
- inbound webhook signature gate proven;
- owned number/provider identity proven;
- local/model-router health proven;
- conversation queue + worker proven;
- suppression and eligibility evidence proven;
- external execution gate proven;
- idempotency proven;
- provider receipt + Proof Ledger append proven;
- one bounded live canary proven;
- rollback/kill switch proven.

`provider credentials != authority`

`inbound message != marketing consent`

`draft != sent`

`provider 200 != verified business outcome`
