"""Tests for ``auto_client_acquisition/designops/exporter.py``.

Covers the hard rules:
  - local-only writes, no upload
  - filename sanitization rejects path traversal
  - PDF / PPTX raise NotImplementedError with a clear message
  - empty content dict raises ValueError
  - explicit format subset is honored
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.designops.exporter import (
    SUPPORTED_FORMATS,
    export_artifact,
)


@pytest.fixture
def manifest() -> dict:
    return {
        "artifact_id": "mini-diag-001",
        "skill_id": "mini_diagnostic",
        "safe_to_send": False,
    }


@pytest.fixture
def content() -> dict:
    return {
        "markdown": "# Mini Diagnostic\n\nFounder review required.",
        "html": "<h1>Mini Diagnostic</h1><p>Founder review required.</p>",
    }


def test_export_writes_md_html_json_to_tmp_path(tmp_path, manifest, content):
    result = export_artifact(manifest, content, out_dir=tmp_path)

    assert set(result["formats_emitted"]) == set(SUPPORTED_FORMATS)
    assert result["formats_skipped"] == []
    assert result["reason_skipped"] == {}
    assert len(result["written_files"]) == 3

    md = tmp_path / "mini-diag-001.md"
    html = tmp_path / "mini-diag-001.html"
    js = tmp_path / "mini-diag-001.json"
    assert md.exists() and html.exists() and js.exists()
    assert md.read_text(encoding="utf-8").startswith("# Mini Diagnostic")
    assert "<h1>Mini Diagnostic</h1>" in html.read_text(encoding="utf-8")

    payload = json.loads(js.read_text(encoding="utf-8"))
    assert payload["manifest"]["artifact_id"] == "mini-diag-001"
    assert payload["manifest"]["safe_to_send"] is False
    assert payload["content"]["markdown"].startswith("# Mini Diagnostic")


def test_filename_sanitization_rejects_path_traversal(tmp_path, content):
    bad_ids = [
        "../etc/passwd",
        "..\\windows\\system32",
        "foo/bar",
        "foo\\bar",
        "..",
    ]
    for bad in bad_ids:
        with pytest.raises(ValueError, match="path traversal|non-empty|safe"):
            export_artifact({"artifact_id": bad}, content, out_dir=tmp_path)


def test_filename_sanitization_strips_unsafe_chars(tmp_path, content):
    # spaces and punctuation get stripped, result is still valid
    result = export_artifact(
        {"artifact_id": "hello world! 2026"},
        content,
        out_dir=tmp_path,
        formats=["markdown"],
    )
    written = Path(result["written_files"][0])
    assert written.name == "helloworld2026.md"


def test_pdf_raises_not_implemented(tmp_path, manifest, content):
    with pytest.raises(NotImplementedError) as exc:
        export_artifact(manifest, content, out_dir=tmp_path, formats=["pdf"])
    msg = str(exc.value)
    assert "pdf" in msg.lower()
    assert "deferred" in msg.lower() or "not implemented" in msg.lower()


def test_pptx_raises_not_implemented(tmp_path, manifest, content):
    with pytest.raises(NotImplementedError) as exc:
        export_artifact(manifest, content, out_dir=tmp_path, formats=["pptx"])
    assert "pptx" in str(exc.value).lower()


def test_no_remote_upload_happens(tmp_path, manifest, content, monkeypatch):
    """Defensive: even an artifact whose manifest claims safe_to_send=True
    must not trigger any external HTTP. We monkey-patch common HTTP
    libraries and assert they are never called.
    """
    calls: list[str] = []

    def fail(*args, **kwargs):  # pragma: no cover — must never fire
        calls.append("HTTP_CALL_DETECTED")
        raise AssertionError("exporter must not perform any HTTP request")

    # Patch every plausible network surface.
    import urllib.request

    monkeypatch.setattr(urllib.request, "urlopen", fail, raising=False)
    try:
        import requests  # type: ignore

        monkeypatch.setattr(requests, "post", fail, raising=False)
        monkeypatch.setattr(requests, "get", fail, raising=False)
        monkeypatch.setattr(requests, "put", fail, raising=False)
    except ImportError:
        pass
    try:
        import httpx  # type: ignore

        monkeypatch.setattr(httpx, "post", fail, raising=False)
        monkeypatch.setattr(httpx, "get", fail, raising=False)
    except ImportError:
        pass

    rogue_manifest = {**manifest, "safe_to_send": True}
    result = export_artifact(rogue_manifest, content, out_dir=tmp_path)
    assert calls == []
    assert result["formats_emitted"] == list(SUPPORTED_FORMATS)
    # And we still wrote files locally only.
    for p in result["written_files"]:
        assert str(tmp_path) in p


def test_explicit_formats_html_only(tmp_path, manifest, content):
    result = export_artifact(
        manifest, content, out_dir=tmp_path, formats=["html"]
    )
    assert result["formats_emitted"] == ["html"]
    assert result["formats_skipped"] == []
    assert len(result["written_files"]) == 1
    assert result["written_files"][0].endswith(".html")
    # md / json must NOT exist
    assert not (tmp_path / "mini-diag-001.md").exists()
    assert not (tmp_path / "mini-diag-001.json").exists()


def test_empty_content_raises(tmp_path, manifest):
    with pytest.raises(ValueError, match="empty"):
        export_artifact(manifest, {}, out_dir=tmp_path)


def test_missing_markdown_skipped_with_reason(tmp_path, manifest):
    # Only html present — markdown should be skipped with a reason,
    # json should still emit.
    result = export_artifact(
        manifest,
        {"html": "<p>only html</p>"},
        out_dir=tmp_path,
    )
    assert "html" in result["formats_emitted"]
    assert "json" in result["formats_emitted"]
    assert "markdown" in result["formats_skipped"]
    assert "markdown" in result["reason_skipped"]


def test_unknown_format_raises(tmp_path, manifest, content):
    with pytest.raises(ValueError, match="Unknown format"):
        export_artifact(
            manifest, content, out_dir=tmp_path, formats=["docx"]
        )
