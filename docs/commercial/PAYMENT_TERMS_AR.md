# Payment Terms — شروط الدفع
**Dealix — Agent #3**

> **الغرض:** شروط دفع واضحة لكل عرض، مع سياسات الاسترداد، والتأخر، والمتأخرات.

---

## 1. Payment Terms by Offer

| العرض | Default | Variations |
|-------|---------|------------|
| Readiness Scan | 100% upfront | Net 7 (founder approval) |
| Revenue Leakage Diagnostic (any tier) | 100% upfront | Net 7 (L1) |
| Follow-up Recovery Workflow | 50/50 | 100% upfront (-5%) |
| AI Revenue Ops Starter | 50/50 | 100% upfront (-5%) or 30/70 |
| Full Revenue OS | 30/40/30 | milestones |
| Monthly Retainer | Monthly upfront | Quarterly (-10%) |
| Custom Company OS | milestones per SOW | TBD |

**Source:** `MANUAL_PAYMENT_SOP.md` (existing) + extension

---

## 2. Payment Methods

| Method | Status | Notes |
|--------|--------|-------|
| Bank transfer (SAR) | ✅ primary | Saudi local bank |
| Moyasar (sandbox) | ✅ default | `MOYASAR_LIVE_MODE=0` |
| Moyasar (live) | ⚠️ with approval | `MOYASAR_LIVE_MODE=1` |
| Stripe | ❌ not used | — |
| Cash | ⚠️ rare | only for diagnostic, with receipt |
| Check | ❌ not used | — |

---

## 3. Invoicing

### 3.1 Standard Process
1. Quote approved (founder)
2. Invoice created (ZATCA-compliant)
3. Payment link sent (Moyasar)
4. Client pays
5. Webhook confirms payment
6. Delivery starts

### 3.2 ZATCA Compliance
- All invoices ZATCA-compliant
- Use `dealix/commercial/zatca_invoice.py` (existing)
- VAT 15% added

### 3.3 Invoice Format
- Client name
- Client VAT number (if B2B)
- Date
- Offer + scope
- Price (pre-VAT)
- VAT 15%
- Total
- Payment terms
- Bank details or Moyasar link

---

## 4. Refund Policy

### 4.1 When Allowed
- ✅ Delivery failure (Dealix fault)
- ✅ Material scope mismatch
- ✅ Client cancels before delivery start (full refund)
- ✅ Client cancels during delivery (partial, founder approval)
- ✅ Walk-away by Dealix (full refund)

### 4.2 When Not Allowed
- ❌ Client changed mind after delivery
- ❌ Client claims satisfaction but wants refund
- ❌ Bulk refund requests
- ❌ Refund > 30 days post-delivery

### 4.3 Refund Process
1. Client request (email)
2. Founder review
3. Decision (full/partial/no)
4. Approval level: L3 for any refund
5. Refund processed via original method
6. Reason logged

### 4.4 Refund Format
```yaml
- refund_id: "ref_001"
- opportunity_id: "opp_001"
- client_name: "Acme"
- original_amount_sar: 25000
- refund_amount_sar: 10000
- reason: "delivery_failure"
- approval_level: L3
- founder_approved: true
- processed_at: "2026-06-03"
- method: "bank_transfer"
```

---

## 5. Late Payment Policy

### 5.1 Timeline
- Net 7: payment due 7 days
- Net 30: payment due 30 days
- Retainer: due 1st of month

### 5.2 Actions
- Day 1 past due: gentle reminder
- Day 7 past due: formal reminder + pause delivery
- Day 14 past due: founder call
- Day 30 past due: late fee + legal review

### 5.3 Late Fee
- 5% per month on overdue amount
- Founder approval required
- Legal grounds per Saudi law

### 5.4 Pause Rules
- Pause new work on day 7 overdue
- Pause support on day 14 overdue
- Founder call before any pause

---

## 6. Disputed Payment

### 6.1 When Client Disputes
1. Listen + document
2. Founder review
3. Find resolution (refund, partial, work completion)
4. Document in dispute log

### 6.2 If Refused
- Legal review
- Possibly stop work
- Possibly legal action (rare)

### 6.3 Pattern Detection
- 1 dispute = note
- 2 disputes from same client = founder attention
- 3+ disputes = walk away (no new deals)

---

## 7. Payment Confirmation

### 7.1 After Payment
- Webhook (Moyasar) or bank confirmation
- Update CRM
- Notify team
- Send thank-you + next step

### 7.2 Receipt
- Auto-receipt (Moyasar)
- Or manual receipt (bank)
- Client gets within 24h

---

## 8. Payment Handoff to Delivery

### 8.1 After Payment Confirmed
- Update CRM (status: paid)
- Trigger delivery kickoff
- Notify delivery team
- Send client welcome (CS agent drafts, founder approves)

### 8.2 Approval Required
- All payment-related actions require founder approval
- Per `approval_policy.yaml`:
  - `invoice_send`: high, requires_approval
  - `refund_request`: high, requires_approval
  - `affiliate_payout`: high, requires_approval
  - `discount_request`: medium, requires_approval

---

## 9. Multi-Currency (Future)

Currently SAR only. If international:
- USD, AED, EUR (founder approval)
- FX rate at invoice date
- Bank fees borne by client

---

## 10. Tax & Compliance

### 10.1 VAT
- 15% on all B2B invoices
- B2C: also 15% (if applicable)
- VAT registration required for B2B > 375K SAR/year

### 10.2 ZATCA
- All invoices ZATCA-compliant (Phase 2)
- E-invoicing required
- Use existing `zatca_invoice.py`

### 10.3 Withholding Tax
- If client is foreign: possible withholding
- Founder + legal review

---

## 11. Companion Files

- Guardrails: `PRICING_GUARDRAILS_AR.md`
- Discount: `DISCOUNT_POLICY_AR.md`
- Approval: `QUOTE_APPROVAL_POLICY_AR.md`
- Anchoring: `PRICE_ANCHORING_GUIDE_AR.md`
- Existing: `MANUAL_PAYMENT_SOP.md`

---

**شروط دفع واضحة = توقعات واضحة = نزاعات أقل. founder يوافق، النظام ينفّذ، الـ log يحمي.**
