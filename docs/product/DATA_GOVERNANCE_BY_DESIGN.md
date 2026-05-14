# Data Governance by Design

Every **dataset** processed for AI ops carries explicit metadata—traditional data management is not enough when models amplify error and leakage ([Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk)).

## Required metadata

- **source** (system, export, manual upload)
- **owner** (client DRI)
- **purpose** (proportionality)
- **sensitivity** (public / internal / confidential / regulated)
- **retention** (align with [`../governance/DATA_RETENTION.md`](../governance/DATA_RETENTION.md))
- **allowed uses** (model training? reporting? drafts only?)
- **blocked uses** (e.g. resale, unapproved outbound)
- **lawful basis** if personal data exists (PDPL)
- **redaction status** (raw / redacted / synthetic)

## Dealix default

- Client-provided **only** unless contract says otherwise
- **Minimize** PII; prefer aggregates in client-facing reports
- Log **governance decisions** in [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md)
