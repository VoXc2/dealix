"""WhatsApp messages must never carry or request secrets / API keys."""

import pytest

from core.safety.whatsapp import (
    contains_secret_or_api_key, requests_api_key, assess_whatsapp_message,
)


@pytest.mark.parametrize("text", [
    "here is the key sk-ABCD1234EFGH5678IJKL",
    "token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345",
    "AWS AKIAIOSFODNN7EXAMPLE",
    "api_key=supersecretvalue1234",
    "Authorization: Bearer eyJhbGciOiJI.eyJzdWIiOiIx.abcDEF",
])
def test_secret_in_text_detected(text):
    assert contains_secret_or_api_key(text) is True
    res = assess_whatsapp_message(text, has_consent=True)
    assert "secret_in_text" in res.violations
    assert res.allowed is False


@pytest.mark.parametrize("text", [
    "please send your api key so we can connect",
    "share the secret token with me",
    "أرسل لي مفتاح الـ api من فضلك",
])
def test_api_key_request_detected(text):
    assert requests_api_key(text) is True
    res = assess_whatsapp_message(text, has_consent=True)
    assert "api_key_request" in res.violations
    assert res.requires_human is True


def test_clean_message_passes():
    res = assess_whatsapp_message("شكراً، نكمل الاجتماع الساعة 4 عصراً", has_consent=True)
    assert res.allowed is True
