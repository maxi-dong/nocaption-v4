#!/bin/bash
set -e

echo "Starting macOS local build..."

# 1. Download FFmpeg static build for macOS (Apple Silicon & Intel universal if possible)
echo "Downloading FFmpeg for macOS..."
if [ ! -f "ffmpeg" ]; then
    # Homebrew fallback or download static binary
    # We will use evermeet.cx or just brew
    if command -v brew &> /dev/null; then
        echo "Homebrew found. Extracting ffmpeg from homebrew..."
        brew install ffmpeg || true
        cp $(which ffmpeg) ./ffmpeg
    else
        echo "Error: Homebrew is required for local build to get FFmpeg."
        exit 1
    fi
fi

# 2. Setup Venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install pyinstaller Pillow

# 3. Build
echo "Building with PyInstaller..."
pyinstaller NOCAPTION_MAC.spec --clean -y

echo "Done! The app is in the dist/ folder."
