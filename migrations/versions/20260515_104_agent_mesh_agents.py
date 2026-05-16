"""Agent mesh agents schema reference for enterprise control plane."""

DDL = """
CREATE TABLE agent_mesh_agents (
  agent_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  name TEXT NOT NULL,
  owner TEXT NOT NULL,
  capabilities JSONB NOT NULL DEFAULT '[]',
  trust_tier TEXT NOT NULL,
  status TEXT NOT NULL,
  autonomy_level INT NOT NULL,
  endpoint TEXT,
  composite_score DOUBLE PRECISION,
  tool_permissions JSONB NOT NULL DEFAULT '[]',
  registered_at TIMESTAMPTZ NOT NULL
);
"""
