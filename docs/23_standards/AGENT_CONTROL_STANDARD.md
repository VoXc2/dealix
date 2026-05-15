# Agent Control Standard

## معيار التحكم في وكلاء الذكاء الاصطناعي

> Open Standard, version 1.0. Defines the identity, autonomy, tool boundary, runtime state machine, and kill-switch contract for AI agents operating inside Saudi B2B operations. Any organization may adopt it.

An AI agent is any software entity that (a) reads inputs, (b) invokes a model, and (c) can take an action with effects outside its own process. An agent that can only suggest text to a human is still an agent under this standard; it must have an identity, a card, and a controlling owner. An agent that can send a message, write to a CRM, or call an external API is more strongly constrained.

The Dealix reference implementation will live in `auto_client_acquisition/agent_os/` and `auto_client_acquisition/secure_agent_runtime_os/`.

---

## 1. Agent Card — بطاقة الوكيل

No agent may run in production without a complete Agent Card. The Card is the agent's identity document, equivalent in spirit to the Source Passport for data.

### Required fields

| Field | Type | Meaning |
|-------|------|---------|
| `agent_id` | string, unique | Stable identifier within the tenant. |
| `name` | string | Human-readable name. |
| `owner` | string | The named person accountable for the agent. Not a team, not a tool. |
| `purpose` | string | One-sentence statement of the agent's job. |
| `autonomy_level` | enum `L0`..`L5` | Operating authority. Defined below. |
| `allowed_tools` | array of tool ids | Closed list of tools the agent may invoke. |
| `forbidden_tools` | array of tool ids | Explicitly denied tools, even if listed elsewhere. |
| `kill_switch_owner` | string | The named person empowered to immediately revoke the agent. |
| `status` | enum | `proposed`, `approved`, `active`, `paused`, `retired`. |

Optional but recommended: `version`, `created_at`, `last_reviewed_at`, `linked_workflow`, `linked_proof_pack`.

```json
{
  "agent_id": "lead-prep-v1",
  "name": "Lead Prep Drafter",
  "owner": "ops.lead@example.com",
  "purpose": "Draft a one-page brief per shortlisted account from existing CRM data.",
  "autonomy_level": "L1",
  "allowed_tools": ["read", "analyze", "draft", "queue_for_approval"],
  "forbidden_tools": ["send_email", "send_whatsapp", "linkedin_post", "scrape_web", "export_pii"],
  "kill_switch_owner": "founder@example.com",
  "status": "active"
}
```

An agent missing any required field is non-conformant and must not run.

---

## 2. Autonomy levels — مستويات الاستقلالية

Six levels, from human-only to fully autonomous. The MVP default is `L1`. Levels above `L4` are banned in MVP.

| Level | Name | Description |
|-------|------|-------------|
| `L0` | **Human-only** | The agent does not act. Used during evaluation. All outputs are advisory text. |
| `L1` | **Draft-assisted** (MVP default) | The agent produces drafts a human must review before any action. |
| `L2` | **Review-required** | The agent prepares actions but cannot execute them without explicit human approval per action. |
| `L3` | **Conditional-auto** | The agent may execute pre-approved action classes inside a narrow scope; everything else escalates. |
| `L4` | **Auto-with-audit** | The agent executes broadly within its allowed tools; every action is audited and reviewable. |
| `L5` | **Fully-autonomous** | The agent acts without per-action human involvement. **Banned in MVP.** |

Promotion between levels requires: a written justification, a re-issued Agent Card, an updated Proof Pack precedent, and the kill-switch owner's signed approval.

الترقية بين المستويات تستلزم مبرراً مكتوباً وبطاقة وكيل مُحدَّثة وموافقة موقَّعة من صاحب مفتاح الإيقاف.

---

## 3. Tools — الأدوات

### Hard-blocked tools in MVP

The following tools are denied for any agent in MVP, regardless of autonomy level, Card configuration, or owner approval. Attempting to invoke them produces `BLOCK` and a recorded incident.

- `send_email`
- `send_whatsapp`
- `linkedin_post`
- `scrape_web`
- `export_pii`

This list is a doctrine boundary, not a configuration. Lifting any item requires a separate standard revision, not a setting change.

### Allowed tools

The following tools are permitted for agents whose Card lists them.

- `read` — read declared data sources that pass the Source Passport check.
- `analyze` — derive aggregates, scores, classifications.
- `draft` — produce text artifacts.
- `recommend` — produce a ranked recommendation with reasoning.
- `queue_for_approval` — place a proposed action in a human review queue.

Any tool not in either list is implicitly forbidden until the standard is revised.

---

## 4. Runtime states — حالات التشغيل

An active agent exists in exactly one of six runtime states at any moment.

