# Workflow Runtime Design

Every Dealix workflow has:

## 1. Trigger

What starts it?

## 2. Input

What data/files are required?

## 3. AI Step

What does AI produce?

## 4. Governance Check

What must be checked?

## 5. Human Review

Who approves?

## 6. Output

What is delivered?

## 7. Proof Event

What evidence is logged?

## 8. Next Action

What happens after?

---

## Example: Lead Scoring Workflow

```text
Trigger: client uploads lead file
Input: CSV + ICP
AI Step: score accounts
Governance: source + PII + claims risk
Human Review: delivery owner reviews top 50
Output: ranked account list
Proof Event: accounts scored + data quality
Next Action: outreach draft or pilot
```
