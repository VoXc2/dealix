# Dealix AI Agent Security Model

## Hard Rules

- No auto-send.
- No scraping.
- No external publishing.
- No client-data export without explicit permission.
- No payment or contract action without founder approval.
- No ROI claim without baseline.

## Agent Permissions

| Agent | Can Draft | Can Read Internal Docs | Can Send | Can Scrape |
|---|---:|---:|---:|---:|
| CEO Brain | yes | yes | no | no |
| Draft Agent | yes | yes | no | no |
| Proof Agent | yes | yes | no | no |
| Risk Agent | yes | yes | no | no |
| Finance Agent | yes | yes | no | no |

## Threats

- Prompt injection.
- Excessive agency.
- Secret leakage.
- Unsafe output handling.
- Hallucinated proof.
- Unapproved outreach.

## Controls

- Approval queue.
- No external action flags.
- Human review.
- Report files.
- Git audit trail.
- Production watchdog.
