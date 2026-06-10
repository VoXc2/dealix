"""contract_status — record whether a Wave 4 contract is satisfied."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade.schemas import ContractStatus


def contract_status(
    *,
    name: str,
    available: bool,
    degraded: bool = False,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    return ContractStatus(
        name=name,
        available=available,
        degraded=degraded,
        blockers=blockers or [],
    ).model_dump(mode="json")
