# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## الغرض

تشرح هذه الوثيقة نموذج جاهزية المؤسسة لمنصة دياليكس. النموذج طبقة وصفية (meta-layer) — لا ينفّذ منطقاً ولا يستبدل كوداً، بل يصف كيف نتحقق أن كل طبقة من الطبقات الثلاث عشرة "مبنية فعلاً" بدلاً من افتراض ذلك. الهدف الصريح: التوقف عن خداع النفس. طبقة موثّقة جيداً وغير مُختبَرة ليست طبقة جاهزة.

## القاعدة الموحّدة المكوّنة من ثمانية أجزاء

لا تُعدّ أي طبقة "مبنية" إلا إذا توافرت لها الأجزاء الثمانية التالية، كل منها بدليل قابل للتحقق:

1. **معمارية (architecture)** — وثيقة تشرح المكونات وحدودها ومسارات الكود الحقيقية.
2. **جاهزية (readiness.md)** — قائمة تحقق ثنائية اللغة بدرجة ونطاق ومبرر.
3. **اختبارات (tests)** — مواصفة اختبار تحدد ما الذي يثبت السلوك وما الذي يوقف الدمج.
4. **مراقبة (observability)** — لوحات وتنبيهات وسجلات تكشف الفشل عند حدوثه.
5. **حوكمة (governance)** — سياسات وقواعد موافقة وحدود خطورة مكتوبة.
6. **تراجع (rollback)** — إجراء موثّق للعودة إلى آخر حالة خضراء معروفة.
7. **مقاييس (metrics)** — مؤشرات بمصدر وحد نجاح، لا أرقام مضمونة.
8. **مالك (owner)** — شخص أو دور مسؤول مُسمّى لكل طبقة.

أي جزء ناقص يخفض درجة الطبقة ويمنعها من بلوغ نطاق "جاهز للمؤسسات".

## الطبقات الثلاث عشرة

| الطبقة | الاسم | الغرض في سطر واحد |
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
| 13 | الجاهزية والتحقق العابر للطبقات | هذه الطبقة الوصفية: تتحقق أن الطبقات 1–12 مبنية فعلاً. |

## كيف تُربط الطبقة الوصفية بالكود الحقيقي (ولا تكرّره)

الطبقة الثالثة عشرة لا تحتوي منطق تشغيل. كل مرجع يشير إلى كود قائم، لا إلى كود جديد:

- منطق الوكلاء يعيش في `auto_client_acquisition/agent_os/` و`auto_client_acquisition/secure_agent_runtime_os/` و`core/agents/`.
- منطق سير العمل يعيش في `auto_client_acquisition/workflow_os/` و`auto_client_acquisition/execution_os/` و`dealix/execution/`.
- منطق الحوكمة يعيش في `auto_client_acquisition/governance_os/` و`dealix/governance/approvals.py` و`dealix/trust/`.
- التكاملات تعيش في `integrations/` و`dealix/connectors/`.
- المراقبة تعيش في `dealix/observability/` و`auto_client_acquisition/observability_adapters/`.
- المعرفة والذاكرة تعيش في `auto_client_acquisition/knowledge_os/` و`auto_client_acquisition/company_brain/` و`core/memory/`.

الطبقة الثالثة عشرة تقرأ هذه الحقائق وتسجّل التحقق منها. إن تعارضت الوثيقة مع الكود، فالكود هو المصدر.

## روابط ذات صلة

- `readiness/scoring_system.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `platform/README.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Purpose

This document explains the enterprise readiness model for the Dealix platform. The model is a meta-layer — it runs no logic and replaces no code; it describes how we verify that each of the thirteen layers is "actually built" rather than assumed to be. The explicit goal: stop fooling yourself. A well-documented, untested layer is not a ready layer.

## The universal 8-part rule

A layer is not counted as "built" unless all eight parts below exist, each with verifiable evidence:

1. **architecture** — a document explaining components, their boundaries, and real code paths.
2. **readiness.md** — a bilingual checklist with a score, a band, and a rationale.
3. **tests** — a test spec stating what proves the behavior and what blocks a merge.
4. **observability** — dashboards, alerts, and logs that surface failure when it happens.
5. **governance** — written policies, approval rules, and risk thresholds.
6. **rollback** — a documented procedure to return to the last known-green state.
7. **metrics** — indicators with a source and a pass threshold, never guaranteed numbers.
8. **owner** — a named responsible person or role for the layer.

Any missing part lowers the layer's score and prevents it from reaching the enterprise-ready band.

## The thirteen layers

| Layer | Name | One-line purpose |
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
| 13 | Readiness & Cross-Layer Validation | This meta-layer: verifies Layers 1-12 are actually built. |

## How the meta-layer maps to (never duplicates) real code

Layer 13 holds no runtime logic. Every reference points to existing code, not new code:

- Agent logic lives in `auto_client_acquisition/agent_os/`, `auto_client_acquisition/secure_agent_runtime_os/`, and `core/agents/`.
- Workflow logic lives in `auto_client_acquisition/workflow_os/`, `auto_client_acquisition/execution_os/`, and `dealix/execution/`.
- Governance logic lives in `auto_client_acquisition/governance_os/`, `dealix/governance/approvals.py`, and `dealix/trust/`.
- Integrations live in `integrations/` and `dealix/connectors/`.
- Observability lives in `dealix/observability/` and `auto_client_acquisition/observability_adapters/`.
- Knowledge and memory live in `auto_client_acquisition/knowledge_os/`, `auto_client_acquisition/company_brain/`, and `core/memory/`.

Layer 13 reads these facts and records the verification of them. If a document conflicts with the code, the code is the source of truth.

## Related links

- `readiness/scoring_system.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`
- `platform/README.md`

Estimated value is not Verified value.
