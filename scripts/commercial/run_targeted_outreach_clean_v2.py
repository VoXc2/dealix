#!/usr/bin/env python3
"""Evidence-first targeted outreach preparation. Creates Gmail drafts only; never sends."""
from __future__ import annotations
import argparse, base64, csv, json, os, re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_JSON=ROOT/'data/self_operating_company_os/targets.json'
DEFAULT_CSV=ROOT/'data/targets/targeted_outreach_verified.csv'
DEFAULT_PROFILE=ROOT/'artifacts/commercial/Dealix_Company_Profile_2026.pdf'
DEFAULT_REPORT=ROOT/'reports/targeted_outreach'
PROBABILITY_REPORT=ROOT/'reports/probability_revenue_engine'
RIYADH=ZoneInfo('Asia/Riyadh')
REAL_RELATIONSHIP={'REAL_INTERACTION','VERIFIED_RELATIONSHIP','INBOUND','WARM','REFERRED'}
CONSENT_OK={'PURPOSE_SPECIFIC','INBOUND_REQUEST','CONSENTED'}
SUPPRESSED={'SUPPRESSED','OPTED_OUT','WITHDRAWN','DO_NOT_CONTACT'}
CHANNEL_DRAFT_BLOCKED={'BLOCKED','RESEARCH_ONLY','INBOUND_ONLY'}
CHANNEL_DISPATCH_OK={'ELIGIBLE_PENDING_ACTION_AUTHORITY'}
EMAIL_RE=re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
@dataclass
class Candidate:
    company:str; email:str; contact_name:str; language:str; source:str; evidence_refs:list[str]; relationship_state:str; consent_state:str; suppression_state:str; channel_eligibility_state:str; pain_hypothesis:str; why_now:str; offer:str; evidence_score:int; draft_eligible:bool; dispatch_eligible:bool; blocker:str; probability_rank:int|None
def today(): return datetime.now(RIYADH).strftime('%Y-%m-%d')
def utc_now(): return datetime.now(UTC).isoformat(timespec='seconds')
def probability_day(): return datetime.now(UTC).strftime('%Y-%m-%d')
def to_list(v:Any)->list[str]:
    if isinstance(v,list): return [str(x).strip() for x in v if str(x).strip()]
    if isinstance(v,str) and v.strip(): return [x.strip() for x in v.split('|') if x.strip()]
    return []
def bounded_int(v:Any,default:int)->int:
    try: return max(0,min(100,int(v)))
    except (TypeError,ValueError): return default
def evidence_score(item:dict[str,Any])->int:
    raw=bounded_int(item.get('fit_score'),55)*.30+bounded_int(item.get('urgency_score'),50)*.25+bounded_int(item.get('evidence_score'),40)*.25+bounded_int(item.get('access_score'),25)*.20-bounded_int(item.get('risk_score'),25)*.15
    return max(0,min(100,round(raw)))
def probability_ranks()->dict[str,int]:
    path=PROBABILITY_REPORT/f'{probability_day()}.json'
    try: data=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError): return {}
    result={}
    for row in data.get('ranked_targets',[]):
        if isinstance(row,dict) and row.get('deep_wip_candidate') is True and row.get('company_name') and isinstance(row.get('rank'),int): result[str(row['company_name']).strip().casefold()]=int(row['rank'])
    return result
