# Dealix Revenue Playbook — Final (Phase 13 Wave 5)

**Date:** 2026-05-07
**Audience:** founder + sales
**Goal:** convert warm intros to paid pilots → monthly recurring → agency partner.

---

## Target ICP (3 verticals)

| Vertical | Why this vertical works |
|---|---|
| **B2B agencies** (Saudi marketing/consulting/IT) | They run on leads + proof; they get the value of approval-first immediately; they know how to sell upmarket |
| **B2B services** (legal, accounting, advisory, technical) | Recurring relationships, low-volume / high-value, perfect for Approval Center |
| **Consulting/Training** | Output is documents + sessions; Proof Pack format maps perfectly |

NOT YET in scope (deferred until 3 paid pilots):
- Real-estate agencies (existing diagnostic-real-estate.html stays — but not the primary push)
- E-commerce (volume too high for 1-founder approval-first model)
- Restaurants / hospitality (channel mismatch)

## Offer ladder — Governed Revenue & AI Ops

Canonical source: [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) and [`strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md`](strategic/GOVERNED_REVENUE_AI_OPS_STRATEGY.md).

| # | Offer | Price (SAR) | Trigger condition |
|---|---|---|---|
| 0 | Governed Revenue & AI Ops Risk Score + Sample Proof Pack | 0 | warm intro |
| 1 | 7-Day Governed Revenue & AI Ops Diagnostic | 4,999 / 9,999 / 15,000 / 25,000 (4 tiers) | Risk Score completed |
| 2 | Revenue Intelligence Sprint | 25,000+ (scoped) | diagnostic completed |
| 3 | Governed Ops Retainer | 4,999–35,000/mo | Sprint proven |
| 4 | Adjacent offers — Board Decision Memo · AI Governance / Trust Pack Lite · CRM/Data Readiness for AI | scoped | on request |

---

## First 10 warm intros — outreach process

### Selection criteria
1. Personal-network first (founder already trusted)
2. Saudi-based (Riyadh / Jeddah / Eastern province)
3. Already has at least 5 leads/month (not pre-revenue)
4. Decision-maker is the contact (not employee → escalation chain)

### Outreach script template (Saudi Arabic)

```
السلام عليكم [الاسم]،
كيف الأحوال؟ أتذكر [اللحظة المشتركة].

اشتغل على شيء يهمك: Dealix — طبقة AI تشغّل المبيعات + النمو
+ الدعم لشركتك قبل ما توظف فريق كامل. كل قرار خارجي بموافقتك،
ومحمي بـ ٨ بوّابات أمان (PDPL، لا scraping، لا cold WhatsApp).

عندي ٤ أماكن founding-partner — تشخيص مجّاني ٢ دقيقة:
https://dealix.me/diagnostic.html?ref=warm

إذا حسّيتك مهتم، نسوي مكالمة قصيرة ٣٠ دقيقة هذا الأسبوع.
```

### Follow-up cadence
- Day 0: send the message
- Day 3 (if no reply): "ذكّرني هل وصلتك رسالتي؟"
- Day 7 (if no reply): pause for 4 weeks → try once more

---

## Diagnostic process (≤ 2 hours of founder time)

1. Customer fills `/diagnostic.html` (6 questions, ~2 min)
2. Founder receives lead in `/founder-leads.html` within 30 min
3. Founder calls customer (30-min Calendly link sent)
4. During call: Saudi context + sector specifics + KPI commitment
5. After call: founder writes 1-page diagnostic report (~30 min)
6. Customer receives report + Sprint signup link within 24h

---

## Diagnostic conversion

**Goal:** convert Risk Score completions into a paid 7-Day Governed Revenue & AI Ops Diagnostic (4,999 SAR Starter and up).

### Day 0 onboarding
- Customer signs Service Agreement + PDPL consent (electronic)
- Manual Moyasar invoice or bank transfer (NO_LIVE_CHARGE — founder confirms)
- Founder schedules 7-day kickoff call

