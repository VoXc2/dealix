"""Guard the founder frontend from browser-exposed admin credentials."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPS_ADMIN = ROOT / "frontend" / "src" / "lib" / "opsAdmin.ts"
OPS_PROXY = (
    ROOT
    / "frontend"
    / "src"
    / "app"
    / "api"
    / "dealix-proxy"
    / "[...path]"
    / "route.ts"
)
DNS_RUNBOOK = ROOT / "docs" / "ops" / "DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
SYNC_ENV = ROOT / "scripts" / "sync_railway_generated_env.py"

PUBLIC_ADMIN_KEY = "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"


def test_ops_admin_helper_never_reads_public_admin_key() -> None:
    text = OPS_ADMIN.read_text(encoding="utf-8")
    assert PUBLIC_ADMIN_KEY not in text
    assert 'localStorage.getItem(LS_KEY)' in text
    assert 'if (typeof window === "undefined") return ""' in text


def test_server_proxy_keeps_admin_key_server_side() -> None:
    text = OPS_PROXY.read_text(encoding="utf-8")
    assert 'process.env.DEALIX_ADMIN_API_KEY || ""' in text
    assert 'process.env.DEALIX_API_KEY || ""' in text
    assert '"X-Admin-API-Key": ADMIN_KEY' in text
    assert '"X-API-Key": SERVICE_KEY' in text
    assert PUBLIC_ADMIN_KEY not in text


def test_sync_removes_legacy_public_admin_key() -> None:
    text = SYNC_ENV.read_text(encoding="utf-8")
    assert f'public_admin_key = "{PUBLIC_ADMIN_KEY}"' in text
    assert 'FE:REMOVE_' in text


def test_dns_runbook_forbids_public_admin_key_assignment() -> None:
    text = DNS_RUNBOOK.read_text(encoding="utf-8")
    assert f"ممنوع:\n\n```text\n{PUBLIC_ADMIN_KEY}=..." in text
    assert "DEALIX_ADMIN_API_KEY=<server-side only>" in text
    assert "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1" in text
