"""
Model routing configuration — maps tasks to the best LLM provider.
توجيه النماذج — يربط كل مهمة بأفضل مزود نموذج.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Provider(str, Enum):
    """Supported LLM providers | المزودون المدعومون."""

    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GLM = "glm"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"


class Task(str, Enum):
    """Task categories — route each to the best provider | أنواع المهام."""

    # Reasoning / writing → Claude
    REASONING = "reasoning"
    SUMMARY = "summary"
    PROPOSAL = "proposal"
    PAGE_COPY = "page_copy"
    ORCHESTRATION = "orchestration"

    # Research / multimodal → Gemini
    RESEARCH = "research"
    MULTIMODAL = "multimodal"
    SOURCE_ANALYSIS = "source_analysis"

    # Fast classification → Groq
    CLASSIFICATION = "classification"
    TAGGING = "tagging"
    FAST_VARIANTS = "fast_variants"
    TRIAGE = "triage"

    # Code → DeepSeek
    CODE = "code"
    IMPLEMENTATION = "implementation"
    DEBUG = "debug"

    # Arabic / bulk → GLM
    ARABIC_TASKS = "arabic_tasks"
    CHINESE_TASKS = "chinese_tasks"
    BULK_TASKS = "bulk_tasks"


@dataclass(frozen=True)
class ModelConfig:
    """Immutable model configuration | إعدادات نموذج ثابتة."""

    provider: Provider
    model_id: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


# ═══════════════════════════════════════════════════════════════
# TASK → PROVIDER ROUTING TABLE
# جدول توجيه المهام إلى المزودين
# ═══════════════════════════════════════════════════════════════

TASK_ROUTING: dict[Task, Provider] = {
    # Claude — reasoning, writing, orchestration
    Task.REASONING: Provider.ANTHROPIC,
    Task.SUMMARY: Provider.ANTHROPIC,
    Task.PROPOSAL: Provider.ANTHROPIC,
    Task.PAGE_COPY: Provider.ANTHROPIC,
    Task.ORCHESTRATION: Provider.ANTHROPIC,

    # Gemini — research, multimodal, sources
    Task.RESEARCH: Provider.GEMINI,
    Task.MULTIMODAL: Provider.GEMINI,
    Task.SOURCE_ANALYSIS: Provider.GEMINI,

    # Groq — fast, cheap
    Task.CLASSIFICATION: Provider.GROQ,
    Task.TAGGING: Provider.GROQ,
    Task.FAST_VARIANTS: Provider.GROQ,
    Task.TRIAGE: Provider.GROQ,

    # DeepSeek — code
    Task.CODE: Provider.DEEPSEEK,
    Task.IMPLEMENTATION: Provider.DEEPSEEK,
    Task.DEBUG: Provider.DEEPSEEK,

    # GLM — Arabic, Chinese, bulk
    Task.ARABIC_TASKS: Provider.GLM,
    Task.CHINESE_TASKS: Provider.GLM,
    Task.BULK_TASKS: Provider.GLM,
}


# Fallback chain — if primary provider fails, try these in order
# سلسلة الاحتياط — إذا فشل المزود الرئيسي جرّب هؤلاء
FALLBACK_CHAIN: dict[Provider, list[Provider]] = {
    Provider.ANTHROPIC: [Provider.OPENAI, Provider.GLM],
    Provider.DEEPSEEK: [Provider.ANTHROPIC, Provider.OPENAI],
    Provider.GLM: [Provider.ANTHROPIC, Provider.GROQ],
    Provider.GEMINI: [Provider.ANTHROPIC, Provider.OPENAI],
    Provider.GROQ: [Provider.GLM, Provider.DEEPSEEK],
    Provider.OPENAI: [Provider.ANTHROPIC, Provider.GLM],
}


def get_provider_for_task(task: Task) -> Provider:
    """Get primary provider for a task | المزود الرئيسي للمهمة."""
    return TASK_ROUTING.get(task, Provider.ANTHROPIC)


def get_fallbacks(provider: Provider) -> list[Provider]:
    """Get fallback chain for a provider | سلسلة الاحتياط للمزود."""
    return FALLBACK_CHAIN.get(provider, [Provider.ANTHROPIC])
