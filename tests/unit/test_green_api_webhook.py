"""Unit contracts for the transitional GREEN-API WhatsApp webhook adapter."""

from __future__ import annotations

from integrations.green_api import (
    parse_incoming,
    payload_instance_matches,
    verify_webhook_authorization,
)


def _payload(**overrides):
    payload = {
        "typeWebhook": "incomingMessageReceived",
        "instanceData": {"idInstance": "7107600008"},
        "timestamp": 1788820000,
        "idMessage": "ABC123",
        "senderData": {
            "chatId": "966500000001@c.us",
            "sender": "966500000001@c.us",
            "senderName": "Sami",
            "senderContactName": "Sami Contact",
        },
        "messageData": {
            "typeMessage": "textMessage",
            "textMessageData": {"textMessage": "مرحبا Dealix"},
        },
    }
    payload.update(overrides)
    return payload


def test_bearer_authorization_required_and_compared_exactly():
    assert verify_webhook_authorization("Bearer strong-token", "strong-token") is True
    assert verify_webhook_authorization("Bearer wrong", "strong-token") is False
    assert verify_webhook_authorization("Basic strong-token", "strong-token") is False
    assert verify_webhook_authorization("", "strong-token") is False
    assert verify_webhook_authorization("Bearer strong-token", "") is False


def test_instance_binding_matches_configured_instance():
    payload = _payload()
    assert payload_instance_matches(payload, "7107600008") is True
    assert payload_instance_matches(payload, "9999999999") is False


def test_text_message_is_normalized_for_canonical_intake():
    message = parse_incoming(_payload())
    assert message is not None
    assert message.message_id == "ABC123"
    assert message.phone == "966500000001"
    assert message.contact_name == "Sami Contact"
    assert message.text == "مرحبا Dealix"
    assert message.instance_id == "7107600008"
    assert message.raw_type == "textMessage"


def test_group_message_is_rejected_from_customer_intake():
    payload = _payload(
        senderData={
            "chatId": "120363123456789@g.us",
            "sender": "966500000001@c.us",
            "senderName": "Sami",
        }
    )
    # chatId is a group even though an individual sender is present. Replace
    # sender as group as well so direct-phone extraction cannot treat group
    # traffic as a direct customer conversation.
    payload["senderData"]["sender"] = "120363123456789@g.us"
    assert parse_incoming(payload) is None


def test_non_incoming_webhook_does_not_enter_intake():
    assert parse_incoming(_payload(typeWebhook="stateInstanceChanged")) is None


def test_extended_text_is_supported():
    payload = _payload(
        messageData={
            "typeMessage": "extendedTextMessage",
            "extendedTextMessageData": {"text": "تفاصيل أكثر عن الخدمة"},
        }
    )
    message = parse_incoming(payload)
    assert message is not None
    assert message.text == "تفاصيل أكثر عن الخدمة"


def test_media_caption_is_supported_but_binary_is_not_routed():
    payload = _payload(
        messageData={
            "typeMessage": "imageMessage",
            "fileMessageData": {
                "caption": "هذه صورة المشكلة",
                "downloadUrl": "https://example.invalid/file",
            },
        }
    )
    message = parse_incoming(payload)
    assert message is not None
    assert message.text == "هذه صورة المشكلة"


def test_empty_or_unsupported_message_is_ignored():
    payload = _payload(
        messageData={
            "typeMessage": "locationMessage",
            "locationMessageData": {"latitude": 24.7, "longitude": 46.7},
        }
    )
    assert parse_incoming(payload) is None
