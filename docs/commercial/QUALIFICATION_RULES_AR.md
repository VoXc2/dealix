# Qualification Rules — قواعد التأهيل
**Dealix — Agent #3**

> **الغرض:** كيف نقرر أن lead مؤهل (qualified) أم لا. المعايير، الأسئلة، والحدود.

---

## 1. Qualification Framework (BANT + Dealix Extended)

نستخدم BANT التقليدي + إضافات Dealix:

| البُعد | السؤال | Threshold |
|--------|--------|-----------|
| **B**udget | عنده ميزانية؟ | ≥ 5,000 SAR |
| **A**uthority | عنده صلاحية القرار؟ | Decision maker accessible |
| **N**eed | عنده pain حقيقي؟ | Pain category identified |
| **T**iming | متى يريد البدء؟ | Within 60 days |
| **D**ata Readiness | عنده data / tools؟ | CRM OR file |
| **F**it (Dealix) | في ICP؟ | Score ≥ 10 |
| **C**ompliance (Dealix) | يقبل PDPL + governance? | yes |

---

## 2. The 7 Qualification Questions

### 2.1 B - Budget
- "ما الميزانية المتوقعة لهذا المشروع؟"
- "هل هناك ميزانية مخصصة؟"
- "من يوافق على الصرف؟"
- **Min:** 5,000 SAR (4,999 minimum diagnostic)

### 2.2 A - Authority
- "من سيتخذ القرار النهائي؟"
- "هل أنت صاحب القرار أم تنسق مع أحد؟"
- **Min:** Direct access OR clear champion

### 2.3 N - Need
- "ما المشكلة الأساسية التي تريد حلها؟"
- "كم مرة تحدث هذه المشكلة؟"
- "ما تأثيرها على الإيراد/الوقت/السمعة؟"
- **Min:** Pain category identified + severity medium+

### 2.4 T - Timing
- "متى تريد البدء؟"
- "ما الموعد النهائي؟"
- "هل هناك حدث/موسم/quarterly يدفع هذا؟"
- **Min:** Within 60 days

### 2.5 D - Data Readiness
- "أين تسجل leads/عملاءك؟"
- "هل تستخدم CRM؟"
- "ما البيانات المتوفرة؟"
- **Min:** Has some structure (CRM, file, even manual but recorded)

### 2.6 F - Fit
- "في أي قطاع؟"
- "كم فريق/موظف؟"
- "ما حجم العملاء؟"
- **Min:** ICP score ≥ 10 (qualified_B) or ≥ 15 (qualified_A)

### 2.7 C - Compliance
- "هل تقبل سياسة PDPL؟"
- "هل توافق على workflow الموافقة قبل الإرسال؟"
- "هل توافق على عدم الادعاءات المضمونة؟"
- **Min:** All 3 yes

---

## 3. Qualification Scoring

| Score Range | Tier | Action |
|-------------|------|--------|
| 15+ | qualified_A | active selling |
| 10-14 | qualified_B | active selling with care |
| 6-9 | nurture | long-term follow-up |
| 0-5 | disqualify | refer out or archive |

**Scoring weights:**
- Budget fit: 0-3
- Authority access: 0-3
- Need severity: 0-3
- Timing urgency: 0-2
- Data readiness: 0-2
- ICP fit: 0-5 (pre-computed)
- Compliance: 0-2

---

## 4. Disqualification Triggers

### 4.1 Hard Disqualify (no override)
- ❌ Spam/guarantee request
- ❌ No budget (< 5K)
- ❌ Refuses PDPL
- ❌ Refuses approval workflow
- ❌ Wants illegal scraping
- ❌ Abusive behavior

### 4.2 Soft Disqualify (founder override)
- ⚠️ No decision maker (but champion)
- ⚠️ Bad timing (not within 60 days)
- ⚠️ Some compliance concerns
- ⚠️ Marginal ICP fit (score 8-9)

### 4.3 Re-qualify Later
- 3-6 months: timing changes
- New decision maker
- New budget cycle
- Trigger event

---

## 5. Qualification by Source

### 5.1 Inbound (demo request, pricing)
- Higher intent (already engaged)
- But still need qualification
- Faster path to qualified

### 5.2 Warm Email (after interest)
- Medium intent
- Need discovery for qualification
- Personal context helps

### 5.3 Partner Referral
- High intent
- Pre-qualified by partner
- But verify before assumption

### 5.4 Cold Outreach
- Low intent
- Heavy qualification needed
- High disqualify rate expected

### 5.5 Content / Inbound SEO
- Variable intent
- Heavy qualification
- Often nurture, not qualified

---

## 6. Qualification Output Format

```yaml
- qualification_id: "qual_001"
- opportunity_id: "opp_001"
- score: 15
- tier: qualified_A
- budget: { confirmed: true, range_sar: 15000, source: "explicit" }
- authority: { confirmed: true, dm_accessible: true, dm_name: "Ahmed" }
- need: { category: "lead_leakage", severity: "high", evidence: "..." }
- timing: { urgency: "30_days", reason: "campaign_starting" }
- data_readiness: { crm: "HubSpot", structured: true, accessible: true }
- fit: { icp_segment: "marketing_agency", score: 17, fit: "strong" }
- compliance: { pdpl: true, approval_workflow: true, no_guarantee: true }
- next_action: "schedule_discovery"
- next_action_due: "2026-06-10"
- founder_approved: true
- approved_at: "2026-06-03"
```

---

## 7. Common Failure Modes

### 7.1 Skipping Qualification
- ❌ "They look good" → no discovery
- ❌ Result: wasted time on bad fit
- ✅ Always qualify before discovery

### 7.2 Over-qualifying
- ❌ 3 calls before proposal
- ❌ Result: slow, lose to faster competitor
- ✅ 1 discovery call max

### 7.3 Wrong Questions
- ❌ Asking about features before pain
- ❌ Result: no real qualification
- ✅ Pain first, then fit

### 7.4 Ignoring Red Flags
- ❌ "They'll figure it out"
- ❌ Result: bad client, wasted time
- ✅ Trust your gut, disqualify early

---

## 8. Re-qualification Triggers

- New pain surfaces
- Decision maker changes
- Budget cycle changes
- New requirements
- Long time in pipeline (> 60 days)

---

## 9. Companion Files

- ICP: `ICP_MATRIX_AR.md`
- Process: `SALES_PROCESS_AR.md`
- Pipeline: `PIPELINE_STAGES_AR.md`
- Discovery: `DISCOVERY_PROCESS_AR.md`
- Disqualification: `DISQUALIFICATION_RULES_AR.md`
- Data: `data/commercial/opportunities.jsonl`
- Schema: `schemas/opportunity.schema.json`

---

**Qualification = الفلتر. كل lead مؤهل = وقت محفوظ. كل lead غير مؤهل = رفض مبكر. founder يحمي الوقت، النظام يدعم.**
