# Architecture Governance

Every technical **module** must be intentional—no orphan code paths.

## Required fields (per module)

- **purpose**
- **service(s) supported**
- **owner** (human DRI)
- **inputs**
- **outputs**
- **tests** (or explicit risk acceptance)
- **risks** (PII, cost, misuse)
- **logging / audit** (when actions are sensitive)
- **future path** (deprecate / promote to SaaS)

## Example — Data OS (illustrative)

| Field | Content |
|-------|---------|
| Purpose | Prepare client data for AI operations safely |
| Supports | Lead Intelligence, readiness reviews, cleanup sprints |
| Inputs | CSV, spreadsheet, CRM export (client-provided) |
| Outputs | Import preview, data quality score, PII flags, source report |
| Tests | `tests/test_data_os_helpers.py` (etc.) |
| Risks | PII leakage, wrong lawful basis assumed |
| Logging | Redact PII; no raw dumps in logs |

Link modules: [`MODULE_MAP.md`](MODULE_MAP.md), [`CAPABILITY_MATRIX.md`](CAPABILITY_MATRIX.md).
