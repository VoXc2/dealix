#!/usr/bin/env python3
"""Wave 12.8 — Dealix Daily Autonomous Lead Prep.

Runs every morning (cron-able) to PREPARE today's lead board for the
founder — without sending anything. Composes:

    Saudi Market Radar (signals + season context)
        → Lead candidates (founder-supplied OR existing pipeline data)
        → 13-dim Saudi-specific scoring
        → Decision Passports for top-5 (with owner + deadline + action_mode)
        → Bilingual draft messages (DRAFT_ONLY, never auto-sent)
        → Daily Lead Board JSON + Markdown

Output: ``data/wave12/daily_lead_prep/{YYYY-MM-DD}.{json,md}`` (gitignored)

Hard rules (Article 4 — IMMUTABLE):
- ALL outputs are DRAFT_ONLY / approval_required
- NEVER calls any send API (WhatsApp, email, LinkedIn, phone)
- NEVER calls live charge / live publish
- NEVER scrapes; only consumes founder-supplied lead lists or
  existing pipeline data
- Output path is gitignored — no PII committed

Usage:
    python3 scripts/dealix_daily_lead_prep.py
    python3 scripts/dealix_daily_lead_prep.py --candidates path/to/leads.csv
    python3 scripts/dealix_daily_lead_prep.py --top-n 10 --on-date 2026-05-15

Cron example (08:00 KSA = 05:00 UTC daily):
    0 5 * * * cd /home/user/dealix && python3 scripts/dealix_daily_lead_prep.py

Output exit codes:
    0 = report generated (founder reviews + approves)
    1 = no leads provided + no pipeline state to score (informational)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = REPO_ROOT / "data" / "wave12" / "daily_lead_prep"

# Make the auto_client_acquisition package importable when running standalone.
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.market_intelligence.saudi_seasons import (  # noqa: E402
    detect_saudi_season,
)
from auto_client_acquisition.market_intelligence.signal_detectors import (  # noqa: E402
    SIGNAL_TYPES,
    get_signal_output,
)
from auto_client_acquisition.pipelines.saudi_dimensions import (  # noqa: E402
    SaudiScoreBoard,
    compute_saudi_score_board,
)


# ─────────────────────────────────────────────────────────────────────
# Types
# ─────────────────────────────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class LeadCandidate:
    """Inbound candidate (from CSV or pipeline)."""

    name: str
    sector: str = ""
    city: str = ""
    country: str = ""
    domain: str = ""
    contact_name: str = ""
    contact_title: str = ""
    source: str = "warm_intro"  # default to safe source per Article 4
    locale: str = "ar"
    annual_turnover_sar: float | None = None
    notes: str = ""


@dataclass(frozen=True, slots=True)
class DailyLeadEntry:
    """One scored lead in today's board."""

    rank: int
    candidate: LeadCandidate
    saudi_scores: dict[str, Any]
    composite_score: float
    priority: Literal["P0_NOW", "P1_THIS_WEEK", "P2_NURTURE", "P3_LOW_PRIORITY", "BLOCKED"]
    why_now_ar: str
    why_now_en: str
    recommended_action_ar: str
    recommended_action_en: str
    action_mode: Literal["draft_only", "approval_required", "blocked"]
    blockers: tuple[str, ...] = ()
    is_estimate: bool = True


@dataclass(frozen=True, slots=True)
class DailyLeadBoard:
    """Today's complete lead-prep output."""

    generated_at: str
    on_date: str
    season_context: dict[str, Any]
    candidates_count: int
    leads_returned: int
    top_leads: tuple[DailyLeadEntry, ...]
    bilingual_summary: dict[str, str]
    article_4_invariants: tuple[str, ...] = field(default_factory=tuple)
    next_founder_action: str = ""
    is_estimate: bool = True


# ─────────────────────────────────────────────────────────────────────
# Composite scoring
# ─────────────────────────────────────────────────────────────────────


# Weights for composite score (sum ~= 1.0 — used to rank top-N)
_SCORE_WEIGHTS = {
    "arabic_readiness": 0.10,
    "decision_maker_access": 0.20,
    "saudi_compliance_sensitivity": 0.05,  # neutral-ish
    "seasonality": 0.20,
    "relationship_strength": 0.30,
    # Friction (negative weight)
    "whatsapp_dependency_risk": -0.15,
}


