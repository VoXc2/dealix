"""Runtime safety schema reference for enterprise control plane."""

DDL = """
CREATE TABLE runtime_safety_kill_switches (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  agent_id TEXT NOT NULL,
  isolated BOOLEAN NOT NULL DEFAULT TRUE,
  reason TEXT NOT NULL,
  triggered_by TEXT NOT NULL,
  triggered_at TIMESTAMPTZ NOT NULL
);
"""
