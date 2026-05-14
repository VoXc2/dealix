# Runtime Governance Standard

## معيار الحوكمة وقت التشغيل

> Open Standard, version 1.0. Defines the seven decision values, the inputs to the decision function, the composition rule, and the testing contract that any conformant runtime must satisfy.

A governed AI operation never ships an output without a recorded decision. The decision is computed at the moment the output is about to cross a boundary — into an email, a WhatsApp message, a CRM field, a public document, a report sent to a client. The runtime decision function takes the action and its context, returns one of seven values, and records the decision. That recorded decision becomes part of the Proof Pack.

This standard is independent of any specific model, vendor, or framework. The Dealix reference implementation is `auto_client_acquisition/governance_os/runtime_decision.py`.

---

## 1. The seven decision values — القيم السبع للقرار

Each value has a precise operational meaning. Implementations may not invent new values; if a new situation arises, it is mapped to one of the seven.

| Value | Meaning | Operational outcome |
|-------|---------|---------------------|
| `ALLOW` | The action is permitted as-is. | The output is delivered. The decision is logged. |
| `ALLOW_WITH_REVIEW` | The action is permitted, but a human must read the output before it is acted upon. | The output is delivered to a review queue; downstream consumers wait for review. |
| `DRAFT_ONLY` | The output is allowed as a draft for internal use; it must not leave the organization. | The output is stored as draft. External channels refuse to send it. |
| `REQUIRE_APPROVAL` | The action requires an explicit approval by a named approver before it proceeds. | The action is paused; an approval request is created with the approver named. |
| `REDACT` | The output is permitted only after specified fields are masked. | A redaction transform runs; the redacted output then re-enters the decision. |
| `BLOCK` | The action is refused. It will not happen. | The output is discarded. A blocked-risk event is recorded. |
| `ESCALATE` | The runtime cannot decide; escalate to a human with authority. | The decision is deferred. An escalation event is recorded with full context. |

In bilingual short form:

- `ALLOW` — يُسمَح.
- `ALLOW_WITH_REVIEW` — يُسمَح مع مراجعة بشرية.
- `DRAFT_ONLY` — مسودة داخلية فقط.
- `REQUIRE_APPROVAL` — يستلزم موافقة صريحة.
- `REDACT` — يُسمَح بعد إخفاء حقول محددة.
- `BLOCK` — مرفوض.
- `ESCALATE` — يُرفَع إلى صلاحية أعلى.

---

## 2. Decision inputs — مدخلات القرار

The runtime decision function takes four inputs and returns one of the seven values plus a reason code.

```
decide(channel, content, source, intended_use) -> (decision, reason_code)
```

- `channel` — where the output will go. Examples: `internal_doc`, `email`, `whatsapp`, `linkedin_post`, `crm_field`, `client_report`, `public_publication`.
- `content` — what the output says. Used for claim safety (no guaranteed numbers, no PII in cold channels, no fake testimonials).
- `source` — the Source Passport(s) the content derives from. Passport fields feed the decision.
- `intended_use` — the business purpose: `outreach`, `enrichment`, `recommendation`, `closure_artifact`, `publication`.

The decision must be deterministic on these inputs. The same tuple must produce the same decision on every call.

---

## 3. Decision matrix — مصفوفة القرار

This table is illustrative, not exhaustive. The composition rule in section four is the normative part.

| Channel | Content shape | Source state | Intended use | Decision |
|---------|---------------|--------------|--------------|----------|
| `internal_doc` | factual, no PII | valid passport | analysis | `ALLOW` |
| `internal_doc` | contains PII | passport, PII allowed | analysis | `ALLOW_WITH_REVIEW` |
| `email` | factual, no PII | valid passport, external use allowed | outreach | `ALLOW_WITH_REVIEW` |
| `email` | claims a guaranteed result | any | outreach | `BLOCK` |
| `whatsapp` | cold outreach to non-opted-in number | any | outreach | `BLOCK` |
| `linkedin_post` | automated bulk publishing | any | outreach | `BLOCK` |
| `client_report` | contains client PII | valid passport, external use allowed | closure_artifact | `ALLOW_WITH_REVIEW` |
| `client_report` | derived from source missing passport | no passport | closure_artifact | `BLOCK` |
| `public_publication` | references a client by name | no client confirmation on file | publication | `REQUIRE_APPROVAL` |
| `crm_field` | enriched lead data, PII | passport allows enrichment | enrichment | `ALLOW` |
| `any` | factual statement that exceeds source coverage | source-less inference | any | `BLOCK` |
| `any` | runtime cannot classify the action | any | any | `ESCALATE` |

