"""CSV preview for account-style imports (stdlib only, deterministic)."""

from __future__ import annotations

import csv
import io
from typing import Any

from auto_client_acquisition.data_os.data_quality_score import summarize_table_quality

_MAX_BYTES = 512_000


def parse_account_csv(
    csv_text: str,
    *,
    max_rows: int = 500,
    preview_limit: int = 20,
) -> dict[str, Any]:
    if len(csv_text.encode("utf-8")) > _MAX_BYTES:
        return {"error": "csv_too_large", "max_bytes": _MAX_BYTES}

    stream = io.StringIO(csv_text)
    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        return {"error": "no_header_row", "rows": []}

    fieldnames = [f.strip() for f in reader.fieldnames if f]
    rows: list[dict[str, Any]] = []
    for i, row in enumerate(reader):
        if i >= max_rows:
            break
        clean = {str(k).strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
        # normalize company column
        if "company_name" not in clean and "company" in clean:
            clean["company_name"] = clean.get("company") or ""
        rows.append(clean)

    required = ("company_name", "sector", "city")
    quality = summarize_table_quality(rows, required_keys=required)

    return {
        "detected_columns": fieldnames,
        "parsed_row_count": len(rows),
        "preview_rows": rows[:preview_limit],
        "data_quality": quality,
    }
