from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import tomllib

from dealix.observability import otel


class _FakeTracer:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    @contextmanager
    def start_as_current_span(self, name: str, *, attributes: dict[str, object]):
        self.calls.append((name, attributes))
        yield object()


def test_safe_span_attributes_allowlist_and_sensitive_drop() -> None:
    attrs = otel.safe_span_attributes(
        {
            "operation_name": "chat",
            "provider_name": "openai",
            "workload_id": "workload:123",
            "evidence_id": "evidence:abc",
            "authority_class": "INTERNAL_ONLY",
            "result": "PASS",
            "source_sha": "abc123",
            "cost_usd": 1.25,
            "elapsed_ms": 42,
            "founder_minutes": 3.5,
            "agent_minutes": 8,
            "prompt": "customer secret",
            "input_messages": "pii",
            "customer_id": "customer-1",
            "payload": {"raw": "data"},
            "authorization_header": "Bearer secret",
            "unknown_key": "ignored",
        }
    )

    assert attrs["gen_ai.operation.name"] == "chat"
    assert attrs["gen_ai.provider.name"] == "openai"
    assert attrs["dealix.workload.id"] == "workload:123"
    assert attrs["dealix.evidence.id"] == "evidence:abc"
    assert attrs["dealix.cost.usd"] == 1.25
    assert attrs["dealix.elapsed.ms"] == 42
    serialized = repr(attrs).lower()
    assert "secret" not in serialized
    assert "customer-1" not in serialized
    assert "pii" not in serialized
    assert "unknown_key" not in serialized


def test_unsafe_labels_are_replaced_and_negative_cost_is_dropped() -> None:
    attrs = otel.safe_span_attributes(
        {
            "workload_id": "contains customer narrative with spaces",
            "cost_usd": -1,
            "elapsed_ms": -2,
        }
    )
    assert attrs["dealix.workload.id"] == "redacted_unclassified"
    assert "dealix.cost.usd" not in attrs
    assert "dealix.elapsed.ms" not in attrs


def test_llm_agent_and_tool_spans_use_stable_names_and_no_raw_content(monkeypatch) -> None:
    tracer = _FakeTracer()
    monkeypatch.setattr(otel, "_HAS_OTEL", True)
    monkeypatch.setattr(otel, "_tracer", tracer)

    with otel.llm_span(
        "deepseek/deepseek-v4-flash",
        "commercial_review",
        provider_name="deepseek",
        workload_id="work:1",
        prompt="DO NOT EXPORT ME",
    ):
        pass
    with otel.agent_span("dealix-sales", workload_id="work:2", customer="private"):
        pass
    with otel.tool_span("github.search", evidence_id="evidence:1", output="private"):
        pass

    assert [call[0] for call in tracer.calls] == [
        "gen_ai.operation",
        "gen_ai.agent",
        "dealix.tool",
    ]
    all_attrs = repr([call[1] for call in tracer.calls])
    assert "DO NOT EXPORT ME" not in all_attrs
    assert "private" not in all_attrs
    assert tracer.calls[0][1]["gen_ai.request.model"] == "deepseek/deepseek-v4-flash"
    assert tracer.calls[1][1]["gen_ai.agent.name"] == "dealix-sales"
    assert tracer.calls[2][1]["dealix.tool.name"] == "github.search"


def test_observability_extra_contains_the_imported_otlp_http_exporter() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject.open("rb") as handle:
        config = tomllib.load(handle)
    deps = config["project"]["optional-dependencies"]["observability"]
    assert any(dep.startswith("opentelemetry-exporter-otlp-proto-http") for dep in deps)


def test_source_does_not_log_otlp_endpoint_or_headers() -> None:
    source = (Path(__file__).resolve().parents[1] / "dealix/observability/otel.py").read_text()
    assert 'extra={"endpoint"' not in source
    assert 'extra={"headers"' not in source
    assert "OTEL_EXPORTER_OTLP_HEADERS" in source
    assert "safe_span_attributes" in source
