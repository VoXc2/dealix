"""Contract: knowledge answers without sources mark insufficient evidence."""

from __future__ import annotations

from auto_client_acquisition.knowledge_os.knowledge_eval import eval_no_source_policy


def test_no_source_no_answer_policy() -> None:
    assert eval_no_source_policy() is True
