"""No API keys / secrets in WhatsApp text or any committed data file."""
from _util import decide, find_secret_like, DATA, ROOT


def test_detector_flags_api_key_in_message():
    # Clearly-fake placeholder token (not a real provider secret) — must still be caught.
    msg = "تمام، أرسل لي مفتاح الدخول: api_key=EXAMPLE_FAKE_TOKEN_1234567890"
    assert find_secret_like(msg), "detector should flag an api_key in a WhatsApp message"


def test_detector_flags_password_kv():
    assert find_secret_like("password=PLACEHOLDER_VALUE_123")


def test_clean_arabic_message_is_not_flagged():
    msg = "أهلًا، نبدأ بفحص الجاهزية؟ تقدر تختار: ابدأ، عندي سؤال، أو ما أعرف — اقترح علي."
    assert find_secret_like(msg) == [], "clean message must not be flagged"


def test_whatsapp_requesting_secret_is_rejected():
    case = {"channel": "whatsapp", "consent_basis": "positive_reply", "message_requests_secret": True}
    assert decide(case) == "reject"


def test_committed_whatsapp_data_has_no_secrets():
    for path in (DATA / "whatsapp").glob("*.jsonl"):
        text = path.read_text(encoding="utf-8")
        assert find_secret_like(text) == [], f"secret-like content in {path.name}"
    # templates/flows config too
    for name in ("templates.yaml", "flows.yaml"):
        text = (DATA / "whatsapp" / name).read_text(encoding="utf-8")
        assert find_secret_like(text) == [], f"secret-like content in {name}"
