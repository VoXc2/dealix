# 01 — استخبارات السوق / Market Intelligence (Layer 1)

**الهدف / Goal:** أن تعرف من نبيع له **الآن**، وليس نظرياً.

## العربية

### الـ ICPs الأولى الخمسة

1. **B2B Services** — استشارات، وكالات، شركات تنفيذ، خدمات مهنية.
2. **Clinics / Healthcare Operators** — عيادات، مجموعات طبية، خدمات كثيفة المواعيد.
3. **Fintech / Regulated Workflows** — مدفوعات، إقراض، عمليات كثيفة الامتثال.
4. **CRM / AI Consultants** — شركاء، منفّذون، مستشارون، fractional operators.
5. **VC / Portfolio Operators** — شركات ناشئة تحتاج governance playbook.

### إشارات الشراء

ابحث عن هذه الإشارات (من **مصادر علنية بموافقة فقط — لا scraping**):

```
hiring RevOps           hiring AI lead          CRM migration
HubSpot / Zoho / Salesforce usage               founder posting about AI
sales team growing      new funding             new location
high lead volume        complaints about follow-up
manual reporting
```

### قاعدة CEO للاستهداف

لا تستهدف «أي شركة مهتمة بـ AI». استهدف شركة عندها:

```
revenue workflow مؤلم  +  AI curiosity  +  قدرة دفع
```

ثلاثتها معاً. غياب أي واحدة = لا استهداف مباشر الآن.

### الربط بالنظام

- تقييم الـ ICP موجود فعلاً في `auto_client_acquisition/sales_os/icp_score.py`
  (5 أبعاد: B2B fit، data maturity، governance posture، budget signal،
  decision velocity).
- إشارات الشراء تُدخل يدوياً كحقل `main_pain` / `urgency` على الـ lead
  (انظر `03_LEAD_CAPTURE.md`).

---

## English

### The first five ICPs

1. **B2B Services** — consulting, agencies, implementation firms, professional services.
2. **Clinics / Healthcare Operators** — clinics, medical groups, appointment-heavy services.
3. **Fintech / Regulated Workflows** — payments, lending, compliance-heavy operations.
4. **CRM / AI Consultants** — partners, implementers, advisors, fractional operators.
5. **VC / Portfolio Operators** — startups needing a governance playbook.

### Buying signals

Look for these signals (from **public, consented sources only — no scraping**):

```
hiring RevOps           hiring AI lead          CRM migration
HubSpot / Zoho / Salesforce usage               founder posting about AI
sales team growing      new funding             new location
high lead volume        complaints about follow-up
manual reporting
```

### The CEO targeting rule

Do not target "any company interested in AI". Target a company that has:

```
a painful revenue workflow  +  AI curiosity  +  ability to pay
```

All three. Missing any one = no direct targeting now.

### How it connects to the system

- ICP scoring already exists in `auto_client_acquisition/sales_os/icp_score.py`
  (5 dimensions: B2B fit, data maturity, governance posture, budget signal,
  decision velocity).
- Buying signals are entered manually as the `main_pain` / `urgency` fields on
  the lead (see `03_LEAD_CAPTURE.md`).
