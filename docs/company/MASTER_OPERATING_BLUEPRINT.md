# Dealix Master Operating Blueprint

الدستور التشغيلي: [`DEALIX_CONSTITUTION.md`](DEALIX_CONSTITUTION.md). المعادلة التشغيلية: [`OPERATING_EQUATION.md`](OPERATING_EQUATION.md). **عقيدة التنفيذ:** [`DEALIX_SOVEREIGN_OPERATING_MODEL.md`](DEALIX_SOVEREIGN_OPERATING_MODEL.md). **معمارية التنفيذ السيادية:** [`DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md`](DEALIX_SOVEREIGN_EXECUTION_ARCHITECTURE.md). **Grand Strategy:** [`DEALIX_GRAND_STRATEGY.md`](DEALIX_GRAND_STRATEGY.md). **Holding OS:** [`DEALIX_HOLDING_OS.md`](DEALIX_HOLDING_OS.md). الرؤية التنفيذية الموحدة (CEO/CTO/CSO): [`DEALIX_UNIFIED_EXECUTIVE_BLUEPRINT.md`](DEALIX_UNIFIED_EXECUTIVE_BLUEPRINT.md). **استراتيجية CEO/CTO v3:** [`DEALIX_CEO_CTO_MASTER_STRATEGY_V3.md`](DEALIX_CEO_CTO_MASTER_STRATEGY_V3.md).

Operating manual الكامل (طبقات Offer→Scale، كتالوج، بنية، APIs، Proof/Capital، موقع، شركاء): [`DEALIX_MASTER_OPERATING_SYSTEM.md`](DEALIX_MASTER_OPERATING_SYSTEM.md).

تنفيذي، موحّد، وجاهز للبيع والتسليم والتوسع. يجمع **رأس المال التراكمي** (خمسة أنواع) مع **بناء القدرات التشغيلية** داخل العميل، لا مخرجات لمرة واحدة.

## North Star

**Dealix هي AI Operating Partner للشركات السعودية: تحوّل البيانات والعمليات والمعرفة إلى قدرات تشغيلية قابلة للقياس، مع حوكمة، موافقات، Proof Packs، وتحسين شهري مستمر.**

ليس الهدف: وكالة AI، أو أتمتة عشوائية، أو مكشط leads، أو بوت فقط.

الهدف: **Governed AI Operations Company** — تشغيل موحّد لـ Revenue، Customer، Operations، Knowledge، Data، Governance، Reporting، وDelivery بشكل قابل للتكرار والبيع.

---

## Business lines

1. **Grow Revenue** — leads، scoring، pipeline، مسودات outreach، RevOps  
2. **Serve Customers** — inbox، مسودات ردود، دعم، SLA  
3. **Automate Operations** — workflows، تقارير، موافقات، SOPs  
4. **Build Company Brain** — معرفة، RAG، إجابات بمصادر  
5. **Govern AI** — سياسات، موافقات، audit، PDPL-aware  
6. **Data & Intelligence** — جودة بيانات، dashboards، جاهزية  
7. **Managed AI Ops** — cadence شهري وتحسين مستمر  
8. **Enterprise AI OS** — فرق وworkflows متعددة مع منصة محكومة  

## Product systems (مرجع)

Strategy OS، Revenue OS، Customer OS، Marketing OS، Operations OS، Knowledge OS، Data OS، Governance OS، Delivery OS، Reporting OS، LLM Gateway، AI Workforce، Proof Ledger، Founder Command Center، Client Workspace.

## Revenue motion

`Diagnostic → Sprint → Pilot → Retainer → Enterprise → (Academy / Platform لاحقًا)`

---

## Rule: عشرة مكوّنات لكل خدمة رسمية

1. Offer واضح  
2. Scope واضح  
3. Intake  
4. Data request  
5. Delivery checklist  
6. QA checklist  
7. Product module (دعم كود/مسار)  
8. Governance rules  
9. Proof pack  
10. Upsell path  

بدونها = **beta فقط**، لا بيع رسمي.

---

## Trust OS (غير قابلة للتفاوض)

ممنوع افتراضيًا: scraping، cold WhatsApp، أتمتة LinkedIn، proof مزيف، ادعاءات ضمان، PII في سجلات حساسة، إجابة معرفية بلا مصدر عندما السياسة تتطلب مصدرًا، إرسال خارجي بلا موافقة، agent بلا مالك، مخرج موجه للعميل بلا QA.

