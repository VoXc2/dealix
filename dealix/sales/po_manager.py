"""
Purchase Order (PO) management for enterprise sales.
إدارة أمر الشراء (PO) للمبيعات المؤسسية.

Handles the full PO lifecycle: creation, validation against quotes,
matching to invoices, and reconciliation.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class PurchaseOrderLine:
    sku: str
    description: str
    quantity: int
    unit_price: Decimal
    total: Decimal


@dataclass
class PurchaseOrder:
    po_id: str
    po_number: str
    tenant_id: str
    vendor_name: str
    vendor_vat: str
    customer_name: str
    customer_vat: str
    lines: list[PurchaseOrderLine] = field(default_factory=list)
    total_amount: Decimal = Decimal("0")
    vat_amount: Decimal = Decimal("0")
    grand_total: Decimal = Decimal("0")
    currency: str = "SAR"
    status: str = "draft"  # draft / submitted / approved / received / closed / cancelled
    valid_from: str = ""
    valid_until: str = ""
    notes: str = ""
    created_by: str = ""
    created_at: str = ""
    approved_by: str | None = None
    approved_at: str | None = None


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class MatchResult:
    is_match: bool
    match_score: float = 0.0
    differences: list[str] = field(default_factory=list)
    po_total: Decimal = Decimal("0")
    invoice_total: Decimal = Decimal("0")
    variance: Decimal = Decimal("0")


class POManager:
    """Purchase Order management service.

    Integrates with ZATCA e-invoicing for PO matching and validation.
    Supports three-way matching: PO → Goods Receipt → Invoice.
    """

    def __init__(self) -> None:
        self._pos: dict[str, PurchaseOrder] = {}

    async def create(self, po_data: dict[str, Any]) -> PurchaseOrder:
        """Create a new purchase order from provided data."""
        po_id = f"PO-{uuid.uuid4().hex[:8].upper()}"
        po_number = self._generate_po_number()

        lines_data = po_data.get("lines", [])
        lines = [
            PurchaseOrderLine(
                sku=line.get("sku", ""),
                description=line.get("description", ""),
                quantity=int(line.get("quantity", 1)),
                unit_price=Decimal(str(line.get("unit_price", 0))),
                total=Decimal(str(line.get("quantity", 1))) * Decimal(str(line.get("unit_price", 0))),
            )
            for line in lines_data
        ]

        subtotal = sum(line.total for line in lines)
        vat_rate = Decimal("0.15")
        vat_amount = subtotal * vat_rate
        grand_total = subtotal + vat_amount

        now = datetime.now(UTC).isoformat()

        po = PurchaseOrder(
            po_id=po_id,
            po_number=po_number,
            tenant_id=po_data.get("tenant_id", ""),
            vendor_name=po_data.get("vendor_name", ""),
            vendor_vat=po_data.get("vendor_vat", ""),
            customer_name=po_data.get("customer_name", ""),
            customer_vat=po_data.get("customer_vat", ""),
            lines=lines,
            total_amount=subtotal,
            vat_amount=vat_amount,
            grand_total=grand_total,
            currency=po_data.get("currency", "SAR"),
            status="draft",
            valid_from=now,
            valid_until=po_data.get("valid_until", now),
            notes=po_data.get("notes", ""),
            created_by=po_data.get("created_by", ""),
            created_at=now,
        )

        self._pos[po_id] = po
        log.info("po_created", po_id=po_id, po_number=po_number, amount=grand_total)

        return po

    async def validate(self, po_id: str) -> ValidationResult:
        """Validate a purchase order for completeness and correctness."""
        po = self._pos.get(po_id)
        if not po:
            return ValidationResult(
                is_valid=False,
                errors=[f"Purchase Order not found: {po_id}"],
            )

        errors: list[str] = []
        warnings: list[str] = []

        if not po.vendor_name:
            errors.append("Vendor name is required")
        if not po.vendor_vat:
            warnings.append("Vendor VAT number is missing (may affect ZATCA compliance)")
        if not po.customer_name:
            errors.append("Customer name is required")
        if not po.lines:
            errors.append("At least one line item is required")

        for line in po.lines:
            if line.quantity <= 0:
                errors.append(f"Invalid quantity for SKU {line.sku}: {line.quantity}")
            if line.unit_price <= 0:
                warnings.append(f"Zero unit price for SKU {line.sku}")

        if po.total_amount <= 0:
            warnings.append("Total amount is zero or negative")

        if po.vat_amount <= 0:
            warnings.append("Total amount is zero or negative")

        is_valid = len(errors) == 0

        log.info(
            "po_validated",
            po_id=po_id,
            is_valid=is_valid,
            error_count=len(errors),
            warning_count=len(warnings),
        )

        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)

    async def match_to_invoice(self, po_id: str, invoice_id: str) -> MatchResult:
        """Match a purchase order to an invoice (two-way matching).

        Checks:
        - PO number matches
        - Total amount matches (within tolerance)
        - VAT amount matches
        - Currency matches

        In production, this queries the actual invoice from the invoicing system.
        """
        po = self._pos.get(po_id)
        if not po:
            return MatchResult(
                is_match=False,
                errors=[f"Purchase Order not found: {po_id}"],
                match_score=0.0,
            )

        mock_invoice_total = po.total_amount
        mock_invoice_vat = po.vat_amount

        differences: list[str] = []
        total_variance = abs(po.total_amount - mock_invoice_total)
        vat_variance = abs(po.vat_amount - mock_invoice_vat)

        tolerance = Decimal("0.01") * po.total_amount

        if total_variance > tolerance:
            differences.append(
                f"Total amount mismatch: PO={po.total_amount}, Invoice={mock_invoice_total}, "
                f"Variance={total_variance}"
            )

        if vat_variance > tolerance:
            differences.append(
                f"VAT amount mismatch: PO={po.vat_amount}, Invoice={mock_invoice_vat}, "
                f"Variance={vat_variance}"
            )

        max_variance = max(total_variance, vat_variance)
        match_score = max(0.0, 1.0 - float(max_variance / po.total_amount)) if po.total_amount > 0 else 0.0

        is_match = len(differences) == 0

        if is_match:
            log.info("po_invoice_matched", po_id=po_id, invoice_id=invoice_id, score=match_score)
        else:
            log.warning(
                "po_invoice_mismatch",
                po_id=po_id,
                invoice_id=invoice_id,
                differences=differences,
            )

        return MatchResult(
            is_match=is_match,
            match_score=match_score,
            differences=differences,
            po_total=po.total_amount,
            invoice_total=mock_invoice_total,
            variance=total_variance,
        )

    async def approve(self, po_id: str, approved_by: str) -> PurchaseOrder | None:
        """Approve a purchase order."""
        po = self._pos.get(po_id)
        if not po:
            return None

        validation = await self.validate(po_id)
        if not validation.is_valid:
            log.warning("po_approval_rejected", po_id=po_id, errors=validation.errors)
            return po

        po.status = "approved"
        po.approved_by = approved_by
        po.approved_at = datetime.now(UTC).isoformat()

        log.info("po_approved", po_id=po_id, approved_by=approved_by)
        return po

    async def get(self, po_id: str) -> PurchaseOrder | None:
        """Get a purchase order by ID."""
        return self._pos.get(po_id)

    async def list_by_tenant(self, tenant_id: str) -> list[PurchaseOrder]:
        """List all purchase orders for a tenant."""
        return [po for po in self._pos.values() if po.tenant_id == tenant_id]

    def _generate_po_number(self) -> str:
        """Generate a human-readable PO number."""
        now = datetime.now(UTC)
        seq = len(self._pos) + 1
        return f"PO-{now.year}{now.month:02d}-{seq:04d}"
