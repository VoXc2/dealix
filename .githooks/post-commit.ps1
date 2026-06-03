#!/usr/bin/env pwsh
# Auto-push current branch after commit (PowerShell)
$branch = (git rev-parse --abbrev-ref HEAD) -replace '\r',''
if ($branch) {
  git push --no-verify origin $branch > $null 2>&1
}
