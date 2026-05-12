# Vendor security questionnaire — pre-filled answers

> Copy-paste this into the CAIQ / SIG Lite / custom questionnaire
> your prospect sent. Every answer references the code path or
> document that backs it so the buyer can self-verify.

## A — Organisational

| Question | Answer |
| --- | --- |
| Legal entity | Dealix For AI Co. (KSA, MISA licence number on file) |
| Founded | 2025 |
| Headcount | Engineering + founder + ops |
| Sub-processors | Listed at `landing/trust/sub-processors.html` |
| Data residency | KSA-region available for enterprise plans; default EU/US |
| DPA | Template at `docs/legal/DPA.md`, signed copy on request |

## B — Information security policy

| Question | Answer |
| --- | --- |
| Written security policy? | Yes — `AGENTS.md`, `docs/ops/*`, `docs/compliance/CONTROLS.md` |
| Reviewed annually? | Yes; PR-tracked in `docs/adr/` |
| Background checks on staff | Yes (founder + employees) |
| Security training | Quarterly; tracked in OPS_ROTATION.md |

## C — Access control

| Question | Answer |
| --- | --- |
| SSO supported | Yes — WorkOS (SAML + OIDC) |
| SCIM provisioning | Yes — WorkOS Directory Sync |
| MFA required for admin | Yes — TOTP via `pyotp` |
| Password policy | Argon2id; minimum 12 chars |
| Role-based access | Yes — Cerbos policies + JWT scopes |
| Audit log | `db/models.AuditLogRecord`; exportable to CSV + S3 + Datadog + Splunk |

## D — Encryption

| Question | Answer |
| --- | --- |
| At rest | Provider-managed (RDS/Cloud SQL) AES-256; BYOK optional |
| In transit | TLS 1.2+ everywhere |
| BYOK supported | Yes — AWS KMS / GCP KMS / Azure Key Vault |
| Key rotation | Automated quarterly; webhook keys rotatable on demand |

## E — Application security

| Question | Answer |
| --- | --- |
| Pen-test cadence | Annual (Q4 2026 first formal engagement) |
| Vulnerability scanning | Snyk daily + Renovate weekly |
| OWASP Top-10 review | Yes — automated via Semgrep + Bandit |
| Bug bounty | Coordinated via `landing/.well-known/security.txt` |
| AI-safety guardrails | Yes — Lakera / Rebuff + NeMo Guardrails-style runtime |

## F — Operations

| Question | Answer |
| --- | --- |
| Uptime target | 99.5 % (see `docs/sla.md`) |
| RPO | ≤ 24 hours (nightly pg_dump → S3) |
| RTO | ≤ 4 hours for SEV-1 |
| Status page | https://status.dealix.me (BetterStack) |
| Incident response | `docs/ops/incident_response.md`; SEV-1/2/3 escalation |
| DR drill | Quarterly — `scripts/infra/dr_restore_drill.sh` |

## G — Data protection

| Question | Answer |
| --- | --- |
| GDPR DPO | Yes — designated person on file |
| PDPL DPO | Yes — same person; PDPL Article 19 compliant |
| Data subject rights | API at `/api/v1/pdpl/dsr/{export,delete,portability}` |
| Sub-processor list public? | Yes — `landing/trust/sub-processors.html` |
| 30-day right of objection | Yes — fires the `sub_processor_added` Loops event |

## H — Certifications + audits

| Question | Status |
| --- | --- |
| SOC 2 Type I | In progress; target Q3 2026 |
| SOC 2 Type II | Target Q1 2027 |
| ISO 27001:2022 | Aligned; certification target Q4 2026 |
| PCI DSS | Not in scope (Moyasar/Stripe hold the PAN) |
| HIPAA | Not in scope |
| PDPL Saudi | Compliant; ROPA quarterly |

## I — Pricing-relevant questions

| Question | Answer |
| --- | --- |
| Free trial | Yes — 14 days (`api/routers/trial.py`) |
| Annual discount | Yes — 17 % off vs monthly |
| Currency | SAR primary; USD/EUR/AED via Stripe; KWD/BHD/AED via KNET/BENEFIT/Magnati |
| Split-payment | Tabby + Tamara up to 4 instalments |
| Invoice format | ZATCA Phase 2 e-invoice (UBL 2.1) |