قرارات تشغيلية: ALLOW، ALLOW_WITH_REVIEW، DRAFT_ONLY، REQUIRE_APPROVAL، REDACT، BLOCK، ESCALATE (انظر `docs/governance/RUNTIME_GOVERNANCE.md`).

---

## Delivery lifecycle

`Discover → Diagnose → Design → Build → Validate → Deliver → Prove → Expand`

لا مشروع بدون: نطاق موقّع، طلب بيانات، مقاييس نجاح، أعلام حوكمة، checklists، تعريف proof، فرضية upsell.

---

## الآلة التشغيلية (ملخص)

```text
Offer → Intake → Data → Governance → AI Output → QA → Delivery → Proof
→ Capital Asset → Upsell → Product Feature
```

كل مشروع يفترض أن ينتج: **نقد الآن**، **Proof للبيع القادم**، **معرفة للمستقبل**، **تحسين منتج للتوسع**، **ثقة للعلامة** — وسجل في [`CAPITAL_LEDGER.md`](../ledgers/CAPITAL_LEDGER.md) و[`VALUE_LEDGER.md`](../ledgers/VALUE_LEDGER.md) عند التطبيق.

---

## Technical spine (MVP)

- Frontend: Next.js، Tailwind، shadcn  
- Backend: FastAPI، Pydantic، Postgres، Redis  
- AI: LLM Gateway (موحد)، Prompt Registry، validators، cost guard، eval hooks  
- الجودة: pytest، ruff  

حزمة الكود المرجعية: `auto_client_acquisition/data_os`، `governance_os`، `revenue_os`، `reporting_os`، `delivery_os` — وواجهات API تُوسَّع تدريجيًا تحت `api/routers/`.

---

## LLM Gateway (مبدأ)

لا استدعاء LLM عشوائي من التطبيق: توجيه، ميزانية، إصدار prompt، redaction، تحقق من المخطط، fallback، cache، سجل، خطاف تقييم — انظر `docs/product/MODEL_PORTFOLIO.md` و`docs/product/PROMPT_REGISTRY.md`.

---

## AI Workforce (مبدأ)

`AI prepares → Human approves → System logs → Report proves`

بطاقات الـ agents وحدود الاستقلالية: `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`، `docs/product/agent_cards/`، `docs/governance/AUTONOMY_VALIDATION_GATES.md`.

---

## Quality OS

أوزان QA والعبور: `docs/quality/QUALITY_STANDARD_V1.md` و`docs/quality/QUALITY_STANDARD.md`.

---

## Capital & proof

أنواع إثبات القيمة والأحداث: `docs/company/VALUE_REALIZATION_SYSTEM.md`، `docs/ledgers/PROOF_LEDGER.md`، قالب موحد: `docs/templates/PROOF_PACK_TEMPLATE.md`.

---

## Sales OS (ملخص)

قمع: Target → discovery → diagnostic → proposal → sprint → review → pilot → retainer.

أول ثلاثة عروض مميزة للبيع: **Lead Intelligence Sprint**، **AI Quick Win Sprint**، **Company Brain Sprint**.

---

## Full Operating MVP — تعريف الجاهزية

عند تحقق البنود في `docs/company/NEXT_90_DAYS_EXECUTION_PLAN.md` و`SERVICE_READINESS_BOARD.md`، مع spine يعمل: `data_os` + `governance_os` + `revenue_os` + `reporting_os` + `delivery_os`، وكل مشروع ينتج proof pack ويسجل أصول رأس المال حيث ينطبق.

---

## مراجع داخلية

- قدرات: `docs/company/CAPABILITY_OPERATING_MODEL.md`، `docs/company/AI_CAPABILITY_FACTORY.md`  
- حوكمة مؤسسية: `docs/enterprise/ENTERPRISE_GOVERNANCE_LAYER.md`  
- خريطة تشغيل: `docs/product/OPERATING_SYSTEM_MAP.md`، `docs/product/DEALIX_CLOUD_VISION.md`  
- تسعير وهامش: `docs/company/MARGIN_CONTROL.md`، `docs/company/RISK_ADJUSTED_PRICING.md`  

الجملة الختامية:

**Dealix تكون قوية عندما لا تبيع «AI»، بل تبيع قدرة تشغيلية مثبتة: بيانات جاهزة، workflow واضح، AI مساعد، حوكمة وقت التشغيل، تقرير، Proof Pack، وتحسين شهري مستمر.**
