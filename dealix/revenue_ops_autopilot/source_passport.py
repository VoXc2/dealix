"""Source Passport — audit of all lead sources for the Revenue Intelligence Sprint.

Every engagement starts with a Source Passport that documents where leads come
from, how clean they are, and whether they are trustworthy enough to score and
act on.  A DQ score < 70 surfaces a founder-review gate before any outreach
drafts are generated.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

SourceType = Literal["crm", "whatsapp", "referral", "cold", "inbound"]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class LeadSource(BaseModel):
    """A single lead origin channel."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, description="Human-readable channel name.")
    type: SourceType = Field(..., description="Channel category.")
    count: int = Field(..., ge=0, description="Total leads from this source.")
    qualified_count: int = Field(
        ..., ge=0, description="Leads that reached a qualified stage."
    )
    conversion_rate: float = Field(
        ..., ge=0.0, le=1.0, description="qualified / total (0-1)."
    )
    avg_deal_value: float = Field(
        default=0.0, ge=0.0, description="Average deal value in SAR."
    )
    notes: str = Field(default="", description="Free-text observations.")


class SourcePassport(BaseModel):
    """Aggregated audit of all lead sources for one engagement."""

    model_config = ConfigDict(extra="forbid")

    sources: list[LeadSource] = Field(default_factory=list)
    total_leads: int = Field(default=0, ge=0)
    total_qualified: int = Field(default=0, ge=0)
    overall_dq_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Data Quality score 0-100.  < 70 triggers founder review.",
    )
    red_flags: list[str] = Field(default_factory=list)
    recommendations_ar: list[str] = Field(default_factory=list)
    recommendations_en: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

# Conversion thresholds
_LOW_CONVERSION_THRESHOLD = 0.20  # below 20 % is penalised
_GOOD_CONVERSION_THRESHOLD = 0.40  # above 40 % is rewarded

# DQ weight per source type (higher = more trustworthy signal)
_SOURCE_TYPE_WEIGHT: dict[str, float] = {
    "referral": 1.25,   # referrals have built-in vetting
    "inbound": 1.15,    # intent-driven leads
    "crm": 1.00,        # structured data
    "whatsapp": 0.85,   # informal, often missing fields
    "cold": 0.70,       # lowest-trust channel
}


