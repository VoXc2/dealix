# Governance OS — القرار والسياسات

## الهدف

تحويل المخاطر إلى **قرارات تشغيلية** قابلة للتسجيل: ALLOW، ALLOW_WITH_REVIEW، DRAFT_ONLY، REQUIRE_APPROVAL، REDACT، BLOCK، ESCALATE.

## مثال قرار (مرجعي)

```json
{
  "decision": "DRAFT_ONLY",
  "risk_level": "medium",
  "matched_rules": [
    "external_action_requires_approval",
    "pii_requires_review"
  ],
  "reason": "Personal contact data exists and external sending is not approved.",
  "next_action": "human_review"
}
```

## التنفيذ في الريبو

- `auto_client_acquisition/governance_os/` — مسودات، تدقيق نصوص، بوابات intake.
- `auto_client_acquisition/revenue_os/anti_waste.py` — قواعد لا إجراء خارجي بدون جواز قرار، لا upsell بدون proof، إلخ.
- قواعد القنوات: `auto_client_acquisition/compliance_trust_os/channel_policy.py`
- قواعد المطالبات: `auto_client_acquisition/compliance_trust_os/claim_safety.py`

## قواعد Dealix (غير قابلة للنقض)

ممنوع: كشط تلقائي، واتساب بارد، أتمتة لينكدإن، ادّعاءات ضمان وهمية — انظر الاختبارات في [TESTS_REQUIRED.md](TESTS_REQUIRED.md).

## روابط

- [LLM_GATEWAY.md](LLM_GATEWAY.md) — [TRUST_OS.md](TRUST_OS.md)
