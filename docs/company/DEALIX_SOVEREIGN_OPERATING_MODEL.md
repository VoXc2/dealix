# Dealix Sovereign Operating Model

**عقيدة تنفيذ CEO / CTO / COO:** تحويل الرؤية إلى **نظام شركة قابضة تشغيلية** — لا خطة عامة فحسب، بل ضمان أن كل جزء **يُنفَّذ** و**يُقاس** و**يتحسن** و**يخلق قيمة**.

**معمارية التنفيذ السيادية (كيف «تُربط» كل الطبقات عمليًا):** [`DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md`](DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md)

**التعريف:** نموذج تشغيل «سيادي» خاص بـ Dealix — مختلف عن الوكالة، وSaaS التقليدي، والاستشارات فقط. يجمع:

```text
Holding Strategy
+ Productized Services
+ AI Operating System
+ Runtime Governance
+ Proof Economy
+ Capital Ledger
+ Vertical Ventures
+ Saudi/MENA Standard
```

مراجع: [`../group/DEALIX_COMPOUND_HOLDING_DOCTRINE.md`](../group/DEALIX_COMPOUND_HOLDING_DOCTRINE.md) · [`../group/DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md`](../group/DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md) · [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md) · [`DEALIX_GRAND_STRATEGY.md`](DEALIX_GRAND_STRATEGY.md) · [`DEALIX_CONSTITUTION.md`](DEALIX_CONSTITUTION.md) · [`OPERATING_EQUATION.md`](OPERATING_EQUATION.md) · [`DEALIX_CAPITAL_MODEL.md`](DEALIX_CAPITAL_MODEL.md)

---

## 1. الهدف الأعلى

**ليس** ريبو ممتازًا فقط · **ليس** MVP فقط · **ليس** lead engine فقط.

### Dealix Group (Endgame)

**EN:** A **Saudi AI Operations Holding Company** that owns the **operating system**, **delivery method**, **proof standard**, **vertical playbooks**, **AI governance layer**, and **software platform** for transforming companies with AI.

**AR:** **شركة قابضة تشغيلية** للذكاء الاصطناعي تملك **نظام التشغيل**، **المنهجية**، **معيار الإثبات**، **playbooks القطاعية**، **طبقة الحوكمة**، و**المنصة البرمجية** لتحويل الشركات بالـ AI.

---

## 2. Dealix Success Assurance System

لا نجاح بلا **Assurance**. النظام يراقب الشركة من **9 زوايا** — لكل منها metrics و**gates**.

### 2.1 Revenue Assurance

**السؤال:** هل تدخل الشركة مالًا بطريقة صحية؟

**تقيس:** project revenue · MRR · ACV · gross margin · proposal win rate · sprint-to-retainer · retainer expansion.

**إشارات خطر:** إيراد مشاريع بلا retainers · خصومات كثيرة · دفع بلا proof · هامش **< 50%** (مؤشر تحذيري).

**قواعد CEO**

```text
Revenue without margin is stress.
Revenue without proof is temporary.
Revenue without retainer path is fragile.
```

### 2.2 Delivery Assurance

**السؤال:** هل نسلّم بجودة ثابتة؟

**تقيس:** on-time · QA score · rework · scope creep · handoff · رضا عميل.

**Gates:** QA average **≥ 85** · امتياز Governance كامل حيث يُفرض على المسار · **لا** إغلاق مشروع بلا **Proof Pack**.

### 2.3 Product Assurance

**السؤال:** هل المنتج يقلل الجهد ويرفع الهامش؟

**تقيس:** خطوات يدوية متكررة · features مُعاد استخدامها · ساعات داخلية موفرة · module adoption · workflows مُنتَجة.

**قواعد**

```text
If a manual step repeats 3 times → product candidate.
If a feature is not reused → not product capital.
```

### 2.4 Governance Assurance

**السؤال:** هل النظام آمن وقابل للثقة؟

**تقيس:** PII incidents · blocked actions · approval completion · audit coverage · source attribution · policy violations.

**Gates:** **0** حوادث PII حرجة · مخرجات AI للعميل لها **QA** · إجراءات خارجية **بموافقة** صريحة.

