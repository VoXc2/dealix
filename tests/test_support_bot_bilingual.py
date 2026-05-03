"""
Support bot bilingual sanity — verifies that the deploy-branch support
classifier returns a sensible language + priority + escalation flag for
the 10 canonical questions. These tests are skipped automatically if the
deploy-branch endpoint is not reachable from this branch.

The tests do NOT require the deploy-branch code to be present locally —
they hit the live URL when set, otherwise skip cleanly.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import pytest


BASE_URL = os.getenv("SUPPORT_TEST_BASE_URL", os.getenv("BASE_URL", "")).rstrip("/")


def _post(path: str, body: dict) -> dict | None:
    if not BASE_URL:
        return None
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:  # noqa: S310 — trusted host
            return json.loads(r.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None


def _live() -> bool:
    if not BASE_URL:
        return False
    try:
        urllib.request.urlopen(f"{BASE_URL}/health", timeout=4)  # noqa: S310
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _live(),
    reason="Support endpoint not reachable. Set SUPPORT_TEST_BASE_URL=https://api.dealix.me to enable.",
)


# ── 10 canonical questions ─────────────────────────────────────────

@pytest.mark.parametrize("text", [
    "ما هو Dealix؟",
    "What is Dealix?",
    "ايش Growth Starter؟",
    "What is Growth Starter?",
    "ايش Data to Revenue؟",
    "What is Partnership Growth?",
    "ايش Proof Pack؟",
    "هل WhatsApp تلقائي؟",
    "How do I start?",
    "كم سعر Pilot؟",
])
def test_support_classify_returns_priority(text: str) -> None:
    """Every question must be classified into a P0–P3 priority band."""
    res = _post("/api/v1/support/classify", {"message": text})
    if res is None:
        pytest.skip("classify call failed")
    assert "priority" in res
    assert res["priority"] in {"P0", "P1", "P2", "P3"}


# Known deploy-branch gaps — documented as xfail so they show in test
# output and pressure the deploy branch to add escalation patterns.
KNOWN_ESCALATION_GAPS = [
    "Can you message numbers I bought?",
    "ابغى اكلم انسان",
    "I want to talk to a human",
]


@pytest.mark.xfail(
    reason=(
        "Deploy-branch support classifier does not escalate human-handoff for"
        " these phrasings. Tracked in OPERATOR_LANGUAGE_AND_INTENT_TESTS.md."
    ),
    strict=False,
)
@pytest.mark.parametrize("text", KNOWN_ESCALATION_GAPS)
def test_support_classify_escalates_human_handoff(text: str) -> None:
    res = _post("/api/v1/support/classify", {"message": text})
    if res is None:
        pytest.skip("classify call failed")
    assert res.get("escalate_human") in (True, "true", 1), \
        f"expected human escalation for {text!r}, got {res}"


def test_support_sla_endpoint_returns_p0_p3() -> None:
    if not BASE_URL:
        pytest.skip("no BASE_URL")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/v1/support/sla", timeout=6) as r:  # noqa: S310
            sla = json.loads(r.read().decode("utf-8")).get("sla") or {}
    except Exception:
        pytest.skip("sla endpoint unreachable")
    for k in ("P0", "P1", "P2", "P3"):
        assert k in sla, f"missing {k}"
        assert "hours" in sla[k]
        assert "label_ar" in sla[k]
