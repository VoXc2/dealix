# 03 — التقاط الـ Leads / Lead Capture (Layer 3)

**القاعدة:** أي شخص يدخل من أي قناة لازم يدخل النظام كحدث موثق.
**Rule:** anyone entering from any channel must enter the system as a logged event.

## العربية

### حقول CRM

```
name              company           role
email             linkedin          industry
country           company_size      current_CRM
AI_usage          main_pain         urgency
budget_range      source            consent
lead_score        stage             next_action
last_touch        evidence_level
```

### تصنيف مصدر الـ Lead (source taxonomy)

```
linkedin_content   linkedin_dm        email_outbound
partner_referral   landing_page       proof_pack_download
risk_score         warm_intro         event
manual
```

### حدث الإثبات (evidence event)

كل lead يدخل كحدث:

```yaml
event_type: lead_captured
source: linkedin | form | email | partner
summary: why this lead matters
approved_by: system | Sami
```

### الربط بالنظام

- مخطط CRM موجود في `auto_client_acquisition/crm_v10/schemas.py`
  (`Account` / `Lead` / `Deal` / `Stage`). الحقول الإضافية أعلاه هي **فجوة**
  تُسد في **المرحلة 1** من `ENGINEERING_ROADMAP.md`.
- مداخل الالتقاط الحالية: `/api/v1/public/demo-request` و `lead_inbox.py`.
- نسب المصدر (`source`) جزء من `auto_client_acquisition/data_os/`.
- `consent` إلزامي قبل أي تخزين — `no_unconsented_data`.

---

## English

### CRM fields

```
name              company           role
email             linkedin          industry
country           company_size      current_CRM
AI_usage          main_pain         urgency
budget_range      source            consent
lead_score        stage             next_action
last_touch        evidence_level
```

### Lead source taxonomy

```
linkedin_content   linkedin_dm        email_outbound
partner_referral   landing_page       proof_pack_download
risk_score         warm_intro         event
manual
```

### Evidence event

Every lead enters as an event:

```yaml
event_type: lead_captured
source: linkedin | form | email | partner
summary: why this lead matters
approved_by: system | Sami
```

### How it connects to the system

- The CRM schema lives in `auto_client_acquisition/crm_v10/schemas.py`
  (`Account` / `Lead` / `Deal` / `Stage`). The extra fields above are a **gap**
  closed in **Phase 1** of `ENGINEERING_ROADMAP.md`.
- Existing capture entrypoints: `/api/v1/public/demo-request` and `lead_inbox.py`.
- Source attribution (`source`) is part of `auto_client_acquisition/data_os/`.
- `consent` is mandatory before any storage — `no_unconsented_data`.
