from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "dealix_openship_private_pilot.sh"
DOC = ROOT / "docs" / "ops" / "DEALIX_OPENSHIP_PRIVATE_STAGING_PILOT.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_pilot_forces_bare_mode_and_requires_true_readiness() -> None:
    text = read(SCRIPT)
    assert "up --bare" in text
    assert "wait_for_ready" in text
    assert "validate_status_json" in text
    assert "verify_direct_health" in text
    assert "rc != 0 && rc != 124" in text
    assert "both must pass strict CLI/API health" in text


def test_pilot_rejects_all_non_loopback_control_listeners() -> None:
    text = read(SCRIPT)
    assert "non_loopback_control_listener_present" in text
    assert "unsafe_control_listener=" in text
    assert "127.0.0.1:3001" in text
    assert r"\[::1\]:4000" in text
    assert "control_listener_owner_is_dealix" in text


def test_installer_is_not_downloaded_or_executed() -> None:
    text = read(SCRIPT)
    assert 'OPENSHIP_VERSION="0.4.8"' in text
    assert "get.openship.io" not in text
    assert "bun.sh/install" not in text
    assert "curl -fsSL" not in text
    assert "PINNED_PREINSTALLED" in text
    assert "Governed pilot refuses mutable network installers" in text


def test_pilot_does_not_authorize_public_or_production_mutation() -> None:
    text = read(SCRIPT)
    forbidden = (
        "--public-url",
        "--managed-edge",
        " up --compose",
        "railway up",
        "railway redeploy",
        "gh pr merge",
        "git push origin main",
        "openship domain add",
    )
    for token in forbidden:
        assert token not in text

    assert "PRODUCTION_MUTATION=false" in text
    assert "PUBLIC_DOMAIN=false" in text
    assert "DNS_MUTATION=false" in text
    assert "PRODUCTION_SECRET_COPY=false" in text
    assert "EXTERNAL_SEND=false" in text
    assert "PAYMENT=false" in text


def test_mcp_guard_requires_explicit_auth_denial() -> None:
    text = read(SCRIPT)
    assert "/api/mcp" in text
    assert "401|403" in text
    assert "MCP_ANONYMOUS_ACCESS=EXPLICITLY_DENIED" in text
    assert "BLOCKED_OR_UNAVAILABLE" not in text
    assert "mcp_transport_rc=" in text


def test_mcp_failure_stops_and_verifies_rollback() -> None:
    text = read(SCRIPT)
    assert "fail_closed_stop" in text
    assert "verified_stop" in text
    assert "FAIL_CLOSED_ROLLBACK=PASS" in text
    assert "OPENSHIP_STOP=LISTENERS_REMAIN" in text


def test_synthetic_fixture_is_root_staged_then_atomically_published() -> None:
    text = read(SCRIPT)
    assert 'mktemp -d "$PILOT_ROOT/.synthetic-stage-' in text
    assert "synthetic staging directory must be root-owned" in text
    assert 'mv -- "$SYNTH_STAGE" "$app_dir"' in text
    assert 'chown -R "$RUN_USER:$RUN_USER" "$app_dir"' in text
    assert 'synthetic-app-$STAMP' in text
    assert 'synthetic-app"' not in text


def test_full_private_pilot_stops_before_real_deployment() -> None:
    text = read(SCRIPT)
    start = text.index("full-private-pilot)")
    body = text[start : text.index(";;", start)]
    assert "preflight" in body
    assert "verify_cli" in body
    assert "start_private" in body
    assert "mcp_auth_guard" in body
    assert "scaffold_synthetic" in body
    assert "openship init" not in body
    assert "openship deploy" not in body


def test_status_requires_local_api_context_and_fixed_ports() -> None:
    text = read(SCRIPT)
    assert 'int(ports.get("api") or 0) != 4000' in text
    assert 'int(ports.get("dashboard") or 0) != 3001' in text
    assert 'parsed.hostname not in {"127.0.0.1", "localhost", "::1"}' in text
    assert "OPENSHIP_STATUS=HEALTHY" in text


def test_documentation_keeps_railway_as_production_core() -> None:
    text = read(DOC)
    assert "Railway remains the production core." in text
    assert "Issue #1171" in text
    assert "OpenShip is a private staging / preview pilot" in text
    assert "attaching `dealix.me`" in text
    assert "production database credentials or secrets" in text
