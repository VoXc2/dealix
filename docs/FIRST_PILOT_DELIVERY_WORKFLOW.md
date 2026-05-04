# First Pilot — 7-Day Delivery Workflow

> Strict day-by-day. The Proof Pack on day 7 is the deliverable that
> closes the pilot and unlocks the upsell conversation. No live external
> sends during delivery.

## Day 0 — payment confirmed

- [ ] Mark `paid_or_committed` in `docs/FIRST_CUSTOMER_LIVE_BOARD.md`
- [ ] Confirm the company info (name, website, sector, city)
- [ ] Confirm the ICP (one ICP — no scope creep)
- [ ] Confirm allowed channels (LinkedIn manual / inbound wa.me / opt-in form / email draft)
- [ ] Send a 1-line confirmation in Arabic: "Pilot ابتدأ. أرجع لك بالتقرير اليومي خلال ٧ أيام."

## Day 1 — service session + first segment

- [ ] Create service session: `POST /api/v1/operator/service/start { bundle_id:"growth_starter", company_name, sector, ideal_customer, ... }`
- [ ] Define the **target segment** (≥ 1 specific industry × city × size band)
- [ ] Run `POST /api/v1/business/verticals/recommend` for sector-fit signals
- [ ] Draft the first 5 of the 10 opportunities (specific company names)

## Day 2 — full opportunity list + contactability scoring

- [ ] Complete the 10 opportunities
- [ ] For each: `POST /api/v1/compliance/check-outreach` to flag any opt-out / consent risk
- [ ] Score each by contactability (warm path? mutual contact? inbound history?)
- [ ] Note risks per row — what NOT to do per opportunity

## Day 3 — message drafts

- [ ] 6 message drafts (Arabic + English variants where useful)
- [ ] Run `POST /api/v1/personal-operator/messages/draft` for each
- [ ] Forbidden-tokens sweep on every draft (no `نضمن`, no `guaranteed`)
- [ ] 3 follow-up angles, one per day after first send

## Day 4 — scripts + risk review

- [ ] If the customer's offer suits calls/meetings: prepare a meeting brief via `POST /api/v1/personal-operator/meetings/schedule-draft`
- [ ] Risk review: collect every blocked decision from the week so far (compliance/check-outreach `allowed:false` rows)
- [ ] Build the "what was protected" section for the Proof Pack

## Day 5 — Proof Pack draft + next recommendation

- [ ] Open `docs/FIRST_CUSTOMER_PROOF_PACK_TEMPLATE.md` and fill it
- [ ] Run `POST /api/v1/customers/{customer_id}/proof-pack` and `POST /api/v1/command-center/proof-pack`
- [ ] Identify the next-step recommendation:
  - Continue Pilot (if customer wants more)
  - Upgrade to **Executive Growth OS** (2,999 SAR/mo) — only if grade ≥ B
  - Run **Data to Revenue** (1,500 SAR) — if customer has a list
  - Run **Partnership Growth** (3,000-7,500 SAR) — if customer is an agency
  - Stop — if not a fit

## Day 6 — review + clean

- [ ] Founder/operator self-review: every claim has evidence
- [ ] Estimates clearly labeled as `تقدير` / `estimate` — never bare numbers
- [ ] No invented opportunities, no invented outcomes
- [ ] Arabic tone is Saudi-professional, not robotic

## Day 7 — deliver

- [ ] Send the Proof Pack via LinkedIn DM or email (manual)
- [ ] Update board row to `proof_pack_sent`
- [ ] Schedule a 24h follow-up to discuss the next step
- [ ] If customer agrees to upgrade → start Executive Growth OS onboarding
- [ ] If customer declines → say thanks, move to `nurture`, do NOT push

## Hard rules during delivery

| Rule | Reason |
| --- | --- |
| No live external sends | We deliver drafts + recommendations; customer sends if they want |
| All compliance checks recorded | Each blocked outreach becomes an entry in "What was protected" |
| Daily progress note | One short update per day to the customer's WhatsApp/email |
| Bounded scope | 10 opps / 6 drafts / 3 follow-ups / 1 ICP — never expand silently |
| No discount, no scope discount-trade | If they ask for more, offer the next tier |
| Day 7 is hard | If you slip → trust gone → no upsell |

## Definition of done

- [ ] Proof Pack delivered on day 7 (HMAC label TBD, but content complete)
- [ ] Board row = `proof_pack_sent`
- [ ] Upsell recommendation explicit
- [ ] Next-step ask sent
