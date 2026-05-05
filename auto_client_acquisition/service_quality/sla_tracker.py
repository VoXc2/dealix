"""Per-service SLA reader — uses the YAML matrix as source of truth."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.self_growth_os.service_activation_matrix import (
    load_matrix,
)


@dataclass(frozen=True)
class SLA:
    service_id: str
    sla_text: str
    name_ar: str
    name_en: str
    status: str
    bundle: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "sla_text": self.sla_text,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "status": self.status,
            "bundle": self.bundle,
            "notes": self.notes,
        }


def get_sla(service_id: str) -> SLA:
    matrix = load_matrix()
    for svc in matrix.get("services", []) or []:
        if svc.get("service_id") == service_id:
            return SLA(
                service_id=service_id,
                sla_text=str(svc.get("sla", "—")),
                name_ar=str(svc.get("name_ar", "")),
                name_en=str(svc.get("name_en", "")),
                status=str(svc.get("status", "target")),
                bundle=str(svc.get("bundle", "unknown")),
                notes=(
                    "SLA is honored only when service status is `live` or "
                    "`pilot`; partial/target services have a documented "
                    "SLA but real customers should be told it's a target, "
                    "not a commitment."
                ),
            )
    raise KeyError(f"unknown service_id: {service_id}")


def list_slas() -> list[dict[str, Any]]:
    matrix = load_matrix()
    out: list[dict[str, Any]] = []
    for svc in matrix.get("services", []) or []:
        out.append({
            "service_id": svc.get("service_id"),
            "name_ar": svc.get("name_ar", ""),
            "name_en": svc.get("name_en", ""),
            "sla_text": svc.get("sla", "—"),
            "status": svc.get("status", "target"),
            "bundle": svc.get("bundle", "unknown"),
        })
    return out
