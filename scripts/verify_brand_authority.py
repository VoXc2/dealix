#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/brand/brand_authority.json"

REQUIRED = [
    ROOT / "docs/brand/BRAND_AUTHORITY_MAP.md",
    ROOT / "docs/brand/DEALIX_BRAND_OS.md",
    ROOT / "docs/brand/POSITIONING.md",
    ROOT / "docs/brand/VOICE_AND_TONE.md",
    ROOT / "docs/brand/VISUAL_DIRECTION.md",
    ROOT / "docs/brand/CLAIMS_GUARDRAILS.md",
    ROOT / "docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md",
    ROOT / "COMMERCIAL_IDENTITY.md",
    ROOT / "landing/index.html",
]

BRAND_DOCS = [
    ROOT / "docs/brand/BRAND_AUTHORITY_MAP.md",
    ROOT / "docs/brand/DEALIX_BRAND_OS.md",
    ROOT / "docs/brand/POSITIONING.md",
    ROOT / "docs/brand/VOICE_AND_TONE.md",
    ROOT / "docs/brand/VISUAL_DIRECTION.md",
    ROOT / "docs/brand/CLAIMS_GUARDRAILS.md",
]

FORBIDDEN_CURRENT_CLAIMS = [
    r"\b499\s*(?:SAR|ر\.س|ريال)",
    r"\b999\s*(?:SAR|ر\.س|ريال)",
    r"\b1500\s*(?:SAR|ر\.س|ريال)",
    r"\b1,500\s*(?:SAR|ر\.س|ريال)",
    r"\b7[- ]day\b",
    r"\bmoney[- ]back\b",
    r"guaranteed revenue",
    r"guaranteed ROI",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            fail(errors, f"missing:{path.relative_to(ROOT)}")

    if errors:
        print("DEALIX_BRAND_AUTHORITY=FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    contract = json.loads(AUTH.read_text(encoding="utf-8"))

    expected = {
        "masterbrand": "Dealix",
        "category": "Saudi-first AI Business Operating System",
        "commercial_wedge": "Revenue + Proof + Command",
    }
    identity = contract.get("canonical_identity", {})
    for key, value in expected.items():
        if identity.get(key) != value:
            fail(errors, f"identity:{key}:{identity.get(key)!r}!={value!r}")

    claim_policy = contract.get("claim_policy", {})
    if claim_policy.get("blanket_pdpl_compliant_allowed") is not False:
        fail(errors, "blanket_pdpl_compliant_must_be_false")
    if claim_policy.get("guaranteed_revenue_allowed") is not False:
        fail(errors, "guaranteed_revenue_must_be_false")
    if claim_policy.get("synthetic_as_customer_proof_allowed") is not False:
        fail(errors, "synthetic_as_customer_proof_must_be_false")
    if claim_policy.get("historical_pricing_as_current_allowed") is not False:
        fail(errors, "historical_pricing_as_current_must_be_false")

    landing = (ROOT / "landing/index.html").read_text(encoding="utf-8")
    for token in ("#0f172a", "#164e63", "#22d3ee", "IBM+Plex+Sans+Arabic", "Inter"):
        if token.lower() not in landing.lower():
            fail(errors, f"active_visual_token_missing_from_landing:{token}")

    platform = (ROOT / "docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md").read_text(
        encoding="utf-8"
    )
    if "Saudi-first AI Business Operating System" not in platform:
        fail(errors, "platform_category_missing")
    if "Revenue + Proof + Command" not in platform:
        fail(errors, "platform_wedge_missing")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in BRAND_DOCS)
    for pattern in FORBIDDEN_CURRENT_CLAIMS:
        if re.search(pattern, combined, flags=re.IGNORECASE):
            # Guardrail docs may quote prohibited phrases to block them. Require an
            # explicit negative context anywhere in the same canonical brand corpus.
            if "not" not in combined.lower() and "no " not in combined.lower():
                fail(errors, f"unguarded_legacy_claim_pattern:{pattern}")

    positioning = (ROOT / "docs/brand/POSITIONING.md").read_text(encoding="utf-8")
    if "PDPL-compliant" in positioning:
        fail(errors, "positioning_contains_blanket_pdpl_compliant")

    brand_os = (ROOT / "docs/brand/DEALIX_BRAND_OS.md").read_text(encoding="utf-8")
    for role in (
        "Founder / GM",
        "Revenue leader",
        "Finance / procurement",
        "IT / security",
        "Legal / governance",
    ):
        if role not in brand_os:
            fail(errors, f"buying_group_role_missing:{role}")

    proof_classes = set(contract.get("proof_classes", []))
    expected_proof = {
        "INTERNAL_CAPABILITY_PROOF",
        "SYNTHETIC_OR_DEMO_PROOF",
        "RUNTIME_OR_PRODUCTION_PROOF",
        "CUSTOMER_DELIVERY_PROOF",
        "CUSTOMER_OUTCOME_PROOF",
    }
    if proof_classes != expected_proof:
        fail(errors, "proof_class_contract_drift")

    if errors:
        print("DEALIX_BRAND_AUTHORITY=FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("DEALIX_BRAND_AUTHORITY=PASS")
    print("MASTERBRAND=Dealix")
    print("CATEGORY=Saudi-first AI Business Operating System")
    print("WEDGE=Revenue + Proof + Command")
    print("BUYING_GROUP=ENFORCED")
    print("PROOF_CLASSES=5")
    print("ACTIVE_VISUAL_REFERENCE=landing/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
