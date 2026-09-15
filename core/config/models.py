"""Legacy model-routing compatibility metadata.

Omega V3 model/provider/cost/data authority belongs to the canonical Dealix
broker and Session Factory.  This module keeps historical enums/model metadata
for imports, telemetry and migrations, but *automatic* task routing now resolves
to ``Provider.HOLD``.  Legacy callers must migrate to the governed execution
fabric instead of selecting a provider or model here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Provider(StrEnum):
    """Compatibility provider identifiers; not automatic authority."""

    HOLD = "hold"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GLM = "glm"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"


class Task(StrEnum):
    REASONING = "reasoning"
    SUMMARY = "summary"
    PROPOSAL = "proposal"
    PAGE_COPY = "page_copy"
    ORCHESTRATION = "orchestration"
    RESEARCH = "research"
    MULTIMODAL = "multimodal"
    SOURCE_ANALYSIS = "source_analysis"
    CLASSIFICATION = "classification"
    TAGGING = "tagging"
    FAST_VARIANTS = "fast_variants"
    TRIAGE = "triage"
    CODE = "code"
    IMPLEMENTATION = "implementation"
    DEBUG = "debug"
    ARABIC_TASKS = "arabic_tasks"
    CHINESE_TASKS = "chinese_tasks"
    BULK_TASKS = "bulk_tasks"


@dataclass(frozen=True)
class ModelConfig:
    provider: Provider
    model_id: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


HOLD_MODEL_ID = "HOLD_CANONICAL_BROKER_REQUIRED"
HOLD_CONFIG = ModelConfig(
    provider=Provider.HOLD,
    model_id=HOLD_MODEL_ID,
    max_tokens=0,
    temperature=0.0,
    timeout=1,
)

# Automatic routing is deliberately disabled in this legacy layer.  A caller
# that needs a model must enter through Company Operator -> Session Factory ->
# canonical broker with trusted DATA_SENSITIVITY and resource admission.
TASK_ROUTING: dict[Task, Provider] = {task: Provider.HOLD for task in Task}

# The HOLD provider has no fallback.  Historical provider rows below are kept
# only for compatibility/introspection and are never reached automatically.
FALLBACK_CHAIN: dict[Provider, list[Provider]] = {provider: [] for provider in Provider}


def get_provider_for_task(task: Task) -> Provider:
    _ = task
    return Provider.HOLD


def get_fallbacks(provider: Provider) -> list[Provider]:
    _ = provider
    return []


PROVIDER_MODELS: dict[Provider, ModelConfig] = {
    Provider.HOLD: HOLD_CONFIG,
    Provider.ANTHROPIC: ModelConfig(
        provider=Provider.ANTHROPIC,
        model_id="claude-sonnet-4-5",
        max_tokens=4096,
        temperature=0.3,
    ),
    Provider.DEEPSEEK: ModelConfig(
        provider=Provider.DEEPSEEK,
        model_id="deepseek-chat",
        max_tokens=4096,
        temperature=0.2,
    ),
    Provider.GLM: ModelConfig(
        provider=Provider.GLM,
        model_id="glm-4",
        max_tokens=4096,
        temperature=0.3,
    ),
    Provider.GEMINI: ModelConfig(
        provider=Provider.GEMINI,
        model_id="gemini-2.5-flash",
        max_tokens=8192,
        temperature=0.3,
    ),
    Provider.GROQ: ModelConfig(
        provider=Provider.GROQ,
        model_id="llama-3.3-70b-versatile",
        max_tokens=2048,
        temperature=0.1,
    ),
    Provider.OPENAI: ModelConfig(
        provider=Provider.OPENAI,
        model_id="gpt-4o-mini",
        max_tokens=4096,
        temperature=0.3,
    ),
}

# Historical observability hints only; never automatic spending authority.
COST_HINTS: dict[Provider, tuple[float, float]] = {
    Provider.HOLD: (0.0, 0.0),
    Provider.ANTHROPIC: (3.00, 15.00),
    Provider.DEEPSEEK: (0.14, 0.28),
    Provider.GLM: (0.14, 0.28),
    Provider.GEMINI: (0.075, 0.30),
    Provider.GROQ: (0.00, 0.00),
    Provider.OPENAI: (0.15, 0.60),
}

ARABIC_THRESHOLD = 0.30
SHORT_EXTRACTION_TOKENS = 2000
CRITICAL_TASKS = {
    Task.REASONING,
    Task.PROPOSAL,
    Task.ORCHESTRATION,
}


def _arabic_ratio(text: str) -> float:
    if not text:
        return 0.0
    arabic = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    return arabic / max(len(text), 1)


def smart_route(
    task: Task,
    *,
    text_sample: str = "",
    est_tokens: int = 0,
    critical: bool = False,
) -> ModelConfig:
    """Fail closed: legacy smart routing no longer selects a model/provider."""

    _ = task, text_sample, est_tokens, critical
    return HOLD_CONFIG


def ordered_providers(
    task: Task, *, text_sample: str = "", critical: bool = False
) -> list[Provider]:
    """Return only the migration HOLD sentinel; no provider fallback chain."""

    _ = task, text_sample, critical
    return [Provider.HOLD]
