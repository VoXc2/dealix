# Pricing Guardrails — حواجز التسعير
**Dealix — Agent #3**

> **الغرض:** قواعد صارمة تحمي التسعير من التآكل، وتضمن أن كل سعر له موافقة مناسبة، وأن الهامش محفوظ.

---

## 1. Principles (المبادئ)

### 1.1 Pricing is Anchor + Floor + Ceiling
- **Anchor** — price clients expect
- **Floor** — minimum price to maintain margin
- **Ceiling** — maximum price within published range
- **Outside range** = approval level up

### 1.2 Pricing Tied to Value, Not Cost-Plus
- Default: value-based (what client gets)
- Floor: cost + 30% margin
- Anchor: market rate × positioning

### 1.3 Never Discount for Hesitation
- Hesitation = sign of bad fit, not negotiation
- Discount = loss of margin, not win
- Re-evaluate fit, not price

### 1.4 Founder Approves All Final Prices
- All prices require founder approval (L1-L5)
- Quotes cannot be sent without approval
- No "I think we can do X" without founder sign-off

---

## 2. Pricing Rules (Per Pricing.yaml)

| العرض | Min (SAR) | Max (SAR) | Approval Level |
|-------|-----------|-----------|----------------|
| Readiness Scan | 0 | 499 | L1 (auto) |
| Revenue Leakage Diagnostic (starter) | 1,500 | 1,999 | L1 |
| Revenue Leakage Diagnostic (standard) | 3,500 | 3,999 | L1 |
| Revenue Leakage Diagnostic (executive) | 4,500 | 5,000 | L1 |
| Revenue Leakage Diagnostic (enterprise) | 5,001 | 25,000 | L2 |
| Follow-up Recovery Workflow (basic) | 8,000 | 10,000 | L1 |
| Follow-up Recovery Workflow (standard) | 11,000 | 14,000 | L1 |
| Follow-up Recovery Workflow (advanced) | 15,000 | 18,000 | L2 |
| AI Revenue Ops Starter (lite) | 18,000 | 22,000 | L2 |
| AI Revenue Ops Starter (standard) | 23,000 | 28,000 | L2 |
| AI Revenue Ops Starter (pro) | 29,000 | 35,000 | L3 |
| Full Revenue OS (standard) | 35,000 | 50,000 | L3 |
| Full Revenue OS (pro) | 51,000 | 75,000 | L3 |
| Full Revenue OS (enterprise) | 76,000 | 90,000 | L4 |
| Monthly Retainer (bronze) | 3,000 | 5,000 | L1 |
| Monthly Retainer (silver) | 6,000 | 10,000 | L1 |
| Monthly Retainer (gold) | 11,000 | 15,000 | L2 |
| Custom Company OS | 90,000+ | open | L5 + legal |

**Source:** `dealix/config/pricing.yaml` (existing) + extension

---

## 3. Margin Floors (الحد الأدنى للهامش)

| Tier | Min Margin | Reason |
|------|-----------|--------|
| Readiness Scan | 100% | just time |
| Diagnostic | 50% | small, fast |
| Workflow | 50% | mid-effort |
| AI Starter | 40% | mid-effort + 4 weeks |
| Full OS | 35% | high effort + 60 days |
| Retainer | 60% | ongoing, relationship |
| Custom | 30% | complex, founder approval |

**Note:** هذه floors تقريبية. القيم الفعلية تحتاج calibration من data.

---

## 4. Approval Levels (L1-L5)

### 4.1 L1 — Auto-Approve
- Within published range
- Standard terms
- Single offer
- No discount
- **Approver:** founder (1 click)

### 4.2 L2 — Founder Review
- Within range + complex delivery
- Small discount (<5%)
- Multi-workflow
- **Approver:** founder with reason

### 4.3 L3 — Founder + Reason
- Mid-tier (Standard, Pro)
- Discount 5-15%
- Multiple offers
- **Approver:** founder + log

### 4.4 L4 — Founder + Legal
- Premium tier
- Discount > 15%
- Multi-month contract
- **Approver:** founder + counsel review

### 4.5 L5 — Custom + Legal
- Custom enterprise
- Custom SOW
- > 90,000 SAR
- **Approver:** founder + legal counsel + board (if needed)

---

## 5. Discount Governance

