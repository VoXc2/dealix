# Railway + GitHub env readiness (reads current process env).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
py -3 scripts/railway_launch_env_check.py
exit $LASTEXITCODE
