# download_ffmpeg.ps1
# Downloads FFmpeg release essentials from gyan.dev and extracts ffmpeg.exe / ffprobe.exe
# into the current directory for bundling with PyInstaller.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$FFmpegUrl  = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$ZipFile    = "ffmpeg-release-essentials.zip"
$ExtractDir = "ffmpeg"

Write-Host "=== FFmpeg Downloader for NOCAPTION V4 ===" -ForegroundColor Cyan

# ── 1. Download ──────────────────────────────────────────────────────────────
if (Test-Path $ZipFile) {
    Write-Host "  [skip] $ZipFile already exists, using cached copy."
} else {
    Write-Host "  [download] Downloading FFmpeg from gyan.dev ..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $FFmpegUrl -OutFile $ZipFile -UseBasicParsing
    Write-Host "  [done] Download complete."
}

# ── 2. Extract ───────────────────────────────────────────────────────────────
if (Test-Path $ExtractDir) {
    Write-Host "  [clean] Removing old extraction directory ..."
    Remove-Item -Recurse -Force $ExtractDir
}

Write-Host "  [extract] Extracting archive ..."
Expand-Archive -Path $ZipFile -DestinationPath $ExtractDir -Force

# ── 3. Locate and copy binaries ──────────────────────────────────────────────
# The archive contains a top-level folder like ffmpeg-7.0-essentials_build/bin/
$BinDir = Get-ChildItem -Path $ExtractDir -Recurse -Directory -Filter "bin" | Select-Object -First 1

if (-not $BinDir) {
    Write-Error "Could not locate bin/ directory inside the extracted archive."
    exit 1
}

Write-Host "  [copy] Found binaries in: $($BinDir.FullName)"

Copy-Item -Path (Join-Path $BinDir.FullName "ffmpeg.exe")  -Destination "." -Force
Copy-Item -Path (Join-Path $BinDir.FullName "ffprobe.exe") -Destination "." -Force

# Verify the copies landed
if ((Test-Path "ffmpeg.exe") -and (Test-Path "ffprobe.exe")) {
    Write-Host "  [ok] ffmpeg.exe  -> $(Resolve-Path 'ffmpeg.exe')" -ForegroundColor Green
    Write-Host "  [ok] ffprobe.exe -> $(Resolve-Path 'ffprobe.exe')" -ForegroundColor Green
} else {
    Write-Error "Failed to copy one or both executables."
    exit 1
}

# ── 4. Cleanup ───────────────────────────────────────────────────────────────
Write-Host "  [clean] Removing temporary files ..."
Remove-Item -Recurse -Force $ExtractDir
Remove-Item -Force $ZipFile

Write-Host ""
Write-Host "FFmpeg is ready. You can now run build.bat to build the application." -ForegroundColor Green
