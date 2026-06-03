# AI CONVENTIONS — Dealix Three Gear System v3.0
# Primary: DeepSeek (Gear 1) / Minimax M2.5 (Gear 2) / Minimax M2.7 (Gear 3)
# Fallback: DeepSeek-chat

## 1. GEAR SELECTION RULES
- Gear 1 (DeepSeek): 90% of tasks. Refactoring, tests, docs, small fixes.
- Gear 2 (Minimax M2.5): 9% of tasks. New features, bug fixes, pipeline logic.
- Gear 3 (Minimax M2.7): 1% of tasks. System design, compliance, hard bugs.
- ALWAYS start with Gear 1 unless task is clearly Gear 2/3.
- Switch UP a gear if Gear 1 fails 2 times on same task.

## 2. PROVIDER RULES
- ALL requests go through OpenRouter.
- NEVER use OpenAI directly.
- Preserve reasoning_details blocks when using Minimax models.
- DeepSeek has NO reasoning_details - skip that field.

## 3. CODE STANDARDS
- Type hints EVERYWHERE.
- Pydantic v2 models for ALL agent I/O.
- Google-style docstrings.
- Keep functions under 40 lines.
- Use | None instead of Optional (Python 3.11+).
- Structured outputs with JSON Schema when calling LLMs.

## 4. BILINGUAL AR/EN
- Variable names, function names: English only.
- Docstrings: English.
- User-facing strings: Arabic + English (bilingual dict).
- Comments explaining Saudi business logic: Arabic acceptable.

## 5. SECURITY
- NO hardcoded secrets. EVER.
- SecretStr for all sensitive config fields.
- .env.local ONLY -- never commit secrets.
- Run pytest before considering task complete.
- Run py_compile on all modified files.

## 6. TASK WORKFLOW
1. Read relevant files in plane order.
2. State plan explicitly.
3. Implement with SEARCH/REPLACE blocks.
4. Add/update tests.
5. Verify: pytest + py_compile + check.py.
6. Commit with descriptive English message.
7. Report: files changed, tests passed, cost tier used.

## 7. COST OPTIMIZATION
- Always prefer Gear 1 (DeepSeek) unless task demands higher.
- Keep prompt context minimal (use /add sparingly).
- Use --map-tokens 1024 in Aider.
- Check credits with: py -3 scripts/credit-guard.py
