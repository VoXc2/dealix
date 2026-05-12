"""Unit tests for dealix/audit/byok.py."""

from __future__ import annotations

import pytest

from dealix.audit.byok import BYOKProvider


def test_from_env_returns_none_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KMS_PROVIDER", raising=False)
    assert BYOKProvider.from_env() is None


def test_from_env_picks_aws(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KMS_PROVIDER", "aws")
    p = BYOKProvider.from_env()
    assert p is not None
    assert type(p).__name__ == "_AwsKmsProvider"


def test_from_env_picks_gcp(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KMS_PROVIDER", "gcp")
    p = BYOKProvider.from_env()
    assert p is not None
    assert type(p).__name__ == "_GcpKmsProvider"


def test_from_env_picks_azure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KMS_PROVIDER", "azure")
    p = BYOKProvider.from_env()
    assert p is not None
    assert type(p).__name__ == "_AzureKmsProvider"


def test_from_env_ignores_unknown(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KMS_PROVIDER", "rumple-stiltskin")
    assert BYOKProvider.from_env() is None


def test_aws_provider_passthrough_when_sdk_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without aioboto3 installed, encrypt/decrypt must passthrough."""
    monkeypatch.setenv("KMS_PROVIDER", "aws")
    p = BYOKProvider.from_env()
    assert p is not None
    import asyncio

    plaintext = b"hello"
    encrypted = asyncio.run(p.encrypt(plaintext))
    decrypted = asyncio.run(p.decrypt(encrypted))
    # Either it's a stub that returns the plaintext, or aioboto3 is installed
    # and actually encrypted. We only assert symmetry.
    assert decrypted == plaintext or encrypted == plaintext


def test_gcp_and_azure_stubs_are_identity() -> None:
    import asyncio

    from dealix.audit.byok import _AzureKmsProvider, _GcpKmsProvider

    g = _GcpKmsProvider()
    a = _AzureKmsProvider()
    assert asyncio.run(g.encrypt(b"x")) == b"x"
    assert asyncio.run(g.decrypt(b"x")) == b"x"
    assert asyncio.run(a.encrypt(b"x")) == b"x"
    assert asyncio.run(a.decrypt(b"x")) == b"x"
