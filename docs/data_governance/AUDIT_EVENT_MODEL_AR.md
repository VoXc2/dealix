# Audit Event Model (AR)

> **Append-only. Immutable. 7-year retention.**

---

## 1. Event Schema

```json
{
  "event_id": "audit-2026-001-abc",
  "ts": "2026-06-03T03:15:00Z",
  "actor": "user:123 | agent:20 | system",
  "actor_type": "human | agent | service",
  "action": "read | write | update | delete | export | approve | send | pay | deploy | access_secret",
  "entity": "Prospect | Client | Draft | ...",
  "entity_id": "p-001",
  "tenant_id": "acme-sa | null",
  "data_class": "D0 | D1 | D2 | D3 | D4 | D5",
  "fields_accessed": ["email", "phone"],
  "justification": "explicit user request | standard workflow | ...",
  "source_ip": "...",
  "user_agent": "...",
  "request_id": "...",
  "status": "ok | denied | failed",
  "notes": ""
}
```

---

## 2. What Gets Logged

**Always:**
- Any D2+ access
- Any privileged action (approve, send, pay, deploy, delete)
- Any cross-tenant access attempt
- Any secret access
- Any schema/permission change
- Any production deploy
- Any partner/vendor agreement action

**Conditionally:**
- D1 access in bulk
- Auth failures
- Schema validation failures

**Never logged:**
- Prompt content (T3/T4)
- PII fields (D2-D5) — only metadata
- Free-text user messages to AI

---

## 3. Storage

- **Primary:** `data/governance/audit_events.jsonl` (append-only)
- **Backup:** provider-managed
- **Archive:** cold storage بعد 12 شهر
- **Retention:** 7y minimum

**No edit. No delete (except via retention expiry).**

---

## 4. Access

- **Read:** founder + security officer + privacy officer
- **Query:** via API/UI
- **Export:** with founder approval + audit
- **Public:** aggregated, anonymized only

---

## 5. Use Cases

- **Compliance audit:** prove controls worked
- **Incident investigation:** trace what happened
- **Subject access request:** what data we hold
- **Forensic:** who did what when
- **Anomaly detection:** unusual patterns

---

## 6. Integrity

- Each event: timestamp + hash chain (مُخطط)
- Detection: any tampering = alert
- Periodic verification: scheduled job

---

## 7. Reporting

- **Daily:** count by action
- **Weekly:** anomalies, denied actions
- **Monthly:** compliance report
- **Quarterly:** integrity verification

---

> **Owner:** Founder + Security · **Review:** سنوي
> **Cross-ref:** `docs/governance/AUDIT_LOG_POLICY.md` (existing)
