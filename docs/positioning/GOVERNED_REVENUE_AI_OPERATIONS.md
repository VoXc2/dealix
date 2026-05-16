# Dealix — Governed Revenue & AI Operations

> **EN:** Dealix sells the governed operation of revenue and AI: clear sources,
> approvals, evidence, decisions, and measurable value.
>
> **AR:** Dealix لا تبيع الذكاء الاصطناعي فقط، ولا RevOps فقط. Dealix تبيع التشغيل
> المحكوم للإيراد والذكاء الاصطناعي: مصادر واضحة، موافقات، أدلة، قرارات، وقيمة قابلة للقياس.

## Why this positioning

Most companies have adopted AI but lack the operating layer to make it
trustworthy: source clarity, approval boundaries, evidence trails, and proof of
value. "Governed Revenue & AI Operations" is stronger than a plain AI agency and
stronger than ordinary RevOps because it combines Revenue Ops + AI Governance +
an Evidence Ledger + an Approval Center + Decision Passports + Proof Packs +
Retainers into one operating discipline.

## The canonical chain

Every unit of work passes through this chain — anything that skips a link is
likely a distraction:

```
Signal → Source → Approval → Action → Evidence → Decision → Value → Asset
```

## North Star — Governed Value Decisions Created

The North Star is **not** user count. It is the number of revenue or operational
decisions taken with: a clear source, a clear approval, an evidence trail, and a
measurable impact. Encoded in
`auto_client_acquisition/governed_value_os/decisions_ledger.py` — a decision
without source, approval, and evidence is refused, not recorded.

## The 3 headline offers

Present three packages, not seven:

1. **Governed Revenue Ops Diagnostic** — 4,999–25,000 SAR
2. **Revenue Intelligence Sprint** — 25,000 SAR
3. **Governed Ops Retainer** — 4,999–35,000 SAR / month

Catalog of record: `auto_client_acquisition/service_catalog/governed_catalog.py`
(7 governed services; AI Governance, CRM/Data Readiness, Board Decision Memo, and
Trust Pack Lite are scoped per engagement). The existing 7 canonical offerings in
`registry.py` are kept alongside this governed tier — nothing is retired.

## The strict proof state machine (L2–L7)

`auto_client_acquisition/governed_value_os/state_machine.py`:

| State | Level | Hard rule |
|---|---|---|
| prepared_not_sent | L2 | — |
| sent | L4 | no `sent` without `founder_confirmed` |
| replied_interested / meeting_booked | L4 | — |
| used_in_meeting | L5 | no L5 without a prior booked meeting |
| scope_requested / pilot_intro_requested | L6 | no L6 without a scope/intro request |
| invoice_sent | L7_candidate | — |
| invoice_paid | L7_confirmed | no L7 confirmed without a payment reference |

Revenue is recognized only at `invoice_paid`. These rules are codified as 4 of the
**11 non-negotiables** (`safe_send_gateway/doctrine.py`).

## The 7-gate map

`auto_client_acquisition/governed_value_os/gate_map.py` — build only past Gate 7:

1. First Market Proof — 5 messages sent, first reply/silence classified
2. Meeting Proof — `used_in_meeting` (L5) reached
3. Pull Proof — `scope_requested` (L6) reached
4. Revenue Proof — `invoice_paid` (L7 confirmed) reached
5. Repeatability — the same offer sold twice
6. Retainer — a recurring monthly engagement is live
7. Platform Signal — a manual workflow repeated 3+ times

## Full Ops — what it means

Full Ops does **not** mean AI sends, charges, and acts on its own. It means: the
system prepares, suggests, warns, records, verifies, classifies, and drafts — and
the founder approves every external action. This control plane is the moat, not
the bottleneck.

## Moats

Proof moat · Trust moat · Revenue moat · Workflow moat · Saudi/GCC localization
moat · Approval-first safety moat · Service-to-platform learning moat.

## Versus competitors

- **Traditional RevOps** gives CRM cleanup, pipeline reporting, forecasting.
  Dealix adds AI governance, approval boundaries, evidence trails, decision
  passports, proof packs, and no autonomous external actions.
- **AI sales agents** give AI SDR / AI outbound. Dealix requires source clarity,
  approval boundaries, evidence, and risk gates *before* anything is sent.
- **AI consulting** gives decks and workshops. Dealix adds an execution ledger,
  proof pack, billing, decision passport, and operational gates.

## Signals

`python scripts/governed_value_signals.py` prints the North Star count, the
7-gate map, and the proof state machine.
