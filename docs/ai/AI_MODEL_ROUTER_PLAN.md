# AI Model Router Plan (Dealix)

## Goals
- Single router for all LLM calls in Dealix
- Cost + latency + quality + safety observable
- Easy to swap providers
- Demo mode works without API keys

## Components
- `dealix/ai/router.py` — central router
- `dealix/ai/providers/base.py` — provider interface
- `dealix/ai/providers/openai.py` — OpenAI provider
- `dealix/ai/providers/anthropic.py` — Anthropic provider
- `dealix/ai/providers/local.py` — local stub for demo

## Routing table
| Task class | Default | Fallback |
|------------|---------|----------|
| Outbound draft | OpenAI gpt-4o-mini | local stub |
| Proposal | OpenAI gpt-4o | local stub |
| Proof report | OpenAI gpt-4o | local stub |
| Industry analysis | Anthropic claude-sonnet | local stub |

## Safety
- Every prompt has a `safety_tag` injected
- Every response is checked for banned claims
- No response is auto-used — output is always draft
