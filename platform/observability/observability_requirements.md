# Observability Requirements (Enterprise Readiness)

## Required Signals

1. **Traces**: cross-service and cross-layer workflow execution.
2. **Metrics**: reliability, governance, quality, and business impact.
3. **Logs**: structured, policy-safe, correlated with traces.

## Mandatory Metrics

### Reliability
- workflow_success_rate
- workflow_failure_rate
- workflow_p95_latency_seconds
- retry_rate

### Governance
- approval_required_rate
- approval_bypass_attempt_count
- policy_deny_rate

### Quality/Evals
- response_quality_score
- policy_compliance_score
- citation_coverage_rate

### Business Impact
- qualified_leads_count
- crm_update_success_rate
- conversion_proxy_score

## Readiness Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-OBS-001 | all governed workflows emit trace ids | T-OBS-001 |
| G-OBS-002 | all critical actions emit audit-correlated logs | T-OBS-002 |
| G-OBS-003 | reliability and governance alerts configured | T-OBS-003 |
| G-OBS-004 | incident response playbook linked and tested | T-OBS-004 |

## Data Hygiene

- No sensitive secrets in plain logs.
- PII logging minimized and masked by policy.
- Retention policies enforced per environment and tenant obligations.
