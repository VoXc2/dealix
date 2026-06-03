# Management API Spec (design)

Turn **management** into software: readiness, requests, governance, quality, proof, learning. Paths are **indicative**—normalize under `/api/v1/` when implementing.

## Readiness

- `GET /readiness/company`  
- `GET /readiness/services`  
- `POST /readiness/service-score`  

## Requests

- `POST /requests`  
- `GET /requests`  
- `POST /requests/{id}/decision`  

## Clients

- `POST /clients`  
- `GET /clients/{id}/health`  
- `GET /clients/{id}/capability-roadmap`  

## Governance

- `POST /governance/check`  
- `POST /governance/approval`  
- `GET /governance/events`  

## Quality

- `POST /quality/score`  
- `GET /quality/reviews`  

## Proof

- `POST /proof-pack/generate`  
- `GET /proof-ledger`  

## Learning

- `POST /post-project-review`  
- `GET /feature-candidates`  

**Auth / audit / PII:** every route must satisfy [`API_GOVERNANCE.md`](API_GOVERNANCE.md), [`RUNTIME_GOVERNANCE.md`](../governance/RUNTIME_GOVERNANCE.md), [`DATA_GOVERNANCE_BY_DESIGN.md`](DATA_GOVERNANCE_BY_DESIGN.md).
