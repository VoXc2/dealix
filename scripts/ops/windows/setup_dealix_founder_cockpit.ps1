param(
    [string]$ServerHost = "",
    [string]$BootstrapUser = "root",
    [string]$RemoteUser = "dealix",
    [string]$HostAlias = "dealix",
    [string]$Repo = "Dealix-sa/dealix",
    [string]$Branch = "ops/windows-vps-founder-cockpit-20260821",
    [switch]$SkipPackages,
    [switch]$SkipRemoteBootstrap
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Step([string]$Text) {
    Write-Host "`n===== $Text =====" -ForegroundColor Cyan
}

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found."
    }
}

function Ensure-WingetPackage([string]$Id) {
    if ($SkipPackages) { return }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Warning "winget is unavailable; skipping package installation for $Id"
        return
    }
    $installed = winget list --id $Id --exact --accept-source-agreements 2>$null | Out-String
    if ($LASTEXITCODE -eq 0 -and $installed -match [regex]::Escape($Id)) {
        Write-Host "$Id already installed"
        return
    }
    winget install --id $Id --exact --accept-package-agreements --accept-source-agreements --silent
}

Write-Step "DEALIX WINDOWS FOUNDER COCKPIT"
Write-Host "This script does not modify, stash, reset, commit, or push your current repository worktree."

Write-Step "LOCAL PACKAGE BASELINE"
Ensure-WingetPackage "Microsoft.VisualStudioCode"
Ensure-WingetPackage "Microsoft.WindowsTerminal"
Ensure-WingetPackage "Tailscale.Tailscale"

Require-Command ssh
Require-Command ssh-keygen
Require-Command gh

if ([string]::IsNullOrWhiteSpace($ServerHost)) {
    $ServerHost = Read-Host "Enter the VPS Tailscale IP/DNS name (preferred) or public IP"
}
if ([string]::IsNullOrWhiteSpace($ServerHost)) {
    throw "ServerHost cannot be empty."
}

Write-Step "GITHUB AUTH PROOF"
gh auth status
if ($LASTEXITCODE -ne 0) { throw "GitHub CLI is not authenticated." }

gh repo view $Repo --json nameWithOwner,defaultBranchRef,url | Out-Host
if ($LASTEXITCODE -ne 0) { throw "Cannot access $Repo through GitHub CLI." }

Write-Step "SSH KEY"
$sshDir = Join-Path $HOME ".ssh"
$keyPath = Join-Path $sshDir "dealix_ed25519"
$configPath = Join-Path $sshDir "config"
New-Item -ItemType Directory -Path $sshDir -Force | Out-Null

if (-not (Test-Path $keyPath)) {
    $emptyPassphrase = ""
    & ssh-keygen -t ed25519 -a 64 -f $keyPath -C "dealix-founder-cockpit" -N $emptyPassphrase
    if ($LASTEXITCODE -ne 0) { throw "ssh-keygen failed." }
} else {
    Write-Host "SSH key already exists: $keyPath"
}

$pubKey = (Get-Content "$keyPath.pub" -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($pubKey)) { throw "Public key is empty." }

Write-Step "INSTALL KEY ON VPS"
Write-Host "You may be asked for the existing VPS SSH password once. Do not paste it into ChatGPT."
$remoteInstall = @'
set -Eeuo pipefail
REMOTE_USER="$1"
PUBKEY="$2"
id "$REMOTE_USER" >/dev/null 2>&1 || { echo "BLOCKED: user $REMOTE_USER does not exist"; exit 2; }
HOME_DIR="$(getent passwd "$REMOTE_USER" | cut -d: -f6)"
install -d -m 700 -o "$REMOTE_USER" -g "$REMOTE_USER" "$HOME_DIR/.ssh"
touch "$HOME_DIR/.ssh/authorized_keys"
chown "$REMOTE_USER:$REMOTE_USER" "$HOME_DIR/.ssh/authorized_keys"
chmod 600 "$HOME_DIR/.ssh/authorized_keys"
if ! grep -Fqx "$PUBKEY" "$HOME_DIR/.ssh/authorized_keys"; then
  printf '%s\n' "$PUBKEY" >> "$HOME_DIR/.ssh/authorized_keys"
fi
echo "SSH_KEY_INSTALL=PASS"
'@

