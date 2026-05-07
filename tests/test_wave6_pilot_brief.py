"""Wave 6 Phase 4 — Pilot Brief generator tests."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/dealix_pilot_brief.py")


def _run(args: list[str]):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True,
    )


def test_script_exists() -> None:
    assert SCRIPT.exists()


def test_brief_default_499(tmp_path) -> None:
    out_md = tmp_path / "b.md"
    out_json = tmp_path / "b.json"
    r = _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 0, r.stderr
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["amount_sar"] == 499.0
    assert b["amount_halalah"] == 49900
    assert b["duration_days"] == 7


def test_brief_halalah_conversion(tmp_path) -> None:
    """1 SAR = 100 halalah."""
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "agencies",
        "--amount-sar", "100",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["amount_halalah"] == 10000


def test_brief_blocks_amount_above_sprint_cap(tmp_path) -> None:
    """499 SAR is the Sprint tier cap. Higher = blocked."""
    out_json = tmp_path / "b.json"
    r = _run([
        "--company", "Test Co",
        "--sector", "consulting",
        "--amount-sar", "1500",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    assert r.returncode == 2
    assert "Sprint tier cap" in r.stderr


def test_brief_no_live_charge(tmp_path) -> None:
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["payment"]["live_charge"] is False
    assert b["payment"]["moyasar_live"] is False
    assert b["payment"]["founder_must_confirm_manually"] is True


def test_brief_no_revenue_claim(tmp_path) -> None:
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "agencies",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["no_revenue_claim"] is True
    assert b["no_guaranteed_claim"] is True


def test_brief_kpi_is_commitment_not_guarantee(tmp_path) -> None:
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "services",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["kpi_commitment"]["type"] == "commitment_not_guarantee"


def test_brief_refund_policy(tmp_path) -> None:
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert b["refund_policy"]["rate_pct"] == 100
    assert b["refund_policy"]["window_days"] == 14
    assert b["refund_policy"]["questions_required"] is False


def test_brief_excludes_live_actions(tmp_path) -> None:
    """The 'what_is_excluded' list must mention all forbidden live actions."""
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    blob = " ".join(b["what_is_excluded"]).lower()
    assert "حيّ" in blob or "live" in blob
    assert "manual" in blob


def test_brief_no_forbidden_tokens_in_output(tmp_path) -> None:
    out_md = tmp_path / "b.md"
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ])
    md_text = out_md.read_text(encoding="utf-8")
    json_text = out_json.read_text(encoding="utf-8")
    for token in [r"\bguaranteed?\b", r"\bblast\b", r"\bscraping\b",
                   r"\bcold\s+whatsapp\b", "نضمن"]:
        assert not re.search(token, md_text, re.IGNORECASE), f"md contains: {token}"
        assert not re.search(token, json_text, re.IGNORECASE), f"json contains: {token}"


def test_brief_markdown_includes_arabic(tmp_path) -> None:
    out_md = tmp_path / "b.md"
    _run([
        "--company", "Test Co",
        "--sector", "real_estate",
        "--out-md", str(out_md),
        "--out-json", str(tmp_path / "b.json"),
    ])
    md = out_md.read_text(encoding="utf-8")
    assert "المخرجات" in md
    assert "الجدول الزمني" in md
    assert "ريال" in md
    assert "Proof Pack" in md


def test_brief_no_invoice_api_call(tmp_path) -> None:
    """Script must NOT make any LIVE HTTP calls or invoke Moyasar API."""
    src = SCRIPT.read_text(encoding="utf-8")
    # No live HTTP libraries used
    assert "requests.post" not in src
    assert "httpx.post" not in src
    assert "urllib.request.urlopen" not in src
    # If Moyasar mentioned, must explicitly mark live_charge=False
    if "moyasar" in src.lower():
        assert '"moyasar_live": False' in src or "moyasar_live=False" in src


def test_brief_with_diagnostic_file(tmp_path) -> None:
    """If diagnostic file provided, brief includes its summary."""
    # Create a fake diagnostic.json
    diag = tmp_path / "diag.json"
    diag.write_text(json.dumps({
        "executive_summary_ar": "ملخّص التشخيص للاختبار",
    }), encoding="utf-8")
    out_json = tmp_path / "b.json"
    _run([
        "--company", "Test Co",
        "--sector", "agencies",
        "--diagnostic-file", str(diag),
        "--out-md", str(tmp_path / "b.md"),
        "--out-json", str(out_json),
    ])
    b = json.loads(out_json.read_text(encoding="utf-8"))
    assert "ملخّص التشخيص" in b["diagnostic_summary"]
