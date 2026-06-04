#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pyinstaller \
  --noconfirm \
  --windowed \
  --name "NOCAPTION" \
  --icon "assets/icons/nocaption_v1.icns" \
  nocaption_tk.py
