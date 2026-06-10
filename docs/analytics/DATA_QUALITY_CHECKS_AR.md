# Data Quality Checks — Arabic
## فحوصات جودة البيانات

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

This document defines automated data quality checks and their enforcement.

---

## 2. Check Types

### 2.1 Pre-Insert Checks

Events must pass these checks before entering the system:

| Check | Description | Action on Failure |
|-------|-------------|-------------------|
| required_fields | All required fields present | REJECT |
| format_validation | Field formats correct | REJECT |
| sector_valid | Sector in allowed list | REJECT |
| offer_valid | Offer ID in allowed list | WARN + REJECT |
| funnel_stage_valid | Stage in allowed list | REJECT |
| evidence_level_valid | Level L0-L5 | REJECT |
| timestamp_valid | Not future, not > 30 days old | REJECT |
| no_duplicate | Event ID not already exists | REJECT |
| not_suppressed | Contact not on suppression list | REJECT |

### 2.2 Post-Insert Checks

Run daily on all events:

| Check | Description | Alert Threshold |
|-------|-------------|-----------------|
| missing_sector | Events without sector | > 5% |
| missing_offer | Deal events without offer | > 2% |
| missing_funnel_stage | Events without stage | > 1% |
| missing_evidence_level | Events without evidence | > 0% |
| duplicate_prospects | Duplicate companies | > 1% |
| inconsistent_status | Contradictory status | > 0 |
| future_timestamps | Events with future dates | > 0 |
| old_events | Events > 7 days unprocessed | > 0 |

---

## 3. Check Implementation

### 3.1 Pre-Insert Validation

```python
from typing import Optional
from datetime import datetime, timedelta

VALID_SECTORS = [
    "technology", "healthcare", "finance", "retail",
    "manufacturing", "education", "government", "real_estate",
    "logistics", "hospitality", "construction", "energy"
]

VALID_OFFERS = [
    "offer_diagnostic", "offer_pilot", "offer_proof",
    "offer_retainer", "offer_training", "offer_consulting"
]

VALID_FUNNEL_STAGES = [
    "signal_detected", "researched", "qualified", "drafted",
    "approved_for_outreach", "contacted", "replied", "positive_reply",
    "discovery_scheduled", "discovery_completed", "proposal_needed",
    "proposal_sent", "negotiation", "payment_handoff", "won",
    "delivery_handoff", "active_delivery", "renewal_candidate", "renewed"
]

VALID_EVIDENCE_LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]

def validate_event(event: dict) -> tuple[bool, list[str]]:
    """Validate event before insertion."""
    errors = []
    
    # Required fields
    required = ["event_id", "event_type", "customer_id", "occurred_at", "funnel_stage"]
    for field in required:
        if field not in event or event[field] is None:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Sector validation
    if "sector" in event and event["sector"] not in VALID_SECTORS:
        errors.append(f"Invalid sector: {event['sector']}")
    
    # Offer validation (warning for deal events)
    if "deal" in event.get("event_type", "") or event.get("subject_type") == "deal":
        if "offer_id" not in event:
            errors.append("Missing offer_id for deal event")
        elif event.get("offer_id") not in VALID_OFFERS:
            errors.append(f"Invalid offer_id: {event['offer_id']}")
    
    # Funnel stage validation
    if event.get("funnel_stage") not in VALID_FUNNEL_STAGES:
        errors.append(f"Invalid funnel_stage: {event.get('funnel_stage')}")
    
    # Evidence level validation
    if "evidence_level" in event and event["evidence_level"] not in VALID_EVIDENCE_LEVELS:
        errors.append(f"Invalid evidence_level: {event['evidence_level']}")
    
    # Timestamp validation
    try:
        occurred_at = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
        if occurred_at > datetime.now(occurred_at.tzinfo):
            errors.append("Future timestamp not allowed")
        if occurred_at < datetime.now(occurred_at.tzinfo) - timedelta(days=30):
            errors.append("Event too old (> 30 days)")
    except (ValueError, TypeError):
        errors.append("Invalid timestamp format")
    
    return len(errors) == 0, errors
```

### 3.2 Deduplication Check

```python
def check_duplicate(event: dict, existing_ids: set) -> bool:
    """Check if event_id already exists."""
    return event.get("event_id") in existing_ids

def check_duplicate_prospect(event: dict, prospect_tracker: dict) -> bool:
    """Check for duplicate prospect (same email_domain + company_name)."""
    email_domain = event.get("payload", {}).get("email_domain")
    company_name = event.get("payload", {}).get("company_name")
    
    if email_domain and company_name:
        key = f"{email_domain}_{company_name}"
        if key in prospect_tracker:
            return True  # Duplicate found
        prospect_tracker[key] = event.get("event_id")
    return False
```

