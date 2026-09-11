import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cmd',ROOT/'scripts/commercial/run_president_portfolio_command_v1.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
REG=json.loads((ROOT/'config/company/dealix_arm_registry.json').read_text()); DIMS=json.loads((ROOT/'config/company/dealix_portfolio_dimensions.json').read_text()); ARMS={a['id']:a for a in REG['arms']}
def base(**kw):
 d={'candidate_id':'x','arm_id':'ARM-001','sector_id':'PROFESSIONAL_SERVICES','buyer_group_id':'FOUNDER_CEO_GM','problem_class':'REVENUE_LEAKAGE','source':'evidence://x','evidence_refs':['ev1'],'buyer_access_evidence_refs':['ev2'],'economic_evidence_refs':['econ1'],'stop_loss_evidence_refs':[],'relationship_state':'REAL_INTERACTION','suppression_state':'CLEAR','commercial_stage':'QUALIFIED_PROBLEM','validated_problem':True,'metrics':{k:80 for k in m.POS_WEIGHTS}|{k:10 for k in m.NEG_WEIGHTS}}; d.update(kw); return d
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

def test_select_deep_hard_caps_at_three():
    rows=[{'candidate_id':str(i),'status':'DEEP_WIP_ELIGIBLE'} for i in range(5)]
    assert len(m.select_deep(rows,3))==3
    assert [x['candidate_id'] for x in m.select_deep(rows,3)]==['0','1','2']

def test_legacy_target_scores_feed_radar_metrics_without_new_commercial_facts(tmp_path):
    old_candidates,old_targets=m.DEFAULT_CANDIDATES,m.DEFAULT_TARGETS
    try:
        m.DEFAULT_CANDIDATES=tmp_path/'missing.json'
        m.DEFAULT_TARGETS=tmp_path/'targets.json'
        m.DEFAULT_TARGETS.write_text(json.dumps([{
            'id':'legacy-1','source':'evidence://legacy','evidence_refs':['ev'],
            'evidence_score':70,'urgency_score':60,'access_score':40,'fit_score':80
        }]))
        rows,_=m.candidate_source(None)
        assert rows[0]['metrics']=={'evidence_strength':70,'urgency':60,'buyer_access':40,'strategic_reuse':80}
        assert rows[0]['validated_problem'] is False
        assert rows[0]['relationship_state']=='RESEARCH'
    finally:
        m.DEFAULT_CANDIDATES, m.DEFAULT_TARGETS = old_candidates,old_targets

def test_mapping_suggestion_is_hypothesis_only():
    s=m.suggest_mapping({'segment':'Saudi logistics and fleet operator','pain_hypothesis':'manual workflow and document delays'})
    assert s['sector_id']=='LOGISTICS_SUPPLY_CHAIN'
    assert s['arm_id']=='ARM-018'
    assert s['origin']=='DETERMINISTIC_HYPOTHESIS_NOT_EVIDENCE'

def test_mapping_suggestion_does_not_make_candidate_deep():
    row=base(arm_id=None,sector_id=None,buyer_group_id=None,problem_class=None,segment='logistics',pain_hypothesis='manual handoff')
    _=m.suggest_mapping(row)
    assert m.classify(row,ARMS,DIMS)[0]=='RADAR_ONLY'

def test_missing_economic_evidence_stays_radar_only():
    status,gaps=m.classify(base(economic_evidence_refs=[]),ARMS,DIMS)
    assert status=='RADAR_ONLY'
    assert 'ECONOMIC_EVIDENCE_REQUIRED' in gaps

def test_evidenced_stop_loss_demotes_without_score_based_kill():
    status,gaps=m.classify(base(stop_loss_triggered=True,stop_loss_evidence_refs=['stop-proof']),ARMS,DIMS)
    assert status=='STOP_OR_DEMOTE'
    assert gaps==['STOP_LOSS_EVIDENCED']
