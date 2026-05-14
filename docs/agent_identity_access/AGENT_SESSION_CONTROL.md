# Agent Session Control

Each agent run = session: session_id, agent_id, client_id, project_id, task, allowed_tools, expires_at, status.

Typed: `agent_identity_access_os.session_control.AgentSession` rejects missing client/project + empty tools.
