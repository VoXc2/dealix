# Expand targeting (120 rows) + social 16w + weekly content drafts
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
if ($env:PY) { & $env:PY scripts/expand_commercial_operating_stack.py @args }
else { & py -3 scripts/expand_commercial_operating_stack.py @args }
exit $LASTEXITCODE
