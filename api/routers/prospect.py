"""
Prospect discovery endpoint — public, rate-limited.

POST /api/v1/prospect/discover
    body: {"icp": str, "use_case": "sales|partnership|collaboration|investor|b2c_audience", "count": 10}
    returns: ProspectResult JSON

POST /api/v1/prospect/demo
    returns: a canned demo result (no LLM call) for instant landing UI preview
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agents.prospector import (
    MAX_COUNT,
    USE_CASES,
    ProspectorAgent,
)
from auto_client_acquisition.agents.rules_router import (
    generate_messages as _rules_generate_messages,
    route_account as _rules_route,
)
from auto_client_acquisition.connectors.google_search import google_search
from auto_client_acquisition.connectors.tech_detect import detect_stack

router = APIRouter(prefix="/api/v1/prospect", tags=["prospect"])
log = logging.getLogger(__name__)

_agent = ProspectorAgent()


@router.get("/use-cases")
async def list_use_cases() -> dict[str, Any]:
    return {"use_cases": USE_CASES, "max_count": MAX_COUNT}


@router.post("/discover")
async def discover(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    icp = str(body.get("icp") or "").strip()
    use_case = str(body.get("use_case") or "sales").strip().lower()
    count = int(body.get("count") or 10)

    if len(icp) < 20:
        raise HTTPException(
            status_code=400,
            detail="icp_too_short: provide at least 20 characters describing your ideal customer",
        )
    if len(icp) > 2000:
        raise HTTPException(
            status_code=400,
            detail="icp_too_long: keep ICP under 2000 characters",
        )
    if use_case not in USE_CASES:
        raise HTTPException(
            status_code=400,
            detail=f"unknown_use_case: {use_case}. Valid: {list(USE_CASES.keys())}",
        )
    if count < 1 or count > MAX_COUNT:
        raise HTTPException(
            status_code=400,
            detail=f"count_out_of_range: 1..{MAX_COUNT}",
        )

    try:
        result = await _agent.run(icp=icp, use_case=use_case, count=count)
    except Exception as exc:
        log.warning("prospector_llm_unavailable use_case=%s — serving degraded rules mode", use_case)
        # Degraded mode: serve the canned demo with a status flag
        demo_resp = await demo()
        demo_resp["status"] = "degraded"
        demo_resp["reason"] = "missing_llm_key"
        demo_resp["hint"] = "Add GROQ_API_KEY (or ANTHROPIC_API_KEY) in Railway env 'Dealix' service 'web' to enable live discovery."
        demo_resp["error_type"] = type(exc).__name__
        return demo_resp

    return result.to_dict()


@router.get("/search-diag")
async def search_diag() -> dict[str, Any]:
    """Diagnose env var presence without revealing values."""
    import os
    k = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    c = os.getenv("GOOGLE_SEARCH_CX", "")
    m = os.getenv("MOYASAR_SECRET_KEY", "")
    w = os.getenv("MOYASAR_WEBHOOK_SECRET", "")

    # Also list ALL env vars whose names start with target prefixes — helps detect typos
    related = sorted([
        name for name in os.environ.keys()
        if name.startswith(("GOOGLE_", "MOYASAR_", "ANTHROPIC_", "POSTHOG_", "SENTRY_", "DATABASE_", "APP_URL", "PORT", "RAILWAY_"))
    ])
    return {
        "GOOGLE_SEARCH_API_KEY": {"set": bool(k), "length": len(k), "prefix": (k[:6] + "...") if k else ""},
        "GOOGLE_SEARCH_CX":      {"set": bool(c), "length": len(c), "prefix": (c[:6] + "...") if c else ""},
        "MOYASAR_SECRET_KEY":    {"set": bool(m), "length": len(m), "prefix": (m[:6] + "...") if m else ""},
        "MOYASAR_WEBHOOK_SECRET":{"set": bool(w), "length": len(w)},
        "all_visible_env_var_names_starting_with_known_prefixes": related,
        "railway_environment_name": os.getenv("RAILWAY_ENVIRONMENT_NAME", "(not set)"),
        "railway_service_name": os.getenv("RAILWAY_SERVICE_NAME", "(not set)"),
        "railway_project_name": os.getenv("RAILWAY_PROJECT_NAME", "(not set)"),
        "hint": (
            "both_google_ok" if k and c else
            "api_key_missing_or_empty" if not k else
            "cx_missing_or_empty"
        ),
    }


@router.post("/search")
async def search(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Run a Google Custom Search query using server-side keys.
    Body: {"query": "...", "num": 10, "site": "linkedin.com" (optional), "lang": "ar"|"en"}
    Returns: SearchResponse JSON.
    """
    q = str(body.get("query") or "").strip()
    if len(q) < 3 or len(q) > 500:
        raise HTTPException(status_code=400, detail="query_length_out_of_range")

    num = int(body.get("num") or 10)
    if num < 1 or num > 10:
        raise HTTPException(status_code=400, detail="num_out_of_range: 1..10")

    site = body.get("site")
    site = str(site).strip() if site else None
    lang = body.get("lang")
    lang = str(lang).strip().lower() if lang else None
    if lang and lang not in {"ar", "en", "fr", "es"}:
        raise HTTPException(status_code=400, detail="unsupported_lang")

    try:
        resp = await google_search(q, num=num, site=site, lang=lang, timeout=10.0)
    except Exception as exc:  # noqa: BLE001
        log.exception("google_search_call_failed q=%r", q)
        raise HTTPException(status_code=502, detail="search_error") from exc

    if resp.status == "no_keys":
        raise HTTPException(status_code=503, detail="search_not_configured")

    return resp.to_dict()


