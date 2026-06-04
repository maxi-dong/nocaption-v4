@echo off
REM ============================================================================
REM  build.bat – Build script for NOCAPTION V4 (Windows)
REM  Run this from the nocaption_app\windows\ directory.
REM ============================================================================
setlocal enabledelayedexpansion

echo.
echo ===================================================
echo   NOCAPTION V4 – Windows Build Script
echo ===================================================
echo.

REM ── 1. Check Python ────────────────────────────────────────────────────────
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not on PATH.
    echo         Please install Python 3.10+ from https://python.org
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [INFO] Found %%v

REM ── 2. Virtual environment ────────────────────────────────────────────────
if not exist "venv" (
    echo [INFO] Creating virtual environment ...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        exit /b 1
    )
    echo [OK]   Virtual environment created.
) else (
    echo [INFO] Virtual environment already exists, reusing.
)

echo [INFO] Activating virtual environment ...
call venv\Scripts\activate.bat

REM ── 3. Install requirements ───────────────────────────────────────────────
echo [INFO] Installing requirements ...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] pip install failed.
    exit /b 1
)
echo [OK]   Requirements installed.

REM ── 4. Check FFmpeg ────────────────────────────────────────────────────────
if not exist "ffmpeg.exe" (
    echo.
    echo [WARNING] ffmpeg.exe not found in the current directory.
    echo           Please run the following command first:
    echo.
    echo               powershell -ExecutionPolicy Bypass -File download_ffmpeg.ps1
    echo.
    exit /b 1
)

if not exist "ffprobe.exe" (
    echo.
    echo [WARNING] ffprobe.exe not found in the current directory.
    echo           Please run download_ffmpeg.ps1 first.
    echo.
    exit /b 1
)

echo [OK]   ffmpeg.exe and ffprobe.exe found.

REM ── 5. Check icon ─────────────────────────────────────────────────────────
if exist "icon.ico" (
    echo [OK]   icon.ico found – will be embedded in the executable.
) else (
    echo [INFO] icon.ico not found – building without a custom icon.
)

REM ── 6. Run PyInstaller ────────────────────────────────────────────────────
echo.
echo [BUILD] Running PyInstaller ...
echo.
pyinstaller NOCAPTION_WIN.spec --noconfirm
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller build failed. See output above for details.
    exit /b 1
)

REM ── 7. Done ────────────────────────────────────────────────────────────────
echo.
echo ===================================================
echo   BUILD SUCCESSFUL
echo ===================================================
echo.
echo   Output folder:
echo       %cd%\dist\NOCAPTION V4\
echo.
echo   To create an installer, open installer.iss with
echo   Inno Setup and compile it.
echo.

endlocal
