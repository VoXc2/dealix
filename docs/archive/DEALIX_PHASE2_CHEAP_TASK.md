# Dealix Phase 2 Cheap Local Task

You are editing only:
- dealix-v2/dealix_os/cli.py
- dealix-v2/tests/
- scripts/
- docs/

Do not create dealix-builder-api.
Do not touch dealix-1 or dealix-1.worktrees.
Do not edit legacy folders.

Goal:
Make dealix-v2 a complete local terminal-first platform.

Required CLI commands:
- doctor
- services
- capabilities
- assess
- recommend-sprint
- governance-check
- score
- client-pack
- value
- proof-pack
- proposal
- dashboard
- monthly-review

Commands that must work without API keys:
- doctor
- services
- capabilities
- governance-check
- score
- client-pack
- value
- dashboard

Implementation rules:
- Use Python standard library only.
- Keep all generated client files inside dealix-v2/clients.
- Keep ledgers inside dealix-v2/ledgers.
- Block path traversal for client slugs.
- No Node.js.
- No npm.
- No API server.

Create:
- scripts/dealix-local.ps1
- scripts/dealix-test-local.ps1
- DEALIX_CHEAP_LOCAL_WORKFLOW.md
- DEALIX_OLLAMA_AIDER_WORKFLOW.md

Add tests in:
- dealix-v2/tests/test_cli_local.py

Validation:
Run:
py -3 -m pytest dealix-v2/tests
py -3 dealix-v2/dealix_os/cli.py doctor
py -3 dealix-v2/dealix_os/cli.py governance-check "we guarantee sales"
py -3 dealix-v2/dealix_os/cli.py score "paid B2B agency partner with monthly retainer and CRM data"

Make real edits.
Do not ask questions.
Keep the patch small and reliable.
