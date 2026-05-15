# Dealix Governed Workflow Engine (Foundation)

This directory documents the execution-fabric layer described in the master blueprint:

1. trigger
2. steps
3. tool calls
4. retries
5. risk checks
6. approval checks
7. execution
8. metrics
9. audit logs

Current implementation:

- Runtime module: `auto_client_acquisition/workflow_engine/governed_runtime.py`
- First governed workflow: `workflows/sales/lead_qualification.workflow.yaml`

Design rule:

- Start with the smallest governed workflow that produces measurable operational value.
- Expand breadth (more workflows/integrations) only after operational reliability is proven.
