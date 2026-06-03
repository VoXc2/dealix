from pathlib import Path
import sys

required = [
    "apps/web/app/ar/control-room/page.tsx",
    ".github/workflows/brain-control-command.yml",
    "docs/company_os/control_plane/MOBILE_CONTROL_ROOM_AR.md",
    "scripts/dealix_brain_control.py",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("MOBILE_CONTROL_ROOM=FAIL")
    for p in missing:
        print("missing=" + p)
    sys.exit(1)

print("MOBILE_CONTROL_ROOM=PASS")
for p in required:
    print("ok=" + p)
