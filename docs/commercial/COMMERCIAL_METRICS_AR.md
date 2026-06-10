# Commercial Metrics — مؤشرات الأداء التجارية
**Dealix — Agent #3**

> **الغرض:** قائمة المؤشرات التي يجب أن يعرفها المؤسس يومياً/أسبوعياً/شهرياً، وكيفية حسابها، وأين مصدرها، وماذا يفعل بها. مرتبط بـ `kpi_founder_commercial_registry.yaml` و `claim_policy.yaml`.

---

## 1. الفلسفة

**مبدأ جوهري:** الأرقام تأتي من CRM أو من النظام — لا تخمين. أي رقم في هذا الملف له:
- **مصدر بيانات** (Source)
- **تردد قراءة** (Cadence)
- **مالك** (Owner)
- **threshold** للقرار

**حماية الأرقام:** `claim_policy.yaml.numeric_claim_in_customer_pack.must_have_source_or: is_estimate_true` — أي رقم في customer pack يجب أن يكون له source أو يكون estimate labeled.

---

## 2. Daily Metrics (يومية)

### 2.1 ما يجب أن يعرفه المؤسس كل صباح

| المؤشر | المصدر | الحساب | ماذا يعني |
|--------|--------|--------|----------|
| **Open qualified pipeline value (SAR)** | CRM | sum of qualified_A + qualified_B values | قوة الـ pipeline |
| **Proposals awaiting approval** | approvals queue | count | bottleneck detection |
| **Payments awaiting handoff** | billing queue | count | founder action needed |
| **Active risks** | risk register | count of open high/critical | attention needed |
| **Discovery calls today** | calendar | count | preparedness |
| **New leads yesterday** | lead capture | count by segment | flow health |
| **Founder approval count** | approvals log | count last 24h | load |

### 2.2 Daily Card Spec (top of `/ops/founder`)
```
┌────────────────────────────────────────────┐
│  Pipeline Value: 145,000 SAR               │
│  Proposals Awaiting: 3                     │
│  Payment Handoffs: 1                       │
│  Active Risks: 2                           │
│  Today's Discovery: 2                      │
│  Yesterday's New Leads: 12                 │
│  Founder Approvals (24h): 5                │
└────────────────────────────────────────────┘
```

---

## 3. Weekly Metrics (أسبوعية)

### 3.1 ما يجب أن يعرفه المؤسس كل أحد

| المؤشر | المصدر | الحساب | threshold |
|--------|--------|--------|-----------|
| **Won this week (SAR)** | CRM closed-won | sum | vs plan |
| **Lost this week (count)** | CRM closed-lost | count | reasons analysis |
| **Win rate** | CRM | won/(won+lost) | ≥ 25% |
| **Avg deal size** | CRM | sum/closed-won count | trend |
| **Time in stage** | CRM analytics | avg by stage | identify bottleneck |
| **Conversion by stage** | CRM analytics | % moved forward | funnel health |
| **Best offer (this month)** | CRM offer tag | close rate by offer | focus signal |
| **Best channel (this month)** | UTM/source tag | cost per won by channel | ROI signal |
| **Customer health avg** | client_health.jsonl | mean score | > 70 |
| **Renewal candidates (in 30 days)** | active contracts | count | prepare |
| **Expansion signals** | CS notes | count | follow up |
| **Channel cost** | spend log | sum by channel | vs ROI |

### 3.2 Weekly Card Spec
```
┌────────────────────────────────────────────────────┐
│  Won This Week: 35,000 SAR                         │
│  Win Rate: 28%                                     │
│  Avg Deal Size: 17,500 SAR                        │
│  Best Offer: Diagnostic 9,999 (45% close)          │
│  Best Channel: Inbound (5x ROI)                    │
│  Customer Health: 78/100                          │
│  Renewals in 30 days: 3                            │
│  Expansion Signals: 2                              │
└────────────────────────────────────────────────────┘
```

---

## 4. Monthly Metrics (شهرية)

### 4.1 ما يجب أن يعرفه المؤسس أول كل شهر

| المؤشر | المصدر | الحساب | ماذا يقرّر |
|--------|--------|--------|------------|
| **Total revenue (MR + one-time)** | CRM + invoices | sum | target vs actual |
| **Recurring revenue (MRR)** | active retainers | sum | LTV component |
| **New MRR added** | this month new | sum | growth |
| **Churned MRR** | this month lost | sum | quality signal |
| **Net MRR change** | new - churned | sum | direction |
| **CAC by channel** | spend / new customers | by channel | cut/increase |
| **LTV estimate** | avg MRR × avg lifetime | formula | LTV/CAC ratio |
| **LTV/CAC ratio** | LTV / CAC | formula | > 3 healthy |
| **Gross margin by offer** | revenue - delivery cost | by offer | > 30% floor |
| **Founder time by activity** | calendar | % by tag | reallocation |
| **Payback period (months)** | CAC / monthly margin | formula | < 12 months |
| **Active retainers** | contracts | count | LTV base |
| **Partner-sourced revenue** | partner tag | sum | channel ROI |
| **Cash on hand** | bank | current | runway |

