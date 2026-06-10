# Dealix Data Quality Policy — Arabic
## سياسة جودة بيانات ديلوكس

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

This policy defines data quality standards, validation rules, and enforcement mechanisms for all Dealix analytics data.

---

## 2. Quality Dimensions

### 2.1 Completeness
- All required fields must be populated
- Target: 100% for critical fields, 95% for standard fields
- Missing data must have documented reason

### 2.2 Accuracy
- Data must reflect real-world state
- Validation against source systems
- Error rate threshold: < 1%

### 2.3 Consistency
- Same data same format across all systems
- Cross-field validation
- No contradictory records

### 2.4 Timeliness
- Events captured within 5 minutes of occurrence
- Metrics updated daily by 07:00
- Decision reports available by 07:30

### 2.5 Uniqueness
- No duplicate records
- Deduplication on key fields
- Merge procedures for identified duplicates

---

## 3. Required Field Standards

### 3.1 Universal Required Fields

| Field | Type | Validation | Acceptable Missing Reason |
|-------|------|------------|--------------------------|
| event_id | string | UUID format | NEVER |
| event_type | string | Must be in taxonomy | NEVER |
| customer_id | string | Must exist in CRM | NEVER |
| occurred_at | datetime | UTC, valid date | NEVER |
| sector | string | Must be valid sector | ONLY for internal-only events |
| funnel_stage | string | Must be valid stage | NEVER |
| evidence_level | string | L0-L5 | NEVER |
| actor | string | Must be valid actor | NEVER |

### 3.2 Conditional Required Fields

| Field | Required When | Validation |
|-------|----------------|------------|
| offer_id | Deal lifecycle events | Must be valid offer |
| approval_status | Outreach events | Must be valid status |
| channel | Message events | email/whatsapp |
| bounce_type | Bounce events | hard/soft |
| classification | Reply events | Valid reply type |

---

## 4. Validation Rules

### 4.1 Format Validation

```python
# Event ID format
EVENT_ID_PATTERN = r"^evt_[a-z0-9]{24}$"

# Datetime format (ISO 8601)
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Sector validation
VALID_SECTORS = [
    "technology", "healthcare", "finance", "retail",
    "manufacturing", "education", "government", "real_estate",
    "logistics", "hospitality", "construction", "energy"
]

# Offer validation
VALID_OFFERS = [
    "offer_diagnostic", "offer_pilot", "offer_proof",
    "offer_retainer", "offer_training", "offer_consulting"
]
```

### 4.2 Business Rule Validation

1. **Funnel progression**: Events can only move forward in funnel (except to nurture)
2. **Timing validation**: occurred_at cannot be in the future
3. **Causation validation**: causation_id must reference existing event
4. **Deduplication**: No duplicate event_id
5. **Suppression check**: recipient must not be on suppression list

### 4.3 Cross-Field Validation

| Rule | Condition | Action |
|------|-----------|--------|
| deal.won requires positive_reply | deal.won must have preceding positive_reply | REJECT if missing |
| meeting.held requires meeting.booked | Must have booking event | REJECT if missing |
| customer.churned requires customer.health_changed | Must have declining health | WARN if missing |
| deal.lost requires rejection reason | Must include lost_reason | REJECT if missing |

---

## 5. Data Quality Checks

### 5.1 Pre-Insert Checks

```python
def validate_event(event: dict) -> tuple[bool, list[str]]:
    """Validate event before insertion."""
    errors = []
    
    # Check required fields
    for field in REQUIRED_UNIVERSAL_FIELDS:
        if field not in event or event[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Check sector
    if 'sector' in event and event['sector'] not in VALID_SECTORS:
        errors.append(f"Invalid sector: {event['sector']}")
    
    # Check timestamp
    if event.get('occurred_at', '') > datetime.utcnow().isoformat():
        errors.append("Future timestamp not allowed")
    
    # Check for duplicates
    if event_exists(event['event_id']):
        errors.append(f"Duplicate event_id: {event['event_id']}")
    
    # Check suppression
    if event.get('subject_type') == 'contact':
        if is_suppressed(event['subject_id']):
            errors.append("Contact is on suppression list")
    
    return len(errors) == 0, errors
```

### 5.2 Daily Quality Checks

| Check | Description | Threshold |
|-------|-------------|-----------|
| missing_sector_pct | Events without sector | < 5% |
| missing_offer_pct | Deal events without offer | < 2% |
| duplicate_prospects | Duplicate company records | < 1% |
| suppressed_used | Suppressed contacts contacted | = 0 |
| missing_funnel_stage | Events without stage | < 1% |
| inconsistent_status | Contradictory status | = 0 |
| future_timestamps | Events with future dates | = 0 |
| invalid_evidence_level | Non-L0-L5 levels | = 0 |

---

## 6. Quality Scoring

### 6.1 Score Calculation

```
Data Quality Score = (
    completeness_score * 0.30 +
    accuracy_score * 0.25 +
    consistency_score * 0.20 +
    timeliness_score * 0.15 +
    uniqueness_score * 0.10
)
```

### 6.2 Score Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 95-100 | Excellent | Monitor only |
| 85-94 | Good | Review monthly |
| 70-84 | Fair | Review weekly |
| < 70 | Poor | Immediate action |

---

## 7. Quality Reporting

### 7.1 Daily Report

```
Data Quality Daily Report
Date: 2026-06-03

Completeness:
- Total events: 1,234
- Events with sector: 1,220 (98.9%)
- Events with funnel stage: 1,234 (100%)
- Events with evidence level: 1,234 (100%)

Accuracy:
- Format validation failures: 0
- Business rule violations: 2
- Future timestamp events: 0

Consistency:
- Duplicate event_ids: 0
- Inconsistent status: 0

Timeliness:
- Events processed within 5 min: 1,234 (100%)
- Metrics updated: 07:00

Uniqueness:
- Duplicate prospects: 3
- Merged records: 2

Overall Score: 97/100 (Excellent)
```

---

## 8. Enforcement

### 8.1 Blocking Rules

Events that FAIL the following checks are REJECTED:

| Check | Reason |
|-------|--------|
| Missing event_id | Cannot track |
| Missing event_type | Cannot classify |
| Missing customer_id | Cannot attribute |
| Missing occurred_at | Cannot time-order |
| Missing funnel_stage | Cannot measure conversion |
| Missing evidence_level | Cannot assess quality |
| Future timestamp | Data integrity |
| Duplicate event_id | Cannot double-count |
| Suppressed contact used | Compliance violation |

### 8.2 Warning Rules

Events that WARN but are ACCEPTED:

| Check | Warning Threshold | Action |
|-------|-------------------|--------|
| Missing sector | > 5% of batch | Alert data team |
| Missing offer_id | > 2% of deal events | Alert commercial team |
| Timing delay | > 5 min | Alert ops team |

---

## 9. Data Quality Improvement

### 9.1 Root Cause Analysis

For any quality score below 85%:

1. Identify affected events
2. Trace to source system
3. Document root cause
4. Create fix action
5. Implement preventive measure
6. Retest within 48 hours

### 9.2 Quality Goals

| Metric | Current | Q2 Target | Q3 Target |
|--------|---------|----------|-----------|
| Completeness | 95% | 98% | 100% |
| Accuracy | 99% | 99.5% | 100% |
| Timeliness | 98% | 99% | 100% |
| Overall Score | 92 | 96 | 99 |

---

## 10. Compliance

This policy complies with:
- PDPL (Saudi Personal Data Protection Law)
- GDPR (where applicable)
- SOC 2 requirements
- Industry best practices

---

**Next:** See `DATA_QUALITY_CHECKS_AR.md` for implementation details.
