#!/usr/bin/env python3
"""Backup verification script (W5.3).

Verifies that the most recent DB backup in S3 is:
  1. Present (≥ 1 object under the configured prefix)
  2. Fresh (last-modified < BACKUP_MAX_AGE_HOURS, default 2)
  3. Non-empty (size > BACKUP_MIN_SIZE_BYTES, default 1 MiB)
  4. Restorable (optional: download + pg_restore --list, runs only with --restore-check)

Used by:
  - Manual operator check before any risky DB migration
  - Cron job (suggested: every 2h, alert on failure)
  - deploy_runbook.md Phase 6 "before alembic downgrade" gate

Env vars (read-only, no writes):
  BACKUP_S3_BUCKET            (required)
  BACKUP_S3_PREFIX            (default: dealix/hourly)
  AWS_DEFAULT_REGION          (default: me-south-1)
  BACKUP_MAX_AGE_HOURS        (default: 2)
  BACKUP_MIN_SIZE_BYTES       (default: 1048576 = 1 MiB)

Exit codes:
  0  backup verified fresh + non-empty
  1  backup missing or stale or too small
  2  S3 access error or AWS misconfigured
  3  --restore-check failed (only when that flag is set)

Usage:
  python scripts/verify_backup.py
  python scripts/verify_backup.py --json
  python scripts/verify_backup.py --restore-check  # download + pg_restore --list
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time


def _verify(verbose: bool, json_mode: bool) -> tuple[int, dict[str, object]]:
    bucket = os.environ.get("BACKUP_S3_BUCKET")
    if not bucket:
        return 2, {"error": "BACKUP_S3_BUCKET not set"}

    prefix = os.environ.get("BACKUP_S3_PREFIX", "dealix/hourly")
    max_age_h = int(os.environ.get("BACKUP_MAX_AGE_HOURS", "2"))
    min_size = int(os.environ.get("BACKUP_MIN_SIZE_BYTES", str(1024 * 1024)))
    region = os.environ.get("AWS_DEFAULT_REGION", "me-south-1")

    try:
        import boto3  # type: ignore
        from botocore.exceptions import BotoCoreError, ClientError  # type: ignore
    except ImportError:
        return 2, {"error": "boto3 not installed (pip install boto3)"}

    try:
        s3 = boto3.client("s3", region_name=region)
    except Exception as exc:
        return 2, {"error": f"boto3 client init failed: {exc}"}

    # Paginate full prefix — mirrors preflight_check.py R10 fix to not miss
    # newer objects buried deeper in the listing.
    latest = None
    obj_count = 0
    try:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix + "/"):
            for obj in page.get("Contents") or []:
                obj_count += 1
                if latest is None or obj["LastModified"] > latest["LastModified"]:
                    latest = obj
    except (BotoCoreError, ClientError) as exc:
        return 2, {"error": f"S3 list failed: {exc}"}

    if latest is None:
        return 1, {
            "status": "FAIL",
            "reason": "no objects found under prefix",
            "bucket": bucket,
            "prefix": prefix,
        }

    age_sec = time.time() - latest["LastModified"].timestamp()
    age_h = age_sec / 3600
    size_bytes = int(latest["Size"])

    findings = {
        "bucket": bucket,
        "prefix": prefix,
        "object_count": obj_count,
        "latest_key": latest["Key"],
        "latest_age_hours": round(age_h, 2),
        "latest_age_minutes": round(age_sec / 60, 1),
        "latest_size_bytes": size_bytes,
        "latest_size_mib": round(size_bytes / (1024 * 1024), 2),
        "thresholds": {
            "max_age_hours": max_age_h,
            "min_size_bytes": min_size,
        },
    }

    if age_h > max_age_h:
        findings["status"] = "FAIL"
        findings["reason"] = f"latest backup is {age_h:.1f}h old (max {max_age_h}h)"
        return 1, findings

    if size_bytes < min_size:
        findings["status"] = "FAIL"
        findings["reason"] = f"latest backup is {size_bytes} bytes (min {min_size})"
        return 1, findings

    findings["status"] = "PASS"
    findings["reason"] = "fresh and non-empty"
    return 0, findings


def _restore_check(findings: dict[str, object]) -> tuple[int, dict[str, object]]:
    """Download the latest backup and run pg_restore --list to verify integrity.
    Requires pg_restore on PATH. Does NOT actually restore to a database."""
    if shutil.which("pg_restore") is None:
        return 3, {"error": "pg_restore not on PATH (apt install postgresql-client)"}

    bucket = findings["bucket"]
    key = findings["latest_key"]

    try:
        import boto3  # type: ignore
        s3 = boto3.client("s3", region_name=os.environ.get("AWS_DEFAULT_REGION", "me-south-1"))
    except Exception as exc:
        return 3, {"error": f"boto3 init failed: {exc}"}

    with tempfile.NamedTemporaryFile(suffix=".dump", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        s3.download_file(bucket, key, tmp_path)
        result = subprocess.run(
            ["pg_restore", "--list", tmp_path],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return 3, {
                "error": "pg_restore --list failed",
                "stderr": result.stderr[:500],
            }
        return 0, {
            "restore_check": "passed",
            "toc_entries": result.stdout.count("\n"),
        }
    except Exception as exc:
        return 3, {"error": f"restore check failed: {exc}"}
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="JSON output only")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--restore-check", action="store_true",
                   help="download + run pg_restore --list (requires pg_restore on PATH)")
    args = p.parse_args()

    exit_code, findings = _verify(args.verbose, args.json)

    if args.restore_check and exit_code == 0:
        restore_code, restore_findings = _restore_check(findings)
        findings.update(restore_findings)
        if restore_code != 0:
            exit_code = restore_code

    if args.json:
        print(json.dumps(findings, indent=2, ensure_ascii=False, default=str))
    else:
        status = findings.get("status", "?")
        reason = findings.get("reason", "")
        print(f"[{status}] {reason}")
        if args.verbose or status != "PASS":
            for k, v in findings.items():
                if k in ("status", "reason"):
                    continue
                print(f"  {k}: {v}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
