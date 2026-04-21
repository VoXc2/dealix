"""
Local Model Catalog — tier-based selection for on-prem deployment.

The catalog maps open-weight LLMs (Ollama tags) to:
  • A server tier (nano / small / balanced / performance)
  • A task kind (router / general / coder / reasoner / multilingual)
  • RAM & disk footprint estimates

At runtime, `detect_server_tier()` inspects RAM / swap / disk and
picks the highest tier the machine can safely run. `pick_model_for_task`
then chooses the best catalogued model for that tier + task.

No API-hosted models (Claude, GPT-4, Gemini, Grok) are listed here —
those cannot be downloaded and are served through `model_router.py`.
"""
from __future__ import annotations

import logging
import os
import shutil
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


class ServerTier(str, Enum):
    NANO = "nano"           # < 4 GB usable RAM (router-only, CPU)
    SMALL = "small"          # 4–8 GB RAM (single 3B model, CPU)
    BALANCED = "balanced"    # 8–16 GB RAM (7B Q4, CPU or modest GPU)
    PERFORMANCE = "performance"  # 16+ GB RAM and/or CUDA GPU (multi-model, 8B+)


class TaskKind(str, Enum):
    ROUTER = "router"               # Fast intent classification / routing
    GENERAL = "general"             # Summaries, short drafts, Q&A
    MULTILINGUAL = "multilingual"   # Arabic ↔ English reasoning
    CODER = "coder"                 # Code generation / review
    REASONER = "reasoner"           # Complex planning / analysis


@dataclass(frozen=True)
class LocalModelSpec:
    """A model that can actually be pulled by Ollama on a modest server."""
    ollama_tag: str            # e.g. "qwen2.5:3b-instruct"
    family: str                # e.g. "qwen2.5"
    approx_size_gb: float      # rough disk/VRAM footprint
    min_ram_gb: float          # minimum free RAM recommended
    tier: ServerTier           # smallest tier that can host this model
    tasks: tuple[TaskKind, ...]
    arabic_quality: int        # 1 (weak) – 5 (strong) subjective rating
    english_quality: int
    notes: str = ""


