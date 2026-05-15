# Onboarding Playbook (Revenue OS)

## Outcome

Bring one tenant live with governed workflow controls.

## Steps

1. Create tenant and role assignments.
2. Configure RBAC and approval rule.
3. Connect CRM integration in controlled mode.
4. Validate workflow and observability plumbing.
5. Run first supervised production batch.

## Mandatory Checks

- `tenant_id` propagated across all steps.
- High-risk actions blocked without approval.
- Audit logs visible with trace links.

## Exit Criteria

- 1 tenant live
- 3 users active
- 2 roles enforced
- First approved CRM update completed
