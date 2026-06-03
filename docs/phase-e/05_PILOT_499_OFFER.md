# Pilot 499 SAR — Offer

The pilot tier is **499 SAR / 7 days**, manual payment only, scoped
to the `growth_starter` bundle in `docs/registry/SERVICE_READINESS_MATRIX.yaml`.

## What the customer gets (canonical)

1. **10 qualified opportunities** — ranked by feasibility × revenue
2. **10 Arabic draft messages** — bilingual where the customer's
   audience is mixed
3. **Best-channel recommendation** per opportunity (warm intro,
   referral, reply-to-existing-thread, inbound DM)
4. **7-day follow-up plan** — what to send when, with who follows up
5. **Risk check** — 1–3 specific risks to avoid for this customer
6. **Initial Proof Pack** (draft, internal-only) — for review at end
   of pilot

## What the customer does NOT get

- ❌ NO Dealix sending on their behalf (every message is manual)
- ❌ NO scraped data, NO purchased lists
- ❌ NO LinkedIn DM automation
- ❌ NO cold WhatsApp blast
- ❌ NO guarantee of revenue / leads / ROI
- ❌ NO public mention of their company without their written approval

## Pricing (canonical, do NOT change without proof)

| Item | Amount |
|---|---|
| Pilot tier | **499 SAR** (= 49,900 halalah) |
| Duration | 7 days |
| Refund window | 7 days from delivery if delivery fails the spec |
| Payment | Moyasar test-mode invoice OR bank transfer |
| Live charge | DISABLED — manual confirmation required |

> Pricing change rule: do NOT change 499 SAR until ≥ 3 archived proof
> events justify it. See `docs/PRICING_STRATEGY.md` for the full rule.

## Bilingual offer copy

**Arabic** — paste into WhatsApp / Email after the customer accepts
the Mini Diagnostic:

> ممتاز [الاسم]. عرض الـ Pilot:
> - 499 ريال (دفع يدوي)
> - 7 أيام
> - 10 فرص + 10 مسودات + خطة متابعة + Proof Pack مبدئي
> - الدفع عبر Moyasar (test) أو تحويل بنكي
> - كل رسالة بتمر عليك للموافقة قبل الإرسال
> - استرجاع كامل خلال 7 أيام إذا التسليم ما طابق المواصفات
>
> هل أرسل الفاتورة؟

**English** equivalent:

> Great [Name]. Pilot offer:
> - 499 SAR (manual payment)
> - 7 days
> - 10 opportunities + 10 drafts + follow-up plan + initial Proof Pack
> - Payment via Moyasar (test mode) or bank transfer
> - Every message passes through you for approval — Dealix never sends
> - Full refund within 7 days if delivery does not match spec
>
> Should I send the invoice?

## Acceptance steps

1. Customer says yes → run `python scripts/dealix_invoice.py` to
   draft a Moyasar test-mode invoice OR provide bank details
2. Customer pays / confirms commitment → mark `pilot=paid_or_committed`
   in the board
3. Same day: start delivery per `07_7_DAY_PILOT_DELIVERY_PLAN.md`
4. Day 7: deliver Proof Pack draft per `08_PROOF_PACK_TEMPLATE.md`
5. Day 8–10: customer review + upsell call per
   `09_CUSTOMER_REVIEW_AND_UPSELL.md`
