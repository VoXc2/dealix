"""
Conftest for intelligence tests — isolated from the main app conftest.
Avoids importing app.main (which needs database connections).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure backend/ is on path
BACKEND = Path(__file__).parent.parent.parent
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
