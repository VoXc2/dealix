"""Optional OTel span event export from contract_trace_hook."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from auto_client_acquisition.observability_v10.contract_trace_hook import (
    record_contract_trace_event,
)


def test_otel_export_adds_span_event_when_enabled() -> None:
    mock_span = MagicMock()
    mock_span.is_recording.return_value = True

    class _Settings:
        otel_contract_trace_export = True

    with (
        patch("core.config.settings.get_settings", return_value=_Settings()),
        patch("opentelemetry.trace.get_current_span", return_value=mock_span),
    ):
        record_contract_trace_event(
            tenant_id="t1",
            correlation_id="c1",
            run_id="r1",
            event_type="value.metric.recorded",
            source_module="tests",
            actor="agent",
        )
    mock_span.add_event.assert_called_once()
    args, _kwargs = mock_span.add_event.call_args
    assert args[0] == "dealix.contract_trace"
