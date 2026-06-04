#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pyinstaller \
  --noconfirm \
  --windowed \
  --name "NOCAPTION V2" \
  --icon "assets/icons/nocaption_v2.icns" \
  nocaption_tk_v2.py
