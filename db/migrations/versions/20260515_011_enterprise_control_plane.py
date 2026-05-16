"""Enterprise Control Plane persistence tables.

Revision ID: 011
Revises: 010
Create Date: 2026-05-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "011"
down_revision: Union[str, Sequence[str], None] = "010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "workflow_runs",
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("workflow_id", sa.Text(), nullable=False),
        sa.Column("customer_id", sa.Text(), nullable=True),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column("correlation_id", sa.Text(), nullable=True),
        sa.Column("parent_run_id", sa.Text(), nullable=True),
        sa.Column("current_step", sa.Text(), nullable=True),
        sa.Column(
            "attached_policy_ids",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "metadata",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index("ix_workflow_runs_tenant", "workflow_runs", ["tenant_id"])
    op.create_index("ix_workflow_runs_state", "workflow_runs", ["state"])

    op.create_table(
        "control_events",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("source_module", sa.Text(), nullable=False),
        sa.Column("actor", sa.Text(), nullable=False),
        sa.Column("subject_type", sa.Text(), nullable=True),
        sa.Column("subject_id", sa.Text(), nullable=True),
        sa.Column("run_id", sa.Text(), nullable=True),
        sa.Column("correlation_id", sa.Text(), nullable=True),
        sa.Column("decision", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "payload",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("redacted", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_control_events_tenant", "control_events", ["tenant_id"])
    op.create_index("ix_control_events_run", "control_events", ["run_id"])
    op.create_index("ix_control_events_type", "control_events", ["event_type"])

    op.create_table(
        "approval_tickets",
        sa.Column("ticket_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requested_by", sa.Text(), nullable=False),
        sa.Column("source_module", sa.Text(), nullable=False),
        sa.Column("subject_type", sa.Text(), nullable=True),
        sa.Column("subject_id", sa.Text(), nullable=True),
        sa.Column("run_id", sa.Text(), nullable=True),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column("granted_by", sa.Text(), nullable=True),
        sa.Column("rejected_by", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "metadata",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("ticket_id"),
    )
    op.create_index("ix_approval_tickets_tenant", "approval_tickets", ["tenant_id"])
    op.create_index("ix_approval_tickets_state", "approval_tickets", ["state"])

    op.create_table(
        "agent_mesh_agents",
        sa.Column("agent_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("owner", sa.Text(), nullable=False),
        sa.Column(
            "capabilities",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("trust_tier", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("autonomy_level", sa.Integer(), nullable=False),
        sa.Column("endpoint", sa.Text(), nullable=True),
        sa.Column("composite_score", sa.Float(), nullable=True),
        sa.Column(
            "tool_permissions",
            JSONB,
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("agent_id"),
    )
    op.create_index("ix_agent_mesh_agents_tenant", "agent_mesh_agents", ["tenant_id"])
    op.create_index("ix_agent_mesh_agents_status", "agent_mesh_agents", ["status"])

    op.create_table(
        "assurance_contracts",
        sa.Column("contract_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("action_type", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("external_action", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "irreversible_action",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "rollback_plan_required",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("contract_id"),
        sa.UniqueConstraint("tenant_id", "action_type", name="uq_assurance_contract_tenant_action"),
    )
    op.create_index("ix_assurance_contracts_tenant", "assurance_contracts", ["tenant_id"])

    op.create_table(
        "runtime_safety_kill_switches",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("agent_id", sa.Text(), nullable=False),
        sa.Column("isolated", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("triggered_by", sa.Text(), nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_runtime_safety_tenant", "runtime_safety_kill_switches", ["tenant_id"])

    op.create_table(
        "value_metrics",
        sa.Column("metric_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("metric_name", sa.Text(), nullable=False),
        sa.Column("metric_kind", sa.Text(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("metric_id"),
    )
    op.create_index("ix_value_metrics_tenant", "value_metrics", ["tenant_id"])
    op.create_index("ix_value_metrics_run", "value_metrics", ["run_id"])

    op.create_table(
        "improvement_proposals",
        sa.Column("proposal_id", sa.Text(), nullable=False),
        sa.Column("tenant_id", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("change_summary", sa.Text(), nullable=False),
        sa.Column("proposed_by", sa.Text(), nullable=False),
        sa.Column("state", sa.Text(), nullable=False),
        sa.Column(
            "metadata",
            JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("approved_by", sa.Text(), nullable=True),
        sa.Column("applied_by", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("proposal_id"),
    )
    op.create_index("ix_improvement_proposals_tenant", "improvement_proposals", ["tenant_id"])
    op.create_index("ix_improvement_proposals_state", "improvement_proposals", ["state"])


def downgrade() -> None:
    op.drop_index("ix_improvement_proposals_state", table_name="improvement_proposals")
    op.drop_index("ix_improvement_proposals_tenant", table_name="improvement_proposals")
    op.drop_table("improvement_proposals")

    op.drop_index("ix_value_metrics_run", table_name="value_metrics")
    op.drop_index("ix_value_metrics_tenant", table_name="value_metrics")
    op.drop_table("value_metrics")

    op.drop_index("ix_runtime_safety_tenant", table_name="runtime_safety_kill_switches")
    op.drop_table("runtime_safety_kill_switches")

    op.drop_index("ix_assurance_contracts_tenant", table_name="assurance_contracts")
    op.drop_table("assurance_contracts")

    op.drop_index("ix_agent_mesh_agents_status", table_name="agent_mesh_agents")
    op.drop_index("ix_agent_mesh_agents_tenant", table_name="agent_mesh_agents")
    op.drop_table("agent_mesh_agents")

    op.drop_index("ix_approval_tickets_state", table_name="approval_tickets")
    op.drop_index("ix_approval_tickets_tenant", table_name="approval_tickets")
    op.drop_table("approval_tickets")

    op.drop_index("ix_control_events_type", table_name="control_events")
    op.drop_index("ix_control_events_run", table_name="control_events")
    op.drop_index("ix_control_events_tenant", table_name="control_events")
    op.drop_table("control_events")

    op.drop_index("ix_workflow_runs_state", table_name="workflow_runs")
    op.drop_index("ix_workflow_runs_tenant", table_name="workflow_runs")
    op.drop_table("workflow_runs")