MODEL_CATALOG: tuple[LocalModelSpec, ...] = (
    # ── Router / nano tier ─────────────────────────────────────────
    LocalModelSpec(
        ollama_tag="qwen2.5:0.5b",
        family="qwen2.5",
        approx_size_gb=0.4,
        min_ram_gb=1.5,
        tier=ServerTier.NANO,
        tasks=(TaskKind.ROUTER,),
        arabic_quality=2,
        english_quality=3,
        notes="Ultra-light router. Use for intent tags / classification only.",
    ),
    LocalModelSpec(
        ollama_tag="llama3.2:1b",
        family="llama3.2",
        approx_size_gb=1.3,
        min_ram_gb=3.0,
        tier=ServerTier.NANO,
        tasks=(TaskKind.ROUTER, TaskKind.GENERAL),
        arabic_quality=2,
        english_quality=4,
        notes="Meta Llama 3.2 1B — good tiny English model.",
    ),

    # ── Small tier (3B class) ─────────────────────────────────────
    LocalModelSpec(
        ollama_tag="qwen2.5:3b-instruct",
        family="qwen2.5",
        approx_size_gb=2.0,
        min_ram_gb=4.5,
        tier=ServerTier.SMALL,
        tasks=(TaskKind.GENERAL, TaskKind.MULTILINGUAL),
        arabic_quality=4,
        english_quality=4,
        notes="Best Arabic-capable small model. Default for SMALL tier.",
    ),
    LocalModelSpec(
        ollama_tag="llama3.2:3b",
        family="llama3.2",
        approx_size_gb=2.0,
        min_ram_gb=4.5,
        tier=ServerTier.SMALL,
        tasks=(TaskKind.GENERAL, TaskKind.REASONER),
        arabic_quality=3,
        english_quality=4,
        notes="Meta Llama 3.2 3B — balanced general-purpose.",
    ),
    LocalModelSpec(
        ollama_tag="phi3:mini",
        family="phi3",
        approx_size_gb=2.2,
        min_ram_gb=4.5,
        tier=ServerTier.SMALL,
        tasks=(TaskKind.GENERAL, TaskKind.REASONER),
        arabic_quality=2,
        english_quality=4,
        notes="Microsoft Phi-3 Mini — strong reasoning per byte.",
    ),
    LocalModelSpec(
        ollama_tag="gemma2:2b",
        family="gemma2",
        approx_size_gb=1.6,
        min_ram_gb=3.5,
        tier=ServerTier.SMALL,
        tasks=(TaskKind.GENERAL,),
        arabic_quality=3,
        english_quality=4,
        notes="Google Gemma 2 2B — fast, multilingual-friendly.",
    ),

    # ── Balanced tier (7B class, Q4 quant) ────────────────────────
    LocalModelSpec(
        ollama_tag="qwen2.5:7b-instruct",
        family="qwen2.5",
        approx_size_gb=4.7,
        min_ram_gb=9.0,
        tier=ServerTier.BALANCED,
        tasks=(TaskKind.GENERAL, TaskKind.MULTILINGUAL, TaskKind.REASONER),
        arabic_quality=5,
        english_quality=5,
        notes="Primary choice for Arabic business reasoning.",
    ),
    LocalModelSpec(
        ollama_tag="llama3.1:8b",
        family="llama3.1",
        approx_size_gb=4.9,
        min_ram_gb=9.5,
        tier=ServerTier.BALANCED,
        tasks=(TaskKind.GENERAL, TaskKind.REASONER),
        arabic_quality=3,
        english_quality=5,
        notes="Meta Llama 3.1 8B — strongest English 7–8B.",
    ),
    LocalModelSpec(
        ollama_tag="qwen2.5-coder:7b",
        family="qwen2.5-coder",
        approx_size_gb=4.7,
        min_ram_gb=9.0,
        tier=ServerTier.BALANCED,
        tasks=(TaskKind.CODER,),
        arabic_quality=2,
        english_quality=5,
        notes="Top open coding model in the 7B class.",
    ),

    # ── Performance tier (14B+ / multi-model) ─────────────────────
    LocalModelSpec(
        ollama_tag="qwen2.5:14b-instruct",
        family="qwen2.5",
        approx_size_gb=8.8,
        min_ram_gb=18.0,
        tier=ServerTier.PERFORMANCE,
        tasks=(TaskKind.REASONER, TaskKind.MULTILINGUAL, TaskKind.GENERAL),
        arabic_quality=5,
        english_quality=5,
        notes="Best-in-class local reasoner for Arabic business.",
    ),
    LocalModelSpec(
        ollama_tag="deepseek-coder-v2:lite",
        family="deepseek-coder-v2",
        approx_size_gb=9.0,
        min_ram_gb=18.0,
        tier=ServerTier.PERFORMANCE,
        tasks=(TaskKind.CODER,),
        arabic_quality=2,
        english_quality=5,
        notes="Strongest open coder at ~16B MoE, still runnable on CPU.",
    ),
)


# ── Tier detection ────────────────────────────────────────────────

