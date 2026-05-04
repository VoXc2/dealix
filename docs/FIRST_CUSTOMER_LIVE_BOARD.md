# First Customer Live Board

> Single source of truth for every prospect through pilot through proof.
> Update after every interaction. Use placeholders until real names are
> recorded by the founder.

## Board

| # | Company | Person | Segment | Source | Channel | Status | Last Action | Next Step | Diagnostic Sent | Pilot Offered | Payment/Commitment | Proof Pack | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | _placeholder_ | _placeholder_ | _saas/agency/training/services/recruitment_ | linkedin_1st / referral / inbound | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 2 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 3 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 4 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 5 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 6 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 7 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 8 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 9 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |
| 10 | _placeholder_ | _placeholder_ | | | linkedin_manual | selected | — | send Arabic warm | — | — | — | — | — |

## Allowed status values

```
selected
messaged
replied
diagnostic_requested
diagnostic_sent
pilot_offered
invoice_or_payment_sent
paid_or_committed
in_delivery
proof_pack_sent
closed_won
closed_lost
nurture
```

## Allowed channels

```
linkedin_manual         (1st-degree, founder sends from own account)
inbound_wa_me           (prospect messages first via wa.me link)
opt_in_form             (prospect submits the website form)
email_draft_with_approval  (founder approves before send)
referral                (warm intro from a mutual contact)
```

## Forbidden — never log these as "messaged"

- cold WhatsApp to numbers without recorded consent
- LinkedIn automation tools (Phantom, Dux, Expandi, etc.)
- purchased lists
- email blasts
- scraped contacts

## Daily logging rule

Every prospect must have at least one row update per day they're active.
Empty days = `nurture` status. Missing daily updates = data loss.
