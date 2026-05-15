"""In-memory tracing for platform observability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TraceSpan:
    trace_id: str
    span_id: str
    name: str
    start_epoch_ms: int
    end_epoch_ms: int
    status: str

    @property
    def duration_ms(self) -> int:
        return max(0, self.end_epoch_ms - self.start_epoch_ms)


_TRACE_SPANS: list[TraceSpan] = []


def record_span(span: TraceSpan) -> None:
    _TRACE_SPANS.append(span)


def list_spans() -> tuple[TraceSpan, ...]:
    return tuple(_TRACE_SPANS)


def clear_spans_for_tests() -> None:
    _TRACE_SPANS.clear()


__all__ = ['TraceSpan', 'clear_spans_for_tests', 'list_spans', 'record_span']