@router.post("/enrich-tech")
async def enrich_tech(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Detect tech stack for a domain using Dealix native detector (free, self-hosted).
    Body: {"domain": "foodics.com", "extra_paths": ["/careers", "/contact"]}
    """
    domain = str(body.get("domain") or "").strip()
    extra = body.get("extra_paths") or []
    if not isinstance(extra, list):
        extra = []
    extra = [str(p)[:80] for p in extra[:5]]

    if not domain or "." not in domain or len(domain) > 200:
        raise HTTPException(status_code=400, detail="invalid_domain")

    try:
        result = await detect_stack(domain, timeout=10.0, extra_paths=extra)
    except Exception as exc:  # noqa: BLE001
        log.exception("tech_detect_failed domain=%s", domain)
        raise HTTPException(status_code=502, detail="tech_detect_error") from exc
    return result.to_dict()


@router.post("/enrich-domain")
async def enrich_domain(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    End-to-end enrichment: given a domain + opportunity hint, combine tech stack
    detection + LLM analysis to return a full lead record per LEAD_OUTPUT_SCHEMA.

    Body:
      {
        "domain": "foodics.com",
        "opportunity_hint": "DIRECT_CUSTOMER|AGENCY_PARTNER|..." (optional),
        "context_notes": "optional extra human context"
      }

    Returns: full lead object (opportunity_type, scores, signals, outreach opening, etc.)
    """
    domain = str(body.get("domain") or "").strip()
    opportunity_hint = str(body.get("opportunity_hint") or "").strip().upper()
    context_notes = str(body.get("context_notes") or "").strip()[:1000]

    if not domain or "." not in domain or len(domain) > 200:
        raise HTTPException(status_code=400, detail="invalid_domain")

    # Step 1 — tech detection (free, always available)
    try:
        tech = await detect_stack(domain, timeout=10.0, extra_paths=["/careers", "/about"])
    except Exception:
        log.exception("tech_detect_failed domain=%s", domain)
        tech = None

    tech_dict = tech.to_dict() if tech else {"tools": [], "signals": [], "status": "unavailable"}

    # Step 2 — LLM analysis using ProspectorAgent-style prompt but domain-scoped
    from auto_client_acquisition.agents.prospector import ProspectorAgent, USE_CASES

    agent = ProspectorAgent()
    icp_text = (
        f"الشركة: {domain}\n"
        f"الأدوات المكتشفة عبر tech detector: "
        f"{', '.join(t['name'] for t in tech_dict.get('tools', []))}\n"
        f"الإشارات المستخرجة: "
        f"{', '.join(s['evidence'] for s in tech_dict.get('signals', []))}\n"
        + (f"سياق إضافي: {context_notes}\n" if context_notes else "")
        + (f"تلميح لنوع الفرصة: {opportunity_hint}\n" if opportunity_hint else "")
        + "\nحلّل هذه الشركة تحديداً: صنّف نوع الفرصة، احسب ال 4 scores، اقترح sequence من الخطوات، وأعد نفس شكل JSON كما هو محدد."
    )
    use_case = "sales"  # default; the LLM will classify opportunity_type freely

    try:
        result = await agent.run(icp=icp_text, use_case=use_case, count=1)
        leads = result.leads
        lead_dict = leads[0].to_dict() if leads else None
        search_notes = result.search_notes
        status = "ok"
    except Exception:
        log.warning("enrich_domain_llm_unavailable domain=%s — serving tech-only + rules", domain)
        # Degraded: run rules router over the tech signals to still produce actionable lead
        signals_for_router = [
            {"name": s.get("name", ""), "weight": s.get("weight", 0), "evidence": s.get("evidence", "")}
            for s in tech_dict.get("signals", [])
        ]
        res = _rules_route(
            company=domain.split(".")[0].replace("-", " ").title(),
            sector="",
            country="SA",
            domain=domain,
            signals=signals_for_router,
            tags="",
            decision_maker=None,
        )
        # Also produce messages deterministically
        msgs = _rules_generate_messages(
            company=domain.split(".")[0].replace("-", " ").title(),
            decision_maker=None,
            opportunity_type=res.opportunity_type,
            signals=signals_for_router,
        )
        lead_dict = {
            **res.to_dict(),
            "company_en": domain.split(".")[0].replace("-", " ").title(),
            "company_ar": "",
            "website": f"https://{domain}",
            "outreach_opening": msgs["linkedin"][:280],
            "signals": signals_for_router,
            "confidence": 60,
        }
        search_notes = "degraded mode — rules router + tech detect only (no LLM key)"
        status = "degraded"

    return {
        "domain": domain,
        "tech": tech_dict,
        "lead": lead_dict,
        "search_notes": search_notes,
        "fetched_at": tech_dict.get("fetched_at"),
        "status": status,
    }


@router.post("/route")
async def route_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Deterministic rule-based router — classify + score + route an account without LLM.
    Body: {company, sector?, country?, domain?, signals?, tags?, decision_maker?, size_hint?, is_government?, desired_goal?}
    """
    company = str(body.get("company") or "").strip()
    if not company:
        raise HTTPException(status_code=400, detail="company_required")
    res = _rules_route(
        company=company,
        sector=str(body.get("sector") or ""),
        country=str(body.get("country") or ""),
        domain=str(body.get("domain") or ""),
        signals=body.get("signals") or [],
        tags=str(body.get("tags") or ""),
        decision_maker=body.get("decision_maker"),
        size_hint=str(body.get("size_hint") or ""),
        is_government=bool(body.get("is_government") or False),
        desired_goal=body.get("desired_goal"),
    )
    return {"mode": "rules", "result": res.to_dict()}


@router.post("/score")
async def score_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Score an account against the 100-pt ICP model. Same inputs as /route.
    Returns only the score breakdown (no messages).
    """
    company = str(body.get("company") or "").strip()
    if not company:
        raise HTTPException(status_code=400, detail="company_required")
    res = _rules_route(
        company=company,
        sector=str(body.get("sector") or ""),
        country=str(body.get("country") or ""),
        domain=str(body.get("domain") or ""),
        signals=body.get("signals") or [],
        tags=str(body.get("tags") or ""),
        decision_maker=body.get("decision_maker"),
        size_hint=str(body.get("size_hint") or ""),
        is_government=bool(body.get("is_government") or False),
    )
    r = res.to_dict()
    return {
        "company": company,
        "fit_score": r["fit_score"],
        "intent_score": r["intent_score"],
        "access_score": r["access_score"],
        "revenue_score": r["revenue_score"],
        "priority_score": r["priority_score"],
        "priority_tier": r["priority_tier"],
        "risk_level": r["risk_level"],
        "opportunity_type": r["opportunity_type"],
        "reason": r["reason"],
    }


@router.post("/message")
async def message_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Generate templated, signal-aware Arabic outreach for an account.
    Body: {company, decision_maker?, opportunity_type?, signals?}
    Returns: {linkedin, email, whatsapp_warm_only, follow_up_plus_2/5/10}
    """
    company = str(body.get("company") or "").strip()
    if not company:
        raise HTTPException(status_code=400, detail="company_required")

    opp = str(body.get("opportunity_type") or "").strip().upper()
    if not opp:
        # Fall back: classify via rules
        res = _rules_route(
            company=company,
            sector=str(body.get("sector") or ""),
            tags=str(body.get("tags") or ""),
            signals=body.get("signals") or [],
        )
        opp = res.opportunity_type

    msgs = _rules_generate_messages(
        company=company,
        decision_maker=body.get("decision_maker"),
        opportunity_type=opp,
        signals=body.get("signals") or [],
    )
    return {"mode": "rules", "opportunity_type": opp, "messages": msgs}


@router.post("/bulk-enrich")
async def bulk_enrich(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Bulk tech-detect enrichment for a list of domains.
    Body: {"domains": ["foodics.com", "salla.sa", ...], "concurrency": 5}
    Returns: {"results": {domain: tech_result, ...}, "summary": {...}}

    Hard limit: 25 domains per request (prevent abuse).
    """
    domains_raw = body.get("domains") or []
    if not isinstance(domains_raw, list):
        raise HTTPException(status_code=400, detail="domains_must_be_list")

    domains = [str(d).strip() for d in domains_raw if d and "." in str(d)]
    domains = list(dict.fromkeys(domains))[:25]  # dedupe, cap

    if not domains:
        raise HTTPException(status_code=400, detail="no_valid_domains")

    concurrency = int(body.get("concurrency") or 5)
    concurrency = max(1, min(10, concurrency))

    import asyncio as _asyncio
    sem = _asyncio.Semaphore(concurrency)

    async def _one(d: str) -> tuple[str, dict]:
        async with sem:
            try:
                r = await detect_stack(d, timeout=10.0)
                return d, r.to_dict()
            except Exception as exc:  # noqa: BLE001
                return d, {"status": "error", "error": str(exc), "domain": d}

    pairs = await _asyncio.gather(*(_one(d) for d in domains))
    results = dict(pairs)

    total_tools = sum(len(r.get("tools", [])) for r in results.values())
    total_signals = sum(len(r.get("signals", [])) for r in results.values())
    ok_count = sum(1 for r in results.values() if r.get("status") == "ok")

    return {
        "summary": {
            "domains_requested": len(domains),
            "ok_count": ok_count,
            "total_tools_detected": total_tools,
            "total_signals_detected": total_signals,
        },
        "results": results,
    }


@router.post("/demo")
async def demo() -> dict[str, Any]:
    """Canned demo response for landing UI preview. No LLM call."""
    return {
        "use_case": "sales",
        "icp": "شركات SaaS سعودية B2B بحجم 20-100 موظف تبيع للمطاعم",
        "count_requested": 3,
        "count_returned": 3,
        "search_notes": "نتائج توضيحية — جرب الواجهة الحقيقية للحصول على قائمة مخصصة لمواصفاتك.",
        "leads": [
            {
                "company_ar": "فودكس",
                "company_en": "Foodics",
                "industry": "SaaS للمطاعم",
                "est_size": "200-1000",
                "website": "https://www.foodics.com",
                "linkedin": "https://www.linkedin.com/company/foodics",
                "decision_maker_hints": ["Ahmad Al-Zaini — CEO", "Mosab Alothmani — Co-founder"],
                "signals": ["جولة Series C بـ $170M 2025", "توسع في الخليج وشمال أفريقيا"],
                "outreach_opening": "أحمد، مبروك Series C — 170M = فرصة مضاعفة السرعة في onboarding العملاء الجدد.",
                "fit_score": 92,
                "confidence": 90,
                "evidence": "شركة SaaS سعودية واضحة، تستهدف restaurant operators، بحجم يطابق الـ ICP.",
            },
            {
                "company_ar": "رُكاز",
                "company_en": "Rekaz",
                "industry": "SaaS للـ SMB",
                "est_size": "10-50",
                "website": "https://rekaz.io",
                "linkedin": None,
                "decision_maker_hints": ["Abdullah Al-Shalan — Founder"],
                "signals": ["منصة متخصصة في إدارة المستودعات للتجار"],
                "outreach_opening": "عبدالله، رُكاز تبني الطبقة التشغيلية للتاجر السعودي — هذا تماماً مكان AI sales rep بالعربي.",
                "fit_score": 85,
                "confidence": 75,
                "evidence": "SMB-focused SaaS سعودي ضمن الحجم المطلوب.",
            },
            {
                "company_ar": "زد",
                "company_en": "Zid",
                "industry": "E-commerce Platform",
                "est_size": "200-1000",
                "website": "https://zid.sa",
                "linkedin": "https://www.linkedin.com/company/zidsa",
                "decision_maker_hints": ["Sultan Mofarreh — Co-founder"],
                "signals": ["منافس لسلة مع 15K تاجر+", "ركّز على SMB merchants"],
                "outreach_opening": "سلطان، 15K تاجر = فرصة توزيع هائلة لـ AI sales rep داخل zid marketplace.",
                "fit_score": 88,
                "confidence": 85,
                "evidence": "منصة تجارة إلكترونية سعودية راسخة ضمن الحجم المطلوب.",
            },
        ],
    }
