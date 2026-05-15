# Organizational Intelligence Infrastructure — بنية الذكاء المؤسسي

> **التاريخ / Date:** 2026-05-15
> **الفرع / Branch:** `claude/org-intelligence-infrastructure-287eC`
> **الغرض / Purpose:** خارطة نضج (maturity roadmap) تترجم رؤية "Dealix كبنية تشغيلية
> للمؤسسة الوكيلة" إلى ما هو **مبنيٌّ فعلًا** في المستودع، وتُسمّي الفجوات الحقيقية،
> وترتّب البناء في موجات تحترم دستور Dealix.

---

## 0. ملاحظة دستورية — Doctrine note

هذه الوثيقة **خارطة طريق، وليست ادعاء منتج**. لا شيء هنا يُعتبر قدرة جاهزة (Production)
إلا إذا كان مُسجّلًا بهذه الحالة في `dealix/registers/no_overclaim.yaml`. كل طبقة أدناه
تحمل حالة صادقة. الطبقة 10 (Self-Evolving) مُسوّرة خلف **المادة 11 من الدستور**
(لا بنية استقلالية V13/V14 جديدة قبل وجود إثبات).

This document is a **roadmap, not a product claim**. Nothing here is "Production"
unless registered as such in `no_overclaim.yaml`. Every layer carries an honest status.
Layer 10 is fenced behind **Constitution Article 11**.

> **تمييز عن الوثائق الأخرى — Distinction from existing docs.** هذه الطبقات العشر
> **ليست** نفس طبقات `docs/FULL_OPS_10_LAYER_CURRENT_REALITY.md` — تلك طبقات *تسليم
> تشغيلي* (LeadOps → Case Study). أمّا هذه فطبقات *بنية ذكاء*: كيف تفكّر المؤسسة وتُحكَم
> وتنفّذ وتتذكّر. الخريطة الكنسية للمجلدات في `docs/ARCHITECTURE_LAYER_MAP.md` تبقى
> مرجع التسمية. لا يُعاد تسمية أي مجلد قائم.

---

## 1. الفرضية الصادقة — The honest premise

الرؤية: ألّا يكون Dealix "أداة AI" بل **طبقة البنية التشغيلية للمؤسسة الوكيلة** — نظام
تشغيل، دماغ تنظيمي، طبقة حوكمة، طبقة تنفيذ، قوة عاملة رقمية، ذكاء تشغيلي واستراتيجي.

الواقع: Dealix اليوم نظام إنتاجي يقارب **202 ألف سطر Python**. آخر التزام على هذا الفرع
(`4687755` — "maturity roadmap OS layers") سلّم كودًا حقيقيًا لأجزاء كبيرة من الطبقات
2 و3 و5 و6 و7 و8. لذلك المهمة **ليست صفحة بيضاء** — بل مهمة *ربط وترتيب*: ستّ من عشر
طبقات موجودة بصيغة جزئية، والفجوات الحقيقية مركّزة في الطبقات 1 و4 و9 و10.

The task is **mapping + sequencing**, not greenfield construction. ~6 of 10 layers
already exist partially; the real gaps concentrate in Layers 1, 4, 9, 10.

---

## 2. مفتاح الحالات — Status legend

**حالة النضج (من `no_overclaim.yaml`):**

| الحالة / Status | المعنى / Meaning |
|---|---|
| `Planned` | لم يُبنَ بعد — not built yet |
| `Pilot` | مبني ومُختبَر داخليًا فقط، غير مُفعّل افتراضيًا |
| `Partial` | متاح خلف flag، ينقصه التحصين (hardening) |
| `Production` | مبني ومُختبَر بالكامل، مُفعّل افتراضيًا |

**نوع المجلد الكنسي (من `ARCHITECTURE_LAYER_MAP.md`):**

| الرمز | المعنى |
|---|---|
| **W** | Wrapper — واجهة رفيعة تستورد من مجلدات قائمة |
| **N** | Net-new — مجلد كنسي جديد كليًا |
| **E** | Existing-named — الاسم الكنسي يطابق مجلدًا قائمًا |

