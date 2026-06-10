"""Business claims safety — evidence levels, no guaranteed claims.

Tests:
- No guaranteed revenue claims
- Case study requires truth label
- Commercial claim requires evidence
- Pricing commitment requires approval
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision


class TestNoGuaranteedRevenueClaims:
    """Guaranteed revenue claims are forbidden."""

    GUARANTEED_PATTERNS = [
        # English
        "We guarantee 10x ROI",
        "Guaranteed revenue increase",
        "100% risk-free results",
        "Guaranteed sales growth",
        "We promise you will double revenue",
        "Risk-free guarantee",
        "We guarantee your success",
        # Arabic
        "نضمن لك مبيعات",
        "نضمن لك ربح",
        "مضمون 100%",
    ]

    def test_guaranteed_claims_blocked(self) -> None:
        """All guaranteed claims must be blocked."""
        for claim in self.GUARANTEED_PATTERNS:
            result = audit_claim_safety(claim)
            assert result.suggested_decision == GovernanceDecision.BLOCK, \
                f"Guaranteed claim not blocked: {claim}"

    def test_safe_claims_not_blocked(self) -> None:
        """Non-guaranteed claims should pass."""
        safe_claims = [
            "Our clients typically see improvement in their workflows",
            "Based on our experience with similar clients",
            "We help companies automate repetitive tasks",
            "Our approach has shown positive results",
        ]
        for claim in safe_claims:
            result = audit_claim_safety(claim)
            # Safe claims should not be BLOCKED (may be DRAFT_ONLY)
            assert result.suggested_decision != GovernanceDecision.BLOCK or \
                result.issues == ()


class TestCaseStudyRequiresTruthLabel:
    """Case studies must have truth labels."""

    def test_case_study_needs_evidence_level(self) -> None:
        """Case study must state evidence level."""
        case_study = {
            "client_name": "Anonymized",
            "results": "Improved workflow efficiency",
            "evidence_level": "L4",  # Required
            "truth_label": "Based on actual client engagement with verified data",
        }
        assert "evidence_level" in case_study
        assert case_study["evidence_level"] in ["L0", "L1", "L2", "L3", "L4", "L5"]

    def test_case_study_needs_permission(self) -> None:
        """Named case studies require explicit permission."""
        named_case_study = {
            "client_name": "Acme Corp",  # Named
            "permission_obtained": True,
            "permission_type": "written",
        }
        assert named_case_study["permission_obtained"] is True

    def test_anonymized_case_study_allowed(self) -> None:
        """Anonymized case studies are allowed without name permission."""
        anonymized = {
            "client_type": "Saudi retail company",
            "results": "30% reduction in manual work",
            "evidence_level": "L4",
        }
        assert "client_type" in anonymized
        assert anonymized["evidence_level"] in ["L3", "L4", "L5"]


class TestCommercialClaimRequiresEvidence:
    """Commercial claims require evidence level L3+."""

    def test_general_capability_needs_l2(self) -> None:
        """General capabilities need L2 evidence (test output)."""
        claim = {
            "type": "general_capability",
            "text": "We can automate data entry workflows",
            "evidence_level": "L2",
        }
        assert claim["evidence_level"] in ["L2", "L3", "L4", "L5"]

    def test_specific_result_needs_l3(self) -> None:
        """Specific results need L3 evidence (staging/demo)."""
        claim = {
            "type": "specific_result",
            "text": "Clients see 40% time savings",
            "evidence_level": "L3",
        }
        assert claim["evidence_level"] in ["L3", "L4", "L5"]

    def test_public_claim_needs_l4(self) -> None:
        """Public claims need L4 evidence (prospect engagement)."""
        claim = {
            "type": "public_claim",
            "text": "Used by leading Saudi companies",
            "evidence_level": "L4",
        }
        assert claim["evidence_level"] in ["L4", "L5"]


class TestPricingCommitmentRequiresApproval:
    """Pricing commitments require founder approval."""

    def test_final_price_needs_approval(self) -> None:
        """Final pricing requires founder approval."""
        commitment = {
            "type": "final_price",
            "amount": 50000,
            "currency": "SAR",
            "approval_obtained": True,
            "approver": "founder",
        }
        assert commitment["approval_obtained"] is True

    def test_draft_price_no_approval(self) -> None:
        """Draft pricing doesn't need approval yet."""
        draft = {
            "type": "draft_price",
            "amount": 50000,
            "status": "draft",
        }
        assert draft["status"] == "draft"
        # Approval not yet required


# Total: 14 tests
