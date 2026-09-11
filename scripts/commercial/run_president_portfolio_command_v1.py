#!/usr/bin/env python3
"""Evidence-first economic ranking across Dealix arm/sector capability cells.

This command is internal/draft-only. It does not create prospects or commercial
facts, and never sends, publishes, pays, bids, merges, deploys, or mutates prod.
"""
from __future__ import annotations
import argparse, json, os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/'config'/'company'/'dealix_arm_registry.json'
DIMENSIONS=ROOT/'config'/'company'/'dealix_portfolio_dimensions.json'
DEFAULT_CANDIDATES=ROOT/'data'/'self_operating_company_os'/'portfolio_candidates.json'
DEFAULT_TARGETS=ROOT/'data'/'self_operating_company_os'/'targets.json'
OUT_ROOT=ROOT/'reports'/'president_portfolio_command'
FORBIDDEN_ENV={'DEALIX_EXTERNAL_SEND','DEALIX_EMAIL_LIVE_SEND','DEALIX_WHATSAPP_OUTBOUND','DEALIX_PUBLIC_PUBLISH','DEALIX_PAID_SPEND','DEALIX_PAYMENT_EXECUTION','DEALIX_PRODUCTION_MUTATION','DEALIX_DNS_MUTATION','DEALIX_DB_MUTATION','DEALIX_SECRET_MUTATION','DEALIX_IDENTITY_MUTATION','AUTO_MERGE_ENABLED','AUTO_DEPLOY_ENABLED'}
REAL_STAGES={'REAL_INTERACTION','VERIFIED_RELATIONSHIP','QUALIFIED_PROBLEM','FREE_MINI_DIAGNOSTIC','QUALIFIED_DISCOVERY','CUSTOMER_SPECIFIC_QUOTE','VERIFIED_PAYMENT','PAYMENT_EVIDENCE','DELIVERY','DELIVERY_EVIDENCE','CUSTOMER_VALIDATED_PROOF'}
SUPPRESSED={'SUPPRESSED','OPTED_OUT','WITHDRAWN'}
POS_WEIGHTS={'evidence_strength':0.16,'urgency':0.11,'buyer_access':0.10,'economic_impact':0.11,'gross_margin':0.08,'automation_ratio':0.07,'collection_probability':0.08,'proof_reuse':0.07,'strategic_reuse':0.06,'expansion_value':0.06,'partner_leverage':0.05,'productization_potential':0.05}
NEG_WEIGHTS={'time_to_cash':0.14,'founder_minutes':0.10,'delivery_cost':0.10,'compute_cost':0.05,'sales_cycle':0.10,'working_capital_risk':0.10,'compliance_risk':0.12,'security_risk':0.10,'irreversibility':0.07,'maintenance_debt':0.06,'opportunity_cost':0.06}

