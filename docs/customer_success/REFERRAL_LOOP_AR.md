# Referral Loop
# حلقة الإحالة

> **النسخة:** 1.0  
> **التاريخ:** 2026-06-03  
> **Owner:** Customer Success Lead  
> **الغرض:** بناء نظام إحالات مستدام يحول العملاء السعداء إلى سفراء

---

## 1. Referral Overview

### 1.1 Referral Philosophy

- **أفضل العملاء يجلبون أفضل العملاء**
- **الإحالة ثقة مصدقة**
- **كل إحالة فرصة لنمو**
- **المعاملة المتبادلة = برنامج مستدام**

### 1.2 Referral Types

| Type | Description | Conversion Rate |
|------|-------------|-----------------|
| Direct Referral | Client names specific prospect | 30-50% |
| Warm Introduction | Client introduces via email/call | 20-30% |
| Mention | Client mentions to peer | 10-20% |
| Public Mention | Client posts/shares publicly | 5-15% |

### 1.3 Referral Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      REFERRAL LIFECYCLE                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │Identify  │───▶│Request   │───▶│Capture   │───▶│Nurture    │        │
│  │Opportunity│    │Referral  │    │Referral  │    │Lead       │        │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘        │
│                                                          │             │
│                                                          ▼             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │Thank     │◀───│Convert   │◀───│Introduce  │◀───│Qualify   │        │
│  │Client    │    │to Client │    │Prospect  │    │Prospect  │        │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Referral Triggers

### 2.1 Proactive Referral Signals

| Signal | Indicator | Action |
|--------|-----------|--------|
| Positive feedback | "This is great" | Ask "Who else?" |
| Success milestone | Goal achieved | Celebrate, ask |
| Business growth | Client expands | Ask about peers |
| Industry event | Client attends | Offer to co-attend |
| Referral intent | "I know someone..." | Capture immediately |
| Advocacy | Client promotes us | Thank, nurture |

### 2.2 Reactive Referral Moments

| Moment | Best Ask |
|--------|----------|
| After first success | "Who else faces this?" |
| Renewal signed | "Who should we help next?" |
| Expansion closed | "What other teams could benefit?" |
| Positive meeting | "I appreciate the intro" |
| Industry news | "This reminds me of your situation" |
| Quarterly review | "Who else should we talk to?" |

---

## 3. Referral Process

### 3.1 Step 1: Identify Opportunity

**Activities:**
- Monitor for referral signals
- Ask discovery questions in calls
- Review meeting notes for mentions
- Track social media mentions
- Watch for industry events

**Questions to Ask:**
- "Who else on your team should be involved?"
- "Who else faces similar challenges?"
- "Who in your network might benefit?"
- "Are there other departments with similar needs?"

### 3.2 Step 2: Request Referral

**When to Ask:**
- After delivering value
- When client is happy
- When conversation is positive
- When client brings up industry
- At natural conversation pause

**How to Ask:**
```
[Natural moment] → [Compliment] → [Ask]

"Based on what you've told me, I think we could help 
[company type] as well. Do you know anyone who might 
be facing similar challenges?"
```

### 3.3 Step 3: Capture Referral

**Information to Capture:**
- Prospect name
- Company name
- Contact info (if available)
- Challenge/problem
- Relationship to referrer
- Referrer's permission level

**Referral Capture Form:**
```json
{
  "referral_id": "string",
  "referrer_id": "string",
  "referrer_name": "string",
  "prospect_name": "string",
  "prospect_company": "string",
  "prospect_email": "string | null",
  "prospect_phone": "string | null",
  "challenge": "string",
  "relationship": "string",
  "permission_level": "warm_intro | name_only | permission_pending",
  "capture_date": "date",
  "notes": "string"
}
```

### 3.4 Step 4: Thank the Client

**Thank You Options:**

| Referral Type | Thank You |
|---------------|-----------|
| Warm introduction | Personal thank you + lunch/coffee |
| Direct referral | Gift + personal thank you |
| Named lead | Credit + thank you |
| Public mention | Public thank you + small gift |

**Thank You Template:**
```
Subject: Thank You!

Dear <name>,

Thank you for connecting me with <prospect>. Your confidence 
in our work means a great deal.

I'll make sure to share how things go, and I'll be sure to 
thank you properly when we work together.

Would you be open to a call next week to catch up?

Best regards,
<cs_name>
```

