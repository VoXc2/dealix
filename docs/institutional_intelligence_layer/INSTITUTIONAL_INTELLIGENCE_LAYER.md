# Dealix Institutional Intelligence Layer — SYSTEM 56–65 / Layers 37–46

**الدستور:** [../DEALIX_MASTER_LAYERS_MAP.md](../DEALIX_MASTER_LAYERS_MAP.md) ·
**التعيين للكود:** [../enterprise_architecture/SYSTEM_MAP.md](../enterprise_architecture/SYSTEM_MAP.md)

## 1. الأطروحة (Thesis)

Dealix ينتقل من **«بنية تحتية للمؤسسة» (Enterprise Infrastructure)** إلى
**«طبقة تشغيل للمؤسسة نفسها» (Institutional Intelligence Layer)** — ليس منتجًا
ولا منصة SaaS ولا workflow engine، بل **النواة التشغيلية للمؤسسة الوكيلية**:
ذاكرة مؤسسية، control plane، governance runtime، نسيج تنسيق الوكلاء، طبقة
استدلال تنفيذي.

The future is not single AI systems but **coordinated societies of agents**;
success depends on the machinery around the model, not the model alone.

## 2. مبدأ القياس (Measurement principle)

> لا تقِس عدد الوكلاء. قِس **الاعتماد المؤسسي**.

السؤال الحقيقي: هل تعتمد المؤسسة على Dealix للتشغيل، القرار، التنسيق،
الحوكمة، التنفيذ، الذاكرة، المراقبة، والتحسين؟ إذا نعم ⇒ **Infrastructure Status**.

هذا المبدأ مُجسَّد في كود قابل للقياس: **مؤشر الاعتماد المؤسسي**
(`auto_client_acquisition/institutional_dependency_os/`، Layer 46).

## 3. ملاحظة معمارية مهمة (Architecture note)

المخطط الاستراتيجي اقترح شجرة `/platform/` جديدة بأسماء أنظمة `SYSTEM 56–65`.
**القرار:** عدم إنشاء شجرة فارغة. Dealix ليس greenfield — لديه 172 وحدة تحت
`auto_client_acquisition/` وأغلب الأنظمة العشرة موجودة فعلًا. لذلك:

- الأنظمة تُدمج كـ **طبقات 37–46** في الدستور المرقّم (Layers 00–36 → 00–46).
- لا مجلد `/platform/`؛ الوحدات تتبع عُرف `auto_client_acquisition/<name>_os/`.
- الجديد الوحيد في الكود: `institutional_dependency_os` — أداة القياس المفقودة.

## 4. جدول التعيين (SYSTEM 56–65 ↔ Layer 37–46 ↔ Packages)

| SYSTEM | Layer | الحزمة الأساسية | الحالة |
|---|---|---|---|
| 56 Control Plane | 37 | `institutional_control_os`, `orchestrator` | موجود |
| 57 Agent Society | 38 | `agent_governance`, `agentic_operations_os`, `ai_workforce` | موجود |
| 58 Assurance Contracts | 39 | `governance_os`, `secure_agent_runtime_os`, `tool_guardrail_gateway` | موجود — عقد موحّد رفيع |
| 59 Memory Fabric | 40 | `revenue_memory`, `knowledge_os` | موجود |
| 60 Org Reasoning | 41 | `intelligence_os`, `intelligence_compounding_os`, `meta_os` | موجود — causal رفيع |
| 61 Resilience/Chaos | 42 | `risk_resilience_os`, `revenue_memory` (replay) | موجود — chaos رفيع |
| 62 Meta-Governance | 43 | `meta_os`, `governance_os` | موجود — كشف تعارض رفيع |
| 63 Value Engine | 44 | `value_capture_os`, `value_os`, `proof_architecture_os` | موجود |
| 64 Learning Engine | 45 | `learning_flywheel` | موجود |
| 65 Operating Core | 46 | `institutional_dependency_os` | **جديد** |

## 5. تحليل الفجوات (Gap analysis)

موجود وقوي: control plane، agent governance، event-sourced memory، value
ledger، learning flywheel، risk register. راجع تفاصيل كل نظام في
`docs/37_*` … `docs/46_*/README.md`.

الفجوات الرفيعة (مرشّحات عمل لاحق، خارج نطاق هذا التسليم):
- **58** عقد ضمان موحّد قابل للتركيب يربط الأبعاد الخمسة لكل action.
- **60** causal reasoning وrisk propagation صريحان.
- **61** chaos testing مُمنهج وcanary trials للـ workflows.
- **62** كشف تعارض السياسات تلقائيًا ورصد approval overload.

## 6. مؤشر الاعتماد المؤسسي (Institutional Dependency Index)

الوحدة: `auto_client_acquisition/institutional_dependency_os/dependency_index.py`.

عشرة أبعاد 0–100، بُعد لكل نظام 56–65، أوزان متساوية تجمع 100:

| البُعد | النظام |
|---|---|
| `control_plane_coverage` | 56 |
| `agent_society_governed` | 57 |
| `assurance_contract_coverage` | 58 |
| `memory_fabric_traceability` | 59 |
| `org_reasoning_depth` | 60 |
| `resilience_recovery` | 61 |
| `meta_governance_improvement` | 62 |
| `value_measurability` | 63 |
| `learning_loop_active` | 64 |
| `operating_core_reliance` | 65 |

**الدوال:**
- `institutional_dependency_index(dims) -> int` — مؤشر مرجّح 0–100.
- `dependency_band(score)` — العتبات: `< 50` tool · `50–69` platform ·
  `70–84` infrastructure · `≥ 85` institutional_operating_core.
- `dependency_blockers(dims)` — أي بُعد `< 70` يُنتج blocker مُسمّى يمنع
  ادّعاء «النواة التشغيلية».

**API:** `GET /api/v1/institutional-dependency/status` ·
`POST /api/v1/institutional-dependency/index` (جسم بالأبعاد العشرة).

## 7. كيف تعرف أنك وصلت؟ (Arrival)

المؤشر ≥ 85 **وبلا blockers** ⇒ band = `institutional_operating_core`.
عندها Dealix لم يعد AI startup، بل **The Institutional Operating
Infrastructure for the Agentic Enterprise**.

## 8. الامتثال للدستور (Doctrine)

المؤشر تقييم ذاتي صادق للاعتماد، لا ادّعاء إثبات. بوابات `dependency_blockers`
وعتبات الـ band تحترم `no_fake_proof` و`no_unverified_outcomes`؛ قصّ المدخلات
عبر `_clamp_pct` يحترم `no_silent_failures`؛ والوحدة منطق قياس بحت — بلا إرسال
ولا تحصيل ولا scraping.
