"""Commercial value map status + API payload shape."""

from __future__ import annotations

from dealix.commercial_ops.value_map_status import (
    build_commercial_value_map,
    build_value_map_status,
)


def test_build_value_map_status_shape() -> None:
    st = build_value_map_status()
    assert st["agency_seed_rows"] >= 0
    assert "first_paid" in st
    assert st["doc_path"].endswith("COMMERCIAL_VALUE_MAP_AR.md")


def test_build_commercial_value_map_includes_value_plan() -> None:
    blob = build_commercial_value_map(include_value_plan=True, motion_top_n=3)
    assert blob["catalog"]
    assert blob["status"]
    vp = blob["value_plan"]
    assert vp["schema_version"] == "1.0"
    assert vp.get("motion_a")


def test_write_value_map_artifacts_and_markdown() -> None:
    from dealix.commercial_ops.value_map_status import (
        render_commercial_value_map_markdown,
        write_value_map_artifacts,
    )

    paths = write_value_map_artifacts(motion_top_n=2)
    assert paths["md"].endswith(".md")
    assert paths["json"].endswith(".json")
    blob = build_commercial_value_map(include_value_plan=True, motion_top_n=2)
    md = render_commercial_value_map_markdown(blob)
    assert "Commercial Value Map" in md
    assert "North Star" in md