---

## 3. الطبقات العشر — The ten layers

كل طبقة تتبع البنية نفسها: *الرؤية* / *ما هو موجود فعلًا* / *الحالة الصادقة* /
*الفجوة الحقيقية* / *اختبار الوصول* / *الموطن الكنسي*.

---

### Layer 1 — Operating Fabric — نسيج التشغيل

- **الرؤية / Vision:** ربط الـ workflows والـ agents والموافقات والذاكرة والتنفيذ
  والحوكمة والرصد في نسيج واحد، بحيث يفهم Dealix أي حدث داخل المؤسسة.
- **What already exists:**
  - `dealix/execution/__init__.py::GovernedPipeline` — يركّب الـ Trust Plane فوق
    `AcquisitionPipeline` دون تعديلها (DecisionOutputs + policy + approvals + audit).
  - `auto_client_acquisition/workflow_os_v10/` — `state_machine.py`, `checkpoint.py`,
    `idempotency.py`, `retry_policy.py`.
  - `dealix/masters/execution_fabric_spec.md` — مواصفة النسيج التنفيذي.
- **الحالة / Status:** `Partial` — نوع المجلد: **W** (واجهة تركّب القائم).
- **الفجوة الحقيقية / The real gap:** لا يوجد **event mesh** موحّد ولا **organizational
  context engine** يجعل كل workflow يرى تلقائيًا: الشركة، العميل، التاريخ، السياسات،
  الموافقات، المخاطر، العمليات السابقة.
- **اختبار الوصول / Arrival test:** أيّ workflow جديد يقرأ سياق المؤسسة الكامل دون
  تمرير يدوي لكل حقل.
- **الموطن الكنسي / Canonical home:** يُركّب فوق `workflow_os_v10/` + `dealix/execution/`
  (لا مجلد `/platform/` جديد).

---

### Layer 2 — Digital Workforce — القوة العاملة الرقمية

- **الرؤية:** إدارة موظفين/مدراء/أقسام AI لكلٍّ منهم هوية، دور، صلاحيات، ذاكرة، ملف
  مخاطر، KPIs، نطاق عمل، حدود حوكمة.
- **What already exists:**
  - `auto_client_acquisition/agent_os/` — `agent_card.py`, `agent_registry.py`,
    `agent_lifecycle.py`, `autonomy_levels.py`, `tool_permissions.py`.
  - `auto_client_acquisition/agentic_operations_os/` — `agent_identity.py`,
    `agent_governance.py`, `agent_permissions.py`, `agent_risk_score.py`,
    `agent_lifecycle.py`, `agent_auditability_card.py`, `handoff.py`.
  - `auto_client_acquisition/agent_identity_access_os/` — `agent_identity.py`,
    `agent_access.py`, `session_control.py`, `permission_review.py`, `chain_control.py`.
  - `auto_client_acquisition/ai_workforce_v10/`.
- **الحالة / Status:** `Partial` — نوع المجلد: **E** (الأسماء كنسية أصلًا).
- **الفجوة الحقيقية:** الحلقة غير مُغلقة — لا توجد **KPIs/درجات تقييم لكل agent** ولا
  مسار **onboarding/offboarding** كامل مُقاس.
- **اختبار الوصول:** لكل agent: onboarding، lifecycle، KPIs، حوكمة، رصد، offboarding.
- **الموطن الكنسي:** `agent_os/` + `agentic_operations_os/`.

---

### Layer 3 — Agentic BPM Engine — محرك العمليات الوكيلة

- **الرؤية:** الانتقال من أتمتة المهام إلى عمليات أعمال مستقلة موجّهة بالأهداف، مع
  workflows متكيّفة لا تكسر الحوكمة.
- **What already exists:**
  - `auto_client_acquisition/workflow_os_v10/` — `diagnostic_workflow.py`,
    `service_session_workflow.py`, `proof_pack_workflow.py`, `state_machine.py`.
  - `dealix/execution/__init__.py::GovernedPipeline` — تنفيذ محكوم خطوة بخطوة.
