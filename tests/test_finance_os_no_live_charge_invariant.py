"""Hard rule: NO env combination can make live charge allowed.

This test sets `MOYASAR_SECRET_KEY=sk_live_...` AND
`DEALIX_ALLOW_LIVE_CHARGE=1` simultaneously and asserts
`is_live_charge_allowed()['allowed']` is STILL False. The CLI
guard at scripts/dealix_invoice.py is a second layer; this test
exercises the platform-level finance_os guard.
"""
from __future__ import annotations

import os

import pytest

from auto_client_acquisition.finance_os import is_live_charge_allowed


@pytest.fixture(autouse=False)
def restore_env():
    snapshot = {
        "MOYASAR_SECRET_KEY": os.environ.get("MOYASAR_SECRET_KEY"),
        "DEALIX_ALLOW_LIVE_CHARGE": os.environ.get("DEALIX_ALLOW_LIVE_CHARGE"),
    }
    yield
    for k, v in snapshot.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def test_default_state_is_blocked():
    result = is_live_charge_allowed()
    assert result["allowed"] is False


def test_sk_live_key_alone_does_not_unlock(restore_env):
    os.environ["MOYASAR_SECRET_KEY"] = "sk_" + "live" + "_test_should_be_refused"
    os.environ.pop("DEALIX_ALLOW_LIVE_CHARGE", None)
    result = is_live_charge_allowed()
    assert result["allowed"] is False
    assert result["key_mode"] == "live"


def test_explicit_allow_flag_alone_does_not_unlock(restore_env):
    os.environ.pop("MOYASAR_SECRET_KEY", None)
    os.environ["DEALIX_ALLOW_LIVE_CHARGE"] = "1"
    result = is_live_charge_allowed()
    assert result["allowed"] is False


def test_sk_live_AND_explicit_allow_flag_still_blocked(restore_env):
    """The hard invariant: even both signals together do NOT unlock
    a live charge. Founder must edit the CLI deliberately."""
    os.environ["MOYASAR_SECRET_KEY"] = "sk_" + "live" + "_test_should_be_refused"
    os.environ["DEALIX_ALLOW_LIVE_CHARGE"] = "1"
    result = is_live_charge_allowed()
    assert result["allowed"] is False, (
        "is_live_charge_allowed must remain False even with sk_live_* "
        "+ DEALIX_ALLOW_LIVE_CHARGE=1; this is a hard platform invariant"
    )
    assert result["key_mode"] == "live"
    assert result["explicit_flag_set"] is True


def test_test_mode_key_does_not_unlock(restore_env):
    os.environ["MOYASAR_SECRET_KEY"] = "sk_test_safe_value"
    os.environ.pop("DEALIX_ALLOW_LIVE_CHARGE", None)
    result = is_live_charge_allowed()
    assert result["allowed"] is False
    assert result["key_mode"] == "test"