class SourcePassportBuilder:
    """Deterministic builder — no LLM, no external calls."""

    def build(self, sources: list[dict]) -> SourcePassport:
        """Validate, score, and annotate a list of raw source dicts."""
        parsed: list[LeadSource] = []
        for raw in sources:
            # Compute conversion_rate if not supplied
            if "conversion_rate" not in raw and raw.get("count", 0) > 0:
                raw = dict(raw)
                raw["conversion_rate"] = raw.get("qualified_count", 0) / raw["count"]
            elif "conversion_rate" not in raw:
                raw = dict(raw)
                raw["conversion_rate"] = 0.0
            parsed.append(LeadSource(**raw))

        total_leads = sum(s.count for s in parsed)
        total_qualified = sum(s.qualified_count for s in parsed)

        # ----------------------------------------------------------------
        # DQ scoring
        # ----------------------------------------------------------------
        # Start from 60 — a neutral baseline for "some data present".
        # Each source adjusts the pool-level score proportional to its
        # share of total leads.
        # ----------------------------------------------------------------
        if not parsed:
            dq_score = 0.0
            red_flags: list[str] = ["no_sources_provided"]
            recs_ar: list[str] = ["لم يتم تقديم أي مصادر — يرجى توثيق قنوات العملاء المحتملين."]
            recs_en: list[str] = ["No sources provided — please document your lead channels."]
            return SourcePassport(
                sources=parsed,
                total_leads=0,
                total_qualified=0,
                overall_dq_score=dq_score,
                red_flags=red_flags,
                recommendations_ar=recs_ar,
                recommendations_en=recs_en,
            )

        weighted_score = 0.0
        red_flags = []
        recs_ar: list[str] = []
        recs_en: list[str] = []

        for source in parsed:
            share = source.count / total_leads if total_leads > 0 else 1.0 / len(parsed)
            base = 60.0

            # Conversion quality
            if source.conversion_rate < _LOW_CONVERSION_THRESHOLD:
                base -= 20.0
                red_flags.append(
                    f"low_conversion:{source.name} ({source.conversion_rate:.0%})"
                )
                recs_ar.append(
                    f"قناة '{source.name}' لديها معدل تحويل منخفض ({source.conversion_rate:.0%}) "
                    "— راجع جودة الاستهداف أو احذف الإدخالات غير المؤهَّلة."
                )
                recs_en.append(
                    f"Source '{source.name}' has a low conversion rate "
                    f"({source.conversion_rate:.0%}) — review targeting or remove "
                    "unqualified entries."
                )
            elif source.conversion_rate >= _GOOD_CONVERSION_THRESHOLD:
                base += 15.0

            # Channel trust weight
            weight = _SOURCE_TYPE_WEIGHT.get(source.type, 1.0)
            base *= weight

            # Reward high-trust channels explicitly
            if source.type in ("referral", "inbound"):
                if source.count > 0:
                    recs_ar.append(
                        f"قناة '{source.name}' من نوع {source.type} — استمر في تعزيزها "
                        "لأنها تُولّد عملاء محتملين عاليي الجودة."
                    )
                    recs_en.append(
                        f"Source '{source.name}' ({source.type}) — keep investing here "
                        "as it generates high-quality leads."
                    )

            # Cold-source risk flag
            if source.type == "cold" and source.count > 0:
                red_flags.append(f"cold_source:{source.name}")
                recs_ar.append(
                    f"قناة '{source.name}' (بارد) — تأكد من الامتثال لسياسة الاتصال "
                    "قبل أي مراسلة."
                )
                recs_en.append(
                    f"Source '{source.name}' (cold) — verify contact-policy compliance "
                    "before any outreach."
                )

            # Missing deal value info
            if source.avg_deal_value == 0.0 and source.type in ("crm", "inbound"):
                red_flags.append(f"missing_deal_value:{source.name}")
                recs_ar.append(
                    f"قناة '{source.name}' لا تحتوي على متوسط قيمة الصفقة "
                    "— أضف هذا البُعد لتحسين التسعير."
                )
                recs_en.append(
                    f"Source '{source.name}' is missing average deal value "
                    "— populate it to improve pricing decisions."
                )

            # Clamp per-source contribution to [0, 100]
            base = max(0.0, min(100.0, base))
            weighted_score += share * base

        # Bonus: diversity of trustworthy channel types
        trustworthy_types = {
            s.type for s in parsed if s.type in ("referral", "inbound", "crm")
        }
        if len(trustworthy_types) >= 2:
            weighted_score = min(100.0, weighted_score + 5.0)

        # Zero-lead penalty
        if total_leads == 0:
            weighted_score = max(0.0, weighted_score - 30.0)
            red_flags.append("zero_total_leads")

        dq_score = round(max(0.0, min(100.0, weighted_score)), 2)

        # Deduplicate while preserving order
        seen_r: set[str] = set()
        recs_ar_dedup: list[str] = []
        for r in recs_ar:
            if r not in seen_r:
                recs_ar_dedup.append(r)
                seen_r.add(r)

        seen_e: set[str] = set()
        recs_en_dedup: list[str] = []
        for r in recs_en:
            if r not in seen_e:
                recs_en_dedup.append(r)
                seen_e.add(r)

        return SourcePassport(
            sources=parsed,
            total_leads=total_leads,
            total_qualified=total_qualified,
            overall_dq_score=dq_score,
            red_flags=list(dict.fromkeys(red_flags)),
            recommendations_ar=recs_ar_dedup,
            recommendations_en=recs_en_dedup,
        )
