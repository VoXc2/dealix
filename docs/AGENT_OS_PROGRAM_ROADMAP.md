# خارطة برنامج نظام تشغيل الوكلاء — Agent Operating System Program Roadmap

<!-- Owner: Founder | Arabic primary + English parallel -->
<!-- Branch: claude/ai-agent-os-framework-7XFhc -->

> **تحذير:** كل الأهداف أدناه أهداف تشغيلية، وليست ضمانات تجارية. القيمة التقديرية ليست قيمة مُتحقَّقة.
> **Disclaimer:** All targets below are operational goals, not commercial guarantees. Estimated value is not Verified value.

---

## 1. السياق — Context

**عربي:** هذه خارطة برنامج مدّتها 90 يومًا لبناء «نظام تشغيل الوكلاء» (Agent Operating System) داخل Dealix.
القائمة الأصلية تضم 50 مهمة في 8 أقسام. الاستكشاف أظهر أنّ Dealix منصّة ناضجة (≈1,880 ملف Python، 146 موجِّهًا،
≈425 اختبارًا، 13 سجلًّا) وأنّ نحو **70% من المهام الخمسين موجودة فعليًا** بشكلٍ ما عبر الحزم:
`agent_os`، `agent_governance`، `agent_observability`، `secure_agent_runtime_os`،
`workflow_os` / `workflow_os_v10`، `governance_os`، `revenue_memory`، و`evals`.
لا يمكن بناء الخمسين جميعها بجودة في جلسة واحدة — إنّه برنامج 90 يومًا.

كما رُصد **خلل قائم**: حزمة `auto_client_acquisition/agent_os/` كانت نسخة MVP قديمة لا تُصدِّر عقد «Wave 14F»
الذي تعتمده ثلاثة ملفات اختبار والموجِّه `api/routers/agent_os.py` وحدود الأمان في `secure_agent_runtime_os`.
هذه الجلسة **أصلحت ذلك الخلل ونفّذت القسم 1 بالكامل (المهام 1–8)** — انظر القسم 7 أدناه.

**English:** This is a 90-day program roadmap for building the Agent Operating System inside Dealix.
The source list has 50 tasks across 8 sections. Exploration showed Dealix is a mature platform
(≈1,880 Python files, 146 routers, ≈425 tests, 13 ledgers) and that **~70% of the 50 tasks already
exist** in some form. All 50 cannot be built to quality in one session — it is a 90-day program.
A confirmed regression in the `agent_os` package was also fixed this session, and Section 1
(tasks 1–8) was fully implemented — see Section 7.

### مفتاح الحالة — Status key
- ✅ **مكتمل / Done** — موجود ومُختبَر، أو نُفِّذ في هذه الجلسة.
- 🟡 **جزئي / Partial** — أساس موجود، يحتاج توسعة أو ربطًا.
- 🔴 **فجوة / Gap** — غير موجود، يحتاج بناءً جديدًا.

### الأولويات — Priorities
**P0** = المرحلة 1 (أيام 1–30) · **P1** = المرحلة 2 (أيام 31–60) · **P2** = المرحلة 3 (أيام 61–90).

---

## 2. ملخّص الحالة — Status Summary

| القسم — Section | ✅ | 🟡 | 🔴 |
|---|---|---|---|
| 1 — Agent OS (1–8) | 8 (نُفِّذ الآن) | 0 | 0 |
| 2 — Workflow Orchestration (9–16) | 4 | 2 | 2 |
| 3 — Organizational Memory Fabric (17–23) | 2 | 4 | 1 |
| 4 — Governance OS (24–30) | 2 | 4 | 1 |
| 5 — Execution Infrastructure (31–36) | 3 | 2 | 1 |
| 6 — Evals + Observability (37–42) | 2 | 3 | 1 |
| 7 — Executive Intelligence (43–47) | 1 | 3 | 1 |
| 8 — Digital Workforce (48–50) | 0 | 1 | 2 |
| **الإجمالي — Total** | **22** | **19** | **9** |

---

## 3. الجدول الكامل للمهام الخمسين — Full 50-Task Table