def normalize(item:dict[str,Any],ranks:dict[str,int])->Candidate:
    company=str(item.get('company_name') or item.get('company') or '').strip(); email=str(item.get('verified_email') or item.get('email') or '').strip(); source=str(item.get('source') or item.get('source_url') or '').strip(); evidence=to_list(item.get('evidence_refs') or item.get('evidence')); rel=str(item.get('relationship_state') or 'RESEARCH').upper().strip(); consent=str(item.get('consent_state') or 'NONE').upper().strip(); suppression=str(item.get('suppression_state') or 'CLEAR').upper().strip(); channel=str(item.get('email_channel_eligibility') or item.get('channel_eligibility_state') or item.get('channel_eligibility') or 'UNKNOWN_NOT_EVIDENCE_BACKED').upper().strip(); blockers=[]
    if not company: blockers.append('company_missing')
    if suppression in SUPPRESSED: blockers.append('suppressed')
    if channel in CHANNEL_DRAFT_BLOCKED: blockers.append(f'channel_{channel.lower()}')
    if not source or not evidence: blockers.append('evidence_missing')
    if not email or not EMAIL_RE.match(email): blockers.append('verified_email_missing')
    draft_ok=not blockers; dispatch=draft_ok and channel in CHANNEL_DISPATCH_OK and (rel in REAL_RELATIONSHIP or consent in CONSENT_OK)
    return Candidate(company or 'Unknown company',email,str(item.get('contact_name') or '').strip(),'ar' if str(item.get('language') or item.get('language_pref') or 'en').lower().startswith('ar') else 'en',source or 'UNKNOWN_NOT_EVIDENCE_BACKED',evidence,rel,consent,suppression,channel,str(item.get('pain_hypothesis') or item.get('pain_angle') or 'UNKNOWN_NOT_EVIDENCE_BACKED').strip(),str(item.get('why_now') or item.get('trigger') or item.get('economic_trigger') or 'Current evidence suggests this workflow may be worth validating now.').strip(),str(item.get('recommended_offer') or item.get('offer') or 'Free Execution Diagnostic').strip(),evidence_score(item),draft_ok,dispatch,','.join(blockers),ranks.get(company.casefold()) if company else None)
def load_items(path:Path)->list[dict[str,Any]]:
    if not path.is_file(): return []
    if path.suffix.lower()=='.csv':
        with path.open(encoding='utf-8-sig',newline='') as fh: return [dict(r) for r in csv.DictReader(fh)]
    try: data=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError): return []
    return [x for x in data if isinstance(x,dict)] if isinstance(data,list) else []
def select(items:list[dict[str,Any]],limit:int)->tuple[list[Candidate],list[Candidate]]:
    ranks=probability_ranks(); rows=[normalize(x,ranks) for x in items]; rows.sort(key=lambda x:(x.probability_rank is not None,-(x.probability_rank or 10**9),x.evidence_score),reverse=True); return [x for x in rows if x.draft_eligible][:limit],[x for x in rows if not x.draft_eligible]
def subject(c:Candidate)->str: return f'{c.company} - فكرة تشخيص تنفيذ مختصر من Dealix' if c.language=='ar' else f'{c.company} - a focused execution diagnostic from Dealix'
def body(c:Candidate)->str:
    ref=c.evidence_refs[0] if c.evidence_refs else c.source
    if c.language=='ar': return f"السلام عليكم {' '+c.contact_name if c.contact_name else 'فريق '+c.company},\n\nمعك سامي، مؤسس Dealix. أتواصل لسبب محدد وليس برسالة عامة.\n\nWHY NOW: {c.why_now}\nفرضية نحتاج نتحقق منها — وليست ادعاء: {c.pain_hypothesis}\nمرجع الدليل: {ref}\n\nإذا كان الموضوع قريبًا من واقعكم، أقدر أجهز Free Execution Diagnostic من صفحة واحدة لهذا الـworkflow فقط. أرفقت ملف Dealix للتعريف.\n\nإذا غير مناسب، يكفيني رد مختصر وسأتوقف عن المتابعة.\n\nسامي\nFounder, Dealix\nRevenue + Proof + Command\n\n[DRAFT_ONLY — لم يتم الإرسال آليًا]"
    return f"Hello {c.contact_name or c.company+' team'},\n\nI'm Sami, founder of Dealix. I'm reaching out for a specific reason rather than a generic AI pitch.\n\nWHY NOW: {c.why_now}\nWorking hypothesis — not a claim: {c.pain_hypothesis}\nEvidence reference: {ref}\n\nIf this is relevant, I can prepare a one-page Free Execution Diagnostic focused only on this workflow. I've attached our company profile.\n\nIf it is not relevant, a short reply is enough and I will stop the follow-up.\n\nSami\nFounder, Dealix\nRevenue + Proof + Command\n\n[DRAFT_ONLY — not sent automatically]"