مع توسع **الوكلاء**، تظهر مخاطر **agent sprawl** والصلاحيات والتحكم **وقت التشغيل** — يلزم **control plane**: identity/persona registry · runtime policy · kill-switch · lifecycle · audit. مرجع داخلي: [`../product/AGENT_LIFECYCLE_MANAGEMENT.md`](../product/AGENT_LIFECYCLE_MANAGEMENT.md) · [`../governance/GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md).

### 2.5 Proof Assurance

**السؤال:** هل كل تسليم يثبت قيمة؟

**تقيس:** proof packs · proof events per project · value metrics · case candidates · نتائج معتمدة من العميل.

**Gate — كل مشروع:**

```text
1 proof pack + 1 value metric + 1 recommended next step
```

### 2.6 Capital Assurance

**السؤال:** هل كل عميل يقوي Dealix؟

**تقيس:** service / product / knowledge / trust / market assets.

**Gate:**

```text
1 Trust Asset + 1 Product or Knowledge Asset + 1 Expansion Path
```

فلسفة: مشروع لا يزيد الأصول الخمسة يبيع **وقتًا** فقط — مشروع جيد يخلق proof وtemplate وfeature وplaybook أو benchmark. [`DEALIX_CAPITAL_MODEL.md`](DEALIX_CAPITAL_MODEL.md)

### 2.7 Client Assurance

**السؤال:** هل العميل مناسب للتوسع؟

**تقيس:** client health · مشاركة أصحاب القرار · موثوقية دفع · تعاون بيانات · جاهزية توسعة.

**Health Score:** 85–100 expansion-ready · 70–84 healthy · 50–69 attention · <50 risky.

### 2.8 Market Assurance

**السؤال:** هل السوق يفهم Dealix؟

**تقيس:** inbound · referrals · partner leads · تفاعل محتوى · طلبات diagnostic · اعتراضات متكررة.

**Gate:** المحتوى بلا محادثات = تعليم فقط لا growth.

### 2.9 Strategic Assurance

**السؤال:** هل Dealix تتحول **holding** لا مجرد مزود خدمة؟

**تقيس:** نضج وحدات الأعمال · نضج playbooks · جاهزية شركاء · academy · enterprise · platform.

---

## 3. النموذج الاستراتيجي الأفضل: Compound AI Operations Holding

**ليس SaaS فقط.** المعادلة:

```text
Core OS
+ Productized Services
+ Proof Ledger
+ Capital Ledger
+ Vertical Playbooks
+ Retainers
+ Partners
+ Academy
+ Ventures
= AI Operations Holding Company
```

**كيف يشتغل (10 خطوات):**

1. Core OS يشغّل كل شيء.  
2. Services = cash + تعلم.  
3. Proof Ledger = trust.  
4. Capital Ledger = أصول من التسليم.  
5. Retainers = استقرار.  
6. Product modules = تكلفة أقل.  
7. Playbooks = verticals.  
8. Partners = توزيع.  
9. Academy = معيار + سوق.  
10. Ventures = فصل الوحدات الناجحة.

**لماذا أقوى من SaaS وحده؟** SaaS يحتاج وقت طويل لاكتشاف المنتج؛ الوكالة لا تتوسع؛ الاستشارات لا تبني IP بهذا الشكل. هنا: **cash + تعلم + product + retainers + standards + ventures**.

(موازٍ للتفصيل: [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md) §11–12.)

---

## 4. هيكل الشركة القابضة (منطق تشغيل)

```
Dealix Group
│
├─ Dealix Core OS
│  ├─ Data OS
│  ├─ Governance OS
│  ├─ LLM Gateway
│  ├─ AI Workforce Registry
│  ├─ Proof Ledger
│  ├─ Capital Ledger
│  ├─ Quality OS
│  └─ Client Workspace
│
├─ Dealix Revenue      (Diagnostic, Lead Intel, Pilot Conversion, RevOps)
├─ Dealix Operations   (Quick Win, Workflow, Monthly AI Ops)
├─ Dealix Brain        (Brain Sprint, Sales Knowledge, Monthly Brain)
├─ Dealix Support      (Support Desk, Feedback, Monthly Support AI)
├─ Dealix Governance   (Readiness, Policy, Governance Program)
├─ Dealix Data         (Readiness, Cleanup, Quality Dashboard)
├─ Dealix Academy
├─ Dealix Partners
├─ Dealix Labs
└─ Dealix Ventures
```

**تطبيق عملي:** لا حاجة لتأسيس كل كيان **قانونيًا** الآن — صمّن **الريبو**، الملفات، الـdashboards، والتقارير بهذا المنطق من البداية.

---

## 5. أفضل هيكل معماري تقني

### المبدأ

**Modular Monolith** أولًا — **لا** microservices في البداية؛ حدود واضحة **كأنك ستفصل لاحقًا**.

**لماذا؟** سرعة · تعقيد أقل · اختبار أسهل · تكلفة أقل · قابلية فصل لاحقًا.

### الطبقات (مرجع)

| الطبقة | مكونات |
| --- | --- |
| **Presentation** | Founder Command Center · Client Workspace · Delivery Workspace · Partner Portal · Admin |
| **Application** | Data · Revenue · Operations · Brain · Support · Governance · Reporting · Delivery OS |
| **AI Control** | LLM Gateway · Prompt Registry · Router · Eval · AI Run Ledger · Agent Registry · Cost Guard |
| **Governance** | Policy Engine · PII · Permission Mirroring · Approvals · Audit · Incidents · Runtime guardrails |
| **Data** | Postgres · Object storage · Vector (لاحقًا) · Event store · Metrics · Source registry |
| **Learning** | Proof · Capital · Productization Ledgers · Playbook updates · Benchmark engine |

(تفصيل: [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md) §6.)

---

## 6. تطبيق تنفيذي لكل جزء

### 6.1 Core OS

**الهدف:** النواة التي تستخدمها كل الوحدات.

**Modules مستهدفة:** `data_os/` · `governance_os/` · `llm_gateway/` · `reporting_os/` · `delivery_os/`

**قاعدة:** كل خدمة **تمر** عبر Data OS · Governance OS · Proof Pack · QA · Audit Event — **لا** خدمة خارج النواة.

### 6.2 Data OS

**يبني:** import preview · schema validation · dedupe · PII detection · data readiness score · source registry.

**Output (مرجع):**

```json
{
  "dataset_id": "DS-001",
  "records_total": 500,
  "records_valid": 420,
  "duplicates_found": 46,
  "pii_fields": ["email", "phone"],
  "data_readiness_score": 76,
  "decision": "usable_with_review",
  "required_actions": [
    "review lawful basis for phone numbers",
    "fill missing sector fields"
  ]
}
```

**نجاحه:** كل dataset مدخل له score ومخاطر ومصدر.

### 6.3 Governance OS

**يبني:** policy rules · forbidden actions · PII redaction · approval matrix · audit log · runtime check.

**Rules (أسماء):** `no_cold_whatsapp` · `no_linkedin_automation` · `no_scraping` · `no_guaranteed_claims` · `no_fake_proof` · `no_pii_in_logs` · `no_source_no_answer` · `external_action_requires_approval`

**Output (مرجع):**

```json
{
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "blocked_rules": [],
  "required_approvals": ["delivery_owner"],
  "audit_event_id": "AUD-001"
}
```

**نجاحه:** لا مخرج مواجه للعميل بلا `governance_status`.

**Runtime:** سلوك الوكلاء **غير حتمي** ويعتمد على **مسار التنفيذ**؛ الحوكمة لا تكتمل عند التصميم فقط — يلزم **وساطة وقت التشغيل** (هوية الوكيل · المسار · الفعل المقترح · حالة المؤسسة). [`GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md).

