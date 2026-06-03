# Push main using GitHub CLI token (fixes Windows GCM stale PAT vs bearer header)
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$ahead = git rev-list --count origin/main..HEAD 2>$null
if (-not $ahead -or [int]$ahead -eq 0) {
    Write-Host "PUSH_MAIN=SKIP (nothing ahead of origin/main)"
    exit 0
}

Write-Host "Commits ahead: $ahead"
$token = (gh auth token 2>$null)
if (-not $token) {
    Write-Host "Run: gh auth login -h github.com -p https -s repo"
    exit 1
}
$token = $token.Trim()
$env:GIT_TERMINAL_PROMPT = "0"
$env:GH_TOKEN = $token

gh auth refresh -h github.com -s repo 2>$null | Out-Null
gh auth setup-git 2>$null | Out-Null

# Attempt 1: disable credential helper + bearer header (bypasses stale GCM PAT)
git -c credential.helper= -c "http.extraheader=AUTHORIZATION: bearer $token" push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK"
    exit 0
}

# Attempt 2: embed token in remote URL (no credential helper)
$remoteUrl = "https://x-access-token:${token}@github.com/VoXc2/dealix.git"
git -c credential.helper= push $remoteUrl HEAD:main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK (token remote)"
    exit 0
}

# Attempt 3: gh-configured credential helper
git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK (gh credential helper)"
    exit 0
}

Write-Host "PUSH_MAIN=trying GitHub API fallback..."
py -3 scripts/push_via_gh_api.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "PUSH_MAIN=OK (via GitHub API)"
    exit 0
}

Write-Host "PUSH_MAIN=FAIL - git pull --rebase origin main then retry"
Write-Host "  gh auth refresh -h github.com -s repo"
exit 1
