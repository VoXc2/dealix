# Alerting Standard

## Goal

Detect reliability, governance, and business-impact failures early with actionable alerts.

## Alert Classes

1. Reliability alerts (latency, error rate, queue backlog).
2. Governance alerts (approval bypass attempts, policy failures).
3. Data safety alerts (cross-tenant access attempts, citation failure spikes).
4. Business alerts (lead flow stall, CRM sync failure spike).

## Baseline Alert Rules (v1)

| Alert ID | Condition | Severity |
|---|---|---|
| A-REL-001 | workflow failure rate > 5% (15m) | high |
| A-REL-002 | p95 workflow latency > threshold | medium |
| A-GOV-001 | high-risk action executed without approval | critical |
| A-GOV-002 | policy engine unavailable | critical |
| A-DAT-001 | cross-tenant read attempt detected | critical |
| A-BIZ-001 | CRM update failure rate > 3% | high |

## Mandatory Tests

| Test ID | Scenario |
|---|---|
| T-ALT-001 | synthetic workflow failure triggers alert |
| T-ALT-002 | approval bypass simulation triggers critical alert |
| T-ALT-003 | observability pipeline outage triggers incident workflow |

## Incident Integration

Every critical alert must open or link to an incident log with:
- `incident_id`
- owner
- timeline
- impact
- mitigation
- resolution evidence
