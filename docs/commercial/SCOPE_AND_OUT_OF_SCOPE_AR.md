# Scope and Out-of-Scope — النطاق والـ Out-of-Scope
**Dealix — Agent #3**

> **الغرض:** لكل عرض، ما هو مشمول (in-scope) وما هو غير مشمول (out-of-scope). هذا الملف يمنع scope creep ويحمي الهامش.

---

## 1. Why This File Exists

**Scope creep** = أكبر قاتل للهامش في شركات الخدمات.

**الحماية = وضوح ما هو "نعم" وما هو "لا" قبل البدء.**

كل عرض له:
- **In-scope** (مشمول)
- **Out-of-scope** (غير مشمول)
- **Change order** (إذا العميل طلب إضافة)

---

## 2. Cross-Cutting Out-of-Scope

ما لا يدخل في **أي** عرض إلا بموافقة founder + سعر مخصص:

### 2.1 External Sending (autonomous)
- ❌ Cold email blasts
- ❌ Cold WhatsApp
- ❌ LinkedIn automation
- ❌ Auto social posts (low quality)
- ❌ Mass scraping

### 2.2 Compliance-Heavy Work
- ❌ Legal contracts (founder + counsel)
- ❌ Tax filings
- ❌ Audit support
- ❌ Regulatory submissions

### 2.3 Custom Development (out of standard scope)
- ❌ Custom integrations (unless in SOW)
- ❌ New product features
- ❌ Bug fixes in third-party tools
- ❌ Hosting setup

### 2.4 Data Operations (out of standard)
- ❌ Mass data entry
- ❌ Manual transcription
- ❌ Data deletion requests (refer to legal)

### 2.5 Spam/Guaranteed Operations
- ❌ Spam behavior (always out)
- ❌ Guaranteed ROI claims (always out)
- ❌ Bulk WhatsApp (always out)
- ❌ Cold outreach (always out)

---

## 3. Per-Product Scope

### 3.1 Readiness Scan
**In-scope:**
- 30-min questionnaire
- 1-page report
- Top 3 priorities
- Recommended path

**Out-of-scope:**
- Multiple iterations
- Custom advice
- Implementation
- Direct comparison with competitors
- Pricing quote

### 3.2 Revenue Leakage Diagnostic
**In-scope:**
- 2-3 calls (90 min each)
- Data review
- 1 leakage map
- Top 3 priorities
- First workflow recommendation
- 1 executive report

**Out-of-scope:**
- Implementation
- Multiple reports
- Custom analysis beyond scope
- Data correction
- Tool migration
- Team training

### 3.3 Follow-up Recovery Workflow
**In-scope:**
- 1 follow-up workflow
- 3 channels max (email, WhatsApp, internal)
- Draft templates (5-10)
- Approval workflow setup
- 2 weeks support
- Weekly report

**Out-of-scope:**
- Multi-workflow
- Custom integrations beyond 1
- Tool migration
- 24/7 support
- Channel expansion (4+ channels)
- Team training beyond 1 session
- CRM rebuild

### 3.4 AI Revenue Ops Starter
**In-scope:**
- 3-5 workflows
- 1 dashboard
- 4 weeks delivery
- 2 weeks support
- Weekly review
- Draft/follow-up process
- 1 integration (e.g., CRM)

**Out-of-scope:**
- Full OS (5+ workflows)
- 2+ dashboards
- Multi-team setup
- Multi-integration
- Custom features
- 24/7 support
- Long-term retainer
- Tool migration

### 3.5 Full Revenue OS
**In-scope:**
- 5-10 workflows
- 2-3 dashboards
- 60-day delivery
- 30-day support
- Weekly review
- Training (1-2 sessions)
- 2-3 integrations
- Delivery reporting

**Out-of-scope:**
- Custom OS (90K+ SOW)
- Multi-region setup
- 4+ integrations
- Long-term retainer
- Bug fixes beyond scope
- 24/7 support

### 3.6 Monthly Optimization Retainer
**In-scope:**
- Weekly 1-hour review
- 2-3 experiments/month
- Monthly report
- Ad-hoc support (4h/month)
- Renewal/expansion discussions

