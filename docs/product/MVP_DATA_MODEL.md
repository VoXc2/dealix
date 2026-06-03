# MVP Data Model (Concept)

Objects/tables for the first product spine:

```text
Client
Project
ServicePackage
DataSource
Dataset
Record
Account
Opportunity
Draft
Workflow
Approval
GovernanceEvent
AuditEvent
ProofEvent
Report
CapitalAsset
FeatureCandidate
```

## Relationships

```text
Client has Projects
Project has ServicePackage
Project has DataSources
Dataset has Records
Record can become Account
Account can become Opportunity
Draft belongs to Account / Project
GovernanceEvent belongs to Project
ProofEvent belongs to Project
CapitalAsset created from Project
FeatureCandidate created from repeated task
```

Deeper schema draft: [`ADVANCED_DATA_MODEL.md`](ADVANCED_DATA_MODEL.md).
