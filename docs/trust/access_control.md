---
title: Dealix Access Control & Identity (Saudi Enterprise)
doc_id: W3.T07d.access-control
owner: CTO
status: draft
last_reviewed: 2026-05-13
audience: [customer, partner, internal]
language: en
ar_companion: docs/trust/access_control.ar.md
related: [W0.T00, W3.T07a, W3.T07b, W3.T07c, W3.T15]
kpi:
  metric: enterprise_sso_adoption_percent
  target: 90
  window: 90d
rice:
  reach: 70
  impact: 3
  confidence: 0.9
  effort: 2
  score: 94
---

# Dealix Access Control & Identity

## 1. Context

Saudi enterprise security teams treat identity and access management (IAM) as the single highest-value control after data residency. SAMA's Cyber Security Framework, NCA Essential Controls, and the practical realities of distributed enterprise teams in the Kingdom — frequent contractor turnover, multi-entity customers (group holding structure), and the need to onboard implementation-partner staff — make IAM the most frequently negotiated section of the MSA. This document describes the access-control controls Dealix offers customers and the operational discipline Dealix applies to itself.

The internal references that authorise the claims in this document are the Dealix security runbooks (`docs/SECURITY_GUIDE.md`, `docs/SECURITY_RUNBOOK.md`, `docs/SECURITY_PDPL_CHECKLIST.md`), the planned multi-tenant isolation Architectural Decision Record (`docs/adr/0003-multi-tenant-isolation.md` — pending; tracked under the architectural backlog), and the engineering wiring map (`docs/FRONTEND_BACKEND_WIRING_MAP.md`).

## 2. Audience

- Customer security and IAM teams negotiating SSO/MFA enforcement.
- Customer auditors validating access controls.
- Procurement teams populating IAM sections of vendor questionnaires.
- Dealix engineering, support, and partner-enablement teams.

## 3. Decisions & Content

### 3.1 Identity Federation

Dealix supports enterprise identity federation through both SAML 2.0 and OpenID Connect (OIDC). Tested identity providers include Microsoft Entra ID (Azure AD), Okta, Ping Identity, Google Workspace, and JumpCloud. Saudi-specific configurations have been validated against Microsoft Entra ID tenants registered in Saudi-eligible regions and against on-prem ADFS gateways behind customer-controlled reverse proxies. Just-in-time (JIT) user provisioning is supported via both SAML attribute mapping and SCIM 2.0 for provisioning/de-provisioning; group-to-role mapping is configurable per tenant.

### 3.2 Multi-Factor Authentication

For non-SSO authentication paths, MFA is **enforced by default on all administrative roles** and is configurable as required for all users on the Business and Enterprise plans. Supported factors include TOTP (RFC 6238), WebAuthn/FIDO2 (Yubikey, platform authenticators), SMS as a fallback only for users without device access, and push-based authentication via supported authenticator apps. Customers may set per-role minimum factor strength (e.g., "WebAuthn-only for tenant admins").

### 3.3 Role-Based Access Control (RBAC)

Dealix ships a baseline RBAC model that customers may extend through custom roles on the Enterprise plan. The baseline roles are:

| Role | Purpose | Default scope |
|---|---|---|
| Tenant Owner | Full administrative control of the tenant | Single tenant |
| Tenant Admin | User & role management, integrations, billing | Single tenant |
| Workspace Admin | Configuration and content management within a workspace | One or more workspaces |
| Sales User | Lead pipeline read/write within assigned territory | Assigned data slice |
| Read-Only Auditor | Read-only across the tenant for audit/compliance | Tenant-wide read |
| API Service Account | Programmatic access via scoped API keys | Scoped to API key permissions |
| Partner Co-Manager | Implementation partner role with delegated authority | Configurable, audit-flagged |

The complete RBAC permission matrix is published in the customer admin console under "Roles & Permissions" and exported in CSV form on request for the customer's audit file.

### 3.4 Tenant Isolation

Dealix is a multi-tenant SaaS. Tenant isolation is enforced at the application layer (mandatory tenant scoping in every persistence query, integration test coverage on cross-tenant query attempts), at the data layer (row-level security policies on shared tables; separate schemas for customer-uploaded content), and at the operational layer (no Dealix engineer routinely operates with cross-tenant query capability). The forthcoming Architectural Decision Record on multi-tenant isolation (`docs/adr/0003-multi-tenant-isolation.md`) will document the binding technical contract. Dedicated single-tenant deployments are available on the Enterprise plan and described in the Enterprise Pack.

