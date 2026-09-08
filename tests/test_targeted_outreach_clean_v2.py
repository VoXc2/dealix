import importlib.util
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'scripts/commercial/run_targeted_outreach_clean_v2.py'
WRAPPER=ROOT/'scripts/ops/run_targeted_outreach_clean_v2_from_current_main.sh'
def module():
    spec=importlib.util.spec_from_file_location('outreach',RUNNER); m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m); return m
def base(**updates):
    item={'company_name':'Acme','verified_email':'x@acme.sa','source':'https://example.com','evidence_refs':['x']}
    item.update(updates); return item
def test_runner_has_no_send_endpoint():
    t=RUNNER.read_text().lower(); assert 'messages().send' not in t; assert 'messages.send' not in t; assert "drafts().create" in t
def test_suppression_blocks_draft():
    m=module(); c=m.normalize(base(suppression_state='OPTED_OUT'),{}); assert not c.draft_eligible and not c.dispatch_eligible
def test_channel_research_only_blocks_outreach_draft():
    m=module(); c=m.normalize(base(channel_eligibility_state='RESEARCH_ONLY'),{}); assert not c.draft_eligible and not c.dispatch_eligible
def test_public_contact_can_be_internal_draft_but_not_dispatch_when_channel_unknown():
    m=module(); c=m.normalize(base(relationship_state='RESEARCH',consent_state='NONE'),{}); assert c.draft_eligible and not c.dispatch_eligible; assert c.channel_eligibility_state=='UNKNOWN_NOT_EVIDENCE_BACKED'
def test_real_relationship_alone_cannot_bypass_channel_eligibility():
    m=module(); c=m.normalize(base(relationship_state='WARM',channel_eligibility_state='DRAFT_ONLY'),{}); assert c.draft_eligible and not c.dispatch_eligible
def test_dispatch_candidate_requires_channel_eligibility_and_relationship_or_consent():
    m=module(); c=m.normalize(base(relationship_state='WARM',channel_eligibility_state='ELIGIBLE_PENDING_ACTION_AUTHORITY'),{}); assert c.dispatch_eligible
    c2=m.normalize(base(consent_state='PURPOSE_SPECIFIC',channel_eligibility_state='ELIGIBLE_PENDING_ACTION_AUTHORITY'),{}); assert c2.dispatch_eligible
    c3=m.normalize(base(channel_eligibility_state='ELIGIBLE_PENDING_ACTION_AUTHORITY'),{}); assert not c3.dispatch_eligible
def test_probability_is_optional_consumer_only():
    t=RUNNER.read_text(); assert 'probability_revenue_engine' in t; assert 'probability_maximization_policy' not in t; assert 'probability_revenue_engine_v1.json' not in t
def test_wrapper_is_current_main_and_l4_only():
    t=WRAPPER.read_text().lower(); assert 'fetch origin main' in t; assert 'worktree add --detach' in t; assert 'reset --hard' not in t; assert 'external_send=0' in t; assert 'max_drafts=3' in t; assert 'l5_executed=none' in t