### 3.3 Suppression Check

```python
def check_suppression(event: dict, suppression_list: set) -> bool:
    """Check if contact is on suppression list."""
    contact_id = event.get("subject_id")
    if event.get("subject_type") == "contact" and contact_id:
        return contact_id in suppression_list
    return False
```

---

## 4. Quality Metrics

### 4.1 Daily Quality Score

```python
def calculate_quality_score(check_results: dict) -> float:
    """Calculate overall data quality score."""
    weights = {
        "completeness": 0.30,
        "accuracy": 0.25,
        "consistency": 0.20,
        "timeliness": 0.15,
        "uniqueness": 0.10
    }
    
    scores = {
        "completeness": 100 - (check_results.get("missing_sector_pct", 0) * 5),
        "accuracy": 100 - (check_results.get("format_errors", 0) * 10),
        "consistency": 100 - (check_results.get("inconsistencies", 0) * 20),
        "timeliness": 100 if check_results.get("future_timestamps", 0) == 0 else 0,
        "uniqueness": 100 - (check_results.get("duplicates", 0) * 5)
    }
    
    total_score = sum(scores[k] * weights[k] for k in weights)
    return max(0, min(100, total_score))
```

### 4.2 Quality Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 95-100 | Excellent | Monitor |
| 85-94 | Good | Review weekly |
| 70-84 | Fair | Review daily |
| < 70 | Poor | Immediate action |

---

## 5. Alert Configuration

### 5.1 Alert Rules

```yaml
alerts:
  critical:
    - name: future_timestamps
      condition: count > 0
      severity: critical
      action: page_founder
      channels: [slack, sms]
    
    - name: duplicate_event_id
      condition: count > 0
      severity: critical
      action: block_insert
      channels: [slack]
    
    - name: suppressed_contact_used
      condition: count > 0
      severity: critical
      action: block_insert + alert_compliance
      channels: [slack, email]
  
  high:
    - name: missing_sector_pct
      condition: pct > 5
      severity: high
      action: alert_data_team
      channels: [slack]
    
    - name: quality_score
      condition: score < 85
      severity: high
      action: alert_head_of_data
      channels: [slack, email]
  
  medium:
    - name: missing_offer_pct
      condition: pct > 2
      severity: medium
      action: alert_commercial_team
      channels: [slack]
```

---

## 6. Reporting

### 6.1 Daily Quality Report

```markdown
# Data Quality Report — 2026-06-03

## Overall Score: 97/100 (Excellent)

## Completeness
| Metric | Value | Status |
|--------|-------|--------|
| Events with sector | 98.9% | ✅ |
| Events with funnel stage | 100% | ✅ |
| Events with evidence level | 100% | ✅ |
| Deal events with offer | 98.5% | ⚠️ |

## Accuracy
| Metric | Value | Status |
|--------|-------|--------|
| Format validation errors | 0 | ✅ |
| Business rule violations | 2 | ✅ |
| Future timestamps | 0 | ✅ |

## Consistency
| Metric | Value | Status |
|--------|-------|--------|
| Duplicate event_ids | 0 | ✅ |
| Inconsistent status | 0 | ✅ |
| Duplicate prospects | 3 | ⚠️ |

## Alerts
- ⚠️ 3 duplicate prospects detected (action: merge scheduled)
- ⚠️ 1.5% deal events missing offer_id (action: data team notified)

## Actions Required
1. Merge 3 duplicate prospect records (Owner: Data Team, Due: Tomorrow)
2. Add offer_id validation to deal creation flow (Owner: Engineering, Due: This week)
```

---

## 7. Automation

### 7.1 Scheduled Checks

| Check | Frequency | Owner |
|-------|-----------|-------|
| Pre-insert validation | Real-time | System |
| Daily quality score | Daily 06:00 | System |
| Duplicate detection | Daily 06:30 | System |
| Quality report generation | Daily 07:00 | System |
| Quality review | Daily 08:00 | Head of Data |

### 7.2 Remediation Workflow

```python
def remediate_issue(issue: QualityIssue):
    """Automatically remediate common issues."""
    if issue.type == "duplicate_prospect":
        merge_prospects(issue.prospect_ids)
        log_remediation(issue, "merged")
    
    elif issue.type == "missing_sector":
        # For internal events, set sector to "internal"
        update_sector(issue.event_ids, "internal")
        log_remediation(issue, "sector_added")
    
    elif issue.type == "stale_event":
        archive_event(issue.event_id)
        log_remediation(issue, "archived")
```

---

**Next:** See `ANALYTICS_PRIVACY_REDACTION_AR.md` for privacy redaction details.