### 6.4 Revenue OS

**يبني:** ICP builder · account scoring · pipeline · outreach draft pack · revenue report.

**Scoring (مرجع):**

```text
final_score =
  fit_score * 0.30
+ urgency_score * 0.20
+ value_score * 0.20
+ data_quality_score * 0.15
+ compliance_score * 0.15
```

**Output (مرجع):**

```json
{
  "account_id": "ACC-001",
  "company_name": "Example Co",
  "final_score": 84,
  "reasons_ar": [
    "القطاع مناسب للعرض",
    "المدينة ضمن أولوية الإطلاق",
    "البيانات كافية للتأهيل الأولي"
  ],
  "risks": ["لا يوجد decision maker مؤكد"],
  "recommended_next_action": "manual_research_then_email_draft"
}
```

**نجاحه:** بعد الـ sprint يعرف العميل أفضل الفرص وخطواتها.

### 6.5 Reporting OS

**يبني:** executive report · proof pack · value dashboard · weekly summary.

**Proof Pack:** Problem · Inputs · Work Completed · Metrics · AI Outputs · Governance · Business Value · Risks · Recommended Next Step.

**نجاحه:** كل proof **قابل للاستخدام** في البيع التالي.

### 6.6 Capital Ledger

**يبني:** سجلات service / product / knowledge / trust / market assets.

