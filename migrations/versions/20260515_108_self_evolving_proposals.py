"""Self-evolving proposals schema reference for enterprise control plane."""

DDL = """
CREATE TABLE improvement_proposals (
  proposal_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  title TEXT NOT NULL,
  change_summary TEXT NOT NULL,
  proposed_by TEXT NOT NULL,
  state TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  approved_by TEXT,
  applied_by TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
"""
