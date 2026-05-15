# Cross-Layer Validation

The control plane is only "real" if the layers work *together*. The
end-to-end test `tests/test_enterprise_control_plane_e2e.py` wires the
real modules into one flow and asserts each hand-off.

| Step | Layer / module | Assertion |
|---|---|---|
| Tenant resolved | `agent_os` | tenant-scoped agent registered; cross-tenant fetch is `None` |
| Run registered | `institutional_control_os.run_registry` | run in `running` state, carries `tenant_id` |
| Action evaluated | `agent_governance.evaluate_action` | external-visible tool → `REQUIRES_APPROVAL` |
| Action escalated | `governance_os.runtime_decision.decide` | high-risk action → escalation, `approval_required` |
| Approval queued | `approval_center` | ticket appears in `list_pending(tenant_id)`; no cross-tenant leak |
| Approval granted | `approval_center` | status → `APPROVED` |
| Value recorded | `value_os.value_ledger` | `verified` metric carries `source_ref`; `is_measured` true |
| Run trace | `evidence_control_plane_os.evidence_store` | trace contains ai_run + governance_decision + approval + value |
| Rollback gated | `run_registry` + `approval_center` | `finalize_rollback` blocked until ticket approved |
| Self-evolving gated | `approval_center` | proposal stays `PENDING` — never auto-applies |

Run: `python -m pytest tests/test_enterprise_control_plane_e2e.py -q`.
