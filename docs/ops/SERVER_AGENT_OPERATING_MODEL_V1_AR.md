# Dealix Server Agent Operating Model V1

## النتيجة

أضفت عقد تشغيل موحّد لوكلاء Dealix الذين يعملون عبر عقدة الـVPS الحالية. هذا ليس Agent Fleet جديدًا؛ هو طبقة ربط بين:

`OpenClaw → Hermes → LLM Router/Ollama → Agent Council → Company Brain/Graphs → Governance → existing runners → receipts`

ويغطي التسويق، الرادار، الحسابات، المبيعات، التفاوض، التشخيص، التسليم، الدعم، الشركاء، البرهان، التمويل، الأمن، الهندسة والتطوير الذاتي.

الحالة في هذا الـPR هي:

- الـManifest جاهز.
- التركيب الفعلي على السيرفر غير مدّعى.
- لم يتم restart أو install أو تغيير secret أو production.
- لا يوجد Agent runtime جديد.
- لا يوجد scheduler أو timer جديد.
- كل التأثيرات الخارجية افتراضيًا `false`.

## مصدر الحقيقة

الهيكل الجديد يستخدم ما هو موجود أصلًا:

- Company Brain كذاكرة الشركة.
- Opportunity Graph كحقيقة الفرص.
- Approval Center كمالك الموافقات.
- Proof Ledger كمالك الإثبات.
- Daily Command كواجهة الأولويات.
- Agent Council كطبقة توزيع المسؤوليات.
- Hermes/OpenClaw/LLM Router/Ollama/n8n/systemd كخدمات وعمّال/واجهات، لا كمصادر حقيقة مستقلة.

## طبقات الوكلاء

### 1. Founder Command / Executive Portfolio

يختار هدفًا أساسيًا واحدًا، يوزع الـWIP، يوقف العمل منخفض القيمة، ويعرض أقرب مسار إلى Verified Paid Pilot.

### 2. Market Radar / Account Intelligence

يبحث في السوق السعودي والخليجي والعالمي، القطاعات، المنافسين، البرامج، الفعاليات، المناقصات، الشركاء، التوظيف والتغيرات العامة. الناتج Signal وEvidence وHypothesis فقط؛ البحث لا يصبح علاقة ولا فرصة ولا موافقة.

### 3. Revenue / Diagnostic / Discovery / Negotiation

يحوّل التفاعل الحقيقي أو الـExplicit Inbound إلى مشكلة مؤهلة، ثم Diagnostic وDiscovery وProposal وNegotiation preparation. لا يرسل ولا يلتزم بسعر أو عقد أو دفع.

### 4. Brand / Content / Creative / Distribution

يبني أطروحات ثنائية اللغة، محتوى، فيديو، قوالب، UTM وchannel variants من Brand Truth وEvidence وBuyer Pain. النشر الخارجي يمر عبر Approval وchannel policy.

### 5. Lifecycle / Support / Delivery / Customer Success

يعالج inbound والردود، suppression، handoffs، دعم العملاء، جاهزية التسليم، المخاطر، القبول، والتوسع. الغموض والبيانات الحساسة والأسعار والعقود تتحول إلى Human Handoff.

### 6. Proof / Finance / Governance / Security

يمنع تضخيم الإيراد أو الإثبات، يراجع claims وconsent وpayment evidence، ويفرض kill-switches وapproval classes. هذه الطبقة Hard Gate وليست وكيلًا اختياريًا.

### 7. Engineering / SRE / Learning Factory

يبني أصغر إصلاح قابل للتحقق عند وجود فجوة مثبتة، ويفصل branch/PR عن main/production. التعلم يقيس before/after ولا يستطيع تخفيف الصلاحيات أو تغيير الحقيقة التجارية والقانونية.

## طريقة التشغيل

كل workload يمر بهذا المسار:

`Trigger → Source/Scope → Company Brain Context → Typed Handoff → Specialist Workload → Governance/Proof → Internal Action or Approval Packet → Receipt → Daily Command/Learning`

الـhandoff لا يكون رسالة حرة؛ يجب أن يحمل:

- facts / inferences / unknowns.
- evidence refs ومصدرها.
- الحالة الحالية والتالية.
- next evidence.
- authority/approval class.
- idempotency key.
- stop condition.
- الزمن والتكلفة وFounder Minutes.
- economic delta.

## توزيع الـ12 نظامًا

| النظام | lane المسؤول | cadence |
|---|---|---|
| Command OS | Executive Portfolio | daily existing runner |
| Revenue OS | Revenue Qualification | event + daily |
| Proof OS | Proof Evidence | event + weekly |
| Client OS | Delivery / Customer Success | event + daily |
| Delivery OS | Delivery / Customer Success | event |
| Support OS | Support Operations | event |
| Finance OS | Finance / Commercial Truth | event + daily |
| Data OS | Market Radar | event + daily |
| Governance OS | Governance / Security | every action |
| Academy OS | Brand / Content Strategy | daily + weekly |
| Partner OS | Partner / Market Access | event + weekly |
| Venture OS | Product Engineering | evidence-triggered |

## cadence على السيرفر

يتم ربط الهيكل بالـexisting cadence:

- Event-driven: inbound، replies، suppression، provider receipts، payment evidence، delivery evidence، proof evidence، critical health.
- Daily existing runner: portfolio priority، market radar، account read reconciliation، content queue، analytics summary، morning command.
- Weekly existing runner: experiments، proof-to-distribution، partners، competitors، cost/friction، self-improvement.

لا يضيف هذا التغيير timer جديدًا. التشغيل الدوري الحالي يبقى المالك الوحيد.

## الصلاحيات

| المستوى | ما يفعله الوكيل |
|---|---|
| L0 | مراقبة وقراءة |
| L1 | تحليل وتصنيف وترتيب |
| L2 | Drafts وpackets |
| L3 | أعمال داخلية آمنة وقابلة للعكس |
| L4 | branch/worktree/tests/commits/Draft PR |
| L5 | merge، production، DNS، secrets، payment، contract، tender، customer send، public proof — موافقة محددة |

## تحقق السيرفر

بعد وصول الكود إلى بيئة تشغيل موثوقة، شغّل من جذر المستودع:

```bash
PYTHONPATH=. python scripts/ops/verify_server_agent_operating_model_v1.py
bash scripts/ops/inspect_server_agent_runtime_v1.sh
```

الـinspection read-only. قد ينتج `PASS_OR_UNVERIFIED` إذا كانت بعض الوحدات أو المنافذ غير قابلة للتحقق؛ لا يتحول ذلك إلى قبول تشغيلي. قبول exact-head يحتاج receipt من السيرفر، SHA، timestamp، stdout، ونتيجة واضحة.

## Definition of Done

- كل نظام من الـ12 له accountable lane واحد.
- كل lane مربوط بruntime agent موجود.
- كل workload typed handoff + receipt.
- Governance hard gate.
- جميع external effects افتراضيًا false.
- لا Agent runtime جديد.
- لا scheduler جديد.
- لا ادعاء بتفعيل السيرفر قبل exact-head runtime acceptance.
- التعلم لا يرفع السلطة.
