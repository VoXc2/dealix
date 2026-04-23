# Dealix — النموذج المالي

## P&L 12 شهر + Unit Economics + Cash Flow

**آخر تحديث:** 2026-04-23 | **أفق التخطيط:** 2026-04 → 2029-12 (3 سنوات)

---

## 1. الافتراضات الأساسية

### التسعير (SAR، شامل VAT 15%)

| الخطة | شهري | سنوي (خصم 15%) | Target % |
|------|------|---------------|---------|
| Pilot | 1 | — | 20% (conversion funnel) |
| Starter | 999 | 10,189 | 40% |
| Growth | 2,999 | 30,590 | 30% |
| Scale | 7,999 | 81,590 | 10% |

**ARPU مُرجّح:** (0.4 × 999) + (0.3 × 2,999) + (0.1 × 7,999) = **2,099 SAR/شهر** (بعد تجاوز Pilot)

### معدلات النمو (شهر بشهر)

| Metric | Y1 | Y2 | Y3 |
|--------|----|----|----|
| New customers/شهر | 2-15 | 20-50 | 80-150 |
| Churn شهري | 5% | 4% | 3% |
| Gross margin | 75% | 82% | 85% |

### افتراضات التكلفة

| البند | Y1/شهر | Y2/شهر | Y3/شهر |
|------|--------|--------|--------|
| Infrastructure (Railway + STC Cloud) | 1,500 | 8,000 | 25,000 |
| SaaS tools (Moyasar + PostHog + Sentry) | 800 | 3,500 | 10,000 |
| Founder salary (Sami) | 0 (Y1 Q1-Q2), 8K (Q3-Q4) | 25K | 40K |
| Engineers (Y1: 0, Y2: 2, Y3: 5) | 0 | 40K | 100K |
| Sales/CSM (Y1: 0, Y2: 1, Y3: 3) | 0 | 15K | 45K |
| Marketing | 2,000 | 15,000 | 50,000 |
| Legal + accounting | 1,500 | 3,000 | 6,000 |
| Office + misc | 500 | 3,000 | 8,000 |

---

## 2. P&L — السنة الأولى (شهر بشهر)

**العملة: SAR | Customers = cumulative**

| الشهر | New | Total | MRR | Churn | Net MRR | Costs | Net Profit |
|-------|-----|-------|-----|-------|---------|-------|-----------|
| M1 (Apr 26) | 2 | 2 | 2,000 | 0 | 2,000 | 6,300 | -4,300 |
| M2 (May) | 3 | 5 | 5,500 | 100 | 5,400 | 6,300 | -900 |
| M3 (Jun) | 4 | 9 | 10,000 | 275 | 9,725 | 6,300 | 3,425 |
| M4 (Jul) | 5 | 13 | 15,500 | 500 | 15,000 | 6,300 | 8,700 |
| M5 (Aug) | 6 | 18 | 22,000 | 775 | 21,225 | 14,300 | 6,925 |
| M6 (Sep) | 8 | 25 | 31,500 | 1,100 | 30,400 | 14,300 | 16,100 |
| M7 (Oct) | 10 | 33 | 43,500 | 1,575 | 41,925 | 14,300 | 27,625 |
| M8 (Nov) | 12 | 43 | 58,500 | 2,175 | 56,325 | 14,300 | 42,025 |
| M9 (Dec) | 14 | 55 | 76,500 | 2,925 | 73,575 | 14,300 | 59,275 |
| M10 (Jan 27) | 14 | 66 | 93,500 | 3,825 | 89,675 | 14,300 | 75,375 |
| M11 (Feb) | 15 | 77 | 112,500 | 4,675 | 107,825 | 14,300 | 93,525 |
| M12 (Mar) | 15 | 87 | 132,500 | 5,625 | 126,875 | 14,300 | 112,575 |

### Y1 Totals
- **Ending customers:** 87
- **Ending MRR:** 126,875 SAR
- **Ending ARR:** ~1.52M SAR
- **Total Revenue Y1:** ~580K SAR
- **Total Costs Y1:** ~130K SAR
- **Net Profit Y1:** ~450K SAR (من الشهر 3 onwards)
- **Cash breakeven:** الشهر 3

---

## 3. Unit Economics

### LTV / CAC

| Metric | القيمة | كيف |
|--------|-------|-----|
| **ARPU شهري** | 2,099 SAR | mix 40/30/10 |
| **Gross Margin** | 75% | Y1 infra + support |
| **Churn شهري** | 5% | conservative Y1 |
| **Lifetime (أشهر)** | 20 | 1 / 0.05 |
| **LTV** | 31,485 SAR | ARPU × GM × lifetime |
| **CAC (ref: Referral)** | ~2,000 SAR | 20% commission على سنة |
| **CAC (ref: Outbound)** | ~800 SAR | Sami time cost/customer |
| **CAC (blended)** | 1,200 SAR | 60/40 mix |
| **LTV/CAC** | **26×** | ممتاز (target > 3×) |
| **Payback** | 1.1 شهر | (CAC / ARPU × GM) |

### Rule of 40
- Revenue growth: ~400% Y1 → Y2
- Profit margin: ~30% Y1
- **Rule of 40 score: 430** (excellent)

---

## 4. النموذج 3 سنوات

