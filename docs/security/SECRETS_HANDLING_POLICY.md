# Secrets Handling Policy
## سياسة التعامل مع الأسرار

**Document Type:** Security Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines how Dealix handles secrets (API keys, PATs, credentials, tokens, passwords) to prevent leakage through prompts, logs, reports, or outputs.

---

## 2. Core Principle

> **SECRETS MUST NEVER APPEAR IN PROMPTS, LOGS, REPORTS, OR OUTPUTS.**

---

## 3. Secret Definitions

### 3.1 Secret Types

| Type | Examples | Risk |
|------|----------|------|
| API Keys | `sk-xxx`, `pk_xxx`, `api_key=xxx` | CRITICAL |
| Personal Access Tokens | `ghp_xxx`, `github_pat_xxx` | CRITICAL |
| OAuth Tokens | `Bearer xxx`, `access_token=xxx` | CRITICAL |
| Database Credentials | `password=xxx`, `DB_PASS=xxx` | CRITICAL |
| Encryption Keys | `ENCRYPTION_KEY=xxx`, `JWT_SECRET=xxx` | CRITICAL |
| Service Account Keys | JSON key files, `.pem` files | CRITICAL |
| Payment Credentials | Moyasar keys, Stripe keys | CRITICAL |
| WhatsApp Tokens | Meta business tokens | CRITICAL |
| LLM API Keys | Anthropic, OpenAI, Gemini keys | HIGH |

### 3.2 Secret Patterns

```python
SECRET_PATTERNS = [
    r'sk-[a-zA-Z0-9]{20,}',           # OpenAI/Anthropic
    r'ghp_[a-zA-Z0-9]{36,}',          # GitHub PAT
    r'github_pat_[a-zA-Z0-9_]{22,}',  # GitHub fine-grained PAT
    r'pk_[a-zA-Z0-9]{20,}',           # Stripe
    r'Bearer\s+[a-zA-Z0-9_-]{20,}',   # Bearer tokens
    r'api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9_-]{20,}["\']',  # API key assignments
    r'secret["\']?\s*[:=]\s*["\'][a-zA-Z0-9_-]{20,}["\']',  # Secret assignments
    r'password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',  # Passwords
    r'DB_PASS|DB_PASSWORD|DATABASE_PASSWORD',  # DB credentials
    r'ENCRYPTION_KEY|JWT_SECRET|APP_SECRET',  # Crypto keys
    r'\+966[0-9]{9}',  # Saudi phone (PII, treated as secret in some contexts)
]
```

---

## 4. Handling Requirements

### 4.1 Secrets in Prompts

| Context | Rule | Implementation |
|---------|------|----------------|
| Agent prompts | NEVER | Never include secrets in system/user prompts |
| Tool inputs | NEVER | Validate tool inputs for secrets before call |
| Context windows | NEVER | Never pass secrets in context |
| Code generation | NEVER | Never generate code with real secrets |

**When a secret is accidentally included:**
1. STOP processing immediately
2. DO NOT execute any actions
3. LOG the incident (severity: CRITICAL)
4. ESCALATE to founder
5. DO NOT proceed until cleared

### 4.2 Secrets in Logs

| Context | Rule | Implementation |
|---------|------|----------------|
| Agent logs | NEVER | Strip secrets before logging |
| API logs | NEVER | Mask secrets in log output |
| Error logs | NEVER | Never include full secrets |
| Audit logs | LOG REFERENCE | Log "SECRET_ACCESS: type=xxx, hash=xxx" |

**Log Format for Secret Access:**
```yaml
secret_access_log:
  timestamp: ISO8601
  event: "SECRET_ACCESS"
  secret_type: "API_KEY | PAT | TOKEN | PASSWORD"
  secret_reference: "DEALIX_API_KEY | HUBSPOT_TOKEN | ..."
  action: "read | write | rotate | delete"
  result: "success | failure"
  agent_id: agent_name
  justification: "Why secret was accessed"
  approved_by: founder_name
```

### 4.3 Secrets in Reports

| Context | Rule | Implementation |
|---------|------|----------------|
| Generated reports | NEVER | Redact all secrets |
| Weekly reports | NEVER | Never include credentials |
| Audit reports | LOG REFERENCE | Reference by name, not value |
| Debug reports | NEVER | Never include secrets |

**Report Secret Handling:**
```python
def sanitize_report_for_secrets(report_content: str) -> str:
    """Remove all secrets from report content."""
    sanitized = report_content
    
    for pattern in SECRET_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED_SECRET]", sanitized)
    
    return sanitized
```

### 4.4 Secrets in Outputs

| Context | Rule | Implementation |
|---------|------|----------------|
| Agent responses | NEVER | Never output secrets |
| Tool outputs | SANITIZE | Redact secrets from outputs |
| MCP tool outputs | SANITIZE | Never expose secrets |
| API responses | NEVER | Never return secrets in response |

### 4.5 Secrets in WhatsApp

| Context | Rule | Implementation |
|---------|------|----------------|
| WhatsApp messages | NEVER | Never send secrets via WhatsApp |
| User asks for API key | REFUSE | "I cannot share API keys via WhatsApp" |
| User asks for credentials | REFUSE | "Use the secure portal instead" |
| Shared links with secrets | REFUSE | "Remove secrets before sharing" |

