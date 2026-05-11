# الخطة الشاملة — Enterprise Playbook Generator

## الهدف
تحويل كل خدمة في Dealix إلى حزمة تنفيذية جاهزة للبيع فورًا لكل عميل:
1. Proposal
2. SOW
3. KPI Contract
4. Governance Contract

## أمر التشغيل الموحد
`python3 -m saudi_ai_provider enterprise-playbook --service <SERVICE_ID> --intake-file <INTAKE_JSON> --profile <hermes_agents|openclaw_runtime|hybrid_governed_execution> --lang ar`

## لماذا هذه الطبقة مهمة
- تربط البيع بالتسليم والقياس في ملف واحد متماسك.
- تمنع أي عرض بدون حوكمة أو KPI واضح.
- تترجم profile التقني (Hermes/OpenClaw/Hybrid) إلى مخرجات تجارية مفهومة للإدارة.

## منهج التطبيق الأفضل لكل Profile

### Hermes Agents
- الأفضل لخدمات التسليم والعمليات السريعة.
- يرفع سرعة الإنتاج وتكرار playbooks.
- KPI تركيز: cycle time / throughput / delivery velocity.

### OpenClaw Runtime
- الأفضل لخدمات الحوكمة والامتثال والضبط.
- يرفع control coverage وaudit traceability.
- KPI تركيز: policy violations / approval trace / compliance readiness.

### Hybrid Governed Execution
- الأفضل لخدمات القرار التنفيذي والإيراد والمراقبة.
- يجمع سرعة التنفيذ مع سياسات الإلزام.
- KPI تركيز: decision cycle time / ROI velocity / incident MTTR.

## خطة تشغيل 30/60/90

### أول 30 يوم
1. تطبيق generator على أهم 5 خدمات (Governance/Revenue/Customer Ops/Observability/Runtime).
2. اعتماد profile افتراضي لكل خدمة.
3. تشغيل validator تلقائيًا داخل verify pipeline.

### 31–60 يوم
1. تخصيص عقود KPI حسب segment.
2. توحيد عقود الحوكمة مع escalation matrix.
3. ربط playbook outputs بلوحة command center.

### 61–90 يوم
1. تحويل العقود إلى proposal flow تلقائي يومي للمبيعات.
2. إضافة proposal score gating قبل أي إرسال خارجي.
3. تشغيل expansion playbook تلقائي من proof + health score.

## شرط الجودة قبل الإرسال للعميل
لا يتم اعتماد أي عرض إلا إذا:
1. KPI Contract مكتمل.
2. Governance Contract مكتمل.
3. Profile مختار بوضوح.
4. Decision owner وAcceptance signer موجودين في intake.
5. sellability + compliance gates = PASS.
