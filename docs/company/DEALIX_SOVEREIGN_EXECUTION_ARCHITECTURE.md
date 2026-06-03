# Dealix Sovereign Execution Architecture

**معمارية تنفيذ سيادية:** تربط الاستراتيجية، التقنية، التشغيل، الحوكمة، المبيعات، الـProof، ونموذج القابضة في **نظام واحد** — حتى لا تنجح Dealix بالصدفة، بل لأن عندها **هندسة نجاح**.

**الفكرة:** Dealix لا تُدار كمشروع برمجي، بل ك**آلة مركبة** — كل عميل يولّد كاش، Proof، معرفة، منتج، وثقة؛ ثم يتحول إلى Retainer أو مسار وحدة أعمال.

مراجع: [`../group/DEALIX_COMPOUND_HOLDING_DOCTRINE.md`](../group/DEALIX_COMPOUND_HOLDING_DOCTRINE.md) · [`../group/DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md`](../group/DEALIX_COMPOUND_HOLDING_OPERATING_LAYER.md) · [`DEALIX_SOVEREIGN_OPERATING_MODEL.md`](DEALIX_SOVEREIGN_OPERATING_MODEL.md) · [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md) · [`DEALIX_GRAND_STRATEGY.md`](DEALIX_GRAND_STRATEGY.md) · [`DEALIX_CONSTITUTION.md`](DEALIX_CONSTITUTION.md)

---

## 1. مبدأ النجاح الأعلى

**أقوى ضمان:** بناء **نظام قياس** قبل أو مع **نظام التنفيذ**.

لا تسأل فقط: «هل بنينا الميزة؟»  
اسأل:

```text
هل زادت المبيعات؟ هل قلّ وقت التسليم؟ هل رفعت الثقة؟ هل خفّضت المخاطر؟
هل فتحت Retainer؟ هل أصبحت reusable؟
```

**سياق السوق:** كثير من المؤسسات تجاوزت مرحلة «هل نستخدم AI؟» إلى «كيف **ننفّذ** AI بحوكمة وقيمة وتشغيل؟» — الفجوة بين التبني والأثر المؤسسي والتوسع الآمن تظل واسعة في مسوح مثل [McKinsey — The state of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai). Dealix تصمَّم لتغلق هذه الفجوة **في العمل والتشغيل وليس في الشعار فقط**.

---

## 2. Dealix Success Pyramid

```
                 Category Leadership
                        ▲
                  Holding Company
                        ▲
                Platform + Standards
                        ▲
              Retainers + Proof Engine
                        ▲
             Productized Services
                        ▲
               Core Operating OS
                        ▲
                  Revenue Wedge
```

**المعنى:** تبدأ من **Revenue Intelligence** (wedge) → **Core OS** → **Services** → **Proof** → **Retainers** → **Platform** → **Standards** → **Holding / category leadership**.

- تبدأ من **platform/holding** مباشرة = بناء كثير قبل السوق.  
- البقاء في **services** فقط = ميل للوكالة.  
- **الصح:** الجمع عبر **Proof + Productization**.

---

## 3. Dealix Dual Engine

### Engine 1 — Cash

Diagnostics · Sprints · Pilots · Retainers  

**هدف:** revenue · cash flow · client proof · market learning.

### Engine 2 — Compound

Core OS · Proof/Capital Ledgers · Playbooks · Product Modules · Academy · Partners · Ventures  

**هدف:** IP · moat · scale · category · هامش أعلى.

### القاعدة الذهبية

```text
كل مشروع: كاش الآن + أصل مركّب للمستقبل.
```

كاش فقط = خدمة مؤقتة. منتج فقط بلا كاش = بناء في فراغ. الاثنان = **holding**.

(يتوازى مع [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md) §11.)

---

