# Customer Success SOP — Dealix

**Status:** DRAFT — to be calibrated after first 3 customers
**Owner:** Sami (founder, owns CS through Wave 7) → CSM (Wave 8+)
**Last updated:** 2026-05-07
**Companion docs:** `docs/sales-kit/dealix_customer_onboarding.md` · `docs/V14_TURNKEY_PACKAGE.md` · `docs/WAVE6_PILOT_TO_MONTHLY_UPSELL_AR_EN.md` · `auto_client_acquisition/crm_v10/customer_health.py` · Plan §23.5.3

> **Why this doc exists:** A 14-day Sprint that ends with a "thanks bye" loses the Partner upsell. A Sprint that ends with a structured Day-7 review + NPS + clear path forward converts at 80%. The difference = this SOP.

---

## 1. The customer journey (post-payment_confirmed)

```
Day 0      Sprint kickoff call (30 min)
Day 1-7    Daily voice notes + decisions queue
Day 7      Mid-Sprint review (15 min)  ← upsell signal check
Day 14     Final review + Proof Pack delivery + upsell pitch
Day 14     NPS-1 deployed (Sprint NPS)
─────────────────────────────────────────────────────────────
[IF Partner signed]
Month 1    Weekly Pipeline Audit + 1 founder call/week
Month 1    NPS-2 deployed end of month
Month 2    Mid-commitment KPI review (commitment check)
Month 3    NPS-3 deployed
Month 3    Renewal check-in (4-month commitment ends)
Month 4    Renewal call OR honest exit conversation
```

---

## 2. Day 14 close-out — the most important meeting

This is where Sprint becomes Partner. Use `docs/WAVE6_PILOT_TO_MONTHLY_UPSELL_AR_EN.md` Section 1-3 verbatim.

**30-minute structure:**

| Time | What |
|---|---|
| 0:00-5:00 | Walk through Proof Pack (real events only, no fake metrics) |
| 5:00-15:00 | "وش طلع لك من الـ 7 أيّام؟" — listen, take notes |
| 15:00-20:00 | Section 2A-2E (continue / price / proof gap / guarantees / WhatsApp automation) |
| 20:00-25:00 | Section 3 close OR park OR refund |
| 25:00-30:00 | Either: Service Agreement + bank link · OR: 30-day follow-up booked · OR: refund initiated |

**Commit to one of three outcomes by end of meeting:**

1. **Pilot → Partner signed** → run `dealix_demo_outcome.py --outcome paid` + start contract
2. **Pilot → 30-day follow-up** → run `dealix_demo_outcome.py --outcome follow_up`
3. **Pilot → refund** → run `dealix_payment_confirmation_stub.py --action refund` per `REFUND_SOP.md`

NO middle ground. No "let me think about it for a month" without a calendar entry.

---

## 3. NPS deployment — bilingual, single-question

Send via WhatsApp (manual, with founder signature).

### NPS-1 (Sprint Day 14, after close-out call)

> «شاكر لك على ٧ أيّام Sprint [الاسم]. سؤال واحد بس:
>
> على مقياس من ٠ إلى ١٠، كم احتمال توصي Dealix لصاحب شركة B2B سعودي ثاني؟
>
> رد عليّ بالرقم فقط — وإن أحببت تكتب جملة سبب، أكون شاكر لك.»

### NPS-2 (Partner end of month 1) and NPS-3 (Partner end of month 3)

> «انقضى شهر / ٣ شهور من Managed Revenue Ops [الاسم]. سؤال واحد:
>
> ٠–١٠، كم احتمال توصي Dealix؟»

**Categorize responses:**

| Score | Category | Action |
|---|---|---|
| 9-10 | Promoter | Ask for testimonial (signed_publish_permission) within 7 days |
| 7-8 | Passive | Ask: "وش يخلّيك تعطي ١٠؟" — note for product backlog |
| 0-6 | Detractor | Schedule 30-min recovery call within 48 hours, founder leads |

**Logging:** append to `docs/wave6/live/nps_log.jsonl` (gitignored), schema:

```json
{
  "customer_handle": "...",
  "nps_round": "sprint_d14 | partner_m1 | partner_m3",
  "score": 8,
  "verbatim": "...",
  "responded_at": "ISO date",
  "follow_up_taken": "..."
}
```

---

## 4. Renewal triggers (Partner)

### Month 3 (1 month before commitment ends)

Trigger: **30 days before `commitment_end_at` date in Tab 1 of Finance Dashboard**

Action by founder:
1. Send WhatsApp: "نحن في شهر ٣ من ٤. هل تبي تستمرّ لأربعة شهور ثانية؟"
2. Pull Proof Pack (cumulative all proof events for this customer)
3. Run KPI commitment check (was +20% lift achieved? evidence in `proof_ledger`)

