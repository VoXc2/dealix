# Platform Foundation Lockdown

This directory captures the non-negotiable platform foundation for Dealix Revenue OS:

- tenant isolation as a hard boundary (`tenant_id` first)
- RBAC on every governed workflow step
- append-only audit events for all sensitive operations
- rollback tokens for compensating CRM and external updates

Primary executable reference:

- `dealix/workflows/lead_qualification.py`
- `workflows/lead_qualification.workflow.yaml`
