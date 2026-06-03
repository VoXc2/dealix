# Dealix Turnkey Package — Master Service Spec

**Version:** v1.0 · May 2026
**Status:** Closed scope · Production-ready · Buy-today-deliver-tomorrow
**Sales surface:** `dealix.me/launchpad.html`
**Customer kickoff:** `dealix.me/pilot-day-0.html`
**Active customer dashboard:** `dealix.me/decisions.html`

---

## 1. The closed package (no negotiation, no scope creep)

Dealix sells exactly **two SKUs** — nothing else. No customizations. No "let me ask the team." No discount negotiations. The package is closed by design so:

- **Customer** knows exactly what they get
- **Founder** knows exactly what to deliver
- **System** knows exactly which endpoints fire when

### SKU 1: Sector Sprint
- **Price:** 5,000 SAR (one-time)
- **Calendar:** 14 days
- **Refund:** 100% within 14 days, no questions
- **Outcome:** 5 deliverable PDFs (Pipeline Audit · Lead Quality Report · Broker Performance Brief · KSA Sector Benchmark · 30-Day Action Plan)
- **Targets:** First-time customers + customers needing baseline data before committing to Partner

### SKU 2: Managed AI Partner
- **Price:** 12,000 SAR/month
- **Commitment:** 4-month minimum (48,000 SAR)
- **KPI guarantee:** chosen KPI lifts ≥20% in 4 months OR founder works free until it does
- **Outcome:** Daily Decisions inbox + weekly Pipeline Audit refresh + monthly Exec Brief + 1 founder call/week + WhatsApp + quarterly Proof Pack + Sector Benchmark Data access
- **Targets:** Customers who finished a Sprint successfully (≥80% conversion rate)

### Sector Domination (mentioned, not sold yet)
- Custom · referral only · revenue share
- **Trigger:** ≥5 paid customers in same sector
- Not in this Master Spec — separate playbook lands when triggered

---

## 2. The 7 immutable contractual commitments (every customer)

Every Sprint and Partner customer gets these 7 things — no exceptions, no sliders:

1. **5 AI Agents productized** — Sales · Growth · Support · Ops · Executive (each = real live endpoint)
2. **8 hard gates immutable** — NO_LIVE_SEND · NO_LIVE_CHARGE · NO_COLD_WHATSAPP · NO_LINKEDIN_AUTO · NO_SCRAPING · NO_FAKE_PROOF · NO_FAKE_REVENUE · NO_UNAPPROVED_TESTIMONIAL
3. **Saudi-Arabic UX** — dialect-correct, prayer-time aware, KSA quiet-hours (21:00–08:00), 72h active conversation window
4. **PDPL-safe by-design** — SDAIA-aligned, per-channel × per-purpose consent table, default-deny, audit trail with correlation_id
5. **Founder access** — direct WhatsApp with Sami; 30-min response in business hours, 4h after
6. **Compounding Proof Pack** — every week adds claim+evidence pairs (60+ pages by month 6)
7. **Sector Benchmark Data** (Partner only) — anonymized peer comparison Western SaaS can't reproduce

---

## 3. Sprint delivery contract (14-day day-by-day)

This is the **founder's exact SOP** for every Sprint customer. Same plays every time. Predictable.

| Day | Deliverable | Endpoint(s) | Founder action (~time) |
|---|---|---|---|
| **D0** (payment day) | WhatsApp voice note + Day-0 link + KPI commit | `/pilot-day-0.html` | 30 min: voice note + Calendly + agreement |
| **D1-2** | Discovery call + Sales Agent qualifies 3 prospects from customer's CRM | `/api/v1/sales-os/qualify` | 90 min: 30-min call + 1h reviewing 3 outputs |
| **D3-4** | Growth Agent: 3 warm-route message drafts for the 3 prospects | `/api/v1/growth-beast/warm-route/draft` | 60 min: review + adjust drafts; customer approves on `/decisions.html` |
| **D5-6** | Support Agent: build first FAQ + escalation policy (12-category classifier) | `/api/v1/support-os/classify` + `/draft-response` | 90 min: 1 customer-data review + 30 min QA |
| **D7-8** | Ops Agent: 7-step delivery checklist + daily ops report template | `/api/v1/full-ops/today` + `/daily-command-center` | 90 min: tailor to customer's specific service line |
| **D9** | Executive Agent: weekly executive brief (top-3 decisions + revenue truth + finance brief) | `/api/v1/role-command-v125/today/ceo` + `/founder/beast-command-center` + `/revops/finance-brief` | 60 min: review + customize |
| **D10-11** | **Pipeline Audit PDF** (~15 pages) — every active deal scored | (composed from above endpoints) | 3h PDF assembly + customer review |
| **D11-12** | **KSA Sector Benchmark** (~1 page) + **30-Day Action Plan** (~5 pages) | (manual research + sector data) | 3h: benchmark research + plan customization |
| **D13** | Proof Pack drafted | `/api/v1/proof-to-market/snippet` | 90 min: claim+evidence pairs |
| **D14** | Final 30-min review call → upsell OR refund | (manual) | 60 min: call + decision |

