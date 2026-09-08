import importlib.util
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'scripts/commercial/run_targeted_outreach_clean_v2.py'
WRAPPER=ROOT/'scripts/ops/run_targeted_outreach_clean_v2_from_current_main.sh'
def module():
    spec=importlib.util.spec_from_file_location('outreach',RUNNER); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m); return m
def test_runner_has_no_send_endpoint():
    t=RUNNER.read_text().lower(); assert 'messages().send' not in t; assert 'messages.send' not in t; assert "drafts().create" in t
def test_suppression_blocks_draft():
    m=module(); c=m.normalize({'company_name':'Acme','verified_email':'x@acme.sa','source':'https://example.com','evidence_refs':['x'],'suppression_state':'OPTED_OUT'},{}); assert not c.draft_eligible and not c.dispatch_eligible
def test_public_contact_can_be_draft_but_not_dispatch():
    m=module(); c=m.normalize({'company_name':'Acme','verified_email':'x@acme.sa','source':'https://example.com','evidence_refs':['x'],'relationship_state':'RESEARCH','consent_state':'NONE'},{}); assert c.draft_eligible and not c.dispatch_eligible
def test_real_relationship_can_be_dispatch_candidate_without_send_authority():
    m=module(); c=m.normalize({'company_name':'Acme','verified_email':'x@acme.sa','source':'https://example.com','evidence_refs':['x'],'relationship_state':'WARM'},{}); assert c.dispatch_eligible
def test_probability_is_optional_consumer_only():
    t=RUNNER.read_text(); assert 'probability_revenue_engine' in t; assert 'probability_maximization_policy' not in t; assert 'probability_revenue_engine_v1.json' not in t
def test_wrapper_is_current_main_and_l4_only():
    t=WRAPPER.read_text().lower(); assert 'fetch origin main' in t; assert 'worktree add --detach' in t; assert 'reset --hard' not in t; assert 'external_send=0' in t; assert 'max_drafts=3' in t; assert 'l5_executed=none' in t
