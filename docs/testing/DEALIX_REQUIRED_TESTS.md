# Dealix Required Tests

These tests **must exist** (names may map to current `tests/` files; keep behavior, not only filenames).

```text
tests/test_import_preview.py
tests/test_data_quality_score.py
tests/test_pii_detection.py
tests/test_governance_policy_check.py
tests/test_no_cold_whatsapp.py
tests/test_no_linkedin_automation.py
tests/test_no_guaranteed_claims.py
tests/test_no_fake_proof.py
tests/test_no_pii_in_logs.py
tests/test_no_source_no_answer.py
tests/test_account_scoring.py
tests/test_outreach_draft_only.py
tests/test_proof_pack_required.py
tests/test_qa_score.py
```

## Examples (reference signatures)

```python
def test_cold_whatsapp_is_blocked():
    context = {
        "channel": "whatsapp",
        "relationship_status": "unknown",
        "action": "send_message",
    }
    result = check_policy(context)
    assert result.decision == "BLOCK"


def test_outreach_is_draft_only_by_default():
    draft = generate_outreach_draft(account, offer)
    assert draft["draft_only"] is True
    assert draft["requires_human_approval"] is True


def test_company_brain_requires_source():
    answer = answer_question(question="What is policy?", sources=[])
    assert answer["insufficient_evidence"] is True
```

Repo today: align with `tests/test_data_os_helpers.py`, `tests/test_governance_*.py`, `tests/test_revenue_scoring.py`, etc. This document is the **contract**; filenames can be consolidated over time.
