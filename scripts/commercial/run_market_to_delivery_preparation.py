#!/usr/bin/env python3
"""Local artifact runner. No connector writes, auto-approval or live actions."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('dealix_mtd_preparation', ROOT / 'auto_client_acquisition/service_catalog/market_to_delivery.py')
assert SPEC is not None and SPEC.loader is not None
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)


def write_bundle(bundle: dict, root: Path) -> Path:
    """Private, exclusive artifact directory. A replay revalidates every byte."""
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if root.is_symlink() or root.stat().st_mode & 0o077:
        raise ValueError('output_root_must_be_private_non_symlink')
    target = root / bundle['artifact_digest']
    files = {'preparation.json': bundle, 'diagnostic.json': bundle['diagnostic'],
             'quote-draft.json': bundle['quote_draft'], 'project-cell-draft.json': bundle['project_cell_draft']}
    encoded = {name: engine.canonical_bytes(value) + b'\n' for name, value in files.items()}
    receipt = {'schema_version': 'dealix.market-to-delivery.local-receipt.v1',
               'artifact_digest': bundle['artifact_digest'], 'status': 'LOCAL_PREPARATION_ONLY',
               'files': {name: hashlib.sha256(value).hexdigest() for name, value in encoded.items()},
               'live_effects': False, 'canonical_store_ingestion': 'NOT_EXECUTED'}
    encoded['receipt.json'] = engine.canonical_bytes(receipt) + b'\n'
    try:
        target.mkdir(mode=0o700)
    except FileExistsError:
        if target.is_symlink() or not target.is_dir() or target.stat().st_mode & 0o077:
            raise ValueError('unsafe_existing_artifact')
        for name, contents in encoded.items():
            p = target / name
            if p.is_symlink() or not p.is_file() or p.stat().st_mode & 0o077 or p.read_bytes() != contents:
                raise ValueError('artifact_conflict_or_tamper')
        return target
    for name, contents in encoded.items():
        fd = os.open(target / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.input.is_symlink() or not args.input.is_file() or args.input.stat().st_size > 131072:
            raise ValueError('invalid_input_file')
        bundle = engine.prepare(json.loads(args.input.read_text(encoding='utf-8')))
        path = write_bundle(bundle, args.output_root)
    except (ValueError, OSError) as exc:
        # Never print arbitrary file contents or exception messages containing customer data.
        code = str(exc) if isinstance(exc, ValueError) and str(exc).replace('_', '').isalnum() else type(exc).__name__
        print('PREPARATION=BLOCKED\nREASON=' + code, file=sys.stderr)
        return 2
    print('PREPARATION=' + bundle['status'])
    print('ARTIFACT_DIGEST=' + bundle['artifact_digest'])
    print('OUTPUT=' + str(path))
    print('LIVE_EFFECTS=false\nCANONICAL_STORE_INGESTION=NOT_EXECUTED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
