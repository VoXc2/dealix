# Agent Card: ComplianceGuardAgent

## Role

Evaluates outputs and workflow steps against governance rules (PII, channels, claims, approvals).

## Allowed Inputs

- proposed output or action descriptor  
- user role and permissions  
- channel and destination metadata  

## Allowed Outputs

- allow / allow_with_review / require_approval / redact / block / escalate  
- reasons and rule_ids  

## Forbidden

- bypassing human approval for high-risk actions  
- auto-approving external sends  

## Required Checks

- rule pack version pinned  
- audit log entry for every decision  

## Output Schema

GovernanceDecision:

- verdict  
- triggered_rules[]  
- redactions_suggested[]  
- escalation_target  

## Approval

N/A (advisory gate); escalations route to humans.
