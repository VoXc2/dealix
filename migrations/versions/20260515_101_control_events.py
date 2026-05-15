"""Control events schema reference for enterprise control plane.

Source of truth migration: db/migrations/versions/20260515_011_enterprise_control_plane.py
"""

DDL = """
CREATE TABLE control_events (
  id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  source_module TEXT NOT NULL,
  actor TEXT NOT NULL,
  subject_type TEXT,
  subject_id TEXT,
  run_id TEXT,
  correlation_id TEXT,
  decision TEXT,
  occurred_at TIMESTAMPTZ NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}',
  redacted BOOLEAN NOT NULL DEFAULT TRUE
);
"""
