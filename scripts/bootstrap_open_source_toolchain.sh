#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL_DIR="$ROOT/tooling/oss"
MISE_BIN="${MISE_BIN:-$HOME/.local/bin/mise}"
UV_BIN="${UV_BIN:-$HOME/.local/bin/uv}"

if [[ ! -x "$MISE_BIN" ]]; then
  echo "mise is missing. Install the reviewed mise release first; bootstrap will not curl|sh implicitly." >&2
  exit 2
fi
if [[ ! -x "$UV_BIN" ]]; then
  echo "uv is missing at $UV_BIN" >&2
  exit 2
fi

"$MISE_BIN" trust "$TOOL_DIR/mise.toml" >/dev/null
MISE_LOCKED=1 "$MISE_BIN" -C "$TOOL_DIR" install

while IFS= read -r spec; do
  [[ -z "$spec" || "$spec" == \#* ]] && continue
  "$UV_BIN" tool install --force "$spec"
done < "$TOOL_DIR/uv-tools.txt"

python3 "$ROOT/scripts/verify_open_source_toolchain.py" --check-installed
printf "OPEN_SOURCE_TOOLCHAIN_BOOTSTRAP=PASS\n"
printf "No services were started, enabled, exposed, or deployed.\n"
