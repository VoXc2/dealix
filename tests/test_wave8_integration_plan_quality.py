"""Wave 8 — Integration Plan Quality Gate tests."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "dealix_integration_plan_quality_check.py"

import importlib.util
import sys

def _load_module():
    spec = importlib.util.spec_from_file_location("plan_quality", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_exists():
    assert SCRIPT_PATH.exists()


def test_nonexistent_plan_returns_file_not_found():
    mod = _load_module()
    result = mod.check_plan_file(Path("/nonexistent/path/plan.md"))
    assert result["verdict"] == "FILE_NOT_FOUND"


def test_valid_plan_passes():
    mod = _load_module()
    valid_plan = """# خطّة الإدماج — Test Company

**Customer handle:** `test-company`
**Sector:** real_estate
**Generated:** 2026-05-07T00:00:00+00:00
**DPA signed:** ✅

هذا الملف يلخّص كيف تربط بياناتك مع Dealix.

---

## القنوات المُفعّلة

### 1. whatsapp — ✅ مُفعّل

- **phone:** +966500000000

---

## Hard rules

- ❌ Dealix لا يرسل WhatsApp تلقائي (NO_LIVE_SEND)
- ❌ Dealix لا يخصم بطاقة بدون تأكيد المؤسس (NO_LIVE_CHARGE)
- ❌ Dealix لا يستخرج بيانات منافسيك (NO_SCRAPING)
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(valid_plan)
        tmp_path = Path(f.name)
    try:
        result = mod.check_plan_file(tmp_path)
        # Should have no forbidden token failures
        forbidden_fails = [c for c in result["checks"] if "no_forbidden" in c["name"] and c["status"] == "FAIL"]
        assert not forbidden_fails, f"Forbidden token failures: {forbidden_fails}"
    finally:
        tmp_path.unlink(missing_ok=True)


def test_plan_with_guaranteed_fails():
    mod = _load_module()
    bad_plan = """# خطّة الإدماج — Test Company

**Customer handle:** `test-co`
**DPA signed:** ✅

نحن نضمن لك نتائج رائعة. We guaranteed results.

## القنوات المُفعّلة
## Hard rules
NO_LIVE_SEND NO_LIVE_CHARGE NO_SCRAPING
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(bad_plan)
        tmp_path = Path(f.name)
    try:
        result = mod.check_plan_file(tmp_path)
        forbidden_fails = [c for c in result["checks"] if "no_forbidden" in c["name"] and c["status"] == "FAIL"]
        assert len(forbidden_fails) > 0, "Should fail for guaranteed/نضمن tokens"
    finally:
        tmp_path.unlink(missing_ok=True)


def test_plan_with_unredacted_token_fails():
    mod = _load_module()
    bad_plan = """# خطّة الإدماج — Test

**Customer handle:** `test`
**DPA signed:** ✅

token: dealix-cust-abcdefghijklmnopqrstuvwxyz123456

## القنوات
## Hard rules
NO_LIVE_SEND NO_LIVE_CHARGE NO_SCRAPING
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(bad_plan)
        tmp_path = Path(f.name)
    try:
        result = mod.check_plan_file(tmp_path)
        token_fails = [c for c in result["checks"] if "no_token_leak" in c["name"] and c["status"] == "FAIL"]
        assert len(token_fails) > 0, "Should fail for unredacted portal token"
    finally:
        tmp_path.unlink(missing_ok=True)


def test_no_plan_file_returns_zero_exit(tmp_path):
    """When no plan exists yet, quality gate should not fail (no customer yet)."""
    mod = _load_module()
    result = mod.check_plan_file(tmp_path / "nonexistent.md")
    assert result["exists"] is False
