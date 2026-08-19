"""Source contracts for fail-closed tenant-owned autonomous writes."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "api" / "routers" / "autonomous.py").read_text(encoding="utf-8")


def _block(start: str, end: str) -> str:
    start_index = SOURCE.index(start)
    end_index = SOURCE.index(end, start_index)
    return SOURCE[start_index:end_index]


def test_conversation_create_commits_or_raises_instead_of_reporting_skip() -> None:
    block = _block(
        "async def create_conversation(",
        '@router.get("/conversations")',
    )
    assert "LeadRecord.tenant_id == tenant_id" in block
    assert "session.add(rec)" in block
    assert "await session.commit()" in block
    assert "_safe_commit" not in block
    assert "skipped_db_unreachable" not in block
    assert "auto_sent=False" in block


def test_deal_create_verifies_lead_ownership_and_commits_strictly() -> None:
    block = _block(
        "async def create_deal(",
        '@router.patch("/deals/{deal_id}")',
    )
    assert "LeadRecord.id == lead_id" in block
    assert "LeadRecord.tenant_id == tenant_id" in block
    assert 'detail="lead_not_found"' in block
    assert "session.add(deal)" in block
    assert "await session.commit()" in block
    assert "_safe_commit" not in block
    assert "skipped_db_unreachable" not in block


def test_tenant_scope_is_separated_from_module_logger() -> None:
    assert "return tenant_id\n\n\nlog = logging.getLogger(__name__)" in SOURCE
