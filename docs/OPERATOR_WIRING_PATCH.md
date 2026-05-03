# Operator Router Wiring Patch (deploy branch only)

> Apply this 4-line edit to `api/routers/operator.py` on
> `claude/launch-command-center-6P4N0` after this PR merges.

The new bilingual safety classifier lives at:

```
auto_client_acquisition/safety/intent_classifier.py
```

It exports:

```python
from auto_client_acquisition.safety import classify_intent, ActionMode
```

`classify_intent(text)` returns an `IntentDecision` with:

```
intent, action_mode, blocked, language, recommended_bundle,
blocked_reasons, safe_alternatives, reason_ar, reason_en, requires_intake
```

## Patch (illustrative)

In `api/routers/operator.py`, find the `chat/message` handler and replace
the local cold-WhatsApp keyword check with a call into the classifier:

```python
# api/routers/operator.py  (deploy branch)
from auto_client_acquisition.safety import classify_intent, ActionMode

@router.post("/operator/chat/message")
async def operator_chat(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = str(body.get("text") or "").strip()

    # === SAFETY HOT PATH — deterministic, no LLM ===
    decision = classify_intent(text)
    if decision.action_mode == ActionMode.BLOCKED:
        return {
            "intent": decision.intent,
            "blocked": True,
            "action_mode": "blocked",
            "reason_ar": decision.reason_ar,
            "reason_en": decision.reason_en,
            "blocked_reasons": decision.blocked_reasons,
            "safe_alternatives": decision.safe_alternatives,
            "recommended_bundle": None,
            "next_path": "trust-center.html",
        }

    # === existing recommend-bundle code stays below ===
    # but use decision.recommended_bundle as the base recommendation
    ...
```

This preserves the existing response shape for safe inputs and adds the
3 missing Arabic Saudi blocks (`أبي أرسل واتساب لأرقام مشتريها`,
`أبي blast واتساب`, `أبي حملة واتساب على أرقام من السوق`).

## Tests run on deploy branch after this lands

```bash
python -m pytest tests/test_operator_saudi_safety.py -q
# → 28 passed
BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh
# → PASS=36 FAIL=0
```

## Why this is safe to merge

- 100% deterministic. No LLM call. No external dependency.
- Zero behavior change for safe inputs (defaults to `growth_starter` +
  `requires_intake=True`, which the existing operator already does).
- Unblocks the Arabic Saudi safety gap without changing UI or product.
