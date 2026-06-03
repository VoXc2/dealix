# Suppression Review — Dealix (Phase 8)

Report template for reviewing the suppression list. The list is the single legal source that blocks sends and is applied before any plan. No PII in this report: use role/domain placeholders only (e.g. `optout-example.sa`). Defaults stay `dry_run=true`, `approval_required=true`, `send_enabled=false`.

Canonical list: `data/outreach/suppression_list.jsonl` (`schemas/suppression.schema.json`). Policy: `docs/privacy/OUTREACH_SUPPRESSION_POLICY_AR.md`.

---

## 1. Summary

| Field | Value |
|-------|-------|
| Review date | `____` |
| Total entries | `____` |
| New since last review | `____` |
| Removed (with justification) | `____` |
| Applied pre-send | ☐ (must be yes) |

---

## 2. Entries by Type

| Type | Count |
|------|-------|
| domain | `__` |
| email | `__` |
| company | `__` |

---

## 3. Entries by Reason

| Reason | Count |
|--------|-------|
| opt_out_requested | `__` |
| do_not_contact | `__` |
| role_account | `__` |
| competitor | `__` |
| hard_bounce | `__` |
| spam_complaint | `__` |
| manual | `__` |

---

## 4. Integrity Checks

| Check | Status |
|-------|--------|
| Every entry has valid type/value/reason/scope | ☐ |
| No PII in values (role/domain/company only) | ☐ |
| Suppression enforced before every plan | ☐ |
| No re-contact of suppressed addresses | ☐ |
| Removals justified and documented | ☐ |

Linked flows: `docs/outreach/BOUNCE_UNSUBSCRIBE_HANDLING_AR.md`, `docs/privacy/DELETION_REQUEST_RUNBOOK_AR.md`.

---

## 5. Decision

| Field | Value |
|-------|-------|
| List healthy | `____` (yes/no) |
| Actions required | `____` |
| Reviewed by | `____` |

---

*Dealix · Suppression Review · suppression blocks send, applied pre-plan · no PII (role/domain only) · send_enabled stays false · Ref: SDAIA PDPL*
