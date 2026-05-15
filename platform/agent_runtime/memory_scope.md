# العربية

**Owner:** مالك منصة وقت تشغيل الوكلاء (Agent Runtime Platform Lead).

## الغرض

نطاق الذاكرة يحدد ما يمكن لكل وكيل قراءته وكتابته. كل وكيل معزول عن ذاكرة غيره؛ لا تُشارَك الذاكرة عبر الوكلاء إلا عبر عقد صريح. هذا يمنع تسرّب بيانات عميل إلى سياق وكيل آخر.

## نطاقات الذاكرة المعرّفة

- `customer_memory` — ذاكرة محادثة وحساب العميل، مقيّدة بـ `tenant_id`.
- `product_knowledge` — معرفة المنتج والخدمات، مشتركة للقراءة فقط.
- `ops_memory` — ذاكرة العمليات الداخلية والمهام.
- `governance_memory` — سجل القرارات والموافقات والمخاطر.
- `executive_memory` — ملخصات تنفيذية ومؤشرات مجمَّعة.

## المكوّنات

- **مخزن الذاكرة:** `auto_client_acquisition/ai_workforce_v10/memory_store.py` يعزل الذاكرة لكل وكيل.
- **حدود السياق:** `auto_client_acquisition/secure_agent_runtime_os/context_boundary.py` يمنع قراءة سياق خارج النطاق.
- **حدود البيانات:** `auto_client_acquisition/secure_agent_runtime_os/data_boundary.py` يفرض حدود `tenant_id`.

## قائمة الجاهزية

- [x] لكل وكيل نطاق ذاكرة معلن في `agent.yaml`.
- [x] الذاكرة مقيّدة بـ `tenant_id`.
- [x] لا يقرأ وكيل ذاكرة وكيل آخر دون عقد.
- [ ] انتهاء صلاحية ذاكرة العميل وفق جدول احتفاظ PDPL موثَّق.

## المقاييس

- عدد محاولات الوصول خارج النطاق (هدف: صفر).
- نسبة عناصر الذاكرة الحاملة لـ `tenant_id`: 100%.
- حجم الذاكرة لكل وكيل.

## خطافات المراقبة

- حدث `memory.read` و`memory.write` و`memory.scope_violation` عبر `auto_client_acquisition/agent_observability/trace.py`.
- تنبيه فوري عند `memory.scope_violation`.

## قواعد الحوكمة

- لا يكتب وكيل في نطاق ذاكرة غير معلن في `agent.yaml`.
- مشاركة الذاكرة عبر الوكلاء تتطلب عقداً صريحاً وموافقة قائد الحوكمة.
- لا تُكتب PII في `product_knowledge` أو `executive_memory`.

## إجراء التراجع

عند تسرّب نطاق: أوقف الوكيل فوراً، أبطل عناصر الذاكرة الملوّثة، استعد لقطة الذاكرة النظيفة الأخيرة، وسجّل الحادث.

## درجة الجاهزية الحالية

**73 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

---

# English

**Owner:** Agent Runtime Platform Lead.

## Purpose

Memory Scope defines what each agent may read and write. Every agent is isolated from other agents' memory; memory is not shared across agents except by an explicit contract. This prevents one customer's data from leaking into another agent's context.

## Defined memory scopes

- `customer_memory` — customer conversation and account memory, bound by `tenant_id`.
- `product_knowledge` — product and service knowledge, shared read-only.
- `ops_memory` — internal operations and task memory.
- `governance_memory` — decision, approval, and risk log.
- `executive_memory` — executive summaries and aggregated indicators.

## Components

- **Memory store:** `auto_client_acquisition/ai_workforce_v10/memory_store.py` isolates per-agent memory.
- **Context boundary:** `auto_client_acquisition/secure_agent_runtime_os/context_boundary.py` blocks out-of-scope context reads.
- **Data boundary:** `auto_client_acquisition/secure_agent_runtime_os/data_boundary.py` enforces `tenant_id` limits.

## Readiness checklist

- [x] Every agent has a declared memory scope in `agent.yaml`.
- [x] Memory is bound by `tenant_id`.
- [x] No agent reads another agent's memory without a contract.
- [ ] Customer memory expiry per a documented PDPL retention schedule.

## Metrics

- Count of out-of-scope access attempts (target: zero).
- Share of memory items carrying `tenant_id`: 100%.
- Memory size per agent.

## Observability hooks

- `memory.read`, `memory.write`, and `memory.scope_violation` events via `auto_client_acquisition/agent_observability/trace.py`.
- Immediate alert on `memory.scope_violation`.

## Governance rules

- An agent does not write to a memory scope not declared in its `agent.yaml`.
- Cross-agent memory sharing requires an explicit contract and Governance Lead approval.
- No PII is written into `product_knowledge` or `executive_memory`.

## Rollback procedure

On a scope leak: stop the agent immediately, invalidate the contaminated memory items, restore the last clean memory snapshot, and record the incident.

## Current readiness score

**73 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.
