"""Shared test helpers. Makes the safety-check brain importable under pytest or run_all."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import client_revenue_delivery_check as chk  # noqa: E402

DATA = chk.DATA
decide = chk.decide
find_secret_like = chk.find_secret_like
find_unmasked_pii = chk.find_unmasked_pii
load_jsonl = chk.load_jsonl
load_json = chk.load_json
valid_product_ids = chk.valid_product_ids
