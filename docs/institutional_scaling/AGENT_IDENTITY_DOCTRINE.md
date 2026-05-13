# Agent Identity Doctrine

Every agent inside Dealix carries an identity card. No card = no invocation.

## 1. The card

Canonical schema in `endgame_os/agent_control.py` extended by `institutional_control_os/agent_control_plane.py` with `allowed_tools`.

## 2. Autonomy levels and MVP rule

| Level | Meaning |
| --- | --- |
| 0 | Read |
| 1 | Analyze |
| 2 | Draft / Recommend |
| 3 | Queue for approval |
| 4 | Execute internal after approval |
| 5 | External action restricted |
| 6 | Autonomous external action — forbidden |

MVP allows only levels 0–3. Levels 4–5 require contract clauses. Level 6 is constitutionally forbidden.

## 3. Required attributes

Identity, owner, purpose, allowed inputs, allowed tools, forbidden actions, autonomy level, approval requirements, audit requirements, decommission rule.

## 4. Lifecycle

Register before first invocation; revise only with cross-BU approval at autonomy ≥ 4; pause at any time; retire with the card preserved for audit.

## 5. The principle

> Every agent is a registered identity inside Dealix. There are no anonymous actors.
