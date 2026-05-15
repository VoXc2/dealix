"""Reporting OS — thin facade over executive_reporting."""

from auto_client_acquisition.executive_reporting.schemas import WeeklyReport
from auto_client_acquisition.reporting_os.executive_report import empty_weekly_report
from auto_client_acquisition.reporting_os.proof_pack import (
    MASTER_SECTION_KEYS,
    build_master_proof_pack_dict,
    build_proof_pack_dict,
    proof_pack_has_required_sections,
    proof_pack_master_complete,
    render_proof_pack_markdown,
)

__all__ = [
    "WeeklyReport",
    "MASTER_SECTION_KEYS",
    "build_master_proof_pack_dict",
    "build_proof_pack_dict",
    "empty_weekly_report",
    "proof_pack_has_required_sections",
    "proof_pack_master_complete",
    "render_proof_pack_markdown",
]
