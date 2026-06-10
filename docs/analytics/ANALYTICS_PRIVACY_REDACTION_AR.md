# Analytics Privacy Redaction — Arabic
## إعادة تحديد الهوية للتحليلات

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

This document defines privacy redaction rules for all analytics data to ensure PDPL compliance.

---

## 2. Redaction Levels

### 2.1 Level 1: Hash Only
For internal use only. Email addresses are hashed.

```json
{
  "email": "HASH_abc123def456"
}
```

### 2.2 Level 2: Domain Only
For aggregated reports. Keep domain, remove local part.

```json
{
  "email_domain": "company.com"
}
```

### 2.3 Level 3: Masked
For exceptions. Keep partial, mask most.

```json
{
  "phone": "****4567"
}
```

### 2.4 Level 4: Redacted
For sensitive data. Remove entirely.

```json
{
  "name": "REDACTED",
  "national_id": "[REDACTED]"
}
```

---

## 3. Field Redaction Rules

### 3.1 PII Fields

| Field | Redaction Level | Method |
|-------|-----------------|--------|
| email | L2 | Domain only in reports, hash in events |
| phone | L3 | Mask last 4 digits |
| name | L4 | Use company name instead |
| address | L4 | Remove entirely |
| national_id | L4 | Never store |
| bank_account | L4 | Never store |
| date_of_birth | L4 | Remove entirely |

### 3.2 Quasi-Identifier Fields

| Field | Redaction Level | Aggregation Rule |
|-------|-----------------|------------------|
| company_name | L1 | OK if count >= 3 |
| job_title | L1 | OK if count >= 3 |
| company_size | L1 | OK always |
| location | L1 | OK if regional (not specific) |
| sector | L1 | OK always |
| revenue | L1 | OK if count >= 3 |

### 3.3 Non-PII Fields

| Field | Redaction Level | Notes |
|-------|-----------------|-------|
| event_type | None | Always OK |
| metric_value | None | Always OK |
| timestamp | None | Always OK |
| sector | None | Always OK |
| funnel_stage | None | Always OK |

---

## 4. Implementation

### 4.1 Email Redaction

```python
import hashlib

def redact_email(email: str, level: str = "hash") -> str:
    """Redact email based on level."""
    if not email:
        return None
    
    email = email.lower().strip()
    
    if level == "hash":
        # Full hash for internal use
        return f"HASH_{hashlib.sha256(email.encode()).hexdigest()[:16]}"
    
    elif level == "domain":
        # Domain only for reports
        if "@" in email:
            return email.split("@")[1]
        return "unknown"
    
    elif level == "none":
        return email
    
    return email

def redact_event_email(event: dict, level: str = "hash") -> dict:
    """Redact email from event payload."""
    redacted = event.copy()
    
    if "payload" in redacted and "email" in redacted["payload"]:
        redacted["payload"]["email"] = redact_email(
            redacted["payload"]["email"], 
            level
        )
        # Always add domain separately for reporting
        original = event["payload"].get("email", "")
        if "@" in original:
            redacted["payload"]["email_domain"] = original.split("@")[1]
    
    return redacted
```

### 4.2 Phone Redaction

```python
def redact_phone(phone: str) -> str:
    """Redact phone number, keeping last 4 digits."""
    if not phone:
        return None
    
    # Remove all non-digits
    digits = ''.join(c for c in phone if c.isdigit())
    
    if len(digits) <= 4:
        return "****"
    
    return "*" * (len(digits) - 4) + digits[-4:]

def redact_event_phone(event: dict) -> dict:
    """Redact phone from event payload."""
    redacted = event.copy()
    
    if "payload" in redacted and "phone" in redacted["payload"]:
        redacted["payload"]["phone"] = redact_phone(
            redacted["payload"]["phone"]
        )
    
    return redacted
```

### 4.3 Name Redaction

```python
def redact_name(name: str, company_name: str = None) -> str:
    """Redact personal name, use company name if available."""
    if company_name:
        return company_name  # Prefer company name
    return "REDACTED"  # Otherwise redact entirely

def redact_event_name(event: dict) -> dict:
    """Redact name from event payload."""
    redacted = event.copy()
    
    if "payload" in redacted:
        company = redacted["payload"].get("company_name")
        
        if "name" in redacted["payload"]:
            redacted["payload"]["name"] = redact_name(
                redacted["payload"]["name"],
                company
            )
        
        if "contact_name" in redacted["payload"]:
            redacted["payload"]["contact_name"] = redact_name(
                redacted["payload"]["contact_name"],
                company
            )
    
    return redacted
```

---

## 5. Report Redaction

### 5.1 Report Field Redaction

```python
def redact_report_field(field_name: str, value: any, context: dict) -> any:
    """Redact field based on type and context."""
    
    PII_FIELDS = ["email", "phone", "name", "address", "national_id"]
    QUASI_ID_FIELDS = ["company_name", "job_title"]
    
    if field_name in PII_FIELDS:
        if field_name == "email":
            return redact_email(value, level="domain")
        elif field_name == "phone":
            return redact_phone(value)
        else:
            return "REDACTED"
    
    elif field_name in QUASI_ID_FIELDS:
        # Apply aggregation rules
        cohort_size = context.get("cohort_size", 0)
        if cohort_size < 3:
            return "Insufficient data"
        return value
    
    return value
```

### 5.2 Aggregation Rules

```python
MINIMUM_COHORT_SIZE = 3

def check_aggregation_cohort(group_by_fields: dict, data: list) -> bool:
    """Check if aggregation has minimum cohort size."""
    return len(data) >= MINIMUM_COHORT_SIZE

def redact_aggregated_report(report: dict, group_by: list) -> dict:
    """Redact report data based on aggregation."""
    redacted = report.copy()
    
    for row in redacted.get("rows", []):
        cohort_size = row.get("count", 0)
        
        if cohort_size < MINIMUM_COHORT_SIZE:
            row["suppressed"] = True
            row["value"] = "Insufficient data"
            row["suppression_reason"] = f"Cohort size ({cohort_size}) < minimum (3)"
    
    return redacted
```

---

## 6. Audit Trail

### 6.1 Redaction Logging

```python
def log_redaction(
    event_id: str,
    field: str,
    original_value: str,
    redacted_value: str,
    redaction_level: str,
    reason: str
):
    """Log redaction for audit purposes."""
    audit_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "event_id": event_id,
        "field": field,
        "redaction_level": redaction_level,
        "reason": reason,
        # Note: Do NOT log original_value in production
        "action": "redacted"
    })
```

### 6.2 Redaction Audit Report

```markdown
# Privacy Redaction Audit — 2026-06-03

## Redaction Summary
| Level | Count | Fields |
|-------|-------|--------|
| L1 (Hash) | 1,234 | email |
| L2 (Domain) | 5,678 | email (reports) |
| L3 (Masked) | 89 | phone |
| L4 (Redacted) | 45 | name, national_id |

## Compliance Status
- ✅ No PII in daily reports
- ✅ All emails aggregated by domain
- ✅ Minimum cohort size enforced
- ✅ Redaction audit trail maintained

## Incidents
- None this period
```

---

## 7. Verification

### 7.1 Pre-Deployment Checklist

- [ ] All reports use redaction functions
- [ ] Aggregation rules enforced
- [ ] Cohort size checks in place
- [ ] Audit logging enabled
- [ ] No PII in sample data

### 7.2 Quarterly Audit

- [ ] Review redaction logs
- [ ] Check for redaction bypasses
- [ ] Update redaction rules if needed
- [ ] Verify compliance training
