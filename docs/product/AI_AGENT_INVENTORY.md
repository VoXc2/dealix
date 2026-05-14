# AI Agent Inventory

| Agent | Capability | Tools | Data Access | Autonomy Level | Risk | Status |
|---|---|---|---|---:|---|---|
| DataQualityAgent | Data | data_os | datasets | 1 | Medium | MVP |
| RevenueAgent | Revenue | revenue_os | accounts | 2 | Medium | MVP |
| OutreachAgent | Revenue | drafts only | accounts + offer | 2 | High | MVP |
| KnowledgeAgent | Knowledge | retrieval | approved docs | 2 | High | Beta |
| ComplianceGuardAgent | Governance | governance_os | metadata | 3 | High | MVP |
| ReportingAgent | Reporting | reporting_os | project outputs | 2 | Medium | MVP |

## Autonomy Levels

```text
0 = passive helper
1 = analyze
2 = draft/recommend
3 = queue action for approval
4 = execute internal action
5 = external action
6 = autonomous external action
```

## Dealix MVP Rule

```text
Allowed: 0–3
Restricted: 4
Enterprise-only: 5
Forbidden: 6
```
