"""Data OS — tabular quality, preview, validation, PII hints, source coverage."""

from auto_client_acquisition.data_os.data_quality_score import (
    account_row_completeness,
    duplicate_ratio_by_field,
    mean_completeness,
    summarize_table_quality,
)
from auto_client_acquisition.data_os.dedupe import (
    DedupeHint,
    normalize_company_name,
    normalize_domain,
    normalize_phone_e164_hint,
    suggest_dedupe_fingerprint,
)
from auto_client_acquisition.data_os.import_preview import import_preview_csv
from auto_client_acquisition.data_os.normalization import normalize_account_row_fields
from auto_client_acquisition.data_os.pii_detection import (
    column_name_suggests_pii,
    pii_flags_for_row,
)
from auto_client_acquisition.data_os.source_attribution import (
    row_has_source,
    source_coverage_ratio,
    summarize_sources,
)
from auto_client_acquisition.data_os.source_passport import (
    SourcePassport,
    ValidationResult,
    governance_decision_hints_for_passport_gate,
    requires_approval,
    source_passport_allows_task,
    source_passport_from_v2,
    source_passport_valid_for_ai,
    validate,
)
from auto_client_acquisition.data_os.validation_rules import validate_account_row, validate_rows

__all__ = [
    "DedupeHint",
    "account_row_completeness",
    "column_name_suggests_pii",
    "SourcePassport",
    "ValidationResult",
    "duplicate_ratio_by_field",
    "governance_decision_hints_for_passport_gate",
    "import_preview_csv",
    "mean_completeness",
    "normalize_account_row_fields",
    "normalize_company_name",
    "normalize_domain",
    "normalize_phone_e164_hint",
    "pii_flags_for_row",
    "requires_approval",
    "row_has_source",
    "source_coverage_ratio",
    "source_passport_allows_task",
    "source_passport_from_v2",
    "source_passport_valid_for_ai",
    "suggest_dedupe_fingerprint",
    "summarize_sources",
    "summarize_table_quality",
    "validate",
    "validate_account_row",
    "validate_rows",
]
