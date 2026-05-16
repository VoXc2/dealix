"""CLI helper to run the Dealix final scale audit from JSON input."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from auto_client_acquisition.scale_os.scale_dominance_audit import (
    FinalScaleInputs,
    report_as_dict,
    run_final_scale_test,
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python scripts/run_scale_dominance_audit.py <input.json>")
        return 1

    input_path = Path(sys.argv[1])
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    inputs = FinalScaleInputs(**payload)
    report = run_final_scale_test(inputs)
    print(json.dumps(report_as_dict(report), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
