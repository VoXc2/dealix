import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'config/company/dealix_arm_registry.json'
DIMS=ROOT/'config/company/dealix_portfolio_dimensions.json'

def load():
    return json.loads(REG.read_text()), json.loads(DIMS.read_text())

def test_registry_shape():
    r,d=load()
    assert len(r['arms'])==44
    assert r['deep_wip_max']==3
    assert sum(a['state']=='ACTIVE_DEEP' for a in r['arms'])==3
    assert len(r['permanent_agents'])==5

def test_dimensions_and_truth():
    r,d=load()
    assert len(d['operating_systems'])==12
    assert len(d['sectors'])==20
    assert len(d['factories'])==16
    assert len(d['buyer_groups'])==15
    assert len(d['problem_classes'])==24
    assert len(d['monetization_rails'])==18
    assert len(d['distribution_rails'])==20
    assert len(d['procurement_rails'])==10
    assert d['addressable_cell_contract']['minimum_addressable_surface']>=500
    assert d['portfolio_doctrine']['addressability_is_not_pipeline'] is True

def test_all_arms_have_gates_and_profile():
    r,d=load()
    assert all(a['dimension_profile'] in d['dimension_profiles'] for a in r['arms'])
    assert all(a['promotion_gate'] and a['kill_condition'] for a in r['arms'])
    assert all(a['evidence_required'] is True for a in r['arms'])

def test_l5_closed_and_regulated_boundaries():
    r,d=load()
    assert d['authority']['L5_universal'] is False
    assert all(v is False for k,v in d['authority'].items() if k not in {'L0_L4_autonomous','L5_universal'})
    by_id={a['id']:a for a in r['arms']}
    assert by_id['ARM-042']['state']=='BLOCKED'
    assert by_id['ARM-042']['promotion_gate']=='DATA_RIGHTS_GATE'
    for arm_id in {'ARM-023','ARM-024','ARM-028'}:
        assert by_id[arm_id]['promotion_gate']=='REGULATED_PARTNER_GATE'
