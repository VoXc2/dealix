"""WhatsApp only after consent. Cold automation must fail."""
from _util import decide, load_jsonl, DATA

ALLOWED = {"explicit_optin", "positive_reply", "booking", "form_submission", "existing_client"}


def test_cold_whatsapp_is_rejected():
    assert decide({"channel": "whatsapp", "consent_basis": "none"}) == "reject"
    assert decide({"channel": "whatsapp", "consent_basis": None}) == "reject"
    assert decide({"channel": "whatsapp", "consent_basis": "scraped"}) == "reject"


def test_post_consent_whatsapp_is_allowed():
    for basis in ALLOWED:
        case = {"channel": "whatsapp", "consent_basis": basis, "dry_run": True, "send_enabled": False}
        assert decide(case) == "allow", f"{basis} should be allowed"


def test_all_committed_sessions_are_post_consent():
    sessions = load_jsonl(DATA / "whatsapp" / "sessions.jsonl")
    assert sessions, "expected seed sessions"
    for s in sessions:
        basis = (s.get("consent") or {}).get("consent_basis")
        assert basis in ALLOWED, f"session {s.get('id')} not post-consent: {basis}"
        assert s.get("send_enabled") is False, f"session {s.get('id')} must have send_enabled=false in v1"