**Total founder time per Sprint:** ~18-20 hours (2.5 days of work spread over 14 days)
**Total customer time:** ~10 minutes/day (15 review checkboxes total)

---

## 4. The 5 deliverable PDFs (exact contents)

### Deliverable 1: Pipeline Audit (~15 pages)

For each active deal in customer's CRM/Excel/WhatsApp:

- Lead source + first-touch date
- BANT score (Budget · Authority · Need · Timeline) — 0-100 with sub-scores
- Time-to-close estimate
- Recommended next action (founder-approved)
- Broker assignment recommendation (Partner only)
- Risk flags (stalled, overdue, broker-conflict, opt-out)

**Customer outcome:** Their first AI-augmented sales pipeline view ever. Worth more than 5,000 SAR alone.

### Deliverable 2: Lead Quality Report (~10 pages)

Last 90 days of incoming leads, scored by sector benchmark:

- Lead-source breakdown (which channels actually convert)
- KSA-resident vs GCC-investor breakdown
- Family-buyer vs solo-decision breakdown
- Financing vs cash breakdown
- Wasted-budget identification (sources that brought 0 closed deals)
- Top-3 source recommendations for next 90 days

**Customer outcome:** Stops wasting marketing spend on dead channels.

### Deliverable 3: Broker / Team Performance Brief (~8 pages)

Anonymized scoring of customer's broker team:

- Conversion rate per broker
- Average deal size per broker
- Time-to-close per broker
- Customer-satisfaction signals from WhatsApp tone analysis
- Skill gaps + training recommendations
- Top performer identification (replicate behavior)

**Customer outcome:** Pure gold for the office owner — they've never had quantified broker performance before.

### Deliverable 4: KSA Sector Benchmark (~1 page)

Customer's office vs anonymized peers:

- Lead-to-viewing conversion rate (their X% vs Riyadh Y%)
- Cycle time (days from inquiry to close)
- Broker productivity (deals/broker/month)
- Identification of top quartile + what they do differently
- Sector trend (improving/declining vs last quarter)

**Customer outcome:** The 1-page document they show their board.

### Deliverable 5: 30-Day Action Plan (~5 pages)

Concrete prioritized actions for next 30 days:

- 8-12 specific actions, ordered by impact-effort
- Owner assigned to each (broker name / role)
- Weekly checkpoints (4 milestones)
- Success metrics for each action
- Dependencies + blockers

**Customer outcome:** Week-by-week execution roadmap, not generic advice.

---

## 5. Partner monthly delivery contract

For customers who upgrade to 12,000 SAR/month Partner after Sprint:

### Daily (founder ~30 min/day per active customer)
- Daily Decisions inbox auto-populated on `/decisions.html`
- Customer reviews + clicks ✓/✗ on each pending action
- Founder approves/edits drafts before customer-facing send
- WhatsApp voice note from founder if anything needs urgent attention

### Weekly (founder ~3 hours/week per customer)
- Refresh Pipeline Audit from new deals
- Update lead-quality scoring with new leads
- Review broker performance trends
- Friday 30-min check-in call
- Adjust 30-Day Action Plan based on what worked

### Monthly (founder ~6 hours/month per customer)
- **Monthly Executive Brief** — for customer's board
  - Revenue truth (cash collected vs commitments vs forecast)
  - Top-3 decisions for the next month
  - Pipeline health metrics
  - Risk flags
  - Recommended capital allocation
- KPI commitment progress check (against 20% lift goal)
- Sector benchmark refresh (if sector has 3+ Partner customers)

### Quarterly (founder ~10 hours/quarter per customer)
- **Quarterly Proof Pack** — evidence-backed performance vs baseline
  - Every claim has an evidence link (CRM, calendar, WhatsApp, email)
  - Customer-approved testimonial section
  - Public-publish option (signed_publish_permission gate)
- Sector Domination eligibility check (if customer is in sector with 5+ active partners)
- Partner renewal call (month 4)

---

## 6. The 8 hard gates — what customer NEVER worries about

These are unit-tested invariants. The customer doesn't have to remember them — they're just true.

| Gate | Customer benefit |
|---|---|
| `NO_LIVE_SEND` | Every message gets founder approval; no AI auto-spam from your account |
| `NO_LIVE_CHARGE` | Every payment confirmed manually; no Moyasar surprises |
| `NO_COLD_WHATSAPP` | PDPL-safe; no SAR 5M fine risk |
| `NO_LINKEDIN_AUTOMATION` | LinkedIn account never gets banned |
| `NO_SCRAPING` | No purchased lists, no "we found you online" creepiness |
| `NO_FAKE_PROOF` | Every claim has a verifiable source |
| `NO_FAKE_REVENUE` | Pipeline numbers always honest (draft invoice ≠ revenue) |
| `NO_UNAPPROVED_TESTIMONIAL` | Customer testimonials never published without signed permission |

