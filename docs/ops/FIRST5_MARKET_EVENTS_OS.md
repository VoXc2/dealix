# First 5 Market Events OS

Executive rule:

> No new internal build unless tied to a real market event.

This operating loop is for the immediate commercial phase:
- send 5 high-quality warm messages,
- log real outcomes only,
- convert signal to meeting, scope, invoice, and paid proof.

## KPI focus (only 7)

1. `sent_count`
2. `reply_count`
3. `meeting_booked_count`
4. `l5_count`
5. `l6_count`
6. `invoice_sent_count`
7. `paid_proof_count`

Any extra KPI is secondary until paid proof appears.

## Event truth model

- `sent` = L4 exposure. Never log before real send.
- `replied_*` = L4 signal.
- `meeting_booked` = scheduling signal (still pre-L5).
- `used_in_meeting` = L5.
- `scope_requested` or `pilot_intro_requested` = L6.
- `invoice_sent` = L7 candidate.
- `invoice_paid` = revenue confirmed.

## CLI

Prepare first 5 from warm pool (first 20 rows in tracker, unsent only):

- `python3 scripts/dealix_market_events.py prepare-first5`

Record a real send (requires explicit confirmation):

- `python3 scripts/dealix_market_events.py record --id 1 --event sent --source-ref "manual_whatsapp_2026-05-16T12:10Z" --confirm`

Record reply / meeting / scope:

- `python3 scripts/dealix_market_events.py record --id 1 --event replied_interested --source-ref "email_reply_2026-05-17T08:22Z"`
- `python3 scripts/dealix_market_events.py record --id 1 --event meeting_booked --source-ref "calendar_hold_2026-05-17T08:30Z"`
- `python3 scripts/dealix_market_events.py record --id 1 --event scope_requested --source-ref "meeting_notes_2026-05-17"`

Render CEO summary:

- `python3 scripts/dealix_market_events.py summary`

## Governance boundaries

- No cold WhatsApp.
- No LinkedIn automation.
- No scraping.
- No external send by agent.
- No fake proof.
- No fake revenue.
- No attachment blast unless explicitly requested.

## Offer flow

1. Controlled Strategic Diagnostic
2. Revenue Intelligence Sprint
3. Governed Ops Retainer

Pricing and scope changes happen only after real signal (L5/L6), not after silence.
