# Incident Response Runbook
## دليل الاستجابة للحوادث

**Document Type:** Incident Response
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This runbook defines the response protocol for security incidents in Dealix.

---

## 2. Incident Types

| Type | Severity | Examples |
|------|----------|----------|
| Secret exposure | P1 | API key leaked, PAT exposed |
| Unauthorized send | P1 | Email sent without approval |
| Data breach | P1 | Client PII leaked |
| Prompt injection | P2 | Injection detected |
| Workflow violation | P2 | Unauthorized deploy attempt |
| PII leakage | P2 | Data in reports |
| Commercial misrepresentation | P2 | False claim made |

---

## 3. Response Protocol

### P1 (Immediate)

1. STOP the action
2. NOTIFY founder
3. CONTAIN damage
4. INVESTIGATE
5. COMMUNICATE
6. RESOLVE
7. DOCUMENT

### P2 (Within 1 hour)

1. LOG the incident
2. NOTIFY founder
3. INVESTIGATE
4. RESOLVE
5. DOCUMENT

---

## 4. Contact Information

| Role | Contact |
|------|---------|
| Founder | [FOUNDER_CONTACT] |
| Security | Agent #5 via Mavis |
| Legal | [LEGAL_CONTACT] |

---

## 5. Related Documents

| Document | Purpose |
|----------|---------|
| `SECURITY_ESCALATION_MATRIX.md` | Escalation matrix |
| `OUTBOUND_INCIDENT_RESPONSE_AR.md` | Outbound incidents |
| `PRIVACY_INCIDENT_RESPONSE_AR.md` | Privacy incidents |

---

*Runbook maintained by Agent #5 — Security Red Team*
