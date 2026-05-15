"""Assurance contracts schema reference for enterprise control plane."""

DDL = """
CREATE TABLE assurance_contracts (
  contract_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  status TEXT NOT NULL,
  external_action BOOLEAN NOT NULL DEFAULT FALSE,
  irreversible_action BOOLEAN NOT NULL DEFAULT FALSE,
  rollback_plan_required BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL
);
"""