العمود `Module` يشير إلى الحزمة/الملف القائم أو المقترح. العمود `Team` هو الفريق المالك.

### القسم 1 — نظام تشغيل الوكلاء — Agent Operating System (1–8) — **نُفِّذ الآن / Done this session**

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 1 | سجل الوكلاء الموحّد (ID, role, scope, risk) — Unified agent registry | ✅ | `agent_os/agent_card.py`, `agent_registry.py` | Engineering | 100% من الوكلاء يملكون بطاقة هوية | تمّ | P0 |
| 2 | مصفوفة الأدوار والصلاحيات — Role & permission matrix | ✅ | `agent_os/agent_permissions.py` | Governance | 0 إجراء خارج المصفوفة | تمّ | P0 |
| 3 | دورة حياة الوكيل — Agent lifecycle | ✅ | `agent_os/agent_lifecycle.py` | Engineering | كل انتقال حالة مُسجَّل | تمّ | P0 |
| 4 | مخطط الأهداف/الـKPI — Goal/KPI schema | ✅ | `agent_os/agent_kpi.py` | Product | كل وكيل له output + impact metric | تمّ | P0 |
| 5 | عقد ذاكرة الوكيل — Agent memory contract | ✅ | `agent_os/agent_memory_contract.py` | Governance | 0 تخزين PII بلا أساس قانوني | تمّ | P0 |
| 6 | قواعد التصعيد للمشرف البشري — Escalation rules | ✅ | `agent_os/agent_escalation.py` | Governance | كل حالة عالية المخاطر تُصعَّد | تمّ | P0 |
| 7 | بروتوكول التسليم بين الوكلاء — Agent-to-agent handoff | ✅ | `agent_os/agent_handoff.py` | Engineering | 0 تسليم بلا دليل | تمّ | P0 |
| 8 | لوحة أداء الوكلاء — Agent performance dashboard | ✅ | `agent_os/agent_performance.py` | Product | جودة/زمن/تكلفة/امتثال لكل وكيل | تمّ | P0 |

### القسم 2 — تنسيق سير العمل — Workflow Orchestration (9–16)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 9 | نموذج سير عمل معياري — Canonical workflow model | ✅ | `workflow_os/workflow_model.py`, `workflow_os_v10/` | Engineering | كل سير عمل ضمن النموذج | تمّ | P0 |
| 10 | موجِّه سير العمل — Workflow router | 🟡 | `workflow_os/workflow_mapper.py` | Engineering | اختيار المسار حسب الحدث+السياسة | 4 أيام | P1 |
| 11 | محرّك توجيه الموافقات — Approval routing engine | ✅ | `governance_os/approval_matrix.py`, `approval_center/` | Governance | توجيه متعدّد المستويات يعمل | تمّ | P0 |
| 12 | أنماط الإعادة والتعافي — Retry & recovery | ✅ | `workflow_os_v10/retry_policy.py`, `idempotency.py` | Engineering | idempotency + backoff فعّالان | تمّ | P0 |
| 13 | نقاط تدخّل بشري — Human-in-the-loop checkpoints | ✅ | `workflow_os_v10/checkpoint.py` | Governance | العمليات الحرجة تحوي نقطة تدخّل | تمّ | P0 |
| 14 | سياسات SLA لكل سير عمل — SLA policies | 🟡 | `workflow_os/workflow_metrics.py` | Product | زمن/جودة/تكلفة معرّفة لكل سير | 3 أيام | P1 |
| 15 | إصدارات سير العمل + التراجع — Versioning + rollback | 🔴 | جديد — `workflow_os/versioning.py` | Engineering | تراجع واضح لكل إصدار | 5 أيام | P1 |
| 16 | وضع المحاكاة — Simulation mode | 🔴 | جديد — `workflow_os/simulation.py` | Engineering | محاكاة قبل التشغيل الفعلي | 5 أيام | P1 |

