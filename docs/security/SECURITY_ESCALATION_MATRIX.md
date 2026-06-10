# Security Escalation Matrix
## مصفوفة التصعيد الأمنية

**Document Type:** Security Runbook
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This matrix defines how security incidents are classified, who is responsible, and what actions to take. All Dealix team members and agents must follow this escalation path.

---

## 2. Incident Severity Levels

| Level | Definition | Response Time | Examples |
|-------|------------|---------------|----------|
| P1 | Critical — Active breach or major outage | Immediate | Secret exposed, unauthorized send, data breach |
| P2 | High — Significant risk but contained | Within 1 hour | Prompt injection detected, workflow violation |
| P3 | Medium — Moderate risk, potential impact | Within 4 hours | Missing test, policy gap found |
| P4 | Low — Minor risk, informational | Within 24 hours | Documentation update needed |

---

## 3. Incident Categories

### 3.1 Secret Exposure (P1)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Secret in code pushed to repo | Revoke + Rotate + Update | Founder | Immediate notification |
| Secret in logs | Assess exposure + Rotate | Founder | Incident report |
| Secret in report | Recall + Rotate | Founder | Notify affected parties |
| Secret in WhatsApp | Revoke + Assess + Rotate | Founder | Customer notification if needed |

### 3.2 Unauthorized External Action (P1)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Unauthorized email sent | Recall + Suppress + Investigate | Founder | Customer notification if needed |
| Unauthorized WhatsApp sent | Recall + Investigate | Founder | Customer notification if needed |
| Unauthorized deploy | Rollback + Investigate | Founder | Team notification |
| Cold WhatsApp attempt | Block + Log + Investigate | Founder | Team notification |

### 3.3 Prompt Injection (P2)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Injection in website content | Log + Block + Continue | Agent | Report to security |
| Injection in email | Log + Block + Continue | Agent | Report to security |
| Injection in GitHub | Log + Block + Escalate | Agent + Founder | Security review |
| Injection in CRM/notes | Log + Block + Sanitize | Agent | Report to security |

### 3.4 Workflow/Permission Violation (P2)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Broad GitHub permissions | Audit + Reduce | Founder | Security review |
| Production deploy from PR | Rollback + Block | Founder | Team notification |
| `pull_request_target` abuse | Disable + Audit | Founder | Security review |
| `issue_comment` tool execution | Block + Audit | Founder | Security review |

### 3.5 PII Leakage (P1-P2)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| PII in reports | Recall + Redact + Investigate | Founder | Customer notification if needed |
| PII in logs | Assess + Redact + Update | Founder | Report if required |
| Unauthorized PII access | Block + Investigate | Founder | Customer notification if needed |
| PDPL violation suspected | Assess + Legal + Report | Founder + Legal | Saudi authority if required |

### 3.6 Commercial Misrepresentation (P2)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Guaranteed claim made | Retract + Correct + Review | Founder | Customer notification |
| Fake case study | Remove + Correct + Review | Founder | Public correction |
| Fake client result | Remove + Correct + Review | Founder | Public correction |

### 3.7 WhatsApp Policy Violation (P2)

| Indicator | Immediate Action | Owner | Communication |
|-----------|-----------------|-------|---------------|
| Cold WhatsApp attempted | Block + Log + Investigate | Founder | Team notification |
| No consent on file | Block + Request consent | Founder | Customer notification |
| API key shared in WhatsApp | Rotate key + Notify | Founder | Customer notification |
| Sensitive topic via WhatsApp | Retrieve + Human handoff | Founder | Team notification |

---

## 4. Escalation Path

```
┌─────────────────────────────────────────────────────────────────┐
│                     INCIDENT DETECTED                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CLASSIFY INCIDENT                            │
│  P1 / P2 / P3 / P4                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┬───────────────┬───────────────┐
              ▼               ▼               ▼               ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
        │    P1     │   │    P2     │   │    P3     │   │    P4     │
        │ CRITICAL  │   │   HIGH    │   │  MEDIUM   │   │    LOW    │
        └───────────┘   └───────────┘   └───────────┘   └───────────┘
              │               │               │               │
              ▼               ▼               ▼               ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
        │  IMMEDIATE│   │   WITHIN  │   │   WITHIN  │   │   WITHIN  │
        │  ACTION   │   │   1 HOUR  │   │   4 HOURS │   │   24 HRS  │
        └───────────┘   └───────────┘   └───────────┘   └───────────┘
              │               │               │               │
              ▼               ▼               ▼               ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
        │  FOUNDER  │   │  FOUNDER │   │  AGENT #5 │   │  AGENT #5 │
        │ NOTIFY    │   │ NOTIFY    │   │ + FOUNDER │   │ MONITOR   │
        └───────────┘   └───────────┘   └───────────┘   └───────────┘
              │               │               │               │
              ▼               ▼               ▼               ▼
        ┌─────────────────────────────────────────────────────────┐
        │                    INCIDENT REPORT                        │
        │ Timeline | Impact | Actions | Prevention | Sign-off     │
        └─────────────────────────────────────────────────────────┘
```

