# Proof Pack Commercial Guide — دليل حزمة الإثبات التجارية
**Dealix — Agent #3**

> **الغرض:** كيف نبني proof pack (حزمة إثبات) قوية، مسموح بها، وتغلق الصفقات. مكمل لـ `data/templates/proof_pack_ar.md`.

---

## 1. What is a Proof Pack?

**حزمة إثبات = مجموعة من الأدلة والحقائق والحالات التي تثبت قيمة Dealix لعميل معين.**

ليست "case study" فقط — بل:
- قبل/بعد workflow
- leakage points identified
- expected measurement
- evidence level
- relevant examples
- assumptions
- risk
- recommended pilot

---

## 2. Evidence Levels (L0-L5)

| Level | Definition | Allowed? |
|-------|-----------|----------|
| **L0** | No source | ❌ forbidden in customer pack |
| **L1** | Hypothetical example | ✅ with `is_estimate` label |
| **L2** | Anonymized observation | ✅ with disclosure |
| **L3** | Aggregated industry data | ✅ with source |
| **L4** | Single-tenant anonymized | ✅ with opt-in only |
| **L5** | Named case study | ✅ with written permission |

**Source:** `claim_policy.yaml` + `no_overclaim.yaml` (existing)

---

## 3. Proof Pack Sections

### 3.1 Cover
- Client name (or "Sample")
- Date
- Author
- Version
- Approval

### 3.2 Executive Summary (1 page)
- Problem identified
- Solution proposed
- Expected impact
- Evidence level
- Risk disclosure

### 3.3 Current State Analysis
- Leakage points (specific, named)
- Workflow gaps
- Tool/CRM assessment
- Team capability

### 3.4 Recommended Workflow
- Workflow diagram
- Step-by-step
- Tools/integrations
- Approval gates

### 3.5 Expected Impact
- Quantified (with `is_estimate`)
- Range (not point)
- Time-to-value
- Risk disclaimer

### 3.6 Evidence
- Anonymized examples
- Industry data
- Sample workflows
- References (with permission)

### 3.7 Assumptions
- What we assume
- What we need
- What's out of scope

### 3.8 Risks
- Honest assessment
- Mitigation
- Decision needed

### 3.9 Recommended Pilot
- Scope
- Timeline
- Investment
- Success metric

### 3.10 Next Step
- Clear action
- Due date
- Owner

---

## 4. The 5-Question Filter

قبل إرسال proof pack:
1. **هل كل claim له evidence level؟** (yes required)
2. **هل كل ROI labeled `is_estimate`؟** (yes required)
3. **هل المخاطر موثقة؟** (yes required)
4. **هل founder وافق؟** (yes required)
5. **هل النتيجة قابلة للقياس؟** (yes required)

---

## 5. Proof Pack by Use Case

### 5.1 Sales Tool (during sales)
- Show value early
- Customized to client
- Visual + simple
- One page main + details

### 5.2 Magnet (for lead gen)
- Public, anonymized
- Shows category leadership
- Downloadable
- Gated or ungated (founder decides)

### 5.3 Diagnostic Deliverable
- Client-specific
- High evidence level
- Detailed
- Drives next step

### 5.4 Case Study (named)
- Written permission required
- L5 only
- Marketing use
- Multi-channel

### 5.5 Internal Reference
- Internal use
- Higher detail
- For sales team training

---

## 6. Common Proof Pack Mistakes

### 6.1 ❌ Don't Do
- ❌ Claim without evidence
- ❌ ROI without `is_estimate`
- ❌ Named client without permission
- ❌ Hidden risks
- ❌ Fake data
- ❌ Exaggerated numbers

### 6.2 ✅ Do
- ✅ Honest assessment
- ✅ Labeled estimates
- ✅ Clear risks
- ✅ Approved evidence
- ✅ Realistic expectations
- ✅ Founder approval

---

## 7. Proof Pack for Different ICPs

### 7.1 Marketing Agency
- Show campaign ROI improvement
- Show lead quality
- Reference agency-style workflows
- Time-to-value: 14 days

### 7.2 Clinic
- Show appointment recovery
- Show no-show reduction (with PDPL)
- Healthcare compliance highlighted
- Time-to-value: 21 days

### 7.3 Education
- Show enrollment recovery
- Show admission conversion
- Season-aware examples
- Time-to-value: 30 days

### 7.4 Local SaaS
- Show RevOps improvement
- Show dashboard clarity
- Show team productivity
- Time-to-value: 30 days

---

## 8. Proof Pack Approval

### 8.1 L1 — Standard
- L1 evidence only
- Standard format
- Founder review

### 8.2 L2 — Custom
- L2-L3 evidence
- Client-specific
- Founder + reason

### 8.3 L3 — Sensitive
- L4 evidence
- Regulated industry
- Compliance review

### 8.4 L4 — Named
- L5 evidence
- Named client
- Legal + permission

---

## 9. Proof Pack Storage

- Templates: `data/templates/proof_pack_ar.md`
- Per-client: `data/commercial/{client_id}/proof/`
- Sample: `docs/commercial/operations/sample_proof_pack/`
- Schema: `schemas/commercial_proof_pack.schema.json`

---

## 10. Companion Files

- Strategy: `PROPOSAL_STRATEGY_AR.md`
- Case Study: `CASE_STUDY_POLICY_AR.md`
- Existing: `data/templates/proof_pack_ar.md`
- Existing: `dealix/commercial/proof_builder.py`
- Schema: `schemas/commercial_proof_pack.schema.json`
- Report: `reports/commercial/PROPOSAL_COMMERCIAL_REVIEW.md`

---

**Proof pack = وعد مدعوم بالأدلة. كل claim موثّق، كل رقم estimated، كل risk معلن. founder يوقّع، العميل يثق، النظام يحمي.**
