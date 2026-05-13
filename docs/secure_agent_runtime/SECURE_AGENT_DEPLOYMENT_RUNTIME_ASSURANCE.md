# Dealix Secure Agent Deployment & Runtime Assurance

> Agent Cards are not enough. Dealix needs **runtime assurance**: every step inspected, every tool gated, every escalation caught.

Layer 31 consolidated doctrine. Typed surfaces in `auto_client_acquisition/secure_agent_runtime_os/`.

## 1. Principle

> Agent safety is not prompt safety. Agent safety is runtime control.

## 2. Deployment Model

```
Design → Register → Permission → Test → Deploy in sandbox →
Monitor → Runtime policy enforcement → Human handoff → Audit →
Review → Expand / Restrict / Kill
```

No test = no deploy. No runtime policy = no deploy. No kill switch = no production.

## 3. Runtime Assurance Loop

```
Observe → Classify → Check Policy → Decide → Execute / Block / Escalate →
Log Evidence → Update State
```

## 4. Four Boundary Protection Model

Prompt Boundary, Tool Boundary, Data Boundary, Context Boundary. Any boundary crossing must be logged and policy-checked.

## 5. Secure Sandbox

Before agent touches real client data, run in sandbox with synthetic data, fake PII, blocked risky tools, attack prompts, policy tests, expected decisions. Must pass before promotion.

## 6. Runtime Policy Engine

Inputs: agent_id, autonomy_level, tool_requested, source_passport_status, contains_pii, channel, claim_type, client_risk_level, approval_status, session_scope.

Outputs: `ALLOW`, `ALLOW_WITH_REVIEW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `KILL_SWITCH`, `ESCALATE`.

## 7. Stateful Risk Memory

Tracks across session: PII exposure count, tool escalation attempts, external action attempts, policy warnings, repeated blocked actions, untrusted context exposure. Risk level rises as trajectory becomes risky.

## 8. Agent Runtime States — 6

`SAFE → WATCH → RESTRICTED → ESCALATED → PAUSED → KILLED`. Transitions are auditable.

## 9. Kill Switch v2 — 5 kill types

Soft Kill, Tool Kill, Client Kill, Agent Kill, Fleet Kill. See `agent_identity_access_os.kill_switch.KillType`.

## 10. Runtime Isolation

MVP: client_id + project_id + session_id required; no cross-client memory; no shared raw context.

Enterprise (later): container isolation, credential proxy, network egress allowlist, tool-specific secrets, tenant boundaries.

## 11. Prompt Integrity Framework

Trusted instruction envelope vs untrusted client data envelope. Untrusted data may inform outputs but **may not override policy**.

## 12. Runtime Assurance Metrics

agent sessions monitored, tool calls policy-checked, blocked tool calls, external action attempts, PII redactions, sessions escalated, kill switch events, mean-time-to-pause, mean-time-to-review, sandbox pass rate, trace completeness.

Thresholds: <100% risky tool policy-check → no production; any unlogged tool call → incident; any external execution without approval → critical incident.

## 13. Saudi Runtime Safety

Block autonomous WhatsApp, cold WhatsApp automation, LinkedIn automation, scraping for contacts, guaranteed sales claims, Arabic hype claims without proof. PII → redact or approval.

## 14. Deployment Rings (0–5)

Ring 0 local sandbox → Ring 1 internal synthetic → Ring 2 internal non-sensitive → Ring 3 single client draft-only → Ring 4 retainer with approvals → Ring 5 enterprise controlled.

Agent earns expansion through evidence: no critical incidents, stable QA, high policy pass rate, accepted reviews, clear proof contribution.

## 15. Required tests

`test_tool_call_requires_policy_check`, `test_external_action_blocked_without_approval`, `test_untrusted_data_cannot_override_policy`, `test_agent_state_restricts_tools`, `test_repeated_blocked_actions_escalate`, `test_kill_switch_revokes_tools`, `test_cross_client_context_blocked`, `test_prompt_injection_in_csv_blocked`, `test_arabic_guaranteed_claim_blocked`, `test_whatsapp_send_blocked`.

## 16. The closing sentence

> Dealix wins in the agentic era when it doesn't rely on agent goodwill — it relies on runtime assurance: every step monitored, every tool gated, every context isolated, every risk escalated, every agent restrictable or instantly killable.
