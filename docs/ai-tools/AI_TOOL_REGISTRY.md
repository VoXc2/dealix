# AI Tool Registry

## Purpose
Track every AI tool, model, agent, automation, and external service used by Dealix.

## Registry table

| Tool | Category | Use case | Data used | Owner | Risk | Review cadence | Status |
|---|---|---|---|---|---|---|---|
| OpenAI SDK | LLM provider | Generation and reasoning workflows | Prompt and approved context | AI/Product | Medium | Monthly | Active |
| Anthropic SDK | LLM provider | Generation and reasoning workflows | Prompt and approved context | AI/Product | Medium | Monthly | Active |
| Google Gemini SDK | LLM provider | Generation and reasoning workflows | Prompt and approved context | AI/Product | Medium | Monthly | Active |
| Langfuse | Observability | Trace and evaluate LLM calls | Prompts, metadata, outputs | Engineering | Medium | Monthly | Active |
| HubSpot API | CRM integration | CRM records and GTM workflow | Account and CRM data | RevOps | Medium | Monthly | Active |
| Resend | Email infrastructure | Transactional or approved email workflows | Email metadata and content | Engineering | Medium | Monthly | Active |

## Add a new tool

Before adding a new AI or automation tool, create an issue using the AI risk review template and document:

- Business use case
- Data used
- Owner
- Output type
- Human review requirement
- Logging and retention
- Security review
- Fallback path
- Cost estimate
- Vendor risk

## Approval levels

| Level | Meaning | Required review |
|---|---|---|
| Low | Internal helper with no sensitive data | Owner review |
| Medium | Uses business/customer context or affects workflows | Product and security review |
| High | Customer-facing, regulated, or high-impact output | Founder, security, and legal review |
| Critical | Can cause material customer, legal, or security harm | Do not ship without formal approval |

## Monthly review

Each month, review:

1. Unused tools to remove.
2. Tools with unclear owners.
3. Tools sending sensitive data.
4. Tools with rising cost.
5. Tools with poor output quality.
6. Tools lacking fallback.
7. Vendor changes or policy changes.

## Non-negotiable rules

- No tool without owner.
- No customer-facing AI output without human review unless explicitly approved.
- No sensitive data sent to a tool without documented purpose.
- No new provider without cost and data review.
- No silent automation for high-impact actions.
