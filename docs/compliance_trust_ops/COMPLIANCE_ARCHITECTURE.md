# Compliance Architecture

## مسار كل مخرج AI

```text
Input → Source Passport → PII check → Allowed Use → Task Risk → Channel Risk
→ Claim Safety → Governance Decision → Approval if needed → Audit Event → QA → Output
```

## مثال Governance Decision (JSON)

```json
{
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "reason": "Personal contact data exists and external sending is not approved.",
  "matched_rules": ["external_action_requires_approval", "pii_requires_review"],
  "audit_event_id": "AUD-001",
  "next_action": "human_review"
}
```

**الكود:** `governance_decision_for_pii_external` · `KNOWN_RUNTIME_POLICY_RULES` · `COMPLIANCE_CHANNEL_POLICIES` · `claim_compliance` / `claim_safety` — `compliance_trust_os/approval_engine.py` · `policy_registry.py` · `channel_policy.py` · `claim_compliance.py` · `claim_safety.py`

**صعود:** [`SOURCE_PASSPORT_V2.md`](SOURCE_PASSPORT_V2.md)
