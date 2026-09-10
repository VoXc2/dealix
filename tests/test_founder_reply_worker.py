from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "scripts" / "commercial" / "prepare_founder_whatsapp_reply_v1.py"


def test_founder_reply_worker_is_queue_friendly_and_side_effect_free() -> None:
    source = WORKER.read_text(encoding="utf-8")

    assert 'parser.add_argument("--input", required=True' in source
    assert 'parser.add_argument("--out", required=True' in source
    assert "prepare_founder_reply" in source
    assert "model_dump(mode=\"json\")" in source
    assert "os.chmod(temp_path, 0o600)" in source
    assert "temp_path.replace(output_path)" in source
    assert 'print("PROVIDER_EXECUTION_ALLOWED=0")' in source

    for forbidden in (
        "send_whatsapp_smart",
        "WhatsAppClient",
        "httpx",
        "requests",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
    ):
        assert forbidden not in source


def test_worker_stdout_does_not_print_customer_message_or_destination() -> None:
    source = WORKER.read_text(encoding="utf-8")
    print_lines = [line.strip() for line in source.splitlines() if line.strip().startswith("print(")]
    joined = "\n".join(print_lines)
    assert "message_text" not in joined
    assert "event.sender" not in joined
    assert "phone" not in joined.casefold()


def test_worker_entrypoint_imports_repo_package() -> None:
    result = subprocess.run([sys.executable, str(WORKER), "--help"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
