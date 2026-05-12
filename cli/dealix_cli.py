"""
dealix-cli — typer-based CLI for partners and operators.

Usage examples (assumes DEALIX_API_BASE + DEALIX_API_KEY env vars):

    dealix leads list
    dealix leads import path/to/leads.csv
    dealix webhooks tail
    dealix onboarding start --company "Acme" --email "ops@acme.sa"
    dealix support open --subject "..." --body "..." --email "..."
    dealix audit export --since 2026-04-01 > audit.csv

Install (after `feat(devx)` ships the Fern-generated SDK):

    pipx install 'dealix-sdk[cli]'
    # or, from this repo:
    pipx install -e ./
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Dealix CLI")
leads_app = typer.Typer(no_args_is_help=True, help="Lead operations")
webhooks_app = typer.Typer(no_args_is_help=True, help="Webhook utilities")
onboarding_app = typer.Typer(no_args_is_help=True, help="Tenant onboarding")
support_app = typer.Typer(no_args_is_help=True, help="Support tickets")
audit_app = typer.Typer(no_args_is_help=True, help="Audit log export")

app.add_typer(leads_app, name="leads")
app.add_typer(webhooks_app, name="webhooks")
app.add_typer(onboarding_app, name="onboarding")
app.add_typer(support_app, name="support")
app.add_typer(audit_app, name="audit")


def _base() -> str:
    return os.getenv("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")


def _headers() -> dict[str, str]:
    headers = {"accept": "application/json", "content-type": "application/json"}
    key = os.getenv("DEALIX_API_KEY", "").strip()
    if key:
        headers["X-API-Key"] = key
    bearer = os.getenv("DEALIX_BEARER_TOKEN", "").strip()
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    return headers


def _request(method: str, path: str, **kwargs: Any) -> Any:
    url = f"{_base()}{path}"
    with httpx.Client(timeout=30) as c:
        r = c.request(method, url, headers=_headers(), **kwargs)
        if r.status_code >= 400:
            typer.echo(f"error {r.status_code}: {r.text}", err=True)
            raise typer.Exit(code=1)
        if r.headers.get("content-type", "").startswith("application/json"):
            return r.json()
        return r.text


# ── leads ──────────────────────────────────────────────────────────


@leads_app.command("list")
def leads_list(
    limit: Annotated[int, typer.Option(min=1, max=200)] = 50,
) -> None:
    """List recent leads for the caller's tenant."""
    data = _request("GET", f"/api/v1/leads?limit={limit}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


@leads_app.command("import")
def leads_import(
    path: Annotated[Path, typer.Argument(exists=True, file_okay=True)],
) -> None:
    """Bulk-import leads from a CSV file (one POST per row)."""
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ok = err = 0
        for row in reader:
            try:
                _request("POST", "/api/v1/leads", json=row)
                ok += 1
            except typer.Exit:
                err += 1
        typer.echo(f"imported: {ok}, failed: {err}")


# ── webhooks ───────────────────────────────────────────────────────


@webhooks_app.command("tail")
def webhooks_tail() -> None:
    """Stream the realtime audit feed via SSE."""
    url = f"{_base()}/api/v1/realtime/stream"
    headers = _headers()
    headers["accept"] = "text/event-stream"
    typer.echo(f"# streaming {url}")
    with httpx.stream("GET", url, headers=headers, timeout=None) as r:
        for line in r.iter_lines():
            if line:
                typer.echo(line)


# ── onboarding ────────────────────────────────────────────────────


@onboarding_app.command("start")
def onboarding_start(
    company: Annotated[str, typer.Option()],
    email: Annotated[str, typer.Option()],
    name: Annotated[str, typer.Option()] = "Founder",
    locale: Annotated[str, typer.Option()] = "ar",
) -> None:
    """Begin a new tenant onboarding."""
    out = _request(
        "POST",
        "/api/v1/onboarding/start",
        json={"company": company, "email": email, "name": name, "locale": locale},
    )
    typer.echo(json.dumps(out, indent=2, ensure_ascii=False))


# ── support ───────────────────────────────────────────────────────


@support_app.command("open")
def support_open(
    subject: Annotated[str, typer.Option()],
    body: Annotated[str, typer.Option()],
    email: Annotated[str, typer.Option()],
    name: Annotated[str, typer.Option()] = "Partner",
) -> None:
    """Open a support ticket."""
    out = _request(
        "POST",
        "/api/v1/support/tickets",
        json={"subject": subject, "body": body, "email": email, "name": name},
    )
    typer.echo(json.dumps(out, indent=2, ensure_ascii=False))


# ── audit ─────────────────────────────────────────────────────────


@audit_app.command("export")
def audit_export(
    since: Annotated[str, typer.Option(help="ISO date (e.g. 2026-04-01)")] = "",
    until: Annotated[str, typer.Option(help="ISO date (e.g. 2026-05-01)")] = "",
    action: Annotated[str, typer.Option(help="filter by action")] = "",
) -> None:
    """Stream audit-log CSV to stdout."""
    params: list[str] = []
    if since:
        params.append(f"since={since}")
    if until:
        params.append(f"until={until}")
    if action:
        params.append(f"action={action}")
    qs = "?" + "&".join(params) if params else ""
    url = f"{_base()}/api/v1/audit-logs/export.csv{qs}"
    with httpx.stream("GET", url, headers=_headers(), timeout=None) as r:
        if r.status_code >= 400:
            typer.echo(f"error {r.status_code}", err=True)
            raise typer.Exit(code=1)
        for chunk in r.iter_text():
            sys.stdout.write(chunk)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
