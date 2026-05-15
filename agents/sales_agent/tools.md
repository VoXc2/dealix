# sales_agent Tools Contract

## Primary Tools

1. `lead_ingest_tool`
   - Validate and normalize lead input.

2. `tenant_retrieval_tool`
   - Retrieve tenant-scoped knowledge with citation metadata.

3. `qualification_tool`
   - Produce qualification rubric outcome.

4. `scoring_tool`
   - Produce lead score and confidence.

5. `response_draft_tool`
   - Draft suggested response in internal format.

6. `approval_pack_tool`
   - Build approval request with risk context and rationale.

7. `crm_sync_tool`
   - Write to CRM only after approval requirements pass.

8. `audit_log_tool`
   - Persist governance and execution records.

## Tool Guardrails

- Every tool call carries `tenant_id`.
- Retrieval calls must include permission filters.
- CRM tool requires `approval_ref` for high-risk operations.
- All tool outputs include `trace_id` and `run_id`.

## Failure Strategy

- Retry up to configured limit for transient failures.
- For governance failures, stop and return `blocked` state.
- For CRM failures after approval, create incident + retry plan.
