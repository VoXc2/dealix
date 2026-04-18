#!/usr/bin/env python3
"""
عرض توضيحي لمحرك استخبارات الـ Leads — Dealix Intelligence Engine Demo
=========================================================================
يُظهر:
  1. اكتشاف شركات من قطاعات مختلفة
  2. إثراء البيانات (Etimad، LinkedIn، أخبار، توظيف، تقنيات)
  3. تسجيل النقاط مع الشرح الكامل
  4. عرض النتائج في جدول عربي منسّق (rich library)
  5. حفظ النتائج في JSON

Run::
    cd /home/user/workspace/dealix-clean/backend
    python scripts/run_intelligence_demo.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from app.intelligence import (
    IntelligenceOrchestrator,
    DiscoveryCriteria,
    Sector,
    Region,
    Company,
    SocialHandles,
    Contact,
    FundingEvent,
    EstablishmentType,
    Lead,
)

console = Console()

# ─────────────────────────── Demo Companies ──────────────────────────────────
# 5 example companies from different sectors to demonstrate the engine.

DEMO_COMPANIES: list[Company] = [
    Company(
        name="Salla",
        name_ar="سلة",
        domain="salla.com",
        website="https://salla.com",
        sector=Sector.B2B_SAAS,
        sub_sector="ecommerce platform",
        region=Region.MAKKAH,
        city="Jeddah",
        city_ar="جدة",
        employee_count=350,
        revenue_estimate_sar=120_000_000,
        ceo_name="Salah Al-Deen Al-Majali",
        ceo_name_ar="صلاح الدين المجالي",
        tech_stack=["Laravel", "Vue.js", "AWS", "Redis"],
        ecommerce_platform="Custom",
        social_handles=SocialHandles(
            linkedin="company/sallaksa",
            twitter="salla",
            instagram="salla",
        ),
        decision_makers=[
            Contact(
                full_name="Salah Al-Deen Al-Majali",
                full_name_ar="صلاح الدين المجالي",
                title="CEO",
                seniority="c_level",
                is_decision_maker=True,
                linkedin_url="https://linkedin.com/in/salla-ceo",
            )
        ],
    ),
    Company(
        name="Foodics",
        name_ar="فودكس",
        domain="foodics.com",
        website="https://foodics.com",
        sector=Sector.B2B_SAAS,
        sub_sector="restaurant management software",
        region=Region.RIYADH,
        city="Riyadh",
        city_ar="الرياض",
        employee_count=400,
        revenue_estimate_sar=150_000_000,
        ceo_name="Ahmad Al-Zaini",
        ceo_name_ar="أحمد الزيني",
        tech_stack=["React", "Ruby on Rails", "PostgreSQL", "AWS", "HubSpot"],
        social_handles=SocialHandles(
            linkedin="company/foodics",
            twitter="FoodicsApp",
        ),
        funding_events=[
            FundingEvent(
                round_type="Series C",
                amount_usd=170_000_000,
                investors=["Prosus", "STV", "Sequoia"],
                announced_at=datetime(2024, 1, 10),
            )
        ],
    ),
    Company(
        name="Tabby",
        name_ar="تابي",
        domain="tabby.ai",
        website="https://tabby.ai",
        sector=Sector.FINANCIAL_SERVICES,
        sub_sector="BNPL fintech",
        region=Region.RIYADH,
        city="Riyadh",
        city_ar="الرياض",
        employee_count=500,
        revenue_estimate_sar=280_000_000,
        ceo_name="Hosam Arab",
        ceo_name_ar="حسام عرب",
        tech_stack=["React", "Node.js", "PostgreSQL", "AWS", "Stripe", "Braze"],
        social_handles=SocialHandles(
            linkedin="company/tabby-fintech",
            twitter="tabby",
            instagram="tabby",
        ),
        decision_makers=[
            Contact(
                full_name="Hosam Arab",
                title="CEO & Co-Founder",
                seniority="c_level",
                is_decision_maker=True,
                linkedin_url="https://linkedin.com/in/hosamArab",
            ),
            Contact(
                full_name="Daniil Barkalov",
                title="CTO",
                seniority="c_level",
                is_decision_maker=True,
            ),
        ],
        funding_events=[
            FundingEvent(
                round_type="Series D",
                amount_usd=200_000_000,
                investors=["Hassana Investment Company", "Mubadala"],
                announced_at=datetime(2024, 2, 20),
            )
        ],
    ),
    Company(
        name="ROSHN",
        name_ar="روشن",
        domain="roshn.sa",
        website="https://roshn.sa",
        sector=Sector.REAL_ESTATE,
        sub_sector="mega real estate developer",
        region=Region.RIYADH,
        city="Riyadh",
        city_ar="الرياض",
        employee_count=1000,
        revenue_estimate_sar=5_000_000_000,
        ceo_name="David Grover",
        tech_stack=["Salesforce", "Oracle", "SAP", "BIM 360"],
        social_handles=SocialHandles(
            linkedin="company/roshn",
            twitter="ROSHNsa",
            instagram="roshn_sa",
        ),
    ),
    Company(
        name="Noon Academy",
        name_ar="أكاديمية نون",
        domain="noonacademy.com",
        website="https://noonacademy.com",
        sector=Sector.EDUCATION,
        sub_sector="edtech",
        region=Region.RIYADH,
        city="Riyadh",
        city_ar="الرياض",
        employee_count=200,
        revenue_estimate_sar=60_000_000,
        tech_stack=["React Native", "AWS", "Firebase", "Node.js"],
        social_handles=SocialHandles(
            linkedin="company/noon-academy",
            twitter="NoonAcademy",
            instagram="noonacademy",
        ),
    ),
]


# ─────────────────────────── Display Helpers ─────────────────────────────────


def priority_color(tier: str | None) -> str:
    return {
        "hot": "bold red",
        "warm": "bold yellow",
        "cool": "bold cyan",
        "cold": "dim blue",
    }.get(tier or "cold", "white")


def priority_ar(tier: str | None) -> str:
    return {
        "hot": "🔥 حارّ",
        "warm": "🟠 ساخن",
        "cool": "🟡 دافئ",
        "cold": "🔵 بارد",
    }.get(tier or "cold", "غير محدد")


def sector_ar(sector: Sector) -> str:
    return {
        Sector.ECOMMERCE: "تجارة إلكترونية",
        Sector.DIGITAL_AGENCY: "وكالة رقمية",
        Sector.REAL_ESTATE: "عقارات",
        Sector.B2B_SAAS: "B2B SaaS",
        Sector.HEALTHCARE: "رعاية صحية",
        Sector.FINANCIAL_SERVICES: "خدمات مالية",
        Sector.GOVERNMENT: "حكومي",
        Sector.RETAIL: "تجزئة",
        Sector.LOGISTICS: "لوجستيات",
        Sector.EDUCATION: "تعليم",
        Sector.TECHNOLOGY: "تقنية",
        Sector.TELECOM: "اتصالات",
        Sector.ENERGY: "طاقة",
        Sector.OTHER: "أخرى",
    }.get(sector, sector.value)


def build_results_table(leads: list[Lead]) -> Table:
    """بناء جدول النتائج الرئيسي."""
    table = Table(
        title="[bold]نتائج محرك استخبارات Leads — Dealix[/bold]",
        box=box.DOUBLE_EDGE,
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
        show_lines=True,
        padding=(0, 1),
    )

    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("الشركة", style="bold white", min_width=20)
    table.add_column("القطاع", style="cyan", min_width=14)
    table.add_column("المدينة", style="dim", width=10)
    table.add_column("الموظفون", justify="right", width=10)
    table.add_column("الإيرادات (م ر.س)", justify="right", min_width=14)
    table.add_column("Dealix Score", justify="center", min_width=14)
    table.add_column("الأولوية", justify="center", min_width=10)
    table.add_column("ICP", justify="right", width=6)
    table.add_column("Intent", justify="right", width=7)
    table.add_column("Budget", justify="right", width=7)

    for i, lead in enumerate(leads, 1):
        c = lead.company
        s = lead.score

        revenue = c.revenue_estimate_sar
        rev_str = f"{revenue/1_000_000:.0f}م" if revenue else "—"
        emp_str = f"{c.employee_count:,}" if c.employee_count else "—"

        # Score bar
        score = lead.dealix_score
        filled = int(score / 10)
        bar = "█" * filled + "░" * (10 - filled)
        score_text = Text()
        score_text.append(f"{score:.0f}", style=priority_color(lead.priority_tier))
        score_text.append(f" {bar}", style="dim")

        table.add_row(
            str(i),
            f"[bold]{c.name_ar or c.name}[/bold]\n[dim]{c.name}[/dim]",
            sector_ar(c.sector),
            c.city_ar or c.city or "—",
            emp_str,
            rev_str,
            score_text,
            f"[{priority_color(lead.priority_tier)}]{priority_ar(lead.priority_tier)}[/]",
            f"{s.icp_score:.0f}",
            f"{s.intent_score:.0f}",
            f"{s.budget_score:.0f}",
        )

    return table


def build_score_detail_panel(lead: Lead) -> Panel:
    """بناء بانل تفصيل النتيجة لـ lead واحد."""
    s = lead.score
    c = lead.company

    lines: list[str] = [
        f"[bold cyan]{c.name_ar or c.name}[/bold cyan] — [dim]{c.sub_sector or c.sector.value}[/dim]",
        "",
        f"  النتيجة الكلية : [{priority_color(lead.priority_tier)}]{s.total_score:.1f}/100[/] {priority_ar(lead.priority_tier)}",
        "",
        f"  {'ICP':12} : {s.icp_score:>6.1f}/100  {'█' * int(s.icp_score/10)}",
        f"  {'Intent':12} : {s.intent_score:>6.1f}/100  {'█' * int(s.intent_score/10)}",
        f"  {'Timing':12} : {s.timing_score:>6.1f}/100  {'█' * int(s.timing_score/10)}",
        f"  {'Budget':12} : {s.budget_score:>6.1f}/100  {'█' * int(s.budget_score/10)}",
        f"  {'Authority':12} : {s.authority_score:>6.1f}/100  {'█' * int(s.authority_score/10)}",
        f"  {'Engagement':12} : {s.engagement_score:>6.1f}/100  {'█' * int(s.engagement_score/10)}",
    ]

    if s.contributing_signals:
        lines.extend(["", "  [green]✓ الإشارات المؤثرة:[/green]"])
        for sig in s.contributing_signals[:4]:
            lines.append(f"    [green]• {sig}[/green]")

    if s.penalizing_factors:
        lines.extend(["", "  [red]✗ عوامل الخصم:[/red]"])
        for fac in s.penalizing_factors[:3]:
            lines.append(f"    [red]• {fac}[/red]")

    content = "\n".join(lines)
    return Panel(
        content,
        title=f"[bold]تفصيل النتيجة[/bold]",
        border_style=priority_color(lead.priority_tier).replace("bold ", ""),
        padding=(0, 1),
    )


# ─────────────────────────── Main Demo ───────────────────────────────────────


async def run_demo() -> list[dict]:
    """تشغيل العرض التوضيحي الكامل."""
    console.print()
    console.print(Panel(
        "[bold yellow]🚀 Dealix Lead Intelligence Engine — عرض توضيحي[/bold yellow]\n"
        "[dim]اكتشاف · إثراء · تسجيل · ترتيب الأولويات[/dim]",
        style="on dark_blue",
        padding=(1, 4),
    ))
    console.print()

    # Initialize orchestrator (no API keys → uses seed data)
    orchestrator = IntelligenceOrchestrator()
    console.print(
        f"[dim]بيانات seed: {orchestrator.seed_company_count} شركة سعودية متاحة[/dim]\n"
    )

    # ── Step 1: Show input companies ──────────────────────────────────────
    console.print("[bold]الشركات المُختارة للعرض التوضيحي:[/bold]")
    input_table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    input_table.add_column("الشركة", style="bold cyan")
    input_table.add_column("القطاع")
    input_table.add_column("الموظفون", justify="right")
    for c in DEMO_COMPANIES:
        input_table.add_row(
            c.name_ar or c.name,
            sector_ar(c.sector),
            str(c.employee_count or "—"),
        )
    console.print(input_table)
    console.print()

    # ── Step 2: Enrich + Score ────────────────────────────────────────────
    leads: list[Lead] = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]إثراء وتسجيل الشركات...", total=len(DEMO_COMPANIES))

        for company in DEMO_COMPANIES:
            progress.update(task, description=f"[cyan]⚙ {company.name_ar or company.name}...")
            lead = await orchestrator.enrich(company)
            leads.append(lead)
            progress.advance(task)

    console.print()

    # ── Step 3: Main Results Table ────────────────────────────────────────
    # Sort by score
    leads.sort(key=lambda l: l.dealix_score, reverse=True)

    console.print(build_results_table(leads))
    console.print()

    # ── Step 4: Detail Panels for Top 3 ──────────────────────────────────
    console.print("[bold]تفصيل الـ Leads ذات الأولوية العالية:[/bold]")
    console.print()
    for lead in leads[:3]:
        console.print(build_score_detail_panel(lead))
        console.print()

    # ── Step 5: Summary Stats ─────────────────────────────────────────────
    stats_table = Table(
        title="[bold]إحصائيات العرض التوضيحي[/bold]",
        box=box.SIMPLE_HEAD,
        show_header=False,
    )
    stats_table.add_column("المقياس", style="dim")
    stats_table.add_column("القيمة", style="bold")

    hot = sum(1 for l in leads if l.priority_tier == "hot")
    warm = sum(1 for l in leads if l.priority_tier == "warm")
    cool = sum(1 for l in leads if l.priority_tier == "cool")
    cold = sum(1 for l in leads if l.priority_tier == "cold")
    avg_score = sum(l.dealix_score for l in leads) / len(leads) if leads else 0
    top_lead = max(leads, key=lambda l: l.dealix_score) if leads else None

    stats_table.add_row("إجمالي الـ leads", str(len(leads)))
    stats_table.add_row("حارّ 🔥", f"[bold red]{hot}[/bold red]")
    stats_table.add_row("ساخن 🟠", f"[bold yellow]{warm}[/bold yellow]")
    stats_table.add_row("دافئ 🟡", f"[cyan]{cool}[/cyan]")
    stats_table.add_row("بارد 🔵", f"[dim]{cold}[/dim]")
    stats_table.add_row("متوسط النتيجة", f"{avg_score:.1f}/100")
    if top_lead:
        stats_table.add_row(
            "أعلى lead",
            f"[bold]{top_lead.company.name_ar or top_lead.company.name}[/bold] ({top_lead.dealix_score:.0f})"
        )

    console.print(stats_table)
    console.print()

    # ── Step 6: Save to JSON ──────────────────────────────────────────────
    output_path = BACKEND_DIR / "data" / "intelligence_demo_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_data = {
        "generated_at": datetime.utcnow().isoformat(),
        "demo_version": "1.0.0",
        "total_leads": len(leads),
        "summary": {
            "hot": hot,
            "warm": warm,
            "cool": cool,
            "cold": cold,
            "avg_score": round(avg_score, 1),
        },
        "leads": [
            {
                "rank": i + 1,
                "company_name": lead.company.name,
                "company_name_ar": lead.company.name_ar,
                "sector": lead.company.sector.value,
                "city": lead.company.city_ar or lead.company.city,
                "employee_count": lead.company.employee_count,
                "revenue_estimate_sar": lead.company.revenue_estimate_sar,
                "dealix_score": round(lead.dealix_score, 1),
                "priority_tier": lead.priority_tier,
                "status": lead.status.value,
                "score_breakdown": {
                    "icp": lead.score.icp_score,
                    "intent": lead.score.intent_score,
                    "timing": lead.score.timing_score,
                    "budget": lead.score.budget_score,
                    "authority": lead.score.authority_score,
                    "engagement": lead.score.engagement_score,
                    "total": lead.score.total_score,
                },
                "contributing_signals": lead.score.contributing_signals[:5],
                "penalizing_factors": lead.score.penalizing_factors[:3],
                "score_rationale": lead.score.score_rationale,
                "tech_stack": lead.company.tech_stack[:5],
                "decision_makers": [
                    {
                        "name": dm.full_name,
                        "title": dm.title,
                        "seniority": dm.seniority,
                    }
                    for dm in lead.company.decision_makers[:3]
                ],
                "news_events": [
                    {
                        "headline": ne.headline_ar or ne.headline,
                        "source": ne.source_name,
                        "sentiment": ne.sentiment,
                    }
                    for ne in lead.company.last_news_events[:3]
                ],
                "hiring_signals": [
                    {
                        "job_title": hs.job_title,
                        "seniority": hs.seniority,
                        "source": hs.source,
                    }
                    for hs in lead.company.hiring_signals[:3]
                ],
                "tender_wins": [
                    {
                        "title_ar": tw.title_ar,
                        "entity": tw.entity,
                        "value_sar": tw.value_sar,
                    }
                    for tw in lead.company.tender_wins[:3]
                ],
                "social_handles": {
                    "linkedin": lead.company.social_handles.linkedin,
                    "twitter": lead.company.social_handles.twitter,
                    "instagram": lead.company.social_handles.instagram,
                },
                "data_sources": lead.company.data_sources,
                "domain": lead.company.domain,
                "website": lead.company.website,
                "ceo_name": lead.company.ceo_name,
                "ceo_name_ar": lead.company.ceo_name_ar,
            }
            for i, lead in enumerate(leads)
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)

    console.print(
        Panel(
            f"[green]✓ تم حفظ النتائج في:[/green]\n"
            f"[bold]{output_path}[/bold]",
            style="green",
        )
    )
    console.print()

    # ── Step 7: Discovery mode demo ───────────────────────────────────────
    console.print("[bold]اكتشاف شركات B2B SaaS من السجل:[/bold]")
    criteria = DiscoveryCriteria(
        sectors=[Sector.B2B_SAAS, Sector.ECOMMERCE],
        limit=5,
    )
    discovered = await orchestrator.discover(criteria)
    disc_table = Table(box=box.SIMPLE, show_header=True)
    disc_table.add_column("الشركة")
    disc_table.add_column("القطاع")
    disc_table.add_column("الموظفون", justify="right")
    disc_table.add_column("الموقع")
    for c in discovered:
        disc_table.add_row(
            c.name_ar or c.name,
            sector_ar(c.sector),
            str(c.employee_count or "—"),
            c.domain or "—",
        )
    console.print(disc_table)

    console.print()
    console.print("[bold green]✓ اكتمل العرض التوضيحي![/bold green]")
    console.print()

    return results_data["leads"]


if __name__ == "__main__":
    asyncio.run(run_demo())
