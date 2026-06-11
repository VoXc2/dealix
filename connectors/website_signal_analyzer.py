"""Website signal analyzer — reads a locally saved HTML/text snapshot.

Usage:
    python3 connectors/website_signal_analyzer.py --file data/imports/sample_website_text.txt --demo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from base import BaseConnector, ConnectorManifest
from source_audit import audit


SIGNAL_PATTERNS = {
    "no_booking_link": re.compile(r"\b(book|booking|schedule|appointment|احجز|حجز|موعد)\b", re.IGNORECASE),
    "has_contact_form": re.compile(r"<form", re.IGNORECASE),
    "has_whatsapp_link": re.compile(r"wa\.me|whatsapp\.com", re.IGNORECASE),
    "mentions_testimonials": re.compile(r"\b(testimonial|review|case stud|دراسة حالة|تقييم|آراء العملاء)\b", re.IGNORECASE),
    "has_pricing": re.compile(r"\b(pricing|price|تسعير|أسعار)\b", re.IGNORECASE),
    "has_cta": re.compile(r"\b(cta|call to action|تواصل|اتصل)\b", re.IGNORECASE),
    "has_clear_offer": re.compile(r"\b(offer|what we do|our service|خدماتنا|عرضنا)\b", re.IGNORECASE),
}


class WebsiteSignalAnalyzer(BaseConnector):
    manifest = ConnectorManifest(
        name="Website signal analyzer (local file)",
        source_type="website_signal",
        allowed_use="Read a manually saved HTML/text snapshot",
        restricted_use=["Crawling the live internet", "Behind-login content"],
        risk_level="low",
        notes="No network calls. Reads only what founder saved locally.",
    )

    def fetch_or_load(self) -> list[dict]:
        return [{"text": self._text}]

    def normalize(self, raw: list[dict]) -> list[dict]:
        return raw

    def validate(self, record: dict) -> bool:
        return "text" in record and bool(record["text"])

    def analyze(self) -> dict:
        text = self._text or ""
        signals = {k: bool(p.search(text)) for k, p in SIGNAL_PATTERNS.items()}
        weakness_score = sum(1 for v in signals.values() if not v)
        return {
            "signals": signals,
            "weakness_score": weakness_score,
            "weakness_hypothesis": "Possible workflow leakage: " + ", ".join(k for k, v in signals.items() if not v) or "no obvious weakness",
        }

    def run(self, file: Path, demo: bool) -> dict:
        if not file.exists():
            raise FileNotFoundError(file)
        self._source_note = file
        self._text = file.read_text(encoding="utf-8", errors="ignore")
        result = self.analyze()
        result["source"] = str(file)
        result["demo"] = demo
        audit(self, 1, self.root)
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    c = WebsiteSignalAnalyzer()
    out = c.run(args.file, args.demo)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