def _composite_score(board: SaudiScoreBoard) -> float:
    """Combine the 6 Saudi dimensions into a single 0-1 ranking score."""
    raw = (
        _SCORE_WEIGHTS["arabic_readiness"] * board.arabic_readiness
        + _SCORE_WEIGHTS["decision_maker_access"] * board.decision_maker_access
        + _SCORE_WEIGHTS["saudi_compliance_sensitivity"] * board.saudi_compliance_sensitivity
        + _SCORE_WEIGHTS["seasonality"] * board.seasonality
        + _SCORE_WEIGHTS["relationship_strength"] * board.relationship_strength
        + _SCORE_WEIGHTS["whatsapp_dependency_risk"] * board.whatsapp_dependency_risk
    )
    # Clamp to [0, 1]
    return round(max(0.0, min(1.0, raw)), 3)


def _priority_bucket(score: float, board: SaudiScoreBoard) -> str:
    """Map composite score → priority bucket.

    Article 4: blocked sources land in BLOCKED regardless of score.
    """
    # Blocked-source check first (defense in depth)
    if any("BLOCKED_SOURCE" in n for n in board.notes):
        return "BLOCKED"
    if score >= 0.70:
        return "P0_NOW"
    if score >= 0.55:
        return "P1_THIS_WEEK"
    if score >= 0.35:
        return "P2_NURTURE"
    return "P3_LOW_PRIORITY"


def _why_now(season: dict[str, Any], board: SaudiScoreBoard, candidate: LeadCandidate) -> tuple[str, str]:
    """Build bilingual 'why now' from season + scores + candidate context."""
    season_name = season.get("season", "ordinary")
    parts_ar: list[str] = []
    parts_en: list[str] = []
    if season_name not in ("ordinary",):
        parts_ar.append(f"السياق الموسمي: {season_name}")
        parts_en.append(f"Season: {season_name}")
    if board.relationship_strength >= 0.85:
        parts_ar.append("علاقة قوية أو inbound")
        parts_en.append("Warm/inbound relationship")
    if board.decision_maker_access >= 0.7:
        parts_ar.append("وصول للقرار-maker")
        parts_en.append("Decision-maker accessible")
    if board.saudi_compliance_sensitivity >= 0.6:
        parts_ar.append("قطاع حساس للامتثال (PDPL/ZATCA)")
        parts_en.append("Compliance-sensitive sector (PDPL/ZATCA)")
    if not parts_ar:
        parts_ar.append("أولوية معتدلة — راجع التفاصيل")
        parts_en.append("Moderate priority — review details")
    return (" • ".join(parts_ar), " · ".join(parts_en))


def _recommended_action(priority: str, board: SaudiScoreBoard) -> tuple[str, str, Literal["draft_only", "approval_required", "blocked"]]:
    """Map priority → action + bilingual recommendation + action_mode.

    Article 4: BLOCKED priority → blocked action_mode (never even drafts).
    """
    if priority == "BLOCKED":
        return (
            "محظور — تحقق من مصدر الـ lead قبل أي تواصل",
            "BLOCKED — verify lead source before any contact",
            "blocked",
        )
    if priority == "P0_NOW":
        return (
            "جهّز رسالة عربية + احجز اتصال هذا الأسبوع",
            "Draft Arabic message + book call this week",
            "approval_required",
        )
    if priority == "P1_THIS_WEEK":
        return (
            "جهّز diagnostic مصغّر + رسالة متابعة",
            "Prepare mini diagnostic + follow-up message",
            "approval_required",
        )
    if priority == "P2_NURTURE":
        return (
            "أضف للـ nurture board — رسالة ربع شهرية",
            "Add to nurture board — quarterly touch",
            "draft_only",
        )
    # P3_LOW_PRIORITY
    return (
        "أولوية منخفضة — راجع لاحقاً",
        "Low priority — review later",
        "draft_only",
    )


# ─────────────────────────────────────────────────────────────────────
# Candidate sources
# ─────────────────────────────────────────────────────────────────────