### Days 1-7 deliverables
1. Lead Quality Audit (2-page PDF)
2. Pipeline Audit (founder's actual leads scored)
3. 3 Daily Decisions Briefs (sample of `/decisions.html`)
4. 1 sample WhatsApp/email draft (founder approves manually)
5. Initial Proof Pack (3 evidence events minimum)
6. 30-day plan PDF
7. Day 7 review call (decide: continue to Partner OR refund)

### Refund policy
- 100% refund within 14 days of Sprint start, no questions asked
- Bank transfer refund: 3-5 business days

---

## Proof Pack delivery checklist

Every published Proof Pack contains:
- [x] 3+ evidence events (with `evidence_level=customer_confirmed` or `payment_confirmed`)
- [x] Customer-signed `consent_for_publication=True`
- [x] PII redacted (auto via `proof_ledger/evidence_export.py`)
- [x] Bilingual narrative (Arabic primary, English secondary)
- [x] No "guaranteed" / "10x" claims (auto-scrubbed)
- [x] Approval audit trail in `approval_center`
- [x] Saved to `data/case_studies/library.jsonl`

---

## Upsell to the Governed Ops Retainer

**Goal:** convert proven Sprint customers to a monthly Governed Ops Retainer at 4,999–35,000 SAR/month (scoped).

### Conversion script (post-Sprint)
- Run during the Sprint review call
- Lead with the Proof Pack (concrete evidence)
- "بعد ما شفت قيمة الـ Sprint، احتفاظ العمليات المُحوكَمة يخلّيك تشغّل هذا بإيقاع شهري — قرارات مُجهَّزة، موافقات، حزمة إثبات شهرية."
- No guaranteed revenue — evidenced opportunities and a monthly proof pack
- Scoped monthly commitment, unlocked only on a proven Sprint

### Key objections + Saudi-style responses

**"السعر عالي"**
"السعر مقابل founder access مباشر + AI Operating Team جاهز. مقارنة بتوظيف موظف مبيعات (٨٬٠٠٠+ شهري) — أقلّ بكثير وأسرع."

**"ما عندي وقت أديره"**
"ما تديره أنت. تعتمد القرارات اليوميّة على /decisions.html (٣٠ دقيقة في اليوم). كل شي ثاني يشتغل تلقائياً وبموافقتك."

**"شفت AI startups تختفي بعد سنة"**
"Dealix معاه ٢٠٠+ اختبار آلي + ٨ بوّابات أمان مفروضة في الكود + Saudi-PDPL compliance + founder access. كل شي مفتوح وتقدر تطلع بـ Proof Pack كامل لو طلعت."

**"وش تضمن لي؟"**
"ما نضمن إيراد. لكن نضمن KPI lift +٢٠٪ على المؤشّر المتّفق عليه — ولو ما تحقّق، أشتغل مجّاناً حتى يتحقّق. Article 8 — لا ادّعاء بدون دليل."

---

## Agency Partner path

**Trigger:** Saudi/MENA marketing agency with 5+ B2B clients.

### Path
1. Agency sees Dealix Proof Pack from a customer in their network
2. Agency reaches founder with their pipeline
3. Founder pilots Dealix on 1 of agency's clients (free 7-day Sprint)
4. Proof established → Agency signs custom rev-share contract
5. Agency takes over Tier 1-3 customers; Dealix handles Tier 4-5

**Hard rules:**
- Agency cannot bypass `_HARD_GATES`
- Agency customer data isolated (multi-tenant RLS — deferred until customer #2)
- Founder approves agency's first 5 customers personally

---

## Success metrics (per quarter)

| Metric | Target Q1 |
|---|---|
| Warm intros sent | 30 |
| Diagnostics completed | 12 |
| Paid 7-Day Diagnostics | 8 |
| Diagnostic→Sprint→Retainer conversion | 6 |
| Active Governed Ops Retainer customers | 6 (MRR is an estimate, not a guarantee) |
| Published Proof Packs | 4 |
| Customer NPS (P50) | ≥ 7 |
| Full-Ops Score (avg) | ≥ 90 |
| Refund rate | ≤ 15% |

---

## NO-GO statements (what we will refuse to do)

When a customer asks for any of these, refer to Trust Center + decline:
- ❌ "Send WhatsApp blast to my old leads list" → Article 4 NO_COLD_WHATSAPP
- ❌ "Scrape competitor websites" → NO_SCRAPING
- ❌ "Auto-post on LinkedIn" → NO_LINKEDIN_AUTO
- ❌ "Charge customer card automatically" → NO_LIVE_CHARGE without explicit consent
- ❌ "Generate fake testimonials" → NO_FAKE_PROOF
- ❌ "Guarantee revenue" → Article 8 — KPI commitment, not guarantee
- ❌ "Bypass approval for emergency" → approval-first is non-negotiable

---

## Founder's daily rhythm (when running 3+ active Managed customers)

```
06:00  Open /executive-command-center.html?org=...
06:15  Approve top-3 decisions on /decisions.html
06:30  WhatsApp brief: "وش الوضع اليوم؟" (admin-only bot)
07:00  1-on-1 customer call (rotation: 1 per day per active customer)
08:00  Pipeline review (LeadOps Spine + Reliability)
09:00  Founder's other work
17:00  Approve any remaining decisions
17:30  Run scripts/integration_upgrade_verify.sh weekly Friday
```
