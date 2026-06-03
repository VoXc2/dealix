"""Unit tests for the safety gate. Crafted unsafe inputs MUST be caught."""

import safety_gate as sg


# --- Guaranteed-claim detection (Arabic + English) ---------------------------

def test_arabic_guaranteed_revenue_is_flagged():
    assert sg.find_guarantee_claims("نضمن لك زيادة المبيعات خلال شهر")


def test_arabic_guaranteed_results_is_flagged():
    assert sg.find_guarantee_claims("نتائج مضمونة 100%")


def test_english_10x_is_flagged():
    assert sg.find_guarantee_claims("We deliver 10x revenue growth")


def test_english_guarantee_is_flagged():
    assert sg.find_guarantee_claims("guaranteed results, risk-free")


def test_clean_copy_is_not_flagged():
    clean = "نسوي Sprint 5 أيام نكشف فيه أين تضيع الفرص ونعطيك خطة تشغيل."
    assert sg.find_guarantee_claims(clean) == []


# --- Misleading subjects -----------------------------------------------------

def test_fake_re_subject_flagged():
    assert sg.is_fake_reply_subject("Re: our conversation")


def test_fake_arabic_reply_subject_flagged():
    assert sg.is_fake_reply_subject("رد: بخصوص عرضنا")


def test_honest_subject_not_flagged():
    assert not sg.is_fake_reply_subject("وين تضيع فرص عملائك؟")


# --- Secret requests over chat -----------------------------------------------

def test_api_key_request_flagged():
    assert sg.requests_secret("أرسل لنا الـ API key الخاص بحسابك")


def test_password_request_flagged():
    assert sg.requests_secret("نحتاج كلمة المرور للوصول")


def test_normal_message_no_secret():
    assert not sg.requests_secret("نقدر نرسل لك نبذة مختصرة؟")


# --- End-to-end checks on crafted items --------------------------------------

def test_suppressed_recipient_blocked():
    items = [{"id": "APP-900", "type": "outreach_message", "company": "Blocked Co",
              "requires_approval": True, "approved": False, "draft_body": "hi"}]
    findings = sg.check_outbound_items(items, suppressed={"blocked co"})
    assert any(f["rule"] == "OUT-SUPPRESSED" for f in findings)


def test_unapproved_flag_blocked():
    items = [{"id": "APP-901", "type": "outreach_message", "company": "X",
              "requires_approval": False, "approved": False, "draft_body": "hi"}]
    findings = sg.check_outbound_items(items, suppressed=set())
    assert any(f["rule"] == "OUT-NO-APPROVAL-FLAG" for f in findings)


def test_ai_autoapproved_without_reviewer_blocked():
    items = [{"id": "APP-902", "type": "outreach_message", "company": "X",
              "requires_approval": True, "approved": True, "reviewed_by": None,
              "draft_body": "hi"}]
    findings = sg.check_outbound_items(items, suppressed=set())
    assert any(f["rule"] == "OUT-AUTO-APPROVED" for f in findings)


def test_pricing_offer_must_be_high_risk():
    items = [{"id": "APP-903", "type": "pricing_offer", "company": "X", "risk": "low",
              "requires_approval": True, "approved": False}]
    findings = sg.check_outbound_items(items, suppressed=set())
    assert any(f["rule"] == "OUT-RISK-LEVEL" for f in findings)


def test_whatsapp_without_consent_blocked():
    items = [{"id": "APP-904", "type": "outreach_message", "company": "X",
              "channel": "whatsapp_after_consent", "consent": False,
              "requires_approval": True, "approved": False, "draft_body": "hi"}]
    findings = sg.check_outbound_items(items, suppressed=set())
    assert any(f["rule"] == "WA-CONSENT" for f in findings)
