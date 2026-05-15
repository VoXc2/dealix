# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة (Privacy & Trust Plane).

## الغرض

الطبقة 5 — الحوكمة — تضمن أن كل إجراء يقوم به الذكاء الاصطناعي في Dealix محكوم وقابل للتدقيق ومتناسب مع مستوى مخاطره. لا تُنفِّذ هذه الطبقة عملاً بنفسها؛ بل تقف بين قرارات الوكلاء (الطبقة 2) والتنفيذ الفعلي (Execution Plane). كل إجراء يحمل تصنيف مخاطر، وكل إجراء عالي المخاطر لا يُنفَّذ دون موافقة بشرية موثَّقة، وكل موافقة وكل تقييم سياسة يُسجَّل في أثر تدقيق غير قابل للتعديل. الهدف النهائي: أن نُثبت للعميل ما الذي فعله الذكاء الاصطناعي، ولماذا، ومن وافق عليه.

تتماشى هذه الطبقة مع دورة حياة NIST AI RMF (Govern / Map / Measure / Manage) المذكورة في `dealix/registers/compliance_saudi.yaml`.

## المكوّنات

- **محرّك السياسات (Policy Engine):** يُقيّم كل إجراء مقترح مقابل القواعد القابلة للإصدار. مبني على `auto_client_acquisition/governance_os/policy_registry.py` و`policy_check.py` و`runtime_decision.py`، ويُحمّل القواعد من `auto_client_acquisition/governance_os/rules/`.
- **محرّك المخاطر (Risk Engine):** يُسند تصنيف موافقة/قابلية تراجع/حساسية (A/R/S) لكل إجراء عبر `dealix/classifications/__init__.py`، ويُقيّم مخاطر الحملات قبل الإطلاق عبر `auto_client_acquisition/compliance_os/risk_engine.py`.
- **محرّك الموافقات (Approval Engine):** يوجّه الإجراءات عالية المخاطر إلى المراجعين البشريين عبر `auto_client_acquisition/approval_center/` و`dealix/trust/approval.py`.
- **محرّك التدقيق (Audit Engine):** يكتب قيوداً إلحاقية غير قابلة للتعديل عبر `dealix/trust/audit.py`، مرتبطة بحزم الأدلة في `dealix/trust/`.
- **سجل القواعد (Rule Registry):** مصدر الحقيقة للقواعد المفعّلة، مع إصدار ومالك لكل قاعدة، في `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- **محرّك الامتثال (Compliance Engine):** يربط الإجراءات بمتطلبات نظام حماية البيانات الشخصية (PDPL) وفواتير ZATCA المرحلة الثانية عبر `auto_client_acquisition/compliance_os/`.

## تدفّق البيانات

1. يقترح وكيل من الطبقة 2 إجراءً (`NextAction`) عبر عقد القرار `dealix/contracts/decision.py`.
2. يُسند محرّك المخاطر تصنيف A/R/S للإجراء عبر `classify()` في `dealix/classifications/__init__.py`.
3. يُقيّم محرّك السياسات الإجراء مقابل القواعد المفعّلة؛ النتيجة: `allow` أو `require_approval` أو `block`.
4. الإجراءات بتصنيف R3 أو المدرجة في `NEVER_AUTO_EXECUTE` تُرفع دائماً إلى محرّك الموافقات ولا تُنفَّذ آلياً مطلقاً.
5. يُنشئ محرّك الموافقات `ApprovalRequest` بمدة صلاحية محددة وينتظر العدد المطلوب من المراجعين.
6. يكتب محرّك التدقيق قيداً عند كل خطوة: التقييم، القرار، الموافقة أو الرفض، التنفيذ.
7. عند المنح فقط يُسلَّم الإجراء إلى Execution Plane؛ عند الرفض أو انتهاء المهلة يُحجب ويُسجَّل السبب.

## الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي في المستودع |
|---|---|
| سجل السياسات | `auto_client_acquisition/governance_os/policy_registry.py` |
| فحص السياسة | `auto_client_acquisition/governance_os/policy_check.py` |
| قرار وقت التشغيل | `auto_client_acquisition/governance_os/runtime_decision.py` |
| سجل القواعد الافتراضي | `auto_client_acquisition/governance_os/policies/default_registry.yaml` |
| قواعد الحوكمة | `auto_client_acquisition/governance_os/rules/` |
| تصنيفات الإجراءات A/R/S | `dealix/classifications/__init__.py` |
| محرّك مخاطر الحملات | `auto_client_acquisition/compliance_os/risk_engine.py` |
| مركز الموافقات | `auto_client_acquisition/approval_center/` |
| سياسة الموافقة | `auto_client_acquisition/governance_os/approval_policy.py` |
| سير عمل الموافقة | `dealix/trust/approval.py` |
| سجل التدقيق | `dealix/trust/audit.py` |
| حزم الأدلة | `dealix/trust/` |
| سجل الامتثال السعودي | `dealix/registers/compliance_saudi.yaml` |
| محرّك الامتثال | `auto_client_acquisition/compliance_os/` |
| الدستور التشغيلي | `docs/DEALIX_OPERATING_CONSTITUTION.md` |

انظر أيضاً: `platform/governance/readiness.md` و`platform/governance/policy_engine.md` و`platform/governance/approval_engine.md`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## Purpose

Layer 5 — Governance — ensures every AI action in Dealix is governed, auditable, and proportionate to its risk. This layer executes no work itself; it sits between agent decisions (Layer 2) and actual execution (Execution Plane). Every action carries a risk classification, every high-risk action is blocked from execution without a documented human approval, and every approval and policy evaluation is written to an immutable audit trail. The end goal: prove to a customer what the AI did, why, and who approved it.

This layer aligns with the NIST AI RMF lifecycle (Govern / Map / Measure / Manage) referenced in `dealix/registers/compliance_saudi.yaml`.

## Components

- **Policy Engine:** evaluates every proposed action against versioned rules. Built on `auto_client_acquisition/governance_os/policy_registry.py`, `policy_check.py`, and `runtime_decision.py`, loading rules from `auto_client_acquisition/governance_os/rules/`.
- **Risk Engine:** assigns an Approval / Reversibility / Sensitivity (A/R/S) classification to every action via `dealix/classifications/__init__.py`, and scores campaign risk before launch via `auto_client_acquisition/compliance_os/risk_engine.py`.
- **Approval Engine:** routes high-risk actions to human reviewers via `auto_client_acquisition/approval_center/` and `dealix/trust/approval.py`.
- **Audit Engine:** writes immutable append-only entries via `dealix/trust/audit.py`, linked to evidence packs in `dealix/trust/`.
- **Rule Registry:** source of truth for active rules, with a version and owner per rule, in `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- **Compliance Engine:** maps actions to Personal Data Protection Law (PDPL) requirements and ZATCA Phase 2 invoicing via `auto_client_acquisition/compliance_os/`.

