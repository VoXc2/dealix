# A/B Test Policy — Arabic
## سياسة الاختبار A/B

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Policy Statement

Dealix conducts experiments to improve GTM, commercial, and operational outcomes while maintaining ethical standards, compliance, and user trust.

---

## 2. Scope

This policy applies to all experiments involving:
- Outreach content (emails, WhatsApp messages)
- Commercial offers and pricing
- User interfaces and experiences
- Targeting and segmentation
- Process and workflow changes

---

## 3. Prohibited Experiments

### 3.1 Content Restrictions

❌ **NEVER test:**
- Guaranteed claims or promises
- Fake urgency or artificial scarcity
- Misleading subject lines
- Discriminatory content
- False testimonials
- deceptive pricing

### 3.2 Examples of Prohibited Tests

| Prohibited | Why |
|------------|-----|
| "Guaranteed results" vs "Proven results" | Can't guarantee |
| "Only 2 spots left!" vs "Limited availability" | Fake scarcity |
| "You're pre-approved" vs "Apply now" | Deceptive |
| Lower pricing without disclosure | Bait and switch |

### 3.3 Allowed Subject Line Tests

| Allowed | Example |
|---------|---------|
| Different value props | "Reduce costs" vs "Increase revenue" |
| Different questions | "Want to learn more?" vs "Ready to start?" |
| Different lengths | Short vs long subject |
| Different personalization | Name vs Company vs Generic |
| Different urgency (genuine) | "This quarter" vs "This month" |

---

## 4. Required Approvals

### 4.1 Approval Matrix

| Experiment Type | Founder | Legal | Compliance | Ethics |
|-----------------|---------|-------|------------|--------|
| Subject line | Required | Review | Review | Required |
| CTA copy | Required | - | Review | Required |
| Pricing | Required | Required | Required | Required |
| Targeting | Required | Review | Required | Required |
| Process changes | Required | - | - | Required |

### 4.2 Approval Process

```
1. Submit experiment proposal
2. Compliance review (48 hours)
3. Legal review for pricing (72 hours)
4. Founder approval
5. Ethics check
6. Launch
```

---

## 5. Statistical Requirements

### 5.1 Minimum Standards

| Requirement | Value |
|-------------|-------|
| Minimum sample size | 100 per variant |
| Statistical significance | 95% (p < 0.05) |
| Minimum runtime | 7 days |
| Minimum detectable effect | 10% relative |

### 5.2 Sample Size Calculator

```python
import math

def calculate_sample_size(baseline_rate: float, mde: float, alpha: float = 0.05, power: float = 0.8):
    """Calculate required sample size per variant."""
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    
    # pooled proportion
    p_pooled = (p1 + p2) / 2
    
    # Z-scores
    z_alpha = 1.96  # 95% confidence
    z_beta = 0.84   # 80% power
    
    # Sample size formula
    n = (
        (z_alpha * math.sqrt(2 * p_pooled * (1 - p_pooled)) +
         z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    ) / (p2 - p1) ** 2
    
    return math.ceil(n)

# Example
baseline = 0.05  # 5% reply rate
mde = 0.20      # 20% relative improvement
sample_size = calculate_sample_size(baseline, mde)
print(f"Required per variant: {sample_size}")
# Output: 6,280 per variant
```

---

## 6. Compliance Checks

### 6.1 Pre-Launch Checklist

- [ ] Hypothesis documented
- [ ] Variants reviewed for compliance
- [ ] Minimum sample size calculated
- [ ] Statistical test selected
- [ ] Tracking implemented
- [ ] Rollback plan prepared
- [ ] All approvals obtained

### 6.2 Compliance Review Criteria

| Criterion | Question |
|-----------|----------|
| Truthfulness | Are all claims accurate and verifiable? |
| Fairness | Could this harm any group? |
| Transparency | Would users know they're in an experiment? |
| Privacy | Is PII handled correctly? |
| Consent | Is consent obtained where required? |

---

## 7. Results Documentation

### 7.1 Required Documentation

For every experiment, document:
- Hypothesis
- Methodology
- Results (all metrics)
- Statistical analysis
- Decision and rationale
- Learnings

### 7.2 Results Template

```markdown
# Experiment Results

## Metadata
- ID: EXP_XXX
- Name: [name]
- Date: [completion date]
- Owner: [owner]

## Hypothesis
[Original hypothesis]

## Methodology
[How experiment was run]

## Results
| Metric | Control | Treatment | Diff | P-value |
|--------|---------|-----------|------|---------|
| [metric] | [value] | [value] | [%] | [p] |

## Statistical Analysis
- Sample size: [n] / [n]
- Test used: [test]
- P-value: [value]
- Significance: [Yes/No]

## Decision
[IMPLEMENT / DISCARD / REPEAT]

## Learnings
[Key takeaways]
```

---

## 8. Violations

### 8.1 Violation Types

| Severity | Example | Consequence |
|----------|---------|-------------|
| Critical | Testing deceptive claims | Immediate stop, review |
| High | Testing without approval | Project suspension |
| Medium | Missing documentation | Remediation plan |
| Low | Minor policy deviation | Warning |

### 8.2 Reporting Violations

Violations should be reported to:
- Head of Compliance
- Founder
- Ethics advisor (if applicable)

---

## 9. Training

All team members involved in experiments must complete:
- [ ] Compliance training (annual)
- [ ] Statistics basics training
- [ ] Ethics training (annual)
- [ ] Privacy training (annual)

---

**Next:** See `EXPERIMENT_REVIEW.md` for results reporting template.
