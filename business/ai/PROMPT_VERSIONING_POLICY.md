# Prompt Versioning Policy (Dealix)

## Format
- `vMAJOR.MINOR.PATCH`
- MAJOR: breaking change in prompt structure
- MINOR: added field or new behavior
- PATCH: wording tweak

## When to bump
- New constraint added → MINOR
- New task type added → MAJOR (new entry)
- Tone tweak → PATCH

## Where
- `scripts/lib/ai_router.py` references `prompt_versions` map
- `PROMPT_REGISTRY.md` is the source of truth
- `prompt_version` is logged in every AI result