**Output (مرجع):**

```json
{
  "project_id": "PRJ-001",
  "capital_assets": [
    {"type": "Trust", "asset": "anonymized proof pack", "reusable": true},
    {"type": "Knowledge", "asset": "B2B services objections", "reusable": true}
  ]
}
```

**نجاحه:** كل مشروع يقوي الشركة لا يغنيها مؤقتًا فقط.

---

## 7. Service Readiness Gate

**كل خدمة تأخذ score** قبل البيع:

| Area | Points |
| --- | --: |
| Clear buyer | 10 |
| Clear problem | 10 |
| Clear outcome | 10 |
| Scope | 10 |
| Intake | 10 |
| Delivery checklist | 10 |
| QA | 10 |
| Product module | 15 |
| Governance | 10 |
| Upsell | 5 |

**قرار:** 85–100 Sellable · 70–84 Paid pilot · 50–69 Demo only · <50 **Do not sell**.

**قبل البيع:** buyer؟ scope؟ QA؟ proof؟ governance؟ upsell؟ — إن لا، **لا تبع**.

مرجع إضافي: [`SERVICE_READINESS_SCORE.md`](SERVICE_READINESS_SCORE.md) · [`SELLABILITY_DECISION.md`](SELLABILITY_DECISION.md).

---

## 8. Risk-Adjusted Pricing

```text
Price = Base + data complexity + governance risk + urgency
        + integration complexity + stakeholder complexity
```

**مثال Lead Intelligence:** Base e.g. SAR 12,000 · بيانات فوضوية +20% · PII حساس +30% · إلحاح +25% · تكامل = نطاق منفصل.

**لماذا؟** المشاريع الأصعب تستهلك **مخاطر ووقتًا** أكبر.

---

## 9. Productization Gate

**Feature** لا تُبنى إلا إذا:

1. تكررت **3** مرات  
2. مرتبطة **بخدمة تُباع**  
3. توفر وقتًا  
4. تقلل خطرًا  
5. قابلة للاختبار  
6. تُستخدم عبر **أكثر من عميل**  

**قرار تعبيري:** 80+ ابنِ · 60–79 template/script · <60 لا تبنِ.

**مثال:** كتابة proof report · تكرر 5 مرات · 3 ساعات · كل الخدمات · يقلل مخاطر جودة → **`proof_pack.py`**

---

## 10. CEO Command Center

**أقسام:** Group revenue · BU revenue · MRR · gross margin · delivery capacity · QA avg · governance risk · proof packs · capital assets · feature candidates · client health · partner pipeline.

**أسئلة أسبوعية:** ماذا بعنا؟ سلّمنا؟ أثبتنا؟ تعلّمنا؟ ماذا productized؟ ماذا نوقف؟ ماذا نرفع سعره؟ من جاهز لـ retainer؟

مرجع: [`DASHBOARDS_SPEC.md`](DASHBOARDS_SPEC.md) · [`FOUNDER_COMMAND_CENTER.md`](FOUNDER_COMMAND_CENTER.md).

---

## 11. Venture Graduation Gate

وحدة (مثل Revenue أو Brain) تقترب من **venture** مستقل إذا:

- إيراد واضح · **5+** عملاء · **2+** retainers  
- playbook ناضج · product module **مستخدم**  
- delivery متكرر · **owner** واضح  

**مثال:** Lead Intelligence يبيع + Monthly RevOps ثابت + Revenue OS module + B2B playbook ناضج → مرشح **Dealix Revenue OS** / وحدة تابعة.

---

## 12. Failure Modes والعلاج

| الفشل | العلاج |
| --- | --- |
| Overbuilding | لا بناء إلا بعد **3** تكرارات |
| Service chaos | scope + QA + proof + governance لكل خدمة |
| Weak proof | لا إغلاق بلا Proof Pack |
| Compliance | runtime governance + audit + redaction |
| Low margin | risk-adjusted pricing + scope control |
| Founder bottleneck | delivery OS + checklists + أدوات مُنتَجة |
| Agent sprawl | agent registry + owner + autonomy + lifecycle |

