#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REG=ROOT/'config'/'company'/'dealix_arm_registry.json'; DIMS=ROOT/'config'/'company'/'dealix_portfolio_dimensions.json'; CAND=ROOT/'config'/'company'/'dealix_portfolio_candidate_contract.json'
OWNERS=['dealix-pm','dealix-sales','dealix-delivery','dealix-engineer','dealix-content']; IDS={f'ARM-{i:03d}' for i in range(1,45)}
def fail(x): raise SystemExit(f'DEALIX_ARM_REGISTRY=FAIL:{x}')
def main():
 if not REG.is_file() or not DIMS.is_file() or not CAND.is_file(): fail('missing_contract')
 r=json.loads(REG.read_text()); d=json.loads(DIMS.read_text()); c=json.loads(CAND.read_text())
 if r.get('schema')!='dealix.company-arm-portfolio-registry.v2' or d.get('schema')!='dealix.portfolio-dimensions.v1': fail('schema')
 if r.get('dimension_catalog')!='config/company/dealix_portfolio_dimensions.json': fail('dimension_catalog')
 if r.get('north_star')!='CASH_READY_AUTONOMOUS_DEALIX_COMPANY' or d.get('north_star')!=r['north_star']: fail('north_star')
 if r.get('deep_wip_max')!=3 or d.get('deep_wip_max')!=3: fail('deep_wip')
 if r.get('permanent_agents')!=OWNERS or d.get('permanent_agents')!=OWNERS: fail('agents')
 counts={'operating_systems':12,'factories':16,'sectors':20,'buyer_groups':15,'problem_classes':24,'proof_paths':8,'monetization_rails':18,'distribution_rails':20,'procurement_rails':10}
 for k,n in counts.items():
  v=d.get(k)
  if not isinstance(v,list) or len(v)!=n or len(v)!=len(set(v)): fail(k)
 arms=r.get('arms') or []
 if len(arms)!=44 or {a.get('id') for a in arms}!=IDS: fail('arms')
 if sum(a.get('state')=='ACTIVE_DEEP' for a in arms)!=3: fail('active_deep')
 profiles=d.get('dimension_profiles') or {}
 for a in arms:
  if a.get('owner') not in OWNERS or a.get('dimension_profile') not in profiles: fail(f'arm:{a.get("id")}')
  if not a.get('promotion_gate') or not a.get('kill_condition') or a.get('evidence_required') is not True: fail(f'gates:{a.get("id")}')
 by_id={a['id']:a for a in arms}
 if by_id['ARM-042']['state']!='BLOCKED' or by_id['ARM-042']['promotion_gate']!='DATA_RIGHTS_GATE': fail('data_licensing')
 for arm_id in {'ARM-023','ARM-024','ARM-028'}:
  if by_id[arm_id]['promotion_gate']!='REGULATED_PARTNER_GATE': fail(f'regulated_gate:{arm_id}')
 if set((d.get('special_boundaries') or {}).keys()) < {'ARM-016','ARM-023','ARM-024','ARM-028','ARM-042'}: fail('special_boundaries')
 if c.get('schema')!='dealix.portfolio-candidate-contract.v1' or c.get('promotion_law',{}).get('deep_wip_limit')!=3 or c.get('material_authority') is not False: fail('candidate_contract')
 catalogs={'sector_ids':set(d['sectors']),'buyer_group_ids':set(d['buyer_groups']),'factory_ids':set(d['factories']),'monetization_rail_ids':set(d['monetization_rails']),'distribution_rail_ids':set(d['distribution_rails']),'procurement_rail_ids':set(d['procurement_rails'])}
 for name,pf in profiles.items():
  for field,allowed in catalogs.items():
   vals=pf.get(field) or []
   if field!='procurement_rail_ids' and not vals: fail(f'profile_empty:{name}:{field}')
   if set(vals)-allowed-{'*'}: fail(f'profile_ref:{name}:{field}')
 if d['portfolio_doctrine'].get('addressability_is_not_pipeline') is not True: fail('addressability_truth')
 if d['addressable_cell_contract'].get('minimum_addressable_surface',0)<500: fail('surface')
 if d['economic_dispatcher'].get('score_type')!='PRIORITIZATION_HEURISTIC_NOT_FORECAST': fail('score_semantics')
 auth=d.get('authority') or {}
 if auth.get('L0_L4_autonomous') is not True or auth.get('L5_universal') is not False: fail('authority')
 if any(v is not False for k,v in auth.items() if k not in {'L0_L4_autonomous','L5_universal'}): fail('l5')
 print('DEALIX_ARM_REGISTRY=PASS'); print('ARMS=44'); print('PERMANENT_AGENTS=5'); print('ACTIVE_DEEP=3'); print('ADDRESSABLE_SURFACE=>=500_CAPABILITY_CELLS_NOT_PIPELINE'); return 0
if __name__=='__main__': raise SystemExit(main())
