# Autonomy Validation Gates

Agents must pass validation based on intended autonomy.

## Level 0 — Read

Can read allowed data.  
**Required:** access check, logging.

## Level 1 — Analyze

Can classify, summarize, extract.  
**Required:** schema validation, sample QA.

## Level 2 — Draft / Recommend

Can create drafts or recommendations.  
**Required:** QA review, forbidden claims check, human review before delivery.

## Level 3 — Queue for Approval

Can prepare action for approval.  
**Required:** approval workflow, audit log, owner confirmation.

## Level 4 — Execute Internal

Can update internal system after approval.  
**Required:** role permission, rollback plan, audit trail, incident response.

## Level 5 — Execute External

Can send/publish/contact after explicit approval.  
**Required:** enterprise controls, consent/lawful basis, approval record, rollback/mitigation plan.

## Level 6 — Autonomous External

Not allowed in Dealix standard.
