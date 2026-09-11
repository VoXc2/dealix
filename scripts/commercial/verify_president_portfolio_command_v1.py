#!/usr/bin/env python3
from __future__ import annotations
import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'scripts'/'commercial'/'run_president_portfolio_command_v1.py'
REGISTRY=ROOT/'config'/'company'/'dealix_arm_registry.json'
DIMENSIONS=ROOT/'config'/'company'/'dealix_portfolio_dimensions.json'

def main()->int:
    if not SCRIPT.is_file() or not REGISTRY.is_file() or not DIMENSIONS.is_file(): raise SystemExit('PRESIDENT_PORTFOLIO_COMMAND_VERIFY=FAIL:missing')
    src=SCRIPT.read_text(encoding='utf-8'); ast.parse(src)
    required=['deep_wip_selection','capability_cells_are_not_opportunities','PRIORITIZATION_HEURISTIC_NOT_PURCHASE_PROBABILITY','SUPPRESSION_BLOCK','ARM_STATE_BLOCKS_ACTIVATION','founder_required_actions','portfolio_enrichment_queue','ARM_MAPPING_REQUIRED']
    for token in required:
        if token not in src: raise SystemExit(f'PRESIDENT_PORTFOLIO_COMMAND_VERIFY=FAIL:missing_token:{token}')
    forbidden=['requests.post(','subprocess.run(','os.system(','git push','gh pr merge','railway up','stripe.','send_message(']
    for token in forbidden:
        if token in src: raise SystemExit(f'PRESIDENT_PORTFOLIO_COMMAND_VERIFY=FAIL:side_effect_surface:{token}')
    print('PRESIDENT_PORTFOLIO_COMMAND_VERIFY=PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
