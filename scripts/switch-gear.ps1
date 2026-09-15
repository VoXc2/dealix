# Dealix legacy Gear Switcher — governed migration HOLD
param([Parameter(Mandatory=$true)][ValidateSet(1,2,3)][int]$Gear)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "Dealix legacy gear switching is disabled for model/provider selection." -ForegroundColor Yellow
Write-Host "Reason: .env/.aider model mutation would bypass Omega V3 model/cost/data authority." -ForegroundColor Yellow
Write-Host "Use Company Operator -> Session Factory -> canonical broker -> OpenCode." -ForegroundColor Cyan
Write-Host "Automatic execution follows founder NO_DEEPSEEK policy and must HOLD when compliant capacity is unavailable." -ForegroundColor Cyan
Write-Host "Requested compatibility gear $Gear was NOT applied." -ForegroundColor DarkGray
Write-Host ""

# Compatibility parameter is intentionally accepted but no environment or
# Aider configuration is mutated. This helper must never become a second model
# router, cost authority, or OpenCode launch path.
exit 64