### القسم 3 — نسيج الذاكرة المؤسسية — Organizational Memory Fabric (17–23)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 17 | توحيد نطاقات الذاكرة — Memory domains | 🟡 | `revenue_memory/`, `docs/ledgers/` | AI | 4 نطاقات موحّدة | 4 أيام | P1 |
| 18 | كتابة ذاكرة مبنية على دليل — Evidence-first writes | ✅ | `dealix/contracts/schemas/evidence_pack.schema.json` | Governance | 0 كتابة بلا مصدر | تمّ | P1 |
| 19 | مخطط سجل القرارات — Decision log schema | ✅ | `docs/ledgers/DECISION_LEDGER.md`, `audit_entry.schema.json` | Governance | كل قرار: لماذا/مَن/متى/مخاطر | تمّ | P1 |
| 20 | تقييم جودة الذاكرة — Memory quality scoring | 🔴 | جديد — `revenue_memory/quality.py` | AI | حداثة/ثقة/اكتمال لكل سجل | 4 أيام | P1 |
| 21 | حوكمة الوصول للذاكرة — Memory access governance | 🟡 | `governance_os/policy_check.py` | Governance | وصول حسب الحساسية | 3 أيام | P1 |
| 22 | طبقة استرجاع عبر سير العمل — Cross-workflow retrieval | 🟡 | `revenue_memory/projections.py` | AI | استدعاء الخبرة المؤسسية | 5 أيام | P2 |
| 23 | إزالة التكرار وحلّ التعارض — De-dup + conflict resolution | 🟡 | `data_os/dedupe.py` | AI | 0 تعارض غير محلول | 5 أيام | P2 |

### القسم 4 — نظام الحوكمة — Governance OS (24–30)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 24 | محرّك السياسات v1 — Policy engine v1 | ✅ | `governance_os/policy_check.py`, `policy_registry.py` | Governance | قواعد عمل + امتثال تعمل | تمّ | P0 |
| 25 | محرّك المخاطر — Risk engine | 🟡 | `audit_entry.schema.json` (R/S classes), `risk_resilience_os/` | Governance | تصنيف low/med/high لكل عملية | 4 أيام | P0 |
| 26 | مسار تدقيق شامل — Audit trail end-to-end | ✅ | `auditability_os/`, `db/models.py:AuditLog` | Governance | كل إجراء وقرار مُسجَّل | تمّ | P0 |
| 27 | طبقة قابلية التفسير — Explainability layer | 🟡 | `decision_passport/` | AI | كل قرار: مدخلات+تبرير+سياسة | 5 أيام | P1 |
| 28 | قوالب بوّابات الامتثال — Compliance gate templates | 🟡 | `governance_os/rules/` (YAML) | Governance | قوالب حسب القطاع/المنطقة | 4 أيام | P1 |
| 29 | لوحة إدارة الاستثناءات — Exception management console | 🔴 | جديد — `governance_os/exception_console.py` | Product | كل استثناء مُتتبَّع ومُغلَق | 5 أيام | P2 |
| 30 | بطاقة أداء الحوكمة — Governance scorecard | 🟡 | `evals/governance_eval.yaml` | Product | بطاقة لكل عميل/قسم | 4 أيام | P2 |

### القسم 5 — بنية التنفيذ — Execution Infrastructure (31–36)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 31 | أفضل 10 موصِّلات مؤسسية — Top 10 enterprise connectors | 🟡 | `integrations/` | Engineering | 10 موصِّلات جاهزة | 8 أيام | P1 |
| 32 | طبقة تجريد الإجراءات — Action abstraction layer | 🟡 | `orchestrator/tools.py` | Engineering | تنفيذ واحد ↔ أدوات متعدّدة | 5 أيام | P1 |
| 33 | ضمانات معاملاتية — Transactional safeguards | ✅ | `governance_os/draft_gate.py`, `approval_center/` | Engineering | approve-before-write نشط | تمّ | P1 |
| 34 | خطوة تحقّق التنفيذ — Execution verification | ✅ | `dealix/trust/tool_verification.py` | Engineering | تحقّق بعد كل إجراء | تمّ | P1 |
| 35 | تدفّقات التعويض/التراجع — Compensation/undo flows | ✅ | `workflow_os_v10/`, `dealix/execution/` | Engineering | تعافٍ من الفشل الجزئي | تمّ | P1 |
| 36 | مركز قيادة العمليات — Operations command center | 🟡 | `api/routers/command_center.py` | Product | مراقبة لحظية للتنفيذ | 5 أيام | P2 |

