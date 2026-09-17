import pytest

from dealix.commercial.partner_program_v2 import PARTNER_POLICY_VERSION
from integrations.partner_portal.partner_registry import PartnerRegistration, PartnerRegistry


async def _registered_partner(registry: PartnerRegistry):
    return await registry.register(
        PartnerRegistration(
            company_name_ar="شركة اختبار",
            company_name_en="Test Partner Co",
            email="partner@example.sa",
            phone="0500000000",
            commercial_registration="CR-12345",
        )
    )


@pytest.mark.asyncio
async def test_activation_fails_closed_without_v3_gates():
    registry = PartnerRegistry()
    partner = await _registered_partner(registry)
    with pytest.raises(ValueError, match="partner_activation_hold"):
        await registry.approve(
            partner.id,
            legal_classification_status="hold",
            terms_accepted=False,
            certification_passed=False,
            tax_profile_recorded=False,
            policy_version="old-policy",
        )
    assert registry.get_partner(partner.id).status == "hold"


@pytest.mark.asyncio
async def test_activation_requires_exact_policy_and_all_evidence():
    registry = PartnerRegistry()
    partner = await _registered_partner(registry)
    active = await registry.approve(
        partner.id,
        legal_classification_status="clear",
        terms_accepted=True,
        certification_passed=True,
        tax_profile_recorded=True,
        policy_version=PARTNER_POLICY_VERSION,
    )
    assert active.status == "active"
    assert active.legal_classification_status == "clear"
    assert active.policy_version == PARTNER_POLICY_VERSION


@pytest.mark.asyncio
async def test_referral_volume_never_auto_upgrades_tier():
    registry = PartnerRegistry()
    partner = await _registered_partner(registry)
    await registry.approve(
        partner.id,
        legal_classification_status="clear",
        terms_accepted=True,
        certification_passed=True,
        tax_profile_recorded=True,
        policy_version=PARTNER_POLICY_VERSION,
    )
    for _ in range(50):
        await registry.update_referral_count(partner.id)
    assert registry.get_partner(partner.id).tier == "bronze"


@pytest.mark.asyncio
async def test_tier_upgrade_requires_verified_quality_and_compliance():
    registry = PartnerRegistry()
    partner = await _registered_partner(registry)
    await registry.approve(
        partner.id,
        legal_classification_status="clear",
        terms_accepted=True,
        certification_passed=True,
        tax_profile_recorded=True,
        policy_version=PARTNER_POLICY_VERSION,
    )
    with pytest.raises(ValueError, match="verified_economic_quality"):
        await registry.upgrade_tier(partner.id)
    upgraded = await registry.upgrade_tier(
        partner.id,
        verified_economic_quality=True,
        compliance_clear=True,
    )
    assert upgraded.tier == "silver"
