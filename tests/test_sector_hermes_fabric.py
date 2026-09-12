from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/commercial/run_sector_hermes_fabric.py"


def _load():
    spec = importlib.util.spec_from_file_location("sector_fabric", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


fabric_mod = _load()


def test_fabric_covers_all_twenty_sectors_with_five_agents() -> None:
    fabric = fabric_mod.build_fabric()
    assert fabric["sector_count"] == 20
    assert fabric["permanent_agents"] == fabric_mod.PERMANENT_AGENTS
    assert len(fabric["deep_wip_sectors"]) == 3
    assert len({cell["sector_id"] for cell in fabric["cells"]}) == 20
    for cell in fabric["cells"]:
        assert [row["agent"] for row in cell["agents"]] == fabric_mod.PERMANENT_AGENTS
        assert not any(cell["authority"].values())
        assert cell["counts_as_pipeline"] is False
        assert cell["counts_as_revenue"] is False


def test_top3_are_research_ranked_not_pipeline() -> None:
    fabric = fabric_mod.build_fabric()
    assert fabric["deep_wip_sectors"] == [
        "retail_commerce_ecommerce",
        "logistics_supply_chain",
        "tourism_hospitality",
    ]
    assert fabric["opencode_promotion"] == "DENIED_UNTIL_EXECUTION_PLANE_GREEN"
    assert not any(fabric["material_authority"].values())


def test_patrol_writes_internal_receipt_only(tmp_path: Path) -> None:
    result = fabric_mod.patrol_sector("retail_commerce_ecommerce", tmp_path)
    assert result["ok"] is True
    receipt = (tmp_path / "receipts/retail_commerce_ecommerce.json").read_text(encoding="utf-8")
    assert "INTERNAL_PATROL_READY" in receipt
    assert '"counts_as_pipeline": false' in receipt
    assert '"counts_as_revenue": false' in receipt
