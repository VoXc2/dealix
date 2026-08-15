"""Read-only audit of runtime code that mixes current-time helpers with model timestamps.

The #1084 write fix must not silently change ORM read semantics. This scanner
finds arithmetic/comparisons where an aware-current-time expression (``utcnow``
or ``datetime.now(UTC)``) is combined with a timestamp-like attribute such as
``created_at``/``updated_at``/``*_at``. It is intentionally conservative and
reports candidates for review; it does not rewrite code or import the app.
"""

from __future__ import annotations

import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_PARTS = {".git", ".venv", "venv", "node_modules", "dist", "build"}


@dataclass(frozen=True)
class Candidate:
    path: str
    line: int
    operation: str
    current_time: str
    timestamp_attributes: tuple[str, ...]


def _call_label(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Call):
        return None
    func = node.func
    if isinstance(func, ast.Name) and func.id == "utcnow":
        return "utcnow()"
    if isinstance(func, ast.Attribute):
        if func.attr == "utcnow":
            return "*.utcnow()"
        if func.attr == "now":
            # datetime.now(UTC) / datetime.now(timezone.utc)
            args = " ".join(ast.unparse(arg) for arg in node.args)
            if "UTC" in args or "timezone.utc" in args:
                return "datetime.now(UTC)"
    return None


def _current_times(node: ast.AST) -> list[str]:
    labels: list[str] = []
    for child in ast.walk(node):
        label = _call_label(child)
        if label:
            labels.append(label)
    return labels


def _timestamp_attrs(node: ast.AST) -> list[str]:
    attrs: list[str] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Attribute):
            continue
        name = child.attr
        if name.endswith("_at") or name in {
            "created_at",
            "updated_at",
            "deleted_at",
            "due_at",
            "completed_at",
            "sent_at",
            "started_at",
            "ended_at",
            "expires_at",
            "last_login",
            "last_seen",
        }:
            attrs.append(name)
    return attrs


def audit_source(source: str, path: str = "<memory>") -> list[Candidate]:
    tree = ast.parse(source, filename=path)
    findings: list[Candidate] = []
    interesting = (ast.BinOp, ast.Compare)
    for node in ast.walk(tree):
        if not isinstance(node, interesting):
            continue
        current = _current_times(node)
        attrs = _timestamp_attrs(node)
        if not current or not attrs:
            continue
        operation = type(node).__name__
        if isinstance(node, ast.BinOp):
            operation += f":{type(node.op).__name__}"
        elif isinstance(node, ast.Compare):
            operation += ":" + ",".join(type(op).__name__ for op in node.ops)
        findings.append(
            Candidate(
                path=path,
                line=getattr(node, "lineno", 0),
                operation=operation,
                current_time=current[0],
                timestamp_attributes=tuple(sorted(set(attrs))),
            )
        )
    return findings


def python_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.py"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    findings: list[Candidate] = []
    parse_errors: list[str] = []
    files = python_files()
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            findings.extend(audit_source(path.read_text(encoding="utf-8"), rel))
        except (SyntaxError, UnicodeDecodeError) as exc:
            parse_errors.append(f"{rel}: {exc}")

    by_path: dict[str, int] = {}
    for item in findings:
        by_path[item.path] = by_path.get(item.path, 0) + 1

    payload = {
        "python_files_scanned": len(files),
        "candidate_operations": len(findings),
        "files_with_candidates": len(by_path),
        "parse_errors": parse_errors,
        "counts_by_file": dict(sorted(by_path.items(), key=lambda kv: (-kv[1], kv[0]))),
        "findings": [asdict(item) for item in findings],
        "interpretation": (
            "Candidates require review. A non-zero count is evidence that globally "
            "changing ORM result values from naive UTC to aware UTC can break existing arithmetic."
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