### 4.2 Monthly Card Spec
```
┌──────────────────────────────────────────────────────────┐
│  Revenue: 65,000 SAR (one-time) + 22,000 SAR (MR)        │
│  New MRR: 9,999 SAR                                      │
│  Churned MRR: 0 SAR                                      │
│  Net MRR: +9,999 SAR                                     │
│  CAC: 1,200 SAR / LTV: 24,000 SAR / LTV:CAC = 20x       │
│  Gross Margin: 45%                                       │
│  Founder Time: Sales 40% / Delivery 25% / Strategy 20%  │
│  Payback Period: 1.5 months                              │
│  Active Retainers: 5                                     │
│  Partner Sourced: 12,000 SAR                             │
│  Cash: 240,000 SAR / 6mo runway                          │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Quarterly Metrics (ربع سنوية)

| المؤشر | الحساب | الهدف |
|--------|--------|-------|
| **Market share by segment** | won / total addressable | growth |
| **NPS** | survey | > 50 |
| **Customer count by segment** | CRM | concentration risk |
| **Channel mix shift** | revenue % by channel | diversification |
| **Brand mentions** | press/social | trend |
| **Partner count active** | contracts | relationship depth |
| **Renewal rate** | renewed / expiring | > 70% |
| **Expansion revenue %** | expansion / total | > 20% |
| **Time-to-first-value** | signed → first deliverable | < 7 days |

---

## 6. Per-Offer Metrics (لكل عرض)

لكل offer في `product_catalog.yaml`:

| المؤشر | الحساب | الهدف |
|--------|--------|-------|
| Close rate | won / proposal_sent | > 25% |
| Avg cycle time | days from qualified → won | < 30 |
| Delivery cost | hours × rate + tool cost | < 70% of price |
| Founder time | hours founder spent | < 40% of total delivery |
| Margin | (price - cost) / price | > 30% |
| Churn rate (retainer) | churned / active | < 10% monthly |
| NPS | survey | > 50 |
| Expansion rate | clients expanding / total | > 15% |
| Renewal rate | renewed / expiring | > 70% |

---

## 7. Per-Channel Metrics (لكل قناة)

لكل قناة في `CHANNEL_STRATEGY_AR.md`:

| المؤشر | الحساب | threshold |
|--------|--------|-----------|
| Volume | leads / week | per channel capacity |
| Cost | spend / period | within budget |
| Cost per lead | spend / leads | < 200 SAR |
| Cost per reply | spend / replies | < 100 SAR |
| Cost per meeting | spend / meetings | < 500 SAR |
| Cost per proposal | spend / proposals | < 1,500 SAR |
| Cost per won | spend / won | < 3,000 SAR |
| ROI | revenue / cost | > 3x |
| Spam rate | spam / sent | < 0.1% |
| Compliance rate | approved / sent | 100% |
| Bounce rate | bounce / sent | < 5% |
| Reply rate | reply / sent | > 5% |

---

## 8. Per-Segment Metrics (لكل شريحة)

لكل ICP في `data/commercial/icp_segments.yaml`:

| المؤشر | الحساب |
|--------|--------|
| Lead volume | per week |
| Qualified rate | qualified / total |
| Discovery rate | discovery / qualified |
| Close rate | won / discovery |
| Avg deal size | mean revenue |
| Time to close | mean days |
| Churn rate | monthly |
| LTV | per segment |
| NPS | per segment |

---

## 9. Anti-Metrics (ما لا نقيسه ولا نهتم به)

- ❌ "Impressions" (vanity)
- ❌ "Followers" (vanity)
- ❌ "Total emails sent" (we don't send bulk)
- ❌ "AI calls" (we measure outcomes, not activity)
- ❌ "Sessions" (we measure signups/qualified)

---

## 10. Source of Truth Hierarchy

```
CRM (source of truth for revenue, customers, deals)
  ↑
Approved registries (kpi_founder_commercial_registry.yaml, business_now_cache.yaml)
  ↑
Reports (reports/commercial/*.md)
  ↑
UI (ops pages, war-room)
  ↑
Read-only dashboards (NO writes from UI)
```

**القاعدة:** لا agent يحدّث KPI — فقط founder يدوياً عبر CRM أو approved scripts (`apply_kpi_founder_commercial.py`).

---

## 11. Read vs Write — Who Does What

| Action | Allowed | Forbidden |
|--------|---------|-----------|
| Read metrics | All agents + founder | — |
| Write to CRM | Founder only | Auto |
| Write to registries | Founder via approved script | Direct edit |
| Display in UI | Approved scripts | Random data |
| Calculate in proposal | from CRM read | Estimate without label |
| Use in customer pack | with source | with assumption only |

---

## 12. Decision Thresholds (حدود القرار)

### 12.1 Stop Channel
- Cost per won > 3,000 SAR → founder reviews
- ROI < 1x → stop
- Spam rate > 0.1% → stop immediately

### 12.2 Stop Offer
- 0 wins after 6 months → review
- Churn > 30% → review
- Margin < 25% → raise or stop

### 12.3 Hire
- Founder time on delivery > 50% → hire contractor
- Sales pipeline < 4 weeks → ramp content/partner

### 12.4 Raise Price
- Delivery cost > 70% of price → raise
- Founder time > 40% on delivery → raise or hire
- Demand > supply → raise

---

## 13. The 5 Numbers a Founder Must Know Today

1. **Pipeline value (qualified)** — هل عندي ما يكفي من الفرص؟
2. **Win rate this month** — هل المبيعات تشتغل؟
3. **Best channel ROI** — وين أركّز؟
4. **Customer health avg** — هل العملاء ناجحين؟
5. **Cash runway (months)** — كم عندي وقت؟

**إذا لم تستطع الإجابة على أي من هذه، النظام فيه مشكلة.**

---

## 14. Reports هذه الوثيقة تُغذّيها

- `reports/commercial/COMMERCIAL_DAILY_COMMAND.md` (PHASE 14)
- `reports/commercial/COMMERCIAL_WEEKLY_REVIEW.md` (PHASE 14)
- `reports/finance/COMMERCIAL_FINANCE_REVIEW.md` (PHASE 12)

---

**كل رقم في هذا الملف له مصدر، تردد، مالك، threshold. لا رقم بدون هذه الأربعة. لا حدس، لا تخمين، لا vanity metrics.**