$remoteInstall | ssh "$BootstrapUser@$ServerHost" "bash -s -- '$RemoteUser' '$pubKey'"
if ($LASTEXITCODE -ne 0) { throw "Failed to install the SSH key on the VPS." }

if (-not $SkipRemoteBootstrap) {
    Write-Step "REMOTE VPS BOOTSTRAP"
    $tmp = New-TemporaryFile
    try {
        gh api -H "Accept: application/vnd.github.raw+json" "repos/$Repo/contents/scripts/ops/dealix_laptop_remote_bootstrap.sh?ref=$Branch" | Set-Content -Path $tmp -Encoding utf8
        if ($LASTEXITCODE -ne 0) { throw "Failed to fetch the remote bootstrap from GitHub." }
        Get-Content $tmp -Raw | ssh "$BootstrapUser@$ServerHost" "bash -s"
        if ($LASTEXITCODE -ne 0) { throw "Remote bootstrap failed." }
    }
    finally {
        Remove-Item $tmp -Force -ErrorAction SilentlyContinue
    }
}

Write-Step "SSH CONFIG"
if (Test-Path $configPath) {
    Copy-Item $configPath "$configPath.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
}

$currentConfig = if (Test-Path $configPath) { Get-Content $configPath -Raw } else { "" }
$begin = "# BEGIN DEALIX FOUNDER COCKPIT"
$end = "# END DEALIX FOUNDER COCKPIT"
$pattern = "(?s)" + [regex]::Escape($begin) + ".*?" + [regex]::Escape($end) + "\s*"
$currentConfig = [regex]::Replace($currentConfig, $pattern, "")
$keyForSsh = $keyPath -replace '\\','/'
$block = @"
$begin
Host $HostAlias
    HostName $ServerHost
    User $RemoteUser
    IdentityFile $keyForSsh
    IdentitiesOnly yes
    ServerAliveInterval 30
    ServerAliveCountMax 3
    TCPKeepAlive yes
    ConnectTimeout 10
$end
"@
Set-Content -Path $configPath -Value ($currentConfig.TrimEnd() + "`r`n`r`n" + $block.Trim() + "`r`n") -Encoding ascii

Write-Step "SSH CONNECTIVITY"
ssh -o BatchMode=yes "$HostAlias" "printf 'SSH_ALIAS=PASS\n'; whoami; hostname; uname -sr"
if ($LASTEXITCODE -ne 0) { throw "ssh $HostAlias failed after configuration." }

Write-Step "REMOTE VERIFICATION"
ssh "$HostAlias" @'
set -u
printf '%s\n' '--- identity ---'
whoami
hostname
printf '%s\n' '--- repo ---'
cd /opt/dealix/workspace/dealix 2>/dev/null || exit 3
git status -sb
git log -1 --oneline
printf '%s\n' '--- github ---'
gh auth status 2>&1 | sed -E 's/(Token:).*/\1 [REDACTED]/I' || true
printf '%s\n' '--- railway ---'
export PATH="$HOME/.railway/bin:$HOME/.local/bin:$PATH"
railway whoami 2>&1 || true
printf '%s\n' '--- docker ---'
docker ps --format 'table {{.Names}}\t{{.Status}}' 2>&1 | head -20 || true
printf '%s\n' '--- tmux ---'
tmux list-sessions 2>&1 || true
printf '%s\n' '--- ollama ---'
curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && echo OLLAMA_API=PASS || echo OLLAMA_API=DEGRADED
printf '%s\n' '--- memory ---'
free -h
'@

Write-Step "VS CODE REMOTE SSH"
if (Get-Command code -ErrorAction SilentlyContinue) {
    code --install-extension ms-vscode-remote.remote-ssh --force | Out-Host
    Write-Host "Open the server with: code --remote ssh-remote+$HostAlias /opt/dealix/workspace/dealix"
} else {
    Write-Warning "VS Code CLI is not currently on PATH. Open VS Code manually and use Remote-SSH -> $HostAlias."
}

Write-Step "SUCCESS"
Write-Host "ssh $HostAlias"
Write-Host "ssh $HostAlias -t 'tmux new -As dealix'"
Write-Host "The Linux tools (tmux/systemctl/docker/Railway) should now be run on the VPS, not in local PowerShell."
Write-Host "No local repository changes were modified by this bootstrap."
