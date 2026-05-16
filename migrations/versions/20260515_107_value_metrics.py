"""Value metrics schema reference for enterprise control plane."""

DDL = """
CREATE TABLE value_metrics (
  metric_id TEXT PRIMARY KEY,
  tenant_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  metric_kind TEXT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  source_ref TEXT,
  created_at TIMESTAMPTZ NOT NULL
);
"""
