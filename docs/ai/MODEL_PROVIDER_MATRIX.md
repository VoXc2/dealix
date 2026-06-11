# Model Provider Matrix (Dealix)

| Provider | Env var | Default in demo? | Notes |
|----------|---------|-------------------|-------|
| minimax | MINIMAX_API_KEY | no | Primary target |
| kimi | KIMI_API_KEY | no | Backup |
| deepseek | DEEPSEEK_API_KEY | no | Cost-effective |
| openrouter | OPENROUTER_API_KEY | no | Multi-model |
| openai | OPENAI_API_KEY | no | Optional |
| deterministic | — | yes | Always works |

Set `AI_PROVIDER_DEFAULT=minimax` to choose.

In demo mode, the router always uses the deterministic templates.
