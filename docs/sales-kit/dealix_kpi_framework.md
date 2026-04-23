# Dealix — KPI Framework

## 5 Core KPIs + Weekly Scorecard + Monthly/Quarterly Review

**Principle:** "ما تقيسه — لا تستطيع تحسينه." لكن قياس كل شي = قياس لا شي.

---

## 1. The 5 Core KPIs

### KPI 1: Monthly Recurring Revenue (MRR)

**التعريف:** إجمالي الإيراد الشهري المتكرر من كل العملاء المدفوعين.

**الصيغة:**
```
MRR = Σ (كل اشتراك نشط × السعر الشهري)
```

**Targets:**
| Q | MRR Target | New MRR | Churn MRR | Net New |
|---|-----------|---------|-----------|---------|
| Q2 2026 | 10K | 15K | 1K | 14K |
| Q3 2026 | 45K | 45K | 5K | 40K |
| Q4 2026 | 120K | 85K | 10K | 75K |
| Q1 2027 | 250K | 160K | 25K | 135K |

**Dashboard source:** PostHog + internal DB
**Owner:** Sami (Y1), Sales lead (Y2+)
**Review cadence:** يومي (snapshot) + أسبوعي (trend)

---

### KPI 2: Customer Churn Rate (شهري)

**التعريف:** % من العملاء اللي ألغوا خلال الشهر.

**الصيغة:**
```
Churn % = (عملاء ألغوا في الشهر / عملاء في بداية الشهر) × 100
```

**Targets:**
- Y1: < 7% شهري (منظر)
- Y2: < 5%
- Y3: < 3%
- اعتبر كل > 10% emergency → root-cause analysis فوري

**Warning signs:**
- 2 أشهر متتالية > target → investigate
- Churn من عملاء paid < 3 أشهر → onboarding issue
- Churn من عملاء > 12 شهر → product stagnation

**Owner:** Sami / CSM
**Review:** أسبوعي

---

### KPI 3: Net Revenue Retention (NRR)

**التعريف:** الإيراد من cohort العملاء القدامى هل ينمو أو ينقص.

**الصيغة:**
```
NRR % = (MRR from cohort X today - churn + expansion) / (Original MRR from cohort X) × 100
```

**Targets:**
- > 100% = ممتاز (expansion > churn)
- > 110% = world-class
- < 90% = red flag

**كيف نرفعها:**
- Starter → Growth upgrades (target 25% upgrade rate)
- Growth → Scale upgrades
- Feature add-ons (future)
- Renewal discounts للـ annual pay

**Owner:** Sami / Sales
**Review:** شهري

---

### KPI 4: Customer Acquisition Cost (CAC)

**التعريف:** تكلفة اكتساب عميل جديد (كل الجهد × السعر).

**الصيغة:**
```
CAC = (Sales + Marketing + SDR + Tool costs) / New customers acquired
```

**Targets:**
- Blended CAC < 1,500 SAR (Y1)
- CAC by source:
  - Referral: < 2,000 SAR (20% commission)
  - Outbound: < 800 SAR (Sami time)
  - Inbound (organic): < 300 SAR (content investment)

**Ratio to watch:** LTV / CAC > 3× (must) > 5× (target) > 10× (excellent)

**Dealix current:** LTV/CAC = 26× (من financial_model — excellent)

**Owner:** Sami
**Review:** شهري

---

### KPI 5: Net Promoter Score (NPS)

**التعريف:** "من 0-10، كم احتمال تنصح Dealix لصديق؟"

**الصيغة:**
```
NPS = % Promoters (9-10) - % Detractors (0-6)
```

**Targets:**
- Y1: > 40 (good)
- Y2: > 50 (great)
- Y3: > 60 (world-class)

**Measurement:**
- In-app prompt after 30 days of use
- Follow-up quarterly
- Deep-dive with detractors (call, not survey)

**Actions by segment:**
- **Promoters (9-10):** ask for referrals + case study
- **Passives (7-8):** understand "what would make it 10?"
- **Detractors (0-6):** call within 48h, address issue

**Owner:** Sami / CSM
**Review:** ربع سنوي + ad-hoc

---

## 2. Supporting Metrics (الـ 5 الأساسية محمية بـ 15 supporting)

### Revenue-side
- **ARR** (MRR × 12)
- **ACV** (average contract value)
- **Expansion revenue %**
- **Pipeline coverage** (3× of quota)
- **Win rate** (closed-won / total deals)

### Customer-side
- **Time to first value** (< 3 أيام target)
- **DAU / MAU ratio** (> 40% = sticky)
- **Feature adoption rate** (% users using feature X)
- **Support ticket volume** (ideal: decreasing per user)
- **CSAT** (post-ticket satisfaction)

### Operational
- **Uptime %** (SLA target: 99.9%)
- **Response time** (P50, P90, P99)
- **Error rate** (Sentry)
- **Cost per customer** (infra / total customers)
- **Employee NPS** (eNPS, after first hire)

---

## 3. Weekly Scorecard (Template)

**كل أحد 9 AM — Sami يُحدث الملف ثم يرسل summary للـ advisors.**

