"""Workflow runs schema reference for enterprise control plane."""

DDL = """
CREATE TABLE workflow_runs (
  run_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  workflow_id TEXT NOT NULL,
  customer_id TEXT,
  state TEXT NOT NULL,
  correlation_id TEXT,
  parent_run_id TEXT,
  current_step TEXT,
  attached_policy_ids JSONB NOT NULL DEFAULT '[]',
  metadata JSONB NOT NULL DEFAULT '{}',
  registered_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);
"""