**Out-of-scope:**
- New implementations
- Custom dev
- Long workshops
- Multi-team
- Multi-region
- 24/7 support
- Crisis management

### 3.7 Custom Company OS
**In-scope:**
- Per SOW (specific to deal)

**Out-of-scope:**
- Per SOW
- Anything outside SOW = change order

---

## 4. Change Order Process

### 4.1 When to Use
- Client asks for more than in-scope
- Client wants different deliverable
- Client wants to add team/region
- Client wants more integrations

### 4.2 Process
1. **Identify** — what's the additional ask?
2. **Estimate** — what is delivery cost?
3. **Price** — what is additional price (within margin floor)?
4. **Approve** — founder approval
5. **Document** — change order signed
6. **Implement** — only after approval

### 4.3 Change Order Format
```yaml
- change_order_id: "co_001"
- original_scope: "..."
- requested_change: "..."
- additional_delivery_hours: 5
- additional_price_sar: 5000
- new_total_sar: 17000
- founder_approved: true
- approved_at: "2026-06-03"
- client_acknowledged: false
```

---

## 5. The "Almost Out-of-Scope" Gray Zone

### 5.1 Common Gray Areas
- "Just one more workflow" → change order
- "Quick training for 2 more people" → small fee or include if low cost
- "Add this integration" → change order
- "One more week of support" → small fee

### 5.2 Default Rule
- إذا كان small (1-2h) → founder decides (often free as goodwill)
- إذا medium (4-8h) → change order with small fee
- إذا large (>8h) → full change order with significant price

---

## 6. Scope Creep Red Flags

### 6.1 Watch For
- ⚠️ "Just a small change" (× 10)
- ⚠️ "We assumed this was included"
- ⚠️ "Can you also do X for free?"
- ⚠️ "This should be part of the package"
- ⚠️ "Other vendors include this"
- ⚠️ "We need this for the project to work"

### 6.2 Response Patterns
- ❌ "Yes" without documenting
- ❌ "Yes, but we'll figure out pricing later"
- ✅ "This is out of scope. Let me prepare a change order."
- ✅ "Yes, with additional fee of X SAR. Founder approval required."

---

## 7. Documentation Standards

### 7.1 In Every Proposal
- Clear in-scope list
- Clear out-of-scope list
- Change order process mentioned
- Assumptions section
- Risks section

### 7.2 In Every Delivery
- Use `os/18_HANDOVER_TEMPLATE.md`
- Reference original scope
- Track actuals
- Flag deviations

### 7.3 In Every Retainer
- Monthly scope confirmation
- Hours tracking
- Out-of-scope flag

---

## 8. Margin Protection Logic

### 8.1 Margin Floor
- لا change order يقلل الـ margin تحت 30%
- إذا client pressure → reduce scope, not price
- إذا delivery cost > 70% → raise price or refuse

### 8.2 Scope Reduction Strategy
- Cut nice-to-haves first
- Cut integrations (1 → 0)
- Cut dashboards (3 → 2)
- Cut workflows (5 → 3)
- Keep core value intact

---

## 9. The "No" Scripts

### 9.1 When Asked for Out-of-Scope
```
"هذا خارج نطاق اتفاقنا. يمكن إضافته كـ change order 
بـ [X] ريال. هل تريد أن أحضر لك change order؟"
```

### 9.2 When Asked for Discount
```
"نقدر نخفض السعر إذا قللنا الـ scope. أي من هذه 
نستطيع حذفها: [list]. أيهم تنازله أسهل؟"
```

### 9.3 When Asked for Free Addition
```
"أقدّر طلبك. هذا خارج النطاق، founder يقدر يوافق 
في حالات خاصة. هل أحضر طلبك له؟"
```

---

## 10. Companion Files

- Catalog: `PRODUCT_CATALOG_AR.md`
- Packaging: `PACKAGING_STRATEGY_AR.md`
- Pricing: `PRICING_GUARDRAILS_AR.md` (PHASE 5)
- Policy: `SCOPE_CREEP_POLICY_AR.md` (PHASE 13)

---

**Scope = العقد الحقيقي. Out-of-scope = حدود العقد. founder يقدر يعدل، لكن مع توثيق. لا شفهي، لا "trust me".**
