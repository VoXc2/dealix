# AI Quick Win Sprint — Data Request / طلب البيانات

Send to the customer at the end of Day-1 discovery. Sealed-credentials vault is the only acceptable transfer channel. All artifacts encrypted at rest. Lawful basis (PDPL Art. 5 — contract) recorded.

## Required process inputs / المدخلات المطلوبة

For the ONE selected use case, the customer must supply:

| Input / المدخل | Form | Notes |
|---|---|---|
| Process owner contact | name + email | Single accountable person, signs off on outputs. |
| 5 sample inputs | real or synthetic | Representative — easy, edge, hard, edge-fail, multilingual. |
| 5 desired outputs | exact format | "If input = X, the correct output is Y." |
| System access | sealed-vault creds | Read-only by default; write-back requires explicit Day-2 approval. |
| Trigger spec | cron / event / manual | When the automation must run. |
| Approval map | role -> action | Who signs off on each side-effect (see `dealix/trust/approval_matrix.py`). |
| Definition of "good" | bilingual paragraph | What "success" means at the end of Day 7. |

## Recommended inputs / مفضّل

- Last 30 runs of the process (timestamped) for ROI baseline.
- Error log or rejected samples for failure-mode coverage.
- Bilingual glossary if AR/EN labels diverge.

## Optional inputs / اختياري

- Brand-voice notes for any customer-facing output.
- Existing internal SOP doc (for Knowledge module if RAG-flavored).
- Test environment access to avoid prod side-effects on Day 2–5.

## Provenance rules / قواعد المصدر

1. Inputs that contain PII pass through `dealix/trust/pii_detector.py` before any LLM call.
2. PDPL Art. 13/14 notices are added to any output that touches an external party (email draft, customer message).
3. Side-effect actions (send, update CRM, post) are routed to the approval matrix — no autosend.
4. Every run emits an immutable audit event via `event_store.append_event`.

## Format / الصيغة

- Samples in `.json` or `.csv` (UTF-8, schema documented).
- Sensitive samples may be redacted before upload; document redaction rules.
- File name: `<customer>_<use_case>_samples_<YYYYMMDD>.ext`.

## Hard stops / حدود فاصلة

- Sample size < 5 -> request escalation, no automation built.
- Use case requires autonomous external comms without approval -> route to bespoke Workflow Automation Sprint, not Quick Win.
- Inputs cannot be sufficiently de-PII'd -> add a 1-day data-hygiene step (extra SAR 2,000) or descope.

## Cross-links

- Intake: `docs/services/ai_quick_win_sprint/intake.md`
- Approval matrix: `dealix/trust/approval_matrix.py`
- PII rules: `dealix/trust/pii_detector.py`
- Audit module: `dealix/trust/audit.py`
- Sealed-vault SOP: `docs/SECURITY_GUIDE.md`
- Three starting offers: `docs/strategy/three_starting_offers.md`