Three paths from this conversation:

| Customer answer | Action |
|---|---|
| "نعم، أكمل" | Send next 4-month invoice (no price increase for founding partners) |
| "لا، أبي وقفة" | Schedule honest exit call. NO churn shame. Pro-rata last-month if KPI unmet. |
| "لا أدري بعد" | Book Day -1 call (1 day before commitment ends). Don't let it auto-lapse. |

### Month 4 (commitment end day)

If no answer by Day -1: PAUSE billing (don't invoice month 5). Send: «انتهى التزام الـ ٤ شهور. أوقفت الفوترة لشهر ٥ — احكي معي قبل ما أقفل.» Wait 7 days. If still silent → archive.

---

## 5. Churn signals — when customer is silent

Use `auto_client_acquisition/crm_v10/customer_health.py` health score weekly.

Yellow flags (act in 24h):
- No Daily Decisions opened in 7+ days
- No WhatsApp reply to founder voice note in 3+ days
- Same support category logged 2+ weeks in a row (root cause not fixed)

Red flags (escalate same day):
- 14+ days no engagement
- Customer mentioned "اتصال مع منافس" or "ندرس بدائل"
- KPI tracking fell ≥30% from baseline

**Recovery playbook:**

| Flag | Action | Channel |
|---|---|---|
| Yellow | Personal voice note + ask one direct question | WhatsApp |
| Red | Founder calls (voice, not text) within 4h | Phone/Zoom |

If recovery call → customer wants out → run §4 honest exit + refund per `REFUND_SOP.md`.

---

## 6. Expansion signals — when customer wants more

Track in weekly Friday review:

- Customer asked for feature outside current Sprint → log to `docs/V14_CUSTOMER_SIGNAL_SYNTHESIS.md`
- Customer asked to add a teammate → trigger ECC tier upsell (12K → 15K SAR/mo) ONLY after Wave 8
- Customer asked for sector benchmark → trigger custom add-on (defer until 5+ same-sector customers)
- Customer praised Dealix to peer → ask for warm-intro reciprocal

**Hard rule:** never sell expansion before the original commitment is met. Trust > short-term revenue.

---

## 7. Weekly customer touch checklist (per active customer)

| Day | Touch | Channel | Time |
|---|---|---|---|
| Sun | Pipeline Audit drafted | dashboard async | 30 min founder time |
| Tue | Mid-week voice note | WhatsApp | 2 min |
| Thu | Daily Decisions queue review | `/decisions.html` | 5 min |
| Fri | Weekly summary (1 line + 1 metric) | WhatsApp | 1 min |

Total: ~40 min/customer/week (Partner). Sprint customers get 2x this in their 14 days, then drop to Partner cadence if they convert.

---

## 8. Onboarding kit — Day 0 of each new customer

Use `docs/sales-kit/dealix_customer_onboarding.md` + verify these arrive in customer's inbox:

1. Welcome voice note (founder, 60-90 sec, Saudi-Arabic)
2. Sprint Brief PDF (from `dealix_pilot_brief.py`)
3. Calendly link for Day 7 mid-Sprint review
4. Customer Portal access link (with `?org=&access=` token from `dealix.me/customer-portal.html?org=<handle>&access=<token>`)
5. WhatsApp group / direct chat thread starter
6. Day 1-7 day-by-day plan (from `V14_TURNKEY_PACKAGE.md` §3)

---

## 9. Hard rules

- ❌ Never auto-renew without an explicit "yes" within commitment_end - 7 days
- ❌ Never deploy NPS more than 3× per customer per 6 months
- ❌ Never use NPS verbatim publicly without signed_publish_permission
- ❌ Never ghost a churning customer — always call once before archiving
- ❌ Never expand a customer who hasn't met first KPI commitment
- ✅ Always log NPS responses same day
- ✅ Always run health-score check weekly
- ✅ Always escalate red flag to founder voice call within 4h
- ✅ Always recover-call before issuing churn refund

---

## 10. KPI targets for Wave 7 (90 days)

| Metric | Target | Source |
|---|---|---|
| Sprint→Partner conversion | ≥80% | NPS-1 promoter rate × close-rate |
| First-cohort NPS (Sprint Day 14) | ≥40 | NPS-1 average |
| Partner NPS (Month 3) | ≥50 | NPS-3 average |
| Churn at month 4 commitment-end | ≤20% | renewal rate ≥80% |
| Days-to-NPS-response | ≤2 | WhatsApp same-day reply rate |

If any target falls below, write 1-line root cause in Friday review. Adjust before scaling.