def gmail_service(token:Path):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    if not token.is_file(): raise RuntimeError(f'Gmail token missing: {token}')
    return build('gmail','v1',credentials=Credentials.from_authorized_user_file(str(token),['https://www.googleapis.com/auth/gmail.modify']),cache_discovery=False)
def create_draft(service,c:Candidate,profile:Path)->dict[str,Any]:
    msg=EmailMessage(); msg['To']=c.email; msg['Subject']=subject(c); msg['X-Dealix-Mode']='draft-only'; msg.set_content(body(c)); msg.add_attachment(profile.read_bytes(),maintype='application',subtype='pdf',filename='Dealix_Company_Profile_2026.pdf'); raw=base64.urlsafe_b64encode(msg.as_bytes()).decode('ascii'); d=service.users().drafts().create(userId='me',body={'message':{'raw':raw}}).execute(); return {'draft_id':d.get('id'),'company':c.company,'to':c.email}
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--targets-json',type=Path,default=Path(os.getenv('DEALIX_TARGETS_JSON',str(DEFAULT_JSON)))); ap.add_argument('--targets-csv',type=Path,default=Path(os.getenv('DEALIX_TARGETS_CSV',str(DEFAULT_CSV)))); ap.add_argument('--profile',type=Path,default=Path(os.getenv('DEALIX_COMPANY_PROFILE_PDF',str(DEFAULT_PROFILE)))); ap.add_argument('--report-root',type=Path,default=Path(os.getenv('DEALIX_TARGETED_OUTREACH_REPORT_ROOT',str(DEFAULT_REPORT)))); ap.add_argument('--max-drafts',type=int,default=int(os.getenv('DEALIX_OUTREACH_MAX_DRAFTS','3'))); ap.add_argument('--gmail-drafts',action='store_true',default=os.getenv('DEALIX_GMAIL_DRAFTS','0')=='1'); ap.add_argument('--gmail-token',type=Path,default=Path(os.getenv('GMAIL_TOKEN_PATH',str(ROOT/'token.json')))); a=ap.parse_args()
    if os.getenv('DEALIX_EMAIL_LIVE_SEND','0')=='1' or os.getenv('DEALIX_EXTERNAL_SEND','0')=='1': print('TARGETED_OUTREACH=BLOCKED_LIVE_SEND_FLAG_PRESENT'); return 2
    if not 1<=a.max_drafts<=3: print('TARGETED_OUTREACH=BLOCKED_WIP_LIMIT'); return 2
    if a.gmail_drafts and not a.profile.is_file(): print(f'TARGETED_OUTREACH=HOLD_COMPANY_PROFILE_MISSING path={a.profile}'); return 3
    items=load_items(a.targets_json); source=str(a.targets_json)
    if not items: items=load_items(a.targets_csv); source=str(a.targets_csv)
    selected,blocked=select(items,a.max_drafts); run=a.report_root/today(); run.mkdir(parents=True,exist_ok=True); (run/'selected_targets.json').write_text(json.dumps([asdict(x) for x in selected],ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (run/'blocked_targets.json').write_text(json.dumps([asdict(x) for x in blocked[:50]],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipts=[]; err=''
    if a.gmail_drafts and selected:
        try:
            service=gmail_service(a.gmail_token)
            for c in selected: receipts.append(create_draft(service,c,a.profile))
        except Exception as exc: err=f'{type(exc).__name__}: {exc}'
    summary={'timestamp':utc_now(),'mode':'draft-only','target_source':source,'eligible_selected':len(selected),'blocked_count':len(blocked),'gmail_drafts_requested':bool(a.gmail_drafts),'gmail_drafts_created':len(receipts),'gmail_error':err,'external_send':0,'dispatch_ready_count':sum(1 for x in selected if x.dispatch_eligible),'probability_policy_owner':'PR1583 when report is present; no local probability policy','note':'Draft artifacts only. This runner contains no Gmail send endpoint.'}; (run/'draft_receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (run/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,ensure_ascii=False,indent=2)); print(f'TARGETED_OUTREACH_REPORT={run}'); print('TARGETED_OUTREACH=PASS_DRAFT_ONLY'); print('L5_EXECUTED=NONE'); return 0
if __name__=='__main__': raise SystemExit(main())
