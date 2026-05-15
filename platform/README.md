# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## الغرض

هذا الفهرس الرئيسي للطبقات الثلاث عشرة لمنصة دياليكس للذكاء الاصطناعي للمؤسسات. كل طبقة وثيقة جاهزية، لا كود. الكود الحقيقي يعيش في الحزم المذكورة في جدول الربط أدناه؛ الوثائق تصف وتتحقق ولا تكرّر.

## القاعدة الموحّدة المكوّنة من ثمانية أجزاء

لا تُعدّ أي طبقة "مبنية" إلا إذا توافرت لها الأجزاء الثمانية، كل منها بدليل قابل للتحقق:

1. معمارية — وثيقة تشرح المكونات وحدودها ومسارات الكود الحقيقية.
2. جاهزية (readiness.md) — قائمة تحقق بدرجة ونطاق ومبرر.
3. اختبارات — مواصفة تحدد ما يثبت السلوك وما يوقف الدمج.
4. مراقبة — لوحات وتنبيهات وسجلات تكشف الفشل.
5. حوكمة — سياسات وقواعد موافقة وحدود خطورة مكتوبة.
6. تراجع — إجراء موثّق للعودة إلى آخر حالة خضراء معروفة.
7. مقاييس — مؤشرات بمصدر وحد نجاح، لا أرقام مضمونة.
8. مالك — دور مسؤول مُسمّى.

## الطبقات الثلاث عشرة — الغرض في سطر واحد

| الطبقة | الاسم | الغرض |
|---|---|---|
| 1 | الأساس | الهوية، تعدد المستأجرين، الأمن، النشر، قاعدة البيانات. |
| 2 | زمن تشغيل الوكيل | تشغيل الوكلاء داخل حدود وأذونات وحالات آمنة. |
| 3 | محرك سير العمل | تنفيذ سير العمل متعدد الخطوات مع بوابات الموافقة. |
| 4 | الذاكرة والمعرفة | ذاكرة المؤسسة والاسترجاع المستند مع عزل المستأجر. |
| 5 | الحوكمة | السياسات وقواعد الموافقة ومصفوفة الخطورة والتدقيق. |
| 6 | التنفيذ والتكاملات | الموصّلات والقنوات الخارجية تحت سياسة موافقة. |
| 7 | المراقبة | لوحات وتنبيهات وسجلات حوادث عبر المنصة. |
| 8 | التقييم | قياس جودة الوكلاء والاسترجاع وسير العمل في CI. |
| 9 | الذكاء التنفيذي | موجزات وتقارير أثر للقيادة، تقديرية حتى التحقق. |
| 10 | تسليم العميل | كتيّبات التسليم وقوالب العملاء وحزم الإثبات. |
| 11 | التحول | نموذج النضج وإعادة تصميم سير العمل وتبنيه. |
| 12 | التطور المستمر | الإصدارات والطرح المرحلي وسياسة التراجع. |
| 13 | الجاهزية والتحقق العابر للطبقات | طبقة وصفية تتحقق أن الطبقات 1–12 مبنية فعلاً. |

## جدول الربط: الطبقة ← الكود القائم

| الطبقة | الكود الحقيقي |
|---|---|
| 1 | `dealix/governance/`، `api/`، `alembic/` |
| 2 | `auto_client_acquisition/agent_os/`، `auto_client_acquisition/secure_agent_runtime_os/` |
| 3 | `auto_client_acquisition/workflow_os/`، `auto_client_acquisition/execution_os/`، `dealix/execution/` |
| 4 | `auto_client_acquisition/knowledge_os/`، `auto_client_acquisition/company_brain/`، `core/memory/` |
| 5 | `auto_client_acquisition/governance_os/`، `dealix/trust/` |
| 6 | `integrations/`، `dealix/connectors/` |
| 7 | `dealix/observability/`، `auto_client_acquisition/observability_adapters/` |
| 8 | `evals/` |
| 9 | `auto_client_acquisition/founder_v10/`، `auto_client_acquisition/executive_command_center/`، `auto_client_acquisition/value_os/` |
| 10 | `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`، `clients/_TEMPLATE/` |
| 11 | `auto_client_acquisition/enterprise_rollout_os/`، `auto_client_acquisition/vertical_os/` |
| 12 | `auto_client_acquisition/self_growth_os/` |
| 13 | `readiness/` |

