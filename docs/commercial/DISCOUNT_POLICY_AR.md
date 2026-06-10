# Discount Policy — سياسة الخصم
**Dealix — Agent #3**

> **الغرض:** قواعد صارمة لمنح الخصومات، متى، كم، ولماذا. حماية الهامش، ومنع الإفراط في التفاوض.

---

## 1. The Core Rule

**خصم فقط مقابل:**
1. ✅ دفع سريع (Net 7 vs Net 30)
2. ✅ pilot-to-retainer (خصم على الـ pilot)
3. ✅ partner referral (per `partner_rules.yaml`)
4. ✅ case study permission (فعلي، بعد التسليم)
5. ✅ scope reduction
6. ✅ multi-team volume
7. ✅ strategic value (founder approval)

**خصم ممنوع لـ:**
- ❌ hesitation, negotiation, "big client", without reason, below margin, scope not reduced, tied to results

---

## 2. Discount Levels

| Level | Range | Approval | Required |
|-------|-------|----------|----------|
| **D0** | 0% (no discount) | L1 (auto) | none |
| **D1** | 1-5% | L1 (founder) | reason logged |
| **D2** | 5-10% | L2 (founder + reason) | reason + scope check |
| **D3** | 10-15% | L2 (founder + reason) | reason + scope review |
| **D4** | 15-25% | L3 (founder + CCO) | reason + scope reduction |
| **D5** | 25%+ | L4 (founder + legal) | forbidden unless strategic + scope cut |

---

## 3. Discount Mechanics

### 3.1 Fast Payment
- **Net 7 vs Net 30** → 5% off
- **Net 0 (upfront)** → 7% off
- **Applies to:** any tier
- **Approval:** L1 auto

### 3.2 Pilot to Retainer
- **Pilot:** 30 days at -20%
- **Then:** full retainer
- **Total commit:** 3 months minimum
- **Approval:** L2

### 3.3 Partner Referral
- **Per `partner_rules.yaml`:**
  - referral_partner: 10-20% of first payment
  - implementation_partner: implementation_fee retained
  - co_selling: per agreement
- **Approval:** per partner agreement (founder-approved)

### 3.4 Case Study Permission
- **After delivery** (not before)
- **Discount:** 5% on retainer
- **Requires:** actual case study, anonymized or named
- **Approval:** L2

### 3.5 Scope Reduction
- **Remove items from scope**
- **Discount:** proportional to removed cost
- **Approval:** L2

### 3.6 Multi-Team Volume
- **Multi-team or multi-region**
- **Discount:** 5-10% on additional units
- **Approval:** L2

### 3.7 Strategic Value
- **Strategic client (founder knows)**
- **Discount:** founder's discretion
- **Approval:** L4+

---

## 4. Discount Request Format

```yaml
- discount_id: "disc_001"
- opportunity_id: "opp_001"
- client_name: "Acme Agency"
- offer_id: "ai_revenue_ops_starter"
- list_price_sar: 25000
- requested_discount_pct: 10
- requested_discount_amount_sar: 2500
- final_price_sar: 22500
- reason: "fast_payment" # or "pilot_to_retainer" or "partner_referral" etc.
- scope_change: "none" # or "removed_X" etc.
- approval_level_required: L2
- founder_approved: false
- approved_at: null
- approved_by: null
```

---

## 5. The Discount Conversation (Scripts)

### 5.1 When Client Asks for Discount
```
"السعر في النطاق. أقدر أنظر في:
1. دفع سريع: -5% إذا دفع خلال 7 أيام
2. شراكة: -10-20% عبر partner program
3. شهادات عميل: -5% بعد التسليم
4. scope أقل: نشوف وش نستطيع ننقص

ما الذي يناسبك أكثر؟"
```

### 5.2 When Client Negotiates Hard
```
"أقدّر جدية اهتمامك. خلني أوضح:
السعر يشمل [deliverables] و [timeline] و [support].
إذا كان الميزانية محدود، أقدر أقترح:
1. Tier أقل: [X SAR] بدلاً من [Y SAR]
2. Payment plan: phase 1 ثم phase 2
3. Pilot صغير أولاً

اللي يناسبك؟"
```

### 5.3 When Client Compares to Competitor
```
"شكراً للمقارنة. ما يميزنا:
- [differentiator 1]
- [differentiator 2]
- [proof of value]

السعر يعكس القيمة، لكن أقدر أنظر في:
- الدفع السريع
- Pilot to retainer

اللي يهمك أكثر؟"
```

---

## 6. Discount Log (Mandatory)

كل خصم يجب أن يُسجّل:
- في `data/commercial/discounts.jsonl`
- Format JSONL (one discount per line)
- Fields: id, opportunity_id, reason, amount, approval, date

**مراجعة شهرية:** founder يطلع على الأنماط.

---

## 7. Anti-Patterns

### 7.1 ❌ Don't Do
- ❌ خصم بدون سبب
- ❌ خصم للتفاوض فقط
- ❌ خصم تحت margin floor
- ❌ خصم مرتبط بنتائج مضمونة
- ❌ خصم قبل discovery
- ❌ خصم متكرر بدون reason
- ❌ خصم متعدد على نفس deal

### 7.2 ✅ Do
- ✅ خصم مقابل قيمة (دفع سريع، partner، case study)
- ✅ خصم مع scope reduction
- ✅ خصم مع founder approval
- ✅ خصم مع log
- ✅ خصم once (لا متعدد)

---

## 8. Discount Recovery

### 8.1 If Client Pushes for More
- Re-evaluate fit (maybe bad fit)
- Re-quote at different tier
- Walk away (sometimes best)

### 8.2 If Discount Doesn't Close
- It's a fit issue, not price
- Move to nurture or disqualify

---

## 9. Discount Impact Tracking

Monthly:
- Total discount amount
- Discount by reason
- Win rate with/without discount
- Margin impact
- Pattern detection (who asks for discount?)

---

## 10. Companion Files

- Guardrails: `PRICING_GUARDRAILS_AR.md`
- Anchoring: `PRICE_ANCHORING_GUIDE_AR.md`
- Approval: `QUOTE_APPROVAL_POLICY_AR.md`
- Terms: `PAYMENT_TERMS_AR.md`
- Data: `data/commercial/pricing_rules.yaml`
- Schema: `schemas/pricing_rule.schema.json`
- Report: `reports/commercial/PRICING_RISK_REVIEW.md`

---

**خصم = تنازل عن هامش. لازم يكون له سبب ولازم يكون موثّق. founder يحمي الهامش، لا الوكلاء.**
