"""All real client-facing copy must be free of guaranteed-revenue claims."""

import safety_gate as sg
from conftest import load_json


def _walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


def test_approval_queue_drafts_have_no_guarantees(company_os):
    queue = load_json(company_os / "governance" / "approval_queue.json")
    for item in queue:
        body = " ".join([str(item.get("draft_subject", "")), str(item.get("draft_body", ""))])
        assert sg.find_guarantee_claims(body) == [], item.get("id")


def test_objection_responses_have_no_guarantees(company_os):
    data = load_json(company_os / "revenue" / "objections.json")
    for text in _walk_strings(data):
        assert sg.find_guarantee_claims(text) == [], text[:80]


def test_outreach_queue_has_no_guarantees(company_os):
    data = load_json(company_os / "revenue" / "outreach_queue.json")
    for text in _walk_strings(data):
        assert sg.find_guarantee_claims(text) == [], text[:80]