SECTOR_HINTS=[
    (('construction','contractor','epc','project services'),'CONSTRUCTION_EPC_PROJECT_SERVICES'),
    (('industrial','manufacturing','factory'),'INDUSTRIAL_MANUFACTURING'),
    (('logistics','supply chain','fleet','warehouse'),'LOGISTICS_SUPPLY_CHAIN'),
    (('energy','utility','oil','gas'),'ENERGY_UTILITIES_OIL_GAS'),
    (('mining','metals'),'MINING_METALS'),
    (('real estate','property','proptech','facility management'),'REAL_ESTATE_PROPTECH_FM'),
    (('healthcare','hospital','clinic','medical'),'HEALTHCARE_LIFE_SCIENCES'),
    (('fintech','bank','insurance','financial services'),'FINANCIAL_SERVICES_FINTECH_INSURANCE'),
    (('retail','ecommerce','e-commerce','shop'),'RETAIL_ECOMMERCE'),
    (('tourism','hospitality','hotel','event'),'TOURISM_HOSPITALITY_EVENTS'),
    (('saas','software','technology','system integrator','si '),'TECHNOLOGY_SAAS_SI'),
    (('telecom','media','marketing'),'TELECOM_MEDIA_MARKETING'),
    (('education','training','workforce'),'EDUCATION_WORKFORCE'),
    (('agriculture','food','water'),'AGRICULTURE_FOOD_WATER'),
    (('automotive','vehicle','mobility'),'MOBILITY_AUTOMOTIVE_FLEET'),
    (('export','import','rhq','market entry'),'EXPORT_IMPORT_RHQ_MARKET_ENTRY'),
    (('government','public sector','b2g'),'GOVERNMENT_B2G'),
]
PROBLEM_HINTS=[
    (('tender','procurement','rfp','rfq'),'PROCUREMENT_DELAY'),
    (('collection','receivable','invoice overdue'),'COLLECTION_DELAY'),
    (('quote','proposal delay'),'QUOTE_DELAY'),
    (('document','pdf','contract','paperwork'),'DOCUMENT_CHAOS'),
    (('approval','signoff'),'APPROVAL_DELAY'),
    (('cyber','security','agent governance'),'CYBER_AI_GOVERNANCE_RISK'),
    (('compliance','pdpl','fatoora'),'COMPLIANCE_RISK'),
    (('support','ticket','backlog'),'SUPPORT_BACKLOG'),
    (('project delay','schedule delay'),'PROJECT_DELAY'),
    (('inventory','stockout'),'INVENTORY_EXCEPTION'),
    (('data fragmentation','fragmented data','data silo'),'DATA_FRAGMENTATION'),
    (('manual handoff','handoff','manual workflow'),'MANUAL_HANDOFF'),
    (('revenue','sales','follow-up','pipeline leakage'),'REVENUE_LEAKAGE'),
    (('cost','waste'),'COST_LEAKAGE'),
    (('slow decision','decision latency'),'DECISION_LATENCY'),
]
SECTOR_ARM_HINTS={
    'INDUSTRIAL_MANUFACTURING':'ARM-017','LOGISTICS_SUPPLY_CHAIN':'ARM-018','REAL_ESTATE_PROPTECH_FM':'ARM-025',
    'HEALTHCARE_LIFE_SCIENCES':'ARM-024','RETAIL_ECOMMERCE':'ARM-022','TOURISM_HOSPITALITY_EVENTS':'ARM-026',
    'EDUCATION_WORKFORCE':'ARM-027','FINANCIAL_SERVICES_FINTECH_INSURANCE':'ARM-023',
}
PROBLEM_ARM_HINTS={'PROCUREMENT_DELAY':'ARM-012','CYBER_AI_GOVERNANCE_RISK':'ARM-006','COMPLIANCE_RISK':'ARM-006','REVENUE_LEAKAGE':'ARM-004'}

def truthy(v: str|None)->bool: return str(v or '').strip().lower() in {'1','true','yes','on'}
def load(path: Path)->Any: return json.loads(path.read_text(encoding='utf-8'))
def clamp(v:Any)->float:
    try: return max(0.0,min(100.0,float(v)))
    except (TypeError,ValueError): return 0.0

def tripwire()->list[str]: return sorted(k for k in FORBIDDEN_ENV if truthy(os.getenv(k)))

def candidate_source(path:Path|None)->tuple[list[dict[str,Any]],str]:
    if path and path.is_file():
        d=load(path); return ([x for x in d if isinstance(x,dict)] if isinstance(d,list) else []),str(path)
    if DEFAULT_CANDIDATES.is_file():
        d=load(DEFAULT_CANDIDATES); return ([x for x in d if isinstance(x,dict)] if isinstance(d,list) else []),str(DEFAULT_CANDIDATES)
    if DEFAULT_TARGETS.is_file():
        d=load(DEFAULT_TARGETS)
        rows=[]
        if isinstance(d,list):
            for i,t in enumerate(d,1):
                if not isinstance(t,dict): continue
                rows.append({
                  'candidate_id':str(t.get('candidate_id') or t.get('id') or f'TARGET-{i:04d}'),
                  'arm_id':t.get('arm_id'),'sector_id':t.get('sector_id'),'buyer_group_id':t.get('buyer_group_id'),
                  'problem_class':t.get('problem_class'),'company_name':t.get('company_name'),'segment':t.get('segment'),'pain_hypothesis':t.get('pain_hypothesis'),'buyer_role':t.get('buyer_role'),'source':t.get('source'),'evidence_refs':t.get('evidence_refs') or [],
                  'buyer_access_evidence_refs':t.get('buyer_access_evidence_refs') or [],
                  'economic_evidence_refs':t.get('economic_evidence_refs') or [],
                  'stop_loss_triggered':bool(t.get('stop_loss_triggered',False)),
                  'stop_loss_evidence_refs':t.get('stop_loss_evidence_refs') or [],
                  'relationship_state':t.get('relationship_state','RESEARCH'),'suppression_state':t.get('suppression_state','CLEAR'),
                  'commercial_stage':t.get('commercial_stage','RESEARCH'),'validated_problem':bool(t.get('validated_problem',False)),
                  'portfolio':t.get('portfolio','MONEY_NOW'),
                  'metrics':t.get('metrics') or {
                      'evidence_strength':t.get('evidence_score',0),
                      'urgency':t.get('urgency_score',0),
                      'buyer_access':t.get('access_score',0),
                      'strategic_reuse':t.get('fit_score',0),
                  },
                })
        return rows,str(DEFAULT_TARGETS)
    return [],'NO_EVIDENCE_SOURCE'