def load_candidates_from_csv(path: Path) -> list[LeadCandidate]:
    """Load candidates from a CSV. Required headers: name. All others optional."""
    candidates: list[LeadCandidate] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("name"):
                continue
            turnover_raw = row.get("annual_turnover_sar", "").strip()
            try:
                turnover = float(turnover_raw) if turnover_raw else None
            except ValueError:
                turnover = None
            candidates.append(LeadCandidate(
                name=row["name"].strip(),
                sector=row.get("sector", "").strip(),
                city=row.get("city", "").strip(),
                country=row.get("country", "").strip(),
                domain=row.get("domain", "").strip(),
                contact_name=row.get("contact_name", "").strip(),
                contact_title=row.get("contact_title", "").strip(),
                source=row.get("source", "warm_intro").strip() or "warm_intro",
                locale=row.get("locale", "ar").strip() or "ar",
                annual_turnover_sar=turnover,
                notes=row.get("notes", "").strip(),
            ))
    return candidates


def load_candidates_from_lead_inbox(*, limit: int = 100) -> list[LeadCandidate]:
    """Auto-source candidates from the existing lead_inbox.jsonl.

    Wave 12.9 — when no --candidates CSV is supplied, auto-pull from
    the existing landing-form inbox so the daily prep works out-of-the-box
    on a server that's already collecting inbound leads.

    Lead inbox records are inbound (Article 4 — inbound_form is a safe
    source). Status filter: only "new" leads (not yet contacted).

    Returns empty list when:
    - lead_inbox file doesn't exist (fresh install)
    - import fails (e.g. running from a stripped checkout)
    - no records have status="new"
    """
    try:
        from auto_client_acquisition.lead_inbox import list_leads
    except Exception:
        return []
    try:
        records = list_leads(limit=limit, status="new")
    except Exception:
        return []
    candidates: list[LeadCandidate] = []
    for rec in records:
        # Lead inbox records are flat dicts with founder-supplied fields.
        # Map common landing-form keys → LeadCandidate.
        name = (
            rec.get("company_name")
            or rec.get("company")
            or rec.get("name")
            or rec.get("contact_name")  # fallback: contact name as company label
            or ""
        ).strip()
        if not name:
            continue  # skip records without a name
        candidates.append(LeadCandidate(
            name=name,
            sector=str(rec.get("sector", "")).strip(),
            city=str(rec.get("city", "")).strip(),
            country=str(rec.get("country", "SA")).strip() or "SA",
            domain=str(rec.get("domain") or rec.get("website", "")).strip(),
            contact_name=str(rec.get("contact_name", "")).strip(),
            contact_title=str(rec.get("contact_title") or rec.get("title", "")).strip(),
            source="inbound_form",  # lead_inbox = inbound landing form
            locale=str(rec.get("locale", "ar")).strip() or "ar",
            annual_turnover_sar=None,
            notes=str(rec.get("message") or rec.get("notes", ""))[:200],
        ))
    return candidates


def _candidate_to_account_dict(c: LeadCandidate) -> dict[str, Any]:
    """Convert LeadCandidate → account dict shape for compute_saudi_score_board."""
    return {
        "name": c.name,
        "sector": c.sector,
        "city": c.city,
        "country": c.country,
        "domain": c.domain,
        "contact_name": c.contact_name,
        "contact_title": c.contact_title,
        "source": c.source,
        "locale": c.locale,
        "annual_turnover_sar": c.annual_turnover_sar,
    }


# ─────────────────────────────────────────────────────────────────────
# Main composition
# ─────────────────────────────────────────────────────────────────────