### 3.5 Customer Admin Tools

The tenant admin console provides:

- User and role management with audit trail.
- SSO/SCIM configuration self-service.
- MFA policy enforcement (per-role minimum factor).
- Session policy (max session lifetime, idle timeout, re-auth on sensitive action).
- API-key issuance with scoping and rotation.
- IP allowlisting per role on Enterprise plan.
- Audit log viewer with search, filter, and CSV export.
- Sub-processor list and DPA acknowledgement state.

### 3.6 Privileged Access Management (Dealix Internal)

Dealix engineering staff do not have standing access to customer production data. Privileged access is granted through a documented **just-in-time (JIT) access** workflow: the engineer opens a ticket with a customer-linked justification, an approver outside the engineer's direct reporting line authorises a time-bound grant (max 8 hours; 30 minutes for routine support), the grant is automatically revoked at expiry, and every action taken under the grant is logged to the immutable audit stream. JIT grants for sub-processor support engagements are reviewed quarterly.

### 3.7 Audit Logging

Security-relevant events — authentication, authorisation decisions, privilege changes, data exports, configuration changes, customer-data access by Dealix staff — are logged to an append-only, integrity-protected audit stream. Retention is **1 year hot, 7 years cold**; cold storage is encrypted and access is restricted to a small set of authorised security and legal personnel. Customer-facing audit exports cover events scoped to the customer's tenant; cross-tenant Dealix-internal audit logs are not exposed but are produced on regulator request under legal process.

### 3.8 Session and API Security

- Session lifetime: 12-hour default, customer-configurable; idle timeout 30 minutes default.
- Re-authentication required for sensitive actions (admin role change, data export over a configured threshold, sub-processor approval).
- API keys: scoped, prefix-tagged for identification, rotatable, expirable, hashed at rest.
- API rate limits enforced per tenant with anomaly alerting on burst behaviour.

### 3.9 Customer-Managed Encryption Keys (BYOK)

Available on the Enterprise plan: customer-managed keys through the cloud provider's KMS, with documented procedures for key rotation, customer-initiated revocation (cryptographic shred), and operational impact transparency. The BYOK contract terms are referenced in the Enterprise MSA (`docs/legal/ENTERPRISE_MSA_TEMPLATE.md`).

### 3.10 Lifecycle Events

- **User onboarding:** SCIM provisioning or self-service SSO JIT; default role per group mapping.
- **Role change:** customer-driven via console; audit-logged.
- **Offboarding:** SCIM de-provisioning revokes within minutes; manual offboarding revokes within 4 working hours of customer notice.
- **Tenant suspension/termination:** documented in MSA termination clause; data export window then irreversible deletion per data governance retention rules.

## 4. KPIs

- **Primary:** 90% of paying enterprise customers using SSO within 90 days of activation.
- 100% of Dealix internal customer-data access via JIT (zero standing access).
- ≥ 99.95% successful authentication availability (rolling 30 days).
- Zero unresolved P1 IAM findings.

## 5. Dependencies

- Publication of `docs/adr/0003-multi-tenant-isolation.md`.
- SCIM connector hardening (engineering backlog).
- Customer-facing audit-log export UX.
- Bilingual admin console.

## 6. Cross-links

- Master plan: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- Pricing (BYOK + Enterprise SSO entitlements): `docs/pricing/pricing_packages_sa.md`
- Security overview: `docs/trust/security_overview.md`
- Data governance: `docs/trust/data_governance.md`
- Incident response: `docs/trust/incident_response.md`
- Enterprise procurement: `docs/procurement/enterprise_pack.md`
- Internal: `docs/SECURITY_GUIDE.md`, `docs/FRONTEND_BACKEND_WIRING_MAP.md`
- Risk register: `docs/legal/enterprise_risk_register.md`
- Architecture: `docs/adr/0003-multi-tenant-isolation.md` (pending publication)

## 7. Owner & Review Cadence

- Owner: CTO; co-signed by HoLegal for contractual representations.
- Reviewed every 30 days during GTM window, then quarterly.

## 8. Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-13 | Initial draft (W3.T07d) | CTO |

## 9. External Attestations

| Attestation | Status | Availability |
|---|---|---|
| IAM control narrative (SOC 2 readiness) | Drafted | Under NDA |
| Penetration-test IAM section | Live (annual) | Under NDA |
| Tenant-isolation test report | Targeted Q3 2026 | Under NDA |
