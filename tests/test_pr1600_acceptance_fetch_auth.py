from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ops" / "run_pr1600_live_full_acceptance.sh"


def _text() -> str:
    assert SCRIPT.is_file()
    return SCRIPT.read_text(encoding="utf-8")


def test_exact_head_fetch_uses_nonpersistent_github_cli_credentials() -> None:
    text = _text()
    assert "gh auth setup-git" not in text
    assert "credential.helper=!gh auth git-credential" in text
    assert 'GIT_REMOTE="https://github.com/${REPOSITORY}.git"' in text
    assert "git_repo()" in text
    assert 'git_repo fetch "$GIT_REMOTE"' in text


def test_exact_head_fetch_reproves_founder_and_private_repository() -> None:
    text = _text()
    assert "as_dealix gh auth status" in text
    assert "GH_AUTH_MISSING" in text
    assert "GH_FOUNDER_AUTH_MISMATCH" in text
    assert "REPOSITORY_NOT_PRIVATE" in text
    assert '[[ "$LOGIN" == "VoXc2" ]]' in text
    assert '[[ "$PRIVATE" == "true" ]]' in text


def test_exact_head_fetch_refreshes_main_and_pull_ref_at_both_boundaries() -> None:
    text = _text()
    main_fetch = 'git_repo fetch "$GIT_REMOTE" "+refs/heads/main:refs/remotes/origin/main" --force --quiet'
    pr_fetch = 'git_repo fetch "$GIT_REMOTE" "+refs/pull/$PR/head:$REF" --force --quiet'
    assert text.count(main_fetch) == 2
    assert text.count(pr_fetch) == 2
    assert "PR_HEAD_RACE" in text
    assert "PR_BEHIND_MAIN" in text
    assert "MAIN_MOVED" in text
    assert "PR_MOVED" in text


def test_exact_head_acceptance_still_forces_material_actions_off() -> None:
    text = _text()
    for token in (
        "PRODUCTION_GREEN=false",
        "DEALIX_EXTERNAL_SEND=0",
        "EMAIL_LIVE_SEND=0",
        "WHATSAPP_OUTBOUND=0",
        "PUBLIC_PUBLISH=0",
        "PAID_SPEND=0",
        "PAYMENT_EXECUTION=0",
        "PRODUCTION_MUTATION=0",
        "RAILWAY_STAGED_APPLY=0",
        "DNS_MUTATION=0",
        "DB_MUTATION=0",
        "SECRET_MUTATION=0",
        "CONTRACT_EXECUTION=0",
        "TENDER_EXECUTION=0",
    ):
        assert token in text

    for forbidden in (
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "git push --force",
        "gh auth setup-git",
    ):
        assert forbidden not in text
