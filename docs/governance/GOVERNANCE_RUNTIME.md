# Governance Runtime

الحوكمة ليست PDF فقط — **runtime**: كل مسار يعمل بالذكاء الاصطناعي يجب أن يمرَّ عبر فحوصات قبل التسليم أو أي إجراء خارجي.

في السياق السعودي، جودة الإفصاح والخصوصية لا تزال متفاوتة عبر قطاعات رقمية؛ راجع مثلًا: [One Year After the PDPL (e-commerce sample)](https://arxiv.org/abs/2602.18616). Dealix تتميَّز مبكرًا بـ **source attribution** و**PII handling** و**audit** من اليوم الأول.

---

## Runtime Checks

1. Source check
2. PII check
3. Permission check
4. Allowed use check
5. Claim safety check
6. Channel safety check
7. External action check
8. Approval requirement
9. Audit event write
10. Proof event write (when value is evidenced)

## Decisions

- `ALLOW`
- `ALLOW_WITH_REVIEW`
- `DRAFT_ONLY`
- `REQUIRE_APPROVAL`
- `REDACT`
- `BLOCK`
- `ESCALATE`

---

## Rule examples (YAML-style)

These illustrate intent; production rules live under `auto_client_acquisition/governance_os/rules/` and loaders.

```yaml
id: no_cold_whatsapp
severity: critical
condition:
  channel: whatsapp
  relationship_status_not_in:
    - existing_relationship
    - consented
action:
  decision: BLOCK
  reason: Cold WhatsApp outreach is not allowed.

id: no_guaranteed_claims
severity: critical
condition:
  output_contains:
    - نضمن
    - guaranteed sales
    - guaranteed leads
    - guaranteed revenue
action:
  decision: BLOCK
  reason: Guaranteed outcome claims are not allowed.

id: no_source_no_answer
severity: high
condition:
  answer_has_source: false
  service: company_brain
action:
  decision: BLOCK
  reason: Knowledge answers require sources.

id: pii_in_logs
severity: critical
condition:
  destination: logs
  contains_pii: true
action:
  decision: REDACT
  reason: PII must not be stored in logs.
```

---

## Governance check output (envelope)

```json
{
  "decision": "REQUIRE_APPROVAL",
  "risk_level": "medium",
  "blocked_rules": [],
  "required_approvals": ["delivery_owner"],
  "redactions": ["phone"],
  "audit_event_id": "AUD-1021",
  "reason": "External outreach draft includes personal contact data."
}
```

Code: `policy_check.py` · `forbidden_actions.py` · `audit_log.py` · [`GOVERNANCE_DECISION.md`](GOVERNANCE_DECISION.md).
