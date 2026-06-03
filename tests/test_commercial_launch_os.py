"""Commercial Launch OS — placeholder-safe evidence scoring."""

from dealix.commercial_ops.commercial_launch_os import build_launch_snapshot, evaluate_check


def test_launch_snapshot_schema() -> None:
    snap = build_launch_snapshot(skip_live=True)
    assert snap["schema_version"] == "1.0"
    assert snap["verdict"] in ("PASS", "WARN", "FAIL")
    assert snap["score"]["max"] >= 4


def test_evaluate_path_check() -> None:
    row = evaluate_check(
        {"id": "gtm_home", "path": "frontend/src/components/gtm/PublicGtmShell.tsx"},
        skip_live=True,
    )
    assert row["ok"] is True
    assert row["rag"] == "green"
