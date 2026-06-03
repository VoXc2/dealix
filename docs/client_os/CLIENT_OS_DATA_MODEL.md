# Client OS Data Model

```text
Client
Workspace
Capability
Project
DataSource
SourcePassport
Dataset
Workflow
Output
Draft
Approval
AuditEvent
ProofEvent
ValueEvent
NextAction
RetainerRecommendation
```

## علاقات موجزة

Client has Workspace · Workspace has Projects · Project uses DataSources · DataSource has SourcePassport · Workflow produces Outputs · Output يتطلب GovernanceDecision وقد يتطلب Approval · ProofEvent / ValueEvent · NextAction من ProofPack.

**صعود:** [`CLIENT_OS_METRICS.md`](CLIENT_OS_METRICS.md)
