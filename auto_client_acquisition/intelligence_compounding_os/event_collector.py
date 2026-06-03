"""Intelligence event streams — taxonomy for compounding inputs."""

from __future__ import annotations

INTELLIGENCE_EVENT_STREAMS: tuple[str, ...] = (
    "market",
    "client",
    "data",
    "workflow",
    "governance",
    "product",
)


def intelligence_event_stream_valid(stream: str) -> bool:
    return stream in INTELLIGENCE_EVENT_STREAMS
