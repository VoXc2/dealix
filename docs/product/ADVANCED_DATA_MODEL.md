# Advanced Data Model (concept)

Target schema when Dealix **productizes** ledgers and readiness—not a migration script yet.

## Core entities (tables/collections)

```text
clients
workspaces
projects
service_packages
requests
decisions
data_sources
datasets
documents
accounts
opportunities
workflows
approvals
ai_runs
qa_reviews
governance_events
proof_events
reports
feature_candidates
playbook_updates
client_health_scores
capability_scores
```

## Key relationships

```text
Client has Workspaces
Workspace has Projects
Project uses ServicePackage
Project has DataSources
Project has GovernanceEvents
Project has QAReviews
Project has ProofEvents
Project updates Playbooks
Project creates FeatureCandidates
Client has CapabilityScores
```

## Why

- Profitability by **service** and **sector**  
- Repeated **risks** and **eval** failures  
- **Retainer** readiness from health + capability trend  
- **Proof** lineage for enterprise buyers  

See [`AI_RUN_LEDGER.md`](../ledgers/AI_RUN_LEDGER.md), [`MANAGEMENT_API_SPEC.md`](MANAGEMENT_API_SPEC.md).