## 4. Dealix Compound Holding (شكل بعيد المدى)

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
├─ Dealix Revenue
├─ Dealix Operations
├─ Dealix Brain
├─ Dealix Support
├─ Dealix Governance
├─ Dealix Data
├─ Dealix Academy
├─ Dealix Partners
├─ Dealix Labs
└─ Dealix Ventures
```

**تنفيذيًا:** لا حاجة لتأسيس كل كيان **قانونيًا** الآن — طبّق كـ **Operating Model** في الريبو والتقارير. كل وحدة مستقبلًا: offer · scope · product module · KPIs · proof type · owner · P&L لاحقًا.

---

## 5. Dealix Core OS — قلب يمنع الفوضى

**كل شيء يمر عبر Core OS.** مكونات مرجعية:

1. Data OS  
2. Governance OS  
3. LLM Gateway  
4. AI Run Ledger  
5. Agent Registry  
6. Proof Ledger  
7. Capital Ledger  
8. QA System  
9. Client Workspace  
10. Founder Command Center  

### قواعد غير قابلة للنقاش

```text
No business unit builds its own governance (منفصل عن السياسة الموحدة).
No agent bypasses LLM Gateway.
No service bypasses Proof Pack.
No client output bypasses QA.
```

---

## 6. المعمارية التقنية الأفضل

**ابدأ بـ Modular Monolith** — ليس microservices مبكرًا (سرعة · ضبط · اختبار · تكلفة أقل قبل الـscale).

| الطبقة | مكونات |
| --- | --- |
| **Presentation** | Founder CC · Client Workspace · Delivery · Partner Portal · Admin |
| **Application** | Data · Revenue · Operations · Brain · Support · Governance · Reporting · Delivery OS |
| **AI Control** | LLM Gateway · Prompt Registry · Router · Eval · AI Run Ledger · Agent Registry · Cost Guard |
| **Governance** | Policy Engine · PII · Approvals · Audit · Incidents · Runtime guardrails |
| **Data** | Postgres · Object storage · Vector لاحقًا · Event store · Metrics · Source registry |
| **Learning** | Proof · Capital · Productization Ledgers · Playbooks · Benchmarks |

**لماذا؟** تفصل **AI** عن **الحوكمة** عن **البيانات** عن **التسليم** عن **الـproof** عن **التعلم** — وهو ما تحتاجه المؤسسات عندما يتحول التحدي من «اختيار نموذج» إلى **تنفيذ وحوكمة وتشغيل** ([McKinsey — state of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)).

---

## 7. Runtime Governance — ميزة استراتيجية

الحوكمة **ليست PDF فقط** — **runtime**. كل مخرج AI يمر بـ:

```text
source · PII · allowed_use · claim safety · channel safety · approval · audit · proof event
```

**قرارات:** ALLOW · ALLOW_WITH_REVIEW · DRAFT_ONLY · REQUIRE_APPROVAL · REDACT · BLOCK · ESCALATE

**Shadow AI:** استخدام أدوات AI **غير موافق عليها** وغياب الرؤية يوسّع فجوة أمنية وتنظيمية؛ مسوح حديثة تبرز انتشار استخدام غير مرخص وقلق فرق IT حول إدارة المخاطر — مثال منظومي: [Protiviti — AI Pulse Survey (Shadow AI & cyber risk)](https://www.protiviti.com/gl-en/survey/ai-pulse). Dealix تموضع كطبقة **مرئية ومحكومة**.

**السعودية / PDPL:** التصميم **PDPL-aware by design**. دراسة 2026 لعينة من مواقع التجارة الإلكترونية في السعودية وجدت أن **31%** فقط أعلنت **العناصر الأربعة** التي فحصتها في سياسات الخصوصية — فجوة إفصاح/امتثال عملي: [arXiv — One Year After the PDPL](https://arxiv.org/abs/2602.18616).

تفاصيل: [`../governance/GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md).

---

## 8. Dealix AI Workforce — لا وكيل بلا هوية

كل agent = **بطاقة** (كموظف افتراضي):

`agent_id` · `owner` · `role` · `allowed_inputs` · `allowed_tools` · `forbidden_actions` · `autonomy_level` · `approval_requirement` · `output_schema` · `eval_tests` · `risk_level` · `audit_requirement`