### 5.1 Allowed Discounts
- ✅ Fast payment (Net 7 vs Net 30)
- ✅ Pilot-to-retainer path
- ✅ Partner referral (per `partner_rules.yaml`)
- ✅ Case study permission
- ✅ Reduced scope
- ✅ Volume (multi-team)

### 5.2 Disallowed Discounts
- ❌ "Client is hesitating"
- ❌ "Client is big name"
- ❌ "No reason, just lower"
- ❌ Below margin floor
- ❌ Without scope reduction
- ❌ Tied to guaranteed results
- ❌ Without founder approval

### 5.3 Discount Levels
- **0-5%:** founder L1 auto
- **5-10%:** founder L2
- **10-15%:** founder L2 + reason
- **15-25%:** founder L3 + reason + scope review
- **> 25%:** founder L4 + scope reduction mandatory

---

## 6. Payment Terms

| العرض | Default Terms | Allowed Variations |
|-------|---------------|---------------------|
| Diagnostic | 100% upfront | Net 7 (founder approval) |
| Workflow | 50/50 | 100% upfront (5% discount) |
| AI Starter | 50/50 | 100% upfront (5% discount) |
| Full OS | 30/40/30 | milestones |
| Retainer | Monthly upfront | quarterly (10% discount) |
| Custom | milestones per SOW | TBD per deal |

**Source:** `MANUAL_PAYMENT_SOP.md` (existing) + extension

---

## 7. Currency & Tax

- **Currency:** SAR (Saudi Riyal)
- **VAT:** 15% (added to invoice)
- **ZATCA:** compliant invoice (Phase 2)
- **Payment:** Moyasar (sandbox default, live with approval)
- **Refund:** case-by-case, founder approval

---

## 8. The Pricing Negotiation Script

### 8.1 When Client Pushes for Lower Price
```
"أقدّر اهتمامك. السعر في [range] يشمل [deliverables]. 
إذا كان خارج النطاق، يمكنني:
1. تقليل scope: [X]، [Y]، [Z]
2. تقسيم على مراحل: phase 1 [X SAR]، phase 2 [Y SAR]
3. تحويل لـ retainer: [X SAR]/month

أيهم يناسبك أكثر؟"
```

### 8.2 When Client Asks for Discount
```
"السعر في النطاق، لكن أقدر أنظر في:
1. دفع سريع: خصم 5% إذا دفع خلال 7 أيام
2. شهادات عميل: خصم 5% إذا وافقت على case study
3. شريك موثوق: خصم 10-20% عبر partner program

ما الذي يناسبك؟"
```

### 8.3 When Client Wants Custom Pricing
```
"السعر يحدد بناءً على scope و timeline. أرسل لي:
1. Pain محدد
2. Scope المقترح
3. Timeline المطلوب
4. Budget التقريبي

ثم نحضر custom quote مع founder approval."
```

---

## 9. Anti-Patterns

### 9.1 ❌ Don't Do
- ❌ Quote without discovery
- ❌ Discount for negotiation
- ❌ Price below margin floor
- ❌ Custom at standard price
- ❌ Discount for case study promise (without actually doing it)
- ❌ "We'll figure out pricing later"
- ❌ "I quoted 5K, can you approve?" (after the fact)

### 9.2 ✅ Do
- ✅ Always refer to pricing.yaml
- ✅ Always check approval level
- ✅ Always log final price
- ✅ Always explain scope
- ✅ Always have backup (different tier)

---

## 10. Pricing Refresh

### 10.1 When to Adjust
- Quarterly review (margin calibration)
- After 3-5 deals in tier
- Market shift (yearly)
- Founder decision (anytime)

### 10.2 Process
1. founder decision
2. Update `pricing.yaml` (founder only)
3. Update `pricing_rules.yaml`
4. Notify sales
5. Update public pricing (if applicable)

---

## 11. Companion Files

- Policy: `DISCOUNT_POLICY_AR.md`
- Terms: `PAYMENT_TERMS_AR.md`
- Anchoring: `PRICE_ANCHORING_GUIDE_AR.md`
- Approval: `QUOTE_APPROVAL_POLICY_AR.md`
- Data: `data/commercial/pricing_rules.yaml`
- Schema: `schemas/pricing_rule.schema.json`
- Report: `reports/commercial/PRICING_RISK_REVIEW.md`
- Config: `dealix/config/pricing.yaml` (existing)

---

**Pricing = حماية المؤسس. كل سعر خارج النطاق = founder approval. كل discount = سبب. كل margin floor = احترام.**
