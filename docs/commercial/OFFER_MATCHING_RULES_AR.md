# Offer Matching Rules — قواعد مطابقة العروض
**Dealix — Agent #3**

> **الغرض:** القواعد التي تحكم كيف نختار العرض المناسب لـ pain معين. مكمل لمصفوفة `PAIN_TO_OFFER_MATRIX_AR.md`.

---

## 1. Selection Logic

### 1.1 الـ 5 أسئلة التي تحدد المطابقة

1. **ما هو الـ pain بالضبط؟** (محدد، ليس "مشكلة عامة")
2. **ما حجم الألم؟** (ميزانية العميل تحلها)
3. **ما سرعة الألم؟** (urgency)
4. **ما درجة الثقة في التشخيص؟** (high/medium/low)
5. **هل العميل ضمن ICP؟** (foundation)

---

## 2. Hard Rules

### 2.1 لا Match بدون Pain
- ❌ لا نبيع عرض لمن لا يعاني
- ❌ لا "upsell" لمن لم يحقق success metric
- ❌ لا diagnostic لمن لم يطلب أو لم يُظهر interest

### 2.2 لا Match بدون ICP Fit
- ❌ لا diagnostic لـ student/job seeker
- ❌ لا enterprise quote لـ micro
- ❌ لا premium لمن budget < 5K

### 2.3 لا Match بدون Evidence
- ❌ لا ادعاء بأرقام بدون source
- ❌ لا "guaranteed" claim
- ❌ لا "ROI 10x" بدون estimate label

### 2.4 لا Match مع Spam Request
- ❌ reject cold spam request
- ❌ reject mass WhatsApp request
- ❌ reject guaranteed revenue

---

## 3. Soft Rules (Founder Approval)

### 3.1 Premium-to-Standard
- إذا العميل premium budget → standard offer + retainer path
- إذا العميل standard budget → premium = risk (override only)

### 3.2 Standard-to-Premium
- إذا الألم أكبر من standard → propose premium
- founder approval required

### 3.3 Diagnostic-to-Implementation
- إذا بعد diagnostic الألم أكبر → upsell
- founder approval + evidence

---

## 4. Decision Tree (شجرة القرار)

```
[Pain signal detected]
   ↓
[Is pain in our 10 categories?]
   ├─ No → nurture or refer out
   └─ Yes ↓
[What's the pain confidence?]
   ├─ Low → discovery first
   ├─ Medium → standard offer with discovery
   └─ High → direct offer
[What's the ICP fit?]
   ├─ Bad fit → disqualify
   └─ Good fit ↓
[What's the budget fit?]
   ├─ < 5K → nurture or partner referral
   ├─ 5-15K → starter/standard
   ├─ 15-35K → mid tier
   └─ 35K+ → premium (founder approval)
[What's the urgency?]
   ├─ High → same-week delivery possible
   └─ Normal → 14-30 day delivery
[What's the evidence level?]
   ├─ L0 → no proposal
   ├─ L1-L2 → internal observation
   └─ L3+ → client data
[Match offer from matrix]
   ↓
[Founder approves?]
   ├─ No → revise or disqualify
   └─ Yes → proposal
```

---

## 5. Conflict Resolution (تعارضات)

### 5.1 Diagnostic vs Direct Offer
- **Default:** diagnostic first (safer)
- **Exception:** if pain is clear and high-confidence → direct offer
- **Founder approval required** for direct offer skip diagnostic

### 5.2 Standard vs Premium
- **Default:** standard
- **Exception:** if client budget > 50K + multi-workflow → premium
- **Founder approval required**

### 5.3 Single Offer vs Package
- **Default:** single offer
- **Exception:** if 2-3 pains intertwined → package
- **Package price = single × 1.3-1.5** (bundle discount, founder approval)

---

## 6. Tier Validation

| العرض | Pain min confidence | ICP min score | Budget min |
|-------|---------------------|---------------|------------|
| Readiness Scan | any | 6+ | 0 (free) |
| Revenue Leakage Diagnostic | medium | 10+ | 5K |
| Follow-up Recovery Workflow | medium | 10+ | 8K |
| AI Revenue Ops Starter | high | 15+ | 18K |
| Full Revenue OS | high | 15+ | 35K |
| Monthly Optimization Retainer | high (post-delivery) | 15+ | 3K/mo |
| Custom Company OS | high (specific) | 15+ | 90K+ |

---

## 7. Match Failure Recovery

### 7.1 إذا لا يوجد Match
- ❌ لا نقول "sorry we don't serve you"
- ✅ نقول: "نقترح [بديل]، أو [nurture for later]، أو [refer to partner]"

### 7.2 إذا Match لكن Client Disagrees
- Founder escalation
- Re-discovery
- Adjust scope or price

### 7.3 إذا Match لكن Budget Insufficient
- Offer alternative (lower tier)
- Offer partner referral
- Offer payment plan (founder approval)

---

## 8. Special Cases

### 8.1 Government / Regulated
- Always founder approval
- Compliance review first
- No "guaranteed" claim
- Procurement awareness

### 8.2 Multi-Stakeholder
- Identify champion first
- Multi-meeting approach
- Custom proposal structure

### 8.3 Existing Customer (Upsell)
- Health score check first
- Success metric must be met
- Founder approval for upsell
- Use existing relationship

### 8.4 Partner-Sourced
- Partner agreement first
- Margin split per `partner_rules.yaml`
- Co-branded materials

---

## 9. Override Protocol

إذا الـ rules تعطي نتيجة خاطئة:
1. Document why
2. Founder approval
3. Log in risk register
4. Update rules if pattern emerges

**لا override صامت. لا override متكرر بدون update.**

---

## 10. Companion Files

- Matrix: `PAIN_TO_OFFER_MATRIX_AR.md`
- Categories: `PROBLEM_CATEGORY_MAP_AR.md`
- Data: `data/commercial/pain_to_offer.yaml`
- Schemas: `schemas/pain_signal.schema.json`, `schemas/offer_match.schema.json`
- Report: `reports/commercial/OFFER_MATCH_REVIEW.md`

---

**الـ rules = guide rails، لا jail. founder يقدر يخرج عنها، لكن مع توثيق. لا استثناء صامت، لا تكرار بدون update.**
