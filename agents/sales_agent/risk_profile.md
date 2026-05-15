# sales_agent Risk Profile

## Risk Categories

1. Data Exposure Risk
2. Decision Quality Risk
3. Execution Risk (CRM updates)
4. Compliance Risk (policy/approval bypass)

## Top Risks and Controls

### R1: Cross-tenant data leakage

- Risk level: Critical
- Controls:
  - mandatory tenant filters
  - access checks per query
  - denied-by-default on missing `tenant_id`

### R2: Hallucinated qualification rationale

- Risk level: High
- Controls:
  - citation requirement for rationale
  - confidence threshold with human fallback
  - sampled weekly quality audits

### R3: Unauthorized CRM modification

- Risk level: High
- Controls:
  - risk score before execution
  - mandatory approval for high-risk actions
  - immutable audit log with approval reference

### R4: Silent operational failures

- Risk level: Medium
- Controls:
  - trace + alerting requirements
  - retry with bounded attempts
  - incident record on retry exhaustion

## Residual Risk Policy

Any unresolved High/Critical risk blocks autonomous execution and forces manual mode.
