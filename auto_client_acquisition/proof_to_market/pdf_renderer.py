"""Markdown → PDF renderer — Wave 14D.4.

Thin wrapper. Prefers `weasyprint` if installed, falls back to `pandoc`
subprocess if available, otherwise returns None + logs reason. The PDF
endpoints in api/routers/*.py call this; if it returns None they fall
back to returning the markdown directly with a Content-Type warning.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


def _try_weasyprint(md: str, title: str) -> bytes | None:
    """Try weasyprint. Returns PDF bytes or None."""
    try:
        # Light HTML wrapper around the markdown — minimal but readable.
        # We avoid heavy markdown→HTML libs; weasyprint can render plain
        # text wrapped in <pre>.
        try:
            import markdown as _md  # type: ignore
            html_body = _md.markdown(md, extensions=["tables", "fenced_code"])
        except ImportError:
            # Fallback: wrap in <pre> for monospace readable output
            import html as _html
            html_body = f"<pre style='white-space:pre-wrap'>{_html.escape(md)}</pre>"

        full_html = (
            "<!doctype html><html lang='ar' dir='auto'><head>"
            "<meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>"
            "body{font-family:'Noto Sans','Helvetica Neue',Arial,sans-serif;line-height:1.5;"
            "margin:2cm;color:#222}"
            "h1,h2,h3{color:#0a0a0a;border-bottom:1px solid #ddd;padding-bottom:6px}"
            "table{border-collapse:collapse;width:100%;margin:12px 0}"
            "th,td{border:1px solid #ccc;padding:6px}"
            "pre{background:#f6f8fa;padding:10px;border-radius:6px;overflow-x:auto}"
            "</style></head><body>"
            f"{html_body}"
            "</body></html>"
        )

        from weasyprint import HTML  # type: ignore
        return HTML(string=full_html).write_pdf()
    except ImportError:
        log.debug("pdf_renderer: weasyprint not installed")
        return None
    except Exception:  # noqa: BLE001
        log.exception("pdf_renderer_weasyprint_failed")
        return None


def _try_pandoc(md: str, title: str) -> bytes | None:
    """Try pandoc subprocess. Returns PDF bytes or None."""
    if not shutil.which("pandoc"):
        log.debug("pdf_renderer: pandoc binary not available on PATH")
        return None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as fp_in:
            fp_in.write(md)
            md_path = Path(fp_in.name)
        out_path = md_path.with_suffix(".pdf")
        proc = subprocess.run(
            [
                "pandoc",
                str(md_path),
                "-o",
                str(out_path),
                "--metadata",
                f"title={title}",
                "--pdf-engine=xelatex",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc.returncode != 0 or not out_path.exists():
            log.warning("pdf_renderer_pandoc_failed: %s", proc.stderr[:200])
            return None
        data = out_path.read_bytes()
        try:
            md_path.unlink(missing_ok=True)
            out_path.unlink(missing_ok=True)
        except Exception:  # noqa: BLE001
            pass
        return data
    except Exception:  # noqa: BLE001
        log.exception("pdf_renderer_pandoc_exception")
        return None


def render_markdown_to_pdf(md: str, title: str = "Dealix Document") -> bytes | None:
    """Render markdown to PDF bytes. Returns None if no renderer available.

    Caller is responsible for falling back to text/markdown response when
    None is returned.
    """
    if not md:
        return None
    pdf = _try_weasyprint(md, title)
    if pdf is not None:
        return pdf
    pdf = _try_pandoc(md, title)
    return pdf


def is_pdf_available() -> dict[str, bool]:
    """Diagnostic helper used by /api/v1/health and tests."""
    weasy = False
    try:
        import weasyprint  # noqa: F401
        weasy = True
    except ImportError:
        pass
    pandoc = bool(shutil.which("pandoc"))
    return {"weasyprint": weasy, "pandoc": pandoc, "any": weasy or pandoc}


__all__ = ["is_pdf_available", "render_markdown_to_pdf"]