**مستويات 0–6.** **MVP:** مسموح 0–3؛ 4 مقيّد؛ 5 enterprise؛ 6 ممنوع (خارجي تلقائي).

يحدّ **agent sprawl**. مرجع طبقات التحكم: [`../product/AGENT_LIFECYCLE_MANAGEMENT.md`](../product/AGENT_LIFECYCLE_MANAGEMENT.md) · [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md).

---

## 9. Event-Driven Operating Model

لا **CRUD** وحده — كل حدث مهم **event** لبناء: audit · proof ledger · analytics · automation · control tower · telemetry · workspace.

**أمثلة:** `project_created` · `dataset_uploaded` · `data_quality_scored` · `pii_detected` · `governance_checked` · `account_scored` · `draft_generated` · `approval_required` · `approval_granted` · `proof_event_created` · `report_delivered` · `capital_asset_created` · `feature_candidate_created` · `retainer_recommended`

```json
{
  "event_type": "governance_checked",
  "project_id": "PRJ-001",
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "created_at": "2026-05-13T12:00:00Z"
}
```

---

## 10. Success Assurance Scorecard

| Dimension | What to Measure | Healthy Signal |
| --- | --- | --- |
| Revenue | MRR، مشاريع، هامش | نمو بهامش صحي |
| Delivery | QA، on-time، rework | QA 85+ |
| Governance | حوادث، blocked، audit | 0 critical |
| Proof | packs، value metrics | كل مشروع proof |
| Product | خطوات مُنتَجة | يدوي ↓ |
| Capital | أصول/مشروع | 2+ |
| Client | health، توسعة | retainers ↑ |
| Market | inbound، referrals | leads أفضل |
| Strategy | نضج وحدات، platform pull | طلب workspace |

**قواعد تشخيص:** revenue ↑ + governance ضعيف = **خطر** · proof ↑ + retainers لا = قيمة لا تتحول لتشغيل · features ↑ + usage ضعيف = **overbuilding** · clients ↑ + capital لا = ميل للوكالة.

(يتوازى مع [`DEALIX_SOVEREIGN_OPERATING_MODEL.md`](DEALIX_SOVEREIGN_OPERATING_MODEL.md) §2.)

---

## 11. Business Unit Template

نفس القالب لكل وحدة:

```text
Name: Dealix Revenue
Problem: فرص مبيعات مبعثرة
Primary Offer: Lead Intelligence Sprint
Recurring Offer: Monthly RevOps OS
Product Module: Revenue OS
Proof Type: Revenue Proof Pack
KPIs: accounts scored · qualified opps · pipeline · sprint-to-retainer
Capital: B2B playbook · templates · scoring benchmark
```

كرر لـ Operations · Brain · Support · Governance · Data.

---

## 12. Venture Graduation Gate

**متى تصبح الوحدة venture/منتجًا مستقلًا داخل القابضة:**

- 5+ عملاء مدفوعين · 2+ retainers  
- تسليم متكرر · product module فعّال · owner · playbook **~80+** · هامش صحي · مكتبة proof  

**مثال:** Lead Intelligence يبيع + RevOps retainers + Revenue OS مستخدم + B2B playbook → **Dealix Revenue OS** كمرشح venture.

---

## 13. Strategy Map النهائي

```text
Wedge: Revenue Intelligence
Core: Governed AI Operations OS
Cash: Productized Services
Stability: Retainers
Moat: Proof + Governance + Saudi Localization + Capital Ledger
Scale: Cloud + Academy + Partners + Ventures
Endgame: Saudi/MENA AI Operations Holding Company
```

---

## 14. تطبيق في الريبو

**اليوم:** الوثائق المركزية في `docs/company/` (`DEALIX_*`) + `docs/governance/` + `docs/services/` + `docs/ledgers/` + [`docs/group/README.md`](../group/README.md).

**مستقبلًا** يمكن إضافة `docs/architecture/` (CORE_OS، MODULAR_MONOLITH، EVENT_MODEL) عند الحاجة — دون تشتيت قبل الاعتماد.

