<#
Creates a backup ZIP of common development/test artifacts and (optionally)
removes them from the repository. Safe to run from the project root.

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\cleanup_and_remove.ps1

The script will create `cleanup-backup.zip` in the repo root and then prompt
for confirmation before deleting files. Type YES (all-caps) to proceed.
#>

param(
    [string]$BackupPath = "cleanup-backup.zip"
)

Set-StrictMode -Version Latest

$root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $root

$candidates = @(
    'tools',
    'app\test_inproc.py',
    'app\test_preview.py',
    'app\test_e2e.py',
    'out_sample.png',
    'preview_docx.png',
    'preview_multipage.png',
    'preview_output.png',
    'preview_test.png',
    'redacted_multipage.pdf',
    'redacted_sample.png',
    'redacted_test.pdf',
    'redacted_test_doc.pdf',
    'redacted_test_img.png',
    'redacted_test_sensitive.docx',
    'sample.png',
    'test.pdf',
    'test_doc_for_preview.docx',
    'test_sensitive.docx'
)

$toArchive = @()
foreach ($p in $candidates) {
    if (Test-Path $p) { $toArchive += $p }
}

if ($toArchive.Count -eq 0) {
    Write-Output "No candidate files or directories found to archive. Nothing to do."
    exit 0
}

Write-Output "Creating backup archive: $BackupPath"
try {
    if (Test-Path $BackupPath) { Remove-Item $BackupPath -Force -ErrorAction SilentlyContinue }
    Compress-Archive -Path $toArchive -DestinationPath $BackupPath -Force -ErrorAction Stop
    Write-Output "Archive created: $BackupPath"
} catch {
    Write-Error "Failed to create archive: $_"
    exit 2
}

Write-Output "The following paths were added to the archive and are candidates for deletion:" 
$toArchive | ForEach-Object { Write-Output " - $_" }

$confirm = Read-Host "Type YES to permanently delete these files (case-sensitive) or press Enter to abort"
if ($confirm -ne 'YES') {
    Write-Output "Aborted by user. Backup saved at: $BackupPath"
    exit 0
}

Write-Output "Removing candidate files..."
foreach ($p in $toArchive) {
    try {
        if (Test-Path $p) {
            Remove-Item $p -Recurse -Force -ErrorAction Stop
            Write-Output "Deleted: $p"
        }
    } catch {
        Write-Warning "Failed to delete $p: $_"
    }
}

Write-Output "Cleanup complete. Keep the backup if you need to restore files: $BackupPath"
