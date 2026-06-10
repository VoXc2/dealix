# Quote Approval Policy — سياسة الموافقة على العروض
**Dealix — Agent #3**

> **الغرض:** مستويات الموافقة على عروض الأسعار، وتفاصيل كل مستوى، وكيفية التوثيق.

---

## 1. The 5 Approval Levels

### 1.1 L1 — Auto-Approve (founder 1-click)
**Conditions (all):**
- Within published price range
- No discount
- Standard terms
- Single offer
- Standard client (no flags)

**Process:**
- Agent drafts quote
- Founder reviews (1 click)
- Quote sent

**Documentation:**
- Quote ID
- Client
- Price
- Founder signature (digital)
- Date

### 1.2 L2 — Founder Review
**Conditions (any):**
- Slightly outside range (±10%)
- Small discount (1-5%)
- Multi-workflow
- Mid-tier offer (AI Starter, Full OS standard)
- Retainer Gold
- Custom with 1 modification

**Process:**
- Agent drafts quote
- Founder reviews with reason
- Approval required
- Quote sent

**Documentation:**
- Quote ID
- Reason for L2
- Founder approval
- Modified terms

### 1.3 L3 — Founder + Reason + Scope Review
**Conditions (any):**
- Mid discount (5-15%)
- Premium tier (Full OS Pro/Enterprise)
- Multi-offer bundle
- Custom enterprise > 90K
- Regulated industry
- 3+ month commitment

**Process:**
- Agent drafts quote
- Founder + reason logged
- Scope review
- Approval
- Quote sent

**Documentation:**
- Quote ID
- Full reason
- Scope verification
- Founder + CCO (if exists) approval

### 1.4 L4 — Founder + Legal
**Conditions (any):**
- Large discount (>15%)
- Custom enterprise (50K-100K)
- Multi-month contract
- Regulated industry
- Government/regulated
- Legal review needed
- > 6 month commitment

**Process:**
- Agent drafts SOW
- Founder + legal review
- Counsel review (optional)
- Approval
- Contract signed

**Documentation:**
- SOW
- Legal review notes
- Founder + counsel approval
- Signed contract

### 1.5 L5 — Custom + Legal + Board
**Conditions (any):**
- > 100K SAR deal
- Custom enterprise OS
- Multi-stakeholder
- Legal risk
- Brand risk
- Strategic (founder + board)

**Process:**
- Custom SOW
- Founder + legal + counsel
- Board review (if needed)
- Multiple approvals
- Signed contract

**Documentation:**
- SOW
- Legal + counsel review
- Board minutes (if applicable)
- Multiple signatures

---

## 2. Quote Format

```yaml
- quote_id: "q_2026_001"
- opportunity_id: "opp_2026_001"
- client_name: "Acme Agency"
- client_contact: "Ahmed Ali, CEO"
- client_sector: "marketing_agency"
- offer_id: "ai_revenue_ops_starter"
- offer_name: "AI Revenue Ops Starter"
- list_price_sar: 25000
- discount_pct: 0
- discount_amount_sar: 0
- final_price_sar: 25000
- currency: SAR
- scope:
  - "3-5 workflows"
  - "1 dashboard"
  - "4 weeks delivery"
  - "2 weeks support"
- out_of_scope:
  - "Multi-team"
  - "24/7 support"
- timeline_days: 21
- payment_terms: "50/50"
- approval_level: L2
- founder_approved: true
- approved_at: "2026-06-03"
- approved_by: "founder"
- valid_until: "2026-06-17"
- notes: "Standard terms"
```

---

## 3. Approval Workflow

### 3.1 Auto-Generated Quote
- Created by Proposal Agent
- Routed to founder queue
- Founder clicks approve/reject/revise
- On approve: sent to client
- On reject: returned to agent for revision
- On revise: notes for next iteration

### 3.2 Manual Override
- Founder can directly edit quote
- Must log reason
- Must update approval level

### 3.3 Audit Trail
- Every quote has audit trail
- Versioning (v1, v2, ...)
- Date, time, actor for each action

---

## 4. Quote Validity

- **Default validity:** 14 days
- **Special cases:** 30 days (founder approval)
- **Expired:** must re-quote (or extend)

---

## 5. Quote Rejection

### 5.1 Common Reasons
- ❌ Out of range
- ❌ Bad fit
- ❌ Spam indicators
- ❌ Missing info
- ❌ Discount too high

### 5.2 Process
- Document reason
- Notify team
- Update opportunity status

---

## 6. Quote Acceptance

### 6.1 When Client Accepts
- Client signs (digital)
- Founder confirms
- Invoice created
- Payment link sent
- Delivery handoff

### 6.2 When Client Negates
- Founder call
- Re-negotiation
- Possible re-quote
- Possible walk away

---

## 7. Special Approval Cases

### 7.1 Government / Regulated
- Always L4 minimum
- Legal review mandatory
- Procurement awareness
- Multi-signature

### 7.2 Multi-Stakeholder
- L3+ if multiple DMs
- All DMs must approve
- Champion identification
- Longer cycle

### 7.3 Renewal (existing client)
- L1 (auto) if within range
- L2 if any modification
- L3 if discount or scope change

### 7.4 Partner-Led
- Per partner agreement
- Co-signed by founder + partner
- L2+ usually

---

## 8. Quote-to-Cash Pipeline

```
Quote Drafted
   ↓
Approval (L1-L5)
   ↓
Quote Sent
   ↓
Client Reviews
   ├─ Accept → Invoice → Payment → Delivery
   ├─ Negotiate → Re-quote
   └─ Reject → Document + Learn
```

---

## 9. Quote Analytics

Monthly:
- Quotes by approval level
- Quotes by outcome (accept/reject/negotiate)
- Average approval time
- Average discount
- Founder time per quote

---

## 10. Companion Files

- Pricing: `PRICING_GUARDRAILS_AR.md`
- Discount: `DISCOUNT_POLICY_AR.md`
- Anchoring: `PRICE_ANCHORING_GUIDE_AR.md`
- Terms: `PAYMENT_TERMS_AR.md`
- Existing: `dealix/config/approval_policy.yaml`
- Existing: `dealix/config/pricing.yaml`
- Data: `data/commercial/pricing_rules.yaml`
- Schema: `schemas/pricing_rule.schema.json`

---

**موافقة = حماية المؤسس + احترام العميل. كل مستوى له سبب، كل سبب موثّق، كل قرار قابل للمراجعة.**
