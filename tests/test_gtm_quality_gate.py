"""The draft quality/compliance gate behaves per the labeled eval set, all
production drafts pass, and a below-P1 draft is never send-ready. Also
cross-checks the Node gate agrees (skipped only if node is unavailable)."""
import shutil
import subprocess

import _loaders as L


def test_eval_cases_match_labels():
    fb, sup = L.forbidden(), L.suppression()
    cases = L.load_jsonl("data/evals/gtm_draft_eval_cases.jsonl")
    assert len(cases) >= 8
    for c in cases:
        res = L.gate_draft(c["draft"], fb, sup)
        got = "pass" if res["ok"] else "fail"
        assert got == c["expect"], f"{c['case_id']}: expected {c['expect']} got {got} {res['reasons']}"
        if c["expect"] == "fail":
            assert c["reason_code"] in res["reasons"], f"{c['case_id']}: {c['reason_code']} not in {res['reasons']}"


def test_all_production_drafts_pass_gate():
    fb, sup = L.forbidden(), L.suppression()
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        res = L.gate_draft(d, fb, sup)
        assert res["ok"], f"production draft {d['draft_id']} failed: {res['reasons']}"


def test_below_p1_is_not_send_ready():
    fb, sup = L.forbidden(), L.suppression()
    d = dict(L.load_jsonl("data/outreach/drafts.jsonl")[0])
    d["personalization_score"] = "P0"
    d["approval_status"] = "approved"
    # Even with an approved status and a sendable verdict, a P0 draft must fail.
    assert not L.is_send_ready(d, fb, sup, "RAMP_READY")


def test_default_verdict_blocks_all_sends():
    fb, sup = L.forbidden(), L.suppression()
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        assert not L.is_send_ready(d, fb, sup, "DRY_RUN_ONLY")


def test_node_gate_agrees_with_labels():
    node = shutil.which("node")
    if not node:  # documented environmental skip, not a rule relaxation
        import pytest
        pytest.skip("node not on PATH")
    r = subprocess.run([node, "scripts/draft-quality-gate.js", "--eval"], cwd=L.ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