| State | Meaning |
|-------|---------|
| `SAFE` | Normal operating state. All tools available per Card. |
| `WATCH` | Heightened observation after a suspicious pattern. Tools available but every action is logged twice. |
| `RESTRICTED` | A subset of tools has been disabled. The agent may still act with the remaining tools. |
| `ESCALATED` | The agent has stopped acting; a human is reviewing the incident. |
| `PAUSED` | The agent is temporarily halted by its owner. All tools disabled. |
| `KILLED` | The kill switch has been triggered. The agent is terminated; all tools revoked; the Card is moved to `retired`. |

### State machine

```
SAFE  ───►  WATCH  ───►  RESTRICTED  ───►  ESCALATED  ───►  PAUSED  ───►  KILLED
  ▲           │              │                │              │
  └───────────┴──────────────┘                │              │
              (recovery to SAFE on review)    │              │
                                              └──────────────┘
                                              (escalation may pause or kill)
```

Allowed transitions:

- `SAFE → WATCH`, `SAFE → RESTRICTED`, `SAFE → ESCALATED`, `SAFE → PAUSED`, `SAFE → KILLED`.
- `WATCH → SAFE` (after clean review), `WATCH → RESTRICTED`, `WATCH → ESCALATED`, `WATCH → KILLED`.
- `RESTRICTED → SAFE` (after review), `RESTRICTED → ESCALATED`, `RESTRICTED → PAUSED`, `RESTRICTED → KILLED`.
- `ESCALATED → SAFE` (after resolution), `ESCALATED → PAUSED`, `ESCALATED → KILLED`.
- `PAUSED → SAFE` (after owner resumes), `PAUSED → KILLED`.
- `KILLED` is terminal.

---

## 5. Four-boundary protection — الحدود الأربعة

Every agent run is wrapped by four boundary checks. A failure on any one moves the agent to at least `RESTRICTED`.

1. **Prompt-integrity boundary** — inputs are checked for injection attempts, jailbreak patterns, and untrusted instructions embedded in source data. Untrusted instructions are stripped, not executed.
2. **Tool-boundary** — every tool call is validated against `allowed_tools` and `forbidden_tools` on the Agent Card. A call to a hard-blocked tool moves the agent to `ESCALATED` and triggers an audit event.
3. **Data-boundary** — every read is validated against the Source Passport rules. A read of a passport-less source moves the agent to `RESTRICTED`.
4. **Context-boundary** — outputs are checked against the Runtime Governance decision before they leave the agent. An output without a recorded decision is refused and the agent moves to `WATCH`.

The boundaries are independent and compose multiplicatively: an action passes only if all four pass.

---

## 6. Kill switch — مفتاح الإيقاف

Every agent has a named `kill_switch_owner`. The kill switch:

- May be triggered by the owner, the kill-switch owner, or a Dealix runtime safeguard.
- Revokes all tools immediately, including read-only tools.
- Sets the agent to `KILLED`. The state is terminal.
- Emits an `agent_kill` audit event with the trigger, the time, and the reason.
- Emits a `friction_log` entry so the incident enters the operational learning loop.
- Moves the Agent Card status to `retired`. A retired card cannot be reactivated; a new agent with a new `agent_id` must be created instead.

The kill switch is not a debug control. Once triggered, the agent is gone.

مفتاح الإيقاف ليس أداة تشخيص. بمجرد تفعيله، يُنهى الوكيل ويُؤرشَف.

---

## 7. Reference implementation — التنفيذ المرجعي

To be added in this same delivery wave:

- `auto_client_acquisition/agent_os/` — Agent Card structures, autonomy enums, lifecycle.
- `auto_client_acquisition/secure_agent_runtime_os/` — runtime state machine, four-boundary wrappers, kill switch.

Conformance does not require these specific modules. Any implementation that produces the same Cards, the same state transitions, and the same audit events is conformant.

---

## 8. Cross-references — مراجع متقاطعة

- [DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md](DEALIX_GOVERNED_AI_OPERATIONS_STANDARD.md).
- [SOURCE_PASSPORT_STANDARD.md](SOURCE_PASSPORT_STANDARD.md) — data-boundary inputs.
- [RUNTIME_GOVERNANCE_STANDARD.md](RUNTIME_GOVERNANCE_STANDARD.md) — context-boundary outputs.
- [PROOF_PACK_STANDARD.md](PROOF_PACK_STANDARD.md) — kill events surface as blocked-risk entries.

---

## 9. Disclaimer — إخلاء مسؤولية

This standard governs operational behavior of AI agents. It does not replace product safety obligations, contractual commitments, or regulatory requirements that may apply in specific sectors (financial services, healthcare, regulated communications).

هذا المعيار يحكم سلوك الوكلاء وقت التشغيل ولا يُغني عن متطلبات الأنظمة القطاعية.
