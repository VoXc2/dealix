# PII Redaction Policy (AR)

> **Source-of-truth:** `docs/governance/PII_REDACTION_POLICY.md` (existing)
> **This doc:** Wave 3 agent-specific extensions.

---

## 1. What is PII?

أي data يمكن أن يُعرّف شخصاً أو يكشف معلومة شخصية:
- مباشر: اسم، email، phone، ID
- غير مباشر: موقع، تاريخ، خصائص

---

## 2. Redaction Levels

| Level | Method | Use |
|-------|--------|-----|
| **R0 — None** | D0/D1 | unrestricted |
| **R1 — Hash** | email/phone → hash | analytics (no reversal) |
| **R2 — Mask** | keep first/last char | display |
| **R3 — Tokenize** | replace with token, store mapping | reversible if needed |
| **R4 — Drop** | remove field entirely | strictest |

---

## 3. Per Use Case

| Use case | Method | Example |
|----------|--------|---------|
| Public report | R1 (hash) | "User [hash:abc] did X" |
| Internal dashboard | R2 (mask) | "ah***@gmail.com" |
| LLM prompt (R1 task) | R3 (tokenize) | "[EMAIL_1]" with mapping |
| LLM prompt (R2 task) | selective R3 | emails, phones, names redacted |
| LLM prompt (R3 task) | R3 + audit | full redaction with audit |
| Audit log | metadata only | no PII content |
| Backup | encrypted at-rest | full, encrypted |

---

## 4. When NOT to Redact

- **D0/D1:** unrestricted
- **Direct contact with user:** full PII (e.g., personalized email reply)
- **Legal hold:** preserve per legal advice
- **Client-explicit consent:** documented

---

## 5. Pipeline

```
[Input] → [Detect PII] → [Apply Level per Use Case] → [Process] → [Output] → [Restore if needed]
```

## 6. Detection Patterns

| Pattern | Regex | Action |
|---------|-------|--------|
| Email | `[\w.+-]+@[\w-]+\.[\w.-]+` | tokenize/hash |
| Phone (KSA) | `\+?966?5\d{8}` | tokenize/mask |
| National ID | `\b[12]\d{9}\b` | drop |
| Card | Luhn(13-19) | drop |
| IBAN | `SA\d{22}` | drop |
| API key | known patterns | drop |
| JWT | `eyJ.*\.eyJ.*\..*` | drop |
| URL with PII | any URL with query params | strip params |
| Person name | NER (post-E4) | tokenize |

## 7. Implementation

- **Middleware:** FastAPI middleware scans requests/responses
- **Schema-level:** Pydantic field annotations
- **LLM layer:** Agent 19 applies before model call
- **Logs:** redactor filters before write

## 8. Testing

- Redaction test suite: 100+ PII samples
- Verify: no PII in logs, no PII in LLM prompts (unless declared)
- Monthly audit: grep logs for PII patterns

## 9. Fail-Safe

If redaction fails or uncertain:
- **Conservative path:** drop the field
- **Log:** the detection event
- **Alert:** if repeated failures

---

> **Owner:** Tech Lead + Privacy Officer · **Review:** كل 90 يوم
> **Cross-ref:** `docs/governance/PII_REDACTION_POLICY.md` (existing), `docs/ai_ops/PII_AND_SECRET_MODEL_POLICY_AR.md`
