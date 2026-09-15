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
    assert st["doc_path"].endswith("DEALIX_BUSINESS_MODEL.md")
    assert st["commercial_identity_path"].endswith("COMMERCIAL_IDENTITY.md")
    assert st["first_launch_gate_path"].endswith("first_launch_offer_gate.yaml")


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


def test_seed_placeholders_do_not_count_as_active_targets() -> None:
    st = build_value_map_status()
    assert st["agency_seed_rows"] >= st["agency_active_rows"]
    assert st["agency_placeholder_rows"] == st["agency_seed_rows"] - st["agency_active_rows"]
    if st["agency_active_rows"] < 80:
        assert st["agency_seed_strict_ok"] is False
