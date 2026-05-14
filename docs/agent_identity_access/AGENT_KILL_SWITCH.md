# Agent Kill Switch

5 kill types: Soft Kill (pause session), Tool Kill (revoke tool), Client Kill (block per client/project), Agent Kill (disable globally), Fleet Kill (pause all agents of class).

9 triggers: owner removed, policy violation, unexpected tool request, attempted external action, PII exposure risk, repeated low QA, client boundary violation, prompt injection suspected, unused 90 days.

Typed: `agent_identity_access_os.kill_switch.KillEvent`.
