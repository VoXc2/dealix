# Dealix Privacy-Aware Analytics — Arabic
## تحليلات ديلوكس الواعية بالخصوصية

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

This document defines privacy practices for all Dealix analytics to ensure PDPL compliance while maintaining actionable insights.

---

## 2. Privacy Principles

### 2.1 Data Minimization
- Collect only what is necessary
- Aggregate before reporting
- Delete raw data when not needed

### 2.2 Purpose Limitation
- Data used only for stated purposes
- No secondary use without consent
- Analytics separate from operations

### 2.3 Transparency
- Clear data handling policies
- Documented retention periods
- User-accessible data where required

### 2.4 Security
- Encryption at rest and in transit
- Access controls and audit logging
- Regular security reviews

---

## 3. PII Classification

### 3.1 High-Risk PII (Must Redact)

| Data Type | Examples | Risk Level | Handling |
|-----------|----------|------------|----------|
| Email Address | user@company.com | High | Hash + domain only |
| Phone Number | +966501234567 | High | Mask last 4 digits |
| Full Name | Ahmed Al-Rashid | High | Use company name |
| National ID | IQAMA numbers | Critical | Never store |
| Financial | Bank account | Critical | Never store |
| Health Data | Any | Critical | Never store |

### 3.2 Medium-Risk PII (Aggregate)

| Data Type | Examples | Risk Level | Handling |
|-----------|----------|------------|----------|
| Company Name | ACME Corp | Medium | OK if aggregated |
| Job Title | CEO, VP Sales | Medium | OK if aggregated |
| Company Size | 50-100 employees | Medium | OK |
| Location | Riyadh, Jeddah | Medium | OK if regional |

### 3.3 Low-Risk Data (OK)

| Data Type | Examples | Risk Level | Handling |
|-----------|----------|------------|----------|
| Sector | Technology, Healthcare | Low | Always OK |
| Event Type | message.sent | Low | Always OK |
| Metric Values | reply_rate | Low | Always OK |
| Timestamps | occurred_at | Low | Always OK |

---

## 4. Redaction Rules

### 4.1 Event Redaction

```python
def redact_event(event: dict) -> dict:
    """Redact PII from event payload."""
    redacted = event.copy()
    
    # Email: Hash and keep domain only
    if 'email' in redacted.get('payload', {}):
        email = redacted['payload']['email']
        redacted['payload']['email'] = hash_email(email)
        # Add domain-only for reporting
        redacted['payload']['email_domain'] = email.split('@')[1] if '@' in email else None
    
    # Phone: Mask all but last 4
    if 'phone' in redacted.get('payload', {}):
        phone = redacted['payload']['phone']
        redacted['payload']['phone'] = mask_phone(phone)
    
    # Name: Redact personal names
    if 'name' in redacted.get('payload', {}):
        redacted['payload']['name'] = 'REDACTED'
    
    # Company name: Keep but never show individual
    # Use company_id instead in reports
    
    return redacted

def hash_email(email: str) -> str:
    """Hash email for uniqueness without exposure."""
    return f"HASH_{hashlib.sha256(email.lower().encode()).hexdigest()[:16]}"

def mask_phone(phone: str) -> str:
    """Mask phone keeping last 4 digits."""
    if len(phone) <= 4:
        return "****"
    return "*" * (len(phone) - 4) + phone[-4:]
```

### 4.2 Report Redaction

| Report Type | Allowed | Redacted |
|-------------|---------|----------|
| Founder Daily | Metrics, trends, decisions | All PII |
| Weekly Review | Aggregated by sector | All PII |
| Pipeline Report | Deal values, stages | Contact details |
| Funnel Analysis | Conversion rates | Individual records |

---

## 5. Aggregation Requirements

### 5.1 Minimum Cohort Size

| Aggregation Level | Minimum Count | Rationale |
|-------------------|---------------|-----------|
| Sector | 3 | Prevent individual identification |
| Channel | 3 | Prevent individual identification |
| Deal Stage | 3 | Prevent individual identification |
| Time Period | 5 events | Prevent timing analysis |

### 5.2 Suppression Rules

If any aggregation results in < minimum count:
1. Suppress the value entirely
2. Mark as "Insufficient data"
3. Log for privacy review

---

## 6. Data Retention

### 6.1 Retention Schedule

| Data Type | Retention | Archive | Delete |
|-----------|-----------|---------|--------|
| Raw Events | 90 days | No | Yes |
| Aggregated Metrics | Indefinite | N/A | No |
| Decision Logs | 2 years | Yes | Yes |
| Audit Logs | 5 years | Yes | Yes |
| DSR Records | Per request | Per request | Per request |

### 6.2 Deletion Procedures

```python
# Event deletion after 90 days
def cleanup_old_events():
    cutoff = datetime.utcnow() - timedelta(days=90)
    deleted = event_store.delete_before(cutoff)
    audit_log.log_deletion("events", deleted, cutoff)
    return deleted

# DSR deletion on request
def process_dsr_deletion(dsr_request: DSRRequest):
    # Find all PII for subject
    pii_records = find_pii_by_subject(dsr_request.subject_id)
    # Delete from all systems
    for system in connected_systems:
        system.delete_pii(dsr_request.subject_id)
    # Log completion
    compliance.dsr_completed(dsr_request.id)
    return True
```

---

## 7. Access Controls

### 7.1 Role-Based Access

| Role | Access Level | Reports | Raw Data |
|------|--------------|---------|----------|
| Founder | Full | All | Redacted |
| Head of Data | Full | All | Redacted |
| Analytics | Metrics only | Standard | No |
| Commercial | Pipeline only | Commercial | Redacted |
| Delivery | Delivery only | Delivery | Redacted |
| External | Aggregated | Public | No |

### 7.2 Audit Logging

All analytics access is logged:

```python
def log_analytics_access(
    user_id: str,
    action: str,
    data_accessed: list[str],
    timestamp: datetime
):
    audit_log.append({
        "user_id": user_id,
        "action": action,
        "data_types": data_accessed,
        "timestamp": timestamp.isoformat(),
        "ip_address": get_client_ip(),
        "session_id": get_session_id()
    })
```

---

## 8. PDPL Compliance

### 8.1 Consent Requirements

| Data Type | Consent Required | Consent Type |
|-----------|-----------------|--------------|
| Outreach | Yes | Opt-in |
| Analytics | No | Legitimate interest |
| Third-party sharing | Yes | Explicit |
| Marketing | Yes | Explicit |

### 8.2 Data Subject Rights

| Right | Implementation |
|-------|----------------|
| Access | Export endpoint: `/api/v1/analytics/export` |
| Correction | Correction request: `/api/v1/dsr/correct` |
| Deletion | Deletion request: `/api/v1/dsr/delete` |
| Portability | JSON export format |

### 8.3 Breach Response

1. Detect breach within 24 hours
2. Assess affected data within 48 hours
3. Notify authority within 72 hours (if required)
4. Notify affected individuals (if required)
5. Document and remediate

---

## 9. Privacy Review Checklist

For each new report or dashboard:

- [ ] Does it contain PII?
- [ ] Is PII properly redacted?
- [ ] Are aggregations >= minimum cohort size?
- [ ] Is access logged?
- [ ] Is retention policy followed?
- [ ] Has privacy team reviewed?

---

## 10. Privacy Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| PII incidents | 0 | Monthly |
| DSR response time | < 30 days | Per request |
| Redaction coverage | 100% | Weekly |
| Consent compliance | 100% | Monthly |
| Privacy training | 100% of staff | Annually |

---

**Next:** See `DECISION_INTELLIGENCE_AR.md` for decision framework.