---

## 5. Response Protocols

### 5.1 P1 Response (Immediate)

1. STOP the action immediately
2. NOTIFY founder (phone/message)
3. ASSESS scope of damage
4. TAKE immediate containment (revoke, rollback, recall)
5. LOG all actions with timestamps
6. COMMUNICATE to affected parties within 24 hours
7. COMPLETE incident report within 72 hours
8. UPDATE policies to prevent recurrence

### 5.2 P2 Response (Within 1 hour)

1. LOG the incident
2. NOTIFY founder
3. TAKE containment action
4. INVESTIGATE root cause
5. UPDATE policies
6. COMPLETE incident report within 24 hours

### 5.3 P3 Response (Within 4 hours)

1. LOG the incident
2. NOTIFY Agent #5 (Security Red Team)
3. ASSESS if escalation needed
4. UPDATE documentation/tests
5. COMPLETE report within 48 hours

### 5.4 P4 Response (Within 24 hours)

1. LOG the incident
2. ADD to task list
3. UPDATE during next review cycle

---

## 6. Communication Templates

### 6.1 P1 Notification to Founder

```
🚨 SECURITY INCIDENT — P1 CRITICAL

Incident Type: [Secret Exposure | Unauthorized Send | Data Breach | ...]
Time Detected: [ISO8601]
Time Notified: [ISO8601]
Immediate Actions Taken: [List]
Scope of Impact: [What is affected]
Next Actions Required: [List]
Owner: [Agent name]

Please respond ASAP with approval for containment actions.
```

### 6.2 P2 Notification to Founder

```
⚠️ SECURITY INCIDENT — P2 HIGH

Incident Type: [Prompt Injection | Policy Violation | ...]
Time Detected: [ISO8601]
Actions Taken: [List]
Investigation Status: [In progress / Complete]
Recommendation: [Continue / Escalate to P1 / Close]
Owner: [Agent name]

Please review and advise.
```

### 6.3 Customer Notification (if required)

```
Subject: Important Notice from Dealix

Dear [Customer Name],

We are writing to inform you of a security incident that may affect your data.

What happened: [Brief description]
What we are doing: [Actions taken]
What you should do: [If applicable]
How to contact us: [Contact info]

We take security seriously and apologize for any inconvenience.
```

---

## 7. Incident Report Template

```yaml
incident_report:
  incident_id: "INC-YYYYMMDD-XXX"
  title: "Brief incident title"
  
  classification:
    severity: "P1 | P2 | P3 | P4"
    category: "Secret Exposure | Unauthorized Send | Prompt Injection | ..."
    affected_systems: ["List"]
    affected_parties: ["List"]
  
  timeline:
    detected: ISO8601
    reported: ISO8601
    contained: ISO8601
    resolved: ISO8601
  
  response:
    immediate_actions: ["List"]
    containment_measures: ["List"]
    root_cause: "Description"
    
  impact:
    data_exposed: ["List or None"]
    systems_affected: ["List or None"]
    parties_notified: ["List or None"]
    financial_impact: "Estimated if applicable"
  
  lessons_learned:
    what_went_well: ["List"]
    what_needs_improvement: ["List"]
    prevention_measures: ["List"]
  
  sign_off:
    investigator: name
    reviewer: name
    date: ISO8601
```

---

## 8. Post-Incident Review

After every P1 and P2 incident, conduct a review:

1. **Timeline reconstruction** — What happened, when, who was involved
2. **Root cause analysis** — Why did it happen
3. **Response evaluation** — Was the response appropriate and timely
4. **Policy review** — Were existing policies adequate
5. **Prevention planning** — What changes prevent recurrence
6. **Policy updates** — Document changes
7. **Training** — Update team if needed

---

## 9. Contacts

| Role | Name | Contact | Availability |
|------|------|---------|--------------|
| Founder | [FOUNDER_NAME] | [PHONE/EMAIL] | 24/7 for P1 |
| Security Lead | Agent #5 | Via Mavis | Business hours + P1 |
| Legal Advisor | [LEGAL_NAME] | [EMAIL] | By appointment |
| Technical Lead | [TECH_NAME] | [EMAIL] | Business hours |

---

## 10. Related Documents

| Document | Purpose |
|----------|---------|
| `docs/SECURITY_RUNBOOK.md` | General security runbook |
| `INCIDENT_RESPONSE_RUNBOOK_AR.md` | Arabic incident response |
| `OUTBOUND_INCIDENT_RESPONSE_AR.md` | Outbound-specific incidents |
| `PRIVACY_INCIDENT_RESPONSE_AR.md` | Privacy incidents |
| `AGENT_INCIDENT_RESPONSE_AR.md` | Agent-specific incidents |

---

*Matrix maintained by Agent #5 — Security Red Team*
*Review required: After any incident or quarterly*
