param(
    [string]$Model = "deepseek/deepseek-chat",
    [string]$Prompt = "..\prompts\DEALIX_FOUNDER_MASTER_PROMPT.md"
)

$ErrorActionPreference = "Continue"

$root = Resolve-Path "$PSScriptRoot\.."
$v2 = Join-Path $root "dealix-v2"

if (!(Test-Path $v2)) {
    Write-Host "dealix-v2 not found." -ForegroundColor Red
    exit 1
}

Set-Location $v2

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " DEALIX AIDER v5 - SAFE MODE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Model: $Model" -ForegroundColor Gray
Write-Host " Scope: dealix-v2 only" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan

$args1 = @(
    "--model", $Model,
    "--skip-sanity-check-repo",
    "--subtree-only",
    "--map-tokens", "1024",
    "--aiderignore", "..\.aiderignore",
    "--read", $Prompt
)

& aider @args1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Aider safe mode failed. Trying --no-git fallback..." -ForegroundColor Yellow
    & aider --model $Model --no-git --map-tokens 1024 --read $Prompt
}