### 3.5 Step 5: Nurture and Convert

**Activities:**
- Qualify the referral
- Schedule introduction call
- Deliver value to new prospect
- Keep referrer updated (with permission)
- Close and credit

---

## 4. Referral Tracking

### 4.1 Tracking Fields

```json
{
  "referral_id": "string",
  "referrer_id": "string",
  "referrer_name": "string",
  "referrer_company": "string",
  "prospect_name": "string",
  "prospect_company": "string",
  "prospect_email": "string | null",
  "challenge": "string",
  "permission_level": "warm_intro | name_only | permission_pending",
  "status": "captured | contacted | qualified | opportunity | won | lost",
  "captured_date": "date",
  "contacted_date": "date | null",
  "outcome_date": "date | null",
  "deal_value": "number | null",
  "referrer_reward": "string | null",
  "notes": "string"
}
```

### 4.2 Referral Pipeline

```
Referral Pipeline:
  captured → contacted → qualified → opportunity → won / lost
```

---

## 5. Referral Program

### 5.1 Referral Incentives

| Referral Type | Incentive |
|---------------|-----------|
| Warm introduction → Won | 10% credit or gift |
| Named lead → Won | 5% credit |
| Public mention → Inbound | Thank you + feature |
| Multiple referrals | Premium reward |

### 5.2 Program Rules

**Eligible:**
- ✅ Current clients in good standing
- ✅ Completed at least one workflow
- ✅ Health score 70+
- ✅ Referred decision-maker

**Not Eligible:**
- ❌ Clients with outstanding issues
- ❌ Clients at risk
- ❌ Referral to competitor
- ❌ Self-referral

---

## 6. Referral Templates

### 6.1 Referral Request Email

```
Subject: Quick Question

Hi <name>,

I've really enjoyed working with you on <project/workflow>. 
The results you're seeing are exactly what we aim for.

Quick question: Who else in your network might benefit from 
seeing similar results?

I know you have high standards for who you recommend, so 
I trust your judgment completely.

No pressure — just wanted to put it out there.

Thanks!
<cs_name>
```

### 6.2 Warm Introduction Request

```
Subject: Introduction Request — <prospect_name>

Hi <referrer_name>,

Thank you for thinking of us for <prospect_name>. I'd love 
to connect with them.

Would you be comfortable sending an intro email like this?

---
[Copy of intro email template]
---

Or, if you'd prefer, I can reach out directly mentioning 
your name with your permission.

Let me know what works best!

Best,
<cs_name>
```

### 6.3 Introduction Email Template

```
Subject: Quick Intro — <your name> suggested I reach out

Hi <prospect_name>,

<referrer_name> suggested I reach out. They mentioned you 
might be facing challenges with <problem>.

I help companies like yours <outcome>.

Would you have 15 minutes this week to see if there's a fit?

Best,
<cs_name>
```

---

## 7. Referral Metrics

### 7.1 Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Referral rate | ≥30% of healthy clients | — |
| Referrals per client | 0.5 per year | — |
| Referral conversion rate | ≥25% | — |
| Referral win rate | ≥50% | — |
| Referral revenue | ≥20% of total | — |

### 7.2 Health Score by Referral Status

| Referral Status | Average Health Score |
|----------------|---------------------|
| Made referral → Won | 90+ |
| Made referral → Pending | 85+ |
| Referral captured | 80+ |
| Referral requested | 75+ |
| Identified opportunity | 70+ |

---

## 8. Referral Best Practices

### 8.1 Do's

- ✅ Ask at the right moment
- ✅ Make it easy for the client
- ✅ Always thank the referrer
- ✅ Keep referrer updated
- ✅ Credit the referrer in deal
- ✅ Track all referrals
- ✅ Follow up on referrals quickly

### 8.2 Don'ts

- ❌ Ask too often
- ❌ Push referrals the client isn't comfortable with
- ❌ Spam referrals
- ❌ Forget to thank
- ❌ Ignore referral quality
- ❌ Leave referrals unfollowed

---

**Last Updated:** 2026-06-03  
**Next Review:** 2026-07-03
