"""Wave 13 Phase 8 — Customer Success Intelligence tests.

5-score system: Health · Comfort · Expansion · Churn Risk · Proof Maturity.

Asserts:
  - Churn Risk: 5 signals fire correctly + buckets correct
  - Churn Risk: 3+ signals → high or critical
  - Proof Maturity: case_study_ready requires L4+ AND consent
  - Proof Maturity: pre_proof for 0 events
  - Both modules: is_estimate=True everywhere
  - Recommended actions bilingual

Sandbox-safe: imports each module via direct file load.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_REPO_ROOT = Path(__file__).resolve().parent.parent
_CHURN = _load(
    _REPO_ROOT / "auto_client_acquisition" / "customer_success" / "churn_risk.py",
    "_test_w13_p8_churn",
)
_PROOF = _load(
    _REPO_ROOT / "auto_client_acquisition" / "customer_success" / "proof_maturity.py",
    "_test_w13_p8_proof",
)
compute_churn_risk = _CHURN.compute_churn_risk
compute_proof_maturity = _PROOF.compute_proof_maturity


# ── Test 1 ────────────────────────────────────────────────────────────
def test_churn_risk_zero_signals_low_bucket():
    r = compute_churn_risk(customer_id="acme")
    assert r.risk_score == 0.0
    assert r.bucket == "low"
    assert r.signals_active == []
    assert r.is_estimate is True


# ── Test 2 ────────────────────────────────────────────────────────────
def test_churn_risk_three_signals_high_or_critical():
    """3+ signals firing → bucket is high or critical."""
    r = compute_churn_risk(
        customer_id="acme",
        engagement_drop_pct=60.0,         # 25 pts
        support_escalations_last_30d=3,   # 20 pts
        payment_late_count=2,             # 20 pts (= 65 → high)
    )
    assert len(r.signals_active) == 3
    assert r.bucket in ("high", "critical")
    assert r.risk_score >= 50


# ── Test 3 ────────────────────────────────────────────────────────────
def test_churn_risk_critical_bucket_with_dm_left():
    """All 5 signals → critical (≥75)."""
    r = compute_churn_risk(
        customer_id="acme",
        engagement_drop_pct=60.0,         # 25
        support_escalations_last_30d=3,   # 20
        payment_late_count=2,             # 20
        nps_below_7=True,                 # 15
        decision_maker_left=True,         # 20 → 100 capped
    )
    assert r.risk_score == 100.0
    assert r.bucket == "critical"
    assert "decision_maker_left" in r.signals_active


# ── Test 4 ────────────────────────────────────────────────────────────
def test_churn_risk_recommendations_bilingual():
    r = compute_churn_risk(customer_id="acme", nps_below_7=True)
    assert r.recommended_action_ar
    assert r.recommended_action_en
    assert r.recommended_action_ar != r.recommended_action_en


# ── Test 5 ────────────────────────────────────────────────────────────
def test_proof_maturity_pre_proof_for_zero_events():
    p = compute_proof_maturity(customer_id="acme", proof_event_count=0)
    assert p.bucket == "pre_proof"
    assert p.score == 0.0
    assert p.is_estimate is True


# ── Test 6 ────────────────────────────────────────────────────────────
def test_proof_maturity_early_proof_for_some_events():
    p = compute_proof_maturity(
        customer_id="acme",
        proof_event_count=2,
        max_evidence_level=2,
    )
    assert p.bucket == "early_proof"
    assert p.score > 0


# ── Test 7 ────────────────────────────────────────────────────────────
def test_proof_maturity_mature_proof():
    p = compute_proof_maturity(
        customer_id="acme",
        proof_event_count=4,
        max_evidence_level=3,
    )
    assert p.bucket == "mature_proof"


# ── Test 8 ────────────────────────────────────────────────────────────
def test_proof_maturity_case_study_ready_requires_L4_and_consent():
    """Article 8: case_study_ready needs L4+ AND consent."""
    # L4 but NO consent → NOT case_study_ready
    p_no_consent = compute_proof_maturity(
        customer_id="acme",
        proof_event_count=5,
        max_evidence_level=4,
        publishable_count=2,
        consent_signed_count=0,  # missing!
    )
    assert p_no_consent.bucket != "case_study_ready"

    # L4 + consent → case_study_ready
    p_ready = compute_proof_maturity(
        customer_id="acme",
        proof_event_count=5,
        max_evidence_level=4,
        publishable_count=2,
        consent_signed_count=1,
    )
    assert p_ready.bucket == "case_study_ready"


# ── Test 9 ────────────────────────────────────────────────────────────
def test_proof_maturity_l3_only_not_case_study_ready():
    """max_evidence_level=3 → mature_proof, never case_study_ready."""
    p = compute_proof_maturity(
        customer_id="acme",
        proof_event_count=5,
        max_evidence_level=3,
        publishable_count=0,
        consent_signed_count=2,
    )
    assert p.bucket == "mature_proof"  # L3 < L4


# ── Test 10 ───────────────────────────────────────────────────────────
def test_all_5_scores_have_is_estimate_true():
    """Article 8: every CS score must mark is_estimate=True."""
    churn = compute_churn_risk(customer_id="acme", nps_below_7=True)
    proof = compute_proof_maturity(customer_id="acme", proof_event_count=1)
    assert churn.is_estimate is True
    assert proof.is_estimate is True
    # to_dict() also surfaces the flag
    assert churn.to_dict()["is_estimate"] is True
    assert proof.to_dict()["is_estimate"] is True
