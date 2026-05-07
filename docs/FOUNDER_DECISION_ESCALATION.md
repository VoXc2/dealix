# Founder Decision Escalation Matrix — Dealix

**Status:** DRAFT — founder names P0 backup person before Day 7
**Owner:** Sami (founder)
**Last updated:** 2026-05-07
**Companion docs:** `docs/V14_FOUNDER_DAILY_OPS.md` · `docs/HIRING_CSM_FIRST.md` · `docs/REFUND_SOP.md` · Plan §23.5.4

> **Why this doc exists:** Wave 7 §23.5.4 — solo founder is single-point-of-failure. As load grows from 3 to 6 customers (Day 31), founder will hit decision bottleneck without an escalation matrix. This doc says explicitly: what only Sami decides · what gets delegated when CSM joins · who covers P0 if Sami is unreachable.

---

## 1. Decision categories — who owns what

### Category A — Founder ALWAYS decides (never delegates)

| Decision | Why founder-only |
|---|---|
| Take a paid customer | Trust + ICP fit are personal-judgment calls |
| Refund > 5,000 SAR | Money out the door = founder accountability |
| Sign legal documents (DPA, contracts) | Legal liability |
| Pricing changes (Sprint or Partner SKU) | Strategic positioning |
| Hire / fire team member | Culture + comp |
| Brand voice / public statement | Reputation risk |
| Scope changes that contradict 8 hard gates | Constitutional |
| Wave 8 path decision (Deepen / Expand / Scale) | Article 13 |
| Investor / angel-round conversations | Cap-table |
| Press / media on-record statements | Public reputation |

### Category B — Delegated to CSM when hired (Wave 8+)

| Decision | Delegated when |
|---|---|
| Schedule customer Pipeline Audit | After CSM completes 30-day shadow |
| Draft weekly proof pack | After CSM month 1 |
| Send NPS surveys + categorize responses | After CSM month 1 |
| Approve/reject draft messages on `/decisions.html` (low-risk only) | After CSM month 2 |
| Customer day-to-day support replies | After CSM month 2 |
| Book follow-up demos | After CSM month 3 |
| Onboarding kit delivery | After CSM month 1 |

CSM does NOT make Category A decisions ever.

### Category C — Automated by code (no human decides daily)

| Decision | Enforcement |
|---|---|
| Block cold WhatsApp send | `whatsapp_safe_send.py` 6 gates |
| Block live charge in test env | `revops/payment_confirmation.py` invariant |
| Block scraping outbound | `_HARD_GATES.no_scraping` in every router |
| Refuse fake proof publishing | `proof_pack.public_allowed=False` until consent |
| Refuse customer #4 in Days 1-30 | Founder daily ops cap (manual gate) |

These gates are immutable. Founder cannot disable them via settings — code change required (which goes through normal Article 4 review).

---

## 2. Decision SLAs (response time targets)

| Trigger | Founder response SLA | After CSM hired |
|---|---|---|
| Customer P0 (service down, money lost, payment failed) | 30 min business hours · 4h after | 30 min (CSM+founder both) |
| Customer P1 (proof event missed, NPS detractor) | 4h business · same day | 4h CSM, escalate if needed |
| Customer P2 (feature request, generic question) | 24h | CSM owns within 8h |
| Sales prospect reply | 30 min business hours · 4h after | Founder (sales is Cat A) |
| Refund request | 4h acknowledge · 24h decide · 72h execute | Founder (Cat A) |
| Lawyer back with question | 24h | Founder (Cat A) |
| Vendor critical alert (Railway, Moyasar down) | 1h business · 4h after | Founder (Cat A) |

**Hard cap:** if founder cannot meet SLA for 48h running → declare P0-Backup mode (see §3).

---

## 3. P0-Backup person (the irreplaceable role)

**Why this matters:** if founder gets sick, has emergency, travels with no signal → who covers customer P0 alerts so trust isn't broken?

**Who fits the role:**

- ✅ Trusted family member or close friend with phone access
- ✅ Co-founder if any (Sami currently solo)
- ✅ Fractional ops contractor (e.g., trusted ex-colleague hired on retainer 500 SAR/mo to cover 5-10 days/year)

**Who does NOT fit:**

- ❌ Customer who happens to like Dealix (conflict of interest)
- ❌ Lawyer (not their job)
- ❌ Random VA service (data sensitivity)

### P0-Backup contract — fill in:

| Field | Value |
|---|---|
| Person name | _TBD_ |
| Relationship to founder | _TBD_ |
| Phone (24h reachable) | _TBD_ |
| WhatsApp | _TBD_ |
| Email | _TBD_ |
| Retainer if external | _TBD_ |
| What they're authorized to do | (a) acknowledge customer message within 4h, (b) escalate to founder via emergency channel (call), (c) issue same-day refund up to 5,000 SAR if customer is panicking AND founder unreachable for 24h+, (d) post status update on dealix.me/status.html |
| What they CANNOT do | sign contracts · hire/fire · public statements · disable hard gates · move money outside refund authority · share customer PII |
| Activation trigger | founder unreachable for 24h+ during business hours OR pre-planned travel/leave |