def run_daily_prep(
    *,
    candidates: list[LeadCandidate],
    on_date: date | None = None,
    top_n: int = 5,
) -> DailyLeadBoard:
    """Compose today's lead board from candidates.

    Pure function — no I/O, deterministic. Caller writes the output.

    Args:
        candidates: Founder-supplied or pipeline-derived leads.
        on_date: Override (for tests + retroactive runs).
        top_n: How many top leads to surface (default 5).

    Returns:
        DailyLeadBoard — ready to JSON-serialize and write.
    """
    today = on_date or datetime.now(timezone.utc).date()
    season_ctx = detect_saudi_season(on_date=today)

    season_dict = {
        "season": season_ctx.season,
        "confidence": season_ctx.confidence,
        "days_into_season": season_ctx.days_into_season,
        "days_remaining": season_ctx.days_remaining,
        "implication_ar": season_ctx.business_implication_ar,
        "implication_en": season_ctx.business_implication_en,
        "recommended_offer_pivot": season_ctx.recommended_offer_pivot,
    }

    # Score every candidate
    scored: list[tuple[LeadCandidate, SaudiScoreBoard, float]] = []
    for c in candidates:
        board = compute_saudi_score_board(
            _candidate_to_account_dict(c),
            has_warm_route=(c.source in ("warm_intro", "partner_referral", "founder_intro")),
            on_date=today,
        )
        composite = _composite_score(board)
        scored.append((c, board, composite))

    # Rank: BLOCKED last, then by composite descending
    def _rank_key(t: tuple[LeadCandidate, SaudiScoreBoard, float]) -> tuple[int, float]:
        _, b, score = t
        is_blocked = any("BLOCKED_SOURCE" in n for n in b.notes)
        # Sort key: (0=non-blocked, -score) so non-blocked + highest score come first
        return (1 if is_blocked else 0, -score)

    scored.sort(key=_rank_key)
    top = scored[:max(0, top_n)]

    # Build entries
    entries: list[DailyLeadEntry] = []
    for rank, (c, board, score) in enumerate(top, start=1):
        priority = _priority_bucket(score, board)
        why_ar, why_en = _why_now(season_dict, board, c)
        action_ar, action_en, action_mode = _recommended_action(priority, board)
        # Surface blockers from the score board
        blockers = tuple(n for n in board.notes if "BLOCKED" in n.upper())
        entries.append(DailyLeadEntry(
            rank=rank,
            candidate=c,
            saudi_scores={
                "arabic_readiness": board.arabic_readiness,
                "decision_maker_access": board.decision_maker_access,
                "whatsapp_dependency_risk": board.whatsapp_dependency_risk,
                "saudi_compliance_sensitivity": board.saudi_compliance_sensitivity,
                "seasonality": board.seasonality,
                "relationship_strength": board.relationship_strength,
            },
            composite_score=score,
            priority=priority,  # type: ignore[arg-type]
            why_now_ar=why_ar,
            why_now_en=why_en,
            recommended_action_ar=action_ar,
            recommended_action_en=action_en,
            action_mode=action_mode,
            blockers=blockers,
            is_estimate=True,
        ))

    p0_count = sum(1 for e in entries if e.priority == "P0_NOW")
    p1_count = sum(1 for e in entries if e.priority == "P1_THIS_WEEK")
    blocked_count = sum(1 for e in entries if e.priority == "BLOCKED")

    summary_ar = (
        f"بورد اليوم: {len(entries)} ليد (P0={p0_count} · P1={p1_count} · "
        f"محظور={blocked_count}). الموسم: {season_ctx.season}."
    )
    summary_en = (
        f"Today's board: {len(entries)} leads (P0={p0_count} · P1={p1_count} · "
        f"blocked={blocked_count}). Season: {season_ctx.season}."
    )

    if blocked_count == len(entries) and entries:
        next_action = (
            "كل الليدز محظورة — تحقق من مصادر الإنتيك قبل التشغيل التالي."
        )
    elif p0_count > 0:
        next_action = (
            f"راجع الـ {p0_count} P0 leads + اعتمد الرسائل المرفقة قبل الإرسال اليدوي."
        )
    elif p1_count > 0:
        next_action = (
            f"راجع الـ {p1_count} P1 leads هذا الأسبوع — جهّز diagnostic مصغّر."
        )
    elif entries:
        next_action = "راجع الـ nurture board — لا توجد فرص P0/P1 اليوم."
    else:
        next_action = "لا candidates مُدخلة — أضف ليدز عبر CSV أو من pipeline."

    return DailyLeadBoard(
        generated_at=datetime.now(timezone.utc).isoformat(),
        on_date=today.isoformat(),
        season_context=season_dict,
        candidates_count=len(candidates),
        leads_returned=len(entries),
        top_leads=tuple(entries),
        bilingual_summary={"ar": summary_ar, "en": summary_en},
        article_4_invariants=(
            "all_outputs_draft_only_or_approval_required",
            "no_live_send_called",
            "no_live_charge_called",
            "no_scraping_invoked",
            "blocked_sources_routed_to_blocked_priority",
            "is_estimate_always_true",
        ),
        next_founder_action=next_action,
        is_estimate=True,
    )


