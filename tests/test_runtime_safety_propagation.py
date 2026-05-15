"""Enterprise Control Plane — runtime safety propagation.

Check #7 of the verify contract: the kill switch isolates an agent AND
pauses the workflow run it was driving — a killed agent never leaves a
run live. Isolation is tenant-scoped and recorded as evidence.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.evidence_control_plane_os.evidence_store import (
    clear_evidence_store_for_tests,
    run_trace,
)
from auto_client_acquisition.institutional_control_os.run_registry import (
    RUN_PAUSED,
    RUN_RUNNING,
    clear_run_registry_for_tests,
    get_run,
    register_run,
)
from auto_client_acquisition.secure_agent_runtime_os.agent_isolation import (
    clear_isolation_for_tests,
    is_agent_isolated,
    isolate_agent,
    release_agent,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_isolation_for_tests()
    yield
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_isolation_for_tests()


def test_isolate_agent_marks_it_isolated():
    result = isolate_agent(tenant_id="t1", agent_id="a1", reason="forbidden tool attempt")
    assert result["isolated"] is True
    assert is_agent_isolated("t1", "a1") is True
    # Tenant-scoped — another tenant's agent of the same id is unaffected.
    assert is_agent_isolated("t2", "a1") is False


def test_isolation_requires_a_reason():
    with pytest.raises(ValueError, match="reason"):
        isolate_agent(tenant_id="t1", agent_id="a1", reason="")


def test_kill_switch_pauses_the_run():
    run = register_run(tenant_id="t1", workflow_id="wf")
    assert run.state == RUN_RUNNING
    result = isolate_agent(
        tenant_id="t1", agent_id="a1", reason="risk threshold breached", run_id=run.run_id,
    )
    assert result["run_paused"] is True
    assert get_run(run.run_id).state == RUN_PAUSED


def test_isolation_is_recorded_as_evidence():
    run = register_run(tenant_id="t1", workflow_id="wf")
    isolate_agent(tenant_id="t1", agent_id="a1", reason="manual kill", run_id=run.run_id)
    trace = run_trace(tenant_id="t1", run_id=run.run_id)
    assert any(e.evidence_type == "risk" for e in trace)


def test_release_lifts_isolation():
    isolate_agent(tenant_id="t1", agent_id="a1", reason="test")
    assert release_agent("t1", "a1") is True
    assert is_agent_isolated("t1", "a1") is False
