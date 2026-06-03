# Outbound Data Retention Matrix — Dealix (Phase 8)

Retention matrix for outbound/outreach data, aligned with SDAIA PDPL: data minimization, storage limitation, and right to deletion. No PII in logs or reports. Builds on `company_os/governance/pdpl_checklist.md` and `docs/privacy/SAUDI_PDPL_OUTBOUND_POLICY_AR.md`.

Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

---

## 1. Retention by Data Class

| Data class | Example artifact | Retention period | Deletion trigger |
|------------|------------------|------------------|------------------|
| Public company data | sector, public company profile | While qualified, max 90 days idle | Idle expiry, deletion request |
| Role/business contact | role mailbox, business domain | Active outreach window, max 90 days idle | Opt-out, deletion request, idle expiry |
| Derived signal | inferred pain/buying signal | Tied to source record lifetime | Source deletion, deletion request |
| Suppression entry | domain/email/company + reason | Retained long-term (compliance evidence) | Only with documented justification |
| Sending batch (plan) | planned_count, verdict, status | Operational window + audit need | Superseded plan, audit close |
| Domain health metric | bounce/spam/auth rates (aggregate) | Rolling monitoring window | Rotation; no PII retained |

> 90-day idle deletion aligns with the PDPL checklist (right to destruction). See `company_os/governance/pdpl_checklist.md` §3.

---

## 2. Deletion Triggers (canonical)

| Trigger | Action |
|---------|--------|
| Opt-out / unsubscribe | Add to suppression, delete prospect record |
| Deletion request (data subject) | Run `docs/privacy/DELETION_REQUEST_RUNBOOK_AR.md` |
| Idle expiry (90 days) | Auto-delete prospect/derived data |
| Hard bounce | Suppress + remove dead contact |

Suppression entries persist as compliance evidence even after the contact record is deleted (domain/role only, no PII).

---

## 3. Storage & Minimization Rules

| Rule | Requirement |
|------|-------------|
| Minimization | Store only the minimum fields needed to qualify and contact |
| No special-category data | Never collect PDPL special-category data |
| No PII in logs/reports | Use role/domain placeholders (e.g. `optout-example.sa`) |
| KSA processing | Data processed within KSA; no cross-border transfer |
| Encryption | At rest and in transit (per PDPL checklist §4) |

Data classes defined in `docs/privacy/PROSPECT_DATA_CLASSIFICATION.md`.

---

## 4. Review

| Field | Value |
|-------|-------|
| Review date | `____` |
| Classes over retention | `____` |
| Deletions executed | `____` |
| PII leakage found | `____` (target: none) |

Report into `reports/privacy/OUTBOUND_DATA_MINIMIZATION_REVIEW.md`.

---

*Dealix · Outbound Data Retention Matrix · minimize + delete on trigger · no PII retained · send_enabled stays false · Ref: SDAIA PDPL*
