#!/usr/bin/env python3
"""Verify OpenCode V1 control plane config compat and L5 deny boundaries."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "opencode.json"

# required patterns must exist with deny or ask (for sudo etc)
REQUIRED = [
    ("git push origin main", ["deny"]),
    ("git push --force", ["deny"]),
    ("gh pr merge", ["deny"]),
    ("railway up", ["deny"]),
    ("alembic upgrade head", ["deny"]),
    ("kubectl delete", ["deny"]),
    ("cat *.env", ["deny"]),
    ("cat /home/dealix/.config/dealix-secrets", ["deny"]),
    ("sudo", ["deny","ask"]),
    ("railway delete", ["deny"]),
    ("aws route53", ["deny"]),
    ("gcloud dns", ["deny"]),
    ("gh secret", ["deny"]),
    ("aws secretsmanager", ["deny"]),
]

def main() -> int:
    if not CFG.is_file():
        print(f"FAIL: missing {CFG}"); return 2
    try:
        data = json.loads(CFG.read_text())
    except Exception as e:
        print(f"FAIL: invalid JSON: {e}"); return 2
    ok = True
    def fail(msg):
        nonlocal ok
        print(f"FAIL: {msg}")
        ok = False
    if "permissions" in data:
        fail("found deprecated top-level 'permissions' (V2) — expected 'permission'")
    if "permission" not in data:
        fail("missing top-level 'permission' (V1 required)")
    else:
        perm = data["permission"]
        if not isinstance(perm, dict):
            fail("'permission' must be object")
        else:
            if "bash" not in perm:
                fail("permission missing 'bash' (V1 expects 'bash', not 'shell')")
            if "shell" in perm:
                fail("found deprecated 'shell' inside permission — use 'bash'")
            bash = perm.get("bash", {})
            if isinstance(bash, dict):
                for pattern, allowed in REQUIRED:
                    found=False
                    for k,v in bash.items():
                        if pattern in k and v in allowed:
                            found=True
                            break
                    if not found:
                        fail(f"missing required pattern '{pattern}' with {allowed} (bash keys: {list(bash.keys())[:5]}...)")
                if perm.get("edit") != "allow":
                    fail(f"builder 'edit' should be 'allow', got {perm.get('edit')}")
            elif bash == "deny":
                fail("builder bash is deny — would block L4 repo execute")
    if "provider" not in data:
        fail("missing provider")
    elif "ollama" not in data["provider"]:
        fail("provider missing ollama definitions")
    if "model" not in data:
        fail("missing model")
    raw = CFG.read_text()
    if '"permissions"' in raw:
        fail('raw file contains \'"permissions"\' string — V2 leftover')
    if ok:
        print("PASS: OpenCode V1 config valid, L5 denies preserved, provider/model preserved")
        return 0
    else:
        print("FAIL: OpenCode config validation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
