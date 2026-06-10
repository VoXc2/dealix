# ROI Conversation Guide — دليل محادثة العائد
**Dealix — Agent #3**

> **الغرض:** كيف نتحدث عن ROI/العائد بطريقة أخلاقية، مع `is_estimate`، بدون ادعاءات مضمونة.

---

## 1. The Core Rule

**ROI conversation = إرشاد العميل لحسابه بنفسه، لا بيعه ضمان.**

```
"أقدر أساعدك تحسب العائد المحتمل. 
لا أقدر أضمن نتيجة. 
بناءً على [evidence]، النطاق المتوقع هو [X] إلى [Y]."
```

---

## 2. The ROI Framework (4 Components)

### 2.1 Cost of Status Quo
- ما تكلفة الوضع الحالي سنوياً؟
- Examples:
  - Lost leads: 50 leads/month × 10% close rate × 5,000 SAR = 25,000 SAR/month
  - Manual time: 10 hours/week × 100 SAR/hour × 52 weeks = 52,000 SAR/year
  - Errors/redo: 5 errors/month × 500 SAR = 2,500 SAR/month

### 2.2 Investment
- Dealix cost
- Examples:
  - Diagnostic 9,999 SAR
  - Workflow 12,000 SAR
  - AI Starter 25,000 SAR
  - Retainer 7,000 SAR/month

### 2.3 Expected Impact (with `is_estimate`)
- Range of expected improvement
- Examples:
  - 20-40% reduction in lead leakage (anonymized observation, is_estimate)
  - 30-50% time saved (industry data, is_estimate)
  - 10-20% conversion uplift (aggregated, is_estimate)

### 2.4 Payback Period
- Investment / Monthly impact = Months
- Example: 25,000 / 5,000 = 5 months (is_estimate)

---

## 3. The Conversation Script

### 3.1 Step 1: Quantify Status Quo
```
"خلني أساعدك تحسب الوضع الحالي:
- كم lead تفقد شهرياً بسبب بطء الرد؟
- كم يستغرق فريقك يدوياً على المتابعة؟
- ما متوسط قيمة العميل؟
- ما conversion rate الحالي؟

بناءً على هذا، نقدر نحسب التكلفة."
```

### 3.2 Step 2: Estimate Impact
```
"بناءً على تجربتي مع [N] عملاء مشابهين (anonymized):
- leakage reduction: 20-40% (تقدير)
- time saved: 30-50% (تقدير)
- conversion uplift: 10-20% (تقدير)

كل رقم تقدير. النتائج الفعلية تختلف."
```

### 3.3 Step 3: Calculate Payback
```
"إذا كان الـ impact المتوقع:
- 20,000 SAR/year saved (تقدير)
- Investment: 25,000 SAR

الـ payback: ~15 شهر
أو مع volume: ~6-9 أشهر

كل هذا تقدير، لا ضمان."
```

### 3.4 Step 4: Frame the Decision
```
"السؤال ليس 'كم يكلف Dealix'، بل:
- 'كم يكلفني الوضع الحالي سنوياً؟'
- 'هل التغيير يستحق؟'

بناءً على الأرقام، أنت تقدر تقرر."
```

---

## 4. ROI Examples (Templates)

### 4.1 Marketing Agency
- **Status quo:** 30 leads/month × 20% close × 8,000 SAR = 48,000 SAR/month potential × 30% lost = 14,400 SAR/month leaked (estimate)
- **Investment:** Workflow 12,000 SAR
- **Impact:** 50% leakage reduction = 7,200 SAR/month saved (estimate)
- **Payback:** ~2 months (estimate)

### 4.2 Clinic
- **Status quo:** 200 appointments/month × 15% no-show = 30 missed × 200 SAR = 6,000 SAR/month (estimate)
- **Investment:** Workflow 15,000 SAR
- **Impact:** 50% no-show reduction = 3,000 SAR/month (estimate)
- **Payback:** ~5 months (estimate)

