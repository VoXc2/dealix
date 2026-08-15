"""Database models and session management."""

from db.datetime_types import install_legacy_datetime_listener

# Install before importing any mapped model.  Annotation-inferred ``datetime``
# columns in the legacy schema are TIMESTAMP WITHOUT TIME ZONE; the listener
# normalizes aware UTC values at the bind boundary while preserving existing
# naive-UTC read semantics.  Explicit DateTime(timezone=True) columns are left
# unchanged.
install_legacy_datetime_listener()

from db.models import AgentRunRecord, Base, DealRecord, LeadRecord
from db.models_subscription import PlanRecord, SubscriptionRecord, InvoiceRecord, FeatureFlagRecord, UsageRecord  # noqa: F401
from db.models_erp import (
    ActivityRecord, MeetingRecord, NoteRecord,
    ProjectRecord, TaskRecordERP, TimeEntryRecord, MilestoneRecord,
    TicketRecord, TicketCommentRecord, KBArticleRecord, KBCategoryRecord,
    FolderRecord, DocumentRecord, DocumentPermissionRecord,
    EmployeeRecord, AttendanceRecord, LeaveRecord, PayrollRunRecord, PayrollLineRecord,
    WarehouseRecord, InventoryItemRecord, StockMovementRecord, SupplierRecord,
    PurchaseOrderRecord, PurchaseOrderLineRecord,
    GLAccountRecord, JournalEntryRecord, JournalEntryLineRecord, BankReconciliationRecord,
)  # noqa: F401
from db.session import async_session_factory, get_db

__all__ = [
    "AgentRunRecord",
    "Base",
    "DealRecord",
    "LeadRecord",
    "async_session_factory",
    "get_db",
]
