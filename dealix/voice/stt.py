"""
Speech-to-text — Deepgram primary (streaming Arabic), Whisper fallback,
AssemblyAI as third option.

Public surface:
    await transcribe(audio_bytes, *, locale="ar") -> TranscriptResult

Inert (returns empty text) when no STT provider is configured.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class TranscriptResult:
    text: str
    provider: str
    confidence: float
    locale: str


async def transcribe(audio_bytes: bytes, *, locale: str = "ar") -> TranscriptResult:
    if not audio_bytes:
        return TranscriptResult(text="", provider="none", confidence=0.0, locale=locale)
    # 1) Deepgram (streaming-first; we use the prerecorded endpoint here).
    deepgram_key = os.getenv("DEEPGRAM_API_KEY", "").strip()
    if deepgram_key:
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    "https://api.deepgram.com/v1/listen",
                    headers={
                        "Authorization": f"Token {deepgram_key}",
                        "Content-Type": "application/octet-stream",
                    },
                    params={"language": "ar" if locale.startswith("ar") else "en",
                             "model": "nova-2", "smart_format": "true"},
                    content=audio_bytes,
                )
                r.raise_for_status()
                data = r.json()
            alt = (
                ((data.get("results") or {}).get("channels") or [{}])[0].get("alternatives")
                or [{}]
            )[0]
            return TranscriptResult(
                text=str(alt.get("transcript") or ""),
                provider="deepgram",
                confidence=float(alt.get("confidence") or 0.0),
                locale=locale,
            )
        except Exception:
            log.exception("deepgram_stt_failed")

    # 2) OpenAI Whisper.
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            async with httpx.AsyncClient(timeout=60) as c:
                r = await c.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {openai_key}"},
                    files={"file": ("audio.wav", audio_bytes, "audio/wav")},
                    data={
                        "model": "whisper-1",
                        "language": "ar" if locale.startswith("ar") else "en",
                    },
                )
                r.raise_for_status()
                data = r.json()
            return TranscriptResult(
                text=str(data.get("text") or ""),
                provider="whisper",
                confidence=0.9,
                locale=locale,
            )
        except Exception:
            log.exception("whisper_stt_failed")

    # 3) AssemblyAI.
    aa_key = os.getenv("ASSEMBLYAI_API_KEY", "").strip()
    if aa_key:
        try:
            async with httpx.AsyncClient(timeout=60) as c:
                upload = await c.post(
                    "https://api.assemblyai.com/v2/upload",
                    headers={"authorization": aa_key},
                    content=audio_bytes,
                )
                upload.raise_for_status()
                upload_url = upload.json().get("upload_url")
                if not upload_url:
                    raise RuntimeError("assemblyai_upload_url_missing")
                tx = await c.post(
                    "https://api.assemblyai.com/v2/transcript",
                    headers={"authorization": aa_key, "content-type": "application/json"},
                    json={
                        "audio_url": upload_url,
                        "language_code": "ar" if locale.startswith("ar") else "en",
                    },
                )
                tx.raise_for_status()
                tx_id = tx.json()["id"]
            return TranscriptResult(
                text=f"(assemblyai pending tx={tx_id})",
                provider="assemblyai",
                confidence=0.85,
                locale=locale,
            )
        except Exception:
            log.exception("assemblyai_stt_failed")

    return TranscriptResult(text="", provider="none", confidence=0.0, locale=locale)
