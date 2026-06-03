# Prospect Data Classification — Dealix (Phase 8)

Classification of prospect data used for outbound, with handling rules. Aligned with SDAIA PDPL: data minimization, lawful business basis, and no special-category data. No PII in logs or reports. Builds on `company_os/governance/pdpl_checklist.md` and `docs/privacy/SAUDI_PDPL_OUTBOUND_POLICY_AR.md`.

Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

---

## 1. Data Classes

| Class | Definition | Example (safe placeholder) |
|-------|------------|----------------------------|
| Public company data | Publicly available business facts | sector, public company profile |
| Role/business contact | Business contact tied to a function | role mailbox at `optout-example.sa` |
| Derived signal | Inferred pain/buying signal from public info | `lead_leakage` signal on a sector |

> No personal/special-category data is collected. Contacts are business/role-based, not personal profiles.

---

## 2. Handling Rules by Class

| Class | Collect | Store | Use |
|-------|---------|-------|-----|
| Public company data | Public sources only | Minimum fields | Qualification + targeting |
| Role/business contact | First-party/public business sources | Role + domain, minimized | Outreach within plan |
| Derived signal | Inference from public info, cite `evidence_level` | Tied to source record | Personalization (floor `P1`) |

Purchased lists are prohibited for every class. Personalization tiers and evidence levels: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`.

---

## 3. Prohibited Data

| Prohibited | Note |
|------------|------|
| Special-category data (PDPL) | Never collected or stored |
| Personal (non-business) profiles | Out of scope |
| PII in logs/reports | Use role/domain placeholders only |
| Purchased/rented/scraped personal lists | Prohibited |

---

## 4. Lifecycle Links

| Stage | Reference |
|-------|-----------|
| Retention + deletion triggers | `docs/privacy/OUTBOUND_DATA_RETENTION_MATRIX.md` |
| Opt-out / suppression | `docs/privacy/OUTREACH_SUPPRESSION_POLICY_AR.md` |
| Deletion request | `docs/privacy/DELETION_REQUEST_RUNBOOK_AR.md` |
| PDPL outbound policy | `docs/privacy/SAUDI_PDPL_OUTBOUND_POLICY_AR.md` |

---

## 5. Handling Checklist

| Item | Status |
|------|--------|
| Only the 3 defined classes in use | ☐ |
| No special-category data | ☐ |
| Minimized fields only | ☐ |
| No PII in logs/reports | ☐ |
| First-party sourcing only | ☐ |

---

*Dealix · Prospect Data Classification · business/role data only, no special-category data · send_enabled stays false · Ref: SDAIA PDPL*
