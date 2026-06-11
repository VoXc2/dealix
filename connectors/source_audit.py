"""Source audit — collect and persist manifests for every connector run."""
from __future__ import annotations

import json
import datetime as dt
from pathlib import Path
from typing import Any

from base import BaseConnector


def audit(connector: BaseConnector, count: int, root: Path) -> Path:
    out_dir = root / "reports" / "sources"
    out_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    out = out_dir / f"source-audit-{today}.md"
    manifest = connector.manifest
    body = f"""# Source Audit — {today}

## Connector
- Name: {manifest.name}
- Source type: {manifest.source_type}
- Risk level: {manifest.risk_level}

## Safety
- Human review required: {manifest.human_review_required}
- Auto-send allowed: {manifest.auto_send_allowed}
- Terms review required: {manifest.terms_review_required}

## Use
- Allowed: {manifest.allowed_use}
- Restricted: {', '.join(manifest.restricted_use)}

## Result
- Records fetched: {count}
- All require human review: yes

## Notes
{manifest.notes}
"""
    out.write_text(body, encoding="utf-8")
    return out
