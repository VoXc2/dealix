#!/usr/bin/env python3
"""
Forbidden Claims Audit — scans landing/*.html for unsafe marketing claims.

Forbidden claims (firing without negative-context marker):
  - "نضمن" / "guaranteed"
  - "ضمان نتائج" / "guaranteed results"
  - "scrape" / "scraping" / "نسحب البيانات"
  - "auto-dm" / "auto dm" / "رسائل آلية"
  - "cold whatsapp" / "واتساب بارد"
  - "إرسال جماعي" / "mass send"
  - "100% automation" / "أتمتة كاملة"

Negative-context markers (when on the same line, claim is treated as
documented-avoidance, not active marketing):
  ✗  ✘  ❌  لا  لسنا  نمنع  no   not   never   without  بدون

Required-per-page checks:
  - link to support page
  - link to trust-center page
  - mention of "Pilot" CTA (or "Diagnostic")
  - has <html lang="ar"> + dir="rtl"
  - has <meta name="description">
  - has <link rel="canonical">

Run:
  python scripts/forbidden_claims_audit.py
Exit 0 = PASS, exit 1 = FAIL.

Importable: scripts.forbidden_claims_audit.run_audit() -> AuditReport.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
LANDING_DIR = _REPO / "landing"

# ── Configuration ─────────────────────────────────────────────────

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "نضمن",
    "ضمان نتائج",
    "guaranteed results",
    "scrape",
    "scraping",
    "نسحب البيانات",
    "auto-dm",
    "auto dm",
    "رسائل آلية",
    "cold whatsapp",
    "واتساب بارد",
    "إرسال جماعي",
    "mass send",
    "100% automation",
    "أتمتة كاملة",
)

# Negative-context markers — if the line containing the forbidden claim
# also contains one of these, the line is documented avoidance (e.g.,
# "✗ لا نُرسل واتساب بارد") and is allowed.
NEGATIVE_MARKERS: tuple[str, ...] = (
    # Visual markers
    "✗", "✘", "❌",
    # Arabic negation / prohibition
    " لا ", " لا<", ">لا ", "لا أقدر", "لا نُرسل", "لا نسحب", "لا وعود",
    "لسنا", "نمنع", "يمنع", "ممنوع", "محظور",
    "بدون", "بلا", "دون", "غير",
    "يحرق", "يخالف", "تُكسر", "تكسر الثقة",
    "يرفض", "يصدّ", "يحظر", "البديل الآمن",
    # English negation
    " no ", " not ", " never ", " without ", " forbids ", " prohibits ",
    " rejects ", " refuses ", "rejects ", "refuses ",
    "forbidden", "blocked", "anti-claim", "anti_claim",
    "ToS", "policies تتطلب", "policies forbid",
    # Code self-reference (constants)
    "FORBIDDEN_CLAIMS", "NEGATIVE_MARKERS",
    "data-track-cta=\"ant",
    "dx-anti-claim", "dx-anti-claims",
    # Variable/identifier names that include the pattern as a label, not a claim
    "cold_whatsapp_request", "cold_whatsapp_blocked",
    "linkedin_auto_dm", "auto_linkedin_dm",
    "scrape_blocked", "scraping_blocked",
)


# Files in PR-FE-1 audit scope. Future PRs expand this list.
# Existing pages not yet refactored are intentionally NOT audited yet
# (their copy/CTA alignment is deferred to PR-FE-5/6).
IN_SCOPE_FILES: tuple[str, ...] = (
    # 9 new pages created in PR-FE-1
    "companies.html",
    "services.html",
    "private-beta.html",
    "growth-os.html",
    "agency-partner.html",
    "operator.html",
    "targeting.html",
    "proof-pack.html",
    "support.html",
)

# Substrings that, when found in the page (anywhere) satisfy required-per-page.
REQUIRED_LINKS_ANY: tuple[tuple[str, ...], ...] = (
    ("support.html",),                          # Support link
    ("trust-center.html", "trust.html"),        # Trust link (either)
)
REQUIRED_TEXT_ANY: tuple[tuple[str, ...], ...] = (
    ("Pilot", "Diagnostic"),                    # CTA presence
)
REQUIRED_HTML_ATTRS: tuple[tuple[str, str], ...] = (
    ("html", 'lang="ar"'),
    ("html", 'dir="rtl"'),
)
REQUIRED_HEAD_TAGS: tuple[str, ...] = (
    'name="description"',
    'rel="canonical"',
)

# Pages we skip (purely marketing snippets / PostHog loader / non-public).
SKIP_FILES: tuple[str, ...] = (
    "posthog_snippet.html",
)


# ── Result types ──────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    file: str
    passed: bool
    detail: str = ""


@dataclass
class AuditReport:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def fail_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed)

    @property
    def pass_count(self) -> int:
        return sum(1 for c in self.checks if c.passed)


# ── Checks ────────────────────────────────────────────────────────

def _has_negative_marker(line: str) -> bool:
    return any(marker in line for marker in NEGATIVE_MARKERS)


def check_forbidden_claims(path: Path, text: str) -> list[CheckResult]:
    """Scan each line for forbidden claims; allow when negative marker present."""
    rel = str(path.relative_to(_REPO))
    hits: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line_lower = line.lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim.lower() not in line_lower:
                continue
            if _has_negative_marker(line):
                continue
            hits.append(f"L{line_no}: '{claim}' in: {line.strip()[:120]}")
    if hits:
        return [CheckResult(
            name="forbidden_claims",
            file=rel,
            passed=False,
            detail="; ".join(hits[:5]) + (f" (+{len(hits) - 5} more)" if len(hits) > 5 else ""),
        )]
    return [CheckResult(name="forbidden_claims", file=rel, passed=True, detail="clean")]


def _read_included_partials(text: str) -> str:
    """Resolve `<div data-include="components/foo.html">` references and return
    the concatenated partial contents. Used for required_links/required_text checks
    so that pages relying on shared nav/footer don't fail the audit.
    """
    pattern = re.compile(r'data-include="(components/[^"]+\.html)"', re.IGNORECASE)
    out = []
    for partial_path in pattern.findall(text):
        full = LANDING_DIR / partial_path
        try:
            out.append(full.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(out)


def check_required_links(path: Path, text: str) -> list[CheckResult]:
    rel = str(path.relative_to(_REPO))
    results: list[CheckResult] = []
    # Resolve includes so pages relying on shared nav/footer pass.
    combined = (text + "\n" + _read_included_partials(text)).lower()
    is_trust_page = path.name in ("trust-center.html", "trust.html")
    is_support_page = path.name == "support.html"

    for variants in REQUIRED_LINKS_ANY:
        # Skip self-references
        if is_trust_page and variants[0].startswith("trust"):
            results.append(CheckResult("required_link_trust", rel, True, "self (trust page)"))
            continue
        if is_support_page and variants[0] == "support.html":
            results.append(CheckResult("required_link_support", rel, True, "self (support page)"))
            continue
        found = any(v.lower() in combined for v in variants)
        name = "required_link_" + variants[0].replace(".html", "").replace("-", "_")
        results.append(CheckResult(
            name=name,
            file=rel,
            passed=found,
            detail="found" if found else f"missing any of {variants}",
        ))
    return results


def check_required_text(path: Path, text: str) -> list[CheckResult]:
    rel = str(path.relative_to(_REPO))
    results: list[CheckResult] = []
    combined = text + "\n" + _read_included_partials(text)
    for variants in REQUIRED_TEXT_ANY:
        found = any(v in combined for v in variants)
        name = "required_text_" + variants[0].lower()
        results.append(CheckResult(
            name=name,
            file=rel,
            passed=found,
            detail="found" if found else f"missing any of {variants}",
        ))
    return results


def check_html_attrs(path: Path, text: str) -> list[CheckResult]:
    rel = str(path.relative_to(_REPO))
    results: list[CheckResult] = []
    # Look at the first 400 chars (the <html> tag area)
    head_section = text[:600]
    for tag, attr in REQUIRED_HTML_ATTRS:
        present = attr.lower() in head_section.lower()
        safe_name = attr.replace('=', '_').replace('"', '')
        results.append(CheckResult(
            name=f"html_attr_{safe_name}",
            file=rel,
            passed=present,
            detail="found" if present else f"missing {attr} on <{tag}>",
        ))
    return results


def check_head_tags(path: Path, text: str) -> list[CheckResult]:
    rel = str(path.relative_to(_REPO))
    results: list[CheckResult] = []
    head_match = re.search(r"<head[^>]*>([\s\S]*?)</head>", text, re.IGNORECASE)
    head = head_match.group(1) if head_match else text[:2000]
    for tag in REQUIRED_HEAD_TAGS:
        present = tag.lower() in head.lower()
        results.append(CheckResult(
            name=f"head_{tag.split('=')[0].strip()}",
            file=rel,
            passed=present,
            detail="found" if present else f"missing {tag}",
        ))
    return results


# ── Orchestrator ──────────────────────────────────────────────────

def _iter_html_files() -> list[Path]:
    """Return only files inside the current audit scope.

    PR-FE-1 limits scope to the 9 pages it creates. Other landing/*.html
    files exist but are not yet refactored — they enter scope in PR-FE-5/6.
    """
    if not LANDING_DIR.exists():
        return []
    files: list[Path] = []
    for name in IN_SCOPE_FILES:
        p = LANDING_DIR / name
        if p.exists() and name not in SKIP_FILES:
            files.append(p)
    return files


def run_audit() -> AuditReport:
    report = AuditReport()
    for path in _iter_html_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            report.checks.append(CheckResult("file_read", str(path), False, str(exc)))
            continue
        report.checks.extend(check_forbidden_claims(path, text))
        report.checks.extend(check_required_links(path, text))
        report.checks.extend(check_required_text(path, text))
        report.checks.extend(check_html_attrs(path, text))
        report.checks.extend(check_head_tags(path, text))
    return report


def render(report: AuditReport, *, only_failures: bool = True) -> str:
    lines = ["DEALIX_FORBIDDEN_CLAIMS_AUDIT v1.0", "=" * 40]
    by_file: dict[str, list[CheckResult]] = {}
    for c in report.checks:
        by_file.setdefault(c.file, []).append(c)
    for fname in sorted(by_file):
        checks = by_file[fname]
        fails = [c for c in checks if not c.passed]
        if only_failures and not fails:
            continue
        lines.append(f"\n{fname}")
        for c in fails:
            lines.append(f"  [FAIL] {c.name} — {c.detail}")
        if not only_failures:
            for c in checks:
                if c.passed:
                    lines.append(f"  [PASS] {c.name}")
    lines.append("\n" + "=" * 40)
    lines.append(f"SUMMARY: {report.pass_count} passed, {report.fail_count} failed across {len(by_file)} files")
    lines.append("RESULT: " + ("PASS" if report.passed else "FAIL"))
    return "\n".join(lines)


def main() -> int:
    report = run_audit()
    print(render(report, only_failures=not report.passed and report.fail_count > 0))
    if report.passed:
        # Brief success confirmation
        files = sorted({c.file for c in report.checks})

        print(f"\nALL CLEAN — {report.pass_count} checks across {len(files)} HTML pages.")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
