"""
Row-Level Security (RLS) policies for PostgreSQL multi-tenant isolation.
سياسات أمان مستوى الصف (RLS) لعزل المستأجرين في PostgreSQL.

Enforces tenant isolation at the database level. Every query automatically
filters by tenant_id using the app.tenant_id session variable.

Usage: Run apply_rls() after Alembic migrations create the tables.
Ref: https://www.postgresql.org/docs/16/ddl-rowsecurity.html
"""

from __future__ import annotations

from typing import Any

from core.logging import get_logger
from db.session import get_session

log = get_logger(__name__)

# Maps table name -> policy expression using PostgreSQL current_setting
# The app sets app.tenant_id at the start of each request via middleware
RLS_POLICIES: dict[str, str] = {
    "leads": "tenant_id = current_setting('app.tenant_id', true)",
    "deals": "tenant_id = current_setting('app.tenant_id', true)",
    "contacts": "tenant_id = current_setting('app.tenant_id', true)",
    "invoices": "tenant_id = current_setting('app.tenant_id', true)",
    "proof_events": "tenant_id = current_setting('app.tenant_id', true)",
    "accounts": "tenant_id = current_setting('app.tenant_id', true)",
    "users": "tenant_id = current_setting('app.tenant_id', true)",
    "tenant_themes": "tenant_id = current_setting('app.tenant_id', true)",
    "audit_logs": "tenant_id = current_setting('app.tenant_id', true)",
    "roles": "tenant_id = current_setting('app.tenant_id', true)",
    "revenue_events": "tenant_id = current_setting('app.tenant_id', true)",
    "campaigns": "tenant_id = current_setting('app.tenant_id', true)",
    "outreach_queue": "tenant_id = current_setting('app.tenant_id', true)",
    "email_send_log": "tenant_id = current_setting('app.tenant_id', true)",
    "conversations": "tenant_id = current_setting('app.tenant_id', true)",
    "subscriptions": "tenant_id = current_setting('app.tenant_id', true)",
    "payments": "tenant_id = current_setting('app.tenant_id', true)",
    "proof_ledger": "tenant_id = current_setting('app.tenant_id', true)",
    "value_ledger": "tenant_id = current_setting('app.tenant_id', true)",
}

# Tables that should NOT have RLS (global/system tables)
RLS_EXEMPT_TABLES: list[str] = [
    "tenants",
    "alembic_version",
    "background_jobs",
]


async def apply_rls() -> None:
    """Enable RLS on all tenant-scoped tables and create policies.

    Idempotent: uses IF NOT EXISTS for policy creation.
    Should be called once after migrations, typically from a startup script.

    The app sets ``app.tenant_id`` at middleware level using:
        SET app.tenant_id = '<tenant_id>';

    Super admin users bypass RLS by not setting the session variable
    (set it to an empty string or skip the SET command).
    """
    async with get_session() as session:
        for table_name, policy_expr in RLS_POLICIES.items():
            sqls = [
                f"ALTER TABLE IF EXISTS {table_name} ENABLE ROW LEVEL SECURITY;",
                f"ALTER TABLE IF EXISTS {table_name} FORCE ROW LEVEL SECURITY;",
                (
                    f"DO $$ BEGIN "
                    f"IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = '{table_name}' AND policyname = 'tenant_isolation_policy') THEN "
                    f"CREATE POLICY tenant_isolation_policy ON {table_name} "
                    f"USING ({policy_expr}); "
                    f"END IF; "
                    f"END $$;"
                ),
                # Default-deny policy: if app.tenant_id is not set, no rows returned
                (
                    f"DO $$ BEGIN "
                    f"IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE tablename = '{table_name}' AND policyname = 'tenant_isolation_deny') THEN "
                    f"CREATE POLICY tenant_isolation_deny ON {table_name} "
                    f"AS RESTRICTIVE "
                    f"USING (current_setting('app.tenant_id', true) != ''); "
                    f"END IF; "
                    f"END $$;"
                ),
            ]

            for sql in sqls:
                try:
                    await session.execute(sql)
                except Exception as exc:
                    if "does not exist" in str(exc).lower():
                        log.warning(
                            "rls_table_not_found",
                            table=table_name,
                            error=str(exc),
                        )
                    else:
                        log.error(
                            "rls_policy_creation_failed",
                            table=table_name,
                            error=str(exc),
                        )
                        raise

            log.info("rls_enabled", table=table_name)

    log.info(
        "rls_apply_complete",
        tables_enabled=len(RLS_POLICIES),
        tables_exempt=len(RLS_EXEMPT_TABLES),
    )


async def disable_rls(table_name: str | None = None) -> None:
    """Disable RLS on specific table or all tenant tables."""
    tables = [table_name] if table_name else list(RLS_POLICIES.keys())

    async with get_session() as session:
        for tbl in tables:
            try:
                await session.execute(
                    f"ALTER TABLE IF EXISTS {tbl} DISABLE ROW LEVEL SECURITY;"
                )
                log.info("rls_disabled", table=tbl)
            except Exception as exc:
                log.warning("rls_disable_failed", table=tbl, error=str(exc))


async def verify_rls() -> dict[str, Any]:
    """Verify RLS is active on all tenant tables.

    Returns a dict with status for each table.
    """
    async with get_session() as session:
        tables = list(RLS_POLICIES.keys())
        status: dict[str, Any] = {"enabled": [], "disabled": [], "not_found": []}

        for table_name in tables:
            try:
                result = await session.execute(
                    "SELECT relrowsecurity FROM pg_class WHERE relname = :table_name",
                    {"table_name": table_name},
                )
                row = result.scalar_one_or_none()
                if row is True:
                    status["enabled"].append(table_name)
                elif row is False:
                    status["disabled"].append(table_name)
                else:
                    status["not_found"].append(table_name)
            except Exception:
                status["not_found"].append(table_name)

        return status
