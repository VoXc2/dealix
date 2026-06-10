# Enterprise Control Plane — مستوى التحكم المؤسسي

## الغرض

جعل Dealix **جاهزة للمؤسسات الكبرى** لاحقًا: هوية، سياسات، موافقات، تدقيق، وتكلفة/مخاطر على كل إجراء ووكيل.

## المكوّنات

| مكوّن | وظيفة |
|-------|--------|
| Identity Registry | أشخاص · أدوار · مسؤوليات |
| Agent Registry | تعريف كل وكيل ومالكه |
| Policy Engine | قواعد السماح والمنع |
| Approval Engine | مسارات موافقة مرجعة البشر |
| Audit Engine | أثر قرار قابل للمراجعة |
| AI Run Ledger | تشغيل آمن وقابل للتتبع |
| Proof Ledger | ربط مخرجات بأدلة |
| Cost Guard | حدود تكلفة/استخدام |
| Risk Index | تجميع مخاطر وقت التشغيل |
| Incident Response | ردود على الحوادث |
| Kill Switch | إيقاف مسار أو أداة |

## كل وكيل (حقول مرجعية)

`agent_id` · `owner` · `purpose` · `allowed tools` · `allowed data` · `autonomy level` · `approval requirement` · `risk level` · `decommission rule`

## كل إجراء (حقول مرجعية)

`actor` · `input` · `source` · `risk` · `decision` · `approval` · `audit` · `proof impact`

**مرجع تقني في الريبو:** [`../governance/AGENT_REGISTRY.md`](../governance/AGENT_REGISTRY.md) · [`../governance/GOVERNANCE_RUNTIME.md`](../governance/GOVERNANCE_RUNTIME.md) · MI9 [arXiv:2508.03858](https://arxiv.org/abs/2508.03858).

**صعود:** [`SOVEREIGN_ENTERPRISE_ARCHITECTURE.md`](SOVEREIGN_ENTERPRISE_ARCHITECTURE.md)