عند أي تعارض بين الوثيقة والكود، الكود هو المصدر.

## الدرجة الحالية للمنصة

- **درجة المنصة: 77 من 100 — نطاق تجربة عميل (client pilot).**
- التفاصيل والحكم وقائمة الفجوات في: `readiness/ENTERPRISE_READINESS_SCORECARD.md`.

## روابط ذات صلة

- `readiness/enterprise_readiness_model.md`
- `readiness/scoring_system.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `readiness/cross_layer/`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Purpose

This is the master index of the thirteen layers of the Dealix Enterprise AI Platform. Each layer is a readiness document, not code. The real code lives in the packages named in the mapping table below; the documents describe and verify, they do not duplicate.

## The universal 8-part rule

A layer is not counted as "built" unless all eight parts exist, each with verifiable evidence:

1. architecture — a document explaining components, their boundaries, and real code paths.
2. readiness (readiness.md) — a checklist with a score, a band, and a rationale.
3. tests — a spec stating what proves the behavior and what blocks a merge.
4. observability — dashboards, alerts, and logs that surface failure.
5. governance — written policies, approval rules, and risk thresholds.
6. rollback — a documented procedure to return to the last known-green state.
7. metrics — indicators with a source and a pass threshold, never guaranteed numbers.
8. owner — a named responsible role.

## The thirteen layers — one-line purpose

| Layer | Name | Purpose |
|---|---|---|
| 1 | Foundation | Identity, multi-tenancy, security, deployment, database. |
| 2 | Agent Runtime | Runs agents inside boundaries, permissions, and safe states. |
| 3 | Workflow Engine | Executes multi-step workflows with approval gates. |
| 4 | Memory & Knowledge | Organizational memory and grounded retrieval with tenant isolation. |
| 5 | Governance | Policies, approval rules, risk matrix, and audit. |
| 6 | Execution & Integrations | Connectors and external channels under an approval policy. |
| 7 | Observability | Dashboards, alerts, and incident logs across the platform. |
| 8 | Evaluation | Measures agent, retrieval, and workflow quality in CI. |
| 9 | Executive Intelligence | Leadership briefs and impact reports, estimated until verified. |
| 10 | Client Delivery | Delivery playbooks, client templates, and proof packs. |
| 11 | Transformation | Maturity model, workflow redesign, and adoption. |
| 12 | Continuous Evolution | Versioning, staged rollout, and rollback policy. |
| 13 | Readiness & Cross-Layer Validation | A meta-layer that verifies Layers 1-12 are actually built. |

## Mapping table: Layer to existing code

| Layer | Real code |
|---|---|
| 1 | `dealix/governance/`, `api/`, `alembic/` |
| 2 | `auto_client_acquisition/agent_os/`, `auto_client_acquisition/secure_agent_runtime_os/` |
| 3 | `auto_client_acquisition/workflow_os/`, `auto_client_acquisition/execution_os/`, `dealix/execution/` |
| 4 | `auto_client_acquisition/knowledge_os/`, `auto_client_acquisition/company_brain/`, `core/memory/` |
| 5 | `auto_client_acquisition/governance_os/`, `dealix/trust/` |
| 6 | `integrations/`, `dealix/connectors/` |
| 7 | `dealix/observability/`, `auto_client_acquisition/observability_adapters/` |
| 8 | `evals/` |
| 9 | `auto_client_acquisition/founder_v10/`, `auto_client_acquisition/executive_command_center/`, `auto_client_acquisition/value_os/` |
| 10 | `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`, `clients/_TEMPLATE/` |
| 11 | `auto_client_acquisition/enterprise_rollout_os/`, `auto_client_acquisition/vertical_os/` |
| 12 | `auto_client_acquisition/self_growth_os/` |
| 13 | `readiness/` |

In any conflict between a document and the code, the code is the source.

## Current platform score

- **Platform score: 77 out of 100 — client pilot band.**
- The detail, the verdict, and the gap list are in: `readiness/ENTERPRISE_READINESS_SCORECARD.md`.

## Related links

- `readiness/enterprise_readiness_model.md`
- `readiness/scoring_system.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `readiness/cross_layer/`

Estimated value is not Verified value.
