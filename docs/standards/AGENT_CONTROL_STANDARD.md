# AI Agent Control Standard

## Agent Card schema

agent_id, name, owner, purpose, allowed_inputs, allowed_tools, forbidden_actions, autonomy_level, approval_required_for, audit_required.

## Autonomy

0 Read, 1 Analyze, 2 Draft/Recommend, 3 Queue, 4 Execute internal (contract), 5 External restricted (enterprise), 6 Autonomous external (forbidden).

## MVP

Levels 0–3 only.

Typed: `endgame_os.agent_control.AgentCard` + `institutional_control_os.agent_control_plane.InstitutionalAgentCard` (allowed_tools required).
