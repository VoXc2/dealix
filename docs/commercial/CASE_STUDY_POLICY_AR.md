# Case Study Policy — سياسة دراسات الحالة
**Dealix — Agent #3**

> **الغرض:** كيف ننشر دراسات الحالة (case studies) بطريقة أخلاقية، قانونية، ومفيدة.

---

## 1. Core Principles

### 1.1 No Fake Case Studies ❌
- ❌ لا نخترع case studies
- ❌ لا نستخدم hypothetical بدون label
- ❌ لا نبالغ في النتائج
- ❌ لا ننسب نتائج بدون إذن

### 1.2 Hypothetical Examples ✅
- ✅ إذا استخدمنا hypothetical → نوسم بـ "hypothetical example" أو "is_estimate"
- ✅ لا ننسبها لعميل حقيقي
- ✅ نوضح أنها للتوضيح

### 1.3 Real Results ✅
- ✅ نتائج حقيقية = بسم العميل (مع إذن)
- ✅ نتائج حقيقية = بدون اسم (anonymized)
- ✅ نتائج حقيقية = مع توثيق (data + period + methodology)

---

## 2. Case Study Types

### 2.1 Named Case Study (L5)
**Requirements:**
- Written permission from client
- Founder + legal approval
- Compliance review (if regulated)
- Specific results documented
- Time period specified
- Methodology disclosed

**Process:**
1. Client completes successfully
2. CS Agent asks permission (with sample)
3. Client signs release
4. Draft case study
5. Client reviews + approves
6. Founder + legal final approval
7. Publish

### 2.2 Anonymized Case Study (L4)
**Requirements:**
- Real data, no name
- Methodology disclosed
- Founder approval
- Risk: client can identify themselves (acceptable)

**Process:**
1. Successful delivery
2. Draft anonymized version
3. Founder approval
4. Publish (note: "based on real client experience, name withheld")

### 2.3 Aggregated Industry Data (L3)
**Requirements:**
- Multiple clients
- Aggregated
- Source disclosed
- Methodology disclosed
- Founder approval

**Process:**
1. Aggregate data from N clients
2. Document methodology
3. Founder approval
4. Publish (with sample size and source)

### 2.4 Hypothetical Example (L1)
**Requirements:**
- Labeled clearly
- No real client implied
- Founder approval

**Process:**
1. Draft hypothetical scenario
2. Label as "hypothetical"
3. Founder approval
4. Use in education/sales

---

## 3. Permission Process

### 3.1 Request Permission
- After successful delivery
- During renewal discussion
- After testimonial collected
- Before public use

### 3.2 Permission Format
```yaml
- case_study_id: "cs_001"
- client_name: "Acme Agency"
- contact_name: "Ahmed Ali"
- contact_role: "CEO"
- permission_granted: true
- permission_type: ["named", "logo_use", "metric_citation", "testimonial"]
- valid_until: "2027-06-03"
- signature_date: "2026-06-03"
- restrictions: "no_competitor_comparison"
- founder_approved: true
- legal_reviewed: true
```

### 3.3 Restrictions to Note
- Time limit (e.g., 1 year)
- Channel restriction
- Competitor exclusion
- Industry exclusion
- Logo vs name

---

## 4. What Case Studies Must Include

### 4.1 Required
- ✅ Client name (or "Anonymized")
- ✅ Industry/sector
- ✅ Time period
- ✅ Problem (specific)
- ✅ Solution (what we did)
- ✅ Results (with metric)
- ✅ Evidence level
- ✅ Methodology
- ✅ Disclaimer

### 4.2 Optional
- Quote from client
- Before/after visuals
- Workflow diagram
- Implementation time
- Team involved

### 4.3 Forbidden
- ❌ Guarantees
- ❌ "Always" / "Never" claims
- ❌ Exaggeration
- ❌ Hidden methodology
- ❌ Selective data

---

## 5. Case Study Distribution

### 5.1 Channels
- Website (gated download or public)
- Sales decks
- Email follow-up
- Social media (with permission)
- PR
- Investor materials
- Partner enablement

### 5.2 Approval Per Channel
- Website: L1+
- Sales decks: founder approval
- Email: founder approval
- Social: L2+ only
- PR: L4+ only (legal review)
- Investor: founder + legal
- Partner: founder approval

---

## 6. Case Study Refresh

### 6.1 Cadence
- Quarterly: review all published
- Update stale metrics
- Remove outdated claims
- Add new (with permission)

### 6.2 Sunset Triggers
- Permission expired
- Client relationship ended badly
- Results disputed
- Methodology challenged
- Legal/compliance concern

---

## 7. Common Failure Modes

### 7.1 ❌ Don't Do
- ❌ Publish without permission
- ❌ Exaggerate results
- ❌ Use outdated data
- ❌ Hide methodology
- ❌ Selective reporting
- ❌ Cross-promote competitors

### 7.2 ✅ Do
- ✅ Always permission
- ✅ Realistic results
- ✅ Fresh data
- ✅ Clear methodology
- ✅ Complete reporting
- ✅ Honor restrictions

---

## 8. ROI Statements in Case Studies

### 8.1 Allowed ✅
- "Achieved 30% reduction in [metric] in 60 days"
- "Recovered 50 leads/month previously lost"
- "Saved 10 hours/week of manual work"
- (with measurement, time period, methodology)

### 8.2 Forbidden ❌
- "Guaranteed 5x ROI"
- "Always saves time"
- "Will definitely work for you"
- (without evidence or with `is_estimate` label)

---

## 9. The 5-Question Filter

قبل نشر أي case study:
1. **هل عندنا إذن مكتوب؟** (yes required)
2. **هل النتائج موثقة؟** (yes required)
3. **هل methodology موصوفة؟** (yes required)
4. **هل level صحيح؟** (L1-L5)
5. **هل founder وافق؟** (yes required)

---

## 10. Companion Files

- Strategy: `PROPOSAL_STRATEGY_AR.md`
- Proof: `PROOF_PACK_COMMERCIAL_GUIDE_AR.md`
- Existing: `claim_policy.yaml`
- Existing: `no_overclaim.yaml` (register)
- Schema: `schemas/commercial_proof_pack.schema.json`

---

**Case study = وعد عميل. بدون إذن = انتهاك. بدون توثيق = تضليل. founder يوقّع، العميل يثق، السمعة تبقى.**
