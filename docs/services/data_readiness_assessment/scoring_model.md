# Data Readiness Score Model

Weights sum to **100**. Tune after calibration on real engagements.

| Dimension | Weight | What “good” means |
|-----------|-------:|---------------------|
| Source coverage | 20 | Key entities have authoritative source |
| Completeness | 20 | Critical fields populated; missingness measured |
| Consistency | 15 | IDs, enums, duplicates under control |
| Freshness | 10 | Data age matches decision cadence |
| PII handling | 15 | Lawful basis, minimization, redaction path |
| Access clarity | 10 | Who can export what, how often |
| Business mapping | 10 | Fields map to decisions / KPIs |

## Output bands (example)

| Score | Meaning |
|-------|---------|
| 80+ | Ready for **targeted** AI sprints with governance |
| 60–79 | AI-assisted **with** remediation plan |
| 40–59 | **Readiness / cleanup** first |
| <40 | High risk—narrow scope or diagnostic-only |

Document assumptions in the delivery report.