- **الحالة / Status:** `Partial` — نوع المجلد: **E**.
- **الفجوة الحقيقية:** التوجيه **متكيّف وموجّه بالهدف** ضمن حدود الحوكمة (الـ workflows
  حاليًا ثابتة المسار في معظمها).
- **اختبار الوصول:** الـ workflows تتكيّف دون كسر الحوكمة ولا الموافقات ولا حدود الأعمال.
- **الموطن الكنسي:** `workflow_os_v10/`.

---

### Layer 4 — Organizational Memory Fabric — نسيج الذاكرة المؤسسية

- **الرؤية:** ذاكرة للعميل، للـ workflow، للتنفيذ التشغيلي، للإدارة، للحوكمة، للحوادث —
  مع نَسَب (lineage) واستشهادات (citations).
- **What already exists:**
  - `core/memory/` — `embedding_service.py`, `revenue_memory.py`.
  - `auto_client_acquisition/customer_brain/`, `auto_client_acquisition/company_brain/`.
- **الحالة / Status:** `Pilot` — نوع المجلد: **W** (واجهة تركّب `core/memory/`).
- **الفجوة الحقيقية:** لا يوجد **نسيج ذاكرة موحّد** يربط ذاكرة العميل/الـ workflow/
  الإدارة/الحوادث مع lineage + citations لكل قرار.
- **اختبار الوصول:** لأيّ قرار يمكن معرفة: لماذا؟ متى؟ بواسطة مَن؟ بناءً على أيّ بيانات؟
  وأيّ سياسة؟
- **الموطن الكنسي:** واجهة `memory_fabric` تركّب `core/memory/` + الـ brains.

---

### Layer 5 — Governed Autonomy Engine — محرك الاستقلالية المحكومة

- **الرؤية:** المشكلة ليست الاستقلالية بل الاستقلالية غير المحكومة — حوكمة وقت التشغيل،
  تسييج الأدوات، نقاط موافقة، تصعيد، قابلية عكس.
- **What already exists:**
  - `dealix/trust/` — `policy.py`, `approval.py`, `audit.py`, `tool_verification.py`.
  - `dealix/classifications/__init__.py::NEVER_AUTO_EXECUTE` + تصنيفات A/R/S.
  - `auto_client_acquisition/governance_os/`, `auto_client_acquisition/approval_center/`.
- **الحالة / Status:** `Pilot → Partial` — نوع المجلد: **W/E**.
- **الفجوة الحقيقية:** الـ policy/approval/audit ما زالت **in-memory**؛ لا سياسات
  per-tenant؛ تسييج الأدوات غير مفعّل على نداءات أدوات الـ LLM المباشرة.
- **اختبار الوصول:** أيّ action: traceable، reversible، governed، auditable، explainable.
- **الموطن الكنسي:** `dealix/trust/` + `governance_os/`.

---

### Layer 6 — Execution Dominance Engine — محرك سيادة التنفيذ

- **الرؤية:** المستقبل ليس مخرجات AI بل **تنفيذ تشغيلي**: يشغّل، ينفّذ، ينسّق، يصلح،
  يتابع، يحسّن.
- **What already exists:**
  - `dealix/execution/` — مُحاذِي الـ pipeline المحكوم.
  - `core/queue/` — طابور مهام ARQ غير المتزامن.
  - `workflow_os_v10/` — `retry_policy.py`, `checkpoint.py`, `idempotency.py`.
  - `dealix/masters/execution_fabric_spec.md`.
- **الحالة / Status:** `Partial` — نوع المجلد: **W/E**.
- **الفجوة الحقيقية:** تحصين **idempotency / recovery / compensation logic** عبر كل
  workflow (موجود جزئيًا في `workflow_os_v10/` لكن غير مُعمّم).
- **اختبار الوصول:** أيّ workflow: retryable، idempotent، recoverable، observable، governed.
- **الموطن الكنسي:** `dealix/execution/` + `workflow_os_v10/` + `core/queue/`.

---

### Layer 7 — Executive Intelligence Engine — محرك الذكاء التنفيذي

