# Workflow Engine Layer — architecture

- Layer ID: `workflows`
- Owner: `Delivery + Platform`
- Purpose: Operate this layer as an enterprise-safe building block, not a feature silo.
- Core responsibilities:
  - Workflow contracts and schemas are deterministic.
  - Retry paths exist for workflow execution.
  - Workflow execution can be audited.
  - Failure recovery paths are explicitly tested.
  - Workflow metrics and traces are available.
  - Workflow loading/version hooks exist.

- Mapped implementation paths:
  - `auto_client_acquisition/workflow_os/workflow_model.py`
  - `auto_client_acquisition/workflow_os/workflow_metrics.py`
  - `auto_client_acquisition/workflow_os/workflow_mapper.py`
  - `core/queue/tasks.py`
  - `auto_client_acquisition/delivery_factory/workflow_loader.py`

