# 🚨 Dealix — Crisis Playbook (10 سيناريوهات)
## كتاب الأزمات الشامل: من PR إلى outages إلى churn إلى الاختراق

> **الإصدار:** v1.0 · **التاريخ:** 2026-06-10
> **الفلسفة:** "كل crisis فرصة لبناء ثقة"
> **المالك:** Founder + CTO + Legal Advisor
> **القاعدة:** شفافية كاملة + سرعة استجابة + حماية العميل أولاً

---

## القسم 1 — الإطار الموحد (Framework الموحد لكل الأزمات)

### 1.1 The 4-Phase Crisis Response
```
Phase 1: Detection (15 min)
  ↓
Phase 2: Containment (1-2 hours)
  ↓
Phase 3: Resolution (4-24 hours)
  ↓
Phase 4: Communication (concurrent + post)
```

### 1.2 Severity Levels
- **P0 (Critical):** outage كامل + اختراق بيانات + lawsuit
  - Response: 15 min
  - All-hands on deck
  - Legal involved
  - Public communication required
- **P1 (High):** partial outage + customer-facing bug
  - Response: 1 hour
  - Engineering on it
  - Direct customer communication
- **P2 (Medium):** feature broken + delayed delivery
  - Response: 4 hours
  - Engineering normal priority
  - Affected customers notified
- **P3 (Low):** minor issue + cosmetic bug
  - Response: 24 hours
  - Add to backlog
  - No communication needed

### 1.3 The 5-Step Communication Protocol
1. **Internal first** (before public) — 30 min max
2. **Affected customers** (directly) — 1 hour max
3. **All customers** (status page) — 2 hours max
4. **Public** (if needed) — 4 hours max
5. **Post-mortem** (always, within 7 days)

### 1.4 The Crisis Team
- **Incident Commander:** Founder (default) or CTO
- **Technical Lead:** CTO or senior engineer
- **Communications Lead:** Founder or Head of Marketing
- **Customer Liaison:** Head of CS (or CEO for major)
- **Legal Advisor:** on-call (for P0 only)

---

## القسم 2 — Crisis Scenario 1: Data Breach (اختراق بيانات)

### 2.1 Severity: P0
### 2.2 First 30 Minutes
1. **Detect** (anomaly / monitoring alert)
2. **Lock down** — Revoke compromised credentials
3. **Isolate** — Take affected systems offline
4. **Call Legal** — Within 15 minutes
5. **Document** — Start incident log

### 2.3 First 4 Hours
1. **Forensic analysis** — What was accessed, when, by whom
2. **Notify PDPL** — Mandatory within 24 hours (Saudi law)
3. **Identify affected customers** — Pull logs
4. **Prepare customer notification** — Draft (Legal review)
5. **Prepare public statement** — Draft (PR review)

### 2.4 First 24 Hours
1. **Notify affected customers** (within 24h per PDPL)
   - What happened
   - What data was accessed
   - What we're doing
   - What they should do
2. **Notify all customers** (status page)
3. **Submit PDPL report** (mandatory)
4. **Engage cybersecurity firm** (forensics + remediation)
5. **File insurance claim** (if applicable)

### 2.5 First 7 Days
1. **Post-mortem** (within 7 days, public)
2. **Customer remediation** (free service, credit)
3. **Policy updates** (security, training)
4. **Audit** (third-party security audit)
5. **Insurance / Legal follow-up**

### 2.6 Communication Templates

**Customer Email (Affected):**
```
Subject: [Action Required] Security Incident Notification — [Date]

Dear [Customer],

We are writing to inform you of a security incident that may have 
affected your data on [Date]. 

What happened:
[Brief, factual, no technical jargon]

What data was affected:
[Specific data categories]

What we are doing:
1. [Immediate action 1]
2. [Immediate action 2]
3. [Long-term action 1]

What you should do:
1. Change your password immediately
2. Enable 2FA
3. Review your account activity
4. [Specific actions if applicable]

We sincerely apologize. We take this seriously and are 
working with [cybersecurity firm] and the authorities.

Dedicated support: [email/phone]
Post-mortem: [URL]

[Name, Title]
Dealix
```

**Public Statement (Blog/Status Page):**
```
[Date] — Security Incident Update

We recently identified and addressed a security incident. 
[Details, transparency level decided with Legal]

What we know:
- Date detected: [Date]
- Date contained: [Date]
- Affected: [Number] customers
- Data accessed: [Categories]
- Action taken: [Actions]

What we're doing:
- [List of actions]

We are committed to transparency and will publish a full 
post-mortem within 7 days.

[Link to post-mortem when ready]
```