**Documentation:** create signed (handwritten OK) memo with this table. Store in shared family drive + email to backup person + cc lawyer.

---

## 4. Boundary rules — what to say NO to

These are the standard "no" reasons. Practice them. Use Saudi-Arabic delivery.

| Request | Polite no |
|---|---|
| "Add a 4th customer in Days 1-30" | "أقدر آخذك يوم ٣١ — السقف ٣ في الـ ٣٠ الأوّل لحماية جودة التسليم. أحجز لك الموعد الآن؟" |
| "We want WhatsApp automation for cold outreach" | "هذا ضدّ سياسة الكود + PDPL. لكن نقدر نسوّي drafts بضغطة واحدة من جوّالك. مناسب؟" |
| "Can you guarantee +X% revenue?" | "ما نضمن نتائج لأن السوق + بيانات شركتك متغيّرات. اللي نلتزم به: إن ما حقّقنا KPI خلال ٩٠ يوم، أشتغل مجّاناً حتى يتحقّق." |
| "Lower the price for us" | "السعر مثبّت للـ ٣ founding partners. هل تبي تكون واحد منهم؟" |
| "Build us a custom feature" | "نسجّلها في `V14_CUSTOMER_SIGNAL_SYNTHESIS.md`. لو ٢ عميل ثانيين طلبوها، نبنيها في Wave 8." |
| "Can we white-label Dealix?" | "حالياً لا. أتحدث عنها بعد ٢٠ paid customer." |
| "Please reply at 11pm" | "أرتاح بعد المغرب لأن الجودة تنخفض. أرد عليك أوّل شيء بكره." |

---

## 5. Founder-burnout caps (Article 11 protection)

From `docs/V14_FOUNDER_DAILY_OPS.md` §1, hard limits:

- Days 1-30: max 3 active customers (40h/customer cap = 120h/month redline)
- Days 31-90: max 6 active customers
- After CSM hired: max 10 customers, with CSM owning ~50% of touchpoints
- Working hours: 08:00 - 18:00 Asia/Riyadh, no customer work after Maghrib unless emergency
- Friday: review-only, NO new customer demos or onboarding
- 1 day off per 7 days minimum

**Trigger conditions to enforce:**

- 4th customer asks during Days 1-30 → founder says "Day 31" (per §4)
- Working past 18:00 three days in a row → next day is half-day
- Skipping Friday review 2 weeks in a row → STOP ALL outreach for 1 week, recover

These are not "preferences" — they are product-survival caps.

---

## 6. Information channels (in priority order)

When founder is making a decision, check sources in this order:

1. **Operating Constitution** (`docs/DEALIX_OPERATING_CONSTITUTION.md`) — Articles 1-17 for principle-level questions
2. **8 hard gates** (`auto_client_acquisition/`) — for "is X allowed?"
3. **Customer signal synthesis** (`docs/V14_CUSTOMER_SIGNAL_SYNTHESIS.md`) — for product priority
4. **Wave 7 plan** (`/root/.claude/plans/fluttering-munching-harp.md` §23) — for calendar/sequencing
5. **Lawyer** (when legal angle) — for contract / compliance
6. **Accountant** (when financial) — for tax / cash
7. **Customer (the real human)** — for ICP / pricing-fit
8. **Trusted advisor / mentor** — for "am I crazy?" check
9. **CTO (Claude)** — for code/architecture/verification questions
10. **Internet / benchmarks** — for comparative pricing only

NEVER skip 1-3 to get to 9 fast. Order matters.

---

## 7. Friday review — escalation health check

In addition to `SALES_OPS_SOP.md` §10 weekly review, audit:

1. Did I respond to any customer P0 within SLA this week?
2. Did I work past 18:00 more than 2 days?
3. Did I take 1 full day off?
4. Did I delegate ANY Cat B item that the CSM (when hired) could own?
5. Did I cross any boundary in §4 (said "yes" when I should have said "no")?

If 2+ answers are concerning → discuss with mentor / advisor / spouse before Monday.

---

## 8. Hard rules

- ❌ Never delegate Category A decisions
- ❌ Never break the customer-cap during Days 1-30 (3) or 31-90 (6)
- ❌ Never work past Maghrib for 3+ consecutive days
- ❌ Never give P0-Backup unrestricted contract / financial authority
- ❌ Never let a customer P0 go beyond SLA without acknowledging
- ✅ Always document Cat A decisions same day in Friday review
- ✅ Always activate P0-Backup before pre-planned travel
- ✅ Always pre-write the "polite no" responses (§4) — improvising under pressure leaks boundary
- ✅ Always check sources in priority order (§6)