### 4.3 Education
- **Status quo:** 500 inquiries/season × 5% close = 25 enrollments × 10,000 SAR = 250,000 SAR potential × 40% lost = 100,000 SAR lost (estimate)
- **Investment:** AI Starter 25,000 SAR
- **Impact:** 30% recovery = 30,000 SAR (estimate)
- **Payback:** ~10 months (estimate)

---

## 5. Forbidden ROI Claims

### 5.1 ❌ Don't Do
- ❌ "ضمان 5x ROI"
- ❌ "ستحقق 100,000 ريال في 6 أشهر"
- ❌ "نتائج مضمونة"
- ❌ بدون `is_estimate` label
- ❌ "دائماً" / "أبداً" (always/never)
- ❌ "بدون مخاطرة"

### 5.2 ✅ Do
- ✅ "تقدير"
- ✅ "النطاق المتوقع"
- ✅ "بناءً على anonymized observation"
- ✅ "النتائج الفعلية تختلف"
- ✅ "هذا ليس ضمان"
- ✅ "تخضع لمخاطر"

---

## 6. The "Can I Guarantee" Question

### 6.1 Answer: No
```
"لا أقدر أضمن نتيجة. هذا ضد سياستنا.
ما أقدر أقوله: بناءً على عملاء مشابهين،
النطاق المتوقع [X] إلى [Y]. 
النتيجة الفعلية تعتمد على [factors]."
```

### 6.2 Why We Don't Guarantee
- Legal risk
- Reputation risk
- Honesty principle
- `claim_policy.yaml.roi_or_guarantee.allowed: false`
- PDPL/PROFESSIONAL standards

### 6.3 When Client Insists on Guarantee
- Refuse politely
- Offer different framing
- Walk away if needed

---

## 7. The ROI Calculator (For Client)

نوفر للعميل:
- ROI Calculator (input/output)
- Based on their numbers
- With assumptions
- Not a guarantee, a tool

**Format:** spreadsheet, founder-built, founder-approved

---

## 8. The "What If" Conversation

### 8.1 "What if it doesn't work?"
```
"إذا الـ impact كان أقل من المتوقع:
- we reassess the workflow
- we adjust
- we re-deliver (in scope)
- if needed, partial refund (founder approval)

نحن نتحمل جزء من المخاطر لأن نثق في delivery."
```

### 8.2 "What's the worst case?"
```
"الـ worst case: 
- investment lost
- some time spent
- lessons learned

ليس worst case كارثي. هذا investment in clarity."
```

### 8.3 "What if I want to scale up?"
```
"إذا نجحنا، خيارات scaling:
- workflow آخر
- integration جديد
- multi-team
- Full OS upgrade
- retainer

النجاح يفتح الأبواب، لا يغلقها."
```

---

## 9. The Founder's ROI Stance

### 9.1 Founder Says
```
"Dealix ليس magic. هو نظام محكوم يحقق نتائج 
إذا استخدمته بشكل صحيح. النتائج تعتمد على:
- industry
- adoption
- team
- market

لا أضمن، لكن أقدر أساعدك تقيس."
```

### 9.2 Why This Works
- Honest → trust
- Realistic → no disappointment
- Empowering → client owns decision
- Long-term → repeat business

---

## 10. Companion Files

- Objections: `OBJECTION_BANK_AR.md`
- Enablement: `SALES_ENABLEMENT_PLAYBOOK_AR.md`
- Competitor: `COMPETITOR_POSITIONING_AR.md`
- Risk: `RISK_REVERSAL_POLICY_AR.md`
- Existing: `claim_policy.yaml`
- Existing: `MARKET_INTELLIGENCE_METRICS_CREDIBILITY_AR.md`

---

**ROI = أداة تفكير، لا سلاح بيع. founder يعلّم العميل يحسب، العميل يقرر بوعي. لا ضمان، لا وعود فارغة.**
