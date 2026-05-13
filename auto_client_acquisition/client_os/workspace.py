"""Client Workspace — top-level container with MVP panels."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClientWorkspace:
    """Top-level workspace shown to the client.

    The workspace is constructed from the panels but does not contain
    the data itself — each panel is rendered separately.
    """

    client_id: str
    workspace_id: str
    capability_dashboard_active: bool = True
    data_readiness_panel_active: bool = True
    governance_panel_active: bool = True
    draft_pack_active: bool = True
    proof_timeline_active: bool = False
    approval_center_active: bool = False
    value_dashboard_active: bool = False
    audit_exports_active: bool = False
    tags: tuple[str, ...] = field(default_factory=tuple)

    def is_mvp(self) -> bool:
        """The MVP excludes Approval Center / Proof Timeline / audit / RBAC."""

        return (
            self.capability_dashboard_active
            and self.data_readiness_panel_active
            and self.governance_panel_active
            and self.draft_pack_active
            and not self.approval_center_active
            and not self.audit_exports_active
        )