- **الرؤية:** يصبح Dealix بمثابة AI COO / Chief of Staff — رؤى تشغيلية، تحليل ROI،
  مذكّرات استراتيجية، تحليل اختناقات، تنبّؤ، تحليل مخاطر.
- **What already exists:**
  - `auto_client_acquisition/executive_command_center/`.
  - `auto_client_acquisition/board_decision_os/` — `board_memo_generator.py`,
    `board_scorecards.py`, `decision_engine.py`, `risk_decisions.py`,
    `strategic_bets.py`, `ceo_command_center.py`.
  - `auto_client_acquisition/executive_pack_v2/`.
  - `api/routers/founder_command_summary.py`.
- **الحالة / Status:** `Partial` — نوع المجلد: **E**.
- **الفجوة الحقيقية:** عمق **التنبّؤ (forecasting)** وتحليل الاختناقات والمخاطر — البنية
  موجودة لكن التحليلات وصفية أكثر منها تنبّؤية.
- **اختبار الوصول:** الإدارة تعتمد على Dealix لاتخاذ قرارات تشغيلية واستراتيجية حقيقية.
- **الموطن الكنسي:** `executive_command_center/` + `board_decision_os/`.

---

### Layer 8 — Trust & Explainability Engine — محرك الثقة والتفسير

- **الرؤية:** قابلية تفسير، مساءلة، قابلية عكس، قابلية تدقيق، إشراف بشري.
- **What already exists:**
  - `auto_client_acquisition/auditability_os/` — `audit_event.py`, `evidence_chain.py`,
    `policy_check_log.py`, `responsibility_attribution.py`, `audit_metrics.py`.
  - `dealix/trust/audit.py`, `dealix/contracts/audit_log.py`.
  - Evidence packs — `dealix/masters/evidence_pack_spec.md`.
- **الحالة / Status:** `Pilot → Partial` — نوع المجلد: **N/W**.
- **الفجوة الحقيقية:** سجلّ التدقيق ما زال **in-memory**؛ الـ Postgres-backed sink
  `Planned`؛ التفسير غير مُسطَّح للمستخدم النهائي.
- **اختبار الوصول:** أيّ قرار يمكن تفسيره ومراجعته.
- **الموطن الكنسي:** `auditability_os/` + `dealix/trust/`.

---

### Layer 9 — Evaluation Dominance — سيادة التقييم

- **الرؤية:** التقييم يغطّي الـ workflows والحوكمة وأثر الأعمال والتنسيق وكفاءة التشغيل —
  لا الدقّة فقط.
- **What already exists:**
  - `evals/` — 7 حزم تقييم: `lead_intelligence_eval.yaml`, `company_brain_eval.yaml`,
    `outreach_quality_eval.yaml`, `governance_eval.yaml`, `arabic_quality_eval.yaml`,
    + `personal_operator_cases.jsonl`, `revenue_os_cases.jsonl`.
  - `docs/AI_OBSERVABILITY_AND_EVALS.md`.
  - `scripts/verify_*.py` — بوابات تحقّق.
- **الحالة / Status:** `Partial` — نوع المجلد: **E**.
- **الفجوة الحقيقية:** لا توجد بوابات تقييم لـ **workflow execution / business impact**
  مفروضة في CI — الحزم الحالية معظمها جودة محتوى ودقّة.
- **اختبار الوصول:** أيّ release لا يدخل production إلا بعد اجتياز بوابات التقييم.
- **الموطن الكنسي:** `evals/` + بوابة في `.github/workflows/ci.yml`.

---

### Layer 10 — Self-Evolving Enterprise Engine — المحرك المؤسسي ذاتي التطوّر

- **الرؤية:** نظام ذكاء تنظيمي يحسّن نفسه: workflows، حوكمة، تنسيق، عمليات، تنسيق agents.
- **What already exists:**
  - `auto_client_acquisition/friction_log/` — تجميع الاحتكاك والمشكلات.
  - `auto_client_acquisition/adoption_os/` — `friction_log.py`, مراجعات التبنّي.
  - `auto_client_acquisition/proof_to_market/` — تعلّم من الإثبات.
