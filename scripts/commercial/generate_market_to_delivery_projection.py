#!/usr/bin/env python3
"""Generate/check an explicit non-sensitive UI projection of the canonical catalog."""
import argparse
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('mtd', ROOT / 'auto_client_acquisition/service_catalog/market_to_delivery.py')
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
path = ROOT / 'apps/web/public/market-to-delivery-catalog.json'
expected = json.dumps(m.public_projection(), ensure_ascii=False, separators=(',', ':')) + '\n'
if args.check:
    if not path.is_file() or json.loads(path.read_text(encoding='utf-8')) != m.public_projection():
        raise SystemExit('MARKET_TO_DELIVERY_PROJECTION=FAIL')
else:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(expected, encoding='utf-8')
print('MARKET_TO_DELIVERY_PROJECTION=PASS')