---

## 5. Secret Storage Requirements

### 5.1 Approved Secret Storage

| Storage | Approved? | Notes |
|---------|----------|-------|
| GitHub Secrets | Yes | Encrypted at rest |
| Railway Environment Variables | Yes | Encrypted at rest |
| `.env` file (local) | Yes | Gitignored |
| Environment variables | Yes | In memory only |
| Vault (future) | Yes | Centralized secret management |

### 5.2 Forbidden Secret Storage

| Storage | Forbidden? | Reason |
|---------|------------|--------|
| Code repository | FORBIDDEN | Public exposure risk |
| Comments | FORBIDDEN | Git history exposure |
| Logs | FORBIDDEN | Log aggregation exposure |
| Reports | FORBIDDEN | Distribution exposure |
| Emails | FORBIDDEN | Email exposure |
| WhatsApp/SMS | FORBIDDEN | Messaging exposure |
| GitHub Issues/PRs | FORBIDDEN | Public exposure |
| External tools | FORBIDDEN | No unauthorized storage |

---

## 6. Secret Access Workflow

### 6.1 Request Access

```
┌─────────────────────────────────────────────────────────────────┐
│                   SECRET ACCESS REQUEST                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Justify need — Why is this secret needed?                     │
│ 2. Specify scope — What operations need this secret?            │
│ 3. Request duration — How long is access needed?                 │
│ 4. Acknowledge handling rules — Will follow secrets policy        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FOUNDER APPROVAL                               │
│ Founder reviews:                                                 │
│ - Is the justification valid?                                     │
│ - Is the scope appropriate?                                       │
│ - Is the duration reasonable?                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
        ┌───────────┐                   ┌───────────┐
        │ APPROVED  │                   │  DENIED   │
        └───────────┘                   └───────────┘
              │                               │
              ▼                               ▼
        ┌───────────┐                   ┌───────────┐
        │ Grant     │                   │ Log denial│
        │ temporary │                   │ Notify    │
        │ access    │                   │ requester │
        └───────────┘                   └───────────┘
```

### 6.2 Emergency Access

For genuine emergencies (security incident, production outage):

1. Founder can pre-authorize emergency secret access
2. All actions logged with emergency flag
3. Post-incident review mandatory
4. Access revoked immediately after emergency

---

## 7. Secret Rotation

### 7.1 Rotation Schedule

| Secret Type | Rotation Frequency | Notes |
|-------------|-------------------|-------|
| LLM API Keys | Quarterly | Or immediately if exposed |
| GitHub PATs | Quarterly | Or immediately if exposed |
| Database passwords | Quarterly | Or immediately if exposed |
| Encryption keys | Annually | Or immediately if exposed |
| Service account keys | Quarterly | Or immediately if exposed |
| WhatsApp tokens | As needed | Meta-managed |

### 7.2 Rotation Process

1. Generate new secret
2. Update all systems using old secret
3. Verify new secret works
4. Revoke old secret
5. Log rotation event
6. Update key rotation log

### 7.3 Rotation Log

See `docs/security/key_rotation_log.md`

---

## 8. Incident Response

### 8.1 Secret Exposure

If a secret is exposed (in code, logs, reports, or outputs):

1. **IMMEDIATE:** Revoke the secret
2. **IMMEDIATE:** Rotate the secret
3. **IMMEDIATE:** Update all systems using old secret
4. **WITHIN 1 HOUR:** Assess exposure scope
5. **WITHIN 24 HOURS:** Notify affected parties if needed
6. **WITHIN 72 HOURS:** Complete incident report
7. **AFTER:** Update policies to prevent recurrence

### 8.2 Secret Exposure Runbook

See `docs/SECURITY_RUNBOOK.md` — "حادث تسريب سر"

---

## 9. Code Enforcement

### 9.1 gitleaks Configuration

```yaml
# .gitleaks.toml
[rules]
[[rules.secrets]]
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)\s*[:=]\s*["\'][a-zA-Z0-9_-]{20,}["\']'''

[[rules.secrets]]
description = "GitHub Personal Access Token"
regex = '''ghp_[a-zA-Z0-9]{36,}'''

[[rules.secrets]]
description = "OpenAI/Anthropic API Key"
regex = '''sk-[a-zA-Z0-9]{20,}'''
```

### 9.2 Test Enforcement

```python
def test_no_secrets_in_module(module):
    """Test that module source contains no secrets."""
    src = inspect.getsource(module)
    
    for pattern in SECRET_PATTERNS:
        assert not re.search(pattern, src), \
            f"Secret pattern {pattern} found in {module.__name__}"
```

Example: `test_billing_moyasar_safety.py` enforces no secrets in pricing module.

---

## 10. Related Documents

| Document | Purpose |
|----------|---------|
| `docs/security/key_rotation_log.md` | Rotation tracking |
| `docs/security/KEY_ROTATION.md` | Rotation procedures |
| `docs/SECURITY_RUNBOOK.md` | Incident response |
| `test_billing_moyasar_safety.py` | Secret-free module test |
| `repository-hardening.yml` | gitleaks in CI |

---

*Policy maintained by Agent #5 — Security Red Team*
*Review required: Quarterly or after any secret exposure incident*
