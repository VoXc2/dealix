---
title: PII Redaction Policy — When, How, Escalation, BYOK
doc_id: W6.T37.pii-redaction
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W3.T07b, W4.T14]
kpi:
  metric: pii_leak_incidents
  target: 0
  window: continuous
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 0.5
  score: governance-foundation
---

# PII Redaction Policy

## 1. Context

PII never appears in customer-facing artifacts, logs, prompts, or downstream
systems beyond the records that legitimately need it. The Trust plane's PII
detector (`dealix/trust/pii_detector.py`) and the underlying Data plane
scanner (`auto_client_acquisition.customer_data_plane.pii_detection`) enforce
this in code. This document describes when redaction is applied, how, and
when escalation is required.

## 2. Audience

Engineers (must call the detector before pass-through), CSMs (must verify
artifacts are PII-clean before send), HoLegal (escalations and BYOK
arrangements).

## 3. Detector Verdicts

The detector returns one of three verdicts per record or batch:

| Verdict | When | Default action |
|---------|------|----------------|
| `CLEAN` | No PII found | Pass through |
| `REDACTED` | PII found, redact policy applies | Redact in place, then pass through |
| `BLOCKED` | Sensitive financial PII (card, IBAN) | Reject — cannot pass through |

`BLOCKED` is a hard stop. There is no override.

## 4. Where Redaction Runs

- **Pre-LLM call**: every record sent to a model is scanned and redacted.
  No raw PII leaves the customer's tenant boundary unless policy permits.
- **Pre-outbound message**: drafts are scanned; PII is redacted or
  replaced with non-identifying tokens.
- **Pre-report generation**: every record referenced in an executive
  artifact is scanned. Reports are PII-free by construction.
- **Pre-log write**: structured logs scrubbed by the logging adapter; the
  Trust plane's policy is `allow_pii_in_logs=False`.

## 5. The `PIIPolicy` Toggles

The `PIIPolicy` model controls behaviour per tenant / scope:

| Toggle | Default | When changed |
|--------|--------|-------------|
| `allow_pii_in_outputs` | `False` | Only for internal Trust admin views; never customer-facing |
| `allow_pii_in_logs` | `False` | Never (no toggle path in production) |
| `redact_in_messages` | `True` | Always — outbound messages are redacted |
| `block_card_iban` | `True` | Always — financial PII is blocked |

Changes to `PIIPolicy` are themselves a policy-relevant event and require
HoLegal sign-off.

## 6. Escalation

A `BLOCKED` verdict on an action path triggers:

1. The action is rejected by Governance OS pre-flight.
2. An event is written to the audit log with the record ID (not the PII
   value).
3. CSM is notified — typically the customer sent a CSV with cards/IBANs
   that should not have been included. CSM contacts the customer to
   remediate at source.
4. If the same source produces repeated BLOCKED verdicts, HoLegal is
   notified — possible misconfiguration in the customer's data export.

## 7. BYOK (Bring Your Own Key) Note

Enterprise customers selecting BYOK ship their own KMS keys for encryption
at rest. PII redaction is still applied — encryption does not eliminate
the obligation to scrub. BYOK arrangements are recorded in the DPA and
the audit trail.

## 8. Anti-Patterns

- **Trust-but-don't-scan**: assuming a customer-supplied dataset has no
  PII because they said so. Always scan.
- **Allow-in-logs for debugging**: never. Use anonymised sample data for
  reproduction.
- **Substring redaction**: regex on email handles can miss novel formats.
  Use the detector library, not ad-hoc regex.

## 9. Cross-links

- Code: `dealix/trust/pii_detector.py`
- Underlying scanner: `auto_client_acquisition/customer_data_plane/pii_detection.py`
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- PDPL rules: [`PDPL_DATA_RULES.md`](PDPL_DATA_RULES.md)
- Approval matrix: [`APPROVAL_MATRIX.md`](APPROVAL_MATRIX.md)
- Data governance: [`../trust/data_governance.md`](../trust/data_governance.md)

## 10. Owner & Review Cadence

- **Owner**: HoLegal (with CTO on enforcement code).
- **Review**: quarterly; immediate on any detector miss in production.

## 11. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial verdicts + policy toggles + BYOK note |
