# API Governance

Every HTTP **endpoint** must declare behavior before it becomes a “shadow product.”

## Required (per route)

- **purpose**
- **input schema** (body/query; validation rules)
- **output schema** (stable fields for clients if public)
- **auth** requirement (public / user / admin / service)
- **audit** requirement (yes/no + event shape)
- **PII handling** (none / flag / redact / never log raw)
- **error states** (machine-readable codes where possible)
- **tests** (smoke + boundary)

## Example

**`POST /api/v1/data/import-preview`** (illustrative)

| Aspect | Policy |
|--------|--------|
| Purpose | Preview and validate a client dataset before heavy processing |
| Auth | Authenticated client or internal operator |
| Audit | Yes — who uploaded, file hash/filename, row counts (no raw cell PII) |
| PII | Flag columns; do **not** log raw PII lines |
| Errors | missing required column · unsupported encoding · empty file · size limit |

Future consolidation: align with “readiness API” vision in [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).
