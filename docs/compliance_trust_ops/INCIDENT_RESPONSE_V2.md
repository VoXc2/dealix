# Incident Response v2

## أنواع

PII exposure · unsupported claim · source misuse · wrong client data · unapproved external action · hallucinated answer · partner violation · agent tool misuse.

## تدفق

Detect → Contain → Owner → Severity → Notify → Correct → Log → Rule → Test → Checklist/Trust Pack.

## قاعدة ذهبية

```text
Every incident must produce a rule, test, or checklist.
```

**الكود:** `COMPLIANCE_INCIDENT_TYPES` · `incident_closure_requires_artifact` — `compliance_trust_os/incident_response.py`

**صعود:** [`REGULATORY_READINESS.md`](REGULATORY_READINESS.md)
