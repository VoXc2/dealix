# GTM Execution Plan v6 — خطة الذهاب إلى السوق

> **Hard rule:** All outreach is warm/manual. No automation. No purchased lists.
> **Wedges:** 3 narrow segments. NO 32-service shotgun.

**Date:** 2026-05-05
**Owner:** Founder
**Goal:** First 3 paying Pilots within 14 days.

---

## The 3 wedges

| # | Wedge | Why this wedge first |
|---|---|---|
| 1 | **B2B marketing agencies in Riyadh** | They know `Dealix`-the-product because they live the problem; they buy quickly when they see Proof. |
| 2 | **B2B services companies, 10–50 employees** | Big enough to have lead flow, small enough that founder is the buyer. |
| 3 | **Training & consulting firms with clear offers** | Already have a sales process; Dealix tightens it. They pay for execution, not strategy. |

**NOT in wedges:** B2C, e-commerce, healthcare, real estate, government,
enterprise (>200 employees). Each is a separate go-to-market motion;
defer.

---

## The 14-day plan

### Days 0–2 (today through Day 2)

- [ ] Founder lists **10 warm prospects** across the 3 wedges
  (private note, not in this repo)
- [ ] Verify production redeploy (`bash scripts/post_redeploy_verify.sh`)
- [ ] Each prospect: short 3-line bilingual message (see `FIRST_10_WARM_MESSAGES_AR_EN.md`)

### Days 3–7

- [ ] Send the 10 messages MANUALLY (one platform/day; LinkedIn = manual DM only)
- [ ] Target: 3 replies → 3 Diagnostic calls
- [ ] Run `python scripts/dealix_diagnostic.py` for each
- [ ] Convert at least 1 to Pilot 499 SAR

### Days 8–14

- [ ] Deliver the first Pilot per `docs/V5_PHASE_E_DAY_BY_DAY.md`
- [ ] Assemble the first Proof Pack (`python scripts/dealix_proof_pack.py`)
- [ ] Founder review: what worked, what didn't
- [ ] Update `docs/OBJECTION_HANDLING_V6.md` with patterns observed

---

## Channel rules (re-asserted)

| Channel | Allowed action | Forbidden action |
|---|---|---|
| **WhatsApp** | Reply to inbound. Send to opt-in list. Use approved templates. | Cold WhatsApp. Mass send. Auto-send. |
| **Email** | Manual send to warm prospects. Draft via `dealix_diagnostic.py`. | Cold email. Live auto-send. Mass send. |
| **LinkedIn** | Manual DM to first-degree connections. View public profiles. | Auto DM. Connection automation. Scraping. |
| **SEO / content** | Useful long-form, manual publish, founder-approved. | Scaled content abuse. Mass-generated articles. |
| **Partnerships** | Warm intro + referral. Founder approves each. | Cold partnership pitch. Buying placements. |

---

## Conversion funnel targets (week 1)

| Stage | Target |
|---|---|
| Prospects messaged | 10 |
| Replies received | ≥ 3 |
| Diagnostics delivered | ≥ 2 |
| Pilots offered | ≥ 1 |
| Pilots paid (or written commitment) | ≥ 1 |

If actual ≪ target by Day 7, **don't** double the volume. Diagnose:
- Was the message wrong?
- Was the wedge wrong?
- Was the timing wrong?

Iterate on QUALITY before VOLUME.

---

## Marketing claims allowed

| ✅ Say | ❌ Don't say |
|---|---|
| "نلتزم بالعمل والـ Proof Pack" | "نضمن المبيعات" |
| "Saudi B2B revenue execution" | "Guaranteed leads" |
| "Manual approval before any send" | "Fully automated" |
| "PDPL-compliant by design" | "Send to anyone" |
| "نسلّم 10 فرص في 7 أيّام" | "آلاف الفرص" |
| "No cold WhatsApp, no scraping" | "Best-in-class outreach" (vague) |

---

## What to do AFTER first Pilot delivers

- [ ] Update `docs/FIRST_3_CUSTOMER_LOOP_BOARD.md` slot status
- [ ] Add the customer's anonymized story to the GTM funnel doc (this doc)
- [ ] Send a thank-you note (manual, no template)
- [ ] Schedule Executive Growth OS upsell call for week 3

---

## Post-Pilot pricing message

Once the first Proof Pack lands:

> "كان Pilot 499 ريال السعر التعريفيّ. اعتباراً من العميل #6،
> سيرتفع إلى 990 ريال. لو تعرف شركات تستفيد من Pilot 499، أرسلني
> الآن — السعر مازال قائماً لـ 4 عملاء فقط."

This isn't a discount play; it's authentic urgency tied to the
Decision Pack §S1 trigger.

---

— GTM Execution Plan v6 v1.0 · 2026-05-05 · Dealix