```
# Dealix Weekly — W[N] / 2026-MM-DD

## 🎯 The 5 Core

| KPI | Last Week | This Week | Change | Target | Status |
|-----|-----------|-----------|--------|--------|--------|
| MRR | 8,500 | 12,500 | +47% | 10,000 | ✅ |
| Churn | 0% | 0% | — | <7% | ✅ |
| NRR | 100% | 104% | +4pp | >100% | ✅ |
| CAC | 1,200 | 900 | -25% | <1,500 | ✅ |
| NPS | 48 | 52 | +4 | >40 | ✅ |

## 📈 Wins
- 3 new customers signed (+$X MRR)
- Content post got 50K views
- First Growth tier conversion

## ⚠️ Red Flags
- Demo-to-close rate dropped from 40% → 25%
- 2 support tickets P1 this week
- Infra cost per customer +15% MoM

## 🔬 Experiments (A/B this week)
- [Active] Pricing page CTA: "Start pilot" vs "Book demo"
- [Completed] LinkedIn outreach volume: 5 vs 10/day → 10 wins
- [Next] Demo length: 30 min vs 20 min

## 🎲 Predictions for Next Week
- MRR target: 15,000
- New customers: 4
- Main risk: holiday week (-20% outreach volume)

## 🔥 Priorities
1. [P0] Close deals مع [شركة 1]
2. [P0] Fix bug: WhatsApp thread sync
3. [P1] Content: publish post على LinkedIn الثلاثاء
4. [P1] Hire JD: Senior Engineer
5. [P2] Reach out to 15 new leads
```

---

## 4. Monthly Review (آخر يوم من الشهر، 2 ساعة)

### Agenda
1. **(15د)** Review الـ 5 Core + Supporting
2. **(30د)** Deep dive على أسوأ KPI
3. **(30د)** Case studies وعرض للـ advisors
4. **(15د)** Customer feedback themes
5. **(15د)** Next month's OKRs
6. **(15د)** Open questions

### Deliverables
- Monthly snapshot (1-page PDF)
- Email لـ advisors + investors
- Internal retro doc

---

## 5. Quarterly Business Review (QBR)

### Agenda (نصف يوم — 4 ساعات)
1. **(45د)** Deep dive على KPIs — annual trajectory
2. **(60د)** Product roadmap review + adjustments
3. **(30د)** Competitive analysis update
4. **(45د)** Financials: burn, runway, fundraising
5. **(30د)** Team: hires, retention, morale
6. **(30د)** Big bets للربع القادم

### Deliverables
- Full QBR deck (20-30 شريحة)
- Board meeting (لو funded)
- OKRs للربع الجديد
- Annual strategy adjustments (إن لزم)

---

## 6. Data Infrastructure

### Tools
- **PostHog:** product analytics (events, funnels, cohorts)
- **Moyasar dashboard:** revenue + churn
- **Internal DB queries:** custom metrics (CSV exports)
- **Google Sheets:** consolidation + charts
- **Slack alerts:** anomaly detection (future)

### Data quality rules
- كل event له owner محدد
- تعريف metric موثّق في wiki
- revised quarterly

### Visualization
- Dashboard داخلية: لوحة Sami
- Dashboard خارجي: للـ advisors (read-only)
- Public: nothing (حتى Series A)

---

## 7. OKRs (Objectives + Key Results)

### Q3 2026 OKRs (example)

**Objective 1: Establish product-market fit**
- KR1: 10 paying customers (was 0)
- KR2: NPS ≥ 40
- KR3: 1 case study published
- KR4: Churn ≤ 5%

**Objective 2: Build repeatable acquisition**
- KR1: CAC < 1,500 SAR
- KR2: 2+ channels producing > 3 customers each
- KR3: Demo → close rate > 30%

**Objective 3: Prepare for Q4 scale**
- KR1: 1 senior engineer hired
- KR2: 1 CSM hired
- KR3: Scale tier spec'd

### OKR rules
- 3-5 objectives max
- 3-5 KRs per objective
- Each KR: measurable + ambitious (70% achievement = success)
- Quarterly only (not monthly)

---

## 8. Alerts & Automation (Future Phase 2)

### P1 Alerts (immediate Slack ping)
- MRR drops > 10% in 1 day
- Churn > 15% in a week
- Uptime < 99% over 24h
- Support P1 ticket > 2 in 24h

### P2 Alerts (daily summary)
- New customers signed
- Demos completed
- Content engagement
- Competitor mentions

---

## 9. الفلسفة

### ما يكسب أعلى الأولوية
1. **Leading indicators** (pipeline, NPS trend, feature adoption)
2. **Revenue quality** (NRR, expansion, not just MRR)
3. **Customer-centric** (NPS, ticket resolution, time to value)
4. **Efficiency** (CAC, LTV/CAC, burn multiple)

### ما نتجاهل (للآن)
- Vanity metrics (followers, PR mentions)
- Highly technical (server response, CPU) إلا إن تأثر العميل
- Industry averages (نحن nice B2B Saudi — benchmarks العالمية موب مُناسبة كل مرة)

---

## 10. Review Calendar

| الإيقاع | اليوم/الوقت | الجلسة | المُشاركون |
|---------|-----------|--------|-----------|
| Daily | 9 AM | KPI snapshot check | Sami |
| Weekly | Sunday 9 AM | Weekly scorecard | Sami + CSM (عند hiring) |
| Monthly | Last Thursday | Monthly review | Sami + Advisors |
| Quarterly | Week 13 | QBR | Team + Advisors |
| Annual | December | Strategic planning | Team + Board |

---

*آخر تحديث: 2026-04-23 | Version 1.0*