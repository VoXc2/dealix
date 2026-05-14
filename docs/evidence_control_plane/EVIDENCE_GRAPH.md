# Evidence Graph

Nodes: Client, Project, Source, Dataset, Agent, AI Run, Policy Check, Governance Decision, Human Review, Approval, Output, Proof Event, Value Event, Risk Event, Decision.

Edges: Source `used_by` AI Run; AI Run `produced` Output; Output `checked_by` Governance Decision; Governance Decision `requires` Approval; Approval `authorizes` Output; Output `supports` Proof Event; Proof Event `supports` Value Event; Risk Event `updates` Policy; Value Event `triggers` Board Decision.
