# Sales Automation Security Model (Dealix)

## Principles
- AI-assisted, Human-reviewed
- No auto-send, no scraping, no spam
- Drafts only, with review_status
- Audit log on every external action

## Threat model
| Threat | Mitigation |
|--------|-----------|
| Auto-send in code | `tests/test_no_auto_send.py` + review gate |
| PII leakage | PDPL_AWARE_DATA_BOUNDARIES.md |
| ROI claim | banned-claims checker |
| Spam | No Spam Policy + outreach queue |
| Public API key leak | `scripts/check_no_secrets.py` |
| Untracked change | git history + branch protection |

## Controls
- Branch protection on `main`
- PR review required
- CI runs `check_no_secrets` + `verify_dealix_ultimate_os`
- Every connector has a safety doc
