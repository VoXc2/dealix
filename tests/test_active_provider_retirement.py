from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def test_active_provider_retirement_verifier_passes() -> None:
    proc=subprocess.run(["python3", str(ROOT/"scripts/ops/verify_active_provider_retirement.py")], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ACTIVE_PROVIDER_RETIREMENT=PASS" in proc.stdout
    assert "MIGRATION_PROOF_REFERENCES=PRESERVED" in proc.stdout
