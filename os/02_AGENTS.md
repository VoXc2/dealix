# Dealix Agents Directory

## Overview
هذا الملف يعرّف جميع AI agents في Dealix. كل agent له:
- **Purpose:** ماذا يفعل
- **Inputs:** ما يحتاجه
- **Outputs:** ما يطلع منه
- **Approval Required:** هل يحتاج موافقة بشرية

---

## Revenue Agents

### 1. Market Scanner Agent
**Purpose:** يبحث عن شركات GCC مناسبة لـ Dealix بناءً على القطاع والإشارات التشغيلية.

**Inputs:**
- قطاعات مستهدفة (من `04_MARKETS.yml`)
- معايير التأهيل (من `05_SCORING.yml`)
- استثناءات (شركات محفوظة أو مرفوضة)

**Outputs:**
- قائمة شركات مرشحة مع بيانات أساسية
- industry classification
- public signals مكتشفة

**Approval Required:** لا (بحث عام فقط)

**Quality Gate:**
- الشركة لها website واضح
- الشركة لها نشاط تشغيلي حقيقي
- الشركة لها جهة تواصل يمكن الوصول إليها

---

### 2. Company Research Agent
**Purpose:** يبني company brief كامل لكل شركة مرشحة.

**Inputs:**
- اسم الشركة وموقعها
- مصادر عامة (LinkedIn، website، news)

**Outputs:**
```json
{
  "company_name": "",
  "website": "",
  "sector": "",
  "what_they_do": "",
  "operations_complexity": "low|medium|high",
  "likely_departments": [],
  "likely_pain_points": [],
  "public_signals": [],
  "best_buyer_title": "",
  "recommended_offer": "",
  "why_this_offer_fits": "",
  "custom_email_angle": "",
  "fit_score": 0,
  "next_action": ""
}
```

**Approval Required:** لا (بحث عام فقط)

**Quality Gate:**
- لا hallucination — كل معلومة من مصدر حقيقي أو تُصنّف كـ "inferred"
- fit_score محسوب من `05_SCORING.yml`

---

### 3. Offer Router Agent
**Purpose:** يختار العرض الأنسب من كتالوج Dealix بناءً على profile الشركة.

**Inputs:**
- company brief مكتمل
- كتالوج العروض (من `03_OFFERS.yml`)
- scoring (من `05_SCORING.yml`)

**Outputs:**
- recommended_offer (اسم العرض)
- why_this_offer_fits (3–5 جمل)
- alternative_offer (إذا وجد)
- entry_price_range

**Approval Required:** لا

---

### 4. Draft Writer Agent
**Purpose:** يكتب رسالة outreach مخصصة وقوية لكل شركة.

**Inputs:**
- company brief مكتمل
- recommended offer
- custom email angle
- قواعد الكتابة (من `01_CLAUDE.md`)

**Outputs:**
- subject line
- email body (AR أو EN بحسب الشركة)
- status: "draft — awaiting founder approval"

**Approval Required:** نعم — لا تُرسل تلقائياً أبداً

**Quality Gate:**
- أقل من 150 كلمة
- يذكر اسم الشركة على الأقل مرة
- يذكر ألماً واحداً محدداً
- فيه CTA واحد فقط
- لا قائمة خدمات
- لا "نحن شركة رائدة"

---

### 5. Email Safety Agent
**Purpose:** يراجع كل draft قبل عرضه على المؤسس.

**Inputs:**
- email draft
- company brief

**Outputs:**
- safety_score (0–100)
- personalization_score (0–100)
- issues: []
- approved_for_review: true/false
- notes

**Checks:**
- [ ] personalization present
- [ ] no spam trigger words
- [ ] opt-out mechanism mentioned or not required
- [ ] no pricing shared
- [ ] no promises not backed by delivery
- [ ] tone appropriate for sector
- [ ] length within limits

**Approval Required:** لا (فحص تلقائي، يسبق عرضه على المؤسس)

---

### 6. Reply Handler Agent
**Purpose:** يصنّف ردود العملاء ويقترح الخطوة التالية.

**Inputs:**
- نص الرد
- company brief
- history

**Outputs:**
- classification: interested | details_requested | pricing_requested | credibility_needed | referral_needed | not_interested | nurture
- recommended_action
- draft_reply (إذا مناسب)
- urgency: high | medium | low

**Classification Logic:**

| الرد | التصنيف | الإجراء |
|------|---------|---------|
| مهتمين | interested | جهز call agenda |
| أرسل تفاصيل | details_requested | أرسل one-pager |
| عندنا نظام | existing_system | integration discovery |
| كم السعر؟ | pricing_requested | range + call |
| من أنتم؟ | credibility_needed | founder intro |
| ليس تخصصي | referral_needed | اطلب المناسب |
| غير مهتم | not_interested | suppression |
| لاحقًا | nurture | follow-up بعد 30 يوم |

**Approval Required:** نعم — لأي رد يُرسل خارجياً

---

## Sales Agents

### 7. Discovery Prep Agent
**Purpose:** يجهز المؤسس قبل كل discovery call.

**Inputs:**
- company brief
- reply history
- offer selected