### القسم 6 — التقييمات والرصد — Evals + Observability (37–42)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 37 | حزمة تقييم grounding/hallucination — Eval suite | ✅ | `evals/` (YAML + JSONL) | AI | تغطية تقييم للسياسات | تمّ | P1 |
| 38 | تقييمات النتائج التجارية — Business outcome evals | 🟡 | `evals/revenue_os_cases.jsonl` | AI | تحويل/زمن دورة/تسرّب | 4 أيام | P1 |
| 39 | معرّفات تتبّع موحّدة — Unified trace IDs | ✅ | `agent_observability/` (trace_id), audit correlation v14 | Engineering | trace ID عبر agents/workflows | تمّ | P0 |
| 40 | تصنيف الإخفاقات — Failure taxonomy | 🔴 | جديد — `agent_observability/failure_taxonomy.py` | AI | تصنيف موحّد للإخفاقات | 4 أيام | P2 |
| 41 | لوحة التكلفة/الزمن/الجودة — Cost-Latency-Quality dashboard | 🟡 | `agent_observability/cost.py`, `quality.py` | Product | مثلّث C-L-Q مرئي | 4 أيام | P2 |
| 42 | سيناريوهات الفريق الأحمر — Continuous red-team | 🟡 | `tests/test_v7_*`, `test_prompt_injection` | AI | اختبارات مستمرّة عالية المخاطر | 5 أيام | P2 |

### القسم 7 — الذكاء التنفيذي والتحوّل — Executive Intelligence + Transformation (43–47)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 43 | مولّد الموجز التنفيذي الأسبوعي — Executive brief generator | 🟡 | `api/routers/weekly_executive_pack` | Product | موجز أسبوعي: مخاطر/تسرّب/مكاسب | 5 أيام | P2 |
| 44 | عرض الـAI COO — AI COO view | 🟡 | `bottleneck_radar/`, `founder_dashboard` | Product | أين يتعطّل التشغيل ولماذا | 5 أيام | P2 |
| 45 | نموذج النضج المؤسسي L1–L5 — Maturity model | ✅ | `docs/client_maturity/`, maturity OS layers | Product | تصنيف L1–L5 يعمل | تمّ | P2 |
| 46 | كتيّبات التحوّل لكل وظيفة — Transformation playbooks | 🟡 | `docs/` (Sales/Ops/Support/Finance) | GTM | كتيّب لكل وظيفة | 6 أيام | P2 |
| 47 | نظام المراجعة التشغيلية الفصلية — Quarterly operating review | 🔴 | جديد — `docs/QUARTERLY_OPERATING_REVIEW.md` | GTM | مراجعة مدعومة ببيانات Dealix | 5 أيام | P2 |

### القسم 8 — القوى العاملة الرقمية والتطوّر المستمر — Digital Workforce + Continuous Evolution (48–50)

| # | المهمة — Task | الحالة | Module | Team | KPI | المدة | الأولوية |
|---|---|---|---|---|---|---|---|
| 48 | الهيكل التنظيمي الرقمي — Digital org chart | 🔴 | جديد — `agent_os/org_chart.py` | Product | أدوار AI + مشرفون بشر + مساءلة | 4 أيام | P2 |
| 49 | حلقة تدريب الوكلاء — Agent training loop | 🔴 | جديد — `agent_os/training_loop.py` | AI | تدريب من eval failures + feedback | 6 أيام | P2 |
| 50 | حلقة التحسين الذاتي — Self-optimization loop | 🟡 | `self_improvement_os/`, `self_growth_os/` | AI | رصد→اقتراح→موافقة→نشر→قياس | 6 أيام | P2 |

---

## 4. العرض حسب الفريق — By-Team View