## Data flow

1. A Layer 2 agent proposes an action (`NextAction`) via the decision contract `dealix/contracts/decision.py`.
2. The Risk Engine assigns an A/R/S classification via `classify()` in `dealix/classifications/__init__.py`.
3. The Policy Engine evaluates the action against active rules; result: `allow`, `require_approval`, or `block`.
4. Actions classified R3 or listed in `NEVER_AUTO_EXECUTE` are always raised to the Approval Engine and never auto-execute.
5. The Approval Engine creates an `ApprovalRequest` with a defined TTL and waits for the required reviewer count.
6. The Audit Engine writes an entry at every step: evaluation, decision, grant or rejection, execution.
7. Only on grant is the action handed to the Execution Plane; on rejection or timeout it is blocked and the reason recorded.

## Mapping to existing code

| Component | Real repo path |
|---|---|
| Policy registry | `auto_client_acquisition/governance_os/policy_registry.py` |
| Policy check | `auto_client_acquisition/governance_os/policy_check.py` |
| Runtime decision | `auto_client_acquisition/governance_os/runtime_decision.py` |
| Default rule registry | `auto_client_acquisition/governance_os/policies/default_registry.yaml` |
| Governance rules | `auto_client_acquisition/governance_os/rules/` |
| A/R/S action classifications | `dealix/classifications/__init__.py` |
| Campaign risk engine | `auto_client_acquisition/compliance_os/risk_engine.py` |
| Approval center | `auto_client_acquisition/approval_center/` |
| Approval policy | `auto_client_acquisition/governance_os/approval_policy.py` |
| Approval workflow | `dealix/trust/approval.py` |
| Audit log | `dealix/trust/audit.py` |
| Evidence packs | `dealix/trust/` |
| Saudi compliance register | `dealix/registers/compliance_saudi.yaml` |
| Compliance engine | `auto_client_acquisition/compliance_os/` |
| Operating constitution | `docs/DEALIX_OPERATING_CONSTITUTION.md` |

See also: `platform/governance/readiness.md`, `platform/governance/policy_engine.md`, and `platform/governance/approval_engine.md`.
