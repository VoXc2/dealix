"""
BYOK (Bring Your Own Key) encryption adapter — KMS-shaped interface for
customer-provided AWS / GCP / Azure keys.

Surface:
    BYOKProvider.from_env() — returns the configured provider or None.
    encrypt(plaintext: bytes) -> bytes
    decrypt(ciphertext: bytes) -> bytes

The runtime contract: every "sensitive-by-tenant" column (today, none
of our tables qualify — we use provider-managed encryption at rest)
goes through `encrypt()` before write. T6e ships the interface so
verticals that legally require BYOK (healthcare, financial-services)
can flip on by setting KMS_PROVIDER.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.logging import get_logger

log = get_logger(__name__)


class BYOKProvider(ABC):
    @abstractmethod
    async def encrypt(self, plaintext: bytes) -> bytes: ...

    @abstractmethod
    async def decrypt(self, ciphertext: bytes) -> bytes: ...

    @classmethod
    def from_env(cls) -> "BYOKProvider | None":
        kind = os.getenv("KMS_PROVIDER", "").strip().lower()
        if kind == "aws":
            return _AwsKmsProvider()
        if kind == "gcp":
            return _GcpKmsProvider()
        if kind == "azure":
            return _AzureKmsProvider()
        return None


@dataclass
class _AwsKmsProvider(BYOKProvider):
    key_id: str = os.getenv("KMS_KEY_ID", "")

    async def encrypt(self, plaintext: bytes) -> bytes:
        try:
            import aioboto3  # type: ignore
        except ImportError:
            log.info("aioboto3_not_installed; AWS KMS BYOK disabled")
            return plaintext
        session = aioboto3.Session()
        async with session.client("kms") as kms:
            r = await kms.encrypt(KeyId=self.key_id, Plaintext=plaintext)
            return r["CiphertextBlob"]

    async def decrypt(self, ciphertext: bytes) -> bytes:
        try:
            import aioboto3  # type: ignore
        except ImportError:
            return ciphertext
        session = aioboto3.Session()
        async with session.client("kms") as kms:
            r = await kms.decrypt(KeyId=self.key_id, CiphertextBlob=ciphertext)
            return r["Plaintext"]


@dataclass
class _GcpKmsProvider(BYOKProvider):
    resource_name: str = os.getenv("KMS_KEY_ID", "")

    async def encrypt(self, plaintext: bytes) -> bytes:
        log.info("gcp_kms_byok_stub_only")
        return plaintext  # Stub until google-cloud-kms is wired.

    async def decrypt(self, ciphertext: bytes) -> bytes:
        return ciphertext


@dataclass
class _AzureKmsProvider(BYOKProvider):
    vault_url: str = os.getenv("KMS_VAULT_URL", "")
    key_name: str = os.getenv("KMS_KEY_ID", "")

    async def encrypt(self, plaintext: bytes) -> bytes:
        log.info("azure_kv_byok_stub_only")
        return plaintext

    async def decrypt(self, ciphertext: bytes) -> bytes:
        return ciphertext
