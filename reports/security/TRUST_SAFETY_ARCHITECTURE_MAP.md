# Trust Safety Architecture Map
## خريطة بنية الثقة والأمان

**Document Type:** Architecture Report
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Overview

This document maps all trust, safety, and security components across the Dealix system, showing how they interact to create defense in depth.

---

## 2. Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SOURCES                               │
│  Website | Email | GitHub | CRM | WhatsApp | Files | APIs       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INPUT LAYER                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ UNTRUSTED INPUT CLASSIFICATION                            │   │
│  │ Website → DATA | Email → DATA | GitHub → DATA            │   │
│  │ CRM → DATA | WhatsApp → DATA | Files → DATA              │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PII REDACTION                                            │   │
│  │ redact_text() → [REDACTED_PHONE] | [REDACTED_EMAIL]     │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ INJECTION DETECTION                                       │   │
│  │ Block: system: | ignore previous | curl | exec(         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ AGENT GOVERANCE (auto_client_acquisition/governance_os/) │   │
│  │ no_cold_whatsapp | no_linkedin_automation | no_scraping  │   │
│  │ claim_safety | approval_matrix | draft_gate               │   │
│  │ channel_policy | workflow_control | pii_requires_review    │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ AGENT OUTPUT CONTRACT                                     │   │
│  │ summary | risk_level | approval_required | external_action │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TOOL LAYER                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ MCP SERVER (mcp_server/dealix_mcp.py)                   │   │
│  │ T0-T1: Read tools (safe) | T2: Draft tools (safe)       │   │
│  │ Doctrine enforced: No external send                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ TOOL INPUT FIREWALL                                       │   │
│  │ Validate: secrets | injection | commands | PII              │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ TOOL OUTPUT FIREWALL                                      │   │
│  │ Sanitize: secrets | PII | external_mark                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   APPROVAL LAYER                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ APPROVAL MATRIX (approval_matrix.py)                     │   │
│  │ WhatsApp → high | Email → medium | LinkedIn → blocked   │   │
│  │ Pricing → founder | Payment → founder | Legal → founder  │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ WHATSAPP APPROVAL FLOW                                    │   │
│  │ Consent verified | Human handoff | No API keys            │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ OUTBOUND APPROVAL FLOW                                    │   │
│  │ Unsubscribe | No fake Re:/Fwd | Evidence level           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL ACTIONS                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ EMAIL (blocked by default)                               │   │
│  │ dry_run=true | Founder approval | Trust gates             │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ WHATSAPP (blocked by default)                            │   │
│  │ No cold WhatsApp | Consent required | Human handoff       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ LINKEDIN (BLOCKED)                                       │   │
│  │ No automation ever                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PRODUCTION DEPLOY (approval required)                     │   │
│  │ agentic-security-gate.yml | Founder approval             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Security Controls

### 3.1 Preventive Controls

| Control | Location | Coverage |
|---------|----------|----------|
| Input classification | UNTRUSTED_INPUT_POLICY.md | All external inputs |
| PII redaction | redact_text() | Phones, emails |
| Injection detection | PROMPT_INJECTION_BOUNDARIES.md | Website, email, GitHub |
| SSRF guard | api/security/ssrf_guard.py | External URLs |
| Secrets scanning | gitleaks + detect-secrets | Code, logs |
| CodeQL | security.yml | Vulnerabilities |
| Dependency review | security.yml | Vulnerable deps |
| Approval matrix | approval_matrix.py | All external actions |
| Channel policy | channel_policy.py | Outbound channels |
| Claim safety | claim_safety.py | Commercial claims |
| No cold WhatsApp | no_cold_whatsapp rule | WhatsApp |
| No LinkedIn | no_linkedin_automation rule | LinkedIn |

### 3.2 Detective Controls

| Control | Location | Coverage |
|---------|----------|----------|
| Security tests | test_engine12_security_v1.py | SSRF, deliverability |
| Injection tests | test_v7_prompt_injection_resistance.py | Injection resistance |
| WhatsApp tests | test_whatsapp_*.py | WhatsApp safety |
| Secrets tests | test_billing_moyasar_safety.py | Secrets in modules |
| Cold WhatsApp tests | test_no_cold_whatsapp.py | Cold WhatsApp |

### 3.3 Corrective Controls

| Control | Location | Coverage |
|---------|----------|----------|
| Secret rotation | KEY_ROTATION.md | Leaked secrets |
| Incident response | SECURITY_RUNBOOK.md | All incidents |
| Workflow rollback | UNTRUSTED_GITHUB_EVENT_POLICY.md | Workflow violations |

---

## 4. Governance Rules Summary

From `auto_client_acquisition/governance_os/`:

| Rule | Implementation | Status |
|------|---------------|--------|
| No cold WhatsApp | `no_cold_whatsapp.py` + `draft_gate.py` | ✅ |
| No LinkedIn automation | `no_linkedin_automation.py` | ✅ |
| No scraping | `no_scraping.py` | ✅ |
| Claim safety | `claim_safety.py` | ✅ |
| External action approval | `approval_matrix.py` | ✅ |
| Draft gate | `draft_gate.py` | ✅ |
| Workflow control | `workflow_control_registry.py` | ✅ |
| Channel policy | `channel_policy.py` | ✅ |
| PII requires review | `pii_requires_review.py` | ✅ |
| No guaranteed claims | `no_guaranteed_claims.py` | ✅ |
| External action requires approval | `external_action_requires_approval.py` | ✅ |

---

## 5. Test Coverage Map

| Test File | Coverage |
|-----------|----------|
| `test_engine12_security_v1.py` | SSRF guard (9 tests), Email deliverability (8 tests) |
| `test_v7_prompt_injection_resistance.py` | WorkforceGoal injection (1), redact_text (1), apply_policy (1) |
| `test_no_cold_whatsapp.py` | Cold WhatsApp policy (1) |
| `test_billing_moyasar_safety.py` | No secrets in pricing (3) |
| `test_whatsapp_webhook_integration.py` | WhatsApp webhook |
| `test_whatsapp_signature.py` | WhatsApp signature |
| `test_whatsapp_safe_send_v14.py` | WhatsApp safe send |
| `test_whatsapp_policy.py` | WhatsApp policy |
| `test_whatsapp_full_ops.py` | WhatsApp full ops |
| `test_whatsapp_decision_layer_v2.py` | WhatsApp decision |
| `test_whatsapp_cards.py` | WhatsApp cards |

---

## 6. GitHub Actions Security

| Workflow | Permissions | Classification |
|----------|-------------|----------------|
| `security.yml` | `contents: read`, `security-events: write`, `pull-requests: read` | ✅ SAFE |
| `repository-hardening.yml` | `contents: read`, `security-events: write` | ✅ SAFE |
| `founder_commercial_daily.yml` | `contents: read` | ✅ SAFE |
| `governed-full-ops-daily.yml` | `contents: read` | ✅ SAFE |
| `hermes-revenue-growth-os.yml` | `contents: read` | ✅ SAFE |
| `codeql.yml` | `contents: read`, `security-events: write` | ✅ SAFE |

---

## 7. Evidence Levels

| Level | Definition | Use Case |
|-------|------------|----------|
| L0 | Assumption | Early exploration |
| L1 | Internal doc/template | Initial drafts |
| L2 | Script/test output | Validation |
| L3 | Staging/demo signal | Proof of concept |
| L4 | Prospect engagement | Sales proposal |
| L5 | Paid/revenue | Customer evidence |

---

*Map maintained by Agent #5 — Security Red Team*
