# Dealix Wave 3 — Master Index (AR)

> **Agents 18–28:** الطبقة المؤسسية الكاملة.

---

## الخريطة في 30 ثانية

| # | Agent | الغرض | Tier | Priority |
|---|-------|--------|------|----------|
| 18 | Enterprise Readiness & B2B Procurement | جاهزية البيع للمؤسسات | A2 | **Urgent** |
| 19 | AI Ops, Model Routing & Cost Governance | حوكمة LLM والتكلفة | A2 | **Urgent** |
| 20 | Data Governance & Client Data Architecture | حوكمة البيانات | A2 | **Urgent** |
| 21 | Sales Enablement & Founder Selling | مكنة البيع المؤسسي | A2 | **Urgent** |
| 22 | Service Quality & Delivery Excellence | جودة الخدمة والتسليم | A2 | **Urgent** |
| 23 | Strategic Moats & Competitive Intel | المميزات الدفاعية | A1 | Next |
| 24 | Saudi Vertical GTM | تخصص القطاعات | A1 | Next |
| 25 | Board, Investor & Strategic Partner Pack | عرض المؤسسات | A1 | Next |
| 26 | Internal Controls, Audit & Governance | ضوابط داخلية | A2 | Next |
| 27 | Revenue Forecasting & Scenarios | التخطيط المالي | A1 | Next |
| 28 | Client Education Academy | تعليم العملاء | A1 | Next |

---

## الاثار (Lines of Defense)

كل Agent مبني على **AGENT_SECURITY_FRAMEWORK_AR.md** المشترك:
- Input classification (T0–T5)
- Allowlist side effects
- Audit events to `data/governance/audit_events.jsonl`
- No auto-execution من prompt content
- Secrets لا تذهب لموديلات

**راجع:** `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`

---

## ترتيب التنفيذ

### Urgent (نفّذها أولاً)
- Agent 18 → `docs/enterprise/` (توسعة)
- Agent 19 → `docs/ai_ops/` (جديد)
- Agent 20 → `docs/data_governance/` (جديد)
- Agent 21 → `docs/sales_enablement/` (جديد)
- Agent 22 → `docs/service_quality/` (جديد)

### Next Phase
- Agent 23 → `docs/strategy/`
- Agent 24 → `docs/verticals/`
- Agent 26 → `docs/governance/` (توسعة)
- Agent 27 → `docs/forecasting/`
- Agent 28 → `docs/academy/` (توسعة)

### Later (بعد تثبيت Urgent + Next)
- Agent 25 → `docs/board_ready/` + `docs/data_room/`

---

## المخرجات الرئيسية لكل Agent

كل Agent من 18–22 ينتج:
- **OS Overview Doc** — فهرس شامل
- **3–5 Policy/Framework Docs** — السياسات التفصيلية
- **1–2 Schemas (JSON)** — للتدقيق والأتمتة
- **1–2 Data Files (JSONL)** — قابلة للقراءة من قبل Agents آخرين
- **Final Report** — تقييم ذاتي + next actions

---

## Cross-References (موجود، يُحترم)

- Security: `docs/security/`, `docs/governance/AI_USAGE_POLICY.md`
- Enterprise: `docs/enterprise/ENTERPRISE_READINESS.md`
- Data: `docs/data/SOVEREIGN_DATA_MODEL.md`
- Governance: `docs/governance/APPROVAL_MATRIX.md`
- Academy: `docs/academy/ACADEMY_PATH.md`
- Board: `docs/board_ready/BOARD_DASHBOARD.md`
- Agents registry: `os/02_AGENTS.md`

> Wave 3 **لا يلغي** أي من هذي. يبني عليها ويُفصّلها.

---

> **Last update:** 2026-06-03
