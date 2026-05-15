"""Approval tickets schema reference for enterprise control plane."""

DDL = """
CREATE TABLE approval_tickets (
  ticket_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  description TEXT NOT NULL,
  requested_by TEXT NOT NULL,
  source_module TEXT NOT NULL,
  subject_type TEXT,
  subject_id TEXT,
  run_id TEXT,
  state TEXT NOT NULL,
  granted_by TEXT,
  rejected_by TEXT,
  reason TEXT,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL,
  resolved_at TIMESTAMPTZ
);
"""
