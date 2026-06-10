"""
Interactive CLI — uses Typer + Rich for a nice bilingual console experience.
واجهة سطر أوامر تفاعلية.

Usage:
    python cli.py               # interactive menu
    python cli.py status        # check app status
    python cli.py sector healthcare
    python cli.py demo          # run end-to-end demo
"""

from __future__ import annotations

import asyncio
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from auto_client_acquisition.agents.intake import LeadSource
from auto_client_acquisition.pipeline import AcquisitionPipeline
from autonomous_growth.agents.sector_intel import SaudiSector, SectorIntelAgent
from core.config.settings import get_settings
from core.llm import get_router
from core.prompts.sales_scripts import get_sales_script

app = typer.Typer(help="🏢 AI Company Saudi — CLI")
console = Console()


def _banner() -> None:
    settings = get_settings()
    console.print(
        Panel.fit(
            f"[bold cyan]🏢 {settings.app_name}[/bold cyan]\n"
            f"[dim]v{settings.app_version} · {settings.app_env}[/dim]",
            border_style="cyan",
        )
    )


# ── Commands ───────────────────────────────────────────────────
@app.command()
def status() -> None:
    """Show app status + configured LLM providers."""
    _banner()
    router = get_router()
    providers = router.available_providers()

    table = Table(title="LLM Providers", show_lines=True)
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    for provider in providers:
        table.add_row(provider.value, "✅ configured")
    if not providers:
        table.add_row("(none)", "[red]⚠️  no providers configured[/red]")
    console.print(table)


@app.command()
def sector(
    name: Annotated[str, typer.Argument(help="Sector name, e.g. healthcare")],
    enrich: Annotated[bool, typer.Option("--enrich", "-e")] = False,
) -> None:
    """Show intel for a Saudi sector."""
    _banner()
    try:
        sector_enum = SaudiSector(name)
    except ValueError:
        console.print(f"[red]Unknown sector: {name}[/red]")
        console.print(f"Available: {', '.join(s.value for s in SaudiSector)}")
        raise typer.Exit(code=1)

    agent = SectorIntelAgent()
    intel = asyncio.run(agent.run(sector=sector_enum, enrich_with_llm=enrich))

    table = Table(title=f"Sector: {intel.sector.value}", show_lines=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    table.add_row("Market size", f"{intel.market_size_sar:,.0f} SAR")
    table.add_row("Growth rate", f"{intel.growth_rate:.1%}")
    table.add_row("AI readiness", f"{intel.ai_readiness:.0%}")
    table.add_row("Key players", ", ".join(intel.key_players[:5]) or "—")
    table.add_row("Pain points", "\n".join(f"• {p}" for p in intel.pain_points[:5]))
    table.add_row("Opportunities", "\n".join(f"• {o}" for o in intel.opportunities[:5]))
    table.add_row("Vision 2030", intel.vision_2030_alignment)
    console.print(table)


@app.command()
def script(
    sector_name: Annotated[str, typer.Argument()] = "technology",
    locale: Annotated[str, typer.Option("--locale", "-l")] = "ar",
    script_type: Annotated[str, typer.Option("--type", "-t")] = "opener",
    name: Annotated[str, typer.Option("--name", "-n")] = "",
) -> None:
    """Print a bilingual sales script."""
    try:
        text = get_sales_script(
            script_type,
            locale=locale,
            name=name or ("العميل" if locale == "ar" else "there"),
            sector=sector_name,
            company="",
            date="",
            time="",
            link="",
        )
    except KeyError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
    console.print(Panel(text, title=f"{script_type} ({locale})", border_style="green"))


@app.command()
def lead(
    company: Annotated[str, typer.Option(prompt=True)] = "",
    name: Annotated[str, typer.Option(prompt=True)] = "",
    email: Annotated[str, typer.Option(prompt=True)] = "",
    sector: Annotated[str, typer.Option(prompt=True)] = "technology",
    message: Annotated[str, typer.Option(prompt=True)] = "",
) -> None:
    """Submit a lead through the full Phase 8 pipeline."""
    _banner()
    pipeline = AcquisitionPipeline()
    payload = {
        "company": company,
        "name": name,
        "email": email,
        "sector": sector,
        "region": "Saudi Arabia",
        "message": message,
    }
    with console.status("[cyan]Running pipeline...[/cyan]"):
        result = asyncio.run(pipeline.run(payload=payload, source=LeadSource.MANUAL))

    console.print(Panel("[bold]Pipeline complete[/bold]", border_style="green"))
    console.print(f"Lead ID: [cyan]{result.lead.id}[/cyan]")
    if result.fit_score:
        console.print(
            f"Fit tier: [bold]{result.fit_score.tier}[/bold] "
            f"(score {result.fit_score.overall_score:.2f})"
        )
    console.print(f"Status: {result.lead.status.value}")
    if result.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for w in result.warnings:
            console.print(f"  • {w}")


@app.command()
def demo() -> None:
    """Run an end-to-end demo: Arabic lead → full pipeline."""
    _banner()
    from scripts.run_demo import main as demo_main

    asyncio.run(demo_main())


# ── Hermes sub-app ─────────────────────────────────────────────
hermes_app = typer.Typer(help="Hermes multi-agent commands.")
app.add_typer(hermes_app, name="hermes")


@hermes_app.command("agents")
def hermes_agents() -> None:
    """List all registered Hermes agents."""
    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=get_hermes_config())

    table = Table(title="Hermes Agents", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    for info in registry.all_info():
        table.add_row(info["name"], info["description"])
    if not registry.list_agents():
        table.add_row("(none)", "[dim]no agents registered[/dim]")
    console.print(table)


@hermes_app.command("run")
def hermes_run(
    name: Annotated[str, typer.Argument(help="Agent name to run")],
    input: Annotated[
        str,
        typer.Option("--input", "-i", help="JSON string of input data"),
    ] = "{}",
) -> None:
    """Run a named Hermes agent with optional JSON input."""
    import json

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    try:
        input_data: dict = json.loads(input)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON input: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=get_hermes_config())

    try:
        agent = registry.get(name)
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    with console.status(f"[cyan]Running agent {name!r}...[/cyan]"):
        result = asyncio.run(agent.run(input_data))

    console.print_json(json.dumps(result, ensure_ascii=False, default=str))


