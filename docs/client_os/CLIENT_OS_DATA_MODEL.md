# Client OS Data Model

16 entities + relationships.

## Entities

Client, Workspace, Capability, Project, DataSource, SourcePassport, Dataset, Workflow, Output, Draft, Approval, AuditEvent, ProofEvent, ValueEvent, NextAction, RetainerRecommendation.

## Relationships

```
Client has Workspace
Workspace has Projects
Project uses DataSources
DataSource has SourcePassport
Workflow produces Outputs
Output requires GovernanceDecision
Output may require Approval
ProofEvent belongs to Project
ValueEvent supports ProofEvent
NextAction comes from ProofPack
```

## Principle

> The data model is the boundary between a service repo and an operating system.
