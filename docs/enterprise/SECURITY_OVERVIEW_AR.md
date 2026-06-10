# Security Overview — Dealix (AR)

> **لـ:** CISO, Security procurement, vendor due diligence.
> **Companion to:** `docs/security/SECURITY_RUNBOOK.md`, `docs/governance/AI_USAGE_POLICY.md`.

---

## 1. Security Posture (ملخص)

| Domain | Status | Next milestone |
|--------|--------|----------------|
| Identity & Access | Basic (API keys + admin key) | RBAC + SSO في E3 |
| Secrets management | Env vars + .gitignore | Vault / Doppler في E3 |
| Network | HTTPS via reverse proxy | WAF + rate limit في E3 |
| Application | FastAPI, Pydantic, dependency audit شهري | Pen-test في E4 |
| Data | Postgres at-rest (provider default) | Encryption CMK في E4 |
| AI | Allowlist + audit + no auto-execute | Eval suite + red team في E4 |
| Incident response | Documented (runbook) | Tested drill في E3 |
| Logging | Structured JSON, audit append-only | SIEM في E4 |
| Backups | Provider-managed | Tested restore drill في E3 |
| BCP / DR | In design | Documented in E3 |

## 2. Threats المعرّفة و المعالجة

| Threat | كيف نعالجه |
|--------|-----------|
| Prompt injection | Structural delimiters, allowlist actions، untrusted data isolation (راجع `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`) |
| Secrets in logs | Redaction middleware + audit scan |
| SSRF | Output validation + allowlist hosts |
| Auth bypass | Pydantic schemas + admin API key |
| SQL injection | ORM + parameterized queries |
| Dependency CVEs | `pip-audit` شهري + Dependabot |
| Privilege escalation | No root containers, read-only FS where possible |
| Data exfiltration | Network egress allowlist + per-tenant scoping |
| Insider misuse | Audit trail + dual-control for sensitive ops |

## 3. Access Control

- **Humans:** API key + env (`DEALIX_ADMIN_API_KEY`)
- **Agents:** Service tokens مقيدة بـ `paths_allowed` (راجع security framework)
- **Clients:** Portal session tokens، محدودة الصلاحية، revocable
- **Partners:** Read-only tokens بمدى محدد

## 4. Cryptography

| Use | Method |
|-----|--------|
| In-transit | TLS 1.2+ (managed by Railway / Caddy) |
| At-rest (DB) | Provider-managed disk encryption |
| At-rest (secrets) | Env vars (production: Doppler/Vault مُخطط) |
| Field-level PII | (مُخطط في E4) |

## 5. Vulnerability Management

- **SCA:** `pip-audit` monthly + CI on PR
- **Container:** Trivy على base images
- **Secrets scan:** Gitleaks في pre-commit + CI
- **Pen-test:** مُخطط E4 مع طرف ثالث
- **Bug bounty:** (مُخطط بعد E5)

## 6. Logging & Monitoring

- **Structured logs:** JSON to stdout → Railway
- **Audit events:** `data/governance/audit_events.jsonl` (append-only)
- **Metrics:** FastAPI middleware → `/metrics`
- **Alerts:** rate limit violations, auth failures, schema failures

## 7. Incident Response

راجع `docs/security/SECURITY_RUNBOOK.md` للـ:
- Severity classification
- Containment steps
- Customer notification template
- Post-mortem template

## 8. AI-Specific Security

- **No auto-execute:** أي side effect يحتاج approval
- **Model allowlist:** نماذج مُدارة فقط، لا custom training على client data بدون DPA
- **Input isolation:** T3/T4 = data only
- **Eval suite:** تنحفظ في `data/ai_ops/eval_results.jsonl`
- **Red team:** `docs/security/RED_TEAM_SYSTEM.md` (يوجد) — يُحدّث كل ربع سنة

## 9. ما لا نقدّمه حالياً (Honest Disclosures)

- ❌ SOC2 Type II (نعمل عليه ضمن E4 roadmap)
- ❌ ISO 27001 (post-E5)
- ❌ PCI DSS (لا نتعامل مع card data مباشرة)
- ❌ HIPAA (لا PHI حتى إشعار آخر)
- ❌ Sovereign on-prem (نقبل كـ partnership في E5)

## 10. Customer Responsibilities (Shared Model)

| العميل مسؤول | Dealix مسؤول |
|--------------|--------------|
| Account credential security | Platform security |
| User permission grants | Data encryption |
| Legal basis for processing | Breach notification |
| Opt-out management | Audit availability |
| Acceptable use policy | Service availability per SLO |

---

> **Owner:** Founder + (يُعيَّن) Security Officer · **Review:** كل 90 يوم