**كود مستهدف:** `auto_client_acquisition/` مع `core_os/` (events، schemas) عند تفعيل نموذج الأحداث المركزي؛ ثم `data_os` · `governance_os` · `revenue_os` · `reporting_os` · `delivery_os` · `llm_gateway` · `ai_workforce` (بما فيها `agent_registry` عند النضج).

---

## 15. Build Order — ترتيب اعتماد (بدون أيام)

1. Core schemas  
2. Event model  
3. Data OS  
4. Governance OS  
5. Revenue OS  
6. Reporting OS  
7. Delivery QA  
8. Founder Command Center  
9. Client Workspace  
10. Retainer engine  

**القاعدة:** لا خطوة قبل أن تثبت التي قبلها.

```text
لا outreach drafts قبل Governance OS.
لا Client Workspace قبل Proof Pack.
لا AI Workforce قبل LLM Gateway.
لا Enterprise قبل audit log.
```

---

## 16. أقوى Quality Gates

**Gate 1 — Service:** buyer · problem · scope · price · QA · proof · governance · upsell.  
**Gate 2 — Product:** تكرر 3+ · مرتبط إيراد · يوفر وقتًا · يقلل خطرًا · قابل اختبار · reusable.  
**Gate 3 — Governance:** source · PII · allowed_use · risk · approval · audit.  
**Gate 4 — Proof:** proof pack · value metric · next step · capital asset.  
**Gate 5 — Holding:** إيراد · تكرار · playbook · owner · proof · هامش.

(تفصيل في [`DEALIX_SOVEREIGN_OPERATING_MODEL.md`](DEALIX_SOVEREIGN_OPERATING_MODEL.md) §7–12.)

---

## 17. ما يميّز النظام المركّب (category)

**ليس الـfeature وحده** — النظام المركب:

1. Capability maturity model  
2. Productized AI operations services  
3. Runtime governance  
4. Proof economy  
5. Capital ledger  
6. Saudi/Arabic localization  
7. Holding architecture  
8. Venture graduation  
9. Academy + شركاء معتمدون  
10. **Dealix Standard** (المنهجية + المقاييس)

---

## 18. Dealix Standard — Dealix Method

**مراحل:** Diagnose → Design → Build → Govern → Validate → Deliver → Prove → Operate → Compound  

**Artifact لكل مرحلة:** diagnostic report · workflow map · AI-assisted process · policy decision · QA score · client output · proof pack · retainer cadence · capital asset  

يصبح لاحقًا Academy · Certification · Partner Program.

---

## 19. Final CEO Operating Rule

كل **قرار** يزيد **واحدًا على الأقل** من: Revenue · Proof · Trust · Product · Knowledge · Market · Retention.

كل **مشروع** يزيد **ثلاثة على الأقل**.

**مثال جيد — Lead Intelligence:** Revenue · Proof · Product · Knowledge · Retention.  
**مثال ضعيف — custom لمرة:** قد يزيد revenue فقط → **غير استراتيجي**.

---

## 20. الخلاصة النهائية

```text
Core OS أولًا
Revenue Wedge ثانيًا
Governance دائمًا
Proof في كل مشروع
Capital Ledger بعد كل تسليم
Productization بعد كل تكرار
Retainer بعد كل proof
Business Unit بعد كل playbook
Venture بعد تكرار قوي
Holding بعد نضج الوحدات
```

**النموذج:** **Dealix Compound AI Operations Holding** — قابضة تشغيلية تملك Core AI Operations OS، وحدات متخصصة، خدمات مُنتَجة، Proof، تحويل لـ Retainers، تكرار إلى Product، منتجات إلى Standards، Standards إلى Academy/Partners/Ventures.

**أقصر صيغة:**

```text
Core OS → Revenue Wedge → Productized Services → Proof Ledger → Retainers
→ Product Modules → Business Units → Academy/Partners → Holding Company
```

بهذا تصبح Dealix ليس «مشروعًا ناجحًا» فقط، بل **نظام شركة** قابل أن يصبح **category leader**.
