# Agent Runtime States — 6

SAFE → WATCH → RESTRICTED → ESCALATED → PAUSED → KILLED. Transitions are validated by `secure_agent_runtime_os.agent_runtime_states.is_valid_transition()`.

KILLED is terminal.
