"""Business NOW verdict cache read/write."""

from __future__ import annotations

from pathlib import Path

import yaml

from dealix.business_now.cache import apply_cache_to_platform, load_cache, write_cache


def test_write_and_load_cache(tmp_path: Path, monkeypatch) -> None:
    cache_file = tmp_path / "business_now_cache.yaml"
    monkeypatch.setattr("dealix.business_now.cache.CACHE_PATH", cache_file)

    write_cache(
        transformation_verdict="PASS",
        enterprise_control_plane_verdict="PASS",
        governed_domains=16,
        generated_at="2026-05-16T12:00:00+00:00",
    )

    loaded = load_cache()
    assert loaded is not None
    assert loaded["transformation_verdict"] == "PASS"
    assert loaded["enterprise_control_plane_verdict"] == "PASS"
    assert loaded["governed_domains"] == 16


def test_apply_cache_to_platform(tmp_path: Path, monkeypatch) -> None:
    cache_file = tmp_path / "business_now_cache.yaml"
    monkeypatch.setattr("dealix.business_now.cache.CACHE_PATH", cache_file)

    cache_file.write_text(
        yaml.safe_dump(
            {
                "transformation_verdict": "PASS",
                "enterprise_control_plane_verdict": "FAIL",
                "governed_domains": 16,
                "verdict_source": "generator",
                "generated_at": "2026-05-16T12:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    platform = apply_cache_to_platform(
        {"transformation_verdict": "SKIP", "enterprise_control_plane_verdict": "SKIP"}
    )
    assert platform["transformation_verdict"] == "PASS"
    assert platform["enterprise_control_plane_verdict"] == "FAIL"
    assert platform["verdict_source"] == "generator"
