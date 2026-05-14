"""Knowledge OS — no-source policy."""

from __future__ import annotations

from auto_client_acquisition.knowledge_os import eval_no_source_policy


def test_eval_no_source_policy() -> None:
    assert eval_no_source_policy() is True