def _read_meminfo_gb() -> tuple[float, float]:
    """Return (total_ram_gb, available_ram_gb). Fallback: (4.0, 2.0)."""
    try:
        with open("/proc/meminfo", encoding="utf-8") as fh:
            data = {}
            for line in fh:
                k, _, rest = line.partition(":")
                data[k.strip()] = rest.strip()
        total_kb = int(data.get("MemTotal", "4194304 kB").split()[0])
        avail_kb = int(data.get("MemAvailable", str(total_kb // 2) + " kB").split()[0])
        return total_kb / (1024 * 1024), avail_kb / (1024 * 1024)
    except Exception:
        return 4.0, 2.0


def _free_disk_gb(path: str = "/") -> float:
    try:
        _, _, free = shutil.disk_usage(path)
        return free / (1024**3)
    except Exception:
        return 10.0


def _detect_gpu() -> bool:
    """Best-effort: True if an NVIDIA GPU appears present."""
    if os.environ.get("LOCAL_LLM_HAS_GPU", "").lower() in {"1", "true", "yes"}:
        return True
    return bool(shutil.which("nvidia-smi"))


@dataclass
class ServerCapacity:
    total_ram_gb: float
    available_ram_gb: float
    free_disk_gb: float
    has_gpu: bool
    tier: ServerTier

    def to_dict(self) -> dict:
        return {
            "total_ram_gb": round(self.total_ram_gb, 2),
            "available_ram_gb": round(self.available_ram_gb, 2),
            "free_disk_gb": round(self.free_disk_gb, 2),
            "has_gpu": self.has_gpu,
            "tier": self.tier.value,
        }


def detect_server_tier(min_disk_gb: float = 6.0) -> ServerCapacity:
    """
    Classify the current host. Conservative — prefers underselecting.

    Override with `LOCAL_LLM_FORCE_TIER=nano|small|balanced|performance`.
    """
    forced = os.environ.get("LOCAL_LLM_FORCE_TIER", "").lower().strip()
    total, avail = _read_meminfo_gb()
    disk = _free_disk_gb()
    gpu = _detect_gpu()

    if forced in {t.value for t in ServerTier}:
        tier = ServerTier(forced)
    elif disk < min_disk_gb:
        tier = ServerTier.NANO
    elif gpu or total >= 16.0:
        tier = ServerTier.PERFORMANCE
    elif total >= 8.0:
        tier = ServerTier.BALANCED
    elif total >= 4.0:
        tier = ServerTier.SMALL
    else:
        tier = ServerTier.NANO

    return ServerCapacity(
        total_ram_gb=total,
        available_ram_gb=avail,
        free_disk_gb=disk,
        has_gpu=gpu,
        tier=tier,
    )


# ── Selection helpers ─────────────────────────────────────────────

_TIER_ORDER = {
    ServerTier.NANO: 0,
    ServerTier.SMALL: 1,
    ServerTier.BALANCED: 2,
    ServerTier.PERFORMANCE: 3,
}


def _tier_allows(model_tier: ServerTier, host_tier: ServerTier) -> bool:
    return _TIER_ORDER[model_tier] <= _TIER_ORDER[host_tier]


def select_models_for_tier(
    tier: ServerTier,
    catalog: Iterable[LocalModelSpec] = MODEL_CATALOG,
) -> list[LocalModelSpec]:
    """Return all catalogued models the tier can run, smallest first."""
    eligible = [m for m in catalog if _tier_allows(m.tier, tier)]
    return sorted(eligible, key=lambda m: (m.approx_size_gb, m.ollama_tag))


def pick_model_for_task(
    task: TaskKind,
    tier: ServerTier,
    prefer_arabic: bool = True,
    catalog: Iterable[LocalModelSpec] = MODEL_CATALOG,
) -> Optional[LocalModelSpec]:
    """
    Pick the best model in `catalog` that the `tier` can host and that
    is listed for `task`. Ranks by Arabic quality first (if requested),
    then English quality, then inverse size (smaller wins ties — cheaper).
    """
    candidates = [
        m for m in catalog
        if _tier_allows(m.tier, tier) and task in m.tasks
    ]
    if not candidates:
        # Fallback: any GENERAL model on this tier
        candidates = [
            m for m in catalog
            if _tier_allows(m.tier, tier) and TaskKind.GENERAL in m.tasks
        ]
    if not candidates:
        return None

    def score(m: LocalModelSpec) -> tuple:
        primary = m.arabic_quality if prefer_arabic else m.english_quality
        secondary = m.english_quality if prefer_arabic else m.arabic_quality
        # Higher quality first, then smaller size (ties broken by tag).
        return (-primary, -secondary, m.approx_size_gb, m.ollama_tag)

    candidates.sort(key=score)
    return candidates[0]


def recommended_install_plan(capacity: ServerCapacity) -> list[LocalModelSpec]:
    """
    Minimal recommended model set to pull on this host.

    Strategy: one router, one general/multilingual, plus a coder on
    balanced+ tiers. Filters anything that would not fit in free disk.
    """
    tier = capacity.tier
    desired: list[LocalModelSpec] = []

    router = pick_model_for_task(TaskKind.ROUTER, tier, prefer_arabic=False)
    if router:
        desired.append(router)

    general = pick_model_for_task(TaskKind.MULTILINGUAL, tier, prefer_arabic=True) \
        or pick_model_for_task(TaskKind.GENERAL, tier, prefer_arabic=True)
    if general and general not in desired:
        desired.append(general)

    if tier in (ServerTier.BALANCED, ServerTier.PERFORMANCE):
        coder = pick_model_for_task(TaskKind.CODER, tier, prefer_arabic=False)
        if coder and coder not in desired:
            desired.append(coder)

    # Respect free disk: skip models that would exceed 70% of available disk.
    budget = capacity.free_disk_gb * 0.70
    plan: list[LocalModelSpec] = []
    used = 0.0
    for m in desired:
        if used + m.approx_size_gb <= budget:
            plan.append(m)
            used += m.approx_size_gb
        else:
            logger.info(
                "Skipping %s (~%.1f GB): exceeds 70%% of free disk (%.1f GB)",
                m.ollama_tag, m.approx_size_gb, capacity.free_disk_gb,
            )
    return plan
