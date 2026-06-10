# Proposal Approval Policy — سياسة الموافقة على العروض
**Dealix — Agent #3**

> **الغرض:** كل proposal يمر بمستوى موافقة (L1-L5) حسب الحجم والتعقيد. مكمل لـ `QUOTE_APPROVAL_POLICY_AR.md` (pricing) مع تركيز على proposal.

---

## 1. The 5 Approval Levels (Proposal-Specific)

### 1.1 L1 — Auto-Approve
**Conditions:**
- Standard offer (Diagnostic, Workflow)
- Within published range
- No discount
- Standard terms
- Standard scope

**Approver:** Founder (1 click)
**Time:** < 24 hours
**Documentation:** Standard proposal + founder signature

### 1.2 L2 — Founder Review
**Conditions:**
- Mid-tier (AI Starter)
- Slight discount (1-5%)
- Multi-workflow
- Retainer Gold

**Approver:** Founder with reason
**Time:** 1-2 days
**Documentation:** Proposal + reason logged

### 1.3 L3 — Founder + Reason + Scope Review
**Conditions:**
- Premium tier (Full OS)
- Mid discount (5-15%)
- Bundle offer
- Regulated industry
- Multi-stakeholder

**Approver:** Founder + CCO + reason
**Time:** 2-3 days
**Documentation:** Full proposal + reason + scope verification

### 1.4 L4 — Founder + Legal
**Conditions:**
- Custom enterprise (50K-100K)
- Large discount (> 15%)
- Multi-month contract
- Regulated industry
- Government/regulated
- Legal review needed

**Approver:** Founder + counsel review
**Time:** 3-7 days
**Documentation:** SOW + legal review + signature

### 1.5 L5 — Custom + Legal + Board
**Conditions:**
- > 100K SAR
- Custom Company OS
- Multi-stakeholder
- Brand risk
- Strategic (founder + board)

**Approver:** Founder + legal + counsel + board
**Time:** 7-14 days
**Documentation:** Full SOW + multiple signatures + board minutes

---

## 2. Pre-Approval Checklist

قبل إرسال لأي عميل:

- [ ] Discovery note exists
- [ ] Pain category identified
- [ ] Product match confirmed
- [ ] Success metric defined
- [ ] Scope clear (in/out)
- [ ] Timeline realistic
- [ ] Price within range
- [ ] Discount reason (if any)
- [ ] Compliance reviewed (if needed)
- [ ] Approval level correct
- [ ] Founder signature
- [ ] Validity date set
- [ ] Next step clear
- [ ] Evidence level labeled
- [ ] No forbidden claims
- [ ] Translation if needed

---

## 3. Approval Routing

### 3.1 Standard Flow
```
Proposal Agent drafts
   ↓
Auto-check (price, scope, claims)
   ↓
Founder queue
   ↓
[L1] 1 click
[L2] 1 click + reason
[L3] review + reason + scope
[L4] + legal
[L5] + board
   ↓
Approved → Send
Rejected → Revise
```

### 3.2 Time SLA
- L1: < 24 hours
- L2: 1-2 days
- L3: 2-3 days
- L4: 3-7 days
- L5: 7-14 days

---

## 4. Approval Triggers

### 4.1 Auto-Elevate (to L+1)
- Client in regulated industry
- Government/procurement
- Multi-stakeholder
- Custom enterprise
- > 90K SAR
- > 6 month commitment

### 4.2 Auto-Block (cannot send)
- ❌ No discovery note
- ❌ Pain not clear
- ❌ Forbidden claim present
- ❌ Price out of range (without approval)
- ❌ Discount > 30%
- ❌ Spam indicators

---

## 5. Post-Approval Actions

### 5.1 After Approval
- Lock proposal (no edits without re-approval)
- Send to client
- Log in CRM
- Update opportunity stage
- Schedule follow-up

### 5.2 Validity
- Default: 14 days
- Special: 30 days (founder approval)
- Expired: re-quote or extend

---

## 6. Re-Approval

### 6.1 When Required
- Price change
- Scope change
- Timeline change
- Term change
- After validity expires

### 6.2 Process
- Note the change
- Re-route to appropriate level
- Document the change
- Re-send to client

---

## 7. Approval Rejection

### 7.1 Common Reasons
- Out of range price
- Bad fit
- Missing info
- Forbidden claim
- Too aggressive discount

### 7.2 Process
- Document reason
- Return to agent
- Revise or disqualify
- Update opportunity

---

## 8. Approval Audit

### 8.1 Monthly Review
- Approval distribution by level
- Time to approval
- Rejection reasons
- Discount pattern

### 8.2 Founder Review
- Any pattern of over-approval
- Margin impact
- Process improvement

---

## 9. Companion Files

- Quote: `QUOTE_APPROVAL_POLICY_AR.md` (pricing)
- Pricing: `PRICING_GUARDRAILS_AR.md`
- Strategy: `PROPOSAL_STRATEGY_AR.md`
- Proof: `PROOF_PACK_COMMERCIAL_GUIDE_AR.md`
- Schema: `schemas/commercial_proposal.schema.json`
- Existing: `os/15_PROPOSAL_TEMPLATE.md`
- Existing: `dealix/config/approval_policy.yaml`

---

**موافقة = حماية المؤسس + العميل. كل مستوى له سبب، كل سبب موثّق، كل decision قابل للمراجعة.**
