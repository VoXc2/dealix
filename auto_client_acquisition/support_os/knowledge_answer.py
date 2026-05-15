"""V12 Support OS — knowledge-base answer lookup.

Reads ``docs/knowledge-base/*.md``. Returns ``insufficient_evidence``
when no file matches the category. NEVER invents policy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from auto_client_acquisition.runtime_paths import resolve_repo_root
from auto_client_acquisition.support_os.classifier import SupportCategory

# Category → preferred KB file(s) under docs/knowledge-base/
_CATEGORY_TO_FILES: dict[SupportCategory, tuple[str, ...]] = {
    "onboarding": ("support_faq_ar.md", "support_faq_en.md", "service_delivery_ar_en.md"),
    "billing": ("payment_policy_ar_en.md", "pricing_policy_ar_en.md"),
    "payment": ("payment_policy_ar_en.md",),
    "technical_issue": ("support_faq_ar.md", "support_faq_en.md"),
    "connector_setup": ("service_delivery_ar_en.md",),
    "diagnostic_question": ("service_delivery_ar_en.md", "support_faq_ar.md"),
    "proof_pack_question": ("service_delivery_ar_en.md", "support_faq_en.md"),
    "privacy_pdpl": ("privacy_pdpl_ar_en.md",),
    "refund": ("payment_policy_ar_en.md",),
    "angry_customer": ("escalation_policy_ar_en.md",),
    "upgrade_question": ("pricing_policy_ar_en.md",),
    "unknown": (),
}


@dataclass
class KnowledgeAnswer:
    found: bool
    category: SupportCategory
    sources: list[str] = field(default_factory=list)
    snippet_ar: str = ""
    snippet_en: str = ""
    insufficient_evidence: bool = False


def _kb_dir() -> Path:
    return resolve_repo_root() / "docs" / "knowledge-base"


def _read_first_lines(path: Path, max_chars: int = 600) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    return text[:max_chars]


def answer_from_knowledge_base(category: SupportCategory) -> KnowledgeAnswer:
    files = _CATEGORY_TO_FILES.get(category, ())
    if not files:
        return KnowledgeAnswer(
            found=False,
            category=category,
            insufficient_evidence=True,
        )
    base = _kb_dir()
    sources: list[str] = []
    snippets: list[str] = []
    for fname in files:
        path = base / fname
        if path.exists():
            sources.append(str(path.relative_to(resolve_repo_root())))
            snippets.append(_read_first_lines(path))
    if not sources:
        return KnowledgeAnswer(
            found=False,
            category=category,
            insufficient_evidence=True,
        )
    combined = "\n".join(snippets)
    return KnowledgeAnswer(
        found=True,
        category=category,
        sources=sources,
        snippet_ar=combined,
        snippet_en=combined,
        insufficient_evidence=False,
    )