| الفريق — Team | المهام — Tasks | مالك مقترح — Suggested Owner |
|---|---|---|
| **Product** | 4, 8, 14, 29, 30, 36, 41, 43, 44, 45, 48 | Head of Product |
| **Engineering** | 1, 3, 7, 9, 10, 12, 15, 16, 31, 32, 33, 34, 35, 39 | Lead Engineer |
| **AI** | 17, 20, 22, 23, 27, 37, 38, 40, 42, 49, 50 | AI Lead |
| **Governance** | 2, 5, 6, 11, 13, 18, 19, 21, 24, 25, 26, 28 | Governance Owner |
| **GTM** | 46, 47 | Founder / GTM |

كل مهمة تحمل KPI ومدّة وأولوية في الجدول الكامل (القسم 3). كل فريق يملك المهام المسندة إليه طوال البرنامج.

---

## 5. الجدول الزمني للمراحل — 3-Phase Schedule

| المرحلة — Phase | الأيام — Days | المهام — Tasks | الحالة — Status |
|---|---|---|---|
| **المرحلة 1 — Phase 1** | 1–30 | 1–16 + 24–27 + 39 | القسم 1 (1–8) ✅ نُفِّذ · الباقي P0/P1 |
| **المرحلة 2 — Phase 2** | 31–60 | 17–23 + 31–36 + 37–38 | P1 — مُجدوَل |
| **المرحلة 3 — Phase 3** | 61–90 | 40–50 | P2 — مُجدوَل |

---

## 6. ملاحظة التوحيد — Consolidation Note

**عربي:** طبقة الوكلاء في Dealix موزّعة حاليًا على 5 حزم متداخلة جزئيًا:
`agent_os`، `agent_governance`، `agent_observability`، `secure_agent_runtime_os`، `agent_identity_access_os`.
هذا تشظٍّ يرفع تكلفة الصيانة ويسبّب انجرافًا في العقود (كما حدث في خلل `agent_os`).
**التوصية:** اعتماد `agent_os` كعمود فقري موحّد لزمن التشغيل، وإبقاء `agent_governance` كسلطة على مستوى الأدوات.
هذا بند P1 في الخارطة — لم يُنفَّذ في هذه الجلسة لتجنّب توسّع النطاق.

**English:** The Dealix agent layer is currently spread across 5 partially-overlapping packages.
This fragmentation raises maintenance cost and causes contract drift (as seen in the `agent_os` regression).
Recommendation: make `agent_os` the canonical runtime spine and keep `agent_governance` as the
tool-level authority. This is a P1 roadmap item — not executed this session to avoid scope creep.

---

## 7. ما نُفِّذ في هذه الجلسة — Delivered This Session

تمّ تنفيذ **القسم 1 بالكامل (المهام 1–8)** كرمز إنتاجي مُختبَر، مع إصلاح خلل قائم في حزمة `agent_os`:

- إعادة بناء `auto_client_acquisition/agent_os/` لتطابق عقد «Wave 14F» الذي تعتمده الاختبارات والموجِّه.
- 5 وحدات قدرات جديدة: `agent_permissions`، `agent_kpi`، `agent_memory_contract`،
  `agent_escalation`، `agent_handoff`، إضافةً إلى `agent_performance`.
- إصلاح موجِّه `api/routers/agent_os.py` (نقاط `/kill` و`/audit`) وإضافة `GET /api/v1/agents/{id}/performance`.
- 7 ملفات اختبار جديدة + إنجاح ملف العقد `tests/test_agent_os.py`. **73 اختبارًا ناجحًا.**
- التوافق الخلفي محفوظ: حزم `secure_agent_runtime_os` تستورد بنجاح، واختبارات
  `test_wave_execution_core` و`test_agent_maturity_gates` خضراء.

**خارج النطاق (خلل قائم سابقًا):** `tests/test_secure_agent_runtime.py` (استيراد `RuntimeState`)
و`value_os/monthly_report.py` (استيراد `ValueEvent`) — انجرافات استيراد قائمة على الفرع، لا علاقة
لها بهذا التغيير، ومُوصى بإصلاحها ضمن بند توحيد منفصل.