| Year | Ending Customers | ARR (SAR) | Revenue (السنة) | Gross Profit | Net Profit |
|------|------------------|-----------|-----------------|--------------|-----------|
| Y1 (2026) | 87 | 1.52M | 580K | 435K | 450K |
| Y2 (2027) | 380 | 9.5M | 5.5M | 4.5M | 2.8M |
| Y3 (2028) | 1,200 | 30M | 20M | 17M | 11M |
| Y4 target | 3,500 | 90M | 60M | 51M | 35M |
| Y5 target | 8,000 | 200M | 140M | 119M | 80M |

**Upside scenarios (aggressive):**
- Y1 ARR: 4.3M (لو 150 عميل بنهاية السنة — يحتاج 15 عميل/شهر بنمو قوي)
- Y3 ARR: 50M (لو اختراق UAE + قطر + البحرين)

---

## 5. Cash Flow

### Cash position (initial = 10K SAR من ميزانية Sami)

| الشهر | Cash In | Cash Out | Net | Running |
|-------|---------|----------|-----|---------|
| M1 | 2,000 | 6,300 | -4,300 | 5,700 |
| M2 | 5,500 | 6,300 | -800 | 4,900 |
| M3 | 10,000 | 6,300 | +3,700 | 8,600 |
| M6 | 31,500 | 14,300 | +17,200 | 30,000+ |
| M12 | 132,500 | 14,300 | +118,200 | 500K+ |

**تحليل:**
- أقل نقطة cash: الشهر 2 (5,000 SAR)
- Breakeven: الشهر 3
- Positive cash flow مستمر: من M3
- **لا حاجة لـ funding Y1 — bootstrappable**

---

## 6. سيناريوهات

### Best case (aggressive growth)
- 150 عميل بنهاية Y1 → ARR 4.3M
- يتطلب: 2 full-time hires في M6
- Funding needed: 500K (للـ hires + marketing)

### Base case (balanced — هذا النموذج)
- 87 عميل → ARR 1.5M
- Bootstrappable
- Sami full-time + 1 part-time helper

### Worst case (slow growth)
- 30 عميل → ARR 450K
- Sami يحافظ على full-time job
- Part-time launch

---

## 7. Fundraising Strategy

### متى تُفكّر في seed round?

**Signals إيجابية:**
- 30+ عملاء مدفوعين (Y1 M8-M10)
- NRR > 110% (revenue من عملاء حاليين تنمو)
- LTV/CAC > 3×
- 3+ case studies موثقة
- Pipeline mature (50+ qualified leads)

**متى لا:**
- قبل 10 عملاء — النموذج غير مُثبت
- CAC > LTV/3 — الحل خاطئ
- Churn > 10% شهري — المنتج ما يعلق

### حجم الجولة المقترح (Y1 M10-M12)
- **Seed:** 1-2M SAR (266-533K USD)
- **Dilution:** 10-15%
- **Valuation pre-money:** 10-15M SAR
- **Use of funds:**
  - 40% Product (2 engineers)
  - 30% GTM (1 sales + marketing)
  - 20% Operations (CSM + legal)
  - 10% Reserve

### المستثمرون المستهدفون (KSA)
- **STV (Saudi Telecom Ventures)** — enterprise SaaS
- **Raed Ventures** — early-stage B2B
- **Wa'ed (Aramco)** — Saudi startups
- **IMPACT46** — regional SaaS
- **Khwarizmi Ventures** — Tier 1 KSA VC

### Angel investors المثاليون
- مؤسسون سابقون لشركات SaaS سعودية ناجحة
- VPs of Sales في شركات enterprise
- Consultants في digitization (إحالات + نصائح)

---

## 8. KPIs لمراقبة النموذج

### يومي
- New signups
- MRR added/churned

### أسبوعي
- Qualified demos (> 15 دقيقة)
- Pilot conversions
- Support ticket volume

### شهري
- ARR growth
- Gross margin
- Churn rate
- NPS
- LTV/CAC

### ربع سنوي
- Net Revenue Retention (NRR)
- Customer Acquisition Cost trends
- Cohort retention
- Feature adoption
- Time to first value

---

## 9. المخاطر المالية + Mitigations

| المخاطرة | الاحتمال | الأثر | Mitigation |
|---------|---------|------|-----------|
| Churn > 10% | متوسط | عالي | Customer onboarding playbook + CSM مبكر |
| CAC يرتفع × 2 | متوسط | عالي | Referral program + organic content |
| منافس كبير يقلد | منخفض | متوسط | أول-mover في Arabic RTL + WhatsApp |
| Infrastructure costs تنفجر | منخفض | متوسط | Reserved instances + multi-cloud |
| Founder burnout | عالي | عالي | Hire CSM بالشهر 6 |
| Regulatory shift (PDPL) | منخفض | متوسط | Compliance framework جاهز |

---

## 10. ملاحظات ختامية

**النموذج محافظ intentionally.** السيناريو base case مُحاط بـ assumptions stretched:
- Churn 5% (صناعة: 3-6%)
- ARPU 2,099 SAR (conservative mix)
- نمو customers 15/شهر max Y1 (يقدر يكون أكثر)

**النقاط الأقوى:**
- Bootstrappable — لا حاجة funding Y1
- Breakeven الشهر 3
- LTV/CAC 26× — استثنائي
- Rule of 40 = 430 — top decile

**النقاط التي تحتاج attention:**
- Sami single-founder — key-person risk
- Customer concentration — أول 10 عملاء = 50% من MRR
- No sales team — يعتمد على founder bandwidth

---

*آخر تحديث: 2026-04-23 | Version 1.0*