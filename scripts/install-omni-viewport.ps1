# Install Utah Omni-Viewport into Cursor (Windows).
# Links the repo extension folder into %USERPROFILE%\.cursor\extensions\
# so edits in the repo are live after Reload Window.

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "extensions\utah-omni-viewport"
$target = Join-Path $env:USERPROFILE ".cursor\extensions\utahmosphere.utah-omni-viewport-1.0.0"

if (-not (Test-Path $source)) {
    Write-Error "Extension source not found: $source"
}

$extDir = Split-Path $target -Parent
if (-not (Test-Path $extDir)) {
    New-Item -ItemType Directory -Path $extDir -Force | Out-Null
}

if (Test-Path $target) {
    Remove-Item $target -Force -Recurse
}

New-Item -ItemType Junction -Path $target -Target $source | Out-Null
Write-Host "Installed: $target -> $source"
Write-Host "Reload Cursor (Ctrl+Shift+P -> Developer: Reload Window), then open Omni-Viewport in the activity bar."
