import json
from pathlib import Path

from scripts.ops.verify_production_release_authority import main

ROOT = Path(__file__).resolve().parents[1]


def test_release_authority_contract_fails_closed_by_default():
    c = json.loads((ROOT / "dealix/config/production_release_authority.json").read_text())
    assert c["production_green"] is False
    assert c["release_mode"] == "manual_exact_sha"
    assert c["canonical_acceptance_plane"] == "vps_exact_head"
    assert c["github_actions_release_authority"] is False
    assert c["third_party_commit_status_release_authority"] is False
    assert c["selfhost_release_target"] == "canonical_vps_only"
    assert c["provider_mutation_authority"] == "exact_action_bound_l5"


def test_selfhost_source_contract_is_exact_sha_and_provider_independent():
    assert main() == 0


def test_legacy_provider_configs_are_not_release_authority():
    assert not (ROOT / "railway.json").exists()
    assert not (ROOT / ".github/workflows").exists()
