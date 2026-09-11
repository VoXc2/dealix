import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cmd',ROOT/'scripts/commercial/run_president_portfolio_command_v1.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
REG=json.loads((ROOT/'config/company/dealix_arm_registry.json').read_text()); DIMS=json.loads((ROOT/'config/company/dealix_portfolio_dimensions.json').read_text()); ARMS={a['id']:a for a in REG['arms']}
def base(**kw):
 d={'candidate_id':'x','arm_id':'ARM-001','sector_id':'PROFESSIONAL_SERVICES','buyer_group_id':'FOUNDER_CEO_GM','problem_class':'REVENUE_LEAKAGE','source':'evidence://x','evidence_refs':['ev1'],'buyer_access_evidence_refs':['ev2'],'relationship_state':'REAL_INTERACTION','suppression_state':'CLEAR','commercial_stage':'QUALIFIED_PROBLEM','validated_problem':True,'metrics':{k:80 for k in m.POS_WEIGHTS}|{k:10 for k in m.NEG_WEIGHTS}}; d.update(kw); return d
def test_no_evidence_cannot_deep(): assert m.classify(base(evidence_refs=[]),ARMS,DIMS)[0]=='BLOCKED_OR_EVIDENCE_GAP'
def test_suppression_blocks(): assert m.classify(base(suppression_state='OPTED_OUT'),ARMS,DIMS)[0]=='BLOCKED_OR_EVIDENCE_GAP'
def test_blocked_arm_cannot_activate(): assert m.classify(base(arm_id='ARM-042'),ARMS,DIMS)[0]=='BLOCKED_OR_EVIDENCE_GAP'
def test_research_only_not_deep(): assert m.classify(base(relationship_state='RESEARCH',commercial_stage='RESEARCH',validated_problem=False,buyer_access_evidence_refs=[]),ARMS,DIMS)[0]=='RADAR_ONLY'
def test_score_rewards_evidence_and_low_cost():
 hi=base(); lo=base(metrics={k:20 for k in m.POS_WEIGHTS}|{k:80 for k in m.NEG_WEIGHTS}); assert m.score(hi)[0]>m.score(lo)[0]
def test_deep_limit_contract(): assert REG['deep_wip_max']==3
def test_score_is_not_purchase_probability(): assert DIMS['economic_dispatcher']['score_type']=='PRIORITIZATION_HEURISTIC_NOT_FORECAST'

def test_source_bound_unmapped_target_stays_radar_only():
    status,gaps=m.classify(base(arm_id=None,sector_id=None,buyer_group_id=None,problem_class=None),ARMS,DIMS)
    assert status=='RADAR_ONLY'
    assert {'ARM_MAPPING_REQUIRED','SECTOR_MAPPING_REQUIRED','BUYER_GROUP_MAPPING_REQUIRED','PROBLEM_CLASS_MAPPING_REQUIRED'} <= set(gaps)

def test_complete_evidence_mapping_can_enter_deep_wip():
    assert m.classify(base(),ARMS,DIMS)==('DEEP_WIP_ELIGIBLE',[])