def score(row:dict[str,Any])->tuple[float,dict[str,float],dict[str,float]]:
    m=row.get('metrics') if isinstance(row.get('metrics'),dict) else {}
    pos={k:clamp(m.get(k)) for k in POS_WEIGHTS}; neg={k:clamp(m.get(k)) for k in NEG_WEIGHTS}
    p=sum(pos[k]*w for k,w in POS_WEIGHTS.items()); n=sum(neg[k]*w for k,w in NEG_WEIGHTS.items())
    return round(max(0,min(100,p-(0.45*n))),2),pos,neg

def _hint(text:str,hints:list[tuple[tuple[str,...],str]])->str|None:
    normalized=text.lower()
    for keywords,value in hints:
        if any(k in normalized for k in keywords): return value
    return None

def suggest_mapping(row:dict[str,Any])->dict[str,Any]:
    text=' '.join(str(row.get(k) or '') for k in ('segment','pain_hypothesis','company_name'))
    sector=str(row.get('sector_id') or '').strip() or _hint(text,SECTOR_HINTS)
    problem=str(row.get('problem_class') or '').strip() or _hint(text,PROBLEM_HINTS)
    arm=str(row.get('arm_id') or '').strip() or PROBLEM_ARM_HINTS.get(problem or '') or SECTOR_ARM_HINTS.get(sector or '')
    return {'arm_id':arm,'sector_id':sector,'problem_class':problem,'buyer_group_id':row.get('buyer_group_id'),'origin':'DETERMINISTIC_HYPOTHESIS_NOT_EVIDENCE'}

def economic_ready(row:dict[str,Any])->bool:
    refs=[x for x in (row.get('economic_evidence_refs') or []) if str(x).strip()]
    m=row.get('metrics') if isinstance(row.get('metrics'),dict) else {}
    return bool(refs) and clamp(m.get('economic_impact'))>0 and max(clamp(m.get('gross_margin')),clamp(m.get('collection_probability')))>0

def select_deep(ranked:list[dict[str,Any]],limit:int)->list[dict[str,Any]]:
    return [r for r in ranked if r.get('status')=='DEEP_WIP_ELIGIBLE'][:max(0,int(limit))]