---

## القسم 3 — Crisis Scenario 2: Full Outage (انقطاع كامل)

### 3.1 Severity: P0
### 3.2 First 15 Minutes
1. **Detect** (monitoring, customer report)
2. **Page on-call** (engineering team)
3. **Status page: Investigating** (immediate)
4. **Internal all-hands** (Slack #incident)
5. **Start incident log**

### 3.3 First Hour
1. **Root cause identification** (50% of time)
2. **Workaround or fix** (50% of time)
3. **Status page: Identified** (with ETA)
4. **Notify Enterprise customers** (directly)
5. **Activate runbook** (specific to service)

### 3.4 First 4 Hours
1. **Fix deployed** (or mitigation)
2. **Status page: Monitoring**
3. **Verify all systems operational**
4. **Notify all customers** (status page update)
5. **Prepare detailed post-mortem**

### 3.5 Communication Templates

**Status Page Update:**
```
[Time] — Investigating
We are investigating an issue affecting [service]. 
Customers may experience [symptoms]. We will update 
within 30 minutes.

[Time] — Identified
We have identified the issue. The cause is [brief]. 
We are implementing a fix. ETA: [time].

[Time] — Monitoring
A fix has been deployed. We are monitoring for stability. 
If you continue to experience issues, contact [support].

[Time] — Resolved
This incident is resolved. We will publish a post-mortem 
within 7 days.
```

**Customer Email (Enterprise):**
```
Subject: [Service Disruption] — Update for [Customer]

Dear [Customer],

You may have experienced disruption to [service] 
between [start time] and [end time].

What happened:
[Brief, transparent]

What we did:
[Actions]

What we're doing to prevent recurrence:
[Long-term actions]

We value your trust. As a gesture, we are crediting 
your account with [X] ر.س.

[Name]
Dealix Support
```

---

## القسم 4 — Crisis Scenario 3: Major Customer Churn (فقدان عميل رئيسي)

### 4.1 Severity: P1 (Enterprise) / P2 (SMB)
### 4.2 First 24 Hours
1. **Schedule call** with customer (founder + CSM)
2. **Listen first** (no defense)
3. **Document reasons** (5-7 specific issues)
4. **Identify recovery path** (if any)
5. **Win-back offer** (if appropriate)

### 4.3 First Week
1. **Internal analysis** (why did we lose them?)
2. **Update win/loss tracker**
3. **Action items** (fix root causes)
4. **Team learning** (share in all-hands)
5. **NPS analysis** (is this a trend?)

### 4.4 Win-back Script (لـ 30 يوم بعد الـ churn)

```
[Customer name]،

أتمنى تكون بخير. أنا [Founder]، مؤسس Dealix.

لاحظت إنكم قررتوا عدم الاستمرار معنا. 
أقدّر صراحتكم وأعتذر عن أي قصور.

أبغى أفهم بشكل أعمق: وش كان السبب الرئيسي؟

لا أحاول أبيعكم — أحاول أتعلّم. 
15 دقيقة من وقتك ستكون ذات قيمة كبيرة لنا.

شكراً،
[Founder]
```

---

## القسم 5 — Crisis Scenario 4: Negative Press (تغطية سلبية)

### 5.1 Severity: P0 (viral) / P1 (industry-specific)
### 5.2 First Hour
1. **Monitor** (Google Alerts, Twitter, news)
2. **Assess accuracy** (true / false / mixed)
3. **Draft response** (Legal review)
4. **Identify stakeholders** (customers, investors, team)

### 5.3 First 4 Hours
1. **Public response** (if appropriate)
2. **Private response** (to journalist / author)
3. **Customer reassurance** (if affected)
4. **Internal communication** (team)
5. **Document everything**

### 5.4 First 7 Days
1. **Follow-up** (track narrative)
2. **Long-form response** (blog post)
3. **Engage community** (proactively)
4. **Lessons learned** (internal)

### 5.5 Response Template (Twitter/X)
```
We take [issue] seriously. Here's what happened: [brief]. 
What we're doing: [actions]. Full statement: [link]. 
We value transparency and welcome direct dialogue.
```

---

## القسم 6 — Crisis Scenario 5: Bad Customer Outcome (نتيجة سيئة للعميل)

### 6.1 Severity: P1
### 6.2 First 2 Hours
1. **Acknowledge** (to customer, immediately)
2. **Schedule call** (founder + team)
3. **Listen** (no excuses)
4. **Document** (what went wrong)

### 6.3 First 24 Hours
1. **Root cause analysis**
2. **Compensation offer** (refund, credit, free service)
3. **Action plan** (what we'll do differently)
4. **Follow-up commitment** (specific date)

### 6.4 First Week
1. **Verify action plan** (delivered)
2. **Customer satisfaction** (NPS post-fix)
3. **Internal review** (team learning)
4. **Update process** (prevent recurrence)

---

## القسم 7 — Crisis Scenario 6: Competitor Attack (هجوم منافس)

### 7.1 Severity: P2
### 7.2 Response
1. **Don't engage** (no public mud-slinging)
2. **Strengthen positioning** (internal)
3. **Customer reassurance** (if they ask)
4. **Differentiate clearly** (battlecards)
5. **Continue building** (best response)

### 7.3 Communication to Customers (if asked)
```
نقدّر اهتمامكم. [Competitor] نقدم خدمة مختلفة عنا. 
Dealix يتخصص في [differentiation]. 
لا تعليق على [competitor's claims]. 
دعونا نوضح ما يميز Dealix: [3 differentiators].
```

---

## القسم 8 — Crisis Scenario 7: Team Member Departure (مغادرة عضو فريق)

### 8.1 Severity: P1 (Senior) / P2 (Junior)
### 8.2 First Day
1. **Exit interview** (immediate)
2. **Knowledge transfer** (1 week)
3. **Access revocation** (immediate)
4. **Customer handover** (if customer-facing)
5. **Document** (role, responsibilities)

### 8.3 First Week
1. **Redistribute workload** (temporary)
2. **Plan replacement** (recruiter or internal)
3. **Team communication** (transparent, kind)
4. **Customer reassurance** (if applicable)
5. **Equity** (handle per agreement)

### 8.4 Internal Communication
```
Subject: Team Update

Hi team,

I want to share that [Name] has decided to move on 
from Dealix. We're grateful for their contributions 
during [time], particularly [specific impact].

[Name] will be supporting knowledge transfer over 
the next [X] weeks. [Plan for transition].

We're [hiring internally / looking externally] 
for their replacement. In the meantime, [interim plan].

Please reach out if you have questions.

[Founder]
```

---

## القسم 9 — Crisis Scenario 8: Regulatory Action (إجراء نظامي)

### 9.1 Severity: P0
### 9.2 First 24 Hours
1. **Engage Legal** (immediate)
2. **Document request** (full review)
3. **Internal investigation** (cooperative)
4. **Public silence** (until cleared)

### 9.3 First 30 Days
1. **Submit all requested documents**
2. **Cooperate fully** (with regulator)
3. **Implement corrective action** (if needed)
4. **Communicate to stakeholders** (as appropriate)
5. **Post-resolution** (lessons learned)

---

## القسم 10 — Crisis Scenario 9: Funding Crisis (أزمة تمويل)

### 10.1 Severity: P0
### 10.2 First Week
1. **Cash flow analysis** (runway)
2. **Cost reduction plan** (immediate)
3. **Investor communication** (transparent)
4. **Team communication** (within 48 hours)
5. **Emergency bridge** (if possible)

### 10.3 First 30 Days
1. **Extend runway** (cut costs 30-50%)
2. **Bridge round** (if possible, existing investors)
3. **Strategic alternatives** (acquisition, partnership)
4. **Customer communication** (if impact)
5. **Team retention** (equity refresh, bonuses)

### 10.4 Cost Reduction Levers
- Salaries (founder takes 0)
- Marketing (pause non-essential)
- Travel (0)
- Tools (audit, cut)
- Office (close)
- Contractors (pause)

---

## القسم 11 — Crisis Scenario 10: Founder Health Crisis (أزمة صحية للمؤسس)

### 11.1 Severity: P0
### 11.2 First 24 Hours
1. **Medical attention** (first priority)
2. **Notify Board** (within 24h)
3. **Designate Acting CEO** (if extended)
4. **Customer communication** (if needed)
5. **Team communication** (with care)

### 11.3 First 30 Days
1. **Rest + recovery** (non-negotiable)
2. **Interim leadership** (CTO or Board member)
3. **Customer reassurance** (continuity)
4. **Investor updates** (regular)
5. **Return plan** (when ready, partial first)

### 11.4 Prevention
- Health insurance (top tier)
- Annual health check
- Mental health support
- 4-day week option
- Mandatory vacation (2 weeks/year)

---

## القسم 12 — Crisis Communication Templates

### 12.1 Internal Crisis Email
```
Subject: [CRISIS] — [Brief description]

Team,

We have a [severity] situation: [brief].

Current status: [status]
Impact: [impact]
Lead: [person]

Action items:
- [Action 1] — [Owner] by [time]
- [Action 2] — [Owner] by [time]

Next update: [time]

This is a confidential all-hands. Please don't 
share externally until further notice.

[Name]
```

### 12.2 Customer Crisis Email
```
Subject: Important Update from Dealix

Dear [Customer],

We're writing to inform you of [brief, transparent description].

What happened:
[1-2 sentences]

Impact to you:
[Specific impact]

What we're doing:
1. [Action 1]
2. [Action 2]

What you need to do:
[Action items, if any]

We take this seriously and apologize for any inconvenience.
[Name] is your dedicated point of contact: [contact].

[Name, Title]
Dealix
```

### 12.3 Public Post-Mortem
```
# Post-Mortem: [Incident] — [Date]

## Summary
[Brief description]

## Impact
- Duration: [time]
- Affected: [number/type]
- Severity: [P0/P1/P2]

## Timeline
- [Time] — [Event]
- [Time] — [Event]
- [Time] — Resolution

## Root Cause
[Detailed, technical but accessible]

## What Went Well
- [Positive 1]
- [Positive 2]

## What Went Wrong
- [Issue 1]
- [Issue 2]

## What We're Changing
1. [Action 1] — Owner: [Name]
2. [Action 2] — Owner: [Name]
3. [Action 3] — Owner: [Name]

## Lessons
1. [Lesson 1]
2. [Lesson 2]

We appreciate your patience and feedback.
[Name, Founder]
```

---

## القسم 13 — Post-Mortem Culture

### 13.1 Blameless Post-Mortems
- Focus on systems, not individuals
- Assume good intent
- Identify improvements
- Track action items
- Follow up in 30/60/90 days

### 13.2 The 5 Whys
- Don't stop at first cause
- Ask "why" 5 times
- Find systemic issues

### 13.3 Action Item Tracking
- All post-mortems → Linear / Notion
- Owner assigned
- Due date set
- Reviewed monthly

---

## القسم 14 — Crisis Drills (التدريب على الأزمات)

### 14.1 Quarterly Drill
- **Q1:** Data breach simulation
- **Q2:** Outage simulation
- **Q3:** Negative PR simulation
- **Q4:** Funding crisis simulation

### 14.2 Tabletop Exercise
- 2 hours, all leadership
- Scenario walk-through
- Decisions logged
- Improvements identified

---

## القسم 15 — Crisis Resources (On-call)

### 15.1 Internal
- Founder: [phone] (24/7)
- CTO: [phone] (24/7)
- Legal Advisor: [phone] (after hours)
- PR Firm: [contact]

### 15.2 External
- Cybersecurity firm: [contact]
- PR firm: [contact]
- Legal: [firm name]
- Insurance: [broker]

### 15.3 Tools
- Incident management: [PagerDuty / Opsgenie]
- Status page: [Statuspage / Better Uptime]
- Communication: Slack #incident channel
- Documentation: Notion

---

## القسم 16 — Recovery & Trust Rebuilding

### 16.1 Short-term (1-7 days)
- Direct customer outreach
- Compensation/credit
- Transparent communication
- Action plan delivery

### 16.2 Medium-term (1-3 months)
- Process improvements
- Customer NPS recovery
- Public proof of change
- Win-back campaigns

### 16.3 Long-term (3-12 months)
- Trust rebuilding (gradually)
- Reference customers
- Case studies
- Brand strengthening

---

## القسم 17 — Red Lines (لا تفعل أبداً)

❌ لا تخفي crisis أبداً (يأتي أسوأ)
❌ لا تلوم العميل
❌ لا تبالغ في الرد
❌ لا تتجاهل القانون
❌ لا تكذب على العملاء
❌ لا تتأخر في الاستجابة >24h (P0)
❌ لا تتخذ قرارات كبيرة تحت الضغط
❌ لا تنسحب من التواصل بعد الأزمة

---

## القسم 18 — الخاتمة

> "كل crisis هي لحظة الحقيقة. الصدق + السرعة + التعلّم = بناء ثقة."

> "نحن في Dealix نؤمن أن العميل يستحق الحقيقة، حتى لو كانت مؤلمة. والشفافية هي أصولنا في الأزمات."

---

*آخر تحديث: 2026-06-10. هذا الملف وثيقة حيّة — يُحدّث بعد كل crisis.*

**Built for Resilience. Tuned for Trust. Ready for Anything.**

🌅 Dealix — Crisis is just another moment of truth.
