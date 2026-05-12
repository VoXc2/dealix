"""Pre-deploy gate: every vertical's `agents:` entry must map to a
registered skill handler. Exits 1 with a human-readable report
otherwise.

Run:
    python scripts/dev/check_vertical_truth.py

Wire into CI as a fast pre-merge check so claimed-but-unimplemented
agents never reach a customer-facing brochure.
"""

from __future__ import annotations

import sys

# Side-effect imports populate the handler registry.
from dealix.agents.skills import handlers_data, handlers_llm  # noqa: F401
from dealix.agents.skills.handlers import registered_ids
from dealix.verticals import list_all


def main() -> int:
    registered = set(registered_ids())
    rows: list[tuple[str, list[str], list[str]]] = []
    for v in list_all():
        present = [a for a in v.agents if a in registered]
        missing = [a for a in v.agents if a not in registered]
        rows.append((v.id, present, missing))

    print(f"Registered skill handlers: {len(registered)}")
    print()
    print(f"{'Vertical':<22}  {'Present':<6}  {'Missing':<7}")
    print("-" * 50)
    bad = 0
    for vid, present, missing in rows:
        flag = "OK" if not missing else "FAIL"
        print(f"{vid:<22}  {len(present):<6}  {len(missing):<7}  [{flag}]")
        if missing:
            print(f"  ↳ missing: {', '.join(missing)}")
            bad += 1
    print()
    if bad:
        print(f"❌  {bad} vertical(s) reference unregistered agents.")
        return 1
    print("✅  Every vertical's claimed agents have registered handlers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
