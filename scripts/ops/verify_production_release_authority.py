#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CONTRACT=ROOT/'dealix/config/production_release_authority.json'
IAC=ROOT/'.railway/railway.ts'
RAILWAY=ROOT/'railway.json'
MATRIX=ROOT/'dealix/config/railway_services.json'
REQUIRED_WATCH={'/api/**','/app/**','/db/**','/dealix/**','/alembic/**','/alembic.ini'}

def main()->int:
    contract=json.loads(CONTRACT.read_text())
    assert contract['schema']=='dealix.production-release-authority.v1'
    assert contract['production_green'] is False
    assert contract['release_mode']=='manual_exact_sha'
    assert contract['github_actions_release_authority'] is False
    assert contract['third_party_commit_status_release_authority'] is False
    assert contract['railway_github_autodeploy_target']=='disabled_before_manual_release'
    assert contract['provider_mutation_authority']=='exact_action_bound_l5'
    iac=IAC.read_text()
    assert '"SMTP_PASSWORD="' not in iac
    assert 'SMTP_PASSWORD: preserve()' in iac
    railway=json.loads(RAILWAY.read_text())
    actual=set(railway['build']['watchPatterns'])
    matrix=json.loads(MATRIX.read_text())
    api=next(s for s in matrix['services'] if s.get('role')=='canonical_api' and s.get('productionAuthority') is True)
    expected=set(api['expectedWatchPatterns'])
    assert REQUIRED_WATCH <= actual
    assert actual==expected
    print('PRODUCTION_RELEASE_AUTHORITY=PASS_SOURCE_CONTRACT_ONLY')
    print('RELEASE_MODE=manual_exact_sha')
    print('PRODUCTION_GREEN=false')
    print('PROVIDER_MUTATION_AUTHORITY=exact_action_bound_l5')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
