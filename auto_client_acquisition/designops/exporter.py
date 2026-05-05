"""DesignOps exporter — local-only artifact writer.

Writes a DesignOps artifact (manifest + content) to a local directory
in one or more of the supported formats: ``markdown``, ``html``, ``json``.

Hard rules (enforced here, not just documented):
  - NO upload. NO send. NO external HTTP. This module only writes to disk.
  - Filename comes from ``manifest['artifact_id']`` and is sanitized to
    ``[a-zA-Z0-9_-]`` only. Any path-traversal attempt (``..``, ``/``,
    ``\\``) raises ``ValueError``.
  - PDF / PPTX are deferred — calling with those formats raises
    ``NotImplementedError`` with a clear message.
  - Empty content dict raises ``ValueError`` (defensive).

Usage::

    from auto_client_acquisition.designops.exporter import export_artifact

    result = export_artifact(
        manifest={"artifact_id": "mini-diag-001", "safe_to_send": False},
        content={"markdown": "# Hello", "html": "<h1>Hello</h1>"},
        out_dir=tmp_path,
    )
    # result["written_files"] -> [".../mini-diag-001.md", ...]
"""
from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SUPPORTED_FORMATS: tuple[str, ...] = ("markdown", "html", "json")
DEFERRED_FORMATS: tuple[str, ...] = ("pdf", "pptx")

_FILENAME_SAFE_RE = re.compile(r"^[a-zA-Z0-9_-]+$")
_FILENAME_STRIP_RE = re.compile(r"[^a-zA-Z0-9_-]")

_FORMAT_EXT = {
    "markdown": "md",
    "html": "html",
    "json": "json",
}


def _sanitize_artifact_id(raw: Any) -> str:
    """Sanitize artifact_id to a safe filename stem.

    - Rejects path-traversal sequences (``..``, ``/``, ``\\``).
    - Strips any character not in ``[a-zA-Z0-9_-]``.
    - Raises ``ValueError`` if the result is empty.
    """
    if not isinstance(raw, str) or not raw:
        raise ValueError("manifest['artifact_id'] must be a non-empty string")
    if ".." in raw or "/" in raw or "\\" in raw:
        raise ValueError(
            f"artifact_id rejected (path traversal not allowed): {raw!r}"
        )
    cleaned = _FILENAME_STRIP_RE.sub("", raw)
    if not cleaned:
        raise ValueError(
            f"artifact_id has no safe characters after sanitization: {raw!r}"
        )
    if not _FILENAME_SAFE_RE.match(cleaned):
        # belt-and-suspenders — the strip should already guarantee this
        raise ValueError(f"artifact_id failed safe-name check: {cleaned!r}")
    return cleaned


def _default_out_dir() -> Path:
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    return Path("docs") / "designops" / "exports" / today


def export_artifact(
    manifest: dict,
    content: dict,
    out_dir: Path | str | None = None,
    formats: list[str] | None = None,
) -> dict:
    """Write a DesignOps artifact to ``out_dir`` in the requested formats.

    Parameters
    ----------
    manifest:
        Must contain ``artifact_id`` (string). Other fields (``safe_to_send``,
        ``skill_id`` ...) are preserved when emitting JSON.
    content:
        Mapping with optional keys ``markdown`` and ``html``. Must be a
        non-empty dict.
    out_dir:
        Local directory to write into. If ``None``, defaults to
        ``docs/designops/exports/<YYYY-MM-DD>/``. Created if missing.
    formats:
        Subset of ``("markdown", "html", "json")``. Defaults to all three.
        ``"pdf"`` / ``"pptx"`` raise ``NotImplementedError``.

    Returns
    -------
    dict with keys:
      - ``written_files``: absolute paths of files written
      - ``formats_emitted``: formats that were written
      - ``formats_skipped``: formats requested but skipped (e.g. missing content)
      - ``reason_skipped``: ``{format: reason_str}``
    """
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a dict")
    if not isinstance(content, dict):
        raise ValueError("content must be a dict")
    if not content:
        raise ValueError("content dict is empty — nothing to export")

    artifact_id = _sanitize_artifact_id(manifest.get("artifact_id"))

    if formats is None:
        formats = list(SUPPORTED_FORMATS)
    if not isinstance(formats, list) or not formats:
        raise ValueError("formats must be a non-empty list")

    # Reject deferred formats early with a clear message.
    for fmt in formats:
        if fmt in DEFERRED_FORMATS:
            raise NotImplementedError(
                f"Format '{fmt}' is deferred. DesignOps exporter currently "
                f"supports {SUPPORTED_FORMATS}. PDF/PPTX rendering is "
                f"intentionally not implemented to keep this module local-only "
                f"and dependency-free."
            )
        if fmt not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unknown format '{fmt}'. Supported: {SUPPORTED_FORMATS}"
            )

    target_dir = Path(out_dir) if out_dir is not None else _default_out_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    emitted: list[str] = []
    skipped: list[str] = []
    reason: dict[str, str] = {}

    for fmt in formats:
        ext = _FORMAT_EXT[fmt]
        path = target_dir / f"{artifact_id}.{ext}"

        if fmt == "markdown":
            md = content.get("markdown")
            if not isinstance(md, str) or not md:
                skipped.append(fmt)
                reason[fmt] = "content['markdown'] missing or empty"
                continue
            path.write_text(md, encoding="utf-8")
        elif fmt == "html":
            html = content.get("html")
            if not isinstance(html, str) or not html:
                skipped.append(fmt)
                reason[fmt] = "content['html'] missing or empty"
                continue
            path.write_text(html, encoding="utf-8")
        elif fmt == "json":
            payload = {"manifest": manifest, "content": content}
            path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        else:  # pragma: no cover — guarded above
            continue

        written.append(str(path))
        emitted.append(fmt)

    return {
        "written_files": written,
        "formats_emitted": emitted,
        "formats_skipped": skipped,
        "reason_skipped": reason,
    }