@hermes_app.command("pipeline")
def hermes_pipeline(
    name: Annotated[str, typer.Argument(help="Pipeline name to run")],
    input: Annotated[
        str,
        typer.Option("--input", "-i", help="JSON string of input data"),
    ] = "{}",
) -> None:
    """Run a named Hermes pipeline with optional JSON input."""
    import json

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.orchestrator import HermesOrchestrator
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    try:
        input_data: dict = json.loads(input)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON input: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    config = get_hermes_config()
    registry.build_all_agents(config=config)
    orchestrator = HermesOrchestrator(registry=registry, config=config)

    with console.status(f"[cyan]Running pipeline {name!r}...[/cyan]"):
        result = asyncio.run(orchestrator.run_pipeline(name, input_data))

    console.print_json(json.dumps(result, ensure_ascii=False, default=str))


@hermes_app.command("health")
def hermes_health() -> None:
    """Check Hermes system health: API key presence and registered agents."""
    import os

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    config = get_hermes_config()
    api_key = config.effective_api_key()

    table = Table(title="Hermes Health", show_lines=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status")

    if api_key:
        table.add_row("API key", "[green]set[/green]")
    else:
        table.add_row("API key", "[red]not set (set ANTHROPIC_API_KEY or HERMES_API_KEY)[/red]")

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=config)
    agent_names = registry.list_agents()
    table.add_row(
        "Registered agents",
        f"[green]{len(agent_names)}[/green]: {', '.join(agent_names)}" if agent_names
        else "[yellow]none[/yellow]",
    )

    console.print(table)


@app.command()
def menu() -> None:
    """Interactive menu (Arabic + English)."""
    _banner()
    while True:
        console.print(
            "\n[bold]Commands[/bold]\n"
            " [cyan]1[/cyan] · status\n"
            " [cyan]2[/cyan] · sector <name>\n"
            " [cyan]3[/cyan] · script <sector>\n"
            " [cyan]4[/cyan] · lead (interactive)\n"
            " [cyan]5[/cyan] · demo\n"
            " [cyan]0[/cyan] · exit"
        )
        choice = Prompt.ask("Choose", default="0")
        if choice == "0":
            break
        if choice == "1":
            status()
        elif choice == "2":
            s = Prompt.ask("Sector", default="healthcare")
            sector(s)
        elif choice == "3":
            s = Prompt.ask("Sector", default="technology")
            script(s)
        elif choice == "4":
            lead()
        elif choice == "5":
            demo()


if __name__ == "__main__":
    # Default to menu if no args
    import sys

    if len(sys.argv) == 1:
        menu()
    else:
        app()
