# Technical FAQ

## What verification scripts exist?

See `scripts/verify_*.py` — `verify_company_ready.py` aggregates many gates.

## Where is “no source no answer” enforced?

Knowledge / Company Brain boundary — see `auto_client_acquisition/knowledge_os/` and tests `test_knowledge_os_policy.py`.

## How do I run tests?

`APP_ENV=test pytest` (subset recommended in `AGENTS.md`).
