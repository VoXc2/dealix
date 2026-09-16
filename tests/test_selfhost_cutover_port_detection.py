from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'ops' / 'selfhost_public_cutover.sh'


def test_public_port_detection_accepts_normal_ss_local_address_format() -> None:
    text = SCRIPT.read_text(encoding='utf-8')
    assert "ss -lntH | awk '{print $4}' | grep -Eq '(^|:)(80)$'" in text
    assert "ss -lntH | awk '{print $4}' | grep -Eq '(^|:)(443)$'" in text
    assert "(^|[[:space:]]):80" not in text
    assert "(^|[[:space:]]):443" not in text
