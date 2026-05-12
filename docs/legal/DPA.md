# Data Processing Agreement — Dealix (template)

> **Important.** This document is a template authored by the platform
> team to capture the *current* operational reality of Dealix as a
> processor. Counsel must approve the production version before
> sending it to a customer. Where the template says **[customer]**,
> the executed copy substitutes the customer's legal name.

## 1. Parties

| Party | Role under PDPL & GDPR | Address |
| --- | --- | --- |
| AI Company Saudi Arabia ("Dealix") | Processor (sub-processor when nested) | Riyadh, KSA |
| **[customer]** | Controller | as specified in the signed order form |

## 2. Subject matter

Dealix processes Personal Data on behalf of **[customer]** to deliver
the Services (lead capture, scoring, outreach, customer-success
automation, audit logging, e-invoicing) defined in the Order Form.

## 3. Duration

This DPA enters into effect on the Order Form effective date and
continues for the duration of the Services plus the retention windows
defined in §11.

## 4. Nature and purpose of processing

| Activity | Personal data | Purpose |
| --- | --- | --- |
| Lead capture | name, email, phone | Customer's outbound sales motion. |
| Lead enrichment | firmographic + person data via Apollo / Clearbit / Wathq | Quality scoring; only when the controller activates the chain. |
| Outreach drafting | name, email, locale | LLM-drafted Arabic/English messages on the controller's behalf. |
| Audit logging | tenant_id, user_id, IP, user-agent | PDPL Article 18 compliance. |
| Billing | corporate contact + VAT/CR | ZATCA invoicing + payment. |

## 5. Categories of data subjects

End-customers and prospects of **[customer]**; their employees; the
controller's own staff configured as Dealix users.

## 6. Controller instructions

Dealix processes Personal Data only on the controller's documented
instructions, including transfers, except as required by Saudi PDPL,
the GDPR, or other applicable law. Instructions are deemed delivered
via:

- The Order Form.
- The settings exposed by the Customer Portal.
- Written communication via `support@ai-company.sa`.

## 7. Confidentiality

Personnel with access to Personal Data are bound by written
confidentiality obligations and trained on PDPL + Dealix's security
policies.

## 8. Security measures

Dealix implements technical and organizational measures including:

- Tenant isolation (`api/middleware/tenant_isolation.py`).
- Field-level redaction (`api/middleware/bopla_redaction.py`).
- Encryption in transit (TLS) and at rest (provider-managed).
- Role-based access control (`api/security/rbac.py`,
  `cerbos/policies/dealix_resources.yaml`).
- Audit log retention (`AuditLogRecord`).
- Quarterly DR drill (`scripts/infra/dr_restore_drill.sh`).
- Per-tenant LLM cost guardrails (`core/llm/cost_guard.py`).
- PII redaction on LLM outputs (`core/llm/guardrails.py`).
- Secret management via Infisical (`dealix/integrations/infisical_client.py`).

Full controls list: `docs/compliance/CONTROLS.md`.

## 9. Sub-processors

Authorised sub-processors are listed at
[/trust/sub-processors](../../landing/trust/sub-processors.html) and in
`docs/compliance/SUB_PROCESSORS.md`. Adding a sub-processor triggers a
30-day notification with right of objection.

## 10. Data-subject requests

Dealix provides the PDPL DSR API (`/api/v1/pdpl/dsr/*`) so the
controller can satisfy access, deletion, and portability requests
through self-service.

## 11. Retention

| Category | Default retention |
| --- | --- |
| Audit logs | 7 years (regulatory). |
| Customer records | Duration of contract + 12 months. |
| Lead records | Per controller's configured suppression / opt-out windows. |
| Invoices | 10 years (Saudi tax law). |
| LLM call logs | 90 days (cost analytics) — content is not retained. |

## 12. Cross-border transfers

Some sub-processors are located outside Saudi Arabia. Transfers are
governed by the Cross-Border Transfer Addendum at
`docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, executed alongside this DPA.

## 13. Incident notification

Dealix notifies the controller within 72 hours of becoming aware of a
Personal Data breach. The notification includes the categories of
data subjects affected, an approximate count, likely consequences,
and the mitigation plan.

## 14. Audits

The controller may, no more than once per calendar year, request
documentation of Dealix's security posture (latest SOC 2 report when
available; controls map and audit log samples in the interim).

## 15. Termination

On termination, Dealix returns or deletes Personal Data within 30
days, except where law requires extended retention.

## 16. Governing law

Saudi Arabian law governs this DPA, without prejudice to the GDPR
where applicable to **[customer]** operations in the EU/EEA.

## 17. Signatures

| Party | Name | Title | Date | Signature |
| --- | --- | --- | --- | --- |
| Dealix | Sami Assiri | Founder | | |
| **[customer]** | | | | |
