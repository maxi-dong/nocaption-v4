#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

pyinstaller \
  --noconfirm \
  --windowed \
  --name "NOCAPTION" \
  nocaption_tk.py

# Result:
# dist/NOCAPTION.app