---

## 7. Refund SOP

### Sprint refund
- **Trigger:** Customer says "I want a refund" any time within 14 days from Day 0
- **No questions asked** (founder takes feedback informally for improvement, but doesn't gatekeep)
- **Bank transfer:** 3-5 business days
- **Moyasar:** 2 business days
- **Communication:** Founder personally calls customer within 30 minutes of refund request, expresses appreciation for trying, asks 1 question: "what would have made it work?"
- **Outcome:** Polished refund + insight for next Sprint

### Partner pro-rata refund
- **Trigger:** KPI commitment not met by month 4 + customer wants out
- **Pro-rata:** unused months refunded
- **Alternative:** founder works free until KPI met (most customers prefer this)
- **No question asked** at month 5+ if customer doesn't renew

### What founder NEVER does
- Argue with refund request
- Add fees / penalties
- Make customer feel bad
- Use legal threats

---

## 8. Customer onboarding kit (Day 0 — immediate after payment)

Everything below auto-fires within 30 minutes of payment evidence verified by founder:

### A. WhatsApp voice note from Sami (3-minute)
Saudi-dialect greeting, names KPI from intake form, says "بكره الصبح ٩ نبدأ بالـ Discovery call"

### B. Day-0 page link
`dealix.me/pilot-day-0.html?customer=<handle>` — pre-filled with customer's intake data, shows full 14-day plan, Calendly link for tomorrow's Discovery

### C. Customer Portal access
Subscriber-tier access token shared via WhatsApp. Customer bookmarks `dealix.me/decisions.html?access=<token>`.

### D. Service Agreement signed PDF
1-page agreement (5K SAR Sprint OR 12K/month Partner), signed by Sami, sent via email. Customer counter-signs and emails back.

### E. Calendar invite for Day 1 Discovery call
30-min, Saudi business-hours, voice-only (Saudi preference) or video (customer choice).

### F. Pre-filled invoice in `/pilot-tracker.html`
Founder logs the new pilot manually: company name, sector, contact, payment status. Day-by-day grid initialized.

---

## 9. The pricing-pin guarantee (founding partners)

For the **first 3 paid pilots** (Wave 2):

- Sprint: 5,000 SAR forever (post-Wave-2 raise to 7,500 SAR)
- Partner: 12,000 SAR/month forever (post-Wave-2 raise to 15,000 SAR)
- Sector Domination access if/when customer's sector hits 5 customers

This is the **founding-partner price-lock**. Communicated explicitly to first 3 customers as a closing tool. Honored in writing in the Service Agreement.

---

## 10. Common objections + closing scripts

### "5,000 SAR is too much"
> "أبشر. التشخيص المجّاني ٢٤ ساعة أوّلاً — مجّاناً تماماً. لو ما عجبك التشخيص، ما تدفع شيء. لو عجبك، الـ Sprint هو ١٠٪ من تكلفة موظّف مبيعات شهري واحد، ويسلّم خلال أسبوعين بدل ٣ شهور تدريب."

### "نريد ندرسها"
> "أكيد. لكن سؤال: ما هي البيانات اللي تنقصك للقرار؟ خلّني أرسلك التشخيص المجّاني الآن — لو هذا اللي تحتاجه للقرار، فهو سبب وجود الـ Diagnostic. ٢٤ ساعة وعندك."

### "هل أنت متأكّد ما يكون scam؟"
> "افهم القلق. عندي ٣ أشياء أعطيك: (١) التشخيص المجّاني قبل الدفع — تختبرني صفر مخاطرة. (٢) Sprint استرجاع كامل ١٠٠٪ خلال ١٤ يوم. (٣) رقمي شخصي على WhatsApp، مو شركة بـ ١٠٬٠٠٠ موظّف. لو أيّ شيء يحدث، تتّصل عليّ مباشرة."

### "نحتاج CRM، مو AI agents"
> "Dealix مو CRM — نقعد فوق CRMك (HubSpot / Salesforce / Excel — ما يهمّ). Dealix يصنع القرارات اللي الـ CRM ما يقدر يصنعها: مَن يستحقّ المتابعة الأوّل؟ ما السكربت الأنسب؟ ما الـ broker الأفضل لهذا العميل؟ ٤٨ ساعة Pipeline Audit يثبت لك."

### "Salesforce أرخص شهرياً"
> "صحيح من ناحية license. لكن: (١) Salesforce تنفيذ ٨-٢٦ أسبوع، Dealix ١٤ يوم. (٢) Salesforce admin team تكلّف ٢٥٬٠٠٠ ريال شهري إضافي. (٣) Salesforce ما يفهم 'إن شاء الله' tone أو KSA quiet-hours. (٤) Salesforce بدون ضمان نتيجة. Dealix يعطي ضمان ٢٠٪ KPI lift أو نمدّد مجّاناً."

### "بنشتري Sprint بس مو Partner"
> "أبشر — ٨٠٪ من عملاء الـ Sprint يرقّوا لـ Partner بعد ١٤ يوم. لكن Sprint وحده مفيد جدّاً: عندك Pipeline Audit + Sector Benchmark + 30-Day Plan جاهزة للتنفيذ مع فريقك. لو بعد ١٤ يوم قلت 'هذا كافٍ'، بكل احترام، ما تدفع شيء إضافي."

---

## 11. Customer-success metrics (track every customer)

### Sprint KPIs
- Days from payment to first deliverable (target: ≤ 3)
- Days from payment to Pipeline Audit (target: ≤ 11)
- Customer NPS at Day 14 (target: ≥ 8/10)
- Sprint → Partner conversion rate (target: ≥ 80%)
- Refund rate (target: ≤ 10%)

### Partner KPIs (per customer per month)
- Daily Decisions response rate (target: ≥ 80%)
- Weekly call attendance (target: 100%)
- Monthly Brief read-rate (target: 100%)
- Quarterly Proof Pack delivered on time (target: 100%)
- KPI commitment progress (target: ≥ 5%/month → 20% over 4 months)
- Renewal at month 5 (target: ≥ 60%)

---

## 12. The 4 unbeatable moats (recap from `/launchpad.html`)

1. **Saudi-Arabic-first execution** — dialect mastery + prayer-time + family-decision + "إن شاء الله" tone
2. **8 hard gates immutable in code** — PDPL-safe, unit-tested, not user-toggleable
3. **Compounding Proof Pack** — every customer accumulates 60+ pages of evidence over 6 months
4. **Founder-led trust** — direct WhatsApp with founder; not scalable past ~25 customers, but for the first 25 it's the moat

---

## 13. What's NOT in the package (deliberately excluded)

- ❌ Salesforce / HubSpot / Zoho integrations (until customer #2 needs it)
- ❌ Custom CRM building (use existing CRM, Dealix sits on top)
- ❌ Lead-purchase services (NO_SCRAPING gate)
- ❌ Cold outreach campaigns (NO_COLD_WHATSAPP gate)
- ❌ Marketing automation (we draft, customer sends manually)
- ❌ AI chatbot for customer's website (not in scope)
- ❌ Multilingual (Arabic + English are it; no French/Urdu/etc.)
- ❌ Multi-tenant team accounts (founder + 1 user only until customer #2)
- ❌ White-label (the brand IS the moat — customers want Dealix specifically)

If a prospective customer asks for any of the above, the answer is: "نحن لا نقدم هذا في الباكج المغلق. لكن خلّنا نتحدّث عمّا تريد تنجزه — ربّما الـ Sprint يحلّ مشكلتك بطريقة مختلفة."

---

## 14. Pricing-pin price card (for share/print)

```
═══════════════════════════════════════════════════════
        Dealix Turnkey Package · Founding Partner
═══════════════════════════════════════════════════════

⚡ SECTOR SPRINT             5,000 SAR
   14 days · 100% refund · 5 PDF deliverables
   founding-partner price-lock for life

🎯 MANAGED AI PARTNER       12,000 SAR/month
   4-month minimum (48,000 SAR) · 20% KPI commitment
   founding-partner price-lock for life

📜 SECTOR DOMINATION         Custom · referral only
   Triggered after 5 paid customers in same sector

═══════════════════════════════════════════════════════
   Buy at dealix.me/launchpad.html
   Sami's WhatsApp: [redacted in public — given on call]
   Refund: 100% (Sprint) / pro-rata (Partner)
═══════════════════════════════════════════════════════
```

---

## 15. Founder daily reminder

The package is **closed by design**. The temptation to "make an exception" / "discount once" / "throw in extra" — resist it. Every exception:

- Erodes the price floor
- Confuses the next customer
- Makes the package un-replicable
- Undermines the founding-partner price-lock promise

Stick to the SKU. The customer wins by knowing exactly what they get. The founder wins by knowing exactly what to deliver. The system wins by being predictable.

---

## One-line CEO summary

> _"Two SKUs. Five-thousand SAR or twelve-thousand-a-month. Fourteen-day or four-month commitment. 100% refund or 20% KPI commitment. Saudi-Arabic-first, PDPL-safe, founder-led. The closed package — buy today, deliver tomorrow."_

**Sales surface:** [dealix.me/launchpad.html](https://dealix.me/launchpad.html)
