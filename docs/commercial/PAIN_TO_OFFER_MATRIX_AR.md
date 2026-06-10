# Pain-to-Offer Matrix — مصفوفة الألم إلى العرض
**Dealix — Agent #3**

> **الغرض:** ربط كل مشكلة (pain) بالعرض (offer) المناسب. كل outbound، كل proposal، كل توصية يجب أن يحدد: pain category → offer match → confidence → evidence level → next action.

---

## 1. 10 Problem Categories (فئات المشاكل)

| # | الفئة | الوصف |
|---|-------|-------|
| 1 | **Lead leakage** | العملاء المحتملون يضيعون قبل المتابعة |
| 2 | **Follow-up chaos** | لا يوجد نظام متابعة، تواصل متقطع |
| 3 | **CRM/data disorder** | بيانات غير نظيفة، CRM مهمل |
| 4 | **Proposal delay** | العروض تتأخر، ضائعة |
| 5 | **Weak reporting** | لا رؤية واضحة للأرقام |
| 6 | **Sales team inconsistency** | الفريق بدون process، نتائج متفاوتة |
| 7 | **Support overload** | خدمة العملاء غارقة |
| 8 | **No proof/case study system** | لا دليل اجتماعي منظم |
| 9 | **Slow onboarding** | عملاء جدد يدخلون ببطء |
| 10 | **Weak renewal/upsell** | تجديد ضعيف، لا expansion |

---

## 2. Pain → Offer Mapping

### 2.1 Lead leakage
| البُعد | التفصيل |
|--------|---------|
| **Description** | leads يدخلون ولا أحد يرد، يضيعون |
| **Primary offer** | Revenue Leakage Diagnostic |
| **Secondary offer** | Follow-up Recovery Workflow |
| **Confidence** | high (direct pain, clear measurement) |
| **Evidence level** | L2-L3 (anonymized observation) |
| **ROI claim** | forbidden; use range with `is_estimate` |
| **Next action** | schedule diagnostic (7-14 day) |
| **Forbidden claims** | "we'll save all your leads" |

### 2.2 Follow-up chaos
| البُعد | التفصيل |
|--------|---------|
| **Description** | لا نظام متابعة، messages ضائعة، WhatsApp فوضوي |
| **Primary offer** | Follow-up Recovery Workflow |
| **Secondary offer** | AI Revenue Ops Starter |
| **Confidence** | high |
| **Evidence level** | L2-L3 |
| **Next action** | schedule workflow design (14-21 day) |
| **Forbidden claims** | "we'll organize everything in 1 day" |

### 2.3 CRM/data disorder
| البُعد | التفصيل |
|--------|---------|
| **Description** | CRM فوضوي، data duplicates، لا automation |
| **Primary offer** | AI Revenue Ops Starter (CRM/Funnel Cleanup) |
| **Secondary offer** | CRM/Funnel Cleanup (smaller scope) |
| **Confidence** | medium-high (technical) |
| **Evidence level** | L3 (data audit) |
| **Next action** | data audit first, then propose |
| **Forbidden claims** | "we'll fix all your data" |

### 2.4 Proposal delay
| البُعد | التفصيل |
|--------|---------|
| **Description** | العروض تتأخر، تخرج غير احترافية، تضيع |
| **Primary offer** | Proposal Factory + Proof Pack |
| **Secondary offer** | Proof Pack Factory (smaller) |
| **Confidence** | high (process improvement) |
| **Evidence level** | L2 |
| **Next action** | scope review + template build |
| **Forbidden claims** | "proposals in 1 hour" |

### 2.5 Weak reporting
| البُعد | التفصيل |
|--------|---------|
| **Description** | لا أرقام واضحة، لا visibility، قرارات بدون بيانات |
| **Primary offer** | Weekly Revenue Command (in Starter) |
| **Secondary offer** | Full Revenue OS (larger) |
| **Confidence** | medium |
| **Evidence level** | L3 |
| **Next action** | report structure proposal first |
| **Forbidden claims** | "real-time everything" |

### 2.6 Sales team inconsistency
| البُعد | التفصيل |
|--------|---------|
| **Description** | الفريق بدون process موحد، نتائج متفاوتة |
| **Primary offer** | Sales Playbook + Draft Factory |
| **Secondary offer** | AI Revenue Ops Starter |
| **Confidence** | medium |
| **Evidence level** | L2 |
| **Next action** | discovery on current process |
| **Forbidden claims** | "automate sales" |

### 2.7 Support overload
| البُعد | التفصيل |
|--------|---------|
| **Description** | فريق الدعم غارق، response time عالي، CSAT منخفض |
| **Primary offer** | Support Triage/Draft OS |
| **Secondary offer** | AI Revenue Ops Starter (with support) |
| **Confidence** | medium |
| **Evidence level** | L3 |
| **Next action** | support audit + triage design |
| **Forbidden claims** | "replace support" |

### 2.8 No proof/case study system
| البُعد | التفصيل |
|--------|---------|
| **Description** | لا proof packs، لا case studies، لا evidence |
| **Primary offer** | Proof Pack Factory |
| **Secondary offer** | Full Revenue OS |
| **Confidence** | high |
| **Evidence level** | L1-L3 (hypothetical + anonymized) |
| **Next action** | proof build sprint |
| **Forbidden claims** | "guaranteed results" |