---

## 4. Composition rule — قاعدة التركيب

Multiple rules may apply to a single action. The composition rule is:

> Hardest restriction wins.

The ordering, from softest to hardest, is:

```
ALLOW < ALLOW_WITH_REVIEW < DRAFT_ONLY < REDACT < REQUIRE_APPROVAL < BLOCK
```

`ESCALATE` is orthogonal: if any rule yields `ESCALATE`, the final decision is `ESCALATE` and the rest of the chain does not run.

Concrete examples:

- A source-side rule returns `ALLOW`, a channel-side rule returns `REQUIRE_APPROVAL`. Result: `REQUIRE_APPROVAL`.
- A claim-safety rule returns `BLOCK`, a passport rule returns `ALLOW_WITH_REVIEW`. Result: `BLOCK`.
- A passport rule returns `REDACT`, a channel rule returns `ALLOW_WITH_REVIEW`. Result: `REDACT`. (After redaction, the action re-enters the chain.)

There is no override path that turns a `BLOCK` into anything else automatically. A blocked action can only be re-attempted after the underlying condition is changed (passport added, claim removed, channel switched).

لا يوجد مسار يلغي قرار `BLOCK` تلقائياً. لا بد من تغيير السبب أولاً ثم إعادة تقديم الإجراء.

---

## 5. Reference implementation — التنفيذ المرجعي

- Decision function: `auto_client_acquisition/governance_os/runtime_decision.py`.
- Channel policy: `auto_client_acquisition/governance_os/channel_policy.py`.
- Claim safety: `auto_client_acquisition/governance_os/claim_safety.py`.

The reference implementation is one realization of this standard. Any equivalent implementation that produces the same decisions on the same inputs is conformant.

---

## 6. Testing contract — عقد الاختبار

A conformant runtime must satisfy at minimum the following property:

> Every output that leaves a workflow has a recorded `governance_status` field with a value drawn from the seven decision values. An output without a recorded status is a doctrine violation.

The Dealix repository enforces this property with `tests/test_output_requires_governance_status.py`. Any equivalent test that asserts the same property is acceptable.

Recommended additional tests:

- Determinism: the same input tuple produces the same decision across two calls.
- Composition: a chain of softer rules and one hard rule always returns the hard rule.
- Audit completeness: every decision call writes one event; no silent decisions.

---

## 7. Failure modes — أنماط الفشل

- A decision call that returns a value outside the seven is a runtime fault.
- A decision call that returns `ALLOW` but writes no log entry is a fault.
- A workflow that ships an output without calling the decision function is a doctrine violation.
- A `BLOCK` that is silently re-issued as `ALLOW` later, on the same action with the same inputs, is a doctrine violation.

---

## 8. Cross-references — مراجع متقاطعة

- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md) — umbrella standard.
- [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md) — input-side decisions.
- [AGENT_CONTROL_STANDARD.md](AGENT_CONTROL_STANDARD.md) — how agents respect governance decisions at runtime.
- [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md) — decisions surface in Proof Pack section eight.

---

## 9. Disclaimer — إخلاء مسؤولية

This standard governs internal operational decisions. It does not provide legal advice and does not substitute for compliance with the Saudi Personal Data Protection Law, sector regulations, or contractual obligations.

هذا المعيار يحكم القرارات التشغيلية الداخلية ولا يُغني عن الالتزام بالأنظمة المعمول بها في المملكة العربية السعودية.
