from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db.datetime_types import UTCNaiveDateTime
from db.models import TenantRecord
from scripts.ops.audit_datetime_contract import audit_source


class UnrelatedBase(DeclarativeBase):
    pass


class UnrelatedTimestampProbe(UnrelatedBase):
    __tablename__ = "_unrelated_datetime_listener_probe"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]


def test_audit_flags_aware_utc_default_on_naive_datetime() -> None:
    source = """
from sqlalchemy import Column, DateTime
from core.utils import utcnow
created_at = Column(DateTime, default=utcnow)
"""
    findings = audit_source(source)
    assert len(findings) == 1
    assert findings[0].risk == "aware_default_into_naive_timestamp"
    assert findings[0].utc_default is True
    assert findings[0].timezone_aware_column is False
    assert findings[0].datetime_source == "explicit_datetime"


def test_audit_flags_annotation_inferred_datetime_as_naive_until_explicit() -> None:
    source = """
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from core.utils import utcnow
created_at: Mapped[datetime] = mapped_column(default=utcnow)
"""
    findings = audit_source(source)
    assert len(findings) == 1
    assert findings[0].risk == "aware_default_into_naive_timestamp"
    assert findings[0].timezone_aware_column is False
    assert findings[0].datetime_source == "annotation_inferred_datetime"


def test_audit_accepts_explicit_timezone_aware_datetime() -> None:
    source = """
from sqlalchemy import Column, DateTime
from core.utils import utcnow
updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
"""
    findings = audit_source(source)
    assert len(findings) == 1
    assert findings[0].risk == "ok_timezone_aware"
    assert findings[0].utc_default is True
    assert findings[0].utc_onupdate is True
    assert findings[0].timezone_aware_column is True
    assert findings[0].datetime_source == "explicit_datetime"


def test_listener_normalizes_canonical_metadata_only() -> None:
    canonical_type = TenantRecord.__table__.c.created_at.type
    unrelated_type = UnrelatedTimestampProbe.__table__.c.created_at.type

    assert isinstance(canonical_type, UTCNaiveDateTime)
    assert isinstance(unrelated_type, DateTime)
    assert not isinstance(unrelated_type, UTCNaiveDateTime)
    assert unrelated_type.timezone is False
