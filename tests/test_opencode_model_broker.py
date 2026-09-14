"""Contracts for the identity-stable OpenCode free-model broker (no secrets)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


broker = _load("opencode_model_broker")


def test_parse_catalog_keeps_model_ids_only() -> None:
    text = "Models cache refreshed\nopencode/deepseek-v4-flash\nError: boom\nollama/qwen3:4b\nplainline\n"
    assert broker.parse_catalog(text) == ["opencode/deepseek-v4-flash", "ollama/qwen3:4b"]


def test_candidate_order_prefers_safe_current_then_preferred_free_only() -> None:
    availability = {
        "models": [
            "opencode/zzz-free",
            "opencode/deepseek-v4-flash-free",
            "opencode/paid-x",
            "opencode-go/deepseek-v4.1-flash",
        ],
        "free_models": ["opencode/zzz-free", "opencode/deepseek-v4-flash-free"],
    }
    order = broker.candidate_order(availability, current="opencode/current-free")
    assert order[0] == "opencode/current-free"
    assert "opencode/deepseek-v4-flash-free" not in order
    assert "opencode/paid-x" not in order
    assert "opencode-go/deepseek-v4.1-flash" not in order


def test_candidate_order_rejects_deepseek_current() -> None:
    availability = {
        "models": ["opencode/a-free", "opencode/deepseek-v4-flash-free"],
        "free_models": ["opencode/a-free", "opencode/deepseek-v4-flash-free"],
    }
    assert broker.candidate_order(availability, current="opencode/deepseek-v4-flash-free") == [
        "opencode/a-free"
    ]


def test_candidate_order_rejects_stale_non_free_current() -> None:
    availability = {
        "models": ["opencode/a-free", "opencode/paid-x"],
        "free_models": ["opencode/a-free"],
    }
    assert broker.candidate_order(availability, current="opencode/paid-x") == ["opencode/a-free"]


def test_refresh_writes_availability_without_credentials(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        broker,
        "run_opencode",
        lambda args, timeout=60: (
            0,
            "Models cache refreshed\nopencode/a-free\nopencode/b-free\nopencode/paid-x\n",
        ),
    )
    payload = broker.refresh(tmp_path)
    assert payload["count"] == 3
    assert payload["free_count"] == 2
    assert payload["blocked_non_free_count"] == 1
    assert payload["auto_select_policy"] == "explicit_free_only"
    assert payload["credentials_stored"] is False
    written = json.loads((tmp_path / "model-availability.json").read_text())
    assert written["free_models"] == ["opencode/a-free", "opencode/b-free"]
    assert (tmp_path / "free-model-pool").read_text().split() == ["opencode/a-free", "opencode/b-free"]


def test_select_dry_run_lists_candidates_without_probing(tmp_path: Path) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"models": ["opencode/a-free", "opencode/paid-x"], "free_models": ["opencode/a-free"]})
    )
    result = broker.select(tmp_path, dry_run=True)
    assert result["dry_run"] is True
    assert result["selected"] is None
    assert result["candidates"] == ["opencode/a-free"]
    assert result["auto_select_policy"] == "explicit_free_only"


def test_select_picks_first_healthy_free_model(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"models": ["opencode/a-free", "opencode/b-free"], "free_models": ["opencode/a-free", "opencode/b-free"]})
    )

    calls: list[str] = []

    def fake_run(args, timeout=60):
        model = args[args.index("-m") + 1]
        calls.append(model)
        return (0, "FREE_SELECTOR_OK") if model == "opencode/b-free" else (1, "nope")

    monkeypatch.setattr(broker, "run_opencode", fake_run)
    result = broker.select(tmp_path)
    assert result["selected"] == "opencode/b-free"
    assert calls == ["opencode/a-free", "opencode/b-free"]
    assert (tmp_path / "selected-free-model").read_text().strip() == "opencode/b-free"


def test_select_never_probes_non_free_known_model(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"models": ["opencode/paid-x"], "free_models": []})
    )
    calls: list[list[str]] = []

    def fake_run(args, timeout=60):
        calls.append(args)
        return 0, "FREE_SELECTOR_OK"

    monkeypatch.setattr(broker, "run_opencode", fake_run)
    result = broker.select(tmp_path)
    assert result["selected"] is None
    assert calls == []


def test_select_returns_none_when_no_model_healthy(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"models": ["opencode/a-free"], "free_models": ["opencode/a-free"]})
    )
    monkeypatch.setattr(broker, "run_opencode", lambda args, timeout=60: (1, "nope"))
    assert broker.select(tmp_path)["selected"] is None


def test_status_blocks_stale_non_free_selection(tmp_path: Path) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"count": 3, "free_models": ["opencode/a-free"], "refreshed_at": "2026-09-12T00:00:00Z"})
    )
    (tmp_path / "selected-free-model").write_text("opencode/paid-x\n")
    payload = broker.status(tmp_path)
    assert payload["availability_count"] == 3
    assert payload["selected"] is None
    assert payload["stale_non_free_selection_blocked"] is True
    assert payload["auto_select_policy"] == "explicit_free_only"


def test_status_reports_safe_selection(tmp_path: Path) -> None:
    (tmp_path / "model-availability.json").write_text(
        json.dumps({"count": 3, "free_models": ["opencode/a-free"], "refreshed_at": "2026-09-12T00:00:00Z"})
    )
    (tmp_path / "selected-free-model").write_text("opencode/a-free\n")
    payload = broker.status(tmp_path)
    assert payload["selected"] == "opencode/a-free"
    assert payload["stale_non_free_selection_blocked"] is False
