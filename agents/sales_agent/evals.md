# sales_agent Evaluation Spec

## Evaluation Objectives

1. Task Quality
2. Governance Compliance
3. Operational Reliability
4. Business Impact Signal

## Core Metrics

### Task Quality

- Qualification correctness (human-reviewed sample)
- Score calibration quality
- Response draft relevance and clarity

### Governance Compliance

- Percent of actions with risk classification
- Percent of high-risk actions with valid approval
- Audit completeness rate

### Operational Reliability

- End-to-end workflow success rate
- Retry recovery rate
- Mean processing time per lead

### Business Impact

- Lead progression rate to next stage
- Time-to-first-response reduction
- Suggested-response acceptance rate by operators

## Eval Cadence

- Daily: reliability and governance checks.
- Weekly: quality review with sampled leads.
- Monthly: impact rollup tied to ROI report.

## Pass/Fail Gate (Minimum)

- Governance compliance >= 99%
- Workflow success >= 95%
- Audit completeness = 100%
- No critical policy bypass
