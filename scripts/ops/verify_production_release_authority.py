#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "dealix/config/production_release_authority.json"
COMPOSE = ROOT / "deploy/selfhost/compose.yml"
SELFHOST_RELEASE = ROOT / "scripts/ops/selfhost_release.sh"
SELFHOST_RUNTIME_VERIFY = ROOT / "scripts/ops/verify_selfhost_only_runtime.py"
API_DOCKERFILE = ROOT / "Dockerfile"
WEB_DOCKERFILE = ROOT / "apps/web/Dockerfile"


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"] == "dealix.production-release-authority.v1"
    assert contract["production_green"] is False
    assert contract["release_mode"] == "manual_exact_sha"
    assert contract["canonical_acceptance_plane"] == "vps_exact_head"
    assert contract["github_actions_release_authority"] is False
    assert contract["third_party_commit_status_release_authority"] is False
    assert contract["selfhost_release_target"] == "canonical_vps_only"
    assert contract["provider_mutation_authority"] == "exact_action_bound_l5"

    compose = COMPOSE.read_text(encoding="utf-8")
    for required in (
        "GIT_SHA: ${DEALIX_GIT_SHA:?set exact DEALIX_GIT_SHA}",
        "dealix-api:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
        "dealix-web:${DEALIX_IMAGE_TAG:?set exact DEALIX_IMAGE_TAG}",
        "public-cutover",
        "production-db",
    ):
        assert required in compose

    release = SELFHOST_RELEASE.read_text(encoding="utf-8")
    assert "DEALIX_GIT_SHA" in release
    assert "DEALIX_IMAGE_TAG" in release
    assert "git rev-parse" in release
    assert "verify_selfhosted_production_plane.py" in release

    assert SELFHOST_RUNTIME_VERIFY.exists()
    assert not (ROOT / "railway.json").exists()
    assert not (ROOT / ".github/workflows").exists()

    for dockerfile in (API_DOCKERFILE, WEB_DOCKERFILE):
        source = dockerfile.read_text(encoding="utf-8")
        assert "ARG GIT_SHA=unknown" in source

    print("SELFHOST_RUNTIME_RELEASE_IDENTITY=SOURCE_WIRED")
    print("PRODUCTION_RELEASE_AUTHORITY=PASS_SOURCE_CONTRACT_ONLY")
    print("RELEASE_MODE=manual_exact_sha")
    print("PRODUCTION_GREEN=false")
    print("RUNTIME_MUTATION_AUTHORITY=exact_action_bound_l5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
