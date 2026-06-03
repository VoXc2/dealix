"""GTM must never make guaranteed / exaggerated claims (Arabic + English)."""

import pytest

from core.safety.claims import find_prohibited_claims, has_prohibited_claims


@pytest.mark.parametrize("text", [
    "نضمن زيادة المبيعات خلال شهر",
    "10x revenue in 30 days",
    "results guaranteed or your money back",
    "نتائج مضمونة 100%",
    "نضاعف مبيعاتك",
    "double your revenue overnight",
    "زيادة 300% مضمونة",
])
def test_prohibited_claims_are_detected(text):
    assert has_prohibited_claims(text), f"should flag prohibited claim: {text!r}"
    assert find_prohibited_claims(text), f"should return markers for: {text!r}"


@pytest.mark.parametrize("text", [
    "نساعدك على تحسين التحويل عبر تحليل المسار",
    "We help you find where deals leak and propose a 30-day plan",
    "نطلع لك تقرير وخطة تشغيل واضحة",
])
def test_safe_copy_is_allowed(text):
    assert not has_prohibited_claims(text), f"should NOT flag safe copy: {text!r}"


def test_specific_required_phrase_fails():
    # Explicitly required by the hardening spec.
    assert has_prohibited_claims("نضمن زيادة المبيعات")
