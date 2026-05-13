# Privacy-by-Runtime

Privacy is enforced at runtime, not in a PDF.

## 1. Required checks per AI task

- Source Passport check
- PII Detector
- Allowed Use Checker
- Redaction
- Policy Decision
- Audit Event
- Approval Requirement (if external)

## 2. Example evaluation

```json
{
  "input_contains_pii": true,
  "allowed_use": ["internal_analysis", "draft_only"],
  "external_use_allowed": false,
  "decision": "DRAFT_ONLY",
  "required_action": "human_review_before_any_external_use"
}
```

## 3. Why runtime

Risks emerge from execution paths, not from designs. Agents may collect or expose sensitive data during execution; only a runtime evaluator that sees the trace can catch the failure.

## 4. Operating discipline

- Every task passes all seven checks.
- Failed checks block the task and emit an audit event with the failure reason.
- External actions on PII never default to allow.

## 5. The principle

> Privacy is a runtime decision. A policy document is the floor, not the ceiling.
