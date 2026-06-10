# Dealix Risk Register

Review **monthly** (or after any incident): add risks, validate controls, close or adjust.

| Risk | Severity | Services affected | Control | Status |
|------|----------|-------------------|---------|--------|
| PII leak | High | all | redaction + audit + least-privilege access | active |
| Unsupported claims | Medium | marketing / revenue narratives | draft gate + manual review | active |
| Bad data quality | High | all | data readiness gate; no “full auto” before review | active |
| Scope creep | Medium | all | written scope; change log | active |
| Hallucinated answers | High | Company Brain / RAG | no-source-no-answer; citations | active |
| Unsafe outreach | High | revenue / growth workflows | forbidden actions + approval matrix | active |
| Client no owner | Medium | all | qualification score; stop if no DRI | active |
| Partner / new hire bypasses process | Medium | all | training + audit + DoD | active |
| Vendor / LLM leakage misconfiguration | High | product | secrets policy; logging redaction | active |

**Escalation:** document in `clients/<client>/governance_events.md` and roll lessons into this table.

Related: `docs/governance/FORBIDDEN_ACTIONS.md`, `docs/audit/GOVERNANCE_AUDIT.md`.