---

## 13. تطبيق في الريبو — بنية ملفات مستهدفة

**اليوم:** المرجع التنفيذي الموحد هو **هذا الملف** + [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md).  
**مستقبلًا** يمكن فصل:

```text
docs/group/           ← فهرس مجموعة (اختياري)؛ انظر docs/group/README.md
docs/company/         DEALIX_* + gates + pricing + command center
docs/architecture/    CORE_OS, MODULAR_MONOLITH, EVENT_MODEL (عند الحاجة)
docs/governance/      GOVERNANCE_RUNTIME, AGENT_REGISTRY, ...
docs/ledgers/         PROOF, CAPITAL, AI_RUN, PRODUCTIZATION
docs/services/        لكل SKU مجلد كامل
```

**بنية كود مستهدفة:**

```text
auto_client_acquisition/
  core_os/          events.py, ids.py, schemas.py  (عند إدخال event model مركزي)
  data_os/
  governance_os/
  revenue_os/
  reporting_os/
  delivery_os/
  llm_gateway/
  ai_workforce/
```

**ابدأ:** Core OS → **Revenue wedge**.

ملاحظة: وثيقة `docs/group/README.md` تشير إلى Sovereign + Holding كمدخل المجموعة.

---

## 14. Event Model

كل حركة مهمة → **event** (لـ audit · analytics · automation · proof · command center · control tower).

**أمثلة:** `project_created` · `data_uploaded` · `data_quality_scored` · `pii_detected` · `governance_checked` · `account_scored` · `draft_generated` · `approval_required` · `proof_event_created` · `report_delivered` · `capital_asset_created` · `feature_candidate_created` · `retainer_recommended`

---

## 15. تطبيق Holding — ترتيب النضج

**ابدأ:** Operating model داخل الريبو + traction.  
**ثم:** فصل منطقي/تجاري لـ Revenue · Brain · Governance إلخ.

```text
Service Line → Business Unit → Product Module → Retainer Line
→ Venture Candidate → Brand/Subsidiary منفصلة
```

---

## 16. Endgame — Dealix Group

- **Dealix Cloud** — platform  
- **Dealix Services** — cash + learning  
- **Dealix Academy** — تدريب + سلطة  
- **Dealix Partners** — توزيع  
- **Dealix Labs** — تجارب  
- **Dealix Ventures** — أعمال vertical  
- **Dealix Standards** — امتلاك الفئة  

**المركب:** Services تغذي Cloud · Cloud يحسن Services · Proof يغذي Sales · Academy تدرب Partners · Partners يغذون Services · Labs تخلق Ventures · Ventures تستخدم Core OS · Standards تخلق الفئة.

---

## 17. أقوى Execution Rule — 7 مخرجات لكل مشروع

كل مشروع Dealix «كامل» يخرج:

1. **Revenue** (مع إطار هامش/تسعير سليم)  
2. **Proof Pack**  
3. **Client Next Step**  
4. **Capital Asset**  
5. **Productization Candidate**  
6. **Playbook Update**  
7. **Governance Learning** (rule/checklist/تدريب)

بخلاف ذلك، المشروع **ناقص** مقياس Sovereign.

---

## 18. الخلاصة التنفيذية (10 خطوات آلة)

1. ابنِ Core OS.  
2. ابدأ بـ Revenue wedge.  
3. كل output يمر Governance.  
4. كل delivery يخرج Proof.  
5. كل proof يدخل Capital Ledger.  
6. كل تكرار يدخل Productization Ledger.  
7. كل خدمة تمثل مسارًا إلى Retainer.  
8. كل Retainer يدفع Product Module.  
9. كل Module يقوي Business Unit.  
10. كل Unit تعتمد Core OS.

---

## الجملة النهائية

> **Dealix تنجح إذا صارت قابضة تشغيلية تملك Core AI Operations OS، وتستخدمه لوحدات أعمال متخصصة؛ كل وحدة تبيع خدمات مُنتَجة، تنتج Proof، تحول العملاء إلى Retainers، والتكرار إلى Product، والمعرفة إلى Standards، والـ Standards إلى Academy / Partners / Ventures.**

**بأقصر صيغة:**

```text
Core OS → Productized Services → Proof → Retainers → Product Modules
→ Business Units → Holding Company
```

**هذا هو التطبيق التنفيذي الأعلى.**
