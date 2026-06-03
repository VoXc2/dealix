"""Runs the JSONL eval suites through the safety engine and asserts expectations.

This turns ``data/evals/*.jsonl`` into executable evals: a regression here means
a safety behaviour changed.
"""

import json
import os

import pytest

from core.safety.claims import has_prohibited_claims
from core.safety.outreach import is_fake_reply_subject, assess_outreach
from core.safety.whatsapp import contains_secret_or_api_key, assess_whatsapp_message
from core.safety.draft import evaluate_draft
from core.safety.replies import classify_reply
from core.safety.commercial import payment_handoff, renewal_allowed, won_deal_handoff

EVAL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "evals")


def _load(name):
    path = os.path.join(EVAL_DIR, name)
    cases = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def _run_gtm_safety(case):
    engine, inp, expect = case["engine"], case["input"], case["expect"]
    if engine == "claims":
        return ("block" if has_prohibited_claims(inp) else "allow") == expect
    if engine == "fake_subject":
        return ("block" if is_fake_reply_subject(inp) else "allow") == expect
    if engine == "whatsapp_cold":
        res = assess_whatsapp_message(inp, has_consent=False, inbound=False)
        return ("block" if not res.allowed else "allow") == expect
    if engine == "secret":
        return ("block" if contains_secret_or_api_key(inp) else "allow") == expect
    raise AssertionError(f"unknown engine {engine}")


def _run_draft(case):
    res = evaluate_draft(case["draft"], channel=case.get("channel", "email"))
    got = "send_ready" if res.send_ready else "block"
    return got == case["expect"]


def _run_crd(case):
    engine, inp, expect = case["engine"], case["input"], case["expect"]
    if engine == "reply":
        return classify_reply(inp) == expect
    if engine == "payment":
        return ("allow" if payment_handoff(inp).allowed else "block") == expect
    if engine == "renewal":
        return ("allow" if renewal_allowed(inp).allowed else "block") == expect
    if engine == "won_deal":
        return ("allow" if won_deal_handoff(inp).allowed else "block") == expect
    raise AssertionError(f"unknown engine {engine}")


@pytest.mark.parametrize("case", _load("gtm_safety_eval_cases.jsonl"), ids=lambda c: c["id"])
def test_gtm_safety_evals(case):
    assert _run_gtm_safety(case), f"{case['id']} failed: expected {case['expect']}"


@pytest.mark.parametrize("case", _load("gtm_draft_eval_cases.jsonl"), ids=lambda c: c["id"])
def test_gtm_draft_evals(case):
    assert _run_draft(case), f"{case['id']} failed: expected {case['expect']}"


@pytest.mark.parametrize("case", _load("client_revenue_delivery_cases.jsonl"), ids=lambda c: c["id"])
def test_client_revenue_delivery_evals(case):
    assert _run_crd(case), f"{case['id']} failed: expected {case['expect']}"
