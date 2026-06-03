# Unified founder day (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
py -3 scripts/run_dealix_unified_founder_day.py @args
exit $LASTEXITCODE
