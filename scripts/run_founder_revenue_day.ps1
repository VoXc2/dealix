# Wrapper — canonical: run_founder_commercial_day.ps1 --with-business-now
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
& powershell -File "$Root\scripts\run_founder_commercial_day.ps1" -WithBusinessNow @args
