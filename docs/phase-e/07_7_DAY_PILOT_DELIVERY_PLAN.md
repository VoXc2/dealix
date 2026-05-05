# 7-Day Pilot Delivery Plan

After the customer pays / commits, you have **7 working days** to
deliver. Each day has a specific deliverable. NO live send across the
whole 7 days — every message is drafted by Dealix + sent manually by
the founder + after customer approval.

## Day-by-day

### Day 0 (kickoff, ~30 min)

- Confirm payment / commitment
- Run `python scripts/dealix_diagnostic.py` for the customer (use
  the inputs the customer gave during the warm intro)
- Save the Diagnostic to `docs/diagnostics/<slot>.md` (gitignored
  unless customer asks for repo storage)
- Send the Diagnostic to the customer for record

### Day 1 — Opportunity ranking

- Generate 10 opportunities (use sector + region + customer notes)
- Rank by feasibility × revenue
- Send the 10 to the customer in a single bilingual document
- Customer picks ≤ 5 to act on

### Day 2 — Drafts

- Draft 1 message per chosen opportunity
- Bilingual where the audience is mixed
- NO `نضمن` / `guaranteed` / "blast" / cold-WhatsApp
- All drafts marked `audience: <warm_intro|referral|inbound_dm>`
- Send drafts to customer for approval

### Day 3 — First approved sends

- Customer approves N drafts
- Customer sends them manually (Dealix never sends)
- Log each send in the customer's local notes (NEVER in this repo)

### Day 4 — Follow-up plan

- Build a 7-day follow-up calendar
- Draft 1 follow-up message per opportunity (in case of no reply)
- Customer reviews + approves

### Day 5 — Risk check

- Review what's been sent vs. customer's policy
- Identify ≤ 3 risks (PDPL, brand, tone) to avoid
- Prepare 1-page bilingual risk note for the customer

### Day 6 — Proof Pack draft

- Run `python scripts/dealix_proof_pack.py` with the recorded
  events from day 1–5
- Output marked `audience: internal_only`, `decision: review_required`
- Send to customer for review

### Day 7 — Customer review + upsell

- 30-min call: walk through the Proof Pack
- Get customer feedback on each section
- Mark which events the customer approves to publish (default: NONE)
- Discuss next steps per `09_CUSTOMER_REVIEW_AND_UPSELL.md`

## Quality bars (non-negotiable)

- Every draft passes `tests/test_landing_forbidden_claims.py`
  forbidden-token list
- Every draft is `<= 200 words` for WhatsApp / `<= 400 words` for email
- Every draft includes a clear ask (a question or next step)
- NO draft references a metric the customer didn't supply
- NO draft references a specific named competitor without a public
  source
- NO draft uses the customer's PII in clear (use `[الاسم]` placeholders)

## Delivery escalation

If by Day 5 the customer hasn't approved any drafts:
- Schedule a 15-min call to unblock
- Ask whether the channel choice is wrong, the tone is wrong, or
  the offer itself is wrong
- Adjust + reship — do NOT auto-extend the 7-day window without
  explicit founder agreement

## Bilingual one-liner

**Arabic**: 7 أيام، كل خطوة بموافقتك، Dealix لا يرسل بالنيابة.
**English**: 7 days, every step approved by you, Dealix never sends on your behalf.
