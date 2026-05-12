"""
Text-to-speech — ElevenLabs primary (Arabic Khaliji voices), Cartesia
fallback. Returns raw audio bytes (MP3 by default).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class TtsResult:
    audio: bytes
    provider: str
    voice_id: str
    mime: str = "audio/mpeg"


async def synthesise(text: str, *, voice_id: str | None = None, locale: str = "ar") -> TtsResult:
    if not text:
        return TtsResult(audio=b"", provider="none", voice_id="")
    el_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if el_key:
        vid = voice_id or os.getenv("ELEVENLABS_VOICE_ID_AR", "").strip() or "21m00Tcm4TlvDq8ikWAM"
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
                    headers={"xi-api-key": el_key, "Accept": "audio/mpeg"},
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                    },
                )
                r.raise_for_status()
                return TtsResult(audio=r.content, provider="elevenlabs", voice_id=vid)
        except Exception:
            log.exception("elevenlabs_tts_failed")

    cartesia_key = os.getenv("CARTESIA_API_KEY", "").strip()
    if cartesia_key:
        try:
            vid = voice_id or os.getenv("CARTESIA_VOICE_ID_AR", "").strip() or "default"
            async with httpx.AsyncClient(timeout=30) as c:
                r = await c.post(
                    "https://api.cartesia.ai/tts/bytes",
                    headers={"X-API-Key": cartesia_key, "Cartesia-Version": "2024-11-13"},
                    json={
                        "model_id": "sonic-multilingual",
                        "transcript": text,
                        "voice": {"mode": "id", "id": vid},
                        "output_format": {"container": "mp3", "encoding": "mp3", "sample_rate": 44100, "bit_rate": 128000},
                        "language": "ar" if locale.startswith("ar") else "en",
                    },
                )
                r.raise_for_status()
                return TtsResult(audio=r.content, provider="cartesia", voice_id=vid)
        except Exception:
            log.exception("cartesia_tts_failed")

    return TtsResult(audio=b"", provider="none", voice_id="")
