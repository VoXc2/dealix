#!/usr/bin/env python3
"""Fail-closed verifier for Dealix OpenTelemetry privacy/semantic boundaries."""

from __future__ import annotations

from pathlib import Path
import tomllib

from dealix.observability.otel import safe_span_attributes

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    attrs = safe_span_attributes(
        {
            "operation_name": "chat",
            "provider_name": "openai",
            "workload_id": "work:verify",
            "evidence_id": "evidence:verify",
            "authority_class": "INTERNAL_ONLY",
            "result": "PASS",
            "source_sha": "abc123",
            "cost_usd": 0.25,
            "elapsed_ms": 100,
            "prompt": "must-not-leave-process",
            "input_messages": "must-not-leave-process",
            "customer_id": "must-not-leave-process",
            "authorization_header": "must-not-leave-process",
            "payload": "must-not-leave-process",
        }
    )
    serialized = repr(attrs).lower()
    assert "must-not-leave-process" not in serialized
    assert attrs["gen_ai.operation.name"] == "chat"
    assert attrs["dealix.workload.id"] == "work:verify"

    with (ROOT / "pyproject.toml").open("rb") as handle:
        config = tomllib.load(handle)
    deps = config["project"]["optional-dependencies"]["observability"]
    assert any(dep.startswith("opentelemetry-exporter-otlp-proto-http") for dep in deps)

    source = (ROOT / "dealix/observability/otel.py").read_text()
    assert 'extra={"endpoint"' not in source
    assert 'extra={"headers"' not in source
    assert 'start_as_current_span("gen_ai.operation"' in source
    assert 'start_as_current_span("gen_ai.agent"' in source
    assert 'start_as_current_span("dealix.tool"' in source

    print("DEALIX_OTEL_PRIVACY_CONTRACT=PASS")
    print("PROMPT_CONTENT_CAPTURE_DEFAULT=0")
    print("CUSTOMER_CONTENT_CAPTURE_DEFAULT=0")
    print("OTLP_ENDPOINT_LOGGED=0")
    print("OTLP_HEADERS_LOGGED=0")
    print("UNKNOWN_SPAN_ATTRS_EXPORTED=0")
    print("OTLP_HTTP_EXPORTER_DECLARED=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
