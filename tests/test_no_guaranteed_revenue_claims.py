"""
Test: No Guaranteed Revenue Claims
Ensures no customer-facing artifact contains 'guaranteed revenue', 'guaranteed ROI',
or similar forbidden claims.
"""
from pathlib import Path


FORBIDDEN_PHRASES = [
    "guaranteed revenue",
    "guaranteed roi",
    "guaranteed results",
    "guaranteed increase",
    "ضمان النتائج",
    "ضمان الإيراد",
    "ضمان العائد",
    "نتائج مضمونة",
    "إيراد مضمون",
    "roi مضمون",
    "always will",
    "never fails",
    "100% success",
    "نسبة نجاح 100",
]


def test_no_guaranteed_in_proposal_docs():
    """No guaranteed claims in proposal/proof docs (as positive statements)."""
    docs = [
        "docs/commercial/PROPOSAL_STRATEGY_AR.md",
        "docs/commercial/PROOF_PACK_COMMERCIAL_GUIDE_AR.md",
        "docs/commercial/CASE_STUDY_POLICY_AR.md",
        "docs/commercial/ROI_CONVERSATION_GUIDE_AR.md",
    ]

    for doc_path in docs:
        if not Path(doc_path).exists():
            continue
        content = Path(doc_path).read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            # If phrase appears, it must be in a "forbidden" or "don't" context
            occurrences = content.count(phrase.lower())
            if occurrences > 0:
                # Check context around each occurrence
                for match in re.finditer(re.escape(phrase.lower()), content):
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 100)
                    context = content[start:end]
                    is_forbidden_context = any(
                        kw in context
                        for kw in [
                            "forbidden",
                            "don't",
                            "لا",
                            "ممنوع",
                            "should not",
                            "must not",
                            "refuse",
                            "disqualify",
                            "walk away",
                            "not allowed",
                            "لا نقدم",
                            "لا نضمن",
                            "refused",
                        ]
                    )
                    if not is_forbidden_context:
                        # Allow if the example shows a negative response (e.g., "Client asks for X, response: We don't...")
                        if "refuse" in context or "rejection" in context or "رفض" in context:
                            continue
                        assert False, (
                            f"{doc_path} contains non-forbidden context for '{phrase}': "
                            f"...{context[:150]}..."
                        )


def test_claim_policy_yaml_structure():
    """claim_policy.yaml must have correct structure."""
    import yaml

    with open("dealix/config/claim_policy.yaml", encoding="utf-8") as f:
        policy = yaml.safe_load(f)

    assert "rules" in policy
    assert "labels" in policy

    # ROI/guarantee must be disallowed
    rules = policy["rules"]
    assert rules.get("roi_or_guarantee", {}).get("allowed") is False, (
        "ROI/guarantee claims must be forbidden"
    )


def test_no_overclaim_yaml_structure():
    """no_overclaim.yaml must exist with claims tracking."""
    import yaml

    try:
        with open("dealix/registers/no_overclaim.yaml", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return  # Optional file

    # If exists, must have claims list
    if data:
        assert isinstance(data, (list, dict)), (
            "no_overclaim.yaml must be a list or dict"
        )


def test_pricing_yaml_no_guaranteed():
    """pricing.yaml must not have 'guaranteed' phrasing."""
    import yaml

    with open("dealix/config/pricing.yaml", encoding="utf-8") as f:
        content = f.read().lower()

    forbidden_in_pricing = [
        "guaranteed",
        "ضمان",
        "results guaranteed",
    ]

    for phrase in forbidden_in_pricing:
        if phrase in content:
            # Check context
            if "no " + phrase not in content and "not " + phrase not in content:
                assert False, f"pricing.yaml contains forbidden phrase: {phrase}"


import re


if __name__ == "__main__":
    test_no_guaranteed_in_proposal_docs()
    test_claim_policy_yaml_structure()
    test_no_overclaim_yaml_structure()
    test_pricing_yaml_no_guaranteed()
    print("All no guaranteed revenue claims tests passed")
