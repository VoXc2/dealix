"""Permanent regression: no privileged secret may ship to the browser bundle.

Scans apps/web (the deployed public web source) for NEXT_PUBLIC_* env
references that would inline privileged/admin/private credentials into
client JS at build time, and for high-entropy secret literals in
browser-bundled source. The ops admin key must only ever arrive via the
founder's manual useAdminKey input (localStorage), never via env.
"""

from __future__ import annotations

import re
from pathlib import Path

WEB_ROOT = Path(__file__).resolve().parents[2] / "apps" / "web"

FORBIDDEN_ENV_PATTERNS = [
    re.compile(r"NEXT_PUBLIC_\w*(ADMIN|SECRET|PRIVATE|PRIVILEGED)\w*", re.I),
]

BUNDLED_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}

EXCLUDED_DIRS = {"node_modules", ".next", "dist", "build", "coverage"}


def scan_forbidden_env_refs() -> list[tuple[Path, int, str]]:
    hits: list[tuple[Path, int, str]] = []
    for path in WEB_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in BUNDLED_SUFFIXES:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_ENV_PATTERNS:
            for i, line in enumerate(text.splitlines(), start=1):
                if pattern.search(line):
                    hits.append((path, i, line.strip()))
    return hits


def test_no_privileged_next_public_env_refs_in_public_web() -> None:
    hits = scan_forbidden_env_refs()
    assert not hits, (
        "Privileged NEXT_PUBLIC_* env reference(s) found in apps/web "
        "(would inline a secret into the browser bundle if ever set): "
        + "; ".join(f"{p}:{n}: {line[:120]}" for p, n, line in hits)
    )


def test_ops_admin_key_arrives_only_via_manual_input() -> None:
    """The admin-key gate must be localStorage/manual, never env-baked."""
    hook = WEB_ROOT / "hooks" / "useAdminKey.ts"
    assert hook.exists(), "useAdminKey.ts must remain the canonical admin-key gate"
    text = hook.read_text(encoding="utf-8")
    assert "localStorage" in text, "admin key gate must persist via localStorage"
    for pattern in FORBIDDEN_ENV_PATTERNS:
        assert not pattern.search(text), (
            f"useAdminKey must not read env: {pattern.pattern}"
        )


def test_no_secret_literals_in_lib_layer() -> None:
    """High-entropy literal keys must not sit in shared browser lib code."""
    lib = WEB_ROOT / "lib"
    assert lib.exists()
    hexish = re.compile(r"['\"]([A-Za-z0-9_\-]{32,})['\"]")
    sk_prefix = re.compile(r"['\"](sk-|pk_live|ghp_|xoxb-|AIza)", re.I)
    for path in lib.rglob("*.ts*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in sk_prefix.finditer(text):
            raise AssertionError(f"secret-like literal in {path}: {m.group(0)}")
        for m in hexish.finditer(text):
            token = m.group(1)
            if re.fullmatch(r"[0-9A-Fa-f\-]{32,}", token):
                continue  # css-like id / uuid, not a credential
            if token.upper() == token and "_" in token:
                continue  # SCREAMING_SNAKE status/enum constant
            if token.lower() == token and ("_" in token or token.isalpha()):
                continue  # plain lowercase snake_case identifier / word
            if token.lower().startswith(("http", "api/", "dealix")):
                continue
            raise AssertionError(
                f"possible high-entropy literal in {path}: {token[:16]}..."
            )