def classify(row:dict[str,Any],arms:dict[str,dict[str,Any]],registry:dict[str,Any])->tuple[str,list[str]]:
    hard=[]; mapping=[]
    if bool(row.get('stop_loss_triggered')):
        stop_refs=[x for x in (row.get('stop_loss_evidence_refs') or []) if str(x).strip()]
        if stop_refs:
            return 'STOP_OR_DEMOTE',['STOP_LOSS_EVIDENCED']
        hard.append('STOP_LOSS_EVIDENCE_REQUIRED')
    aid=str(row.get('arm_id') or '').strip()
    arm=arms.get(aid) if aid else None
    if aid and not arm: hard.append('UNKNOWN_ARM_ID')
    elif arm and arm.get('state') in {'BLOCKED','STOPPED'}: hard.append('ARM_STATE_BLOCKS_ACTIVATION')
    elif not aid: mapping.append('ARM_MAPPING_REQUIRED')
    if not str(row.get('source') or '').strip(): hard.append('SOURCE_REQUIRED')
    if not [x for x in (row.get('evidence_refs') or []) if str(x).strip()]: hard.append('EVIDENCE_REFS_REQUIRED')
    if str(row.get('suppression_state','CLEAR')).upper() in SUPPRESSED: hard.append('SUPPRESSION_BLOCK')
    sec=str(row.get('sector_id') or '').strip()
    if sec and sec not in set(registry['sectors']): hard.append('UNKNOWN_SECTOR')
    elif not sec: mapping.append('SECTOR_MAPPING_REQUIRED')
    buyer=str(row.get('buyer_group_id') or '').strip()
    if buyer and buyer not in set(registry['buyer_groups']): hard.append('UNKNOWN_BUYER_GROUP')
    elif not buyer: mapping.append('BUYER_GROUP_MAPPING_REQUIRED')
    problem=str(row.get('problem_class') or '').strip()
    if problem and problem not in set(registry['problem_classes']): hard.append('UNKNOWN_PROBLEM_CLASS')
    elif not problem: mapping.append('PROBLEM_CLASS_MAPPING_REQUIRED')
    if hard: return 'BLOCKED_OR_EVIDENCE_GAP',hard+mapping
    stage=str(row.get('commercial_stage','RESEARCH')).upper()
    rel=str(row.get('relationship_state','RESEARCH')).upper()
    access_refs=[x for x in (row.get('buyer_access_evidence_refs') or []) if str(x).strip()]
    validated=bool(row.get('validated_problem')) or stage in {'QUALIFIED_PROBLEM','FREE_MINI_DIAGNOSTIC','QUALIFIED_DISCOVERY','CUSTOMER_SPECIFIC_QUOTE','VERIFIED_PAYMENT','PAYMENT_EVIDENCE','DELIVERY','DELIVERY_EVIDENCE','CUSTOMER_VALIDATED_PROOF'}
    has_access=bool(access_refs) or stage in REAL_STAGES or rel in {'REAL_INTERACTION','VERIFIED_RELATIONSHIP','INBOUND'}
    if not validated: mapping.append('VALIDATED_PROBLEM_REQUIRED')
    if not has_access: mapping.append('BUYER_ACCESS_EVIDENCE_REQUIRED')
    if not economic_ready(row): mapping.append('ECONOMIC_EVIDENCE_REQUIRED')
    if not mapping: return 'DEEP_WIP_ELIGIBLE',[]
    return 'RADAR_ONLY',mapping

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate-file',type=Path); ap.add_argument('--output-root',type=Path,default=OUT_ROOT); args=ap.parse_args()
    if not REGISTRY.is_file() or not DIMENSIONS.is_file(): print('PRESIDENT_PORTFOLIO_COMMAND=BLOCKED_REGISTRY_MISSING'); return 2
    reg=load(REGISTRY); dims=load(DIMENSIONS); arms={a['id']:a for a in reg['arms']}; violations=tripwire(); rows,source=candidate_source(args.candidate_file)
    ranked=[]; blocked=[]; stopped=[]; source_rows={str(r.get('candidate_id') or 'UNKNOWN'):r for r in rows}
    for raw in rows:
        status,gaps=classify(raw,arms,dims); s,pos,neg=score(raw)
        rec={'candidate_id':str(raw.get('candidate_id') or 'UNKNOWN'),'company_name':raw.get('company_name'),'segment':raw.get('segment'),'pain_hypothesis':raw.get('pain_hypothesis'),'arm_id':raw.get('arm_id'),'sector_id':raw.get('sector_id'),'buyer_group_id':raw.get('buyer_group_id'),'problem_class':raw.get('problem_class'),'portfolio':raw.get('portfolio','MONEY_NOW'),'status':status,'economic_priority_score':s,'score_semantics':'PRIORITIZATION_HEURISTIC_NOT_PURCHASE_PROBABILITY','evidence_refs':raw.get('evidence_refs') or [],'economic_evidence_refs':raw.get('economic_evidence_refs') or [],'stop_loss_evidence_refs':raw.get('stop_loss_evidence_refs') or [],'evidence_gaps':gaps,'positive_metrics':pos,'negative_metrics':neg,'material_authority':False}
        if status=='STOP_OR_DEMOTE': stopped.append(rec)
        elif status=='BLOCKED_OR_EVIDENCE_GAP': blocked.append(rec)
        else: ranked.append(rec)
    ranked.sort(key=lambda x:(-x['economic_priority_score'],x['candidate_id']))
    deep=select_deep(ranked,int(reg['deep_wip_max']))
    enrichment=[{'candidate_id':r['candidate_id'],'score':r['economic_priority_score'],'gaps':r['evidence_gaps'],'suggested_mapping':suggest_mapping(source_rows.get(r['candidate_id'],{})),'owner_agent':'dealix-pm'} for r in ranked if r['status']=='RADAR_ONLY'][:10]
    for r in deep:
        r['selected_deep_wip']=True; r['portfolio_decision']='EXECUTE_DEEP'
    for r in ranked:
        if 'selected_deep_wip' not in r: r['selected_deep_wip']=False
        if 'portfolio_decision' not in r: r['portfolio_decision']='QUEUE_ELIGIBLE' if r['status']=='DEEP_WIP_ELIGIBLE' else 'ENRICH'
    for r in stopped: r['selected_deep_wip']=False; r['portfolio_decision']='STOP_OR_DEMOTE'
    for r in blocked: r['selected_deep_wip']=False; r['portfolio_decision']='BLOCK'
    now=datetime.now(UTC); out=args.output_root/now.strftime('%Y-%m-%d'); out.mkdir(parents=True,exist_ok=True)
    payload={'schema':'dealix.president-portfolio-command.v1','generated_at':now.isoformat(),'mode':'draft-only','north_star':reg['north_star'],'portfolio_doctrine':dims['portfolio_doctrine'],'candidate_source':source,'radar_surface':{'canonical_arms':len(reg['arms']),'sectors':len(dims['sectors']),'buyer_groups':len(dims['buyer_groups']),'factories':len(dims['factories']),'monetization_rails':len(dims['monetization_rails']),'distribution_rails':len(dims['distribution_rails']),'minimum_addressable_capability_cells':dims['addressable_cell_contract']['minimum_addressable_surface'],'capability_cells_are_not_opportunities':True},'tripwire_violations':violations,'ranked_candidates':ranked,'deep_wip_selection':deep,'portfolio_enrichment_queue':enrichment,'stop_or_demote':stopped,'blocked_or_evidence_gap':blocked,'deep_wip_limit':reg['deep_wip_max'],'founder_required_actions':[],'next_autonomous_action':(f"Execute internal L0-L4 preparation for {deep[0]['candidate_id']} and preserve evidence/authority gates." if deep else (f"Record STOP/DEMOTE state for {stopped[0]['candidate_id']} from evidenced stop-loss; do not execute externally." if stopped else (f"Enrich highest-ranked RADAR_ONLY candidate {ranked[0]['candidate_id']} with explicit arm/sector/buyer/problem/economic evidence gaps." if ranked else 'Ingest source-bound candidate evidence; no synthetic opportunities created.'))),'material_authority':dims['authority']}
    (out/'president_command.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Dealix President Portfolio Command','',f"Source: `{source}`",f"Verdict: `{'HALTED_BY_ENV_TRIPWIRE' if violations else 'SAFE_INTERNAL_RANKING'}`",'',f"Radar: {len(reg['arms'])} arms x {len(dims['sectors'])} sectors x {len(dims['buyer_groups'])} buyer groups; addressability is not pipeline.",'','## Deep WIP <= 3']
    if deep:
        for x in deep: lines.append(f"- {x['candidate_id']} - {x['arm_id']} - score={x['economic_priority_score']} (prioritization only)")
    else: lines.append('- none; no evidence-qualified candidate is promoted')
    lines+=['','## Evidence gaps']
    for x in blocked[:20]: lines.append(f"- {x['candidate_id']}: {', '.join(x['evidence_gaps'])}")
    if not blocked: lines.append('- none')
    lines+=['','## Authority','- No external send, publish, tender, payment, merge, deploy, DNS/DB/secret/identity mutation is executed by this command.']
    (out/'president_command.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'ok':not violations,'source':source,'ranked':len(ranked),'deep_wip':len(deep),'stopped':len(stopped),'blocked':len(blocked),'output':str(out)},ensure_ascii=False))
    return 0 if not violations else 2
if __name__=='__main__': raise SystemExit(main())
