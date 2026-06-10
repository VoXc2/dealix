"""Founder-facing notification helpers.

Currently exposes ``notify_founder_on_intake`` which is fired by the
lead-create endpoint after a new ``LeadRecord`` is persisted. The
recipient is always the founder (read from ``Settings.dealix_founder_email``);
this module never sends to a customer.
"""
from auto_client_acquisition.notifications.founder_alerts import (
    FounderAlertPayload,
    notify_founder_on_intake,
)

__all__ = ["FounderAlertPayload", "notify_founder_on_intake"]