### 2.9 Slow onboarding
| البُعد | التفصيل |
|--------|---------|
| **Description** | عملاء جدد يدخلون ببطء، activation منخفض |
| **Primary offer** | Delivery Handoff OS (in Starter) |
| **Secondary offer** | Full Revenue OS |
| **Confidence** | medium |
| **Evidence level** | L3 |
| **Next action** | onboarding audit + redesign |
| **Forbidden claims** | "onboard in 24h" |

### 2.10 Weak renewal/upsell
| البُعد | التفصيل |
|--------|---------|
| **Description** | تجديد ضعيف، لا expansion، churn |
| **Primary offer** | Renewal Engine (in Retainer) |
| **Secondary offer** | Monthly Optimization Retainer |
| **Confidence** | medium |
| **Evidence level** | L3 |
| **Next action** | renewal audit + health score |
| **Forbidden claims** | "renewal guaranteed" |

---

## 3. Pain Combinations (التراكب)

أحياناً العميل عنده 2-3 مشاكل. كيف نطابق؟

### 3.1 Lead leakage + Follow-up chaos
- **Common combo** — agency + clinic + training
- **Primary offer** Follow-up Recovery Workflow
- **Rationale** الألمين متلازمين — follow-up يحل leakage

### 3.2 CRM disorder + Weak reporting
- **Common combo** — local SaaS + education
- **Primary offer** AI Revenue Ops Starter
- **Rationale** الـ data والـ reporting متلازمين

### 3.3 Proposal delay + No proof
- **Common combo** — agency + professional services
- **Primary offer** Proposal Factory + Proof Pack
- **Rationale** العروض تحتاج proof

### 3.4 Sales inconsistency + Weak renewal
- **Common combo** — local SaaS
- **Primary offer** AI RevOps Starter + Retainer
- **Rationale** Sales ops + customer success = package

### 3.5 Support overload + Slow onboarding
- **Common combo** — education + recruitment
- **Primary offer** Full Revenue OS
- **Rationale** Customer lifecycle coverage

---

## 4. Confidence Scoring

| Confidence | Definition | Use Case |
|------------|-----------|----------|
| **High** | Direct, measurable, clear ROI signal | lead leakage, follow-up chaos, no proof |
| **Medium-high** | Measurable but requires discovery | CRM disorder, sales inconsistency |
| **Medium** | Less direct, requires research | support overload, weak reporting |
| **Low** | Speculative, needs deep discovery | (avoid) |

**القاعدة:** لا proposal بـ confidence low. ارفع discovery أولاً.

---

## 5. Evidence Level Requirements

| Pain | Min Evidence | Why |
|------|--------------|-----|
| Lead leakage | L2 | anonymized observation ok |
| Follow-up chaos | L2 | industry pattern |
| CRM disorder | L3 | needs data audit |
| Proposal delay | L2 | process observation |
| Weak reporting | L3 | metrics analysis |
| Sales inconsistency | L2 | observation |
| Support overload | L3 | metrics |
| No proof | L1-L3 | can be hypothetical |
| Slow onboarding | L3 | metrics |
| Weak renewal | L3 | cohort analysis |

**L0 (no source)** = always forbidden.

---

## 6. Anti-Patterns (مطابقات خاطئة شائعة)

### 6.1 ❌ Pain Mismatch
- ادّعاء leakage بدون بيانات
- ادّعاء CRM disorder بدون audit
- ❌ السببية بدون دليل

### 6.2 ❌ Overclaiming
- "we'll 10x your revenue"
- "guaranteed 50% conversion"
- "all your problems solved"

### 6.3 ❌ Under-diagnosis
- عرض صغير على ألم كبير
- عرض كبير على ألم صغير
- ❌ لا match بين scope و pain

### 6.4 ❌ Wrong Persona Match
- عرض "بروف" لـ "أبسط"
- عرض "تشخيص" لـ "موجود"

---

## 7. The Matching Algorithm (How to Match)

```
Input: pain signal from lead/discovery
   ↓
Step 1: Identify pain category (from 10 categories)
   ↓
Step 2: Check pain confidence (high/medium/low)
   ↓
Step 3: Match primary offer (from mapping)
   ↓
Step 4: Check combinations (any 2nd pain?)
   ↓
Step 5: Adjust offer if combo
   ↓
Step 6: Verify evidence level available
   ↓
Step 7: Check ICP fit
   ↓
Output: recommended offer + confidence + evidence + next action
```

---

## 8. Required Output Format

كل outbound / proposal / recommendation يجب أن يحتوي:

```yaml
- pain_category: "follow_up_chaos"
- offer_match: "follow_up_recovery_workflow"
- confidence: "high"
- evidence_level: "L2"
- evidence_source: "agency_observation_aggregated"
- next_action: "schedule_workflow_design_call"
- is_estimate: true
- founder_approval_required: false
- warnings: []
```

---

## 9. Companion Files

- Schema: `schemas/pain_signal.schema.json`
- Schema: `schemas/offer_match.schema.json`
- Data: `data/commercial/pain_to_offer.yaml`
- Categories: `PROBLEM_CATEGORY_MAP_AR.md`
- Rules: `OFFER_MATCHING_RULES_AR.md`
- Report: `reports/commercial/OFFER_MATCH_REVIEW.md`

---

**كل pain → offer match يجب أن يكون قابلاً للتفسير، مدعوماً بأدلة، ومرتبط بـ next action ملموس. لا حدس.**
