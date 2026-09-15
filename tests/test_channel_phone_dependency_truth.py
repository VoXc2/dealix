import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_phone_dependencies_are_channel_specific():
    data = json.loads((ROOT / 'data/commercial/channel_readiness_registry.json').read_text())
    channels = data['channels']
    wa = channels['whatsapp']
    voice = channels['voice']
    assert data['global_rules']['phone_is_not_global_blocker'] is True
    assert wa['phone_dependency'] is True
    assert wa['whatsapp_business_number_dependency'] is True
    assert voice['phone_dependency'] is True
    assert voice['whatsapp_business_number_dependency'] is False
    assert 'provider_and_number' in voice['activation_evidence_required']
    assert 'cold_autodialing' in voice['automation_blocked']
    assert 'live_outbound_without_action_bound_authority' in voice['automation_blocked']
