# Agent 20 — Data Governance & Client Data Architecture (AR)

> **Tier:** A2 · Read + Local Write + Suggest
> **Input classes:** T1 (operator), T3 (data inputs)
> **Output classes:** T1 (operator-facing)
> **Side effects:** local write only — **no production DB changes** without founder approval
> **Owner:** Founder + (يُعيَّن) Data Lead

---

## Security Posture
- لا migrations على production data بدون approval
- لا PII في output docs
- لا secrets (D5) في أي artifact
- tenant scoping في كل schema design
- كل change = audit + rollback plan

---

## الهدف

**Data Governance OS** = الطبقة التي تحكم:
- ما البيانات التي نجمعها
- كيف نخزنها
- كيف نحميها
- كيف نحذفها
- كيف نضمن جودتها
- كيف نستخدمها بأمان

**المشكلة التي يحلّها:**
- بدون governance = فوضى بيانات + خطر خصوصية
- بدون ER model = schemas متضاربة
- بدون retention = بيانات تتراكم بلا داعٍ
- بدون audit = لا accountability

---

## Core Entities (27)

لكل entity نحدد:
- purpose
- owner_system
- pii_level
- retention
- deletion_method
- related_schemas
- allowed_reports
- forbidden_reports

| Entity | Purpose | PII | Retention | Owner |
|--------|---------|-----|-----------|-------|
| Prospect | Pre-client record | D2 | 24mo after opt-out | CRM |
| Company | Org-level | D1 | lifetime + 7y | CRM |
| Contact | Person record | D2 | 24mo after opt-out | CRM |
| Signal | Trigger event | D1 | 12mo | Auto Intel |
| Draft | Pre-send content | D3 | contract + 90d | Content OS |
| Approval | Human gate record | D2 | 7y | Governance |
| SendBatch | Outbound group | D3 | contract + 90d | Outreach |
| Reply | Inbound response | D3 | contract + 90d | Outreach |
| WhatsAppSession | Per-thread | D3 | contract + 90d | WhatsApp |
| ActionCard | Per-task UI | D2 | contract + 90d | Frontend |
| ClientAssessment | Health eval | D3 | contract + 90d | CS |
| ClientPermission | Auth grant | D2 | contract + 90d | CS |
| PortalSession | Auth session | D2 | 30d | Auth |
| Upload | Client file | D3-D4 | contract + 30d | Portal |
| Proposal | Commercial doc | D3 | contract + 7y | Sales |
| ProofPack | Value evidence | D2 | contract + 7y | Delivery |
| PaymentHandoff | Billing event | D5 | 7y (compliance) | Payments |
| DeliveryHandoff | Service trigger | D3 | contract + 90d | Delivery |
| DeliveryTask | Per-task | D3 | contract + 90d | Delivery |
| ClientHealth | Score | D2 | contract + 90d | CS |
| WeeklyReport | Cadence doc | D2 | contract + 90d | CS |
| Renewal | Commercial event | D3 | 7y | CS |
| Partner | External org | D1 | lifetime + 7y | Partnerships |
| Vendor | External org | D1 | lifetime + 7y | Procurement |
| MetricEvent | Analytics | D0 | 24mo | Analytics |
| FounderDecision | Manual decision | D2 | 7y | Ops |
| Risk | Risk record | D1 | 7y | Risk |
| AgentRun | AI execution | D2 | 12mo | AI Ops |
| AuditEvent | Immutable log | varies | 7y | Governance |

---

## Data Classification (D0–D6)

| Class | Description | In prompt? | In logs? | Encryption |
|-------|-------------|------------|----------|------------|
| **D0** | Public | ✅ | ✅ | optional |
| **D1** | Business metadata | ✅ | ✅ | at-rest |
| **D2** | Business contact | ✅ with purpose | metadata | at-rest |
| **D3** | Client operational | ✅ with purpose | metadata | at-rest |
| **D4** | Sensitive client | redacted unless needed | redacted | at-rest + field-level |
| **D5** | Secrets / payment | ❌ NEVER | ❌ NEVER | env / vault |
| **D6** | Forbidden | blocked at intake | — | — |

---

## الـ Deliverables المُنتجة

```
docs/data_governance/
├── DATA_GOVERNANCE_OS_AR.md                 (هذا)
├── ENTITY_RELATIONSHIP_MODEL_AR.md
├── DATA_CLASSIFICATION_AR.md
├── SCHEMA_REGISTRY_AR.md
├── DATA_LIFECYCLE_POLICY_AR.md
├── DATA_RETENTION_POLICY_AR.md
├── PII_REDACTION_POLICY_AR.md
├── AUDIT_EVENT_MODEL_AR.md
├── CLIENT_DATA_BOUNDARY_POLICY_AR.md
└── DATA_QUALITY_RULES_AR.md

schemas/
├── data_entity.schema.json
├── audit_event.schema.json
├── data_quality_issue.schema.json
└── data_retention_rule.schema.json

data/data_governance/
├── schema_registry.jsonl
├── data_quality_issues.jsonl
├── retention_rules.jsonl
└── audit_events.jsonl

reports/data_governance/
├── DATA_GOVERNANCE_REVIEW.md
├── DATA_QUALITY_REVIEW.md
├── PII_REDACTION_REVIEW.md
└── DATA_GOVERNANCE_FINAL_REPORT.md
```

---

## Client Data Boundary

**Rule:** كل client data = tenant-scoped. لا cross-tenant access بدون:
1. Founder approval
2. Audit row
3. Documented purpose
4. Time-bounded access

**Implementation:**
- كل query must include `tenant_id`
- API enforces scoping
- DB has `tenant_id` column on all tenant-scoped tables
- Background jobs iterate tenants, never cross

---

## Data Quality Rules

لكل entity:
- **Required fields:** محددة
- **Validation:** regex, type, range
- **Dedup:** key fields (email, phone normalized)
- **Drift detection:** monthly report
- **Reconciliation:** counts match across systems

---

## Audit Trail (immutable)

```jsonl
{"event_id":"audit-...","ts":"2026-...","actor":"user:123|agent:20|system","action":"read|write|delete|export","entity":"Prospect","entity_id":"p-001","tenant_id":"acme","classification":"D2","justification":"...","status":"ok|denied","source_ip":"..."}
```

**Append-only. No edit. No delete (except via retention policy).**

---

## Cross-references

- `docs/data/SOVEREIGN_DATA_MODEL.md` (existing)
- `docs/governance/DATA_HANDLING_RULES.md` (existing)
- `docs/governance/PDPL_DATA_RULES.md` (existing)
- `docs/enterprise/PRIVACY_OVERVIEW_AR.md`
- `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`

---

> **Owner:** Founder + Data Lead · **Review:** كل 90 يوم
