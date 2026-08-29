#!/usr/bin/env python3
"""Fail-closed Google GenAI dependency/consumer contract for Dealix.

The retired `google-generativeai` package must never return. The current
`google-genai` SDK may be introduced only together with an actual runtime
consumer and a reviewed capability/migration change; dormant SDK surface is not
kept merely for optionality.
"""

from __future__ import annotations

import ast
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
REQUIREMENTS = ROOT / "requirements.txt"
RUNTIME_ROOTS = (
    "core",
    "auto_client_acquisition",
    "autonomous_growth",
    "integrations",
    "api",
    "dealix",
    "platform_core",
)
LEGACY_DEP = "google-generativeai"
CURRENT_DEP = "google-genai"


def _normalized_dependencies() -> set[str]:
    with PYPROJECT.open("rb") as handle:
        payload = tomllib.load(handle)
    raw = payload["project"]["dependencies"]
    names: set[str] = set()
    for dep in raw:
        token = str(dep).strip().split(";", 1)[0].strip()
        for separator in ("[", "<", ">", "=", "!", "~", " "):
            token = token.split(separator, 1)[0]
        if token:
            names.add(token.lower().replace("_", "-"))
    return names


def _requirements_names() -> set[str]:
    names: set[str] = set()
    for raw_line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        token = line.split(";", 1)[0].strip()
        for separator in ("[", "<", ">", "=", "!", "~", " "):
            token = token.split(separator, 1)[0]
        if token:
            names.add(token.lower().replace("_", "-"))
    return names


def _runtime_files() -> list[Path]:
    files: list[Path] = []
    for relative in RUNTIME_ROOTS:
        root = ROOT / relative
        if not root.exists():
            continue
        files.extend(
            path
            for path in root.rglob("*.py")
            if not any(part in {".venv", "venv", "tests", "test", "migrations", "__pycache__"} for part in path.parts)
        )
    return sorted(set(files))


def _consumer_state() -> tuple[list[str], list[str]]:
    legacy_imports: list[str] = []
    current_imports: list[str] = []

    for path in _runtime_files():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            raise SystemExit(f"GOOGLE_GENAI_DEPENDENCY_CONTRACT=FAIL\nREASON=cannot parse {path.relative_to(ROOT)}: {exc}") from exc

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    if name == "google.generativeai" or name.startswith("google.generativeai."):
                        legacy_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:{name}")
                    if name == "google.genai" or name.startswith("google.genai."):
                        current_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:{name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imported = {alias.name for alias in node.names}
                if module == "google.generativeai" or module.startswith("google.generativeai."):
                    legacy_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:from {module}")
                if module == "google.genai" or module.startswith("google.genai."):
                    current_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:from {module}")
                if module == "google" and "generativeai" in imported:
                    legacy_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:from google import generativeai")
                if module == "google" and "genai" in imported:
                    current_imports.append(f"{path.relative_to(ROOT)}:{node.lineno}:from google import genai")

    return legacy_imports, current_imports


def main() -> int:
    pyproject_deps = _normalized_dependencies()
    requirements_deps = _requirements_names()
    legacy_imports, current_imports = _consumer_state()

    if LEGACY_DEP in pyproject_deps or LEGACY_DEP in requirements_deps:
        raise SystemExit("GOOGLE_GENAI_DEPENDENCY_CONTRACT=FAIL\nREASON=legacy google-generativeai dependency is present")
    if legacy_imports:
        raise SystemExit(f"GOOGLE_GENAI_DEPENDENCY_CONTRACT=FAIL\nREASON=legacy runtime imports: {legacy_imports}")

    has_current_dep = CURRENT_DEP in pyproject_deps or CURRENT_DEP in requirements_deps
    has_current_consumer = bool(current_imports)
    if has_current_dep != has_current_consumer:
        state = f"dependency={int(has_current_dep)} consumer={int(has_current_consumer)} imports={current_imports}"
        raise SystemExit(
            "GOOGLE_GENAI_DEPENDENCY_CONTRACT=FAIL\n"
            "REASON=google-genai dependency and runtime consumer must enter together through a reviewed migration; "
            + state
        )

    print("GOOGLE_GENAI_DEPENDENCY_CONTRACT=PASS")
    print("LEGACY_GOOGLE_GENERATIVEAI_DEPENDENCY=0")
    print("LEGACY_GOOGLE_GENERATIVEAI_IMPORT=0")
    print(f"ACTIVE_GOOGLE_GENAI_CONSUMER={int(has_current_consumer)}")
    print(f"ACTIVE_GOOGLE_GENAI_DEPENDENCY={int(has_current_dep)}")
    print("FUTURE_GEMINI_REENTRY=CAPABILITY_INTAKE_PLUS_REVIEWED_GOOGLE_GENAI_ADAPTER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
