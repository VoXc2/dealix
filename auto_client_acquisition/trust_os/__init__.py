"""Trust OS — source passport, enterprise trust pack refs, control plane."""

from __future__ import annotations

from auto_client_acquisition.trust_os.ai_control_plane import (
    CONTROL_PLANE_COMPONENTS,
    example_ai_run_record,
)
from auto_client_acquisition.trust_os.source_passport import (
    SourcePassport,
    example_client_upload_passport,
)
from auto_client_acquisition.trust_os.compliance_report import (
    COMPLIANCE_REPORT_SECTIONS,
    compliance_report_sections_complete,
)
from auto_client_acquisition.trust_os.trust_artifacts import TRUST_ARTIFACT_TYPES, trust_artifact_coverage_score
from auto_client_acquisition.trust_os.trust_dashboard import TRUST_DASHBOARD_SIGNALS, trust_dashboard_coverage_score
from auto_client_acquisition.trust_os.trust_pack import (
    ENTERPRISE_TRUST_SECTIONS,
    TRUST_PACK_MARKDOWN_PATH,
    TrustPack,
    assemble_trust_pack,
)

__all__ = [
    "CONTROL_PLANE_COMPONENTS",
    "COMPLIANCE_REPORT_SECTIONS",
    "ENTERPRISE_TRUST_SECTIONS",
    "TRUST_ARTIFACT_TYPES",
    "TRUST_DASHBOARD_SIGNALS",
    "TRUST_PACK_MARKDOWN_PATH",
    "SourcePassport",
    "TrustPack",
    "assemble_trust_pack",
    "compliance_report_sections_complete",
    "example_ai_run_record",
    "example_client_upload_passport",
    "trust_artifact_coverage_score",
    "trust_dashboard_coverage_score",
]
