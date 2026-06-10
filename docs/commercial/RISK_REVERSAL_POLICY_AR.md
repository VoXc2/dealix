# Risk Reversal Policy — سياسة عكس المخاطر
**Dealix — Agent #3**

> **الغرض:** كيف نقلل المخاطر على العميل (والفريق) بدون تعريض Dealix للخطر.

---

## 1. Core Principle

**Risk reversal = نتحمل جزء من المخاطرة لنكسب ثقة.**

لكن:
- ليس "ضمان استرداد كامل" (سخيف)
- ليس "ضمان نتائج" (يخالف `claim_policy.yaml`)
- ليس "free POC غير محدود" (delivery burden)

**Reversal = structured, founder-approved, documented.**

---

## 2. Reversal Tools

### 2.1 Pilot Discount
- **Structure:** first 30 days at -20%
- **Conditions:** commit to 3-month retainer
- **Risk on Dealix:** discount on early work
- **Risk on Client:** commit to 3 months
- **Approval:** L2

### 2.2 Phased Delivery
- **Structure:** phase 1 (50%), evaluate, phase 2 (50%)
- **Conditions:** phase 1 must deliver
- **Risk on Dealix:** do phase 1 well
- **Risk on Client:** pay phase 2 if satisfied
- **Approval:** L1

### 2.3 Conditional Refund
- **Structure:** if not satisfied, partial refund
- **Conditions:** within 30 days, specific reasons
- **Risk on Dealix:** some refund risk
- **Risk on Client:** honest evaluation
- **Approval:** L3

### 2.4 Money-Back on Diagnostic
- **Structure:** if diagnostic not valuable, refund
- **Conditions:** attended + gave data + reasonable expectations
- **Risk on Dealix:** some refund
- **Risk on Client:** engage in process
- **Approval:** L2

### 2.5 Free Read-Only Assessment
- **Structure:** we review your CRM/data, give recommendations, no implementation
- **Conditions:** data shared, time allocated
- **Risk on Dealix:** time only
- **Risk on Client:** implementation decision
- **Approval:** L1

### 2.6 Pilot to Retainer Path
- **Structure:** pilot 1 month → if value proven → retainer
- **Conditions:** clear success metric
- **Risk on Dealix:** prove value
- **Risk on Client:** commit if value
- **Approval:** L2

---

## 3. What's NOT Reversal (Forbidden)

### 3.1 ❌ Don't Do
- ❌ "Money-back guarantee" (open-ended)
- ❌ "Results guarantee" (claim violation)
- ❌ "Unlimited revisions" (delivery burden)
- ❌ "Free everything" (margin loss)
- ❌ "Pay after results" (cash flow + delivery burden)
- ❌ "We'll do whatever it takes" (open scope)

### 3.2 Why
- Delivery collapse
- Margin loss
- Client disappointment
- Reputation risk
- Legal risk

---

## 4. Reversal Conditions

### 4.1 Must Have
- ✅ Specific scope
- ✅ Specific timeline
- ✅ Specific success metric
- ✅ Refund conditions documented
- ✅ Founder approval
- ✅ Client signature

### 4.2 Cannot Have
- ❌ "Satisfaction" (subjective)
- ❌ "Implied" (vague)
- ❌ Open-ended (no end date)
- ❌ Without scope limit

---

## 5. The Conversation

### 5.1 "How do I know it works?"
```
"ما أقدر أضمن نتيجة. لكن:
- Pilot: 30 يوم بسعر مخفض، تقيم، تقرر
- Phase 1: 50% من الـ scope، تقيّم، phase 2 إذا راضي
- Conditional refund: إذا ما حققنا metric، refund جزئي

أيهما يناسبك؟"
```

### 5.2 "What if I don't like it?"
```
"الخيارات:
- نوقف وننهي (لا refund عادة)
- نعدّل الـ scope ونحاول مرة ثانية
- partial refund في ظروف استثنائية (founder approval)

السؤال: ما 'ما يعجبك' تعنيه؟ إذا حددنا metric مسبقاً،
نعرف إذا حققناه أو لا."
```

### 5.3 "I want to see results first"
```
"هذا exactly الـ pilot:
- 30 يوم
- metric محدد
- إذا تحقق → نكمل
- إذا لم يتحقق → نقيم

ما تحتاج تدفع كامل قبل ما تشوف قيمة."
```

---

## 6. The Refund Path

### 6.1 When
- Delivery failure (Dealix fault)
- Material scope mismatch
- Within refund window
- Founder approval

### 6.2 Process
1. Client requests (email, with reason)
2. Founder review
3. Decision: full / partial / no
4. Approval: L3
5. Refund processed
6. Reason logged

### 6.3 Default Refund Amount
- 0-30 days post-delivery: 50% (founder)
- 30-60 days: 25% (founder)
- > 60 days: 0%
- Material failure: 100% (founder)

**Source:** `PAYMENT_TERMS_AR.md` (PHASE 5)

---

## 7. Reversal Documentation

```yaml
- reversal_id: "rev_001"
- opportunity_id: "opp_001"
- client_name: "Acme"
- reversal_type: "pilot_discount"
- terms: "30 days at -20%, commit to 3-month retainer"
- risk_on_dealix: "discount on early work"
- risk_on_client: "3-month commit"
- success_metric: "30% leakage reduction in 30 days"
- approval_level: L2
- founder_approved: true
- approved_at: "2026-06-03"
- client_signed: false
```

---

## 8. Reversal Tracking

Monthly:
- Reversals by type
- Refund rate
- Refund amount
- Pattern analysis
- Founder time

---

## 9. Anti-Patterns

### 9.1 ❌ Don't Do
- ❌ Reversal for negotiation only
- ❌ Reversal without metric
- ❌ Reversal without approval
- ❌ Reversal more than once
- ❌ Reversal that exceeds margin floor

### 9.2 ✅ Do
- ✅ Reversal as designed tool
- ✅ With clear metric
- ✅ With founder approval
- ✅ Once per client
- ✅ Within margin

---

## 10. Companion Files

- Pricing: `PRICING_GUARDRAILS_AR.md`
- Discount: `DISCOUNT_POLICY_AR.md`
- Terms: `PAYMENT_TERMS_AR.md`
- Objections: `OBJECTION_BANK_AR.md`
- ROI: `ROI_CONVERSATION_GUIDE_AR.md`
- Risk: `COMMERCIAL_RISK_REGISTER_AR.md` (PHASE 13)

---

**Risk reversal = structured tool, not open promise. founder يحدد، العميل يوقّع، النظام يحمي. لا "ضمان"، لا "مجاني"، فقط structured commitment.**
