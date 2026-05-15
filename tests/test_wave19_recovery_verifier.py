"""Wave 19 Recovery — verifier behavior tests.

Lock in the contract of `scripts/verify_all_dealix.py`:
- All systems pass at >= 3/5 on a clean repo.
- CEO-complete is False until partner outreach and first invoice both
  reach 5/5.
- Dishonest log states (counts diverge from entries) downgrade systems.
"""

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFIER_PATH = REPO_ROOT / "scripts/verify_all_dealix.py"


def _load_verifier():
    if "verify_all_dealix" in sys.modules:
        return sys.modules["verify_all_dealix"]
    spec = importlib.util.spec_from_file_location("verify_all_dealix", VERIFIER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["verify_all_dealix"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_verifier_runs_and_all_systems_pass():
    v = _load_verifier()
    results, all_pass, ceo_complete = v.run()
    assert all_pass is True, "all Wave 19 systems should pass at >=3/5"
    assert ceo_complete is False, (
        "CEO-complete must remain False until partner outreach AND first invoice "
        "reach 5/5 (real founder actions)"
    )
    systems = {r.system for r in results}
    expected = {
        "Offer Ladder",
        "Founder Command Center",
        "Partner Motion",
        "First Invoice Motion",
        "Funding Pack",
        "GCC Expansion",
        "Open Doctrine",
    }
    assert expected.issubset(systems)


def test_verifier_master_verification_matrix_documents_systems():
    p = REPO_ROOT / "docs/ops/MASTER_VERIFICATION_MATRIX.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    for system in [
        "Offer Ladder",
        "Founder Command Center",
        "Partner Motion",
        "First Invoice Motion",
        "Funding Pack",
        "GCC Expansion",
        "Open Doctrine",
    ]:
        assert system in text, f"{system} not documented in matrix"


def test_verifier_master_status_exists_and_is_honest():
    p = REPO_ROOT / "docs/ops/DEALIX_MASTER_STATUS.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "CEO-complete: NO" in text
    assert "No outreach has been sent" in text


def test_partner_log_dishonesty_is_detected(tmp_path, monkeypatch):
    """Simulate a dishonest partner log and confirm the check downgrades."""
    v = _load_verifier()
    log_path = REPO_ROOT / "data/partner_outreach_log.json"
    original = json.loads(log_path.read_text(encoding="utf-8"))
    try:
        dishonest = dict(original)
        dishonest["outreach_sent_count"] = 5
        dishonest["entries"] = []
        log_path.write_text(json.dumps(dishonest), encoding="utf-8")
        check = v.check_partner_motion()
        assert check.pass_ is False
        assert "dishonest" in check.details.lower()
    finally:
        log_path.write_text(json.dumps(original, indent=2) + "\n", encoding="utf-8")


def test_first_invoice_log_dishonesty_is_detected():
    v = _load_verifier()
    log_path = REPO_ROOT / "data/first_invoice_log.json"
    original = json.loads(log_path.read_text(encoding="utf-8"))
    try:
        dishonest = dict(original)
        dishonest["invoice_sent_count"] = 0
        dishonest["invoice_paid_count"] = 9
        log_path.write_text(json.dumps(dishonest), encoding="utf-8")
        check = v.check_first_invoice_motion()
        assert check.pass_ is False
        assert "dishonest" in check.details.lower()
    finally:
        log_path.write_text(json.dumps(original, indent=2) + "\n", encoding="utf-8")
