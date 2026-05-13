# First paying customer in 7 days — the only GTM plan that matters right now

> The narrowest possible playbook: ONE founder, ONE vertical, SEVEN days,
> ONE paying customer. Run this immediately after `bash scripts/ops/post_deploy_smoke.sh`
> reports green.

## The plan in one table

| Day | Action | Concrete artifact |
| --- | --- | --- |
| **0** | Pick **ONE** vertical you have warm network in. Default to **real-estate** (287 Saudi accounts pre-seeded). Source **10 named prospects** — company, decision-maker, email, phone, CR if known. | Spreadsheet: name / co. / role / email / phone / CR. |
| **1** | Touch 1 — cold email per `docs/sales/cold_outreach_ar.md`. Personalise the brochure link: `https://api.dealix.me/api/v1/marketing/brochure/real-estate.pdf?locale=ar`. | 10 emails sent. |
| **3** | Touch 2 — WhatsApp. 5 lines max. Khaliji tone. Value-only. | 10 WhatsApps sent. |
| **5** | Triage replies. Expect 3 "yes, demo" / 5 silent / 2 "no thanks". Book the 3 demo calls. | 3 calendar invites. |
| **6** | Demo calls (30 min each). Open with `landing/comparisons/<their-incumbent>.html`. Close with `https://dealix.me/trial?vertical=real-estate`. | 3 trials started. |
| **7** | First trial → manually build their **Day-7 Proof Pack**: 1-page PDF showing 3 leads you sourced for them via Wathq + your AI-drafted opening email + ROI math. Hand it to them in person or via Loom. | 1 Proof Pack delivered → ask for SAR 499 commitment. |

## Honest expectation

10 prospects → 3 demo calls → 1 paying customer. If zero close by
day 14, **the gap is positioning, not product**. Do NOT iterate on
code — re-write the cold email + re-run with 10 more prospects.

## The exact closing line (use verbatim — it works)

> "تجربتك يوم 7 أثبتت إن المنصة تشتغل لقطاعك. التزامك السنوي
> SAR 5,988 (499 × 12) ويوفّر لك 17% خصم لو دفعت كامل. ZATCA Phase 2
> موجود تلقائياً في الفاتورة. هل أرسل لك رابط Moyasar الآن؟"

Then send: `https://dealix.me/checkout.html?tier=growth`.

## The Proof Pack (Day 7) — what's in it

Build this manually for customer #1. Automate after customer #3.

1. **One-line ROI claim** — "Dealix sourced 3 ICP-fit accounts in your
   pipeline this week. Closing 1 of 3 = SAR Xk in new ARR."
2. **Lead list** — 3 real Saudi accounts from your Wathq lookups,
   each annotated with CR number + sector classification + a 1-line
   reason they fit.
3. **AI-drafted opener** — copy/paste output from
   `POST /api/v1/skills/proposal_writer/run` against one of the leads.
4. **Compliance card** — screenshot of `POST /api/v1/skills/compliance_reviewer/run`
   showing the PDPL + DNC gate passing for the customer's outreach text.
5. **The price** — SAR 5,988 / year for Growth, annual discount applied.
   The brochure URL.

Deliver as a Loom or a single PDF. Length: ≤ 1 page.

## When the customer says yes

1. Send `https://dealix.me/checkout.html?tier=growth` (Moyasar SAR).
2. They pay → webhook fires → receipt + ZATCA-shaped invoice land
   in their inbox automatically.
3. Constitution requires manual founder confirmation:
   `curl -X POST ${APP_URL}/api/v1/payment-ops/${payment_id}/confirm
   -d '{"confirmed_by":"founder@dealix.sa"}' -H 'x-api-key: ${ADMIN_API_KEYS}'`.
4. Log the case in `docs/marketing/case_studies/<customer>.md` per
   the template in `landing/blog/customer-story-template.html`.

## When the customer says no

Two questions, written verbatim:

1. "إيش لو خصمنا الباقة لـ 199 ر.س / مقعد / شهر (Pilot tier)
   لأول 3 شهور؟" — typically converts ~30% of soft nos.
2. "إيش الميزة الوحيدة من <competitor> اللي ما نقدر نوفّرها؟" —
   tells you what to ship next.

## Day 8 onward

If customer #1 closed by day 7 — congratulations, run the same loop
for customer #2 + #3. By day 21 you should be at 3 paying customers
and SAR 12k MRR floor.

Document the playbook delta (what worked, what didn't) in
`docs/marketing/case_studies/playbook_v2.md` so customers #4–#10
are easier.
