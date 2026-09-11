from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_command_room_v1.sh"


def test_installer_adds_reply_worker_without_second_scheduler_or_live_send() -> None:
    source = INSTALLER.read_text(encoding="utf-8")

    assert 'REPLY_WRAPPER="$BIN/dealix-founder-whatsapp-reply"' in source
    assert "prepare_founder_whatsapp_reply_v1.py" in source
    assert "founder_whatsapp_reply_path" in source
    assert "SCHEDULER_CREATED=false" in source
    assert "PER_CHANNEL_DAEMON_CREATED=false" in source
    assert "systemctl enable" not in source
    assert "systemctl start" not in source
    assert "sudo -u \"$RUN_USER\" -H git -C \"$REPO\" rev-parse --is-inside-work-tree" in source
    assert '[[ -d "$REPO/.git" ]]' not in source

    assert source.count("export DEALIX_EXTERNAL_SEND=0") >= 2
    assert source.count("export WHATSAPP_ALLOW_LIVE_SEND=0") >= 2
    assert "export LOCAL_LLM_PROVIDER=vllm" in source
    assert "export VLLM_BASE_URL=http://127.0.0.1:11999/v1" in source
    assert "export VLLM_MODEL=dealix-local" in source
    assert "WHATSAPP_ALLOW_LIVE_SEND=1" not in source
    assert "DEALIX_EXTERNAL_SEND=1" not in source