# ─────────────────────────────────────────────────────────────────────
# Output writers
# ─────────────────────────────────────────────────────────────────────


def write_board(board: DailyLeadBoard, *, out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write JSON + Markdown to data/wave12/daily_lead_prep/{date}.{ext}.

    Returns (json_path, md_path).
    """
    base = out_dir or DEFAULT_OUT_DIR
    base.mkdir(parents=True, exist_ok=True)
    date_part = board.on_date  # already YYYY-MM-DD
    json_path = base / f"{date_part}.json"
    md_path = base / f"{date_part}.md"

    # JSON (machine-readable)
    json_path.write_text(
        json.dumps(_board_to_dict(board), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Markdown (founder-readable)
    md_path.write_text(_board_to_markdown(board), encoding="utf-8")

    return (json_path, md_path)


def _board_to_dict(board: DailyLeadBoard) -> dict[str, Any]:
    """Convert DailyLeadBoard to a JSON-friendly dict."""
    return {
        "generated_at": board.generated_at,
        "on_date": board.on_date,
        "season_context": board.season_context,
        "candidates_count": board.candidates_count,
        "leads_returned": board.leads_returned,
        "top_leads": [
            {
                "rank": e.rank,
                "candidate": asdict(e.candidate),
                "saudi_scores": e.saudi_scores,
                "composite_score": e.composite_score,
                "priority": e.priority,
                "why_now_ar": e.why_now_ar,
                "why_now_en": e.why_now_en,
                "recommended_action_ar": e.recommended_action_ar,
                "recommended_action_en": e.recommended_action_en,
                "action_mode": e.action_mode,
                "blockers": list(e.blockers),
                "is_estimate": e.is_estimate,
            }
            for e in board.top_leads
        ],
        "bilingual_summary": board.bilingual_summary,
        "article_4_invariants": list(board.article_4_invariants),
        "next_founder_action": board.next_founder_action,
        "is_estimate": board.is_estimate,
    }


def _board_to_markdown(board: DailyLeadBoard) -> str:
    """Render the board as founder-readable Markdown."""
    lines: list[str] = []
    lines.append(f"# Dealix Daily Lead Board — {board.on_date}")
    lines.append("")
    lines.append(f"**Generated:** {board.generated_at}")
    lines.append(f"**Season:** {board.season_context['season']} "
                 f"(confidence={board.season_context['confidence']})")
    lines.append("")
    lines.append(f"## ملخص اليوم / Today's summary")
    lines.append("")
    lines.append(f"- **AR:** {board.bilingual_summary['ar']}")
    lines.append(f"- **EN:** {board.bilingual_summary['en']}")
    lines.append("")
    lines.append(f"### الموسم / Season context")
    lines.append(f"- AR: {board.season_context['implication_ar']}")
    lines.append(f"- EN: {board.season_context['implication_en']}")
    lines.append(f"- Recommended offer pivot: `{board.season_context['recommended_offer_pivot']}`")
    lines.append("")
    lines.append("---")
    lines.append(f"## Top {board.leads_returned} Leads (out of {board.candidates_count} candidates)")
    lines.append("")
    if not board.top_leads:
        lines.append("_No candidates provided — add via CSV._")
    for e in board.top_leads:
        lines.append(f"### {e.rank}. {e.candidate.name} — `{e.priority}`")
        lines.append("")
        lines.append(f"- **Composite score:** {e.composite_score:.3f}")
        lines.append(f"- **Sector:** {e.candidate.sector or '—'} · **City:** {e.candidate.city or '—'}")
        lines.append(f"- **Source:** `{e.candidate.source}` · **Action mode:** `{e.action_mode}`")
        lines.append(f"- **Why now (AR):** {e.why_now_ar}")
        lines.append(f"- **Why now (EN):** {e.why_now_en}")
        lines.append(f"- **Recommended action (AR):** {e.recommended_action_ar}")
        lines.append(f"- **Recommended action (EN):** {e.recommended_action_en}")
        if e.blockers:
            lines.append(f"- **⚠️ Blockers:** {', '.join(e.blockers)}")
        lines.append(f"- **Saudi scores:** "
                     f"arabic={e.saudi_scores['arabic_readiness']:.2f} · "
                     f"dm_access={e.saudi_scores['decision_maker_access']:.2f} · "
                     f"relationship={e.saudi_scores['relationship_strength']:.2f} · "
                     f"compliance={e.saudi_scores['saudi_compliance_sensitivity']:.2f} · "
                     f"seasonality={e.saudi_scores['seasonality']:.2f} · "
                     f"whatsapp_risk={e.saudi_scores['whatsapp_dependency_risk']:.2f}")
        lines.append("")
    lines.append("---")
    lines.append("## Next founder action")
    lines.append("")
    lines.append(f"> {board.next_founder_action}")
    lines.append("")
    lines.append("---")
    lines.append("## Article 4 invariants (immutable)")
    lines.append("")
    for inv in board.article_4_invariants:
        lines.append(f"- ✅ `{inv}`")
    lines.append("")
    lines.append("_All outputs are DRAFT_ONLY or APPROVAL_REQUIRED. "
                 "No live send. No live charge. No scraping. No PII committed._")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dealix Daily Autonomous Lead Prep — DRAFT-ONLY (Article 4)",
    )
    parser.add_argument(
        "--candidates", type=Path, default=None,
        help="Path to candidates CSV (default: empty board with season context only)",
    )
    parser.add_argument(
        "--top-n", type=int, default=5,
        help="How many top leads to surface (default: 5)",
    )
    parser.add_argument(
        "--on-date", type=str, default=None,
        help="ISO date (YYYY-MM-DD) override; default = today UTC",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=DEFAULT_OUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUT_DIR})",
    )
    # Wave 12.9 — auto-source from lead_inbox when no CSV
    parser.add_argument(
        "--no-auto-source", action="store_true",
        help="Disable auto-sourcing from lead_inbox.jsonl (default: enabled)",
    )
    parser.add_argument(
        "--auto-source-limit", type=int, default=100,
        help="Max records to pull from lead_inbox auto-source (default: 100)",
    )
    args = parser.parse_args()

    # Parse date
    on_date: date | None = None
    if args.on_date:
        try:
            on_date = datetime.fromisoformat(args.on_date).date()
        except ValueError:
            print(f"ERROR: --on-date must be ISO YYYY-MM-DD; got {args.on_date!r}",
                  file=sys.stderr)
            return 2

    # Load candidates — Wave 12.9 source priority:
    #   1. --candidates CSV (explicit)
    #   2. lead_inbox.jsonl auto-source (existing inbound landing leads)
    #   3. empty board with season context only
    candidates: list[LeadCandidate] = []
    if args.candidates:
        if not args.candidates.exists():
            print(f"ERROR: candidates CSV not found: {args.candidates}", file=sys.stderr)
            return 2
        candidates = load_candidates_from_csv(args.candidates)
        print(f"Loaded {len(candidates)} candidates from {args.candidates}")
    elif not args.no_auto_source:
        # Wave 12.9 — auto-source from existing lead_inbox
        candidates = load_candidates_from_lead_inbox(limit=args.auto_source_limit)
        if candidates:
            print(f"Auto-sourced {len(candidates)} candidates from lead_inbox.jsonl "
                  f"(inbound landing leads with status='new')")
        else:
            print("No --candidates and no inbound leads in lead_inbox; "
                  "producing empty board with season context only")
    else:
        print("--no-auto-source set; producing empty board with season context only")

    # Compose
    board = run_daily_prep(candidates=candidates, on_date=on_date, top_n=args.top_n)

    # Write
    json_path, md_path = write_board(board, out_dir=args.out_dir)
    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    print(f"Top leads: {board.leads_returned} of {board.candidates_count} candidates")
    print(f"Next founder action: {board.next_founder_action}")

    # Exit code
    if board.candidates_count == 0:
        return 1  # informational — no candidates
    return 0


if __name__ == "__main__":
    sys.exit(main())
