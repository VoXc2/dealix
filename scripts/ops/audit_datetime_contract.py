"""Audit ORM datetime declarations for UTC/default timezone mismatches.

This is a read-only static audit. It never imports application modules, opens a
database connection, or changes schema/data. The primary risk class is a
UTC-aware Python default (``utcnow``) written into SQLAlchemy ``DateTime`` that
does not explicitly opt into ``timezone=True``. PostgreSQL maps that declaration
to ``TIMESTAMP WITHOUT TIME ZONE`` and asyncpg rejects aware datetime values.

The audit handles both explicit ``DateTime(...)`` declarations and SQLAlchemy 2
annotation-inferred declarations such as ``Mapped[datetime] = mapped_column(...)``.
The audit intentionally reports rather than silently rewriting models. #1084
owns the repository-wide contract decision and any migration/backfill.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATTERNS = ("models.py", "models_*.py")
UTC_DEFAULT_NAMES = {"utcnow"}
COLUMN_CALL_NAMES = {"Column", "mapped_column"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    field: str
    column_factory: str
    datetime_source: str
    timezone_aware_column: bool
    utc_default: bool
    utc_onupdate: bool
    risk: str


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _field_name(node: ast.Assign | ast.AnnAssign) -> str:
    target: ast.AST
    if isinstance(node, ast.Assign):
        target = node.targets[0] if node.targets else ast.Name(id="<unknown>")
    else:
        target = node.target
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return "<unknown>"


def _uses_named_callable(node: ast.AST | None, names: set[str]) -> bool:
    if node is None:
        return False
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and child.id in names:
            return True
        if isinstance(child, ast.Attribute) and child.attr in names:
            return True
    return False


def _annotation_mentions_datetime(annotation: ast.AST | None) -> bool:
    if annotation is None:
        return False
    for node in ast.walk(annotation):
        if isinstance(node, ast.Name) and node.id == "datetime":
            return True
        if isinstance(node, ast.Attribute) and node.attr == "datetime":
            return True
    return False


def _datetime_contract(
    call: ast.Call,
    annotation: ast.AST | None,
) -> tuple[bool, bool, str]:
    """Return (is_datetime_column, timezone_true, declaration_source)."""
    found_explicit_datetime = False
    timezone_true = False
    for node in ast.walk(call):
        if (
            (isinstance(node, ast.Name) and node.id == "DateTime")
            or (isinstance(node, ast.Attribute) and node.attr == "DateTime")
        ):
            found_explicit_datetime = True
        if isinstance(node, ast.Call) and _call_name(node.func) == "DateTime":
            found_explicit_datetime = True
            for kw in node.keywords:
                if kw.arg == "timezone" and isinstance(kw.value, ast.Constant):
                    timezone_true = kw.value.value is True

    if found_explicit_datetime:
        return True, timezone_true, "explicit_datetime"
    if _annotation_mentions_datetime(annotation):
        # SQLAlchemy's default annotation mapping for Python datetime does not
        # itself prove timezone=True. Treat it as naive until explicitly typed.
        return True, False, "annotation_inferred_datetime"
    return False, False, "not_datetime"


def audit_source(source: str, path: str = "<memory>") -> list[Finding]:
    tree = ast.parse(source, filename=path)
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Call):
            continue
        factory = _call_name(value.func)
        if factory not in COLUMN_CALL_NAMES:
            continue
        annotation = node.annotation if isinstance(node, ast.AnnAssign) else None
        is_datetime, timezone_true, datetime_source = _datetime_contract(
            value, annotation
        )
        if not is_datetime:
            continue

        keywords = {kw.arg: kw.value for kw in value.keywords if kw.arg}
        utc_default = _uses_named_callable(keywords.get("default"), UTC_DEFAULT_NAMES)
        utc_onupdate = _uses_named_callable(keywords.get("onupdate"), UTC_DEFAULT_NAMES)
        if not utc_default and not utc_onupdate:
            continue

        risk = "ok_timezone_aware" if timezone_true else "aware_default_into_naive_timestamp"
        findings.append(
            Finding(
                path=path,
                line=getattr(node, "lineno", 0),
                field=_field_name(node),
                column_factory=factory,
                datetime_source=datetime_source,
                timezone_aware_column=timezone_true,
                utc_default=utc_default,
                utc_onupdate=utc_onupdate,
                risk=risk,
            )
        )
    return findings


def model_files(root: Path = ROOT) -> list[Path]:
    db = root / "db"
    files: set[Path] = set()
    for pattern in MODEL_PATTERNS:
        files.update(db.glob(pattern))
    return sorted(path for path in files if path.is_file())


def audit_files(paths: Iterable[Path], root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        findings.extend(audit_source(path.read_text(encoding="utf-8"), rel))
    return sorted(findings, key=lambda item: (item.path, item.line, item.field))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fail-on-risk",
        action="store_true",
        help="Exit non-zero when aware-default/naive-column risks are present.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()

    files = model_files()
    findings = audit_files(files)
    risky = [item for item in findings if item.risk != "ok_timezone_aware"]
    payload = {
        "files_scanned": len(files),
        "utc_datetime_columns": len(findings),
        "risky_columns": len(risky),
        "timezone_aware_columns": len(findings) - len(risky),
        "findings": [asdict(item) for item in findings],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            "DATETIME_CONTRACT_AUDIT "
            f"files={payload['files_scanned']} "
            f"utc_columns={payload['utc_datetime_columns']} "
            f"risky={payload['risky_columns']} "
            f"timezone_aware={payload['timezone_aware_columns']}"
        )
        for item in findings:
            marker = "RISK" if item.risk != "ok_timezone_aware" else "OK"
            print(
                f"{marker} {item.path}:{item.line} field={item.field} "
                f"source={item.datetime_source} "
                f"timezone={item.timezone_aware_column} "
                f"default={item.utc_default} onupdate={item.utc_onupdate}"
            )

    if args.fail_on_risk and risky:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
