#!/usr/bin/env python3
"""Verify Dealix enterprise execution architecture contract."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class VerificationResult:
    name: str
    ok: bool
    detail: str


def _read_manifest(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Manifest not found: {path}")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError("Manifest must be a YAML mapping")
    return loaded


def _check_directories(repo: Path, rel_paths: Iterable[str]) -> list[VerificationResult]:
    results: list[VerificationResult] = []
    for rel_path in rel_paths:
        target = repo / rel_path
        ok = target.is_dir()
        results.append(
            VerificationResult(
                name=f"dir:{rel_path}",
                ok=ok,
                detail="present" if ok else "missing",
            )
        )
    return results


def _check_files(repo: Path, rel_paths: Iterable[str]) -> list[VerificationResult]:
    results: list[VerificationResult] = []
    for rel_path in rel_paths:
        target = repo / rel_path
        ok = target.is_file()
        results.append(
            VerificationResult(
                name=f"file:{rel_path}",
                ok=ok,
                detail="present" if ok else "missing",
            )
        )
    return results


def _check_content_rules(repo: Path, rules: dict[str, list[str]]) -> list[VerificationResult]:
    results: list[VerificationResult] = []
    for rel_path, required_tokens in rules.items():
        target = repo / rel_path
        if not target.is_file():
            results.append(
                VerificationResult(
                    name=f"content:{rel_path}",
                    ok=False,
                    detail="file missing",
                )
            )
            continue
        content = target.read_text(encoding="utf-8")
        missing = [token for token in required_tokens if token not in content]
        if missing:
            results.append(
                VerificationResult(
                    name=f"content:{rel_path}",
                    ok=False,
                    detail=f"missing tokens: {', '.join(missing)}",
                )
            )
            continue
        results.append(
            VerificationResult(
                name=f"content:{rel_path}",
                ok=True,
                detail="tokens present",
            )
        )
    return results


def run_verification(repo: Path, manifest_path: Path) -> tuple[bool, list[VerificationResult]]:
    manifest = _read_manifest(manifest_path)
    required_directories = manifest.get("required_directories") or []
    required_files = manifest.get("required_files") or []
    content_rules = manifest.get("content_rules") or {}

    if not isinstance(required_directories, list):
        raise ValueError("required_directories must be a list")
    if not isinstance(required_files, list):
        raise ValueError("required_files must be a list")
    if not isinstance(content_rules, dict):
        raise ValueError("content_rules must be a mapping")

    results: list[VerificationResult] = []
    results.extend(_check_directories(repo, required_directories))
    results.extend(_check_files(repo, required_files))
    results.extend(_check_content_rules(repo, content_rules))

    ok = all(result.ok for result in results)
    return ok, results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="readiness/execution_architecture_manifest.yaml",
        help="Path to execution architecture manifest relative to repository root.",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    manifest_path = (repo / args.manifest).resolve()

    try:
        ok, results = run_verification(repo, manifest_path)
    except Exception as exc:  # pragma: no cover - defensive runner behavior
        print(f"EXECUTION_ARCH_VERIFICATION_ERROR={exc}")
        print("DEALIX_EXECUTION_ARCH_READY=false")
        return 1

    for result in results:
        print(f"{result.name}={'ok' if result.ok else 'fail'} ({result.detail})")

    print(f"DEALIX_EXECUTION_ARCH_READY={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
