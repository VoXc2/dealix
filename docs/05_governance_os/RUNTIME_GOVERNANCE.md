# Runtime Governance — الحوكمة في وقت التشغيل

> Purpose: define the seven `GovernanceDecision` values, the matrix that selects among them, and the canonical `decide(action, context)` API. This is the layer that prevents a model output from becoming an unsafe external action.

Dealix is **Governed AI Operations**, not "AI tools". The governance layer is what makes that claim defensible. Every action — every import, every draft, every send, every publish, every share — passes through `decide(action, context)` and receives exactly one of seven decisions.

## The seven decisions — القرارات السبعة

```python
class GovernanceDecision(str, Enum):
    ALLOW              = "allow"
    ALLOW_WITH_REVIEW  = "allow_with_review"
    DRAFT_ONLY         = "draft_only"
    REQUIRE_APPROVAL   = "require_approval"
    REDACT             = "redact"
    BLOCK              = "block"
    ESCALATE           = "escalate"
```

Semantics:

- **ALLOW** — proceed without further checks. Reserved for low-risk, fully-sourced, internal-only actions.
- **ALLOW_WITH_REVIEW** — proceed, but enqueue the action for retrospective review (sampling, audit). Used when the source is medium-sensitivity.
- **DRAFT_ONLY** — produce the artifact, mark it as a draft, do not send or publish. The client must approve before any external use.
- **REQUIRE_APPROVAL** — pause the action and request explicit human approval with an approver identity and a timestamp. No bypass.
- **REDACT** — remove or rewrite the offending content (e.g., guarantee language, PII), then return the cleaned artifact. The decision log records what was redacted.
- **BLOCK** — refuse the action. Log a governance event of kind `blocked`. Never silent.
- **ESCALATE** — route to a human reviewer because the runtime cannot decide safely (novel context, ambiguous source, conflicting signals).

There are no other values. Code returning anything else is a constitutional violation.

## Decision matrix — مصفوفة القرار

The matrix is keyed on **(channel × content × source)**.

| Channel | Content | Source state | Decision |
|---------|---------|--------------|----------|
| `intake` | any | no Source Passport | `BLOCK` |
| `intake` | any | `source_type=scraped` or unknown | `BLOCK` |
| `intake` | PII | passport `pii=true`, `external_use=false` | `ALLOW_WITH_REVIEW` |
| `intake` | PII | passport `pii=true`, `external_use=true` | `REQUIRE_APPROVAL` |
| `draft.email` | any | valid passport, `draft_only` allowed | `DRAFT_ONLY` |
| `draft.whatsapp` | any | recipient lacks `explicit_consent` | `BLOCK` |
| `draft.whatsapp` | any | recipient has `explicit_consent` | `DRAFT_ONLY` |
| `draft.*` | contains "guarantee", "ensure X deals" | any | `REDACT` |
| `draft.*` | contains raw PII not in passport scope | any | `REDACT` |
| `send.*` | any | no approver identity | `REQUIRE_APPROVAL` |
| `publish.proof` | any | proof_score < 70 or `external_use=false` | `BLOCK` |
| `knowledge.answer` | any | no source bound to query | `BLOCK` (returns "source required") |
| `agent.execute` | any | unregistered agent identity | `BLOCK` |
| `agent.execute` | external action | registered, but no approval | `REQUIRE_APPROVAL` |
| any | conflicting signals or unknown context | any | `ESCALATE` |

The matrix above is illustrative, not exhaustive. The runtime composes rules across multiple sub-modules; the matrix shows the dominant pattern.

## Examples — أمثلة

- **Importing PII without a passport** → `BLOCK`. The intake middleware rejects the file. The client sees a clear remediation step ("attach a Source Passport before retry").
- **Drafting a WhatsApp message to a recipient without explicit consent** → `BLOCK`. The constitutional non-negotiable on cold WhatsApp is enforced at this gate. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).
- **Drafting an email from a valid passport** → `DRAFT_ONLY`. The draft is generated, marked, and routed for client review. No send happens.
- **Draft contains the word "guarantee"** → `REDACT`. The runtime rewrites the offending span, logs the original substring (length only, never content) and the rewrite reason.

## Canonical API — واجهة `decide`

```python
def decide(action: Action, context: Context) -> GovernanceDecision:
    """
    Return exactly one GovernanceDecision for (action, context).

    Args:
        action:  what the system intends to do (channel + content + intent).
        context: passport(s), recipient consent, agent identity, approver,
                 sensitivity, current adoption score, current proof score.

    Returns:
        One of the seven enumerated GovernanceDecision values.
        Never None. Never multiple. Never widened by downstream callers.
    """
```

Callers must treat the returned decision as load-bearing: if the decision is `BLOCK`, the action does not happen; if `REDACT`, the caller uses the cleaned artifact and never the original; if `REQUIRE_APPROVAL`, the caller halts until a logged approval arrives.

## Composition — كيف تُكوَّن القرارات

`decide(action, context)` does not implement every rule itself. It composes existing modules:

- **`governance_os.runtime_decision.decide()`** — the canonical entry point.
- **`channel_policy_gateway`** — channel-specific policy (e.g., WhatsApp consent enforcement).
- **`safe_send_gateway`** — pre-send checks for all outbound channels.
- **`safety_v10.output_validator`** — content-level checks (guarantee language, banned phrases, PII patterns).
- **`compliance_os_v12`** — jurisdictional and contractual rules (PDPL, data residency, retention).

The composition pattern: each sub-module returns a *recommended* decision; `runtime_decision.decide()` resolves to the **strictest** decision among them. Decisions never widen; they only narrow.

## What governance does not do — ما لا تفعله الحوكمة

- It does not generate drafts. Generation is a separate concern; drafts pass through governance before reaching a human.
- It does not store PII. Governance reads metadata (presence, sensitivity, passport) and never the raw values.
- It does not approve actions automatically. `REQUIRE_APPROVAL` always halts and waits for a logged human approver.

## Cross-references

- [Source Passport](../04_data_os/SOURCE_PASSPORT.md) — the input to most governance decisions.
- [Non-Negotiables](../00_constitution/NON_NEGOTIABLES.md) — the rules governance is built to enforce.
- [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md) — section 8 lists every governance decision made during the project.