- **الحالة / Status:** `Planned` — نوع المجلد: **N**.
- **الفجوة الحقيقية:** لا توجد **حلقات تغذية راجعة** حقيقية ولا تحسين آمن — والأهم:
  أيّ تطوّر ذاتي مُسوّر خلف **المادة 11** (لا استقلالية V13/V14 قبل وجود إثبات: دفعة،
  التزام مكتوب، جلسة تسليم، أو حدث إثبات).
- **اختبار الوصول:** النظام يحسّن workflow/حوكمة/تنسيقًا واحدًا على الأقل **مع إبقاء
  كل تغيير تحت مراجعة بشرية** (لا تعديل ذاتي مستقل).
- **الموطن الكنسي:** واجهة `self_improvement` تركّب `friction_log/` + `adoption_os/`.

---

## 4. تسلسل البناء — Build sequence

الترتيب يضع الطبقات التأسيسية ومنخفضة المخاطر أولًا، ويؤجّل الأكثر تخمينًا.

| الموجة / Wave | الطبقات / Layers | لماذا الآن / Why now |
|---|---|---|
| **A — الأساس** | 1 (Operating Fabric)، 4 (Memory Fabric) | السياق والذاكرة شرط لكل ما فوقهما؛ مخاطر دستورية منخفضة |
| **B — الحوكمة الصلبة** | 5، 8 (تحصين persistence + audit sink على Postgres) | يرفع `Pilot → Partial/Production` ويُزيل ادّعاءات in-memory |
| **C — التنفيذ والقياس** | 6 (تحصين recovery/idempotency)، 9 (بوابات eval في CI) | يجعل الـ release قابلًا للحُكم عليه آليًا |
| **D — القوة العاملة والذكاء** | 2 (KPIs/lifecycle مغلق)، 3 (توجيه متكيّف)، 7 (تنبّؤ) | يُغلق الحلقات فوق أساسٍ مُحصّن |
| **E — مُسوّرة** | 10 (Self-Evolving) | لا تُفتح إلا بعد A–D **وبعد** استيفاء شرط المادة 11 |

كل موجة تُسلّم كودًا حقيقيًا + اختبارات + تسجيلًا في `no_overclaim.yaml` بالحالة
الصادقة، تمامًا كما فعل الالتزام `4687755`.

---

## 5. ما هذا ليس عليه — What this is NOT

- **ليس** ادعاءً بأن Dealix "بنية حضارية" أو نظام تشغيل للاقتصاد — هذه الوثيقة بنية
  نضج هندسية لمنتج محدّد.
- **ليس** اقتراحًا بتنفيذ مستقل يتجاوز أنماط الأفعال المسموحة في الدستور (المادة 9:
  `suggest_only`, `draft_only`, `approval_required`, `approved_manual`, `blocked`).
- **ليس** إذنًا ببناء عشرة مجلدات `/platform/` فارغة — كل طبقة تُبنى بكود حقيقي
  واختبارات قبل أن تُسجَّل كادّعاء.
- **ليس** بديلًا عن `docs/FULL_OPS_10_LAYER_CURRENT_REALITY.md` ولا
  `docs/ARCHITECTURE_LAYER_MAP.md` — بل طبقة رؤية تُكمّلهما.

---

## 6. مراجع — Cross-references

- `docs/ARCHITECTURE_LAYER_MAP.md` — الخريطة الكنسية للمجلدات + مفتاح W/N/E.
- `docs/FULL_OPS_10_LAYER_CURRENT_REALITY.md` — تدقيق طبقات التسليم التشغيلي العشر.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — المواد 3 و9 و11.
- `dealix/registers/no_overclaim.yaml` — مفتاح الحالات وانضباط الادّعاء.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` + `evals/README.md` — أساس الطبقة 9.
- `docs/COMMERCIAL_WIRING_MAP.md` — الـ 11 غير-قابلة-للتفاوض.
- `dealix/masters/execution_fabric_spec.md` — مواصفة الطبقتين 1 و6.
