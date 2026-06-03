"""Meta-safety: the *outbound content* the company would actually send must be
free of guaranteed/exaggerated claims.

We scan the customer-facing content data (outreach queue, approval queue draft
bodies, productized-service promises) — NOT the security/eval docs, which
intentionally quote prohibited phrases as negative examples.
"""

import json
import os

import pytest

from core.safety.claims import find_prohibited_claims

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _outreach_texts():
    path = os.path.join(ROOT, "company_os", "revenue", "outreach_queue.json")
    texts = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for item in data.get("queue", []):
            texts.append((item.get("id", "?"), (item.get("draft_subject", "") + "\n" + item.get("draft_body", ""))))
    return texts


def _approval_texts():
    path = os.path.join(ROOT, "company_os", "governance", "approval_queue.json")
    texts = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if item.get("type") == "outreach_message":
                texts.append((item.get("id", "?"), (item.get("draft_subject", "") + "\n" + item.get("draft_body", ""))))
    return texts


def test_outreach_queue_is_claim_free():
    for cid, text in _outreach_texts():
        claims = find_prohibited_claims(text)
        assert not claims, f"outreach {cid} has prohibited claims: {claims}"


def test_approval_queue_drafts_are_claim_free():
    for cid, text in _approval_texts():
        claims = find_prohibited_claims(text)
        assert not claims, f"approval {cid} has prohibited claims: {claims}"


def test_service_promises_are_claim_free():
    yaml = pytest.importorskip("yaml")
    path = os.path.join(ROOT, "data", "productized_services", "services.yaml")
    with open(path, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    for svc in doc.get("services", []):
        text = (svc.get("name", "") + "\n" + svc.get("promise", ""))
        claims = find_prohibited_claims(text)
        assert not claims, f"service {svc.get('id')} promise has prohibited claims: {claims}"
