"""Dealix internal dogfooding war room — same pipeline as customer War Room."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.paths import DEALIX_INTERNAL_WAR_ROOM_CSV, REPO_ROOT
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets


def build_dogfooding_payload(*, top_n: int = 10) -> dict[str, Any]:
    rows = load_targets(DEALIX_INTERNAL_WAR_ROOM_CSV)
    war = build_war_room_today(rows, top_n=top_n)
    return {
        "kind": "dealix_dogfooding_war_room",
        "source_csv": str(DEALIX_INTERNAL_WAR_ROOM_CSV.relative_to(REPO_ROOT)).replace(
            "\\", "/"
        ),
        "doc": "docs/ops/DEALIX_DOGFOODING_WAR_ROOM_AR.md",
        "policy_ar": "معالم داخلية — لا إرسال خارجي.",
        **war,
    }