**Outputs:**
```markdown
## Discovery Call Brief — [Company Name]
### Who We're Meeting
- Name, title, background

### What We Know
- Business model
- Operations complexity
- Key pain signals

### Hypothesis
- Likely workflow to audit
- Likely offer fit

### Questions to Ask
#### About Operations
1. كيف تبدأ العملية؟
2. من يستقبل الطلب؟
3. أين تتوقف العملية عادة؟
4. ما أكثر خطوة تتكرر يدويًا؟
5. أين تظهر الأخطاء؟

#### About Data
1. هل البيانات في Excel؟
2. هل عندكم نظام tickets؟
3. هل عندكم ERP/CRM؟
4. هل يمكن تصدير البيانات؟
5. هل عندكم sample data؟

#### About Success
1. ما النتيجة التي لو تحققت خلال 30 يوم تعتبر نجاح؟
2. هل تريدون تقليل وقت أم أخطاء أم تسريع تقارير؟

#### About Decision
1. من صاحب القرار النهائي؟
2. هل يوجد budget محدد؟
3. ما القيود الأمنية؟

### Common Objections & Responses
- "عندنا نظام" → نبحث عن integration لا استبدال
- "غالي" → ابدأ بـ audit صغير، الـ ROI واضح بعده
- "ما نثق بالـ AI" → كل قرار حساس يمر على موظفكم

### Recommended Next Step
```

**Approval Required:** لا (تحضير داخلي فقط)

---

### 8. Proposal Builder Agent
**Purpose:** يبني proposal draft بعد discovery call.

**Inputs:**
- discovery call notes
- company brief
- selected offer
- client requirements

**Outputs:** proposal كامل بهيكل محدد (انظر `15_PROPOSAL_TEMPLATE.md`)

**Approval Required:** نعم — قبل إرساله للعميل

---

## Delivery Agents

### 9. Onboarding Agent
**Purpose:** يجمع كل المعلومات اللازمة لبدء المشروع.

**Inputs:**
- signed agreement
- discovery call notes

**Outputs:**
```json
{
  "client": "",
  "project_name": "",
  "primary_contact": "",
  "decision_maker": "",
  "workflow_description": "",
  "current_tools": [],
  "available_files": [],
  "available_apis": [],
  "sample_data_status": "",
  "security_constraints": [],
  "privacy_constraints": [],
  "success_criteria": [],
  "deadline": "",
  "budget_range": "",
  "approval_process": "",
  "weekly_review_time": ""
}
```

**Approval Required:** نعم — قبل طلب أي credentials

---

### 10. Integration Intake Agent
**Purpose:** يجمع كل المعلومات التقنية للتكاملات.

**Inputs:**
- onboarding document
- list of systems

**Outputs لكل نظام:**
- API documentation link
- sandbox access status
- sample payloads
- rate limits
- authentication method
- data fields available
- known limitations

**Approval Required:** نعم — قبل طلب credentials حقيقية

---

### 11. Solution Architect Agent
**Purpose:** يصمم بنية الحل التقني.

**Inputs:**
- onboarding document
- integration data
- offer selected

**Outputs:**
- architecture diagram (text-based)
- data flow description
- agent flow
- human approval points
- MVP scope
- risks and assumptions
- estimated effort

**Approval Required:** نعم — قبل البدء في البناء

---

### 12. Build Agent
**Purpose:** ينفذ الكود المعتمد من الـ Solution Architect.

**Rules:**
- لا يبني features غير معتمدة
- يكتب tests مع كل feature
- يكتب docs مع كل module
- يفتح PR لكل change
- لا يستخدم hardcoded secrets
- يستخدم sample data فقط حتى موافقة صريحة

**Outputs:**
- code commits
- test results
- PR ready for review

**Approval Required:** نعم — كل PR قبل merge

---

### 13. QA Agent
**Purpose:** يتحقق من جودة كل تسليم قبل وصوله للعميل.

**Checks (انظر `17_QA_CHECKLIST.md` للتفاصيل):**
- [ ] build passes
- [ ] unit tests pass
- [ ] integration tests pass
- [ ] sample data test passes
- [ ] no hardcoded secrets
- [ ] permissions correct
- [ ] error handling present
- [ ] logging active
- [ ] rollback plan exists
- [ ] user guide ready
- [ ] admin guide ready
- [ ] demo script ready
- [ ] handover document ready

**Gate Rule:** لا تسليم بدون اجتياز جميع checks

**Approval Required:** نعم — المؤسس يوافق على final delivery

---

### 14. Delivery Agent
**Purpose:** يجهز حزمة التسليم النهائية للعميل.

**Outputs:**
- handover document (من `18_HANDOVER_TEMPLATE.md`)
- user training materials
- admin runbook
- demo recording script
- next phase recommendation

**Approval Required:** نعم — المؤسس يراجع قبل تسليم العميل

---

## Success Agent

### 15. Success Agent
**Purpose:** يتابع صحة المشروع بعد التسليم ويبحث عن فرص التوسعة.

**Cadence:** أسبوعي

**Outputs:**
```markdown
## Weekly Success Report — [Client] — Week [N]

### Usage This Week
- What was used?
- Frequency?
- Users?

### What Worked
- 

### What Failed / Issues
- 

### User Requests
- 

### Manual Work Still Existing
- (فرص أتمتة)

### Expansion Opportunities
- Workflow 2?
- Another department?
- Dashboard for management?
- API integration?
- Retainer support?

### Recommended Next Step
```

**Approval Required:** نعم — قبل مشاركة أي recommendation مع العميل

---

## Founder Chief of Staff Agent

### 16. Founder Chief of Staff Agent
**Purpose:** يعطي المؤسس أولوياته اليومية، تنبيهات المخاطر، pipeline الإيرادات، وأفضل الإجراءات التالية.

**Cadence:** يومي (صباح كل يوم)

**Outputs:** Founder Daily Brief (انظر `10_FOUNDER_DAILY_BRIEF.md`)

**Approval Required:** لا (تقرير داخلي)

---

## Agent Interaction Rules

1. **No Agent Sends Externally** — فقط يكتب drafts
2. **No Agent Accesses Production** — فقط sandbox/sample
3. **No Agent Commits Secrets** — فحص تلقائي قبل أي commit
4. **All External Actions Need Founder Sign-off** — لا استثناء
5. **All Agents Log Decisions** — كل قرار مسجّل
