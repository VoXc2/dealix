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
skills_app = typer.Typer(no_args_is_help=True, help="Agent skills catalogue (T6a)")
verticals_app = typer.Typer(no_args_is_help=True, help="Industry verticals (T6c)")
saudi_app = typer.Typer(no_args_is_help=True, help="Saudi-gov data — Etimad/Maroof/Najiz/Tadawul/MISA (T6f)")
admin_app = typer.Typer(no_args_is_help=True, help="Enterprise admin operations (T6e)")

app.add_typer(leads_app, name="leads")
app.add_typer(webhooks_app, name="webhooks")
app.add_typer(onboarding_app, name="onboarding")
app.add_typer(support_app, name="support")
app.add_typer(audit_app, name="audit")
app.add_typer(skills_app, name="skills")
app.add_typer(verticals_app, name="verticals")
app.add_typer(saudi_app, name="saudi")
app.add_typer(admin_app, name="admin")


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


# ── skills (T6a) ──────────────────────────────────────────────────


@skills_app.command("list")
def skills_list() -> None:
    """List every registered Skill in skills/MANIFEST.yaml."""
    data = _request("GET", "/api/v1/skills")
    for s in data.get("skills", []):
        typer.echo(f"{s['id']:<28} {s['description']}")


@skills_app.command("get")
def skills_get(skill_id: str) -> None:
    """Pretty-print one skill's full record."""
    data = _request("GET", f"/api/v1/skills/{skill_id}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


# ── verticals (T6c) ───────────────────────────────────────────────


@verticals_app.command("list")
def verticals_list() -> None:
    data = _request("GET", "/api/v1/verticals")
    for v in data.get("verticals", []):
        typer.echo(f"{v['id']:<22} {v['label_en']}  ({v['pricing_default_plan']})")


@verticals_app.command("apply")
def verticals_apply(vertical_id: str) -> None:
    """Set the caller's tenant default vertical."""
    data = _request("POST", "/api/v1/verticals/apply", json={"vertical_id": vertical_id})
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


# ── saudi-gov (T6f) ───────────────────────────────────────────────


@saudi_app.command("tenders")
def saudi_tenders(
    sector: Annotated[str, typer.Option(help="filter by sector")] = "",
    region: Annotated[str, typer.Option(help="filter by region")] = "",
    keyword: Annotated[str, typer.Option(help="freeform query")] = "",
    page_size: Annotated[int, typer.Option(min=1, max=100)] = 25,
) -> None:
    """Search active Etimad tenders."""
    params: list[str] = [f"page_size={page_size}"]
    if sector:
        params.append(f"sector={sector}")
    if region:
        params.append(f"region={region}")
    if keyword:
        params.append(f"keyword={keyword}")
    qs = "?" + "&".join(params)
    data = _request("GET", f"/api/v1/saudi-gov/tenders{qs}")
    for t in data.get("tenders", []):
        typer.echo(
            f"{t['id']:<18} {t['submission_deadline']:<12} {t['agency']:<32} {t['title_ar']}"
        )


@saudi_app.command("maroof")
def saudi_maroof(cr_number: str) -> None:
    data = _request("GET", f"/api/v1/saudi-gov/maroof/{cr_number}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


@saudi_app.command("judicial")
def saudi_judicial(cr_number: str) -> None:
    data = _request("GET", f"/api/v1/saudi-gov/judicial/{cr_number}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


@saudi_app.command("tadawul")
def saudi_tadawul(symbol: str) -> None:
    data = _request("GET", f"/api/v1/saudi-gov/tadawul/{symbol}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


@saudi_app.command("misa")
def saudi_misa(licence_number: str) -> None:
    data = _request("GET", f"/api/v1/saudi-gov/misa/{licence_number}")
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


# ── admin (T6e) ───────────────────────────────────────────────────


@admin_app.command("byok-status")
def admin_byok_status() -> None:
    data = _request("GET", "/api/v1/admin/byok/status")
    typer.echo(json.dumps(data, indent=2))


@admin_app.command("audit-forward-status")
def admin_audit_forward_status() -> None:
    data = _request("GET", "/api/v1/admin/audit-forward/status")
    typer.echo(json.dumps(data, indent=2))


@admin_app.command("rotate-webhook")
def admin_rotate_webhook(tenant_id: str) -> None:
    """Rotate a tenant's webhook signing secret. The full secret is
    printed only this once."""
    data = _request(
        "POST", f"/api/v1/admin/tenant/{tenant_id}/webhook-keys/rotate"
    )
    typer.echo(json.dumps(data, indent=2))


@admin_app.command("sandbox-spin-up")
def admin_sandbox_spin_up(
    tenant_id: str,
    label: Annotated[str, typer.Option(help="sandbox label")] = "sandbox",
) -> None:
    """Clone a tenant's config into a fresh sandbox shadow tenant."""
    data = _request(
        "POST",
        "/api/v1/admin/sandbox/spin-up",
        json={"tenant_id": tenant_id, "label": label},
    )
    typer.echo(json.dumps(data, indent=2))


@admin_app.command("set-ip-allowlist")
def admin_set_ip_allowlist(
    tenant_id: str,
    cidrs: Annotated[str, typer.Argument(help="comma-separated CIDRs")],
) -> None:
    """Set a per-tenant IP allowlist. Pass an empty string + `clear-ip-allowlist`
    to remove."""
    parsed = [c.strip() for c in cidrs.split(",") if c.strip()]
    data = _request(
        "POST",
        f"/api/v1/admin/tenant/{tenant_id}/ip-allowlist",
        json={"cidrs": parsed},
    )
    typer.echo(json.dumps(data, indent=2))


@admin_app.command("clear-ip-allowlist")
def admin_clear_ip_allowlist(tenant_id: str) -> None:
    data = _request("DELETE", f"/api/v1/admin/tenant/{tenant_id}/ip-allowlist")
    typer.echo(json.dumps(data, indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
