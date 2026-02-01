<#
Push repository to GitHub (interactive)

Usage (from project root):
  powershell -ExecutionPolicy Bypass -File .\scripts\push_to_github.ps1

This script will:
- Ask for the remote GitHub repo URL (e.g. https://github.com/you/coriolis.git)
- Optionally initialize the repo if missing, create/overwrite 'origin' remote
- Commit all current changes with a default message (editable)
- Push to the chosen branch (defaults to current branch or 'main')

Notes:
- You must have git installed and authenticated (SSH agent or credential helper).
- The script does NOT create a GitHub repository account for you; create the remote repo on GitHub first.
#>

Set-StrictMode -Version Latest

# Ensure running from repo root
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $scriptDir\..\

function Run-Git([string]$args) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'git'
    $psi.Arguments = $args
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $p = [System.Diagnostics.Process]::Start($psi)
    $out = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    return @{ ExitCode = $p.ExitCode; Out = $out; Err = $err }
}

# Ask for remote URL
$remoteUrl = Read-Host "Enter remote GitHub repo URL (https://github.com/you/repo.git)"
if ([string]::IsNullOrWhiteSpace($remoteUrl)) { Write-Error "Remote URL required. Aborting."; exit 1 }

# Determine current branch
$branchRes = Run-Git 'rev-parse --abbrev-ref HEAD'
$branch = 'main'
if ($branchRes.ExitCode -eq 0 -and -not [string]::IsNullOrWhiteSpace($branchRes.Out)) { $branch = $branchRes.Out.Trim() }
$branchInput = Read-Host "Target branch to push (press Enter to use '$branch')"
if (-not [string]::IsNullOrWhiteSpace($branchInput)) { $branch = $branchInput }

# Initialize repo if needed
if (-not (Test-Path .git)) {
    Write-Output "No .git found — initializing repository"
    $init = Run-Git 'init'
    if ($init.ExitCode -ne 0) { Write-Error "git init failed: $($init.Err)"; exit 2 }
}

# Configure origin remote
$remoteCheck = Run-Git 'remote get-url origin'
if ($remoteCheck.ExitCode -eq 0) {
    Write-Output "Existing 'origin' remote found: $($remoteCheck.Out.Trim())"
    $confirm = Read-Host "Overwrite origin remote with $remoteUrl ? Type YES to overwrite"
    if ($confirm -eq 'YES') {
        $setUrl = Run-Git "remote set-url origin $remoteUrl"
        if ($setUrl.ExitCode -ne 0) { Write-Error "Failed to set remote URL: $($setUrl.Err)"; exit 3 }
    } else {
        Write-Output "Keeping existing origin."
    }
} else {
    $add = Run-Git "remote add origin $remoteUrl"
    if ($add.ExitCode -ne 0) { Write-Error "Failed to add origin remote: $($add.Err)"; exit 4 }
}

# Stage all changes
$st = Run-Git 'add -A'
if ($st.ExitCode -ne 0) { Write-Error "git add failed: $($st.Err)"; exit 5 }

# Commit if there are changes
$status = Run-Git 'status --porcelain'
if (-not [string]::IsNullOrWhiteSpace($status.Out)) {
    $msg = Read-Host "Commit message (press Enter for default)"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = 'chore: commit repository changes before push' }
    $cm = Run-Git "commit -m \"$msg\""
    if ($cm.ExitCode -ne 0) {
        Write-Error "git commit failed (maybe nothing to commit): $($cm.Err)"
    } else {
        Write-Output "Committed changes: $msg"
    }
} else {
    Write-Output "No changes to commit."
}

# Push
Write-Output "Pushing to origin/$branch ..."
$push = Run-Git "push -u origin $branch"
if ($push.ExitCode -ne 0) { Write-Error "git push failed: $($push.Err)"; exit 6 }
Write-Output "Push completed successfully."
