# Deterministic Fallback Policy (Dealix)

## When
- AI_MODE_DEMO=true (default)
- Provider key not configured
- Provider call errors

## What
- Router returns `AIResult(provider="deterministic", model="template", prompt_version="v1.0.0")`
- Output is a templated string with the same safety flags

## Why
- Core business scripts (lead scoring, drafts, proposals) must work without external dependencies
- CI must pass without secrets
- Operator can upgrade to production mode when ready
