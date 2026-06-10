# AI Governance and Model Risk Playbook

## Objective
Make Dealix AI capabilities useful, auditable, safe, explainable, and enterprise-ready.

## Governance principle
AI can assist decisions, draft work, summarize information, and prioritize work. AI must not silently make high-impact decisions without review, traceability, and human ownership.

## AI use-case inventory

| Use case | User | Data used | Output | Risk level | Human review | Owner |
|---|---|---|---|---|---|---|
| Account scoring | Sales/GTM | Account metadata, activity, fit criteria | Priority score | Medium | Required | Product |
| Outreach drafting | Sales | Account context, approved positioning | Draft message | Medium | Required | Sales |
| Executive summary | Founder | KPI data, customer evidence | Weekly narrative | Medium | Required | Founder |
| Customer health signal | CS | Usage, outcomes, engagement | Risk flag | Medium | Required | CS |
| Research summary | GTM | Public/company research | Summary | Low/Medium | Required | GTM |

## Risk categories

| Risk | Example | Control |
|---|---|---|
| Hallucination | Incorrect claim about customer/company | Source citation and review |
| Privacy leakage | Sensitive data in prompt/output | Data boundary and redaction |
| Bias or unfair scoring | Unsupported prioritization | Explainability and audit trail |
| Over-automation | AI sends external communication without approval | Human approval workflow |
| Prompt injection | Malicious content manipulates output | Input isolation and output validation |
| Compliance drift | Workflow violates customer policy | Policy review and approvals |

## Required controls

1. Use-case registry for every AI workflow.
2. Data classification before AI use.
3. Human approval for customer-facing outputs.
4. Source attribution for factual outputs.
5. Prompt and output logging where appropriate.
6. Red-team tests for critical workflows.
7. Model/version tracking.
8. Clear fallback when AI is unavailable or low-confidence.
9. Customer-visible explanation for consequential outputs.
10. Periodic quality review.

## AI output quality checklist

Before using an AI output externally, verify:

- Does it cite or reference the evidence used?
- Is it free from unsupported claims?
- Is the tone aligned with Dealix positioning?
- Does it expose sensitive information?
- Does a human owner approve it?
- Is the output stored or logged appropriately?
- Can the customer understand why this recommendation was made?

## Human-in-the-loop matrix

| Output type | Review required? | Reviewer |
|---|---|---|
| Sales email draft | Yes | Sales owner |
| Customer-facing proposal | Yes | Founder or Sales Lead |
| Account priority score | Yes for top-tier actions | GTM Lead |
| Health risk flag | Yes | CS owner |
| Internal KPI summary | Yes | Founder/Ops |
| Legal/security answer | Yes | Legal/Security owner |

## Model evaluation scorecard

| Dimension | Target | Test method |
|---|---|---|
| Accuracy | No unsupported critical claims | Sample review |
| Faithfulness | Output grounded in provided data | Evidence comparison |
| Usefulness | Helps user complete workflow faster | User feedback |
| Safety | No data leakage or unsafe action | Red-team tests |
| Consistency | Same input class produces stable output | Regression tests |
| Explainability | Clear reason for recommendation | Output rubric |

## Incident handling

AI incident examples:

- Incorrect customer claim used externally.
- Sensitive data included in output.
- Scoring produces unfair or unsupported results.
- Automated workflow runs without approval.
- Customer challenges explanation or accuracy.

Incident response:

1. Stop affected workflow.
2. Preserve prompt, output, user, timestamp, model/version.
3. Identify customers or records affected.
4. Correct external communication if needed.
5. Patch prompt, data boundary, or workflow.
6. Add regression test.
7. Document postmortem.

## Required artifacts

- AI use-case registry
- Data classification policy
- Prompt library
- Evaluation rubric
- AI incident register
- Human review SOP
- Model/version log
- Red-team test set
