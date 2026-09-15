# Dealix legacy Aider launcher — governed migration HOLD
param(
    [ValidateSet(1, 2, 3)]
    [int]$Gear = 1,

    [switch]$NoGit,
    [switch]$AutoCommit
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "Dealix legacy Aider launcher is disabled for autonomous model selection." -ForegroundColor Yellow
Write-Host "Reason: model/provider defaults in this helper are non-authoritative under Omega V3." -ForegroundColor Yellow
Write-Host "Use the canonical Dealix Company Operator -> Session Factory -> OpenCode path." -ForegroundColor Cyan
Write-Host "The canonical broker selects an allowed non-DeepSeek model from trusted cost/data/privacy authority." -ForegroundColor Cyan
Write-Host "If no compliant capacity exists, the governed path must HOLD rather than choose a provider here." -ForegroundColor Cyan
Write-Host ""

# Compatibility parameters are intentionally accepted but ignored. This file
# must never become a second model router or bypass the Session Factory.
exit 64
